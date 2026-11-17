"""Replace the camera-limited async comparison with measured controlled-source load results."""
import json,re,html
from pathlib import Path
root=Path('/home/user/workspace/mypresentaion/v4')
data=root/'measurements/orangepi-20261116-retry'
s=json.loads((data/'replay-summary.json').read_text());r={(v['tag'],v['case']):v for v in s['summary']}
assert len(s['runs'])==36 and all(x['repeats']==3 for x in s['summary'])
labels=[('serial640','완료 대기'),('async1','inflight 1'),('async4','inflight 4'),('async6','inflight 6')]
def table(headers,rows):return '<table><thead><tr>'+''.join('<th>'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
def slide(n,title,lead,body,condition):
 return f'<div class="frame"><section class="slide perf-slide" aria-labelledby="perf-{n}"><h1 id="perf-{n}">{title}</h1><div class="brand"><img src="assets/lig-logo.png" alt="LIG D&amp;A"></div><div class="rule"></div><p class="lead">{lead}</p>{body}<p class="perf-condition">{condition}</p><footer><span>올빼미 / Runtime 성능 비교 · Orange Pi 실측 · 2026.11.16</span><span>P{n}</span></footer></section></div>'
body='<div class="perf-statline"><div><span>설계 기준</span><strong>30Hz / 33.3ms</strong></div><div><span>제어 입력 부하</span><strong>30 / 60 / 120 FPS</strong></div><div><span>추가 반복 측정</span><strong>12조건 × 3회</strong></div></div>'
body+='<div class="perf-protocol">'+table(['고정·기록 조건','시험 구성'],[['실행 환경','Orange Pi 5 Plus · DEEPX M1'],['처리 경로','GUI·짐벌·ReID OFF · ByteTrack'],['입력 공급','실제 16-bit 프레임을 메모리 재생'],['비교 조건','완료 대기 / inflight 1·4·6'],['측정 결과','FPS · 누락 · 평균 / p95 / max']])+'<article><h2>입력과 처리 능력을 분리</h2><p>실카메라 재측정도 30fps 미달<br>추론 비교에는 제어 입력 사용</p><p>5초 준비 → 15초 측정 × 3회<br>실제 공급 FPS와 시각도 검증</p><p>SDK·입력 크기 비교는 별도의<br>실카메라 30회 측정 결과</p></article></div>'
p1=slide(1,'일정한 입력 부하로 파이프라인 처리 능력 측정','실제 카메라 프레임을 재사용하고, NPU 추론과 추적은 그대로 실행했습니다.',body,'YOLO26s 640×640 · NPU_ALL · buffer 6 · 설치 SDK / 실카메라 시험과 메모리 재생 시험을 구분')
parts=[]
for fps in [60,120]:
 rows=[]
 for case,label in labels:
  x=r[(f'replay{fps}',case)]
  rows.append([label,f"{x['tracking_fps']:.2f}",f"{x['drop_pct']:.1f}",f"{x['e2e_p95_ms']:.1f}",f"{x['e2e_max_ms']:.1f}"])
 parts.append(f'<article><h2>{fps} FPS 입력</h2>'+table(['제출 방식','완료 FPS','누락 %','p95 ms','max ms'],rows)+'</article>')
a=r[('replay60','serial640')];b=r[('replay60','async6')]
body='<div class="replay-comparison">'+''.join(parts)+'</div>'
rate30=[r[('replay30',c)] for c,_ in labels]
zero=all(x['dropped_frames']==0 for x in rate30)
body+=f'<div class="perf-bottom"><article><h2>30fps 입력도 별도로 확인</h2><p>네 조건 모두 완료 약 30fps'+(' · 누락 0%' if zero else '')+'<br>관측 max와 장시간 보장은 구분</p></article><article><h2>동시 요청은 처리량·지연의 절충</h2><p>60fps에서 완료 대기 '+f"{a['tracking_fps']:.1f} → inflight 6 {b['tracking_fps']:.1f}fps"+'<br>과부하에서는 큐 대기·누락까지 함께 평가</p></article></div>'
p2=slide(2,'비동기 요청으로 입력 부하에 대응하는 범위 확인','같은 프레임·같은 모델에서 요청 중첩 여부와 미완료 요청 상한을 바꿨습니다.',body,'각 조건 15초 × 3회 · 누락률만 종료 전 0.5초 제외 · p95는 반복 평균 / max는 전체 관측값')
pattern=r'<div class="frame"><section class="slide perf-slide" aria-labelledby="perf-{}">.*?</section></div>'
for name in ['index.html','performance.html']:
 p=root/name;t=p.read_text()
 for n,part in [(1,p1),(2,p2)]:
  t,count=re.subn(pattern.format(n),lambda _:part,t,flags=re.S);assert count==1,(name,n,count)
 p.write_text(t)
p=root/'slides.css';css=p.read_text();mark='/* REPLAY_LOAD_COMPARISON */';css=css.split(mark)[0]
css+='\n'+mark+'\n.replay-comparison{position:absolute;left:56px;right:56px;top:204px;display:grid;grid-template-columns:1fr 1fr;gap:28px}.replay-comparison h2{font-size:24px;line-height:32px;margin:0 0 12px}.replay-comparison table{font-size:18px;line-height:26px}.replay-comparison th{font-size:17px;padding:10px 8px}.replay-comparison td{padding:10px 8px}.replay-comparison th:not(:first-child),.replay-comparison td:not(:first-child){text-align:right}.replay-comparison tbody tr:last-child{background:#F3F6FA}\n'
p.write_text(css)
print('Replaced P1/P2 from 36 measured runs')
