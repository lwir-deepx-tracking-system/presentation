# 30 epoch 설정과 실행 근거

발표 4·5쪽(열화상 전이학습, 학습 곡선)의 근거입니다. 공개하지 않는 파일은 `작성자 PC 기록(비공개)`와 파일 이름만 적었습니다.

## YOLO26m을 30 epoch로 정한 이유

YOLO26m FLIR 학습 스크립트 머리말에 설정과 이유가 적혀 있습니다(작성자 PC 기록(비공개): `train_full.py`, 2026-11-01).

- **레시피:** 앞서 FLIR 4,196장으로 학습한 m 교사의 설정을 그대로 씁니다. AdamW lr0 3e-4, 워밍업 3 epoch(warmup_bias_lr 0), nbs 64, BN 이동 통계 고정, seed 202입니다.
- **바꾼 것:** 학습 자료 4,196장 → 10,491장(FLIR 학습셋에서 쓸 수 있는 전체), 크기 증강 0.75(작은 사람을 더 많이 보이게), 모자이크 1.0을 쓰고 마지막 10 epoch에서 끔, 색상·채도 변화는 끔(흑백 열화상), 학습은 640 정사각 레터박스, 선택 기준은 장치와 같은 480×640 화면의 사람 AP입니다.
- **30 epoch:** cosine 학습률을 고정된 30 epoch에 맞췄습니다. 모자이크를 끄는 구간이 21~30 epoch에 오도록 정한 길이입니다.
- 이 실행의 `args.yaml`도 같은 값입니다: epochs 30, patience 0, batch 8, lr0 0.0003, lrf 0.01, cos_lr, warmup_epochs 3, nbs 64, close_mosaic 10, mosaic 1.0, scale 0.75, hsv_h·hsv_s 0, hsv_v 0.4, seed 202(작성자 PC 기록(비공개): `args.yaml`, 실행 이름 m_full_fast).
- 스크립트 머리말에는 FP32라고 적혀 있지만 이 실행은 AMP를 켰습니다(`fast_amp_tf32_noval: true`, `amp: true`). 스크립트에는 실행 뒤 비교용 선택 인자(aug, data)가 더해졌고, 이 실행의 시작 기록에는 그 항목이 없습니다.
- m 교사 레시피 자체를 처음 정한 이유와, 검출기 크기를 s에서 m으로 옮긴 이유를 따로 적은 문서는 찾지 못했습니다.

## 같은 예산으로 FT와 LoRA를 비교한 설계

2026-09-28 비교 설계 문서는 YOLO26s의 Full FT와 LoRA(r8 + 학습하는 검출 머리)를 같은 COCO 초기값, FLIR 자료, 입력 크기, 공통 설정에서 **30 epoch 고정 예산**으로 비교한다고 적습니다. 같은 epoch가 같은 연산량이나 시간을 뜻하지 않으므로 GPU 시간과 메모리를 따로 기록하게 했습니다. 이 문서는 YOLO26s 비교 설계이며, 위의 YOLO26m 실행과는 다른 실험입니다.

- 작성자 PC 기록(비공개): `FT_LORA_CONFIRMATORY_DESIGN_20260928.md`, SHA-256 `0c83ca68b51fb61c6706782d6a149e1a8914570f95920a0ddc5a03e37d60ee99`

## YOLO26m 30 epoch 실행 기록

- 시작 설정: [START.json](학습로그/YOLO26m_FullFT_run_start.json). COCO 가중치에서 시작, 학습 10,491장, 검증 1,144장, batch 8, 30 epoch.
- 완료·최고 epoch: [COMPLETED.json](학습로그/YOLO26m_FullFT_run_completed.json). best_epoch 27.
- epoch별 사람 AP50–95: [검증 CSV](학습로그/YOLO26m_FullFT_30epoch_validation.csv). 학습 중 **매 epoch 끝에 EMA 가중치**를 공통 채점기(480×640 화면)로 FLIR 검증 1,144장에서 잰 값입니다. 학습이 끝난 뒤 저장 체크포인트를 따로 채점한 것이 아닙니다. 저장된 체크포인트는 best와 last 두 개뿐입니다(`save_period -1`).
- epoch별 학습률과 학습 손실: [학습률·손실 CSV](학습로그/YOLO26m_FullFT_30epoch_lr_loss.csv). 이 실행의 `results.csv`에서 `lr/pg0`, `train/box_loss`, `train/cls_loss`를 옮겼습니다.
- 결과: 1 epoch 43.75%, 20 epoch 48.83%, 모자이크를 끈 21 epoch 49.75%, 27 epoch 최고 50.75%(50.7486), 30 epoch 50.62%(50.6209).
- 시작·완료 시각 차이는 7,341.8초(약 2시간 2분)입니다. 이때 RTX 4090을 YOLO26x 학습과 나눠 썼으므로 단독 실행 시간은 아닙니다.
- 같은 검증셋으로 최고 epoch를 골랐으므로 독립 시험 점수가 아닙니다. 30 epoch가 언제나 가장 좋은 길이라는 뜻도 아닙니다.
- 소형 사람 후보 비교의 기준값 50.72%는 배포한 YOLO26m을 같은 채점기로 다시 잰 값입니다(작성자 PC 기록(비공개): `start_score.json`). 학습 중 기록 50.75%와 0.03%p 차이입니다.
- 같은 모델의 학습 방법 정리: [11월 3일 학습 방법 정리](https://app.notion.com/p/40cb03d00660819bbd57f2072cf001b7)(팀 내부 Notion). 모델 목록의 설정: [model-bank 31ac21b models/README.md](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/README.md)(YOLO26m_(FLIR) 항목).
