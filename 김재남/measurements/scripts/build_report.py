"""실측 집계로 보고서와 비교 그래프를 만든다. 수치를 정적으로 꾸며 넣지 않는다."""
import os,json,csv,statistics
from pathlib import Path
os.environ['MPLCONFIGDIR']='/tmp/lwir-performance-mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path('/home/user/workspace/mypresentaion/v4')
DATA=ROOT/'measurements/orangepi-20261116'
s=json.loads((DATA/'summary.json').read_text());lookup={(r['tag'],r['case']):r for r in s['summary']}
main=[r for r in s['runs'] if r['tag'] in ['on-on','off-on','on-off','off-off']]
assert len(main)==30
assert all(r['duration_s']==15 for r in main)
assert all(r['drop_pct']==0 for r in main)
for r in s['summary']:
 if r['tag'] in ['on-on','off-on','on-off','off-off']:assert r['repeats']==3
# 두 모델 입력 형상의 단계별 평균을 표시한다. inference latency에 NPU 시간을 다시 더하지 않는다.
fig,ax=plt.subplots(figsize=(6.1,3.5),dpi=180)
colors=['#94A7BF','#002F6D','#CCD6E2'];bottom=[0.0,0.0]
for key,label,color in zip(['preprocess_ms','latency_ms','postprocess_ms'],['Preprocess','Inference latency (incl. NPU)','Postprocess'],colors):
 vals=[lookup[('on-on',c)][key] for c in ['async6','rect6']]
 ax.bar(['640 x 640','640 x 480'],vals,bottom=bottom,color=color,width=.46,label=label)
 bottom=[a+b for a,b in zip(bottom,vals)]
for x,y in enumerate(bottom):ax.text(x,y+.35,f'{y:.2f} ms',ha='center',fontsize=14,color='#002F6D')
ax.set_ylabel('Mean stage duration (ms)',fontsize=15);ax.set_ylim(0,max(bottom)*1.32)
ax.tick_params(axis='both',labelsize=14);ax.spines[['top','right']].set_visible(False);ax.spines[['left','bottom']].set_color('#DCE2EA');ax.grid(axis='y',color='#E8EDF2',linewidth=.7);ax.set_axisbelow(True)
fig.legend(loc='lower center',ncol=1,frameon=False,fontsize=13,bbox_to_anchor=(.5,-.02));fig.tight_layout(rect=(0,.18,1,1))
fig.savefig(ROOT/'assets/performance/resolution-stages.svg',bbox_inches='tight');fig.savefig(ROOT/'assets/performance/resolution-stages.png',bbox_inches='tight');plt.close(fig)

def row(r):
 return f"{r['tracking_fps']:.2f} FPS / p95 {r['e2e_p95_ms']:.2f} ms / max {r['e2e_max_ms']:.2f} ms / CPU {r['cpu_core_pct']:.1f}%"
base=lookup[('on-on','async6')];rect=lookup[('on-on','rect6')];off=lookup[('off-on','async6')]
resolution={key:100*(1-rect[key]/base[key]) for key in ['preprocess_ms','npu_ms','e2e_p95_ms','e2e_max_ms']}
quality={
 'main_runs':len(main),'valid_measured_frames':sum(r['tracking_frames'] for r in main),
 'input_fps_min':min(r['camera_fps'] for r in main),'input_fps_max':max(r['camera_fps'] for r in main),
 'resolution_reduction_pct':resolution,
 'format_output_reduction_pct':100*(1-base['output_format_us']/off['output_format_us'])
}
(DATA/'findings.json').write_text(json.dumps(quality,indent=2))
lines=['# Orange Pi パイプライン性能比較'.replace('パイプライン性能比較','파이프라인 성능 비교'),'',
'## 실행과 계측',
'- 보드 main 0fe016f7edd069900457a746dc4cc787569c5ae6의 격리 복사본을 사용했다. WSL의 runtime 작업 트리를 수정하지 않았다.',
'- Orange Pi 5 Plus / RK3588, DEEPX M1, RT 3.4.2 계열, driver 2.6.0, firmware 2.7.4. 상세 환경은 environment.txt에 있다.',
'- core 모드, GUI·짐벌 OFF, 동일 ByteTrack, NPU_ALL, buffer_count 6. ORT 비교 외에는 use_ort=false다.',
'- 카메라 첫 프레임 이후 5초 준비하고 15초 측정했다. 주 비교 10조건 × 3회 = 30회, 추가로 설치 SDK 재확인과 GUI 송신 확인을 수행했다.',
'- 실제 입력은 실행별 약 %.2f~%.2f FPS였다. 따라서 이 시험은 30Hz 입력 유지나 NPU 최대 처리량을 검증하지 않는다.'%(quality['input_fps_min'],quality['input_fps_max']),
'- 실제 카메라 고정 샘플 20장의 검출 결과는 0개다. 사용자 요청에 따라 파이프라인 성능만 평가했다. 객체가 많은 장면의 NMS·추적 부하는 대표하지 않는다.',
'- 평균·p50·p95는 반복별 값의 평균이다. max는 같은 조건 3회에서 관측한 전체 최댓값이며 관측 시간은 조건별 45초다.',
'- 지연은 캡처 완료부터 추적 완료 계측 시점까지다. 센서 노출·PC 표시 지연은 포함하지 않는다.',
'- FPS는 측정 구간 안의 완료 개수/15초다. 지연·누락은 측정 구간에 캡처한 프레임 집합을 종료 후 완료 기록과 대응시켰다.',
'- CPU는 1코어 100% 기준의 프로세스 CPU 시간이다. RSS는 호스트 메모리다. SDK job latency 안에 NPU 시간이 포함되므로 둘을 합산하지 않는다.',
'- 동일 계측을 모든 조건에 적용했다. 계측 이벤트는 메모리에 보관하고 종료 후 기록했다. 계측 오버헤드 자체의 별도 정량 검증은 수행하지 않았다.',
'', '## 비동기·inflight 비교',
'| 조건 | 입력 FPS | 완료 FPS | 평균 ms | p95 ms | 관측 max ms | CPU % |', '| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for c in ['serial640','async1','async4','async6']:
 r=lookup[('on-on',c)];lines.append(f"| {c} | {r['camera_fps']:.2f} | {r['tracking_fps']:.2f} | {r['e2e_mean_ms']:.2f} | {r['e2e_p95_ms']:.2f} | {r['e2e_max_ms']:.2f} | {r['cpu_core_pct']:.1f} |")
lines += ['', '- serial640은 동일 RunAsync 경로에서 매 제출 후 wait_idle을 호출한 요청 중첩 OFF 조건이다. 동기 Run API 자체의 비교가 아니다.',
'- max_inflight는 애플리케이션의 미완료 요청 상한이다. buffer_count 또는 코어 개수와 구분한다.',
'- 카메라 공급 FPS와 완료 FPS가 가깝고 반복 간 입력 변동도 있다. 이 자료로 비동기 처리량의 배수 증가를 주장하지 않는다.',
'- 세 반복에서 추적 완료 누락은 0%였다. 관측 max는 1·6 조건에서 33.3ms를 넘었으므로 p95만으로 지연 상한을 판단하지 않는다.',
'', '## SDK 가속 2×2 비교',
'YOLOv8n 640×640, use_ort=true, inflight 6. Format/CPU 옵션은 프로세스별 별도 libdxrt.so로 바꾸고 /proc/PID/maps와 hash를 기록했다.',
'| Format / CPU | output format ms | CPU task ms | 평균 ms | p95 ms | 관측 max ms | CPU % |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for tag in ['off-off','off-on','on-off','on-on']:
 r=lookup[(tag,'ort8')];lines.append(f"| {tag} | {r['output_format_us']/1000:.3f} | {r['cpu_task_us']/1000:.3f} | {r['e2e_mean_ms']:.2f} | {r['e2e_p95_ms']:.2f} | {r['e2e_max_ms']:.2f} | {r['cpu_core_pct']:.1f} |")
lines += ['',f"- 별도 YOLO26s 비교에서 format OFF→ON의 output-format 평균은 {off['output_format_us']/1000:.3f}→{base['output_format_us']/1000:.3f}ms, 약 {quality['format_output_reduction_pct']:.1f}% 감소했다. 이 비교는 CPU 작업이 없는 모델에서 format 효과를 분리한 것이다.",
'- XNNPACK과 NEON 관련 빌드 경로 및 강제 활성 옵션을 확인했다. CPU task 구간의 ON/OFF 효과는 format 조합별로 다르며 모든 지표가 단조 개선되는 결과는 아니다.',
'- off-on의 77.48ms max는 실제 관측치다. outlier로 제거하거나 p95로 대체하지 않았다.',
'- use_ort=false에서는 같은 YOLOv8n의 출력이 decoded tensor에서 4개 NPU tensor로 바뀌어 현재 후처리 계약과 맞지 않았다. 이 실패 실행은 주 비교에서 제외했다.',
'- 고정 샘플의 SDK 변형별 추론은 종료 코드 0이었다. 모두 검출 0개인 샘플이므로 검출 결과 비교는 제한적이며 정확도 동등성의 증거로 사용하지 않는다.',
'', '## 입력 크기 비교',f"- 640×640: {row(base)}",f"- 640×480: {row(rect)}",
f"- 전처리 {base['preprocess_ms']:.3f}→{rect['preprocess_ms']:.3f}ms ({resolution['preprocess_ms']:.1f}% 감소), NPU core {base['npu_ms']:.3f}→{rect['npu_ms']:.3f}ms ({resolution['npu_ms']:.1f}% 감소).",
f"- p95 {base['e2e_p95_ms']:.2f}→{rect['e2e_p95_ms']:.2f}ms ({resolution['e2e_p95_ms']:.1f}% 감소), 관측 max {base['e2e_max_ms']:.2f}→{rect['e2e_max_ms']:.2f}ms.",
'- 기존 640×640 전처리는 resize 없이 상하 padding을 추가한다. 640×480에서는 padding도 생략하며 동일 크기 전용 cvtColor 경로를 사용한다. 전처리 구현 경로와 출력 버퍼 처리도 달라진다. NPU 입력 면적은 25% 줄어든다.',
'- 선택한 두 YOLO26s DXNN은 입력 형상과 컴파일 산출물이 다르다. 동일 학습 checkpoint·양자화 조건의 완전한 동등성은 입증하지 못했다. 따라서 배포 입력 구성 간 비교로 제시하며 전체 이득을 padding 제거 하나의 효과로 귀속하지 않는다.',
'', '## 복구·운용 상태',
'- 시스템 /usr/local/lib/libdxrt.so와 원본 dxrt.cfg.cmake의 SHA256은 실험 전후 동일하다. 원본 두 가속 옵션은 ON이며, 설치 SDK로 재확인 실행도 정상 종료했다.',
'- 기존 model-bank tracking server는 사용자 요청으로 종료했고 /home/orangepi/lwir_keepalive.pause를 유지했다. 자동 재시작을 재개하지 않았다.',
'- GUI 확인은 설치 SDK로 5초 측정 구간에서 정상 종료했다. PC 수신·화면 동기화의 종단 검증은 수행하지 않았다.',
'- 원본 runtime 작업 트리의 기존 untracked 파일은 보존했다. 실험 복사본과 SDK 변형은 보드 /tmp/lwir-perf-20261116에 남아 있다.',
'', '## 산출물',
'- summary.csv / per-run.csv / summary.json — 집계와 반복별 값',
'- validation-measurements.json — 32개 유효 실행의 frame ID·timestamp·원본 tracking CSV 대조',
'- results/* — 각 실행 YAML, 로그, telemetry.csv, manifest, 라이브러리 maps·hash, 온도·장치 상태',
'- samples / parity — 실제 카메라 샘플과 SDK별 출력 검사 결과',
'- source / runner.py / analyze.py / sdk/*/CMakeCache.txt — 실험 계측과 빌드 조건']
(ROOT/'measurements/performance-report.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(quality,indent=2))
