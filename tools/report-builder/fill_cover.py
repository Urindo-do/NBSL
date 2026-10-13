"""제출용 표지 채우기: 저장소의 빈칸 보고서(docx)에서 표지 정보 표만 조별 구조로 바꿔 새 파일로 저장한다.

python3 fill_cover.py <빈칸 보고서.docx> <cover.local.json> <제출본.docx>

- 본문·목차·그림은 건드리지 않는다. 바뀌는 것은 표지 정보 표(document.xml 안 '담당교수' 표) 하나뿐이다.
- cover.local.json 예:
  {"rows": [["과 목 명", "생체역학.조직공학및실습"], ["담당교수", "..."], ["실 습 일", "2026년 10월 1일"],
            ["제 출 일", "2026년 10월 8일"], ["조", "5조"], ["조 원 1", "..."], ...]}
- 조원 이름이 들어가므로 cover.local.json과 결과 파일(*_표지완성.docx)은 .gitignore로 저장소에서 빠진다.
  저장소에는 빈칸 보고서만 올린다.
"""
import copy, json, sys, zipfile
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
q = lambda t: '{%s}%s' % (W, t)
XML = '{http://www.w3.org/XML/1998/namespace}space'

src, cover_json, dst = sys.argv[1:4]
rows_in = json.load(open(cover_json, encoding='utf-8'))['rows']
ROW_H, C2 = 440, 3700  # 9줄이 표지 테두리 안에 들어가는 높이, 과목명이 한 줄에 들어가는 값 칸 폭

zin = zipfile.ZipFile(src)
root = etree.fromstring(zin.read('word/document.xml'))
tbl = next(e for e in root.iter(q('tbl')) if '담당교수' in ''.join(x.text or '' for x in e.iter(q('t'))))
old = tbl.findall(q('tr')); proto = copy.deepcopy(old[0])
for r in old:
    tbl.remove(r)
# 양식 표(6줄)보다 줄이 3개 많아 Word·한글에서는 표가 2쪽으로 밀린다(LibreOffice 미리보기에서는 안 보임).
# 3회차 제출본에서 Word로 직접 맞춘 것과 같게 표 바로 앞 빈 문단을 4개 지운다 (29개 → 25개).
BLANKS_TO_DROP = 4
prev, dropped = tbl.getprevious(), 0
while prev is not None and dropped < BLANKS_TO_DROP and prev.tag == q('p') \
        and not ''.join(x.text or '' for x in prev.iter(q('t'))) and not prev.findall('.//' + q('drawing')):
    nxt = prev.getprevious(); prev.getparent().remove(prev); prev = nxt; dropped += 1
assert dropped == BLANKS_TO_DROP, dropped
for g, w in zip(tbl.find(q('tblGrid')).findall(q('gridCol')), (2835, C2)):
    g.set(q('w'), str(w))
for label, val in rows_in:
    r = copy.deepcopy(proto)
    r.find(q('trPr')).find(q('trHeight')).set(q('val'), str(ROW_H))
    tc1, tc2 = r.findall(q('tc'))
    ts = list(tc1.iter(q('t'))); ts[0].text = '•'; ts[1].text = label + ':'
    tc2.find(q('tcPr')).find(q('tcW')).set(q('w'), str(C2))
    p = tc2.find(q('p')); p.find(q('pPr')).find(q('jc')).set(q('val'), 'left')
    run = etree.SubElement(p, q('r')); rp = etree.SubElement(run, q('rPr'))
    f = etree.SubElement(rp, q('rFonts'))
    for k in ('ascii', 'eastAsia', 'hAnsi'):
        f.set(q(k), '맑은 고딕')
    etree.SubElement(rp, q('sz')).set(q('val'), '24'); etree.SubElement(rp, q('szCs')).set(q('val'), '24')
    t = etree.SubElement(run, q('t')); t.set(XML, 'preserve'); t.text = ' ' + val
    tbl.append(r)
out = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
    for it in zin.infolist():
        zout.writestr(it, out if it.filename == 'word/document.xml' else zin.read(it.filename))
print('ok', dst, len(rows_in), '줄')
