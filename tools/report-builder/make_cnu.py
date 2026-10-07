"""학교 양식 보고서 한 번에 만들기: 빌드 → PDF → 목차 쪽 번호 채워 다시 빌드 → PDF

python3 make_cnu.py <content.js> <out.docx> [양식.docx]

양식을 주지 않으면 templates/cnu_report_template.docx를 쓴다.
쪽 번호는 LibreOffice 미리보기 기준이다(맑은 고딕이 없으면 대체 글꼴로 계산되어 한글·워드에서 1~2쪽 달라질 수 있다).
양식은 표지를 0쪽, 목차를 1쪽으로 센다(pgNumType start=0).
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
content, out = sys.argv[1], sys.argv[2]
tpl = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, 'templates', 'cnu_report_template.docx')
stem = re.sub(r'\.docx$', '', out)
outdir = os.path.dirname(os.path.abspath(out))


def build(extra=()):
    subprocess.run([sys.executable, os.path.join(HERE, 'build_cnu.py'), content, tpl, out, *extra], check=True)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, out], check=True,
                   capture_output=True)


def page_texts(pdf):
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    return [subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), '-layout', pdf, '-'], capture_output=True,
                           text=True).stdout for i in range(1, n + 1)]


def norm(s):
    return re.sub(r'\s+', '', s)


build()
heads = json.load(open(stem + '.headings.json'))
pages = page_texts(stem + '.pdf')
pmap = {}
for h in heads:
    key = norm(h['text'])
    for i, t in enumerate(pages[2:], start=3):  # 표지(1), 목차(2) 건너뜀
        if any(norm(line).startswith(key) for line in t.splitlines()):
            pmap[h['bm']] = i - 1  # 표지 = 0쪽
            break
    else:
        print('쪽을 못 찾은 제목:', h['text'])
json.dump(pmap, open(stem + '.pages.json', 'w'), indent=1)
build(['--pages', stem + '.pages.json'])
# 두 번째 빌드에서 쪽이 바뀌지 않았는지 확인
pages2 = page_texts(stem + '.pdf')
print('PDF 쪽수:', len(pages2), '(표지 포함) / 목차 항목', len(pmap), '/', len(heads))
