"""제출 보고서 검증: python check.py <report.pdf> <report.labels.json> <참고문헌 개수>
- 초안 표시([수업] [보충] ❓ 📷 ** {f: {t:) 0개인지
- 그림/표 번호가 모두 본문에 있는지
- 참고문헌 [1]~[N]이 본문에서 모두 인용되는지
- 쪽수 출력 (20쪽 이하여야 함)
"""
import json, re, subprocess, sys
pdf, labels, nref = sys.argv[1], sys.argv[2], int(sys.argv[3])
t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
pages = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1)
body = t[:t.rfind('참고문헌')]
marks = {m: t.count(m) for m in ['[수업]', '[보충]', '❓', '📷', '**', '{f:', '{t:']}
missing_labels = [v for v in json.load(open(labels)).values() if v not in body]
cited = {int(x) for x in re.findall(r'\[(\d+)\]', body)}
uncited = [i for i in range(1, nref + 1) if i not in cited]
print('쪽수:', pages)
print('초안 표시:', {k: v for k, v in marks.items() if v} or '없음')
print('본문에 없는 그림/표 번호:', missing_labels or '없음')
print('본문에서 인용 안 된 참고문헌:', uncited or '없음')
ok = int(pages) <= 20 and not any(marks.values()) and not missing_labels and not uncited
print('PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
