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
