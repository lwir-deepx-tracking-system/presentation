# Orange Pi 파이프라인 성능 비교

## 실행과 계측
- 보드 main 0fe016f7edd069900457a746dc4cc787569c5ae6의 격리 복사본을 사용했다. WSL의 runtime 작업 트리를 수정하지 않았다.
- Orange Pi 5 Plus / RK3588, DEEPX M1, RT 3.4.2 계열, driver 2.6.0, firmware 2.7.4. 상세 환경은 environment.txt에 있다.
- core 모드, GUI·짐벌 OFF, 동일 ByteTrack, NPU_ALL, buffer_count 6. ORT 비교 외에는 use_ort=false다.
- 카메라 첫 프레임 이후 5초 준비하고 15초 측정했다. 주 비교 10조건 × 3회 = 30회, 추가로 설치 SDK 재확인과 GUI 송신 확인을 수행했다.
- 실제 입력은 실행별 약 16.87~20.80 FPS였다. 따라서 이 시험은 30Hz 입력 유지나 NPU 최대 처리량을 검증하지 않는다.
- 실제 카메라 고정 샘플 20장의 검출 결과는 0개다. 사용자 요청에 따라 파이프라인 성능만 평가했다. 객체가 많은 장면의 NMS·추적 부하는 대표하지 않는다.
- 평균·p50·p95는 반복별 값의 평균이다. max는 같은 조건 3회에서 관측한 전체 최댓값이며 관측 시간은 조건별 45초다.
- 지연은 캡처 완료부터 추적 완료 계측 시점까지다. 센서 노출·PC 표시 지연은 포함하지 않는다.
- FPS는 측정 구간 안의 완료 개수/15초다. 지연·누락은 측정 구간에 캡처한 프레임 집합을 종료 후 완료 기록과 대응시켰다.
- CPU는 1코어 100% 기준의 프로세스 CPU 시간이다. RSS는 호스트 메모리다. SDK job latency 안에 NPU 시간이 포함되므로 둘을 합산하지 않는다.
- 동일 계측을 모든 조건에 적용했다. 계측 이벤트는 메모리에 보관하고 종료 후 기록했다. 계측 오버헤드 자체의 별도 정량 검증은 수행하지 않았다.

## 비동기·inflight 비교
| 조건 | 입력 FPS | 완료 FPS | 평균 ms | p95 ms | 관측 max ms | CPU % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| serial640 | 18.67 | 18.69 | 20.67 | 23.97 | 32.61 | 20.1 |
| async1 | 18.36 | 18.38 | 21.30 | 24.34 | 45.30 | 20.2 |
| async4 | 18.67 | 18.64 | 20.15 | 23.36 | 28.54 | 20.0 |
| async6 | 19.04 | 19.02 | 21.22 | 23.67 | 40.50 | 22.3 |

- serial640은 동일 RunAsync 경로에서 매 제출 후 wait_idle을 호출한 요청 중첩 OFF 조건이다. 동기 Run API 자체의 비교가 아니다.
- max_inflight는 애플리케이션의 미완료 요청 상한이다. buffer_count 또는 코어 개수와 구분한다.
- 카메라 공급 FPS와 완료 FPS가 가깝고 반복 간 입력 변동도 있다. 이 자료로 비동기 처리량의 배수 증가를 주장하지 않는다.
- 세 반복에서 추적 완료 누락은 0%였다. 관측 max는 1·6 조건에서 33.3ms를 넘었으므로 p95만으로 지연 상한을 판단하지 않는다.

## SDK 가속 2×2 비교
YOLOv8n 640×640, use_ort=true, inflight 6. Format/CPU 옵션은 프로세스별 별도 libdxrt.so로 바꾸고 /proc/PID/maps와 hash를 기록했다.
| Format / CPU | output format ms | CPU task ms | 평균 ms | p95 ms | 관측 max ms | CPU % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| off-off | 1.762 | 1.925 | 18.91 | 20.98 | 27.15 | 30.4 |
| off-on | 1.945 | 1.151 | 16.19 | 17.98 | 77.48 | 28.8 |
| on-off | 1.116 | 1.212 | 15.68 | 19.48 | 26.69 | 26.1 |
| on-on | 0.920 | 1.269 | 15.62 | 17.14 | 28.18 | 23.8 |

- 별도 YOLO26s 비교에서 format OFF→ON의 output-format 평균은 1.633→0.630ms, 약 61.4% 감소했다. 이 비교는 CPU 작업이 없는 모델에서 format 효과를 분리한 것이다.
- XNNPACK과 NEON 관련 빌드 경로 및 강제 활성 옵션을 확인했다. CPU task 구간의 ON/OFF 효과는 format 조합별로 다르며 모든 지표가 단조 개선되는 결과는 아니다.
- off-on의 77.48ms max는 실제 관측치다. outlier로 제거하거나 p95로 대체하지 않았다.
- use_ort=false에서는 같은 YOLOv8n의 출력이 decoded tensor에서 4개 NPU tensor로 바뀌어 현재 후처리 계약과 맞지 않았다. 이 실패 실행은 주 비교에서 제외했다.
- 고정 샘플의 SDK 변형별 추론은 종료 코드 0이었다. 모두 검출 0개인 샘플이므로 검출 결과 비교는 제한적이며 정확도 동등성의 증거로 사용하지 않는다.

## 입력 크기 비교
- 640×640: 19.02 FPS / p95 23.67 ms / max 40.50 ms / CPU 22.3%
- 640×480: 18.91 FPS / p95 17.96 ms / max 29.56 ms / CPU 19.6%
- 전처리 1.653→1.328ms (19.7% 감소), NPU core 13.035→9.675ms (25.8% 감소).
- p95 23.67→17.96ms (24.1% 감소), 관측 max 40.50→29.56ms.
- 기존 640×640 전처리는 resize 없이 상하 padding을 추가한다. 640×480에서는 padding도 생략하며 동일 크기 전용 cvtColor 경로를 사용한다. 전처리 구현 경로와 출력 버퍼 처리도 달라진다. NPU 입력 면적은 25% 줄어든다.
- 선택한 두 YOLO26s DXNN은 입력 형상과 컴파일 산출물이 다르다. 동일 학습 checkpoint·양자화 조건의 완전한 동등성은 입증하지 못했다. 따라서 배포 입력 구성 간 비교로 제시하며 전체 이득을 padding 제거 하나의 효과로 귀속하지 않는다.

## 복구·운용 상태
- 시스템 /usr/local/lib/libdxrt.so와 원본 dxrt.cfg.cmake의 SHA256은 실험 전후 동일하다. 원본 두 가속 옵션은 ON이며, 설치 SDK로 재확인 실행도 정상 종료했다.
- 기존 model-bank tracking server는 사용자 요청으로 종료했고 /home/orangepi/lwir_keepalive.pause를 유지했다. 자동 재시작을 재개하지 않았다.
- GUI 확인은 설치 SDK로 5초 측정 구간에서 정상 종료했다. PC 수신·화면 동기화의 종단 검증은 수행하지 않았다.
- 원본 runtime 작업 트리의 기존 untracked 파일은 보존했다. 최초 실험의 /tmp 복사본·SDK 변형은 이후 보드 재부팅으로 삭제됐다. 원본 자료는 WSL에 보존했고 제어 입력 재시험용 복사본을 다시 만들었다.

## 산출물
- summary.csv / per-run.csv / summary.json — 집계와 반복별 값
- validation-measurements.json — 32개 유효 실행의 frame ID·timestamp·원본 tracking CSV 대조
- results/* — 각 실행 YAML, 로그, telemetry.csv, manifest, 라이브러리 maps·hash, 온도·장치 상태
- samples / parity — 실제 카메라 샘플과 SDK별 출력 검사 결과
- source / runner.py / analyze.py / sdk/*/CMakeCache.txt — 실험 계측과 빌드 조건

## 제어 입력 재시험 추가

실카메라 입력이 부족했던 비동기·inflight 비교를 30·60·120fps의 실제 프레임 메모리 재생 36회로 보완했다. 기존 표는 실카메라 저부하 기록으로 보존하며, 발표 P1·P2는 재시험 결과를 사용한다. [재시험 보고서](orangepi-20261116-retry/report.md)에서 원본과 조건별 처리량·누락·p95·max를 확인한다.
