# 발표 근거와 참고문헌

화면의 숫자가 어느 실험에서 왔는지 찾기 위한 문서입니다. 장마다 숫자와 출처는 [슬라이드별 근거](근거_슬라이드별.md)에 있고, 11월 19일 이후 더한 내용은 [11월 20일 추가 근거](근거_최신_20261120.md)에 모았습니다.

- FLIR 6개 클래스 mAP와 사람 AP, PC FP32와 M1 INT8, 모델 호출 시간과 실시간 종단 지연은 서로 다른 값입니다. 서로 다른 시험의 영상·설정·날짜를 섞어 비교하지 않습니다.
- model-bank 링크는 [31ac21b](https://github.com/lwir-deepx-tracking-system/model-bank/tree/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab)(2026-11-20) 기준입니다. 11월 19일 기록 문서만 그때 커밋을 그대로 씁니다.
- 공개하지 않는 파일은 `작성자 PC 기록(비공개)`와 파일 이름만 적었습니다. Notion 문서는 팀 내부 기록입니다.

## 프로젝트 기록

1. [LWIR 연구 통합 — 학습·평가·발표 근거, 2026-11-12](https://app.notion.com/p/407b03d00660810d8f74c2223ce4d975)(팀 내부 Notion): FLIR 학습 설정, 데이터 규모, FT·LoRA 비교와 실험별 한계. 라벨 10%·297 epoch·5,049 업데이트 수치는 원본 결과와 같음을 확인했습니다(작성자 PC 기록(비공개): `FINAL_COMPARISON.json`, `REPORT.md`). 297 epoch 값은 1,074장 묶음 A·B·C 세 개의 평균이고, 개발 중 이미 본 검증셋이라 독립 시험이 아닙니다.
2. [연구 이야기 — 학습 곡선과 장치 측정 정리](https://app.notion.com/p/402b03d00660810980dafa5450638880)(팀 내부 Notion): YOLO26s epoch별 FT·LoRA 기록. 발표 6쪽 곡선은 아래 학습로그 CSV 세 개로 다시 그렸습니다.
3. [model-bank 모델 목록과 장치 평가](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/README.md): 검출·자세 모델별 학습, RepVGG, 2026-11-06 FLIR 8편 3,749프레임 M1 INT8 비교, 11-04 임의 입력 호출, 11-09 실카메라 측정. 대부분 1회이고 신뢰구간은 없습니다.
4. [자체 카메라 데이터·후보 결과](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/lwir_pose_plan/README.md#L254-L288): 정리·검수·혼합 학습과 NF 후보의 시험 조건, 통과 기준. 자체 촬영 원본과 라벨은 올리지 않았습니다.
5. [FastTrackTr M1 변환 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/fasttracktr_npu/ftt_npu_variant.py) · [학습·장치 평가 INFO](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/e2e/fasttracktr/INFO.json): 논문 원형과 장치용 변형을 나눠 적습니다. INFO의 학습 설정(학습률 5e-5, 백본 0.1배, 1 epoch 워밍업, 2 epoch 뒤 0.1배)은 실제 실행 기록입니다. 28 ms는 프레임을 겹쳐 처리한 뒤의 장치 단계 시간이며 카메라 → 화면 지연이 아닙니다.
6. [짐벌 PD·불감대 시험 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/src/gimbal/PID_TUNING_RECORD_20261110.md): 실제 카메라·짐벌에 가상 표적을 쓴 2026-11-10 시험입니다. 자동 추종 최고 속도 10에서 했고(운영은 100), 등속 비교는 조건당 1회입니다. 나빠진 가로 지표도 함께 적었습니다.
7. [FLIR 가림 사건 비교](https://app.notion.com/p/40db03d00660819c864dc9bf4d5650d1)(팀 내부 Notion): 같은 M1 INT8 검출 결과를 쓴 개발 영상의 가림 전후 사례입니다. 구성 선택에 쓴 자료이며 모든 가림 상황의 성능을 뜻하지 않습니다.
8. [라벨링 서버 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/label_server/README.md): 사람 박스·ID 수정, 17관절 편집, 구간 나눠 함께 라벨링, 저장 방식. 발표의 실내·야외 화면은 작성자의 실제 편집 화면입니다. 화면에서 고른 부위는 검수 필요 상태입니다.
9. [학습·추적 실험 정리](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/LWIR_PRESENTATION_KO.md): 라벨 10%의 FT·LoRA 두 예산, 60 epoch 검출기 증류, 검수 264장 V7/V8, RepVGG 직접 적응과 SOLIDER 증류의 조건·결과·미채택 이유. 시험 자료가 개발에 쓰였거나 학습과 겹친 항목은 독립 평가로 쓰지 않습니다.
10. [인계 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/HANDOFF.md): 위치 GRU 단독 0.122와, 같은 체크포인트에 Kalman 경로 규칙을 더한 0.118을 구분합니다. 11월 19~20일 재학습·분할 C++·짐벌 변경 기록도 이 파일에 있습니다.
11. **짐벌 실측과 가상 카메라 시험, 지연 점검**(작성자 PC 기록(비공개)): `gimbal_speed/RESULT.md`(11-15 실측), `virtual_gimbal_tmot/SPEC.md`(가상 카메라 방법), `tuning_sweep/RESULT.md`, `lead_tuning/RESULT.md`, `recatch/RESULT.md`, `live_coast/RESULT.md`, `search2/RESULT.md`, `search2/long_exit/RESULT.md`, `AUDIT_20261115.md`(장면 → 짐벌 지연). 요약과 상태는 [11월 20일 추가 근거](근거_최신_20261120.md) 3절에 있습니다.

## 논문·방법 참고

- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021), [arXiv:2106.09685](https://arxiv.org/abs/2106.09685). 저랭크 적응의 원리 참고입니다. 이 프로젝트의 LoRA는 r8에 검출 머리를 함께 학습한 형태이며, 결과는 위 프로젝트 실험입니다.
- Liao et al., *FastTrackTr: Towards Fast Multi-Object Tracking with Transformers*, [arXiv:2411.15811](https://arxiv.org/abs/2411.15811). 과거 정보를 쓰는 인코더·디코더 구조 참고입니다. 장치용 구현은 M1 연산 제약 때문에 다릅니다.
- Skogestad, *Simple analytic rules for model reduction and PID controller tuning*, Journal of Process Control 13 (2003), [저자 공개 원문](https://www.nt.ntnu.no/users/skoge/publications/2003/tuningPID/finalpaper.pdf). 제어기 튜닝의 일반 참고이며, 이 논문이 프로젝트 설정의 성능을 입증하지는 않습니다.

## 이론과 구현 참고

아래 논문은 각 방법의 **원리 설명용 참고자료**입니다. 프로젝트 성능과 설정은 위 실험 기록을 따릅니다.

- 전이학습: [Yosinski et al., How transferable are features in deep neural networks?, 2014](https://arxiv.org/abs/1411.1792).
- 데이터 규모: [Hestness et al., Deep Learning Scaling is Predictable, Empirically, 2017](https://arxiv.org/abs/1712.00409). 발표의 네 점은 자료 수와 갱신 수가 함께 바뀌어 스케일 법칙 검증이 아닙니다.
- 증류: [Hinton et al., Distilling the Knowledge in a Neural Network, 2015](https://arxiv.org/abs/1503.02531), [Wang et al., Distilling Object Detectors with Fine-grained Feature Imitation, 2019](https://arxiv.org/abs/1906.03609). 프로젝트의 특징 증류와 같은 구현이라는 뜻은 아닙니다.
- 작은 객체: [Wang et al., A Normalized Gaussian Wasserstein Distance for Tiny Object Detection, 2021](https://arxiv.org/abs/2110.13389).
- GRU: [Cho et al., RNN Encoder–Decoder, 2014](https://arxiv.org/abs/1406.1078). 프로젝트 구현은 [위치 기억 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/src/track/position_memory.py)입니다.
- 박스 크기 필터: [Casiez et al., 1€ Filter, 2012](https://gery.casiez.net/1euro/). 좌표 전체 필터와 크기만 필터는 다른 실험입니다.
- ONNX: [ONNX 공식 문서](https://onnx.ai/onnx/intro/).
- 검출기 변환: [YOLO26m DXNN 컴파일 메타데이터](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/detect/yolo26m/yolo26m_flir_nms_640x480_compile_metadata.json), [공개 640×480 ONNX 내보내기 예시](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/detect/build_scripts/yolo26_640x480_build/build480.py). 내보내기 예시가 원래 YOLO26m 빌드와 같은 실행이었는지는 확인하지 못했습니다.
- 외형 모델 변환: [OTP2 RepVGG 변환 예시](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/reid/build_scripts/repvgg_ft_otp2_build/build_reid.py).
- FastTrackTr 변환: [export 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/e2e/fasttracktr/build_scripts/ftt_trained_export.py), [모델 INFO](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/e2e/fasttracktr/INFO.json). INT8 보정은 **16장**을 썼습니다. 코드는 17장을 읽고 앞 16장으로 보정 파일을 만들며, INFO의 "17장"은 읽은 장 수입니다. 보정 파일은 16장이고, 그 DXNN 해시가 INFO의 장치 파일 해시와 같습니다(작성자 PC 기록(비공개): `calib_ae.npz`, `calib_b0.npz`, `calib_b1.npz`, `EXPORT.json`).

## SOLIDER와 외형 모델 증류를 시험한 배경

사람을 구별하는 열화상 신원 라벨은 모으고 검수하는 데 비용이 들고, M1의 연산 자원도 제한돼 있습니다. 그래서 대규모 사람 이미지로 사전학습한 교사의 표현을 가벼운 학생에게 옮기면 장치에서 돌릴 수 있는지 시험했습니다. 이것은 설계의 기술적 배경이며, 그때 이 이유로 결정했다는 문서는 따로 없습니다.

- [SOLIDER 논문](https://arxiv.org/abs/2303.17602)과 [원저자 저장소](https://github.com/tinyvision/SOLIDER): 라벨 없는 사람 이미지에서 의미·외형 표현을 사전학습합니다. 프로젝트 교사는 LUPerson으로 사전학습한 SOLIDER Swin-Tiny(768차원)이고, 증류에 쓴 교사와 SHA-256이 같습니다(작성자 PC 기록(비공개): `RESULT_KO.md`, 11-20 SOLIDER 추적기 교체 비교).
- [TransReID](https://arxiv.org/abs/2102.04378): Transformer를 쓴 사람 재식별 연구입니다. 열화상에서 교사가 더 낫다는 직접 증거는 아닙니다.
- [Efficient Training of Visual Transformers with Small Datasets](https://arxiv.org/abs/2106.03746): 일부 Transformer가 적은 데이터에서 학습이 어렵다는 연구입니다. 모든 ViT에 일반화하지 않습니다.
- [Cross-Architecture Knowledge Distillation](https://arxiv.org/abs/2207.05273): Transformer에서 CNN으로 특징을 옮길 때 구조 차이를 맞추는 문제입니다. 프로젝트가 이 논문의 방법을 썼다는 뜻은 아닙니다.
- [RepVGG](https://arxiv.org/abs/2101.03697): 학습 때 여러 갈래 구조를 추론 때 단순한 합성곱으로 합치는 모델입니다. 장치 적합성은 실제 DXNN 빌드와 실행 기록으로 판단했습니다.
- [model-bank 외형 모델 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/README.md#L306-L350): 11-15에 교사를 더 학습해 PC 종합 점수 0.738 → 0.773이 됐지만, 그 교사로 증류한 학생은 0.660으로 기존 학생 0.694보다 낮았습니다. 768 → 128차원 차이는 원인 가설이며 검증된 결론이 아닙니다.
- 11-20에 교사 SOLIDER를 추적기에 직접 넣어 비교했습니다. FLIR 녹화 3,749프레임, PC FP32에서 IDF1 66.74 → 66.57%, ID 전환 99 → 100회로 나아지지 않았습니다(같은 `RESULT_KO.md`). 교사의 M1 속도는 재지 않았습니다.
- 장치가 쓰는 외형 모델은 검수 264장으로 직접 미세조정한 RepVGG입니다([인계 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/HANDOFF.md) '실시간 카메라의 녹화 버튼과 SOLIDER 증류 모델 표시'). 검수 264장은 후속 실험 자료이며 전체 학습 자료 규모가 아닙니다.

## 아직 필요한 근거

- YOLO26m을 고를 때의 같은 조건 후보 비교. 지금은 s급 세 계열 비교뿐이고, 크기를 m으로 옮긴 이유와 m 교사 레시피를 처음 정한 이유를 적은 문서는 없습니다.
- 자세 모델, 외형 증류, 위치 GRU·Mamba, FastTrackTr의 epoch별 학습 로그(이 폴더에 없음).
- 같은 가중치·입력의 FP32와 M1 INT8의 정답 기준 정확도. 지금은 YOLO26s FLIR 시험 375장에서 ONNX 검출의 99.2%를 M1이 찾았다는 일치 비교뿐입니다(작성자 PC 기록(비공개): `onnx_vs_m1_test.txt`).
- 사람이 있는 실카메라에서 모든 장 33 ms 이내인지, 여러 명 자동 추종 때 지연.
- 실제 사람·실제 짐벌로 잰 재포착률, SPD 30 초과와 세로(틸트) 응답, 장면 → 짐벌 종단 지연 실측.
- OTP2 별도 시험 2,151장으로 E10 평가, CLAHE 대조 학습, 우리 카메라의 독립 ID 시험.
- 짐벌·카메라·보드 실물 사진과, 같은 시각의 영상·제어 명령·각도 기록.

## 학습 로그 CSV

### 30 epoch FT·LoRA (발표 6쪽)

[FT](학습로그/YOLO26s_FT_seed101.csv) · [LoRA 기본](학습로그/YOLO26s_LoRA_seed101.csv) · [LoRA 학습률 10배](학습로그/YOLO26s_LoRA_lr1e-3_seed101.csv). 모두 YOLO26s, seed 101, batch 4, 30 epoch이고, 9월 30일 학습 곡선에 쓴 원본 파일과 SHA-256이 같습니다. 그래프는 6개 클래스 검증 mAP50–95입니다. YOLO26m·자세 모델 로그와 다른 실행입니다.

- FT SHA-256: `846a2e5703e0cd7021eea28b574829cbf4c1c5458cd7f85ec2b5d744b0257b7b`
- LoRA 기본 SHA-256: `28e103eb5f8a98122d19336a2314e6c955b1ec1dc76de03dcbdbdc20fd977a27`
- LoRA 학습률 10배 SHA-256: `b91cf6c7870ea03e81d917fe7dafbf474e3731c129cb1e5a0326d7356b6d52b2`
- FT CSV의 `monitor_primary6/mAP50_95`는 15 epoch 40.41%, 18 epoch 최고 41.80%, 30 epoch 41.33%입니다. 15 → 30 epoch 변화는 +0.92%p이고, 30 epoch는 최고점보다 0.47%p 낮습니다. 단일 s급 실행의 검증 추이이며 m급의 최적 길이를 보여 주지 않습니다.
- 11월 19일 판 근거 자료 장의 "15 → 30 epoch 약 4.0%p"는 그 장에 그린 곡선과는 맞지만, 위 세 CSV와 다른 실행이고 어느 학습로그 CSV와도 맞지 않습니다. 그래서 그 값에는 이 폴더의 원본을 붙이지 못했습니다. 이전 판에서 이 값을 "정정"이라고 적은 것은 틀린 표현이었습니다.

### 60 epoch 검출기 증류 (발표 8쪽)

[직접 FT CSV](학습로그/YOLO26s_FT_60epoch_seed202.csv) · [특징 증류 CSV](학습로그/YOLO26s_KD_60epoch_seed202.csv). FLIR 4,196장, seed 202, 각 60 epoch입니다. 작성자 PC의 두 실행 사본에서 SHA-256이 같고, 평가 기록의 최종 체크포인트와 사람 AP를 대조했습니다(작성자 PC 기록(비공개): `evaluation_complete.json`, `primary6.json`). 검증 사람 AP는 FT 44.8575%, 증류 44.2334%입니다. 추적 DEV 점수는 별도 평가이고 개발에 노출된 자료입니다.

- 직접 FT CSV SHA-256: `86abce096a3b83e0a709eea277b88ee7933d13a178f0e678008010379bf05143`, 평가 체크포인트 SHA-256 `2f98faf042e2a14e69f2a0823e86494d74b0f856bf9ea1c0133bfc993e6c4196`
- 증류 CSV SHA-256: `9c72401f7f62d100379f8fe8292cd0e062700edad109b12370cf7ed82f0d9702`, 평가 체크포인트 SHA-256 `32c5168629a7c281d16e8466959c8462a000d482dad4ceb6ac774616c6f6385c`
- `train/dis_loss` 8.77978 → 1.45011은 증류 학습 중 손실입니다. 전체 손실이나 검증 사람 AP가 아니며, 손실이 줄었다고 추적이 좋아졌다고 보지 않습니다.

### YOLO26m 30 epoch (발표 4·5쪽)

[epoch별 사람 AP](학습로그/YOLO26m_FullFT_30epoch_validation.csv) · [epoch별 학습률·손실](학습로그/YOLO26m_FullFT_30epoch_lr_loss.csv) · [시작 기록](학습로그/YOLO26m_FullFT_run_start.json) · [완료 기록](학습로그/YOLO26m_FullFT_run_completed.json). 사람 AP는 학습 중 매 epoch 끝 EMA 가중치를 잰 값입니다. 설정 이유와 자세한 내용은 [30 epoch 근거](근거_30epoch.md)에 있습니다.

### 상체 E10 OTP2 검증 (발표 18쪽)

[검증 CSV](학습로그/20261119_E10_OTP2_validation.csv): 이전 1,056장 E10, 현장 650장 E10, 추가 3 epoch 두 조건의 OTP2 934장 박스·관절 AP와 박스 재현율. 근거는 [11월 19일 기록](근거_최신_20261119.md)입니다.

### 외형 모델 CAMEL·TMOT 질의 수 (부록)

검수 264장 비교에서 CAMEL 218질의 Rank-1 맞힌 수는 직접 학습 A 200·200·200, 고정 교사 증류 B 201·201·200, 적응 교사 증류 C 201·201·201개입니다. TMOT 432질의는 세 조건·세 시드 모두 386개입니다. B의 고정 교사는 11-10 자체 실내 자료로 먼저 튜닝한 SOLIDER ep3입니다(model-bank `24663e4`). 다른 장의 CAMEL 90.30·91.68%는 간격별 Rank-1 평균이라 이 맞힌 수와 다른 값입니다. 과거 개발에 쓴 평가 자료이므로 새 카메라의 독립 시험이 아닙니다.

### 짐벌 세로 응답 (발표 32쪽)

[시계열 CSV](학습로그/짐벌_s7_수직응답.csv)는 [2026-11-10 시험 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/src/gimbal/PID_TUNING_RECORD_20261110.md)의 stage7 `frames.csv`에서 실제 카메라·짐벌로 한 `ramp_y30_PD30_6_db04`와 `ramp_y30_PD30_6_db06`의 `phase=run` 행을 뽑은 값입니다. 원본 SHA-256 `4a0f2a6477c0ff0a19f104c8a1d240a683ec733417de25f070f4a19f8d23cd98`.

- 정규화 세로 오차 `ey`에 240을 곱해 px로 바꿨습니다. 가상 표적은 2.5초에 멈춥니다. 조건마다 1회, 각 99·100프레임입니다.
- 멈춘 뒤 방향 반전 4 → 1회는 원문 요약 값이고, PD Kp 30·Ki 0·Kd 6에서 불감대만 바꾼 결과입니다(적분을 뺀 효과가 아님).
- 가로 뒤처짐 14.3 → 18.6 px는 같은 단계의 별도 가로 시험입니다.
- 자동 추종 최고 속도 10에서 한 시험이며, 실제 사람을 따라간 결과가 아닙니다.

## 사람 박스 생성과 안정화 구현

- [라벨 편집기](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/label_server/README.md): 한 사람에 박스·ID 하나이고, 관절과 부위는 그 ID에 연결합니다. 가려진 부위 위치를 모르면 임의로 찍지 않습니다.
- [비율 측정 원자료](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/lwir_pose_plan/results/bodybox_ratio_20261115.json) · [학습용 몸 박스 변환](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/lwir_pose_plan/scripts/pose_partial.py) · [골격 틀 맞춤](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/detect/build_scripts/yolo26m_pose_otp2_bodybox_build/skeleton_box.py): 보이는 관절이 2개 이상이면 골격 틀을 맞춰 머리 위 ~ 골반 박스를 만듭니다. 관절이 모자라면 11-15에 더한 규칙이 COCO 전신 박스의 높이 0.531배, 폭 0.681배를 씁니다. 이 규칙은 이전 F·O 체크포인트에 소급되지 않았고, 이후 NF·V7·E10 학습에서는 꺼져 있었습니다(작성자 PC 기록(비공개): `RUN_MANIFEST.json`, `TRAIN_PROTOCOL.json`).
- [박스 후처리 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/src/track/box_refine.py): `size`는 추적 박스의 log 폭·높이에만 1€ 필터(5 Hz, β 3)를 쓰고 가로 중심과 조준점은 그대로 둡니다. `body`는 별도 변환표와 1.5 Hz·β 0.3을 씁니다. 11-16 인계에 따르면 body 2판은 공개 기준 14개 중 13개를 맞췄지만 조준 떨림 기준 하나를 못 맞춰 그날 장치에 켜지 않았습니다. 11-20 장치 읽기 기록에는 `box_refine body`로 적혀 있어, 그 뒤 누가 언제 바꿨는지는 확인이 필요합니다(작성자 PC 기록(비공개): `DEVICE_SNAPSHOT_1139.md`).

## 자세 모델 분기와 학습 순서

[model-bank 모델 학습 이력](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/README.md#L69-L95)은 COCO 시작 → OTP2 30 epoch → 가림·열화상 증강 17 epoch → 흑백 COCO 추가 14 epoch → 흑백 MOT17 추가 순서를 적습니다. E는 MOT17 단계의 4 epoch 판입니다. 최대 12 epoch였지만 조기 멈춤으로 10 epoch에서 끝났고, 박스 점수가 섞인 기준으로 4 epoch 판이 골라졌습니다([계획·평가 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/lwir_pose_plan/README.md) 2·3절).

- E에서 10 epoch씩 이어 학습한 R0(기존 자료, 대조)와 R1(LLVIP-Pose 추가)을 비교했습니다([R1v2 실행 스크립트](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/research/lwir_pose_plan/scripts/vast_chains/chain_R1v2.sh)).
- R1 마지막 가중치에서 사무실 가림 조각을 넣은 O와 넣지 않은 C를 각각 6 epoch 학습했습니다. F는 C의 `epoch2.pt`, 즉 3 epoch 판입니다.
- O의 3 epoch 판도 겹친 박스 수가 F와 같아서, O 마지막 판과의 차이는 학습 길이 영향입니다. 가림 조각만의 효과는 보여 주지 못했습니다.
- 현장 상체 E10의 시작 가중치 `C_control_v1_epoch2.pt`가 F입니다([LWIR650_E10_CLAHE_REPRO_20261120.md](https://github.com/lwir-deepx-tracking-system/model-bank/blob/31ac21bfa4ff4f40896677d0bb9501f9e2f6ebab/tracking_server/models/detect/yolo26m/LWIR650_E10_CLAHE_REPRO_20261120.md)).

## 다른 근거 문서

- [30 epoch 설정과 실행 근거](근거_30epoch.md): YOLO26m 레시피와 30 epoch를 정한 이유(실행 스크립트 기록), epoch별 검증·손실, 학습 시간.
- [공개 데이터와 학습 설정의 근거](학습_설정_데이터_근거.md): 데이터별 장면·라벨 차이, 공개 데이터 학습 순서, 설정별 이유.
- [모델별 학습 입력·출력과 기록](학습_입출력_로그.md).
- [11월 19일 기록](근거_최신_20261119.md): 현장 650장 상체 E10, 추가 3 epoch과 시간 손실, 전신 표시, 분할 첫 측정.
- [11월 20일 추가 근거](근거_최신_20261120.md): 상체 검출기 후속 재학습, 분할 C++ 이식과 꼬리 지연, 짐벌 실측·가상 시험·지연·놓침 대응, 외형 모델 상태, 11-20 장치 재설치 뒤 상태.
- [평가자 검토 메모](평가자_검토.md).
