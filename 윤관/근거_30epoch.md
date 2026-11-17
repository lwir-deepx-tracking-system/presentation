# 30 epoch 설정과 실행 근거

## 같은 예산으로 비교한 이유

2026-09-28 작성된 `FT_LORA_CONFIRMATORY_DESIGN_20260928.md` 9–11행은 Full FT와 LoRA를 같은 COCO 초기화, FLIR 데이터, 입력 크기와 공통 설정에서 **30 epoch 고정 예산**으로 비교한다고 명시한다. 같은 epoch가 같은 연산량이나 소요 시간을 의미하지 않으므로 GPU 시간과 메모리는 별도로 기록하도록 했다. 이 문서는 YOLO26s 계열의 별도 비교 설계이며, YOLO26m의 최초 30 epoch 결정 이유를 직접 기록한 자료는 아니다.

- 원문 위치: `2026-09-21/training-yunkwan-push/training/flir_yolo26/FT_LORA_CONFIRMATORY_DESIGN_20260928.md` (원 작성 PC)
- 원문 SHA-256: `0c83ca68b51fb61c6706782d6a149e1a8914570f95920a0ddc5a03e37d60ee99`

## YOLO26m의 실제 30 epoch 기록

- 학습 설정·시작 시각: [START.json](학습로그/YOLO26m_FullFT_run_start.json)
- 완료 시각·최고 체크포인트: [COMPLETED.json](학습로그/YOLO26m_FullFT_run_completed.json)
- 저장 체크포인트 30개의 검증 결과: [사람 AP CSV](학습로그/YOLO26m_FullFT_30epoch_validation.csv). 원본 각 `epoch_001_score.json`부터 `epoch_030_score.json`에서 값을 옮겼다.
- 원본 위치: `D:/LIG-Runs/flir_yolo26/claude_tracking_reacq_20261031/vast_ft/results/`, `m_full_fast/` 및 `meta/m_full_fast/`.
- 10,491장·batch 8·30 epoch, 검증 1,144장. 시작·완료 시각의 차이는 7,341.8초(약 2시간 2분 22초)이며 당시 RTX 4090을 X 모델과 공유했다. 단독 실행 속도나 보장 시간은 아니다.
- 학습 후 저장 체크포인트를 검증한 결과 27 epoch 사람 AP50–95 50.7486%, 30 epoch 50.6209%다. 최고점을 고른 동일 검증셋이므로 독립 시험 결과가 아니며, 30 epoch의 보편적 최적성을 뜻하지 않는다.
- [11월 3일 학습 방법 정리](https://app.notion.com/p/40cb03d00660819bbd57f2072cf001b7): 같은 모델의 Vast 4090 약 2시간 기록. [모델뱅크 설정](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/models/README.md): FLIR 10,491장, 30 epoch 기록.

30을 최초에 정한 직접 의사결정 기록은 찾지 못했다. 비교 예산이라는 설계 목적, 실제 실행 비용, 학습 후 관측된 결과는 구분해 설명한다.
