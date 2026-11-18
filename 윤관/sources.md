# 발표 근거와 참고문헌

이 문서는 화면의 숫자가 어느 실험에서 왔는지 추적하기 위한 것이다. FLIR 6개 클래스 mAP와 사람 AP, PC float와 M1 INT8, 모델 호출과 실시간 종단 지연은 서로 다른 항목이다. 원래 시험의 영상·설정·날짜를 바꿔서 비교하지 않는다.

## 프로젝트 기록

1. [LWIR 연구 통합 — 학습·평가·발표 근거, 2026-11-12](https://app.notion.com/p/407b03d00660810d8f74c2223ce4d975): FLIR 학습 설정, 데이터 규모, FT·LoRA 비교와 실험별 제한. 10%·297 epoch·5,049 업데이트 수치는 이 통합 기록에 근거하며 원본 실행 파일은 이번 발표 준비 중 직접 재대조하지 못했다.
2. [연구 이야기 — 학습 곡선과 장치 측정 정리](https://app.notion.com/p/402b03d00660810980dafa5450638880): YOLO26s 에폭별 FT·LoRA 기록. 자동 정리된 과거 문서로 원자료 대조 대기라는 원문 표시를 유지한다. 발표 곡선은 프로젝트의 기존 `0930_evidence/01_learning_curves.png` 산출물이다.
3. [모델뱅크 모델 및 장치 평가, b0358a0](https://github.com/lwir-deepx-tracking-system/model-bank/blob/b0358a0a68b5f7b250cedecc9605684391f7cd4a/tracking_server/models/README.md): 자세 모델별 학습, RepVGG, 2026-11-06 FLIR 8편·3,749프레임 M1 INT8 비교, 11-04 임의 입력 호출 및 11-09 실카메라 측정. 대체로 각 1회이며 신뢰구간은 없다.
4. [자체 카메라 데이터·후보 결과, ccf1ea9](https://github.com/lwir-deepx-tracking-system/model-bank/blob/ccf1ea94b2e14152556cdeca0102ca1985b1338e/tracking_server/research/lwir_pose_plan/README.md#L254-L288): 데이터 정제·검수·혼합과 NF 후보의 시험 조건, 실패 기준 및 2차 후보의 분할 한계. 자체 촬영 원본과 라벨은 포함하지 않는다.
5. [FastTrackTr M1 변환 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/b0358a0a68b5f7b250cedecc9605684391f7cd4a/tracking_server/research/fasttracktr_npu/ftt_npu_variant.py) · [학습·장치 평가 INFO](https://github.com/lwir-deepx-tracking-system/model-bank/blob/b0358a0a68b5f7b250cedecc9605684391f7cd4a/tracking_server/models/e2e/fasttracktr/INFO.json): 논문 원형과 프로젝트 NPU 변형을 구분한다. 28 ms는 AE를 겹쳐 처리한 뒤의 장치 단계 시간이며 카메라→화면 지연이 아니다.
6. [짐벌 제어·시험 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/b0358a0a68b5f7b250cedecc9605684391f7cd4a/tracking_server/src/gimbal/PID_TUNING_RECORD_20261110.md): 실제 카메라와 짐벌, 가상 표적을 사용한 2026-11-10 시험. 등속 비교는 조건당 1회, 별도 가로 지표 악화도 함께 보고한다.
7. [FLIR 가림 사건 비교](https://app.notion.com/p/40db03d00660819c864dc9bf4d5650d1): 같은 M1 INT8 검출 결과를 사용한 개발 영상의 가림 전후 사례. 구성 선택에 사용된 자료이며 모든 가림 사건의 성능을 뜻하지 않는다.

8. [라벨링 서버 사용 기록, dfd2a9d](https://github.com/lwir-deepx-tracking-system/model-bank/blob/dfd2a9d878cf6ae93824ee1f7ad5ab21795b1c08/label_server/README.md): 사람 박스·ID 수정과 신체 부위 검수, 저장 방식. 발표의 실내·야외 화면은 사용자가 직접 제공한 실제 편집기 캡처다. 선택한 부위는 검수 필요로 표시되어 있으며 이 프레임의 완료·학습 사용 여부는 확인되지 않았다.

9. [11월 17일 최신 학습·추적 발표 인계, 6cf676d](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md): 라벨 10%의 FT·LoRA 두 예산, 60에폭 탐지 증류, 검수 264장 V7/V8, RepVGG 직접 적응 및 SOLIDER 증류의 조건·결과·미채택 사유. 시험 자료가 개발에 노출됐거나 학습과 겹친 항목은 독립 평가로 쓰지 않는다.
10. [11월 17일 인계: 위치 GRU와 서버 규칙](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/HANDOFF.md): GRU 단독 0.122와 같은 체크포인트에 Kalman 경로 규칙을 더한 0.118을 구분한다.

## 논문·방법 참고

- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021), [arXiv:2106.09685](https://arxiv.org/abs/2106.09685). 저랭크 적응의 원리 참고. 이 프로젝트의 YOLO 적용 결과는 위 프로젝트 실험에서 따로 확인한다.
- Liao et al., *FastTrackTr: Towards Fast Multi-Object Tracking with Transformers*, [arXiv:2411.15811](https://arxiv.org/abs/2411.15811). 논문의 historical encoder/decoder 및 연결 구조 참고. 프로젝트의 DX-M1 구현은 연산 제약 때문에 다르다.
- Skogestad, *Simple analytic rules for model reduction and PID controller tuning*, Journal of Process Control 13 (2003), [저자 공개 원문](https://www.nt.ntnu.no/users/skoge/publications/2003/tuningPID/finalpaper.pdf). 제어기 튜닝의 일반 참고이며 이 논문이 프로젝트 설정의 성능을 입증한 것은 아니다.

## 이번에 추가한 이론과 구현 근거

아래 논문은 각 방법의 **원리 설명용 참고자료**다. 프로젝트에서 선택 당시 실제로 읽었거나 논문 수치를 재현했다고 확인된 것은 아니다. 프로젝트의 성능과 설정은 위 실험 기록을 우선한다.

- 전이학습: [Yosinski et al., How transferable are features in deep neural networks?, 2014](https://arxiv.org/abs/1411.1792).
- 데이터 규모와 스케일링: [Hestness et al., Deep Learning Scaling is Predictable, Empirically, 2017](https://arxiv.org/abs/1712.00409). 발표의 네 점은 데이터 수와 업데이트가 함께 바뀌어 독립적인 법칙 검증은 아니다.
- 증류: [Hinton et al., Distilling the Knowledge in a Neural Network, 2015](https://arxiv.org/abs/1503.02531), [Wang et al., Distilling Object Detectors with Fine-grained Feature Imitation, 2019](https://arxiv.org/abs/1906.03609). 프로젝트의 특징 증류와 동일 구현이라는 뜻은 아니다.
- 작은 객체: [Wang et al., A Normalized Gaussian Wasserstein Distance for Tiny Object Detection, 2021](https://arxiv.org/abs/2110.13389).
- GRU: [Cho et al., RNN Encoder–Decoder, 2014](https://arxiv.org/abs/1406.1078). [프로젝트 위치 기억 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/src/track/position_memory.py)와 별도로 구분한다.
- 상자 크기 필터: [Casiez et al., 1€ Filter, 2012](https://gery.casiez.net/1euro/). 전체 좌표 필터와 크기만 필터는 다른 실험이다.
- ONNX 일반 개념: [ONNX 공식 문서](https://onnx.ai/onnx/intro/).
- 검출기: [YOLO26m DXNN 컴파일 메타데이터](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/detect/yolo26m/yolo26m_flir_nms_640x480_compile_metadata.json), [공개 640×480 ONNX 내보내기 예시](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/detect/build_scripts/yolo26_640x480_build/build480.py). 후자는 원래 YOLO26m 빌드와 동일한 실행 기록으로 확인되지 않았다.
- 외형 모델: [OTP2 RepVGG 공개 변환 예시](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/reid/build_scripts/repvgg_ft_otp2_build/build_reid.py). 최신 직접학습 가중치의 정확한 변환과 같다고 단정하지 않는다.
- FastTrackTr: [공개 export 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/e2e/fasttracktr/build_scripts/ftt_trained_export.py), [모델 INFO](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/e2e/fasttracktr/INFO.json). INFO는 보정용 17장, 공개 코드는 앞 16장을 사용해 차이를 확인해야 한다.

## SOLIDER와 외형 모델 증류를 선택한 배경

사람의 신원을 구별할 열화상 라벨은 수집과 검수에 비용이 들고, M1의 연산 자원도 제한돼 있다. 그래서 대규모 사람 이미지로 사전학습된 교사의 표현을 가벼운 학생 모델에 전달하면 현장 데이터를 활용하면서 장치에서 실행할 수 있을지 시험했다. **이 설명은 설계의 기술적 배경이며, 데이터 부족이 당시 결정적인 이유였다는 직접 기록은 찾지 못했다.** 최근 검수 264장은 후속 실험의 데이터로 전체 학습 데이터 규모가 아니다.

- [SOLIDER 논문](https://arxiv.org/abs/2303.17602)과 [원저자 저장소](https://github.com/tinyvision/SOLIDER): 무라벨 사람 이미지에서 의미·외형 표현을 사전학습한다. 공식 모델은 Swin Transformer 계열이며, 프로젝트 교사의 정확한 세부 체크포인트는 확인되지 않았다.
- [TransReID](https://arxiv.org/abs/2102.04378): Transformer를 이용한 사람 재식별 연구. 열화상 프로젝트에서 교사가 우월했다는 직접 증거는 아니다.
- [Efficient Training of Visual Transformers with Small Datasets](https://arxiv.org/abs/2106.03746): 일부 Transformer가 적은 데이터에서 학습에 어려움을 겪을 수 있음을 다룬다. 사전학습과 구조에 따라 달라지므로 모든 ViT에 일반화하지 않는다.
- [Cross-Architecture Knowledge Distillation](https://arxiv.org/abs/2207.05273): Transformer에서 CNN으로 특징을 전달할 때 구조 차이를 맞추는 문제를 다룬다. 프로젝트가 이 논문의 projector를 사용했다고 확인된 것은 아니다.
- [RepVGG](https://arxiv.org/abs/2101.03697): 학습 시 여러 갈래 구조를 추론 시 단순한 합성곱 구조로 합치는 모델. 프로젝트의 장치 적합성은 실제 DXNN 빌드와 실행 기록으로 따로 판단한다.
- [프로젝트 외형 모델 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/models/README.md#L312-L346): 이전 교사 종합 점수 0.738→0.773, 기존 학생 0.694 대비 새 증류 학생 0.660. 768→128차원 차이는 원인 가설이며 검증된 결론은 아니다. SOLIDER 교사의 같은 M1 조건 속도와 정확도 비교는 없다.

## 아직 필요한 근거

- YOLO26m을 처음 선택할 때의 후보별 동일 조건 속도·정확도 비교 및 의사결정 기록, YOLO26m 자체의 epoch별 곡선과 최적 checkpoint 원자료.
- 자체 카메라 정제 전후의 공개 가능한 이미지, 학습·평가 분할과 시험별 사람·프레임 수.
- FP32 대 INT8의 동일 가중치·동일 입력 정확도 및 실제 화면까지의 종단 지연 반복 측정.
- 짐벌·카메라·보드 실물 사진, 동일 시각 영상·명령·오차 로그와 조건별 반복 측정.

## 30에폭 FT·LoRA 실제 CSV

[FT](학습로그/YOLO26s_FT_seed101.csv) · [LoRA 기본](학습로그/YOLO26s_LoRA_seed101.csv) · [LoRA 학습률 조정](학습로그/YOLO26s_LoRA_lr1e-3_seed101.csv). 모두 YOLO26s, seed 101, batch 4의 30 epoch 기록이다. 9월 30일 생성된 학습 곡선의 원본 파일과 SHA-256을 대조했다. 실제 그래프는 Primary-6 검증 곡선이며 회색 COCO 기준은 반복 학습 곡선이 아니라 1회 평가 기준이다. 다른 YOLO26m·자세 모델의 원본 로그와 혼동하지 않는다.

- FT SHA-256: `846a2e5703e0cd7021eea28b574829cbf4c1c5458cd7f85ec2b5d744b0257b7b`
- LoRA 기본 SHA-256: `28e103eb5f8a98122d19336a2314e6c955b1ec1dc76de03dcbdbdc20fd977a27`
- LoRA 학습률 조정 SHA-256: `b91cf6c7870ea03e81d917fe7dafbf474e3731c129cb1e5a0326d7356b6d52b2`

## 60 epoch 검출기 증류 학습 로그 대조

[직접 FT CSV](학습로그/YOLO26s_FT_60epoch_seed202.csv) · [특징 증류 CSV](학습로그/YOLO26s_KD_60epoch_seed202.csv). 로컬 `local_execution_v12/runs`와 `retrieved_local_v12/runs` 사본의 SHA-256이 같고, 각각 60 epoch다. `local_evaluation_v2`의 `evaluation_complete.json` 및 `primary6.json`에서 평가된 최종 체크포인트와 사람 AP를 대조했다. FLIR 4,196장, seed 202, 검증 사람 AP FT 44.8575%, KD 44.2334%. 추적 DEV와 검증 AP는 별도 평가이며 개발 자료 노출 한계가 있다.

- 직접 FT CSV SHA-256: `86abce096a3b83e0a709eea277b88ee7933d13a178f0e678008010379bf05143`; 평가 체크포인트 SHA-256 `2f98faf042e2a14e69f2a0823e86494d74b0f856bf9ea1c0133bfc993e6c4196`.
- 증류 CSV SHA-256: `9c72401f7f62d100379f8fe8292cd0e062700edad109b12370cf7ed82f0d9702`; 평가 체크포인트 SHA-256 `32c5168629a7c281d16e8466959c8462a000d482dad4ceb6ac774616c6f6385c`.
- `train/dis_loss` 8.77978→1.45011은 증류 학습 중 손실이다. 전체 손실이나 검증 사람 AP가 아니며 손실 감소로 추적 개선을 단정하지 않는다.
- 11/17 외형 모델 비교의 CAMEL 218질의는 직접 A 200·200·200, 원교사 B 201·201·200, 적응교사 C 201·201·201개. TMOT 432질의는 세 조건·시드 모두 386개. 과거 개발에서 사용한 평가 자료이므로 새 카메라 독립 시험이 아니다. [실험 인계](https://github.com/lwir-deepx-tracking-system/model-bank/blob/835fae5259801784d41675948706151e64f5ba3a/tracking_server/research/LWIR_PRESENTATION_KO.md)

## 실제 짐벌 반응 그래프

[표시한 시계열 CSV](학습로그/짐벌_s7_수직응답.csv)는 [2026-11-10 장치 시험 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/835fae5259801784d41675948706151e64f5ba3a/tracking_server/src/gimbal/PID_TUNING_RECORD_20261110.md)의 stage7 `s7/frames.csv`에서 실제 카메라·짐벌을 사용한 `ramp_y30_PD30_6_db04`와 `ramp_y30_PD30_6_db06`의 `phase=run` 행을 추린 값이다. 원본 SHA-256 `4a0f2a6477c0ff0a19f104c8a1d240a683ec733417de25f070f4a19f8d23cd98`. 정규화 수직 오차 `ey`에 240을 곱해 px로 나타냈으며, 가상 표적 정지는 2.5초다. 각 조건 1회, 각각 99·100프레임이다. 정지 후 방향 반전 4→1회는 원문 summary 값이다. 가로 뒤처짐 14.3→18.6px는 같은 stage의 별도 가로 시험이다. 실제 사람의 종단 추종이나 짐벌 실물 사진을 보여주는 증거는 아니다.

## 학습 에폭 예시 정정

[YOLO26s FT seed 101 원본 CSV](학습로그/YOLO26s_FT_seed101.csv)의 `monitor_primary6/mAP50_95`는 15 epoch 0.404133, 30 epoch 0.413342다. 차이는 **+0.9209%p**이며 단일 s급 실행에서의 검증 추이다. 30 epoch를 m급 최적 종료점으로 입증하지 않는다.

발표 근거로 확인한 model-bank `835fae5`는 발표 근거의 `6cf676d` 이후 웹 H.264 미리보기 변경만 추가했으며, 학습·평가 자료는 같은 내용이다.

## 사람 박스 생성과 안정화 구현

- [라벨 편집기](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/label_server/README.md): 한 사람에 박스·ID 하나, 관절과 부위는 그 ID에 연결한다. 가림 부위 위치를 모르면 임의로 찍지 않는다. 발표에 쓰인 실제 작업 화면의 선택 부위는 검수 필요 상태다.
- [비율 측정 원자료](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/research/lwir_pose_plan/results/bodybox_ratio_20261115.json) · [학습용 몸 상자 변환](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/research/lwir_pose_plan/scripts/pose_partial.py) · [템플릿 맞춤](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/models/detect/build_scripts/yolo26m_pose_otp2_bodybox_build/skeleton_box.py): 2개 이상의 라벨된 관절로 템플릿을 맞추고 머리 위~골반 목표 상자를 만든다. 관절 부족·맞춤 실패 시 11월 15일 보완된 전처리는 COCO 전신 GT의 높이 0.531배, 폭 0.681배(충분한 관절이 있는 32,951명 중앙값)를 사용한다. 이 보완은 기존 F/O 체크포인트에 소급 적용된 것이 아니다.
- [박스 후처리 코드](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/src/track/box_refine.py): `size`는 추적 상자의 log 너비·높이에만 1€ 필터(5Hz, β3)를 적용하고 가로 중심과 필터 전 조준점을 유지한다. `body` 후보는 별도의 변환표와 1.5Hz·β0.3을 사용한다. [11/16 인계](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/HANDOFF.md)에 따르면 body 2판은 공개 기준 13/14, 장치 속도 녹화 기준 4/4였지만 누락한 조준 떨림 기준 때문에 그날 장치에 켜지 않았다. 이후 실시간 설정은 이 기록으로 확정할 수 없다.
- model-bank `d5b6446`은 직전 발표 기준 `835fae5` 이후 영상 스트리밍과 짐벌 홈 제어가 갱신된 버전이다. 박스 생성·안정화 코드는 변경 목록에 없다.

## 자세 모델 분기와 학습 순서 재대조

[모델뱅크 학습 이력](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/models/README.md)은 E의 COCO 초기값 → OTP2 30epoch → 가림·열화상 증강 17epoch → 흑백 COCO 추가 14epoch → MOT17 추가 12epoch 중 선택 순서를 기록한다. [R1v2 실행 스크립트](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/research/lwir_pose_plan/scripts/vast_chains/chain_R1v2.sh)는 조기 종료를 끄고 R1을 10epoch 학습한 설정이다. R1 마지막 가중치에서 O·C를 각각 6epoch 진행했으며, F는 대조 C의 `epoch2.pt`, 즉 세 번째 epoch 체크포인트다. O 6epoch와 C 3epoch 비교는 학습량이 달라 가림 조각의 단독 효과를 증명하지 않는다. [O·C 평가와 F 선정 기록](https://github.com/lwir-deepx-tracking-system/model-bank/blob/d5b6446613db5a10aec094d74fd6934e42f47ce9/tracking_server/research/lwir_pose_plan/README.md)


## 30 epoch 설정과 실행 기록

[비교 설계·실제 m 학습 시간·30개 체크포인트 검증 근거](근거_30epoch.md). 공통 예산 설계는 별도 YOLO26s FT·LoRA 비교이며 m의 최초 설정 이유와 구분한다. m 30 epoch는 X 모델과 RTX 4090을 공유한 1회 기록으로 약 2시간 2분이며, 사후 검증에서 27 epoch가 최고였다.


## 공개 데이터와 학습 설정의 선택 근거

[데이터별 장면·라벨 차이, 공개 데이터 파인튜닝 순서, 모델별 설정 이유와 미확인 항목](학습_설정_데이터_근거.md). OTP2 공식 예시와 프로젝트 라벨 편집 화면은 출처와 학습 포함 미확인을 구분한다. NF 야외 학습 기록과 11/15 야외 학습 제외 원칙의 관계 및 학습·평가 분리 근거는 확인이 필요하다.
