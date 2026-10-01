import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Ellipse
import numpy as np
import os
OUT = os.path.dirname(os.path.abspath(__file__))  # 그림은 이 스크립트 옆에 저장
fp='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
fm.fontManager.addfont(fp)
plt.rcParams['font.family']=fm.FontProperties(fname=fp).get_name()
plt.rcParams['axes.unicode_minus']=False
INK='#222'; BLUE='#2f6db5'; LIQ='#7fb2e5'; GRAY='#bbb'; RED='#c0392b'; AIR='#eef4fb'
def arrow(ax,x1,y1,x2,y2,c=INK,lw=1.6,ms=12):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=ms,color=c,lw=lw))
def save(fig,name):
    fig.savefig(os.path.join(OUT, f'{name}.png'),dpi=220,bbox_inches='tight',facecolor='white'); plt.close(fig)

# ---------- 1. pipette air displacement ----------
fig,axs=plt.subplots(1,3,figsize=(9,4.2))
titles=['① 첫 번째 멈춤까지 누름','② 천천히 놓아 흡입','③ 끝까지 눌러 배출']
piston_y=[3.2,4.6,2.7]; liquid=[0,1.0,0]
for i,ax in enumerate(axs):
    ax.set_xlim(0,4); ax.set_ylim(-1.2,7.2); ax.axis('off')
    # cylinder
    ax.add_patch(Rectangle((1.4,2.2),1.2,3.4,fill=False,lw=1.6,ec=INK))
    # air cushion
    ax.add_patch(Rectangle((1.42,2.2),1.16,piston_y[i]-2.2,fc=AIR,ec='none'))
    # piston
    ax.add_patch(Rectangle((1.5,piston_y[i]),1.0,0.35,fc=GRAY,ec=INK))
    ax.plot([2,2],[piston_y[i]+0.35,6.6],color=INK,lw=2.2)
    # tip
    ax.add_patch(Polygon([[1.55,2.2],[2.45,2.2],[2.08,-0.3],[1.92,-0.3]],closed=True,fill=False,ec=INK,lw=1.4))
    if liquid[i]:
        ax.add_patch(Polygon([[1.92,-0.3],[2.08,-0.3],[2.24,0.75],[1.76,0.75]],closed=True,fc=LIQ,ec='none'))
    ax.text(2,-1.0,titles[i],ha='center',fontsize=10.5)
    if i==0:
        arrow(ax,3.2,6.6,3.2,5.4); ax.text(3.35,6.0,'누름',fontsize=9)
        ax.text(2,3.0-0.35,'공기 밀어냄',ha='center',fontsize=8.5,color=BLUE)
    if i==1:
        arrow(ax,3.2,5.4,3.2,6.6); ax.text(3.35,6.0,'놓음',fontsize=9)
        ax.text(2,3.3,'공기층\n(air cushion)',ha='center',fontsize=8.5,color=BLUE)
        ax.text(0.05,0.2,'압력↓ →\n액체 유입',fontsize=8.5,color=BLUE)
    if i==2:
        arrow(ax,3.2,6.6,3.2,5.0); ax.text(3.35,5.8,'끝까지',fontsize=9)
        arrow(ax,2,-0.35,2,-0.75,c=BLUE,ms=9); ax.text(0.1,0.1,'남은 액체까지\n밀어냄',fontsize=8.5,color=BLUE)
fig.suptitle('공기 치환식 피펫: 피스톤과 액체 사이에 공기층이 있다',fontsize=11,y=1.0)
save(fig,'f_pipette')

# ---------- 2. balance EMFC ----------
fig,ax=plt.subplots(figsize=(8.2,4.6)); ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
ax.add_patch(Rectangle((2.9,5.4),0.8,0.4,fc=LIQ,ec=INK)); ax.text(4.0,5.5,'시료',fontsize=9.5)
ax.add_patch(Rectangle((2.0,5.2),2.6,0.18,fc=GRAY,ec=INK)); ax.text(0.3,5.2,'저울 접시',fontsize=9.5)
ax.plot([3.3,3.3],[5.2,3.2],color=INK,lw=2.5)
# magnet (U shape) and coil
ax.add_patch(Rectangle((2.2,1.2),0.35,2.4,fc='#9aa9c9',ec=INK)); ax.add_patch(Rectangle((4.05,1.2),0.35,2.4,fc='#9aa9c9',ec=INK))
ax.add_patch(Rectangle((2.2,0.9),2.2,0.35,fc='#9aa9c9',ec=INK)); ax.text(3.3,0.45,'영구자석',ha='center',fontsize=9)
ax.add_patch(Rectangle((2.75,2.2),1.1,1.0,fc='#f3d9a4',ec=INK)); ax.text(3.3,2.6,'코일',ha='center',fontsize=9)
ax.add_patch(Rectangle((4.9,3.9),0.7,0.4,fc='#cfe3cf',ec=INK)); ax.text(5.8,4.0,'위치 센서',fontsize=9)
ax.plot([3.3,4.9],[4.1,4.1],color=GRAY,ls=':',lw=1.2)
arrow(ax,1.6,6.2,1.6,5.5,c=RED); ax.text(0.2,6.4,'① 무게 때문에 접시가 살짝 내려감',fontsize=9.5,color=RED)
ax.text(5.8,4.6,'② 센서가 내려간 위치를 감지',fontsize=9.5,color=RED)
arrow(ax,4.9,2.2,4.9,3.3,c=BLUE,lw=2); ax.text(5.2,2.6,'③ 코일 전류↑ → 전자기력이 접시를\n    원래 높이까지 밀어 올림',fontsize=9.5,color=BLUE)
ax.add_patch(FancyBboxPatch((5.4,0.5),4.2,1.1,boxstyle='round,pad=0.1',fc='#fff7e6',ec=INK))
ax.text(7.5,1.05,'④ 이때 필요한 전류 ∝ 질량\n    → 전류값을 질량으로 바꿔 표시',ha='center',va='center',fontsize=9.5)
ax.set_title('전자기력 복원(EMFC) 방식 저울의 원리 (개념도)',fontsize=11)
save(fig,'f_balance')

# ---------- 3. pH Nernst line ----------
fig,ax=plt.subplots(figsize=(6.6,4.2))
ph=np.linspace(2,12,50); E=-59.16*(ph-7)
ax.plot(ph,E,color=BLUE,lw=2,label='이론 직선 (25 °C, 기울기 −59.16 mV/pH)')
pts=[(4.01,-59.16*(4.01-7)),(7.00,0),(10.01,-59.16*(10.01-7))]
for p,e in pts:
    ax.plot(p,e,'o',color=RED,ms=7); ax.annotate(f'pH {p:.2f}\n{e:+.0f} mV' if abs(e)>1 else f'pH {p:.2f}\n0 mV',(p,e),textcoords='offset points',xytext=(10,6),fontsize=9)
ax.axhline(0,color=GRAY,lw=0.8); ax.axvline(7,color=GRAY,lw=0.8,ls='--')
ax.set_xlabel('pH'); ax.set_ylabel('전극 전압 (mV)'); ax.set_xlim(2,12)
ax.text(7.15,-320,'영점: pH 7에서 0 mV',fontsize=9,color='#555')
ax.legend(fontsize=8.5,loc='upper right',frameon=False)
ax.set_title('pH 전극의 전압–pH 관계와 보정점 (이론값)',fontsize=11)
for s in ['top','right']: ax.spines[s].set_visible(False)
save(fig,'f_ph')

# ---------- 4. magnetic stirrer ----------
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10); ax.set_ylim(0,7); ax.axis('off')
ax.add_patch(Polygon([[3,6.2],[3,3.2],[7,3.2],[7,6.2]],closed=False,fill=False,ec=INK,lw=1.6))
ax.add_patch(Rectangle((3.03,3.2),3.94,2.3,fc=LIQ,ec='none',alpha=0.6))
ax.add_patch(FancyBboxPatch((4.3,3.3),1.4,0.3,boxstyle='round,pad=0.05',fc='white',ec=INK)); ax.text(5,3.9,'마그네틱 바',ha='center',fontsize=9)
ax.add_patch(Rectangle((1.5,2.6),7,0.6,fc='#eeeeee',ec=INK)); ax.text(8.6,2.75,'상판',fontsize=9)
ax.add_patch(Rectangle((1.9,2.25),6.2,0.3,fc='#f2b8a0',ec=INK)); ax.text(8.2,2.25,'히터',fontsize=9)
ax.add_patch(Rectangle((4.2,1.5),1.6,0.35,fc='#9aa9c9',ec=INK)); ax.text(2.6,1.55,'회전 자석',fontsize=9)
ax.text(4.25,1.6,'N',fontsize=8,color='white'); ax.text(5.6,1.6,'S',fontsize=8,color='white')
ax.add_patch(Rectangle((4.7,0.5),0.6,0.9,fc=GRAY,ec=INK)); ax.text(5.5,0.7,'모터',fontsize=9)
for dx in [-0.6,0.6]:
    ax.add_patch(Ellipse((5+dx*1.2,2.4),1.4,2.2,fill=False,ec=RED,ls='--',lw=1))
ax.text(6.9,1.5,'자기력으로 연결\n(용기에 구멍 불필요)',fontsize=9,color=RED)
arrow(ax,4.2,4.35,5.8,4.35,c=BLUE); ax.text(3.2,4.6,'함께 회전 → 교반',fontsize=9,color=BLUE)
ax.set_title('핫플레이트 교반기의 자석 커플링 (개념도)',fontsize=11)
save(fig,'f_stirrer')

# ---------- 5. degassing ----------
fig,axs=plt.subplots(1,3,figsize=(9,4.2))
labels=['① 팽창\n압력↓ → 기포 부피↑ (보일)','② 부상\n부피↑ → 부력↑ → 빠르게 상승','③ 파열\n표면의 얇은 액막이 터짐']
for i,ax in enumerate(axs):
    ax.set_xlim(0,4); ax.set_ylim(-1.4,6); ax.axis('off')
    ax.add_patch(Rectangle((0.5,0),3,4.2,fc='#f7e7b8',ec=INK))
    ax.text(2,-1.2,labels[i],ha='center',fontsize=9.5)
    if i==0:
        ax.add_patch(Circle((1.4,1.2),0.12,fc='white',ec=INK)); arrow(ax,1.6,1.2,2.1,1.2,c=GRAY,ms=9)
        ax.add_patch(Circle((2.7,1.2),0.35,fc='white',ec=INK))
        ax.text(2,4.8,'대기압 → 감압',ha='center',fontsize=9)
    if i==1:
        for y,r in [(0.8,0.35),(2.0,0.37),(3.2,0.39)]:
            ax.add_patch(Circle((2,y),r,fc='white',ec=INK,alpha=0.35 if y<3 else 1))
        arrow(ax,3.0,0.8,3.0,3.4,c=BLUE)
        ax.text(2,4.8,'상승 속도 ∝ 반지름² / 점도',ha='center',fontsize=9)
    if i==2:
        ax.add_patch(Polygon([[1.5,4.2],[1.65,4.55],[2.0,4.7],[2.35,4.55],[2.5,4.2]],fill=False,ec=INK,ls='--'))
        for a in np.linspace(0,np.pi,6):
            ax.plot([2+0.55*np.cos(a),2+0.8*np.cos(a)],[4.3+0.55*np.sin(a),4.3+0.8*np.sin(a)],color=RED,lw=1.2)
        ax.text(2,5.4,'표면에서 터짐',ha='center',fontsize=9,color=RED)
fig.suptitle('점도가 높은 PDMS의 진공 탈포 과정',fontsize=11,y=1.0)
save(fig,'f_degas')
print('ok')
