# 프로젝트 담당 슬라이드 v4

| 순서 | 전체 발표 페이지 | 내용 | 목표 시간 |
| --- | --- | --- | --- |
| 1 | 05 | 전체 시스템 구성 | 1분 20초 |
| 2 | 08 | 열화상 전처리·후처리 | 1분 10초 |
| 3 | 11 | 파이프라인·큐 정책 | 1분 |
| 4 | 12 | PC 애플리케이션·통신 | 1분 |

총 목표 시간은 4분 30초다. 각 장 원고와 검증 범위는 speaker-notes.html / speaker-notes.md에서 확인한다. 실제 낭독 속도로 최종 조정한다.

index.html은 오프라인 HTML이다. presentation.pdf는 1280×720 기준으로 슬라이드별 한 페이지인 8페이지 PDF다. 공통 slides.css와 로컬 Pretendard·공식 로고를 포함한다. slide-05.png, slide-08.png, slide-11.png, slide-12.png는 각 장 미리보기이고 overview.png는 모음이다. assets의 SVG는 편집 가능한 독립 구성도다.

코드 근거는 sources.md, 렌더링 검증 결과는 validation.json에 기록했다. PC 화면은 역할·통신 계약 도식으로 표현했다. 실제 GUI 화면 동기화는 미검증이다. NPU 실측 범위는 아래 추가 섹션과 측정 보고서에 명시했다. 작업 경로는 ~/workspace/mypresentaion/v4다.

# 실측 성능 비교 추가 — 2026.11.16

전체 index.html / presentation.pdf는 기존 4장과 성능 비교 P1~P4를 합친 8장이다. performance.html / performance.pdf는 새 성능 비교 4장만 제공한다. 발표 노트에는 추가 원고와 각 수치의 해석 범위를 포함했다. 원래 20분 발표에 전부 통합할 때에는 분량을 재조정한다.

WSL 작업 경로는 ~/workspace/mypresentaion/v4다. measurements/performance-report.md가 상세 보고서이고 measurements/orangepi-20261116에 30회 주 비교와 2회 추가 확인의 원본·집계·검증 결과가 있다. max는 3회 전체 관측 최댓값이다. 조건별 관측 시간은 45초다.

실제 카메라 입력은 약 16.87~20.80 FPS였고 검출 품질은 평가하지 않았다. 처리량 배수 향상이나 30Hz 유지·장시간 지연 상한을 입증했다고 표현하지 않는다. 선택 모델의 실제 NPU 추론·계측은 수행했으며 정확도·PC 표시의 종단 검증은 별도다.

시스템 SDK 파일은 변경하지 않았고 SHA256 일치를 확인했다. 사용자 요청에 따라 보드의 /home/orangepi/lwir_keepalive.pause를 유지해 기존 tracking server의 자동 재시작을 차단했다. 실험 복사본과 SDK 변형은 보드 /tmp/lwir-perf-20261116에 남아 있다.

# 제어 입력 부하 재시험

카메라 입력 부하가 부족했던 P1·P2를 실제 저장 프레임의 30·60·120fps 메모리 재생 36회 결과로 교체했다. 입력 경로만 실험용으로 바꾸고 NPU 추론·추적은 실제로 수행했다. P3·P4는 기존 실카메라 결과를 유지한다. 재시험 조건·누락률·p95·max와 한계는 measurements/orangepi-20261116-retry/report.md에 있다. 실카메라 수신 30fps 확보 문제는 미해결이며, 제어 입력 결과와 구분한다.
