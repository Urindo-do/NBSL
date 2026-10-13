"""목차(고정 텍스트) 쪽 번호를 렌더된 PDF 기준으로 고친다. 쪽 번호 = PDF 쪽 - 1 (표지는 번호 없음).
python3 toc.py <in.docx> <rendered.pdf> <out.docx>
"""
import re, subprocess, sys
from docx import Document

src, pdf, dst = sys.argv[1:4]
n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
pages = [subprocess.run(['pdftotext', '-layout', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
         for i in range(1, n + 1)]
norm = lambda s: re.sub(r'\s+', '', s)
d = Document(src)
changed = 0
for p in d.paragraphs[14:46]:
    runs = p.runs
    if len(runs) < 2 or '\t' not in p.text:
        continue
    title = runs[0].text.strip()
    hit = None
    for i in range(2, n):          # 0: 표지, 1: 목차 → 본문은 index 2부터
        for line in pages[i].splitlines():
            if norm(line).startswith(norm(title)) and len(norm(line)) <= len(norm(title)) + 2:
                hit = i; break
        if hit is not None:
            break
    assert hit is not None, title
    num = str(hit)                 # index i = PDF 쪽 i+1 → 쪽 번호 i
    t = runs[1]._r.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')[-1]
    if t.text != num:
        t.text = num; changed += 1
    print(f'{title:28s} {num}')
d.save(dst)
print('changed', changed)
