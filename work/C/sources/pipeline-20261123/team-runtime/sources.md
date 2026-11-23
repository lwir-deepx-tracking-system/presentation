# 구현 근거

| 발표 내용 | 코드 근거 |
| --- | --- |
| 독립 thread와 큐 연결 | apps/runtime/runtime.cpp, apps/runtime/runtime_workers.cpp |
| 카메라 입력 최신 2개 | src/pipeline/camera_thread.cpp — push_latest(message, 2) |
| 탐지 결과 제출 순서 복원 | src/pipeline/detection_thread.cpp — completed_results, next_output_sequence |
| 탐지 → 추적 FIFO | src/pipeline/detection_thread.cpp — output_queue.push |
| 제어 최신 1개 / GUI 최신 2개 | src/pipeline/tracking_thread.cpp — push_latest |
| 오래된 항목 제거 | include/common/threadsafequeue.hpp — push_latest |
| 원본 프레임의 수명 공유 | include/common/frame.hpp — FrameContextPtr |

담당 커밋의 카메라 큐 제한은 8c54a4d에서 확인된다. 현재 통합 코드의 Control·GUI 큐 정책도 함께 반영했다. 구성도는 논리적인 실행 경로를 요약하며 SDK와 미디어 프레임워크 내부 thread를 모두 나타내지 않는다.

전달 정책은 최신성과 순서에 대한 설계 선택이다. 모든 큐의 용량 제한, 전체 지연 상한, 처리 성능 향상을 측정한 결과로 확대하지 않는다. 본 작업의 확인 범위는 코드 대조와 HTML/PDF 렌더링이며 실제 NPU 실행·성능은 미검증이다.

# 전체 시스템 구성 근거

- src/camera/camera.cpp, cmake/I3System.cmake — i3system 열화상 카메라의 USB 연결
- include/common/frame.hpp — 640×480 CV_16UC1 원본 입력
- src/detection/dxrt_detection_pipeline.cpp — 보드에서 NPU 엔진 생성 및 비동기 추론 요청
- docs/network_setup.md — PC와 Orange Pi의 Ethernet 연결
- docs/pc_communication.md — 영상·메타데이터·명령 경로
- config/runtime.yaml, docs/auto_control.md — Serial 짐벌 제어와 선택 ID 기반 제어

NPU 연결은 현재 프로젝트 장비의 PCIe 기반 구성을 설명한다. 짐벌에서 카메라로 향하는 점선은 물리적인 관측 방향 변경이며 센서 데이터 반환 연결을 뜻하지 않는다. 실제 장치 사진이 제공되지 않아 역할·연결 도식으로 표현했다.

# 08 전처리·후처리 근거

- src/detection/lwir_preprocessor.cpp — CV_16UC1 검증, clip 범위의 8-bit 변환, 3채널 복제, 생성 시 공간 변환 경로 선택
- include/detection/i_preprocessor.hpp — scale, pad_x/pad_y, 원본·모델 입력 크기를 담는 PreprocessContext
- config/detection/yolov8n.yaml — 원본 640×480, 모델 640×640, pad_value 114 예시
- src/detection/yolo_postprocessor_core.cpp — confidence 필터, 설정 기반 NMS, padding 제거·scale 역변환·원본 경계 제한

# 12 PC·통신 근거

- src/gui/gui_sender.cpp — 프레임별 PTS 생성, RTP와 메타데이터 timestamp 대응, 원본 frame ID 전달
- src/gui/gui_protocol.cpp — 메타데이터 인코딩과 ACK/STATUS 형식
- src/control/tracking_command_handler.cpp — 표적 선택, AUTO/MANUAL, 상태 변화 응답
- docs/pc_communication.md, config/runtime.yaml — RTP/UDP 5000, metadata UDP 5001, command TCP 5002

현재 검토는 보드 런타임 코드와 통신 계약에 근거한다. PC 실제 소스나 화면 동작은 직접 검증하지 않아 GUI 기능을 역할 관계도로 표현했다. HOME 완료나 MOVE의 ACK, 모델 전환 UI 구현을 주장하지 않는다. 영상·메타데이터의 실제 도착 지연·누락 처리 결과와 NPU tensor 실행 검증도 미검증이다.

# 실측 성능 비교 P1–P4

2026.11.16 Orange Pi main 0fe016f7edd069900457a746dc4cc787569c5ae6의 격리 복사본에서 실제 카메라와 DEEPX M1으로 측정했다. 기존 슬라이드 제작 당시 미검증 범위와 이번 실제 실행 결과를 구분한다.

- 원본과 실행 조건 — measurements/orangepi-20261116/results
- 반복별 통계 — measurements/orangepi-20261116/per-run.csv
- 조건별 통계 — measurements/orangepi-20261116/summary.csv
- 계측 대조 — measurements/orangepi-20261116/validation-measurements.json
- 긴 지연의 원본 프레임 — measurements/orangepi-20261116/tail-latency-example.json
- SDK 보존 확인 — measurements/orangepi-20261116/sdk-restoration.txt
- 상세 해석 — measurements/performance-report.md

실험용 변경은 perf_experiment.hpp, camera_thread/detection_thread/tracking_thread 계측과 parity 도구다. 기존 runtime·SDK 설치 파일의 작업 트리는 보존했다. 추가 보고서·슬라이드 생성 스크립트는 measurements/scripts에 포함한다.

# 제어 입력 재시험

P1·P2의 수치는 measurements/orangepi-20261116-retry/replay-summary.csv와 replay-summary.json에서 가져왔다. 36회 실행의 원본 CSV·YAML·로그·maps·hash·소스 공급 예정/실제 시각을 보존했다. 검증 결과는 replay-validation.json이다. 입력 교체·계측 소스와 재현 스크립트는 해당 폴더 source 및 scripts에 포함한다. 마지막 0.5초 경계 보호는 누락률에만 적용하며 지연 max는 전체 측정 구간에서 완료된 프레임을 사용한다.
