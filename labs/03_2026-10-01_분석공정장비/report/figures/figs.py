# lab03 원리 그림 6개 — python3 figs.py  → 이 파일 옆에 f_*.png 저장
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
GREEN = '#2e8b57'; YEL = '#f4d03f'; PURP = '#7d3c98'


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.6, ms=12, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw))


def save(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------- 1. 도립 현미경 광 경로 + 분해능 ----------
fig = plt.figure(figsize=(9.6, 4.3))
ax = fig.add_axes([0.0, 0.0, 0.42, 1.0]); ax.set_xlim(0, 6); ax.set_ylim(0, 10); ax.axis('off')
# 조명
ax.add_patch(Rectangle((2.3, 9.0), 1.4, 0.6, fc=YEL, ec=INK)); ax.text(3.9, 9.25, '조명(위)', fontsize=9.5, va='center')
ax.add_patch(Polygon([[2.2, 7.6], [3.8, 7.6], [3.4, 8.2], [2.6, 8.2]], fc=GRAY, ec=INK)); ax.text(3.95, 7.9, '집광부', fontsize=9.5, va='center')
for x in (2.75, 3.0, 3.25):
    arrow(ax, x, 8.95, x, 6.55, c='#d4ac0d', lw=1.2, ms=9)
# 배양 접시와 세포
ax.add_patch(Rectangle((0.6, 5.6), 4.8, 0.25, fc='#888', ec=INK)); ax.text(0.6, 5.25, '재물대', fontsize=9.5)
ax.add_patch(Polygon([[1.5, 5.85], [1.5, 6.6], [1.6, 6.6], [1.6, 5.95], [4.4, 5.95], [4.4, 6.6], [4.5, 6.6], [4.5, 5.85]], fc='#cfe3f7', ec=INK))
ax.add_patch(Rectangle((1.6, 5.95), 2.8, 0.45, fc=AIR, ec='none'))
for cx in np.linspace(1.9, 4.1, 7):
    ax.add_patch(Ellipse((cx, 6.03), 0.28, 0.12, fc=RED, ec='none'))
ax.text(4.65, 6.35, '배양 접시\n바닥의 세포', fontsize=9, va='center')
# 대물렌즈(아래)
ax.add_patch(Polygon([[2.5, 5.4], [3.5, 5.4], [3.3, 4.4], [2.7, 4.4]], fc='#ddd', ec=INK))
ax.add_patch(Rectangle((2.5, 4.95), 1.0, 0.12, fc=YEL, ec='none'))
ax.text(3.75, 4.9, '대물렌즈(아래)', fontsize=9.5, va='center')
arrow(ax, 3.0, 4.35, 3.0, 2.6, c='#d4ac0d', lw=1.4)
ax.add_patch(Polygon([[2.4, 2.5], [3.6, 2.5], [3.0, 1.9]], fc=GRAY, ec=INK))
arrow(ax, 3.0, 1.95, 1.2, 1.95, c='#d4ac0d', lw=1.4); ax.text(0.15, 1.45, '접안렌즈', fontsize=9)
arrow(ax, 3.0, 1.95, 4.8, 1.95, c='#d4ac0d', lw=1.4); ax.text(4.3, 1.45, '카메라·PC', fontsize=9)
ax.text(3.0, 0.4, '(a) 도립 현미경의 광 경로', ha='center', fontsize=10.5)
# 분해능 곡선
ax2 = fig.add_axes([0.53, 0.2, 0.44, 0.72])
NA = np.linspace(0.1, 1.45, 300); r = 0.61 * 0.55 / NA
ax2.plot(NA, r, color=BLUE, lw=2)
for na, lab in ((0.25, '1.34 µm'), (1.40, '0.24 µm')):
    rv = 0.61 * 0.55 / na
    ax2.plot(na, rv, 'o', color=RED); ax2.annotate(f'NA {na:.2f} → {lab}', (na, rv), textcoords='offset points', xytext=(10, 6), fontsize=9.5)
ax2.set_xlabel('대물렌즈 개구수 NA'); ax2.set_ylabel('분해능 r (µm)')
ax2.set_ylim(0, 3.6); ax2.set_xlim(0.05, 1.5); ax2.grid(alpha=0.3)
ax2.text(0.6, 2.9, 'r = 0.61 λ / NA\n(λ = 550 nm 계산값)', fontsize=10)
ax2.set_title('(b) 개구수에 따른 분해능', fontsize=10.5, y=-0.36)
save(fig, 'f_micro')

# ---------- 2. 응력–변형률 곡선(개념) + 시료 ----------
fig = plt.figure(figsize=(9.6, 4.0))
ax = fig.add_axes([0.0, 0.0, 0.25, 1.0]); ax.set_xlim(0, 4); ax.set_ylim(0, 10); ax.axis('off')
ax.add_patch(Rectangle((1.2, 7.6), 1.6, 1.2, fc='#999', ec=INK)); ax.add_patch(Rectangle((1.2, 1.4), 1.6, 1.2, fc='#999', ec=INK))
ax.text(2.0, 9.1, '위 그립', ha='center', fontsize=9.5); ax.text(2.0, 0.95, '아래 그립', ha='center', fontsize=9.5)
ax.add_patch(Rectangle((1.65, 2.6), 0.7, 5.0, fc='#d6eaf8', ec=INK))
ax.annotate('', xy=(3.2, 2.6), xytext=(3.2, 7.6), arrowprops=dict(arrowstyle='<->', color=INK))
ax.text(3.35, 5.1, r'$L_0$', fontsize=11, va='center')
ax.text(0.15, 5.1, 'A$_0$ =\n너비×두께', fontsize=9, va='center')
arrow(ax, 2.0, 9.4, 2.0, 9.95, c=RED, lw=2); arrow(ax, 2.0, 0.6, 2.0, 0.05, c=RED, lw=2)
ax.text(2.0, -0.6, '(a) 시료와 기준 길이', ha='center', fontsize=10.5)
ax2 = fig.add_axes([0.36, 0.2, 0.6, 0.72])
e = np.linspace(0, 1, 400)
s = np.where(e < 0.15, e / 0.15 * 0.55, 0.55 + 0.45 * (1 - np.exp(-(e - 0.15) / 0.18)))
s = np.where(e > 0.62, s - 1.8 * (e - 0.62) ** 2, s)
cut = e <= 0.82
ax2.plot(e[cut], s[cut], color=BLUE, lw=2.2)
im = np.argmax(np.where(cut, s, -1)); ib = np.where(cut)[0][-1]
ax2.plot(e[im], s[im], 'o', color=RED); ax2.annotate('인장 강도(최대 응력)', (e[im], s[im]), xytext=(0.32, 1.06), fontsize=9.5, arrowprops=dict(arrowstyle='->'))
ax2.plot(e[ib], s[ib], 'x', color=RED, ms=9, mew=2); ax2.annotate('파단점', (e[ib], s[ib]), xytext=(0.84, 0.62), fontsize=9.5, arrowprops=dict(arrowstyle='->'))
ax2.plot([0.03, 0.11], [0.11, 0.11], color=INK, lw=1); ax2.plot([0.11, 0.11], [0.11, 0.403], color=INK, lw=1)
ax2.text(0.125, 0.2, '기울기 = 탄성 계수', fontsize=9.5)
ax2.axvspan(0, 0.15, color='#eaf2f8'); ax2.text(0.015, 0.85, '탄성\n구간', fontsize=9)
ax2.set_xlim(0, 1); ax2.set_ylim(0, 1.2); ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_xlabel('x축: 늘어난 길이 ΔL  (변형률 ε = ΔL / L$_0$)')
ax2.set_ylabel('y축: 하중 P  (응력 σ = P / A$_0$)')
ax2.plot(0, 0, 'ks', ms=5); ax2.annotate('원점 (0.0)에서 시작', (0.004, 0.004), xytext=(0.2, 0.04), fontsize=9, arrowprops=dict(arrowstyle='->'))
ax2.set_title('(b) 응력–변형률 곡선 (이론 개형, 측정값 아님)', fontsize=10.5, y=-0.34)
save(fig, 'f_tensile')

# ---------- 3. 스핀 코팅 4단계 + 두께 ----------
fig = plt.figure(figsize=(9.6, 4.6))
names = ['① 용액 올리기', '② 회전 가속', '③ 남는 용액이 날아감', '④ 용매 증발']
for i in range(4):
    ax = fig.add_axes([0.01 + i * 0.245, 0.55, 0.23, 0.42]); ax.set_xlim(-3, 3); ax.set_ylim(-1.6, 3); ax.axis('off')
    ax.add_patch(Rectangle((-0.35, -1.5), 0.7, 1.0, fc='#888', ec=INK))
    ax.add_patch(Rectangle((-2.2, -0.5), 4.4, 0.35, fc='#ccc', ec=INK))
    if i == 0:
        ax.add_patch(Ellipse((0, 0.15), 1.2, 0.55, fc=LIQ, ec=BLUE))
        ax.plot([0, 0], [2.6, 1.2], color=INK, lw=2); ax.add_patch(Polygon([[-0.12, 1.2], [0.12, 1.2], [0, 0.75]], fc=INK))
        ax.add_patch(Circle((0, 0.6), 0.1, fc=LIQ))
    elif i == 1:
        ax.add_patch(Polygon([[-1.6, -0.15], [1.6, -0.15], [1.2, 0.1], [-1.2, 0.1]], fc=LIQ, ec=BLUE))
    elif i == 2:
        ax.add_patch(Rectangle((-2.2, -0.15), 4.4, 0.12, fc=LIQ, ec=BLUE))
        for sx in (-1, 1):
            arrow(ax, sx * 2.1, 0.0, sx * 2.9, 0.4, c=BLUE, lw=1.4, ms=9)
            ax.add_patch(Circle((sx * 2.85, 0.65), 0.08, fc=LIQ))
    else:
        ax.add_patch(Rectangle((-2.2, -0.15), 4.4, 0.06, fc=BLUE, ec=BLUE))
        for x in (-1.2, 0, 1.2):
            ax.annotate('', xy=(x, 1.3), xytext=(x, 0.05), arrowprops=dict(arrowstyle='->', color='#999', ls='--'))
        ax.text(0, 1.5, '용매', ha='center', fontsize=9, color='#777')
    if i > 0:
        ax.annotate('', xy=(0.9, -1.1), xytext=(-0.9, -1.1), arrowprops=dict(arrowstyle='->', color=RED, connectionstyle='arc3,rad=0.4'))
    ax.text(0, 2.6 if i else 2.9, names[i], ha='center', fontsize=10, va='bottom') if False else ax.set_title(names[i], fontsize=10)
ax = fig.add_axes([0.2, 0.09, 0.6, 0.36])
rpm = np.linspace(500, 6000, 300); h = np.sqrt(1000 / rpm)
ax.plot(rpm, h, color=BLUE, lw=2)
for v in (1000, 3500):
    ax.plot(v, np.sqrt(1000 / v), 'o', color=RED)
ax.annotate('3,500 rpm → 0.53배', (3500, np.sqrt(1000 / 3500)), xytext=(3800, 0.85), fontsize=9.5, arrowprops=dict(arrowstyle='->'))
ax.annotate('기준 1,000 rpm = 1', (1000, 1), xytext=(1500, 1.25), fontsize=9.5, arrowprops=dict(arrowstyle='->'))
ax.set_xlabel('회전 속도 (rpm)'); ax.set_ylabel('상대 두께'); ax.set_ylim(0, 1.5); ax.grid(alpha=0.3)
ax.text(4600, 1.2, r'$h \propto \omega^{-1/2}$', fontsize=10.5)
save(fig, 'f_spin')

# ---------- 4. 광중합 + 회절격자 ----------
fig = plt.figure(figsize=(9.6, 3.9))
ax = fig.add_axes([0.0, 0.0, 0.5, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
rng = np.random.default_rng(3)
# 왼쪽: 경화 전
ax.add_patch(Rectangle((0.3, 0.9), 3.6, 3.2, fc='#f6f9fc', ec=INK))
for _ in range(16):
    x, y = rng.uniform(0.6, 3.6), rng.uniform(1.2, 3.8); ax.add_patch(Circle((x, y), 0.1, fc=BLUE))
for x, y in ((1.2, 2.0), (2.8, 3.2)):
    ax.add_patch(Polygon([[x, y + 0.18], [x - 0.16, y - 0.12], [x + 0.16, y - 0.12]], fc=RED))
ax.text(2.1, 0.4, '경화 전: 단량체(●)와 광개시제(▲)', ha='center', fontsize=9.2)
for x in (1.2, 2.1, 3.0):
    ax.annotate('', xy=(x, 4.15), xytext=(x - 0.4, 5.3), arrowprops=dict(arrowstyle='->', color=PURP, lw=1.6))
ax.text(2.1, 5.5, 'UV', ha='center', color=PURP, fontsize=11)
arrow(ax, 4.2, 2.5, 5.6, 2.5, lw=2); ax.text(4.9, 2.8, '라디칼 생성\n→ 중합·가교', ha='center', fontsize=8.5, va='bottom')
# 오른쪽: 경화 후 네트워크
ax.add_patch(Rectangle((5.9, 0.9), 3.6, 3.2, fc='#eaf2f8', ec=INK))
xs = np.linspace(6.3, 9.1, 5); ys = np.linspace(1.3, 3.7, 4)
for y in ys:
    ax.plot(xs, [y] * 5, color=BLUE, lw=1.5)
for x in xs[::2]:
    ax.plot([x, x], [ys[0], ys[-1]], color=BLUE, lw=1.5)
for x in xs:
    for y in ys:
        ax.add_patch(Circle((x, y), 0.09, fc=BLUE))
ax.text(7.7, 0.4, '경화 후: 그물 구조의 고체', ha='center', fontsize=9.2)
ax.text(5.0, -0.3, '(a) UV 광중합', ha='center', fontsize=10.5)
# 회절격자
ax = fig.add_axes([0.54, 0.0, 0.46, 1.0]); ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
for i in range(6):
    ax.add_patch(Rectangle((4.15 + i * 0.32, 0.8), 0.14, 0.35, fc=INK))
ax.add_patch(Rectangle((4.0, 0.6), 2.0, 0.2, fc='#ccc', ec=INK))
ax.plot([4.15, 4.47], [1.35, 1.35], color=RED, lw=1.4)
ax.plot([4.15, 4.15], [1.25, 1.45], color=RED, lw=1.4); ax.plot([4.47, 4.47], [1.25, 1.45], color=RED, lw=1.4)
ax.text(3.75, 1.3, 'd', ha='center', fontsize=11, color=RED)
arrow(ax, 1.4, 4.8, 4.9, 1.25, c='#999', lw=3); ax.text(1.0, 5.1, '백색광', fontsize=10)
for ang, col in ((25, '#6c3483'), (34, '#2471a3'), (43, '#28b463'), (52, '#f1c40f'), (60, '#e74c3c')):
    t = np.radians(ang); arrow(ax, 5.0, 1.25, 5.0 + 4.0 * np.sin(t), 1.25 + 4.0 * np.cos(t), c=col, lw=2, ms=10)
ax.text(7.8, 5.3, '파장별로 다른 방향', fontsize=9.5)
ax.text(7.2, 0.6, 'd sin θ = m λ', ha='center', fontsize=11)
ax.text(5.0, -0.5, '(b) 반복 패턴의 회절', ha='center', fontsize=10.5)
save(fig, 'f_uv')

# ---------- 5. 클린벤치 vs BSC Class II 기류 ----------
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2))
for ax in axs:
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 9.0); ax.axis('off')
def person(ax):
    ax.add_patch(Circle((9.6, 4.6), 0.45, fc='#f5cba7', ec=INK)); ax.add_patch(Rectangle((9.2, 1.5), 0.8, 2.6, fc='#f5cba7', ec=INK))
    ax.text(9.6, 0.95, '작업자', ha='center', fontsize=9)
# (a) 클린벤치: 뒤쪽 HEPA → 앞쪽(작업자)으로 수평 기류, 앞면 개방
ax = axs[0]
ax.plot([1.0, 7.0], [6.5, 6.5], color=INK, lw=1.6); ax.plot([1.0, 7.0], [1.5, 1.5], color=INK, lw=1.6); ax.plot([1.0, 1.0], [1.5, 6.5], color=INK, lw=1.6)
ax.add_patch(Rectangle((1.0, 1.5), 0.6, 5.0, fc='#d5f5e3', ec=INK)); ax.text(1.3, 6.75, 'HEPA', ha='center', fontsize=9)
for y in (2.3, 3.3, 4.3, 5.3):
    arrow(ax, 1.8, y, 8.8, y, c=GREEN, lw=1.6)
ax.add_patch(Rectangle((2.6, 1.5), 1.4, 0.5, fc=LIQ, ec=INK)); ax.text(3.3, 1.0, '시료', ha='center', fontsize=9)
person(ax)
ax.text(0.2, 8.5, '(a) 클린벤치: 거른 공기가 작업자 쪽으로', fontsize=10.5)
ax.text(5.0, 0.15, '시료만 보호', ha='center', fontsize=10, color=RED)
# (b) BSC Class II: 위→아래 기류, 앞쪽 그릴로 실내 공기 흡입, 배기 HEPA
ax = axs[1]
ax.plot([1.0, 7.0], [1.5, 1.5], color=INK, lw=1.6); ax.plot([1.0, 1.0], [1.5, 6.5], color=INK, lw=1.6); ax.plot([1.0, 7.0], [6.5, 6.5], color=INK, lw=1.6)
ax.plot([7.0, 7.0], [3.4, 6.5], color='#5d6d7e', lw=3); ax.text(7.2, 5.0, '앞유리', fontsize=8.5, color='#5d6d7e')
ax.add_patch(Rectangle((1.0, 5.9), 6.0, 0.6, fc='#d5f5e3', ec=INK)); ax.text(3.0, 6.05, '공급 HEPA', ha='center', fontsize=9)
ax.add_patch(Rectangle((4.8, 6.5), 1.8, 0.5, fc='#d5f5e3', ec=INK)); ax.text(6.8, 6.6, '배기 HEPA', fontsize=9)
arrow(ax, 5.7, 7.0, 5.7, 7.8, c='#999', lw=1.4)
for x in (2.0, 3.2, 4.4, 5.6):
    arrow(ax, x, 5.8, x, 2.3, c=GREEN, lw=1.6)
ax.add_patch(Rectangle((6.5, 1.5), 0.5, 0.3, fc='#555')); ax.text(6.2, 1.0, '앞쪽 그릴', fontsize=9)
arrow(ax, 8.9, 2.6, 7.1, 1.9, c=BLUE, lw=1.8); ax.text(7.3, 2.9, '실내 공기\n흡입', fontsize=9, color=BLUE)
ax.add_patch(Rectangle((2.6, 1.5), 1.4, 0.5, fc=LIQ, ec=INK)); ax.text(3.3, 1.0, '시료', ha='center', fontsize=9)
person(ax)
ax.text(0.2, 8.5, '(b) 생물안전작업대(BSC) Class II', fontsize=10.5)
ax.text(5.0, 0.15, '시료·작업자·환경 보호', ha='center', fontsize=10, color=RED)
save(fig, 'f_bsc')

# ---------- 6. 물의 포화 증기 곡선 (IAPWS-IF97 계산) ----------
from iapws import IAPWS97
T = np.linspace(90, 140, 120); P = np.array([IAPWS97(T=t + 273.15, x=1).P * 10 for t in T])  # bar abs
fig, ax = plt.subplots(figsize=(7.2, 3.6))
ax.plot(T, P, color=BLUE, lw=2.2)
for t, lab in ((100, '100 °C, 1.01 bar\n(대기압에서 끓음)'), (121, '121 °C, 2.05 bar\n(게이지 약 1.0 bar)'), (132, '132 °C, 2.87 bar')):
    p = IAPWS97(T=t + 273.15, x=1).P * 10
    ax.plot(t, p, 'o', color=RED)
    ax.annotate(lab, (t, p), xytext=(t - 13 if t != 100 else t + 2, p + (0.35 if t != 100 else 0.55)), fontsize=9.5, arrowprops=dict(arrowstyle='->'))
ax.axhline(1.01325, color='#999', ls='--', lw=1)
ax.set_xlabel('온도 (°C)'); ax.set_ylabel('포화 증기 압력 (bar, 절대압)'); ax.grid(alpha=0.3)
ax.set_xlim(90, 140); ax.set_ylim(0.5, 3.8)
save(fig, 'f_auto')
print('ok')
