"""검증된 실측 집계에서 v4 성능 비교 4장을 생성한다."""
from pathlib import Path
import json,re,html
ROOT=Path('/home/user/workspace/mypresentaion/v4');DATA=ROOT/'measurements/orangepi-20261116'
data=json.loads((DATA/'summary.json').read_text());rows={(r['tag'],r['case']):r for r in data['summary']}
findings=json.loads((DATA/'findings.json').read_text())
def fmt(value,digits=2):
    return f'{value:.{digits}f}'
def table(headers,body):
    return '<table><thead><tr>'+''.join('<th>'+h+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in body)+'</tbody></table>'
def slide(n,title,lead,content,condition):
    return f'''<div class="frame"><section class="slide perf-slide" aria-labelledby="perf-{n}"><h1 id="perf-{n}">{title}</h1><div class="brand"><img src="assets/lig-logo.png" alt="LIG D&amp;A"></div><div class="rule"></div><p class="lead">{lead}</p>{content}<p class="perf-condition">{condition}</p><footer><span>올빼미 / Runtime 성능 비교 · Orange Pi 실측 · 2026.11.16</span><span>P{n}</span></footer></section></div>'''
b=rows[('on-on','async6')];r=rows[('on-on','rect6')];off=rows[('off-on','async6')]
base_condition='core · NPU_ALL · buffer 6 · 5초 준비 + 15초 측정 × 3회 / 지연은 캡처 완료 → 추적 완료'
body='''<div class="perf-statline"><div><span>설계 기준</span><strong>30Hz / 33.3ms</strong></div><div><span>실제 카메라 입력</span><strong>16.87–20.80 FPS</strong></div><div><span>주 비교 측정</span><strong>10조건 × 3회</strong></div></div>'''
body+='<div class="perf-protocol">'+table(['고정·기록 조건','시험 구성'],[
 ['실행 환경','Orange Pi 5 Plus · DEEPX M1'],['처리 경로','GUI·짐벌·ReID OFF · 동일 ByteTrack'],['모델','YOLO26s / CPU 가속 비교는 YOLOv8n'],['기록 항목','프레임별 시각 · SDK 구간 · CPU · RSS'],['측정 결과','FPS · 평균 / p95 / 관측 max · 누락']])+'''<article><h2>실행별 원본 기록을 보존</h2><p>카메라 첫 프레임 이후<br>5초 준비 → 15초 측정</p><p>설정·모델·SDK hash와<br>라이브러리 로딩 경로를 기록</p><p>입력 공급이 30Hz에 못 미쳐<br>최대 처리량 검증과 구분</p></article></div>'''
slides=[slide(1,'처리량과 지연의 최댓값을 함께 측정','동일 조건의 반복 실행으로 파이프라인의 처리 비용과 지연 분포를 비교했습니다.',body,base_condition)]
body_rows=[]
for case,label in [('serial640','제출 후 완료 대기'),('async1','비동기 · inflight 1'),('async4','비동기 · inflight 4'),('async6','비동기 · inflight 6')]:
 x=rows[('on-on',case)];body_rows.append([label,fmt(x['camera_fps']),fmt(x['tracking_fps']),fmt(x['e2e_p95_ms']),fmt(x['e2e_max_ms']),fmt(x['cpu_core_pct'],1)])
body='<p class="perf-subtitle">YOLO26s · 640×640 · SDK 가속 ON/ON</p><div class="perf-table">'+table(['제출 방식','입력 FPS','완료 FPS','p95 ms','max ms','CPU %'],body_rows)+'</div>'
body+='''<div class="perf-bottom"><article><h2>입력과 완료 FPS가 비슷한 조건</h2><p>이번 입력 부하에서는<br>비동기 처리량의 배수 증가를 확인하지 못함</p></article><article><h2>inflight는 요청 수와 지연의 절충</h2><p>1·6 조건에서 33.3ms 초과를 관측<br>평균·p95와 함께 max를 확인</p></article></div>'''
slides.append(slide(2,'비동기·inflight의 효과는 입력 부하와 함께 해석','미완료 요청 상한을 1·4·6으로 바꾸고, 매 제출 후 기다리는 조건과 비교했습니다.',body,'p95는 반복별 p95의 평균 · max는 3회 전체 관측값 · CPU 100% = 1코어 / 모든 조건 누락 0%'))
sdk_rows=[]
for tag,label in [('off-off','OFF / OFF'),('off-on','OFF / ON'),('on-off','ON / OFF'),('on-on','ON / ON')]:
 x=rows[(tag,'ort8')];sdk_rows.append([label,fmt(x['output_format_us']/1000,3),fmt(x['cpu_task_us']/1000,3),fmt(x['e2e_p95_ms']),fmt(x['e2e_max_ms']),fmt(x['cpu_core_pct'],1)])
body='<p class="perf-subtitle">YOLOv8n · 640×640 · use_ort=true · inflight 6</p><div class="perf-table">'+table(['Format / CPU','출력변환 ms','CPU task ms','p95 ms','max ms','CPU %'],sdk_rows)+'</div>'
body+=f'''<div class="perf-bottom"><article><h2>Format 효과를 별도로 확인</h2><p>YOLO26s 출력변환 평균<br>{off['output_format_us']/1000:.3f} → {b['output_format_us']/1000:.3f}ms · {findings['format_output_reduction_pct']:.1f}% 감소</p></article><article><h2>짧은 p95에도 긴 지연이 발생</h2><p>OFF / ON의 p95 17.98ms, max 77.48ms<br>가속 조합을 최악 지연과 함께 판단</p></article></div>'''
slides.append(slide(3,'SDK 가속은 구간별 효과와 조합별 max로 비교','Format 변환과 CPU 연산 가속을 분리해 네 가지 SDK 조합을 측정했습니다.',body,'SDK별 독립 libdxrt 사용 · XNNPACK 경로 확인 · p95는 반복 평균 / max는 조건별 45초 관측 최댓값'))
compare=[]
for label,key,digits in [('전처리 평균 ms','preprocess_ms',3),('NPU 평균 ms','npu_ms',3),('E2E p95 ms','e2e_p95_ms',2),('E2E max ms','e2e_max_ms',2),('RSS peak MiB¹','rss_peak_mib',1)]:compare.append([label,fmt(b[key],digits),fmt(r[key],digits)])
body='<div class="perf-resolution"><figure><img src="assets/performance/resolution-stages.svg" alt="640×640과 640×480의 전처리·호스트 추론 latency·후처리 평균 비교"><figcaption>주요 구간 평균 · NPU 시간은 latency에 포함</figcaption></figure><div>'+table(['측정 항목','640×640','640×480'],compare)+f'''<p class="perf-reduction">p95 {findings['resolution_reduction_pct']['e2e_p95_ms']:.1f}% 감소<br>NPU 시간 {findings['resolution_reduction_pct']['npu_ms']:.1f}% 감소</p></div></div><p class="perf-caveat">동일 계열의 입력 형상별 DXNN 비교 · 전처리 경로와 NPU 입력량이 함께 달라짐<br>전체 개선을 padding 제거 하나의 효과로 귀속하지 않음 · ¹ 반복별 host RSS peak의 평균</p>'''
slides.append(slide(4,'640×480 입력 구성에서 처리 비용과 지연 감소','같은 카메라 원본에 서로 다른 모델 입력 형상을 적용해 단계별 비용을 확인했습니다.',body,'YOLO26s · 비동기 inflight 6 · 가속 ON/ON / 동일 학습·양자화 조건의 완전한 동등성은 미확인'))
p=ROOT/'index.html';s=p.read_text();main=s.index('<main>')+len('<main>');end=s.index('</main>');existing=s[main:end]
# 재실행해도 동일 부록을 중복 추가하지 않는다.
existing=re.sub(r'<div class="frame"><section class="slide perf-slide".*?</section></div>','',existing,flags=re.S)
s=s[:main]+existing+''.join(slides)+s[end:];s=re.sub(r'<nav>.*?</nav>','<nav><span>v4 · 기존 담당 4장 + 실측 성능 비교 P1–P4</span><div><a href="speaker-notes.html">발표 노트</a>　<a href="measurements/performance-report.md">실측 보고서</a>　<button onclick="window.print()">PDF 인쇄</button></div></nav>',s,flags=re.S);p.write_text(s)
only=s[:s.index('<main>')+len('<main>')]+''.join(slides)+s[s.index('</main>'):]
(ROOT/'performance.html').write_text(only.replace('기존 담당 4장 + 실측 성능 비교 P1–P4','실측 성능 비교 P1–P4'))
p=ROOT/'slides.css';css=p.read_text();start=css.find('/* PERF_EXPERIMENT_SLIDES */')
if start>=0:css=css[:start]
css+='''\n/* PERF_EXPERIMENT_SLIDES */
.perf-statline{position:absolute;left:56px;right:56px;top:202px;display:grid;grid-template-columns:repeat(3,1fr);gap:28px}.perf-statline>div{border-top:1px solid var(--line);padding-top:12px}.perf-statline span{display:block;color:var(--muted);font-size:19px;margin-bottom:10px}.perf-statline strong{font-size:29px;font-weight:600;color:var(--blue)}.perf-protocol{position:absolute;left:56px;right:56px;top:326px;display:grid;grid-template-columns:690px 1fr;gap:44px}.perf-protocol article h2{font-size:24px}.perf-protocol article p{font-size:21px;line-height:31px;margin-bottom:17px}.perf-slide table{font-size:20px;line-height:28px;width:100%;table-layout:auto}.perf-slide th{font-size:19px;line-height:26px;padding:10px 13px;white-space:nowrap}.perf-slide td{padding:10px 13px;white-space:nowrap}.perf-slide th:first-child{width:auto}.perf-protocol td{padding-top:8px;padding-bottom:8px}.perf-subtitle{position:absolute;left:56px;right:56px;top:192px;margin:0;font-size:19px;color:var(--muted)}.perf-table{position:absolute;left:56px;right:56px;top:236px}.perf-table th:first-child{width:240px}.perf-table th:not(:first-child),.perf-table td:not(:first-child){text-align:right}.perf-table tbody tr:last-child{background:#F3F6FA}.perf-bottom{position:absolute;left:56px;right:56px;top:507px;display:grid;grid-template-columns:1fr 1fr;gap:44px}.perf-bottom article h2{font-size:24px;line-height:32px;margin-bottom:10px}.perf-bottom article p{font-size:21px;line-height:32px}.perf-condition{position:absolute;left:56px;right:56px;top:645px;margin:0;font-size:12px;line-height:17px;color:var(--muted)}.perf-resolution{position:absolute;left:56px;right:56px;top:204px;display:grid;grid-template-columns:596px 1fr;gap:36px}.perf-resolution figure{margin:0}.perf-resolution img{width:596px;height:344px;object-fit:contain}.perf-resolution figcaption{font-size:15px;line-height:22px;color:var(--muted);margin-top:2px}.perf-resolution table{font-size:19px}.perf-resolution th{font-size:18px;padding:8px}.perf-resolution td{padding:9px 8px}.perf-reduction{font-size:25px!important;line-height:36px!important;color:var(--blue);font-weight:600;margin-top:16px!important}.perf-caveat{position:absolute;left:56px;right:56px;top:588px;font-size:17px;line-height:25px;margin:0;color:var(--muted)}
''';p.write_text(css)
print('Added',len(slides),'performance slides; existing sections',existing.count('section class="slide'))
