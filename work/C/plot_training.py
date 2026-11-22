"""Export training plots from frozen CSV rows; no synthetic intermediate points."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

BASE=Path(__file__).resolve().parent
LOGS=BASE/'sources/latest-20261121/윤관/학습로그'
font=FontProperties(fname='C:/Windows/Fonts/malgun.ttf')
plt.rcParams.update({'font.family':font.get_name(),'font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':False})
COLORS=['#002f6d','#328478','#b57436','#7e8299','#498dc1']

def read(name):
    with (LOGS/name).open(encoding='utf-8-sig',newline='') as file:return list(csv.DictReader(file))

def plot(name, rows, xkey, ykey, xlabel, ylabel, group=None, select=None):
    fig,ax=plt.subplots(figsize=(8.3,4.7),layout='constrained')
    groups=list(dict.fromkeys(r[group] for r in rows)) if group else ['기록값']
    if select is not None:groups=select
    for i,key in enumerate(groups):
        points=[r for r in rows if (not group or r[group]==key) and r.get(xkey) and r.get(ykey)]
        points.sort(key=lambda r:float(r[xkey]))
        ax.plot([float(r[xkey]) for r in points],[float(r[ykey]) for r in points],label=key,color=COLORS[i%len(COLORS)],marker='o',markersize=3,linewidth=2)
    ax.set_xlabel(xlabel);ax.set_ylabel(ylabel);ax.set_ylim(bottom=0);ax.grid(alpha=.2)
    if group:ax.legend(fontsize=10,loc='best')
    fig.savefig(BASE/'assets'/name,dpi=160)
    plt.close(fig)

plot('training-e10.png',read('상체_650장E10재현_학습손실.csv'),'epoch','학습 상자손실','epoch','학습 상자 손실 ↓','실행')
plot('training-repvgg.png',read('외형_11-17_검수264_epoch별.csv'),'epoch','mean_loss','epoch','평균 학습 손실 ↓')
plot('training-solider.png',read('외형_11-20_SOLIDER파인튜닝_선택표.csv'),'step','KEEP','step','선택용 KEEP 점수 ↑','구성')
plot('training-student.png',read('외형_11-20_SOLIDER증류학생_선택표.csv'),'step','S_choose(KEEP)','step','학생 선택용 KEEP 점수 ↑','학생')
rows=read('위치예측_학습곡선.csv')
groups=list(dict.fromkeys(r['모델'] for r in rows))
plot('training-position.png',rows,'epoch','val-A 점수(낮을수록 좋음)','epoch','선택용 val-A 오차 ↓','모델',groups[:3])
# Separate the post-fix DanceTrack stage; do not join incompatible stages or reset logs.
rows=[r for r in read('FastTrackTr_학습손실_100step마다.csv') if r['stage']=='dance_ep3-5_idfix']
for r in rows:r['fractional_epoch']=str(float(r['epoch'])+float(r['iter'])/float(r['of']))
plot('training-fasttrack.png',rows,'fractional_epoch','avg_id','epoch + 기록 step 비율','로그 누적 평균 ID 손실 ↓')
print('Exported six plots from frozen training logs')
