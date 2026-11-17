"""Write the controlled-load report from completed measured runs, with original camera results retained."""
from pathlib import Path
import json,statistics
root=Path('/home/user/workspace/mypresentaion/v4');d=root/'measurements/orangepi-20261116-retry'
s=json.loads((d/'replay-summary.json').read_text());runs=s['runs'];summary=s['summary'];r={(x['tag'],x['case']):x for x in summary}
assert len(runs)==36 and all(x['repeats']==3 for x in summary)
lines=['# 제어 입력 부하 재시험 — 2026.11.16','','## 실카메라 재확인',
'- 보드 재부팅 후 추론·큐 없이 카메라 SDK 수신만 재측정했다. 각 모드는 3초 준비 후 15초 수신했다.',
'- AGC ON: 성공 326장 / 15.014초 = 21.7131fps, SDK 반환 코드 4는 325회. AGC OFF: 성공 264장 / 15.005초 = 17.5941fps, 반환 코드 4는 429회다.',
'- SDK 헤더에서 4는 Data read fail이다. 이 횟수를 누락 프레임 수로 환산하지 않는다. 수신 시도 실패와 센서 프레임 손실은 같은 지표가 아니다.',
'- 현재 공개 헤더의 GetLastUsbDiagnostic 설명은 scan/open 진단이다. RecvImage 실패의 USB 원인을 이 인터페이스로 확정하지 않았다.',
'- 따라서 카메라의 명목 하드웨어 한계로 단정하지 않으며, 실제 카메라 입력 30fps 확보는 미해결이다. SDK 내부 전처리·USB 수신 경로·카메라 설정은 추가 원인 분석 대상이다. FOR_INTERNAL의 SetFrameRate는 공개 API가 아니므로 임의 호출하지 않았다.',
'','## 부하 시험 방법',
'- 보드 main 0fe016f7edd069900457a746dc4cc787569c5ae6의 별도 복사본에서 카메라 입력만 실험용 메모리 재생으로 교체했다. 원본 runtime 파일은 변경하지 않았다.',
'- 이전 실제 카메라에서 저장한 640×480 CV_16UC1 PNG 20장을 시작 시 메모리에 모두 읽고 반복 공급했다. 20개 저장 파일은 SHA256이 모두 같아 단일 고정 프레임 반복에 해당한다. 영상 내용의 다양성을 검증한 시험이 아니다. 입력과 추론 결과를 합성하지 않았다. 실행 중 프레임 읽기 디스크 I/O는 없다.',
'- 소스는 steady_clock의 절대 예정 시각으로 30·60·120fps를 공급하고 예정/실제 공급 시각을 replay-source.csv에 저장했다. 이미지 복사 완료 후 기존 CameraThread가 frame ID·captured_at을 부여했다.',
'- 같은 YOLO26s 640×640 DXNN, use_ort=false, NPU_ALL, buffer_count 6, ByteTrack, GUI·짐벌·ReID OFF, 같은 설치 SDK를 사용했다. 모델·라이브러리 SHA256과 maps를 실행별 보관했다.',
'- 완료 대기는 동일 submit_async 경로에서 매번 wait_idle을 호출한 요청 중첩 OFF 조건이다. SDK의 별도 동기 Run API와 비동기 RunAsync API 자체를 비교한 시험이 아니다.',
'- inflight 1·4·6은 미완료 요청 상한을 바꾼다. 코어 개수를 바꾸는 설정이 아니다.',
'- 각 실행 5초 준비 + 15초 측정, 12조건 × 3회 = 36회다. 반복별 입력 속도 순서와 제출 조건 순서를 회전시켰다.',
'- FPS는 측정 구간 안의 완료 건수/15초다. 누락률의 프레임 집합은 측정 구간 시작부터 종료 0.5초 전까지 공급한 frame ID다. SIGINT 직전 큐의 취소를 정상 운용 누락으로 섞지 않도록 모든 실행에 같은 500ms 경계 보호를 적용했다. 이 집합에서 정상 종료 후에도 추적 완료가 없는 비율을 누락률로 계산한다. 창 경계의 결과 완료 시점 차이로 FPS 기반 비율과 아주 조금 다를 수 있다.',
'- 지연은 15초 측정 구간에 공급하고 추적이 완료된 프레임의 입력 준비 완료부터 추적 완료 계측 시각까지다. 평균·p95·max에는 종료 전 0.5초도 모두 포함한다. 캡처 API·센서 노출·네트워크·PC 표시 지연은 제외한다. 과부하에서 누락된 프레임에는 완료 지연이 없으므로 지연과 누락을 함께 평가한다.',
'- 평균·p95는 반복별 값의 평균, max는 3회 전체 관측 최댓값이다. FPS·지연 관측은 조건별 합계 45초, 누락 프레임 집합은 합계 43.5초이며 영구적인 지연 상한 보장이 아니다.',
'','## 결과',
'| 요청 입력 FPS | 제출 조건 | 실제 입력 FPS | 완료 FPS | 누락 % | 평균 ms | p95 ms | max ms | CPU % |',
'|---:|---|---:|---:|---:|---:|---:|---:|---:|']
labels=[('serial640','완료 대기'),('async1','inflight 1'),('async4','inflight 4'),('async6','inflight 6')]
for fps in [30,60,120]:
 for case,label in labels:
  x=r[(f'replay{fps}',case)]
  lines.append(f"| {fps} | {label} | {x['camera_fps']:.2f} | {x['tracking_fps']:.2f} | {x['drop_pct']:.2f} | {x['e2e_mean_ms']:.2f} | {x['e2e_p95_ms']:.2f} | {x['e2e_max_ms']:.2f} | {x['cpu_core_pct']:.1f} |")
a=r[('replay60','serial640')];b=r[('replay60','async6')]
lines+=['','## 해석',f"- 60fps 입력에서 완료 대기 {a['tracking_fps']:.2f}fps → inflight 6 {b['tracking_fps']:.2f}fps. 이 조건의 관측 완료 처리량 비율은 {b['tracking_fps']/a['tracking_fps']:.3f}배다. 일반적인 속도 향상 배수나 최대 처리 능력으로 확장하지 않는다.",
'- 요청 중첩으로 NPU 처리 중 다음 프레임의 준비·제출을 진행할 수 있다. 유입 속도가 처리 능력을 넘으면 최신 프레임 큐의 누락 정책이 동작하므로, 처리량과 완료된 프레임의 지연만 단독으로 최적화하면 안 된다.',
'- inflight 값 증가에 비례한 개선을 가정하지 않는다. 4와 6 중 선택은 실제 처리량·지연·누락 결과를 함께 본다.',
'- 이 시험은 입력이 충분한 상태의 실제 NPU 파이프라인 처리 능력을 비교한다. 실카메라·GUI·짐벌을 모두 켠 통합 운용 30fps 달성의 증거는 아니다.',
'- 프레임 20장은 기존에 검출 객체 0개로 확인된 장면이다. 사용자 요청에 따라 파이프라인 성능에 집중했으며 객체가 많은 장면의 후처리·추적 부하는 대표하지 않는다.',
'','## 검증과 원본',
f"- {len(runs)}회 실행 모두 정상 종료했고, 실제 입력 FPS는 요청값의 2% 이내다. 단계별 frame ID 중복·음수 지연이 없고 tracking ⊆ detection ⊆ submit ⊆ camera를 확인했다.",
f"- 모든 실행의 동일 모델 SHA256: `{runs[0]['model_sha256']}`.",
f"- 소스 공급 지각의 관측 max: {max(x['source_lateness_max_ms'] for x in runs):.3f}ms. 소스의 예정/실제 시각은 inference 지연과 별도로 저장했다.",
'- replay-summary.csv / replay-per-run.csv / replay-summary.json / replay-validation.json에 집계와 검증 결과가 있다.',
'- results/*에 runtime YAML·로그·telemetry·프로세스 CPU/RSS·라이브러리 maps/hash·replay-source.csv가 있다. source와 scripts에 입력 교체 및 계측 코드를 보관했다.',
'- 기존 실카메라 SDK 2×2 및 입력 형상 비교 결과는 ../performance-report.md의 원래 결과로 남겨 둔다. 이 재생 시험과 원시 표본을 섞어 평균내지 않는다.',
'- 시스템 SDK를 교체하지 않았고 tracking server 자동 시작 차단 파일을 유지했다. 이번에 재생성한 /tmp 실험 복사본은 재부팅 시 삭제될 수 있으므로 WSL 산출물에 원본을 복사했다.']
(d/'report.md').write_text('\n'.join(lines)+'\n')
main=root/'measurements/performance-report.md';text=main.read_text().split('\n## 제어 입력 재시험 추가')[0]
text+='\n## 제어 입력 재시험 추가\n\n실카메라 입력이 부족했던 비동기·inflight 비교를 30·60·120fps의 실제 프레임 메모리 재생 36회로 보완했다. 기존 표는 실카메라 저부하 기록으로 보존하며, 발표 P1·P2는 재시험 결과를 사용한다. [재시험 보고서](orangepi-20261116-retry/report.md)에서 원본과 조건별 처리량·누락·p95·max를 확인한다.\n'
main.write_text(text)
print(d/'report.md')
