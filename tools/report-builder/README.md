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

## 학교 양식(전남대 REPORT)으로 만들기 — 3회차부터

`templates/cnu_report_template.docx`(학교 레포트 양식)의 표지·머리글 로고·쪽 번호·목차 필드를 그대로 쓰고 본문만 채운다.

```bash
python3 tools/report-builder/make_cnu.py labs/NN_.../report/content.js out.docx   # 빌드 → PDF → 목차 쪽 번호 채워 재빌드
python3 tools/report-builder/check.py out.pdf out.labels.json <참고문헌 수>
```

- `content.js`의 `cover.info`는 양식 표 칸 이름(과목명·담당교수·제출일·학과·학번·성명)을 키로 쓴다. 빈 문자열이면 빈칸으로 둔다.
- 참고문헌은 `refs`를 `{키: 문장}` 객체로 두고 본문에 `[Z1]`처럼 키로 인용한다. 처음 인용된 순서대로 [1], [2] …가 매겨진다. 정의만 있고 인용이 없거나 그 반대면 빌드가 멈춘다.
- 참고문헌 문장은 양식 형식을 따른다: (온라인) 사이트명, 「제목」, 주소, 참고날짜 / (논문) 저자, 「제목」, 게재지 권(호), 출판사, 연도, 쪽.
- `photos` 블록은 `h`(사진 높이 cm)와 항목별 `sub`((a) 설명)를 받는다. 사진 줄과 캡션은 나뉘지 않는 칸 하나짜리 표에 들어가 쪽이 바뀌어도 같이 움직인다.
- 목차 쪽 번호는 LibreOffice 미리보기 기준이다. 맑은 고딕 대신 대체 글꼴로 계산되므로 한글에서 열면 쪽이 1~2쪽 달라질 수 있다. 한글에서 목차 쪽 번호를 다시 확인한다.
- 양식은 표지를 0쪽, 목차를 1쪽으로 센다. 20쪽 제한은 표지 포함 PDF 쪽수로 본다.
