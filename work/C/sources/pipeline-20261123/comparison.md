# 멀티스레드 파이프라인 대조

2026-11-23 코드 열람. 실제 장치 실행·설정 조회·성능 재시험은 수행하지 않았다.

모델뱅크 기준 커밋: `549324ca4218f9bdd504e6b6218a28278e1c585a`.
김재남 원본은 presentation `2a34969`의 자료이며 복사본은 team-runtime/에 보존한다.

## 대조 결과

| 항목 | 김재남 자료의 팀 C++ Runtime | 모델뱅크 코드 | 발표 반영 |
|---|---|---|---|
| 작업 분리 | Camera·Detection·Tracking·Control·GUI 독립 작업 | 카메라 reader, npu-feed, 메인 추적 루프, 브리지 writer/reader | 작업을 겹치는 개념만 참고하고 서버 실제 분담으로 재작성 |
| 카메라 대기 | 최신2 | LIVE.q maxlen3. 수신 시 가장 오래된 항목 제거. Feed busy/auto에서 최신1로 정리 | 최대3·밀리면 최신1. 실카메라 Feed 경로로 범위 명시 |
| 추적 입력 | 제출 순서 복원 후 FIFO, 결과 큐 무제한 | Feed.out에 append, _next에서 popleft. seq 단조성 검사·order_bad 계수 | 제출 순서 유지. Runtime 큐 용량을 이식하지 않음 |
| 제어 관측 | 최신1 | GB.wframe 미전송 한 슬롯 교체 | 최신 관측 한 건. 별도 명령·증거 프레임·barrier는 예외 |
| GUI | 최신2 | 앱의 picture lane 협상 시 별도 writer/한 슬롯, 기존 결합 경로는 fallback | 웹 GUI와 GUI 큐 개수는 두 장에서 제외 |
| 두 NPU 결과 회수 | 별도 시험·구현 | C++ worker는 parallel-wait 설정 활성 시 생성 | 항상 활성인 기본 스레드로 그리지 않음 |

## 코드 근거

- `tracking_server/src/app.py:497`: `deque(maxlen=3)` 초기화.
- `src/camera/camera_link.py:35–83`: 수신·초과 제거·reader thread.
- `src/detect/frame_feed.py:257–284`: 모드와 호환 조건에 따른 Feed 활성·fallback.
- `src/detect/frame_feed.py:324–352`: 결과 deque와 npu-feed thread.
- `src/detect/frame_feed.py:382–464`: 입력 정리·전처리·제출·회수·결과 전달. 440–445는 이전 추적 중 타일 회수 겹침.
- `src/detect/frame_feed.py:692–741`: 제출 결과의 순서 소비와 seq 검사.
- `src/gimbal/gimbal_link.py:124–158`: 별도 명령 큐와 미전송 최신 관측 슬롯. gb_send의 일반 명령 거부 임계64를 모든 경로의 전역 상한으로 설명하지 않는다.
- `src/gimbal/gimbal_link.py:201–214,416`: writer 소비와 writer/reader 생성.
- `src/gimbal/live_tracks.py:695–826`: 추적 관측의 브리지 전달. 신원 전환 증거 프레임은 별도 큐에 보존된다.
- `src/detect/split_native.py:13–21,71–75`: 파일 또는 환경변수로 병렬 wait 활성 선택.
- `src/detect/split_sdk.cpp:191–202,254–306`: 옵션 시 작업 스레드 생성·두 코어 회수.

위 src 상대경로의 공통 접두사는 tracking_server/이다. 줄 번호는 동결 커밋 기준.

## 적용 범위

실시간 입력을 버리는 정책은 목표 ‘입력 버림0’의 달성을 뜻하지 않는다. lossless 재생에서는 별도 정책을 쓴다. 구조를 설명하는 개념도 칸 폭은 실측 시간·성능 개선 배수가 아니다. 소프트웨어 작업 겹침과 두 NPU 장치 병렬 실행을 구별한다. Python thread 전체를 CPU 코어별 동시 실행으로 설명하지 않는다. 실제 데모의 런처·모델·Feed 모드·브리지 협상 상태는 계속 확인 대상이다.

김재남 원도의 작업 분담과 큐 정책 설명 순서를 참고했으며, 단계를 모두 독립 C++ thread로 표현한 기존 그림을 모델뱅크 구조로 복제하지 않았다. 신규 8·9장은 모델뱅크 서버 구조, 앞 7장은 팀 공통 C++ Runtime 모듈 구성이다.
