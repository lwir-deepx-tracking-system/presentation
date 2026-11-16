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

## 논문·방법 참고

- Hu et al., *LoRA: Low-Rank Adaptation of Large Language Models* (2021), [arXiv:2106.09685](https://arxiv.org/abs/2106.09685). 저랭크 적응의 원리 참고. 이 프로젝트의 YOLO 적용 결과는 위 프로젝트 실험에서 따로 확인한다.
- Liao et al., *FastTrackTr: Towards Fast Multi-Object Tracking with Transformers*, [arXiv:2411.15811](https://arxiv.org/abs/2411.15811). 논문의 historical encoder/decoder 및 연결 구조 참고. 프로젝트의 DX-M1 구현은 연산 제약 때문에 다르다.
- Skogestad, *Simple analytic rules for model reduction and PID controller tuning*, Journal of Process Control 13 (2003), [저자 공개 원문](https://www.nt.ntnu.no/users/skoge/publications/2003/tuningPID/finalpaper.pdf). 제어기 튜닝의 일반 참고이며 이 논문이 프로젝트 설정의 성능을 입증한 것은 아니다.

## 아직 필요한 근거

- YOLO26m을 처음 선택할 때의 후보별 동일 조건 속도·정확도 비교 및 의사결정 기록, YOLO26m 자체의 epoch별 곡선과 최적 checkpoint 원자료.
- 자체 카메라 정제 전후의 공개 가능한 이미지, 학습·평가 분할과 시험별 사람·프레임 수.
- FP32 대 INT8의 동일 가중치·동일 입력 정확도 및 실제 화면까지의 종단 지연 반복 측정.
- 짐벌·카메라·보드 실물 사진, 동일 시각 영상·명령·오차 로그와 조건별 반복 측정.
