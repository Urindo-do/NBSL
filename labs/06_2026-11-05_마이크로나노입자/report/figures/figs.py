# lab06 원리 그림 4개 — python3 figs.py  → 이 파일 옆에 f_*.png 저장
# 근거: ../../README.md (출처 키 P2·P3·A1·G1·G2·F1~F3). 모두 개념도이며 측정값이 아니다.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse, FancyArrowPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))
fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = '#222'; BLUE = '#2f6db5'; LIQ = '#cfe3f7'; GRAY = '#999'; RED = '#c0392b'
GREEN = '#2e8b57'; YEL = '#f4d03f'; ORG = '#e67e22'; ALG = '#e8a0a8'; GEL = '#d4a017'


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.6, ms=12, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw))


def box(ax, x, y, w, h, txt, fc='white', ec=INK, fs=9.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')


def save(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def jet(ax, x, y_top, y_break, wobble, lam, w=0.16, rng=None):
    """노즐 아래 줄기: 위는 곧고 아래로 갈수록 잘록해진다."""
    ys = np.linspace(y_top, y_break, 300)
    grow = (y_top - ys) / (y_top - y_break)
    if rng is None:
        r = w * (1 - 0.8 * grow ** 2 * (0.5 + 0.5 * np.cos(2 * np.pi * ys / lam)))
    else:
        r = w * (1 - 0.8 * grow ** 2 * wobble(ys))
    ax.fill_betweenx(ys, x - r, x + r, color=ALG, ec=None)


# ---------- 1. PPF: 진동 없이 vs 진동을 줄 때 ----------
fig, axs = plt.subplots(1, 2, figsize=(9.6, 5.0))
rng = np.random.default_rng(3)
JX = 1.6
for ax in axs:
    ax.set_xlim(0, 6.4); ax.set_ylim(0, 10.6); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((JX - 0.45, 8.9), 0.9, 0.7, fc='#ccc', ec=INK))
    ax.add_patch(Rectangle((JX - 0.12, 8.6), 0.24, 0.3, fc='#ccc', ec=INK))
    ax.add_patch(Rectangle((0.2, 0.2), 2.8, 1.2, fc=LIQ, ec=INK))
    ax.text(1.6, 0.8, 'CaCl$_2$ 용액', ha='center', va='center', fontsize=8.5)
ax = axs[0]
ax.text(0.0, 10.2, '(a) 진동 없이 흘릴 때', fontsize=10.5)
mix = lambda ys: 0.5 + 0.5 * (0.6 * np.cos(2 * np.pi * ys / 0.9) + 0.4 * np.cos(2 * np.pi * ys / 1.55 + 1.0))
jet(ax, JX, 8.6, 6.5, mix, None, rng=rng)
sizes = [0.22, 0.12, 0.30, 0.09, 0.18, 0.26, 0.11, 0.2]
y = 6.15
for i, s_ in enumerate(sizes):
    y -= s_
    ax.add_patch(Circle((JX + (0.05 if i % 2 else -0.05), y), s_, fc=ALG, ec='#b05'))
    y -= s_ + 0.12 + 0.18 * rng.random()
ax.text(2.6, 4.8, '여러 파장의 흔들림이\n무작위로 섞여\n끊어지는 간격과\n방울 크기가 제각각', fontsize=8.8, va='center')
ax = axs[1]
ax.text(0.0, 10.2, '(b) 노즐을 주파수 f로 흔들 때', fontsize=10.5)
lam = 0.55
jet(ax, JX, 8.6, 7.0, None, lam)
for i in range(9):
    ax.add_patch(Circle((JX, 6.6 - i * lam), 0.18, fc=ALG, ec='#b05'))
ax.annotate('', xy=(JX + 0.45, 6.6), xytext=(JX + 0.45, 6.6 - lam),
            arrowprops=dict(arrowstyle='<->', color=BLUE, lw=1.2, shrinkA=0, shrinkB=0))
ax.text(JX + 0.6, 6.6 - lam / 2, 'λ = v / f  (v: 줄기 속도)', va='center', fontsize=8.8, color=BLUE)
ax.annotate('', xy=(JX + 0.75, 9.25), xytext=(JX + 1.35, 9.25),
            arrowprops=dict(arrowstyle='<->', color=RED, lw=1.4, shrinkA=0, shrinkB=0))
ax.text(JX + 1.5, 9.25, '진동 (주파수 f)', color=RED, fontsize=8.8, va='center')
ax.text(2.6, 4.0, '새긴 물결이 먼저 자라\n한 주기에 방울 하나\n→ 모두 같은 크기\n\n방울 부피 = Q / f\nd = (6Q / πf)$^{1/3}$\n(Q: 유량)', fontsize=8.8, va='center')
save(fig, 'f_ppf')


# ---------- 2. 알지네이트 egg-box 가교 (개념도) ----------
fig = plt.figure(figsize=(9.0, 3.3))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 18); ax.set_ylim(0, 6.6); ax.axis('off')
ax.text(0.2, 6.2, '(a) 알지네이트 방울이 CaCl$_2$ 용액에 닿으면', fontsize=10.5)
ax.add_patch(Circle((1.8, 3.6), 1.0, fc=ALG, ec='#b05'))
ax.text(1.8, 3.6, '알지네이트\n(−)', ha='center', va='center', fontsize=8.5)
for (x, y) in [(0.5, 2.0), (3.3, 2.2), (3.4, 4.9), (0.4, 5.0), (1.9, 1.7), (1.9, 5.4)]:
    ax.add_patch(Circle((x, y), 0.22, fc=YEL, ec=INK)); ax.text(x, y, '+', ha='center', va='center', fontsize=8)
ax.text(1.8, 0.8, 'Ca$^{2+}$가 표면부터 들어와\n즉시 굳은 껍질을 만든다', ha='center', fontsize=8.5)
arrow(ax, 4.4, 3.6, 5.6, 3.6, c=RED, lw=2.0)
ax.text(6.0, 6.2, '(b) egg-box 모델: Ca$^{2+}$가 이웃 사슬의 G 블록 사이에 끼어 두 사슬을 잇는다', fontsize=10.5)
xs = np.linspace(6.5, 17.0, 300)
top = 4.1 + 0.42 * np.sin((xs - 6.5) * 2 * np.pi / 2.1)
bot = 2.5 - 0.42 * np.sin((xs - 6.5) * 2 * np.pi / 2.1)
ax.plot(xs, top, color=GREEN, lw=3); ax.plot(xs, bot, color=GREEN, lw=3)
for i in range(5):
    cx = 6.5 + 2.1 * (i + 0.75)
    ax.add_patch(Circle((cx, 3.3), 0.24, fc=YEL, ec=INK)); ax.text(cx, 3.3, '+', ha='center', va='center', fontsize=8)
ax.text(17.2, 4.1, 'G 블록\n사슬 1', fontsize=8, va='center', color=GREEN)
ax.text(17.2, 2.5, 'G 블록\n사슬 2', fontsize=8, va='center', color=GREEN)
ax.text(11.75, 1.2, '음전하를 띤 G 블록의 굽은 자리가 달걀판처럼 Ca$^{2+}$(2가 양이온)를 감싼다 — 이온 가교 (개념도)', ha='center', fontsize=8.5)
save(fig, 'f_eggbox')


# ---------- 3. 젤라틴 나노입자 전 과정 흐름 ----------
fig = plt.figure(figsize=(9.4, 2.6))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 19); ax.set_ylim(0, 5.2); ax.axis('off')
steps = [('① 1차 탈용매화', '아세톤을 한 번에\n고분자량만 침전', True),
         ('② 재용해', '침전을 다시\n물에 녹임', False),
         ('③ pH 조절', '산성으로 맞춰\n표면 양전하', False),
         ('④ 2차 탈용매화', '아세톤을 천천히\n나노입자 형성', False),
         ('⑤ 가교', '글루타르알데하이드\n형태 고정', False),
         ('⑥ 정제·건조', '원심분리·건조\n분말', False)]
w, gap = 2.75, 0.42
for i, (t, d, now) in enumerate(steps):
    x = 0.2 + i * (w + gap)
    box(ax, x, 2.0, w, 2.3, '', fc='#fdebd0' if now else 'white', ec=ORG if now else INK)
    ax.text(x + w / 2, 3.75, t, ha='center', va='center', fontsize=9.5, fontweight='bold')
    ax.text(x + w / 2, 2.8, d, ha='center', va='center', fontsize=8.3)
    if i < 5:
        arrow(ax, x + w + 0.03, 3.15, x + w + gap - 0.03, 3.15, ms=9)
ax.text(0.2 + w / 2, 1.45, '이번 실습', ha='center', fontsize=9, color=ORG, fontweight='bold')
ax.text(9.5, 0.55, '②~⑥은 수업 구두 설명 기준. 전체 약 5일 (한 프로토콜 약 75분, 원심분리 1회 약 40분)', ha='center', fontsize=8.5, color='#555')
save(fig, 'f_flow')


# ---------- 4. 1차 탈용매화: 수화층 제거 → 분별 침전, 크기와 빛 산란 ----------
fig = plt.figure(figsize=(9.6, 4.4))
ax = fig.add_axes([0, 0, 0.64, 1]); ax.set_xlim(0, 12.5); ax.set_ylim(0, 8.6); ax.axis('off')
ax.text(0.1, 8.15, '(a) 아세톤을 넣으면 (개념도)', fontsize=10.5)
# 왼쪽: 물에 녹은 상태
ax.add_patch(Rectangle((0.3, 0.8), 4.4, 6.4, fc=LIQ, ec=INK, alpha=0.8))
ax.text(2.5, 0.35, '물에 녹은 젤라틴', ha='center', fontsize=9)
rr = np.random.default_rng(7)
def chain(ax, x, y, L, c=GEL, lw=2.2, shell=True):
    t = np.linspace(0, 1, 40)
    xs = x + L * t; ys = y + 0.18 * np.sin(t * 9 + rr.random() * 3)
    if shell:
        ax.plot(xs, ys, color='white', lw=lw + 7, alpha=0.95, solid_capstyle='round')
        ax.plot(xs, ys, color='#7fb3e0', lw=lw + 7, alpha=0.35, solid_capstyle='round')
    ax.plot(xs, ys, color=c, lw=lw, solid_capstyle='round')
for (x, y, L) in [(0.7, 6.3, 2.6), (1.9, 5.2, 2.4), (0.8, 4.1, 1.0), (2.6, 3.6, 1.0), (0.8, 2.6, 2.7), (3.0, 1.6, 0.9), (1.2, 1.5, 0.8)]:
    chain(ax, x, y, L)
ax.text(2.5, 7.45, '사슬마다 물 분자 껍질(수화층)', ha='center', fontsize=8.3, color=BLUE)
arrow(ax, 4.9, 4.0, 6.4, 4.0, c=RED, lw=2.2)
ax.text(5.65, 4.45, '아세톤\n1 : 1', ha='center', fontsize=8.5, color=RED)
# 오른쪽: 탈용매화 후
ax.add_patch(Rectangle((6.6, 0.8), 4.4, 6.4, fc='#f2f2f2', ec=INK))
for (x, y, L) in [(7.2, 6.0, 0.9), (9.3, 5.3, 0.8), (7.6, 4.4, 0.9), (9.6, 3.6, 0.8)]:
    chain(ax, x, y, L, shell=True)
ax.text(11.15, 4.9, '저분자량:\n상등액에\n남음 → 버림', fontsize=8.3, va='center')
ax.add_patch(Ellipse((8.8, 1.35), 3.6, 0.9, fc=GEL, ec=INK, alpha=0.85))
ax.text(8.8, 1.35, '고분자량 침전', ha='center', va='center', fontsize=8.5)
ax.text(11.15, 1.6, '수화층이 걷힌\n긴 사슬끼리\n뭉쳐 가라앉음', fontsize=8.3, va='center')
ax.text(8.8, 0.35, '3~5분 뒤', ha='center', fontsize=9)
# (b) 크기와 빛 산란
bx = fig.add_axes([0.72, 0.17, 0.27, 0.66])
bx.set_xscale('log'); bx.set_xlim(1, 3000); bx.set_ylim(0, 1); bx.set_yticks([])
bx.axvspan(1, 40, color=LIQ); bx.axvspan(40, 900, color='#e0e0e0'); bx.axvspan(400, 750, color='#f9e79f', alpha=0.6)
bx.text(6, 0.55, '거의\n산란\n없음\n(투명)', ha='center', va='center', fontsize=8.3)
bx.text(190, 0.78, '강한 산란\n(우유색)', ha='center', va='center', fontsize=8.3)
bx.text(550, 0.22, '가시광\n파장', ha='center', va='center', fontsize=7.8)
bx.set_xlabel('입자 지름 (nm, 로그)', fontsize=8.5)
bx.tick_params(labelsize=8)
bx.set_title('(b) 크기와 빛 산란 [틴들 효과]', fontsize=10, loc='left')
save(fig, 'f_desolv')
print('ok')
