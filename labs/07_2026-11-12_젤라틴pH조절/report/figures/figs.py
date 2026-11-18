# lab07 원리 그림 — python3 figs.py  → 이 파일 옆에 f_*.png 저장
# 근거: ../../README.md. 그래프 값은 Ahsan & Rao(2017) 그림 1·2를 눈으로 읽은 근삿값을 다시 그린 것이다.
# 우리 실습에서 제타 전위·입자 크기를 측정하지는 않았다. 나머지는 개념도.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))
fp = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family'] = fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus'] = False
INK = '#222'; BLUE = '#2f6db5'; LIQ = '#cfe3f7'; GRAY = '#999'; RED = '#c0392b'
GREEN = '#2e8b57'; ORG = '#e67e22'; GEL = '#d4a017'; PUR = '#7d3c98'


def arrow(ax, x1, y1, x2, y2, c=INK, lw=1.6, ms=12, style='-|>'):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=c, lw=lw))


def box(ax, x, y, w, h, fc='white', ec=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.12', fc=fc, ec=ec, lw=1.2))


def save(fig, name):
    fig.savefig(os.path.join(OUT, f'{name}.png'), dpi=220, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------- 1. 전 과정 흐름과 이번 단계 ----------
fig = plt.figure(figsize=(9.4, 2.7))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 19); ax.set_ylim(0, 5.4); ax.axis('off')
steps = [('① 1차 탈용매화', '아세톤을 한 번에\n고분자량만 침전', 'again'),
         ('② 재용해', '침전을 다시\n물에 녹임', 'now'),
         ('③ pH 조절', '3 % HCl로\npH 3.00', 'now'),
         ('④ 2차 탈용매화', '아세톤을 천천히\n나노입자 형성', ''),
         ('⑤ 가교', '글루타르알데하이드\n형태 고정', ''),
         ('⑥ 정제·건조', '원심분리·건조\n분말', '')]
w, gap = 2.75, 0.42
for i, (t, d, st) in enumerate(steps):
    x = 0.2 + i * (w + gap)
    hot = st in ('again', 'now')
    box(ax, x, 2.0, w, 2.3, fc='#fdebd0' if hot else 'white', ec=ORG if hot else INK)
    ax.text(x + w / 2, 3.75, t, ha='center', va='center', fontsize=9.5, fontweight='bold')
    ax.text(x + w / 2, 2.8, d, ha='center', va='center', fontsize=8.3)
    if i < 5:
        arrow(ax, x + w + 0.03, 3.15, x + w + gap - 0.03, 3.15, ms=9)
ax.text(0.2 + w / 2, 1.45, '지난 실습 + 이번에 반복', ha='center', fontsize=8.8, color=ORG)
ax.text(0.2 + (w + gap) + (2 * w + gap) / 2, 1.45, '이번 실습', ha='center', fontsize=9.5, color=ORG, fontweight='bold')
ax.annotate('', xy=(0.2 + w + gap + 0.1, 1.85), xytext=(0.2 + 2 * (w + gap) + w - 0.1, 1.85),
            arrowprops=dict(arrowstyle='-', color=ORG, lw=1.5))
ax.text(9.5, 0.55, '④~⑥은 수업 구두 설명 기준이며 이번에 실습하지 않았다', ha='center', fontsize=8.5, color='#555')
save(fig, 'f_flow')


# ---------- 2. pH와 제타 전위 (Ahsan & Rao 2017 그림 1 근삿값) ----------
phA = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5]
zA = [1.4, 7.8, 15.1, 20.1, 17.3, 17.4, 12.4, 10.7, 5.2, 3.0, 2.2, -1.5, -1.1]
phB = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6]
zB = [2.6, 6.7, 15.5, 17.6, 16.5, 9.9, 5.4, -0.3, -2.5, -6.2]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.6, 3.9), gridspec_kw=dict(wspace=0.28))
for ax, ph, z, lab, pi in [(a1, phA, zA, '(a) Type A 젤라틴 (우리가 쓴 종류)', (7.0, 9.0)),
                           (a2, phB, zB, '(b) Type B 젤라틴 (논문 주 실험)', (4.7, 5.2))]:
    ax.axhline(0, color=INK, lw=1)
    ax.axvspan(*pi, color='#d6e4f5', zorder=0)
    ax.plot(ph, z, '-o', color=BLUE, ms=4, lw=1.6)
    ax.set_xlabel('pH', fontsize=9.5); ax.set_ylabel('제타 전위 (mV)', fontsize=9.5)
    ax.set_title(lab, fontsize=10, loc='left')
    ax.tick_params(labelsize=8.5)
    ax.text(pi[0] + 0.08, -4.6, f'등전점\n{pi[0]}~{pi[1]}', fontsize=8, color=BLUE, va='bottom')
a1.set_xlim(1, 9.2); a1.set_ylim(-7, 25)
a2.set_xlim(1, 6.5); a2.set_ylim(-9, 22)
# 우리 실습의 pH 위치 (Type A 곡선 위 보간 위치, 측정값 아님)
for p, txt, c, dx, dy in [(5.6, '처음 약 5.6', GREEN, 0.25, 3.5), (3.0, '목표 3.00', ORG, 0.35, 2.5), (2.08, '과적가 2.08', RED, 0.3, -5.5)]:
    zz = float(np.interp(p, phA, zA))
    a1.plot([p], [zz], 's', ms=8, mfc='none', mec=c, mew=2)
    a1.annotate(txt, (p, zz), (p + dx, zz + dy), fontsize=8.3, color=c,
                arrowprops=dict(arrowstyle='-', color=c, lw=1))
a1.text(1.15, -6.5, '네모: 우리 실습 pH의 위치 (제타 전위는 측정 안 함)', fontsize=7.8, color='#555')
a2.annotate('pH 4 아래:\nAsp·Glu 양성자화', (3.6, 16.5), (4.05, 17.5), fontsize=7.8, color=PUR,
            arrowprops=dict(arrowstyle='-', color=PUR, lw=1))
a2.annotate('최댓값 아래:\nCl$^{-}$ 차폐로 감소', (2.2, 9.5), (1.15, 13.5), fontsize=7.8, color=PUR,
            arrowprops=dict(arrowstyle='-', color=PUR, lw=1))
fig.text(0.5, -0.04, 'Ahsan & Rao(2017) 그림 1의 값을 눈으로 읽어 다시 그린 근삿값 (젤라틴 10 mg/mL, 25 °C). 파란 띠는 등전점 범위', ha='center', fontsize=8.2, color='#555')
save(fig, 'f_zeta')


# ---------- 3. pH와 아세톤 요구량, 입자 크기 (그림 2 근삿값) ----------
fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.4), gridspec_kw=dict(wspace=0.42))
ax = axs[0]
ax.plot([3.0, 3.25, 3.5, 3.75, 4.0], [77.8, 75.0, 71.5, 63.0, 53.5], '-o', color=RED, ms=4)
ax.set_xlabel('pH', fontsize=9); ax.set_ylabel('침전 시작 아세톤 (%)', fontsize=9)
ax.set_title('(a) 필요한 아세톤 양 (Type B)', fontsize=9.5, loc='left'); ax.set_ylim(50, 82)
ax.text(3.55, 76.5, '등전점에서 멀수록\n아세톤이 더 필요', fontsize=7.8, color=RED)
ax = axs[1]
ax.axvspan(2.8, 3.5, color='#eeeeee')
ax.text(3.15, 172, '1 %에서\n입자 안 생김', ha='center', fontsize=7.6, color='#555')
ax.plot([3.5, 4.0, 4.5, 5.0], [141, 120, 157, 175.5], '-o', color=BLUE, ms=4)
ax.set_xlim(2.8, 5.1); ax.set_ylim(110, 185)
ax.set_xlabel('pH', fontsize=9); ax.set_ylabel('입자 크기 (nm)', fontsize=9)
ax.set_title('(b) 입자 크기 (Type A)', fontsize=9.5, loc='left')
ax.axvline(3.0, color=ORG, ls='--', lw=1.2); ax.text(3.04, 113, '우리 3.00', fontsize=7.6, color=ORG)
ax = axs[2]
ax.axvspan(2.8, 3.0, color='#eeeeee')
ax.plot([3.0, 3.25, 3.5, 3.75, 4.0], [153.5, 126.5, 142.5, 148, 178], '-o', color=BLUE, ms=4)
ax.set_xlim(2.8, 4.1); ax.set_ylim(118, 185)
ax.set_xlabel('pH', fontsize=9); ax.set_ylabel('입자 크기 (nm)', fontsize=9)
ax.set_title('(c) 입자 크기 (Type B)', fontsize=9.5, loc='left')
for a in axs:
    a.tick_params(labelsize=8)
fig.text(0.5, -0.06, 'Ahsan & Rao(2017) 그림 2의 값을 눈으로 읽어 다시 그린 근삿값 (2차 탈용매화 젤라틴 1 %). 회색: 입자가 생기지 않은 pH', ha='center', fontsize=8.2, color='#555')
save(fig, 'f_size')


# ---------- 4. 전하 반발과 탈수의 균형 (개념도) ----------
fig = plt.figure(figsize=(9.8, 4.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 30); ax.set_ylim(0, 13); ax.axis('off')
cols = [(1.0, '등전점 근처 (Type A: pH 7~9)', '전하 거의 없음', '반발 약함 → 아세톤이 들어오자마자\n분자끼리 크게 뭉침 (응집, 눈에 보임)', 'agg'),
        (10.8, '알맞은 산성 (우리: pH 3.00)', '양전하 큼', '물을 빼는 힘과 반발이 맞서\n조금씩만 모임 → 나노입자', 'np'),
        (20.6, '너무 낮은 pH (논문: Type A 1 %에서 3.5 아래)', '전하 줄어듦 (Cl$^{-}$ 차폐)', '수화망이 강해 아세톤을 많이 넣어도\n물이 덜 빠짐 → 침전 안 됨', 'none')]
rr = np.random.default_rng(3)
for x0, title, chg, desc, kind in cols:
    box(ax, x0, 3.2, 8.4, 7.2, fc='#fafafa')
    ax.text(x0 + 4.2, 11.2, title, ha='center', fontsize=9.2, fontweight='bold')
    ax.text(x0 + 4.2, 9.75, chg, ha='center', fontsize=8.6, color=PUR)
    cx, cy = x0 + 4.2, 6.6
    if kind == 'agg':
        for i in range(14):
            ax.add_patch(Circle((cx + float(np.clip(rr.normal(0, 0.6), -1.3, 1.3)), cy + float(np.clip(rr.normal(0, 0.5), -1.0, 1.1))), 0.45, fc=GEL, ec=INK, lw=0.6))
        arrow(ax, x0 + 0.7, 8.9, cx - 1.0, 7.4, c=RED, lw=1.8)
        arrow(ax, x0 + 7.7, 8.9, cx + 1.0, 7.4, c=RED, lw=1.8)
    elif kind == 'np':
        for dx in (-2.0, 0, 2.0):
            ax.add_patch(Circle((cx + dx, cy), 0.75, fc=GEL, ec=INK, lw=0.8))
            for k in range(6):
                th = k * np.pi / 3 + 0.3
                ax.text(cx + dx + 1.0 * np.cos(th), cy + 1.0 * np.sin(th), '+', ha='center', va='center', fontsize=7.5, color=PUR)
        arrow(ax, cx - 1.2, cy + 1.6, cx - 0.4, cy + 1.6, c=PUR, lw=1.4, style='<|-|>', ms=9)
        arrow(ax, cx + 0.4, cy + 1.6, cx + 1.2, cy + 1.6, c=PUR, lw=1.4, style='<|-|>', ms=9)
        arrow(ax, cx - 3.4, cy - 1.6, cx - 2.3, cy - 0.9, c=RED, lw=1.6)
        arrow(ax, cx + 3.4, cy - 1.6, cx + 2.3, cy - 0.9, c=RED, lw=1.6)
    else:
        for dx, dy in ((-2.0, 0.5), (0.2, -0.4), (2.2, 0.6)):
            ax.add_patch(Circle((cx + dx, cy + dy), 1.15, fc=LIQ, ec=BLUE, lw=0.8, ls='--'))
            ax.add_patch(Circle((cx + dx, cy + dy), 0.55, fc=GEL, ec=INK, lw=0.6))
            ax.text(cx + dx + 0.95, cy + dy - 0.95, 'Cl$^{-}$', fontsize=6.8, color=GREEN)
    ax.text(x0 + 4.2, 4.2, desc, ha='center', va='center', fontsize=8.2)
ax.text(15, 2.2, '빨간 화살표: 아세톤이 물을 빼앗아 모으는 힘   보라 화살표: 같은 양전하끼리의 반발   파란 점선: 수화층', ha='center', fontsize=8.2)
ax.text(15, 1.2, 'Ahsan & Rao(2017)의 모식도(Scheme 1)와 결과를 바탕으로 다시 그린 개념도', ha='center', fontsize=8.2, color='#555')
save(fig, 'f_balance')


# ---------- 5. pH에 따라 달라지는 형성 경로와 매트릭스 밀도 (개념도) ----------
fig = plt.figure(figsize=(8.6, 3.7))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 26.5); ax.set_ylim(0, 11.5); ax.axis('off')
rr = np.random.default_rng(5)


def blob(ax, x, y, r, n, fill, ec=INK):
    ax.add_patch(Circle((x, y), r, fc='none', ec=GRAY, lw=0.8, ls=':'))
    for _ in range(n):
        a = rr.random() * 2 * np.pi; d = r * np.sqrt(rr.random()) * 0.85
        ax.add_patch(Circle((x + d * np.cos(a), y + d * np.sin(a)), 0.16, fc=fill, ec=ec, lw=0.3))


ax.text(0.4, 10.6, '(a) pH 4: 촘촘한 핵이 먼저 생기고 그 위에 젤라틴이 붙으며 자람 → 높은 매트릭스 밀도(HMD)', fontsize=9)
for i, (r, n) in enumerate([(0.55, 18), (0.95, 50), (1.25, 95)]):
    blob(ax, 4 + i * 6.5, 7.9, r, n, GEL)
    if i < 2:
        arrow(ax, 5.8 + i * 6.5, 7.9, 8.3 + i * 6.5, 7.9, ms=10)
ax.text(19.6, 7.9, '약 236 nm, 단백질 분해효소에\n천천히 분해', fontsize=8.3, va='center')
ax.text(0.4, 5.0, '(b) pH 3.25: 처음엔 물을 머금은 큰 덩어리 → 아세톤이 늘며 오그라듦 → 낮은 매트릭스 밀도(LMD)', fontsize=9)
for i, (r, n) in enumerate([(1.9, 40), (1.4, 45), (1.05, 45)]):
    blob(ax, 4 + i * 6.5, 2.3, r, n, '#f5d98b')
    if i < 2:
        arrow(ax, 6.2 + i * 6.5, 2.3, 8.0 + i * 6.5, 2.3, ms=10)
ax.text(19.6, 2.3, '약 185 nm, 단백질 분해효소에\n빨리 분해', fontsize=8.3, va='center')
ax.text(13.2, 0.15, '아세톤 양 →   (Type B 젤라틴 결과, Ahsan & Rao 2017 그림 3·4를 바탕으로 다시 그린 개념도)', ha='center', fontsize=8, color='#555')
save(fig, 'f_path')
print('ok')
