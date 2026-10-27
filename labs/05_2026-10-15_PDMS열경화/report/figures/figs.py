# lab05 원리 그림 5개 — python3 figs.py  → 이 파일 옆에 f_*.png 저장
# 근거: ../../README.md (출처 키 D2~D6, J1, V1, R1). 계산 그림은 식을 그림 안에 밝힌다.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))
fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = '#222'; BLUE = '#2f6db5'; LIQ = '#cfe3f7'; GRAY = '#bbb'; RED = '#c0392b'
GREEN = '#2e8b57'; YEL = '#f4d03f'; PURP = '#7d3c98'; ORG = '#e67e22'; MOLD = '#f5cba7'; PD = '#d6eaf8'


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.6, ms=12, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw))


def box(ax, x, y, w, h, txt, fc='white', ec=INK, fs=9.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')


def save(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------- 1. 재료: 가교 반응(개념도) + 점도·비중(MSDS 값) ----------
fig = plt.figure(figsize=(9.6, 3.8))
ax = fig.add_axes([0.0, 0.0, 0.58, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 8.6); ax.axis('off')
ax.text(0.1, 8.1, '(a) 베이스와 경화제가 이어지는 반응 (개념도)', fontsize=10.5)
for y in (6.5, 4.9):
    ax.plot([0.4, 3.0], [y, y], color=BLUE, lw=3)
    ax.add_patch(Circle((3.15, y), 0.18, fc=GREEN, ec=INK))
ax.text(1.7, 7.0, '베이스: 비닐 말단 사슬', fontsize=8.5, color=BLUE, ha='center')
ax.text(3.15, 4.25, '비닐기', fontsize=8, color=GREEN, ha='center')
ax.plot([4.3, 4.3], [4.5, 7.0], color=PURP, lw=3)
for y in (6.5, 4.9):
    ax.add_patch(Circle((4.3, y), 0.18, fc=YEL, ec=INK))
ax.text(4.3, 7.35, '경화제: Si–H 사슬', fontsize=8.5, color=PURP, ha='center')
ax.text(3.72, 5.55, '+', fontsize=13, ha='center')
arrow(ax, 5.2, 5.7, 6.5, 5.7, c=RED, lw=2.0)
ax.text(5.85, 6.05, '백금 촉매\n+ 열', ha='center', fontsize=8.5, color=RED)
xs = np.linspace(7.0, 9.4, 4); ys = np.linspace(4.5, 6.9, 4)
for x in xs:
    ax.plot([x, x], [ys[0], ys[-1]], color=PURP, lw=2)
for y in ys:
    ax.plot([xs[0], xs[-1]], [y, y], color=BLUE, lw=2)
for x in xs:
    for y in ys:
        ax.add_patch(Circle((x, y), 0.1, fc=RED, ec=RED))
ax.text(8.2, 3.9, '그물 구조 (가교망)', ha='center', fontsize=9)
ax.text(0.4, 2.6, '섞는 순간 반응이 시작되고, 열을 가하면 빨라진다.\n경화제가 고르게 퍼져야 그물이 고르게 생긴다.', fontsize=9, linespacing=1.6)
ax.text(0.4, 1.2, '빨간 점: Si–H와 비닐기가 이어진 자리', fontsize=8.5, color=RED)
# (b) 점도 비교 (로그축)
ax2 = fig.add_axes([0.66, 0.24, 0.31, 0.62])
names = ['베이스', '경화제', '섞은 뒤']
vals = [5000, 110, 3500]
bars = ax2.bar(names, vals, color=[BLUE, YEL, GRAY], ec=INK)
ax2.set_yscale('log'); ax2.set_ylim(50, 20000)
for i, v in enumerate(vals):
    ax2.text(i, v * 1.25, f'{v:,}', ha='center', fontsize=9)
ax2.set_ylabel('점도 (cSt, 섞은 뒤는 cps)', fontsize=8.5)
ax2.tick_params(labelsize=9); ax2.spines[['top', 'right']].set_visible(False)
ax2.text(0.5, 9000, '약 45배', ha='center', fontsize=9, color=RED)
fig.text(0.62, 0.05, '(b) 제조사 자료의 점도 (측정값 아님, 로그 눈금)', fontsize=10)
save(fig, 'f_material')


# ---------- 2. 저울 영점: 용기 무게 빼기 ----------
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.3))
titles = ['(a) 디쉬를 올리고 영점', '(b) 디쉬를 꺼내면', '(c) 베이스를 담아 다시 올리면']
reads = ['0.0000 g', '−2.5485 g', '+15.0 g 부근']
notes = ['기준 = 디쉬를 올린 상태', '기준보다 디쉬 무게만큼 가벼움', '디쉬 무게는 상쇄, 베이스만 표시']
for k, ax in enumerate(axs):
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
    ax.text(5, 9.4, titles[k], ha='center', fontsize=10)
    ax.add_patch(Rectangle((1.2, 1.6), 7.6, 1.0, fc='#eee', ec=INK))       # 저울 몸체
    ax.add_patch(Rectangle((3.2, 2.6), 3.6, 0.25, fc=GRAY, ec=INK))        # 접시
    ax.add_patch(Rectangle((2.0, 6.2), 6.0, 1.5, fc='#111', ec=INK))       # 표시창
    ax.text(5, 6.95, reads[k], ha='center', va='center', color='white', fontsize=12)
    if k in (0, 2):
        ax.add_patch(Polygon([[3.6, 2.85], [6.4, 2.85], [6.9, 4.0], [3.1, 4.0]], fc='white', ec=INK))
    if k == 1:
        ax.add_patch(Polygon([[7.6, 3.3], [9.4, 3.3], [9.8, 4.2], [7.2, 4.2]], fc='white', ec=INK, ls='--'))
        arrow(ax, 6.3, 3.4, 7.3, 3.7, c=RED)
    if k == 2:
        ax.add_patch(Polygon([[3.75, 3.0], [6.25, 3.0], [6.6, 3.7], [3.4, 3.7]], fc=BLUE, ec=None, alpha=0.6))
    ax.text(5, 0.7, notes[k], ha='center', fontsize=8.8)
fig.text(0.5, -0.04, '(b)의 값은 실습 사진 판독값, (c)는 우리 조 목표량 15 g을 넣었을 때의 개념 표시', ha='center', fontsize=9, color='#555')
save(fig, 'f_tare')


# ---------- 3. 진공 탈포: 보일 + 스토크스 (계산 개형) ----------
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.8))
P = np.linspace(0.1, 1.0, 200)          # 절대압 (bar)
a1.plot(1 - P, 1 / P, color=BLUE, lw=2)
a1.set_xlabel('뺀 압력 (bar, 게이지 눈금의 크기)', fontsize=9)
a1.set_ylabel('기포 부피 (대기압일 때 = 1)', fontsize=9)
a1.set_title('(a) 보일 법칙: 기포 부피 V ∝ 1/P', fontsize=10)
a1.text(0.02, 8.6, '기포 하나의 부피 변화.\n혼합물 전체는 원래 부피의\n약 2~6배까지 부풀었다\n가라앉는다 [V1]', fontsize=8.3, color=ORG, va='top', linespacing=1.4)
a1.set_xlim(0, 0.92); a1.set_ylim(0, 11)
a1.tick_params(labelsize=8.5); a1.spines[['top', 'right']].set_visible(False)
g = 9.81; rho = 1030; mu = 3.5          # PDMS 비중 1.03, 섞은 뒤 3500 cps = 3.5 Pa·s
d = np.linspace(50, 600, 200) * 1e-6
for fac, lab, c in ((1.0, '대기압 그대로', GRAY), (10 ** (1 / 3), '절대압 0.1 bar (부피 10배)', BLUE)):
    r = d / 2 * fac
    v = 2 / 9 * rho * g * r ** 2 / mu
    t = 5e-3 / v / 60
    a2.plot(d * 1e6, t, color=c, lw=2, label=lab)
a2.set_yscale('log'); a2.set_ylim(0.1, 300)
a2.set_xlabel('대기압에서의 기포 지름 (µm)', fontsize=9)
a2.set_ylabel('5 mm 떠오르는 시간 (분)', fontsize=9)
a2.set_title('(b) 스토크스 법칙: v = 2ρgr² / 9μ', fontsize=10)
a2.legend(fontsize=8.5, frameon=False)
a2.tick_params(labelsize=8.5); a2.spines[['top', 'right']].set_visible(False)
fig.text(0.5, -0.05, '계산 개형, 측정값 아님. μ = 3.5 Pa·s, ρ = 1.03 g/cm³ (제조사 자료), 깊이 5 mm 가정. 부피 10배 → 반지름 2.15배 → 속도 4.64배',
         ha='center', fontsize=8.8, color='#555')
fig.tight_layout()
save(fig, 'f_degas')


# ---------- 4. 몰드 복제 (단면 개념도) ----------
fig, axs = plt.subplots(1, 4, figsize=(9.6, 2.9))
heads = ['(a) 준비된 몰드', '(b) PDMS 붓기', '(c) 가열해 굳히기', '(d) 떼어 내면']


def mold(ax):
    ax.add_patch(Rectangle((0.5, 1.0), 9.0, 1.0, fc=MOLD, ec=INK))
    for x in np.arange(1.3, 9.0, 1.5):
        ax.add_patch(Rectangle((x, 2.0), 0.7, 1.8, fc=MOLD, ec=INK))


for k, ax in enumerate(axs):
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis('off')
    ax.text(5, 7.4, heads[k], ha='center', fontsize=10)
    if k < 3:
        mold(ax)
    if k == 1 or k == 2:
        ax.add_patch(Rectangle((0.5, 2.0), 9.0, 3.4, fc=PD, ec=INK, zorder=0))
    if k == 1:
        ax.add_patch(Circle((2.65, 2.35), 0.3, fc='white', ec=RED, zorder=3))
        ax.add_patch(Circle((5.65, 2.3), 0.25, fc='white', ec=RED, zorder=3))
        ax.text(5, 0.25, '돌기 사이에 기포가 갇히기 쉽다', ha='center', fontsize=8.5, color=RED)
    if k == 2:
        for x in (2.5, 5, 7.5):
            ax.annotate('', xy=(x, 0.95), xytext=(x, 0.1), arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.5))
        ax.text(5, 5.8, '가교가 진행', ha='center', fontsize=8.5)
    if k == 3:
        ax.add_patch(Rectangle((0.5, 2.5), 9.0, 3.4, fc=PD, ec=INK))
        for x in np.arange(1.3, 9.0, 1.5):
            ax.add_patch(Rectangle((x, 2.5), 0.7, 1.8, fc='white', ec=INK))
        ax.text(5, 1.3, '돌기 → 구멍 (반대 모양)', ha='center', fontsize=8.5)
fig.text(0.5, -0.03, '개념도. 몰드 하나로 여러 번 복제할 수 있다 [R1]. 우리 조는 (c) 단계까지 했다.', ha='center', fontsize=9, color='#555')
save(fig, 'f_mold')


# ---------- 5. 경화 온도와 시간·영률 (문헌값) ----------
fig, (b1, b2) = plt.subplots(1, 2, figsize=(9.6, 3.6))
T_now = [25, 100, 150]; t_now = [48 * 60, 35, 10]
T_old = [25, 100, 125, 150]; t_old = [48 * 60, 45, 20, 10]
b1.plot(T_now, t_now, 'o-', color=BLUE, lw=2, label='현재 제품 페이지 [D3]')
b1.plot(T_old, t_old, 's--', color=ORG, lw=1.5, label='2007년판 자료 [D6]')
b1.set_yscale('log'); b1.set_ylim(5, 5000)
b1.set_xlabel('경화 온도 (°C)', fontsize=9); b1.set_ylabel('경화 시간 (분, 로그 눈금)', fontsize=9)
b1.set_title('(a) 온도가 높을수록 빨리 굳는다', fontsize=10)
for T, t, s in ((25, 48 * 60, '48 h'), (100, 35, '35 min'), (150, 10, '10 min')):
    b1.text(T + 3, t * 1.15, s, fontsize=8.5, color=BLUE)
b1.legend(fontsize=8, frameon=False, loc='upper right')
b1.tick_params(labelsize=8.5); b1.spines[['top', 'right']].set_visible(False)
b2.plot([25, 200], [1.32, 2.97], color=GREEN, lw=2)
b2.plot([25, 200], [1.32, 2.97], 'o', color=GREEN)
b2.text(30, 1.45, '1.32 MPa', fontsize=8.5); b2.text(150, 3.05, '2.97 MPa', fontsize=8.5)
b2.set_xlim(0, 220); b2.set_ylim(0, 3.6)
b2.set_xlabel('경화 온도 (°C)', fontsize=9); b2.set_ylabel('영률 (MPa)', fontsize=9)
b2.set_title('(b) 높은 온도로 굳히면 더 단단해진다 [J1]', fontsize=10)
b2.tick_params(labelsize=8.5); b2.spines[['top', 'right']].set_visible(False)
fig.text(0.5, -0.04, '문헌값. (b)는 25~200 °C 범위 양 끝값을 이은 선 (논문은 이 범위에서 거의 직선으로 보고), 측정값 아님',
         ha='center', fontsize=8.8, color='#555')
fig.tight_layout()
save(fig, 'f_curetemp')
print('done')
