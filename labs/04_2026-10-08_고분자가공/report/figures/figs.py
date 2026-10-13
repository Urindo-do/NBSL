# lab04 원리 그림 4개 — python3 figs.py  → 이 파일 옆에 f_*.png 저장
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Ellipse
import numpy as np
import os
OUT = os.path.dirname(os.path.abspath(__file__))
fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = '#222'; BLUE = '#2f6db5'; LIQ = '#7fb2e5'; GRAY = '#bbb'; RED = '#c0392b'; AIR = '#eef4fb'
GREEN = '#2e8b57'; YEL = '#f4d03f'; PURP = '#7d3c98'; ORG = '#e67e22'; PUA = '#f5b041'; PET = '#d6eaf8'; SI = '#7f8c8d'


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.6, ms=12, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw))


def box(ax, x, y, w, h, txt, fc='white', ec=INK, fs=9.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, txt, ha='center', va='center', fontsize=fs, fontweight='bold' if bold else 'normal')


def save(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------- 1. 고분자 분류 + 301RM/311RM 문헌값 ----------
fig = plt.figure(figsize=(9.6, 4.0))
ax = fig.add_axes([0.0, 0.0, 0.56, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
box(ax, 3.6, 8.6, 2.8, 1.0, '고분자', fc='#f2f3f4', fs=11, bold=True)
box(ax, 0.3, 6.2, 3.6, 1.0, '천연 고분자', fc='#e8f8f5', fs=10.5)
box(ax, 6.1, 6.2, 3.6, 1.0, '합성 고분자', fc='#fef5e7', fs=10.5)
arrow(ax, 4.4, 8.55, 2.3, 7.3); arrow(ax, 5.6, 8.55, 7.7, 7.3)
ax.text(2.1, 5.6, '콜라겐 (동물 조직)\n키토산 (갑각류)\n알지네이트', ha='center', va='top', fontsize=9.5, linespacing=1.6)
items = [('PDMS', '열경화 (10 : 1 혼합)', 4.9), ('PUA', 'UV 경화 (광중합)', 3.7), ('PCL · PLGA', '용매에 녹여 필름 성형', 2.5)]
for name, how, y in items:
    box(ax, 5.3, y - 0.45, 1.9, 0.9, name, fc='#fdebd0', fs=9.5)
    ax.text(7.35, y, how, va='center', fontsize=9)
ax.text(0.2, 0.6, '(a) 수업에서 소개한 고분자 분류', fontsize=10.5)
# (b) 문헌값 막대
ax1 = fig.add_axes([0.63, 0.22, 0.15, 0.62]); ax2 = fig.add_axes([0.84, 0.22, 0.15, 0.62])
names = ['301RM\n(soft)', '311RM\n(hard)']
ax1.bar(names, [20, 320], color=[LIQ, ORG], ec=INK); ax1.set_title('영률 (MPa)', fontsize=10)
for i, v in enumerate([20, 320]): ax1.text(i, v + 8, str(v), ha='center', fontsize=9.5)
ax1.set_ylim(0, 380)
ax2.bar(names, [45, 9], color=[LIQ, ORG], ec=INK); ax2.set_title('파단 연신율 (%)', fontsize=10)
for i, v in enumerate([45, 9]): ax2.text(i, v + 1.2, str(v), ha='center', fontsize=9.5)
ax2.set_ylim(0, 54)
for a in (ax1, ax2):
    a.tick_params(labelsize=8.5); a.spines[['top', 'right']].set_visible(False)
fig.text(0.63, 0.04, '(b) 경화한 PUA 두 종류의 문헌값 (측정값 아님)', fontsize=10.5)
save(fig, 'f_material')


# ---------- 2. 두 경화 방식: 열(PDMS) vs 빛(PUA) ----------
fig, axs = plt.subplots(1, 2, figsize=(9.6, 3.9))
for ax in axs:
    ax.set_xlim(0, 10); ax.set_ylim(0, 8.6); ax.axis('off')
# (a) PDMS 하이드로실릴화
ax = axs[0]
ax.text(0.1, 8.1, '(a) PDMS: 열로 빨라지는 하이드로실릴화', fontsize=10.5)
for k, y in enumerate((6.6, 5.4)):
    ax.plot([0.5, 3.6], [y, y], color=BLUE, lw=3)
    ax.text(0.5, y + 0.35, '비닐 말단 사슬 (베이스)', fontsize=8.5, color=BLUE)
    ax.add_patch(Circle((3.75, y), 0.18, fc=GREEN, ec=INK))
for y in (6.6, 5.4):
    ax.text(4.2, y - 0.1, '+', fontsize=13)
ax.plot([4.9, 4.9], [5.0, 7.0], color=PURP, lw=3)
for y in (6.6, 5.4):
    ax.add_patch(Circle((4.9, y), 0.18, fc=YEL, ec=INK))
ax.text(4.9, 4.55, 'Si–H를 가진 가교 성분', fontsize=8.5, color=PURP, ha='center')
arrow(ax, 6.3, 6.0, 7.5, 6.0, c=RED, lw=2.0)
ax.text(6.9, 6.35, '백금 촉매\n+ 열', ha='center', fontsize=8.5, color=RED)
# 그물
xs = np.linspace(7.8, 9.8, 4); ys = np.linspace(5.0, 7.0, 4)
for x in xs: ax.plot([x, x], [5.0, 7.0], color=BLUE, lw=1.6)
for y in ys: ax.plot([7.8, 9.8], [y, y], color=PURP, lw=1.6)
ax.text(8.8, 4.45, '가교망 (고무 탄성체)', ha='center', fontsize=8.5)
for i, (t, c) in enumerate([('베이스 10', BLUE), ('경화제 1', PURP)]):
    ax.add_patch(Rectangle((0.6 + i * 2.3, 1.5), 1.9 if i == 0 else 0.4, 1.4, fc='#d6eaf8' if i == 0 else '#e8daef', ec=INK))
ax.text(1.55, 1.0, '베이스 10', ha='center', fontsize=9); ax.text(3.1, 1.0, '경화제 1', ha='center', fontsize=9)
ax.text(2.6, 3.25, '무게비', ha='center', fontsize=9)
arrow(ax, 4.0, 2.2, 5.2, 2.2)
ax.text(5.4, 2.2, '섞기 → 탈포 →\n붓기 → 가열 경화', va='center', fontsize=9)
# (b) PUA 광중합
ax = axs[1]
ax.text(0.1, 8.1, '(b) PUA: 빛이 시작하는 라디칼 광중합', fontsize=10.5)
for x in (1.0, 1.6, 2.2):
    arrow(ax, x, 7.5, x + 0.3, 6.6, c=PURP, lw=1.6, ms=10)
ax.text(2.7, 7.2, 'UV', fontsize=10, color=PURP)
ax.add_patch(Circle((1.6, 5.9), 0.35, fc=YEL, ec=INK)); ax.text(1.6, 5.15, '광개시제', ha='center', fontsize=8.5)
arrow(ax, 2.2, 5.9, 3.3, 5.9, c=RED, lw=1.8)
ax.add_patch(Circle((3.75, 5.9), 0.25, fc=RED, ec=INK)); ax.text(3.75, 5.15, '라디칼', ha='center', fontsize=8.5)
arrow(ax, 4.2, 5.9, 5.3, 5.9, c=RED, lw=1.8)
ax.text(5.6, 6.6, 'C=C에 차례로\n붙으며 성장', fontsize=8.5, va='bottom')
xs = np.linspace(7.8, 9.8, 4); ys = np.linspace(5.0, 7.0, 4)
for x in xs: ax.plot([x, x], [5.0, 7.0], color=ORG, lw=1.6)
for y in ys: ax.plot([7.8, 9.8], [y, y], color=ORG, lw=1.6)
ax.text(8.8, 4.45, '가교망 (굳은 PUA)', ha='center', fontsize=8.5)
ax.text(0.6, 2.9, '방해 요인 ① 산소가 라디칼을 없앰 (산소 저해)', fontsize=9)
ax.text(0.6, 2.1, '방해 요인 ② 굳으며 부피가 줄어듦 (수축·응력)', fontsize=9)
ax.text(0.6, 1.0, '빛을 쬐면 실온에서 빠르게 가교 (가열 불필요)', fontsize=9, color=BLUE)
save(fig, 'f_cure')


# ---------- 3. PUA 복제 단면 4단계 + 조사량 H = E·t ----------
fig = plt.figure(figsize=(9.6, 4.2))
ax = fig.add_axes([0.0, 0.0, 0.55, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')


def wafer(ax, x0, y0, w=3.8, teeth=True):
    ax.add_patch(Rectangle((x0 - 0.3, y0 - 0.25), w + 0.6, 0.25, fc='white', ec=GRAY, lw=1))  # 종이
    ax.add_patch(Rectangle((x0, y0), w, 0.5, fc=SI, ec=INK))
    if teeth:
        for k in range(7):
            ax.add_patch(Rectangle((x0 + 0.25 + k * 0.5, y0 + 0.5), 0.25, 0.22, fc=SI, ec=INK, lw=0.6))


# ① 떨어뜨리기
x0, y0 = 0.5, 7.0
wafer(ax, x0, y0)
for cx in (1.4, 2.4, 3.4):
    ax.add_patch(Ellipse((cx, y0 + 1.05), 0.55, 0.45, fc=PUA, ec=INK))
ax.text(x0, 9.4, '① 원판 위에 PUA 방울', fontsize=9.5)
# ② PET 덮고 롤러 (PUA가 요철 사이를 채움)
x0 = 5.6
ax.add_patch(Rectangle((x0 - 0.1, y0 + 0.5), 4.0, 0.47, fc=PUA, ec='none'))
wafer(ax, x0, y0)
ax.add_patch(Rectangle((x0 - 0.6, y0 + 0.97), 5.0, 0.22, fc=PET, ec=INK))
ax.add_patch(Circle((x0 + 2.6, y0 + 1.7), 0.48, fc='#555', ec=INK))
ax.text(x0, 9.4, '② PET를 덮고 롤러로 밀기', fontsize=9.5)
# ③ UV
x0, y0 = 0.5, 2.6
ax.add_patch(Rectangle((x0 - 0.1, y0 + 0.5), 4.0, 0.47, fc=ORG, ec='none'))
wafer(ax, x0, y0)
ax.add_patch(Rectangle((x0 - 0.6, y0 + 0.97), 5.0, 0.22, fc=PET, ec=INK))
for x in np.linspace(1.0, 3.8, 5):
    arrow(ax, x, y0 + 2.6, x, y0 + 1.3, c=PURP, lw=1.5, ms=10)
ax.text(x0, 5.4, '③ PET 너머로 UV 조사 (수평 유지)', fontsize=9.5)
# ④ 떼기: PET에 붙은 PUA, 원판 요철의 반대 모양
x0 = 5.6
wafer(ax, x0, y0)
lift = 1.3
ax.add_patch(Rectangle((x0 - 0.6, y0 + 0.97 + lift), 5.0, 0.22, fc=PET, ec=INK))
ax.add_patch(Rectangle((x0 - 0.1, y0 + 0.72 + lift), 4.0, 0.25, fc=ORG, ec='none'))
for k in range(8):
    gx = x0 + k * 0.5   # 원판 볼록부 사이(오목한 곳) 위치
    ax.add_patch(Rectangle((gx, y0 + 0.5 + lift), 0.25, 0.22, fc=ORG, ec='none'))
arrow(ax, x0 + 4.2, y0 + 1.6 + lift, x0 + 4.2, y0 + 2.3 + lift, lw=1.4)
ax.text(x0, 5.4, '④ PET를 들어 올려 떼기', fontsize=9.5)
ax.text(0.5, 1.1, '원판의 볼록한 곳 → 복제면의 오목한 곳 (반대 모양)', fontsize=9)
ax.text(0.5, 0.35, '(a) 복제 단면 개념도 (요철은 설명용, 이번 원판은 플랫)', fontsize=10.5)
# (b) 조사량
ax = fig.add_axes([0.63, 0.2, 0.36, 0.7])
t = np.linspace(0, 60, 200)
for E, c in ((5, LIQ), (10, BLUE), (20, PURP)):
    ax.plot(t, E * t, color=c, lw=2.0, label=f'E = {E} mW/cm²')
    tt = 200 / E
    ax.plot(tt, 200, 'o', color=RED, ms=5)
    ax.text(tt + 1.0, 200 - 28, f'{tt:.0f} s', fontsize=8.5, color=RED)
ax.axhline(200, color=RED, ls='--', lw=1)
ax.text(1, 215, '200 mJ/cm² (문헌 조건 예)', fontsize=8.5, color=RED)
ax.set_xlabel('조사 시간 t (s)'); ax.set_ylabel('조사량 H (mJ/cm²)')
ax.set_xlim(0, 60); ax.set_ylim(0, 420); ax.grid(alpha=0.3); ax.legend(fontsize=8.5, loc='upper left', bbox_to_anchor=(0.0, 0.92))
fig.text(0.63, 0.04, '(b) H = E × t (세기는 가정값, 측정값 아님)', fontsize=10.5)
save(fig, 'f_pua')


# ---------- 4. 회절격자: d sin θ = mλ ----------
fig = plt.figure(figsize=(9.6, 3.9))
ax = fig.add_axes([0.0, 0.0, 0.45, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
for k in range(9):
    ax.add_patch(Rectangle((1.0 + k * 0.9, 2.0), 0.45, 0.45, fc=SI, ec=INK, lw=0.6))
ax.add_patch(Rectangle((1.0, 1.6), 8.1, 0.4, fc=SI, ec=INK))
ax.annotate('', (1.9, 1.25), (1.0, 1.25), arrowprops=dict(arrowstyle='<->'))
ax.text(1.45, 0.6, 'd', ha='center', fontsize=11)
for x in (4.6, 5.0):
    arrow(ax, x, 8.6, x, 2.6, c='#999', lw=1.6)
ax.text(5.2, 8.6, '백색광 (수직 입사)', fontsize=9.5)
for ang, c, lab in ((35, '#2e86c1', '파랑'), (48, GREEN, '초록'), (62, RED, '빨강')):
    r = 5.4; a = np.radians(ang)
    arrow(ax, 4.8, 2.6, 4.8 - r * np.sin(a), 2.6 + r * np.cos(a), c=c, lw=1.8)
    ax.text(4.8 - (r + 0.5) * np.sin(a), 2.6 + (r + 0.5) * np.cos(a), lab, fontsize=9, color=c, ha='center')
ax.text(5.4, 5.6, '파장마다 다른\n각도로 갈라짐', fontsize=9)
ax.text(0.3, 0.0, '(a) 반복 패턴의 회절 (개념도, 1차만 표시)', fontsize=10.5)
ax = fig.add_axes([0.55, 0.2, 0.43, 0.7])
lam = np.linspace(400, 700, 301)
for d, c in ((600, ORG), (800, BLUE)):
    s = lam / d; ok = s <= 1
    ax.plot(lam[ok], np.degrees(np.arcsin(s[ok])), color=c, lw=2.2, label=f'd = {d} nm')
ax.axvline(600, color=ORG, ls=':', lw=1)
ax.text(605, 22, 'd = 600 nm면\n600 nm보다 긴 빛은\n1차 회절 없음', fontsize=8.5, color=ORG)
ax.set_xlabel('파장 λ (nm)'); ax.set_ylabel('1차 회절각 θ (°)'); ax.set_xlim(400, 700); ax.set_ylim(20, 92)
ax.grid(alpha=0.3); ax.legend(fontsize=9, loc='upper left')
fig.text(0.55, 0.04, '(b) sin θ = λ / d 계산 (d는 가정값)', fontsize=10.5)
save(fig, 'f_grating')
print('ok')
