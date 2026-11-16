# 모델뱅크 GUI·제어와 기존 PC 앱 비교

분석일: 2026-11-16. 발표 10·12번과 시스템·송신·시험 설명의 기준을 정하기 위한 코드 분석이다.

## 결론

모델뱅크에 별도의 **브라우저 GUI + Python 실시간 서버 + C++ 짐벌 브리지**가 있다. 기존 Qt PC 앱의 UI 코드를 그대로 이식한 형태는 아니다. 기존 Runtime의 제어·장치·PC 통신 코드를 가져와 새 Python 파이프라인에 연결했고, 웹 화면과 별도로 기존 Qt PC 앱 연결도 지원한다.

따라서 “기존 코드 기반”은 제어·통신 재사용 관점에서 확인된다. 웹 GUI 전체와 새 추적·재생·연구 기능까지 기존 PC 앱의 구현으로 설명하면 기여 범위를 과장하게 된다.

발표가 이 웹 GUI를 기준으로 진행된다면 현재 12번의 Qt 화면과 기능 설명은 교체해야 한다. 10번도 P 제어·BBox 중심이라는 설명을 해당 실행 설정에 맞춰 고쳐야 한다. 단, 실제 발표에 사용할 브리지와 옵션은 저장소 기본값만으로 확정할 수 없다.

## 확인한 기준

| 저장소 | 분석 기준 |
| --- | --- |
| model-bank | main 스냅샷 `5ea5b64bcf2be43cc74e30e7ea8492b22d081a11` |
| pc-application | main `8e91e3eb562a56f9fad159fdf69aec6603d2beb0`; 로컬 HEAD와 원격 일치 확인 |
| runtime 현재 main | `0fe016f7edd069900457a746dc4cc787569c5ae6` |
| model-bank가 기록한 원본 | Runtime `5219bce4abb5dbf5ec7a39c5ed1e7bd319dd57fa` |

방법: GitHub 트리와 파일을 위 커밋에 고정해 읽고, 관련 Git blob SHA를 비교했다. 원문은 `.cache/model-bank-audit/`에 분석용으로 보관했다. 장치 접속·실제 실행 설정 조회·빌드·하드웨어 시험은 하지 않았다. 문서의 장치 시험 결과는 해당 작성자의 기록이며 이번 분석에서 재현한 결과가 아니다.

## 1. 기존 코드의 재사용을 확인한 근거

`tracking_server/src/gimbal/team/SOURCE.txt`는 Runtime `5219bce`에서 제어·GUI 코드를 가져왔다고 명시한다. 주석에만 의존하지 않고 저장소의 Git blob SHA도 대조했다.

| model-bank의 team/ 아래 파일 | Runtime 5219bce와 비교 | 현재 Runtime main과 비교 |
| --- | --- | --- |
| src/control/auto_tracking_controller.cpp | 동일 | 동일 |
| src/control/gimbal_command_executor.cpp | 동일 | 동일 |
| src/control/gimbal_device.cpp | 동일 | 동일 |
| src/control/tracking_command_handler.cpp | 동일 | 동일 |
| src/gui/gui_command_handler.cpp | 동일 | 동일 |
| src/gui/gui_protocol.cpp | 동일 | 동일 |
| src/gui/gui_receiver.cpp | 동일 | 동일 |
| src/gui/gui_sender.cpp | 동일 | 동일 |
| src/control/pid_controller.cpp | 변경됨 | 변경됨 |

이 표의 동일은 파일 전체 blob SHA 일치다. 헤더나 저장소 전체가 모두 같다는 의미는 아니다. PID 코드는 관측 기반 미분 입력을 받는 오버로드가 추가됐다. Track 쪽에도 lead·aim_y 확장이 기록돼 있다. v27 전용 제어기와 실행기는 team/ 원본과 별도 파일이다.

발표에서 가능한 표현: **“기존 제어기·장치 실행 경계와 PC 통신 규격을 유지하면서 웹 운용 화면과 실시간 서버에 연결했다.”**

원문: [SOURCE.txt](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/gimbal/team/SOURCE.txt)

## 2. 실행 구조가 달라진 점

기존:

```text
PC Qt UI → ControlClient → TCP 5002 → Runtime 명령 처리 → 제어 실행기 → Serial
PC VideoReceiver ← RTP 영상 UDP 5000
PC MetadataReceiver ← Track 메타데이터 UDP 5001
영상·메타데이터는 PC FrameSynchronizer에서 RTP timestamp로 대응
```

모델뱅크:

```text
PC/휴대폰 브라우저 ← HTTP 8090 → Python tracking_server
    영상: /stream (JPEG multipart)
    명령: POST /gimbal/click, /gimbal/move, /gimbal/stop
    상태: /gimbal/ping, /gimbal/people, /healthz, /model, /rules, /perf
                                     ↓ stdin/stdout 파이프
                             C++ gimbal_bridge_v25 또는 v27
                                     ↓ 제어 실행기·장치 어댑터
                                  USB Serial 짐벌

기존 Qt PC 앱 ←→ C++ 브리지의 GuiSender / GuiReceiver (선택적 병행 경로)
```

웹 경로에는 기존 PC의 UDP 메타데이터 수신·RTP 동기화 클래스가 그대로 사용되지 않는다. 브리지는 선택 ID와 상태·명령을 기존 실행기에 연결한다. 기존 PC가 요청한 모델 전환은 브리지의 ModelRequests가 Python 모델 관리로 넘기고 완료 결과를 다시 전달한다.

원문: [웹 HTTP 처리](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/web/page_handler.py), [v25 브리지](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/gimbal/gimbal_bridge_v25.cpp)

## 3. GUI의 구체적인 차이

| 항목 | 기존 Qt PC 앱 | 모델뱅크 웹 GUI |
| --- | --- | --- |
| 실행 | Windows Qt 애플리케이션 | 보드 Python 서버 + PC/휴대폰 브라우저 |
| 영상 | JPEG/H.264 RTP 수신·디코딩 | HTTP JPEG multipart; fetch 파싱·blob 표시 또는 img 스트림 |
| 박스 | PC에서 RTP timestamp가 맞는 영상에 표시 | 보통 서버가 영상에 직접 그림; Picture First에서는 별도 SSE 결과를 canvas에 표시 |
| 표적 선택 | Track ID 입력/목록·영상 클릭 | 영상 클릭으로 서버가 ID 결정; 겹친 박스는 면적이 가장 작은 박스 선택 |
| 빈 영역 클릭 | 유효 객체를 선택하지 않음 | 선택 표적이 없는 위치 클릭은 정지 동작으로 이어짐 |
| 키보드 | 방향키, Space HOME 요청 | 방향키 + WASD, Space STOP |
| 휴대폰 입력 | 별도 터치 조이스틱 없음 | 영상 터치·드래그로 8방향 가상 조이스틱 |
| 입력 해제 | 키 해제·포커스 상실·연결 해제 처리 | 키 해제·blur·visibilitychange·pagehide·터치 종료 처리 |
| 연결 상태 | QTcpSocket·PING ACK·STATUS | HTTP 상태 조회·0.4초 heartbeat·영상 재연결 |
| 모델 | YAML 이름/ID + TCP 요청·결과 | 서버 카탈로그·현재 모델 조회, POST /model/set, 모델 계층 UI |
| 추적·전처리 설정 | 일반 GUI에서 제한적 표시/운용 | 설정 트리로 검출·추적·외형·필터·예측 등 옵션 조회·변경 |
| 재생·평가 | 기존 운용 앱에 같은 기능 없음 | 녹화 선택·재생·일시정지·프레임 이동·정답 비교·채점 |
| 계측 | PC 성능 CSV, 수신한 Runtime 표본의 별도 CSV | 측정 시작/종료·이력·메모, summary.json·timing.csv·추적 및 영상 기록 |

웹 HTTP 명령 성공과 실제 짐벌 동작 완료는 별개다. 웹의 비동기 브리지 상태 갱신과 기존 PC의 ACK/STATUS 의미를 같은 구현으로 설명하지 않는다.

구체적인 입력 차이:

- 기존 `ManualInputHandler.cpp`는 Space에서 `homeRequested()`를 발생시킨다.
- 웹 `03_gimbal_control.js`는 Space에서 `/gimbal/stop`을 호출한다. 브리지가 받는 `H`는 정지·선택 해제이며 원점 복귀가 아니다.
- 기존 `VideoWidget.cpp`는 박스가 여러 개 겹치면 선택을 보류한다. 웹 `live_tracks.hit_id()`는 면적이 가장 작은 박스를 고른다.
- 웹의 클릭은 비동기 프리뷰/Picture First 경로에서 보이는 박스의 snapshot·ticket을 참조하며, 오래된 영상이나 트래커 경계가 바뀐 상태의 잘못된 선택을 거절하는 검사가 있다.

원문: [웹 입력 처리](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/page/js/03_gimbal_control.js), [클릭·표적 전달](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/gimbal/live_tracks.py), [기존 PC 입력](https://github.com/lwir-deepx-tracking-system/pc-application/blob/8e91e3eb562a56f9fad159fdf69aec6603d2beb0/src/control/ManualInputHandler.cpp)

## 4. 영상·좌표·지연 설명에서 바뀌는 점

- 웹 보통 경로는 Track 박스를 서버에서 그린 JPEG를 보낸다. “PC가 별도 메타데이터를 수신해 RTP timestamp로 동기화한다”는 설명은 **기존 Qt 경로**에 해당한다.
- Picture First는 선택 기능이다. `LWIR_PICTURE_FIRST=1` 또는 실행 중 설정으로 켜며, 코드 기본값은 환경변수로 켜지 않으면 꺼짐이다. 실시간 카메라에만 적용하고 재생·안정화 등 조건에 따라 비활성화된다.
- 이 기능을 켜면 영상은 카메라 프레임 도착 직후 보내고, 박스는 검출·추적 후 `/overlay` SSE로 따로 보낸다. 브라우저는 늦게 도착한 박스를 overlay한다. **같은 프레임의 영상·박스 정합 보장과 영상 최신성 우선은 다른 정책**이다. 기존 동기화 설명을 그대로 쓰면 안 된다.
- 웹 스트림은 브라우저별 처리 경로가 다르다. fetch 가능한 브라우저는 JPEG comment의 프레임·시각을 읽고 대기 영상은 최신 하나를 유지한다. WebKit/iPhone 등은 img 스트림을 사용하고 그 경로의 지연 계측에는 제한이 있다.
- 내부 추적 좌표는 문서 기준 640×512이며, 표시·제어·기존 PC 전달에서는 640×480로 복원하면서 상하 16픽셀 패딩을 제거한다. 새 GUI 설명에 원본/내부 좌표를 혼합하지 않는다.
- 서버 처리시간·JPEG 준비시간·브라우저 표시 추정값은 기존 PC receive→paint와 관측 지점이 다르다. 기존 PC LWTM 통계를 그대로 웹 성능 지표라고 설명하지 않는다. 복사된 GUI 프로토콜 파일이 원본과 동일한 것도 확인됐다.

원문: [Picture First 서버](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/web/picture_first.py), [브라우저 overlay](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/page/js/picture_first.js), [브라우저 스트림](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/page/js/picture_stream.js)

## 5. 제어의 원본 유지·운용 변경·확장 기능

### 기본 v25와 공개 실행 스크립트

v25는 원본 AutoTrackingController, GimbalCommandExecutor, GimbalDevice를 연결한다. 핵심 계산·명령 직렬화·안전 정지 경계를 유지하면서 Python의 관측 결과와 웹/기존 PC 명령을 어댑터로 받는다.

공개 `run_real_gui.sh` 기준:

| 항목 | 현재 발표 초안/Runtime 기반 설명 | 모델뱅크 공개 스크립트 |
| --- | --- | --- |
| 제어 | P 제어 중심 설명 | `--controller pid --ki 0 --kd 6`, 기본 Kp 30 → 실질 PD |
| 조준점 | BBox 중심 | `aim_y=0.08`: BBox 위에서 8% 지점, 가로는 중심 |
| Deadband | 중앙 부근 정지 | 0.06 |
| 수동 속도 | Runtime 운용 설정에 따름 | 20 |
| AUTO 최고 속도 | Runtime 운용 설정에 따름 | 공개 스크립트 기본값 100 |
| 재획득 대기 | 제한 시간 후 선택 해제 | 공개 스크립트 기본값 10000ms |
| 브리지 | 기존 Runtime 통합 경로 | 기본 v25; 환경변수로 v27 선택 가능 |

`aimed()`는 제어에 전달할 BBox 중심만 이동시키고 GUI에는 원래 BBox를 보낸다. 조준점 변경을 검출 박스 자체를 이동한 것으로 설명하지 않는다.

이 표는 공개 스크립트의 기본값이다. `scripts/live.env`와 추가 옵션이 덮어쓸 수 있으므로 실제 보드 실행값으로 단정하지 않는다.

### v27 확장

v27은 별도 Controller·Executor를 사용한다. 관측 기반 미분, lead 적용 분리, 불감대 히스테리시스, 축별 반전 대기, 먼 오차 가속/접근 감속, 유실 시 예측 이동·탐색 등의 확장 코드가 있다. **코드 존재와 사용 중인 기능은 구분**한다.

- `arrival-control`: 현재 v27 브리지 기본 켜짐. 결과 도착 때 제어 계산을 수행하고 watchdog 등 시간 기반 처리는 계속 유지한다.
- `deadband-exit`, `axis-reversal`, `far-gain`, `brake`: 옵션 기본값에서는 해당 확장 효과가 꺼진 상태다.
- `coast`, `search`, `seek`, Follow Guard: 각각 조건·옵션으로 활성화한다. 문서는 seek의 장치 가상 카메라 비교에서 채택 기준을 충족하지 못해 꺼 두었다고 기록한다. 발표에서 “개선 기능으로 모두 적용 완료”로 묶지 않는다.
- 안전 STOP과 부드러운 일반 추종 정지 정책은 별개다. 표적/입력 상실·연결·오류 상황까지 무조건 감속 대기한다고 설명하지 않는다.
- Pan/Tilt 방향을 따로 계산해도 장치 명령은 공통 SPD다. 두 축의 물리 속도를 독립 제어한다고 말하지 않는다.
- v27 위치 눈금은 성공적으로 보낸 이동 명령을 적분한 추정값이며, 실측 엔코더 각도가 아니다.

원문: [공개 실행 스크립트](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/scripts/run_real_gui.sh), [v27 변경 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/gimbal/V27_CHANGES.md)

## 6. 시험 근거의 범위

기존 PC 앱의 Mock·프로토콜·수신·CSV 시험은 기존 PC 앱의 근거다. 새 웹 GUI가 같은 방식으로 검증됐다는 근거로 옮기지 않는다.

모델뱅크에는 다음 종류의 기록·시험 코드가 있다.

- 실제 카메라·짐벌 + 가상 표적을 이용한 PD 튜닝 기록. 검출된 실제 사람이 움직이는 시험과 다르다.
- Python 표적 전달·GUI 브리지·입력 처리 시험, 가상 Serial/PTY 시험, v27 실행기·관측·예측·탐색 시험.
- PC 시뮬레이션과 장치 가상 카메라 시험. 실제 움직이는 카메라의 번짐·기계 끝단·물리 정지 성능을 모두 대신하지 않는다.

특히 11월 10일 PD 튜닝의 AUTO 상한은 10이고 조준점은 0.3이었다. 이후 공개 실행 스크립트는 AUTO 상한 100·조준점 0.08이다. 옛 PD 튜닝 결과를 현 설정의 안정성 검증 결과로 그대로 사용하지 않는다.

원문: [PD 튜닝 조건·결과](https://github.com/lwir-deepx-tracking-system/model-bank/blob/5ea5b64bcf2be43cc74e30e7ea8492b22d081a11/tracking_server/src/gimbal/PID_TUNING_RECORD_20261110.md)

## 7. 발표 슬라이드 반영안

| 슬라이드 | 바꿀 내용 |
| --- | --- |
| 05 시스템 구성 | 브라우저 ↔ HTTP 웹 서버 ↔ C++ 브리지 ↔ 짐벌을 주 경로로 표시. 기존 UDP/TCP PC 앱 경로는 실제 사용 여부에 따라 보조 표시 |
| 10 표적 선택·짐벌 제어 | 실제 조준점, 실제 제어기 P/PD, 공통 SPD·상실·수동 개입을 설명. v27 기능은 실제 켠 옵션만 포함 |
| 11 실시간 처리·영상 송신 | 모델뱅크 파이프라인과 웹 JPEG 송신을 설명. Picture First를 쓴다면 영상 최신성·박스 지연의 절충을 명시 |
| 12 GUI·통신 | Qt Mock 캡처를 실제 발표용 웹 GUI 화면으로 교체. 클릭 표적 선택·상태·설정·재생·측정 중 핵심 3~4개만 설명 |
| 13 시험·성능 | 기존 PC 단독 시험과 모델뱅크 웹/제어 시험을 구분. 실제 실행 버전·설정과 일치하는 결과만 최종 수치로 사용 |

10번 핵심 문장 후보: **“선택 표적의 조준점 오차를 제어기로 보정하고, 수동 개입과 입력 상실에는 이동을 정지한다.”**

12번 핵심 문장 후보: **“웹 화면에서 표적 선택·짐벌 조작·설정·상태 확인을 통합했다.”**

후속 사용자 요청으로 5·10·11·12·13번 HTML/PDF와 발표 노트를 웹 GUI 기준으로 수정했다. 공개 스크립트의 PD·조준점과 실제 실행값을 구분하고, v25/v27·활성 옵션·최종 시험 성과는 확인 필요로 남겼다. 12번은 저장소의 합성 미리보기를 출처와 한계 표시와 함께 사용했다.

## 8. 발표용 기준을 확정할 때 확인할 것

1. 실제 실행 서버의 저장소 경로·커밋과 브리지 바이너리(v25/v27) 및 명령줄.
2. live.env·추가 옵션이 덮어쓴 Kp/Ki/Kd·aim_y·속도·재획득 시간.
3. 실제 GUI의 /rules·/model·/gimbal/people 상태: Picture First·예측·coast/guard 등의 활성값. 조회 시 제어 명령이나 heartbeat를 보내지 않는다.
4. 실제 운용 화면 캡처와 데모가 Qt/웹/병행 중 무엇인지.
5. 그 조건과 동일한 시험 로그를 10·13번의 성능 근거로 선별.

이 확인은 이번 분석에서 수행하지 않았다. 구현 비교 결과와 실제 장치 운용 결과를 구분한다.
