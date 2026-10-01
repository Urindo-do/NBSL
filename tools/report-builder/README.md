# report-builder — 제출 보고서(docx) 생성 도구

회차별 `labs/NN_.../report/content.js`(본문)를 한글에서 열 수 있는 `.docx`로 만든다.
한글에서 열어 "다른 이름으로 저장 → .hwp"로 제출한다.

## 회차 폴더 구성

```
labs/NN_YYYY-MM-DD_주제/
├── README.md            ← 기록 초안 (근거)
├── images/              ← 사진 (content.js에서 ../images/로 참조)
└── report/
    ├── content.js       ← 보고서 본문 (lab02 것을 복사해서 고쳐 쓴다)
    ├── figures/figs.py  ← 원리 그림 생성 스크립트 → figures/*.png
    ├── lab NN_..._보고서.docx
    └── lab NN_..._보고서_미리보기.pdf
```

## 실행 (Claude 작업공간 기준)

```bash
python3 labs/NN_.../report/figures/figs.py                     # 원리 그림
NODE_PATH=$(npm root -g) node tools/report-builder/build.js labs/NN_.../report/content.js out.docx
soffice --headless --convert-to pdf out.docx                   # 미리보기
python3 tools/report-builder/check.py out.pdf out.labels.json <참고문헌 수>
```

## content.js 블록

| t | 필드 | 설명 |
|---|---|---|
| `h1` `h2` `h3` | `x` | 제목. 번호(1. / 1.1 / 1.1.1)는 자동 |
| `p` | `x` | 문단. `{f:key}` → "그림 3-1", `{t:key}` → "표 1-1" 자동 치환 |
| `ol` | `items` | 번호 목록 (사용 순서에만) |
| `fig` | `key img w cap` | 원리 그림 1개 (가로 w px) |
| `photos` | `items[{key img cap}]` | 사진 1~2장 (2장이면 나란히) |
| `table` | `key cap cols head rows` | 표. `cols`는 DXA 폭, 합계 ≤ 9638 |

- 그림 번호는 장(h1)마다 1부터: 그림 3-1, 3-2 …
- 참고문헌은 `refs` 배열 순서가 [1], [2] … 본문에 `[n]`으로 직접 쓴다.
- 표지 칸(과목명·조·조원)은 `[   ]` 빈칸으로 두고 주인이 한글에서 채운다.

## 서식 (한글 기준)

A4, 여백 위 20 / 아래 15 / 좌우 20 mm, 본문 함초롬바탕 11pt 줄 간격 160%, 제목 함초롬돋움,
그림 캡션은 아래·표 캡션은 위, 쪽 번호 아래 가운데(표지 제외).
