# 윤관 | 열화상 모델 학습과 짐벌 제어

제가 맡은 부분을 그림 순서대로 정리했습니다. 각 장의 선택 이유, 방법과 결과를 이어서 볼 수 있습니다.

[발표 흐름 PDF · 71장](발표_전체흐름.pdf) · [전체 근거 PDF · 97장](발표_전체근거.pdf) · [발표 대본](notes.md) · [논문·실험 출처](sources.md) · [HTML](index.html)

**흐름:** 탐지 학습 → 자체 데이터·라벨 → 자세·외형 모델 → GRU·박스 안정화 → FastTrackTr → ONNX·양자화·M1 → 짐벌

*논문은 원리 설명을 위해 추가한 참고자료입니다. 실제 라벨링 화면의 선택 부위는 검수 필요 상태입니다.*


## 담당한 일과 전체 흐름

### 01. 제가 맡은 일

![제가 맡은 일](assets/readme-slides/slide-01.jpg)

열화상 모델 학습·평가와 짐벌 제어를 맡았습니다.

### 02. 프로젝트는 이렇게 진행했습니다

![프로젝트는 이렇게 진행했습니다](assets/readme-slides/slide-02.jpg)

데이터 준비부터 학습, 평가, 장치 시험까지 이어집니다.


## 1. 탐지 모델 선택과 학습

### 03. YOLO26 계열 비교와 m급 학습

![YOLO26 계열 비교와 m급 학습](assets/readme-slides/slide-03.jpg)

s급 모델 세 개를 비교한 뒤 YOLO26m을 학습했습니다.

### 04. 왜 열화상 데이터로 다시 학습했나

![왜 열화상 데이터로 다시 학습했나](assets/readme-slides/slide-04.jpg)

가시광 사전학습 가중치를 열화상 장면에 맞춘 이유입니다. 이론 참고: [전이학습](https://arxiv.org/abs/1411.1792).

### 05. FLIR 열화상으로 파인튜닝

![FLIR 열화상으로 파인튜닝](assets/readme-slides/slide-05.jpg)

COCO 가중치에서 시작해 FLIR 열화상에 맞췄습니다.

### 06. 30에폭으로 비교한 이유

![30에폭으로 비교한 이유](assets/readme-slides/slide-06.jpg)

30에폭은 최적값이 아니라 비교를 위한 최대 예산입니다.

### 07. 학습 곡선으로 본 FT와 LoRA

![학습 곡선으로 본 FT와 LoRA](assets/readme-slides/slide-07.jpg)

YOLO26s의 실제 에폭별 FT·LoRA 검증 곡선입니다.

### 08. 학습 데이터 규모에 따른 검증 정확도

![학습 데이터 규모에 따른 검증 정확도](assets/readme-slides/slide-08.jpg)

채운 점은 실측값, 빈 점은 보간값입니다.

### 09. 데이터가 늘면 정확도는 어떻게 달라질까

![데이터가 늘면 정확도는 어떻게 달라질까](assets/readme-slides/slide-09.jpg)

데이터와 업데이트 수가 함께 늘어난 실험입니다. 이론 참고: [데이터 규모와 성능](https://arxiv.org/abs/1712.00409).

### 10. 전체 파인튜닝과 LoRA를 왜 비교했나

![전체 파인튜닝과 LoRA를 왜 비교했나](assets/readme-slides/slide-10.jpg)

전체 가중치와 저랭크 행렬을 학습하는 방식을 비교했습니다. 원리 참고: [LoRA](https://arxiv.org/abs/2106.09685).

### 11. FT·LoRA: 학습량에 따라 달라진 결과

![FT·LoRA: 학습량에 따라 달라진 결과](assets/readme-slides/slide-11.jpg)

두 학습 예산에서 FT와 LoRA의 순위가 달랐습니다.

### 12. 같은 업데이트 횟수에서 FT·LoRA 비교

![같은 업데이트 횟수에서 FT·LoRA 비교](assets/readme-slides/slide-12.jpg)

5,049 업데이트 조건의 라벨 묶음별 결과입니다.

### 13. 왜 YOLO26m 검출기를 s로 증류했나

![왜 YOLO26m 검출기를 s로 증류했나](assets/readme-slides/slide-13.jpg)

YOLO26m 교사의 검출 특징을 YOLO26s 학생으로 옮기는 별도 실험입니다. [증류 원리](https://arxiv.org/abs/1503.02531)

### 14. 작은 검출기 증류는 종합 개선으로 이어지지 않았다

![작은 검출기 증류는 종합 개선으로 이어지지 않았다](assets/readme-slides/slide-14.jpg)

증류 후 오탐은 줄었지만 누락과 ID 변경은 늘었습니다.

### 15. 작은 사람에 NWD를 시험한 이유

![작은 사람에 NWD를 시험한 이유](assets/readme-slides/slide-15.jpg)

작은 상자의 IoU 민감도를 줄이려는 방법입니다. 원리 참고: [NWD](https://arxiv.org/abs/2110.13389).

### 16. 소형 객체 학습 후보 6개를 비교했다

![소형 객체 학습 후보 6개를 비교했다](assets/readme-slides/slide-16.jpg)

소형 객체 후보 6개와 기존 모델을 비교했습니다.


## 2. 자세 모델 학습과 자체 데이터

### 17. 자세 모델을 학습한 순서

![자세 모델을 학습한 순서](assets/readme-slides/slide-17.jpg)

공개 데이터에서 시작해 자체 카메라 후보로 이어졌습니다.

### 18. 데이터를 추가한 순서와 이유

![데이터를 추가한 순서와 이유](assets/readme-slides/slide-18.jpg)

데이터마다 보강하려는 장면이 달랐습니다.

### 19. 가림과 화면 밖 잘림을 학습에 반영했다

![가림과 화면 밖 잘림을 학습에 반영했다](assets/readme-slides/slide-19.jpg)

가림과 화면 밖 잘림을 학습에 반영했습니다.

### 20. 자세 모델의 학습 설정을 정했다

![자세 모델의 학습 설정을 정했다](assets/readme-slides/slide-20.jpg)

학습률과 배치, 에폭 설정을 정리했습니다.

### 21. 공개 데이터로 학습 결과를 검증했다

![공개 데이터로 학습 결과를 검증했다](assets/readme-slides/slide-21.jpg)

기존 E·F를 공개 데이터에서 평가했습니다.

### 22. 자체 카메라 데이터 확보

![자체 카메라 데이터 확보](assets/readme-slides/slide-22.jpg)

야외 15편과 실내 7편을 확보했습니다.

### 23. 자체 영상의 정답 기준

![자체 영상의 정답 기준](assets/readme-slides/slide-23.jpg)

직접 남긴 사람을 정답으로 쓰는 기준을 정했습니다.

### 24. 실내·야외 실제 라벨링 화면

![실내·야외 실제 라벨링 화면](assets/readme-slides/slide-24.jpg)

실제 실내·야외 편집 화면입니다. 선택 부위는 검수 필요 상태입니다.

### 25. 원거리 배경을 정리하고 정답 사람은 보존했다

![원거리 배경을 정리하고 정답 사람은 보존했다](assets/readme-slides/slide-25.jpg)

원거리 배경을 정리하고 정답 사람의 픽셀을 보존했습니다.

### 26. 야외 관절 후보를 한 명씩 검수했다

![야외 관절 후보를 한 명씩 검수했다](assets/readme-slides/slide-26.jpg)

야외 관절을 확인하고 불확실한 점은 미상으로 처리했습니다.

### 27. 실내 가림 장면은 박스와 관절을 다시 맞췄다

![실내 가림 장면은 박스와 관절을 다시 맞췄다](assets/readme-slides/slide-27.jpg)

실내 가림 장면의 박스와 보이는 관절을 다시 표시했습니다.

### 28. 학습 데이터 구성

![학습 데이터 구성](assets/readme-slides/slide-28.jpg)

자체 자료와 공개 자료의 학습 예제 구성입니다.

### 29. 범용 F에서 추가 학습하기

![범용 F에서 추가 학습하기](assets/readme-slides/slide-29.jpg)

범용 F에서 추가 학습하고 NF를 후보로 골랐습니다.

### 30. 첫 자체 학습 후보의 개선과 악화를 비교했다

![첫 자체 학습 후보의 개선과 악화를 비교했다](assets/readme-slides/slide-30.jpg)

먼 사람은 더 찾았지만 전체 검출과 오탐 기준은 통과하지 못했습니다.

### 31. 추적 점수는 올랐지만 모델은 바로 바꾸지 않았다

![추적 점수는 올랐지만 모델은 바로 바꾸지 않았다](assets/readme-slides/slide-31.jpg)

추적 점수는 올랐지만 다른 기준이 탈락해 교체하지 않았습니다.

### 32. 작은 사람의 상자 크기 오류를 찾아냈다

![작은 사람의 상자 크기 오류를 찾아냈다](assets/readme-slides/slide-32.jpg)

작은 사람과 큰 사람의 박스 기준이 달랐습니다.

### 33. 검수한 264장으로 V7 학습

![검수한 264장으로 V7 학습](assets/readme-slides/slide-33.jpg)

검수한 264장으로 학습했지만 복수 사전 기준은 통과하지 못했습니다.

### 34. V8의 개선과 악화가 함께 나타났다

![V8의 개선과 악화가 함께 나타났다](assets/readme-slides/slide-34.jpg)

중복은 줄었지만 더 작은 사람의 누락과 자세 AP는 악화됐습니다.


## 3. 사람 외형 모델과 증류

### 35. 왜 외형 모델에 증류를 썼나

![왜 외형 모델에 증류를 썼나](assets/readme-slides/slide-35.jpg)

열화상 데이터와 M1 제약을 고려해 사전학습 교사의 표현을 작은 학생에게 옮기려 했습니다.

### 36. SOLIDER는 어떤 특징을 배우나

![SOLIDER는 어떤 특징을 배우나](assets/readme-slides/slide-36.jpg)

SOLIDER와 Transformer 기반 사람 재식별의 원리를 살펴봤습니다. [논문](https://arxiv.org/abs/2303.17602)

### 37. 교사의 표현을 장치용 학생에 전달

![교사의 표현을 장치용 학생에 전달](assets/readme-slides/slide-37.jpg)

SOLIDER 교사의 특징을 RepVGG 학생에 전달해 M1에서 실행했습니다. [구조가 다른 모델 간 증류](https://arxiv.org/abs/2207.05273)

### 38. 증류하면 실제로 좋아졌을까

![증류하면 실제로 좋아졌을까](assets/readme-slides/slide-38.jpg)

이전 실험에서 교사 점수는 올랐지만 새 증류 학생은 기존 학생보다 낮았습니다.

### 39. 이전 실험: OTP2 외형 모델 학습

![이전 실험: OTP2 외형 모델 학습](assets/readme-slides/slide-39.jpg)

OTP2로 학습한 이전 외형 모델의 PC 결과입니다.

### 40. 후속 실험: 검수 데이터로 외형 모델 학습

![후속 실험: 검수 데이터로 외형 모델 학습](assets/readme-slides/slide-40.jpg)

검수 데이터 추가 학습 후 두 평가셋의 결과가 달랐습니다.

### 41. SOLIDER 교사 적응의 추가 이득은 확인되지 않았다

![SOLIDER 교사 적응의 추가 이득은 확인되지 않았다](assets/readme-slides/slide-41.jpg)

교사 적응의 추가 이득은 확인되지 않았습니다.


## 4. 가림 위치 예측과 박스 안정화

### 42. GRU는 사람이 가려졌을 때 어디를 예측하나

![GRU는 사람이 가려졌을 때 어디를 예측하나](assets/readme-slides/slide-42.jpg)

보이는 동안의 이력과 Kalman 예측으로 가려진 위치를 보정합니다. 이론 참고: [GRU](https://arxiv.org/abs/1406.1078).

### 43. 가려진 동안 위치를 기억하는 모델을 다시 학습했다

![가려진 동안 위치를 기억하는 모델을 다시 학습했다](assets/readme-slides/slide-43.jpg)

가려진 사람의 위치를 예측하도록 GRU를 다시 학습했습니다.

### 44. GRU와 Kalman: 같은 14편의 위치 오차

![GRU와 Kalman: 같은 14편의 위치 오차](assets/readme-slides/slide-44.jpg)

14편의 위치 오차에서는 새 GRU보다 Kalman이 낮았습니다.

### 45. 한 영상 재생에서 ID 유지도 비교했다

![한 영상 재생에서 ID 유지도 비교했다](assets/readme-slides/slide-45.jpg)

같은 녹화 한 편의 장치 재생 결과입니다.

### 46. Mamba 위치 기억도 다시 학습해 비교했다

![Mamba 위치 기억도 다시 학습해 비교했다](assets/readme-slides/slide-46.jpg)

Mamba 오차는 줄었지만 같은 자료의 Kalman보다 높았습니다.

### 47. 박스 안정화는 위치 기억과 별도로 시험했다

![박스 안정화는 위치 기억과 별도로 시험했다](assets/readme-slides/slide-47.jpg)

놓친 위치 예측과 보이는 박스 크기 필터는 별도입니다. 원리 참고: [1€ Filter](https://gery.casiez.net/1euro/).

### 48. 박스 크기 변화는 얼마나 줄었나

![박스 크기 변화는 얼마나 줄었나](assets/readme-slides/slide-48.jpg)

박스 크기 변화와 상체 통일 후보를 비교했습니다.

### 49. 검출 모델이 바뀔 때 박스가 튀는 것도 줄였다

![검출 모델이 바뀔 때 박스가 튀는 것도 줄였다](assets/readme-slides/slide-49.jpg)

모델 전환 시 박스 높이 변화를 비교했습니다.

### 50. 박스 안정화를 위해 시도하고 제외한 방법

![박스 안정화를 위해 시도하고 제외한 방법](assets/readme-slides/slide-50.jpg)

전체 좌표 필터와 박스 보정 GRU는 시험 후 제외했습니다.


## 5. FastTrackTr 추적

### 51. FastTrackTr 논문 원형과 M1 구현을 구분했다

![FastTrackTr 논문 원형과 M1 구현을 구분했다](assets/readme-slides/slide-51.jpg)

논문 원형과 M1 구현을 나란히 비교했습니다.

### 52. FastTrackTr 학습 조건을 설정했다

![FastTrackTr 학습 조건을 설정했다](assets/readme-slides/slide-52.jpg)

DanceTrack에서 시작해 열화상 자료로 이어 학습했습니다.

### 53. FastTrackTr 열화상 추가 학습 결과

![FastTrackTr 열화상 추가 학습 결과](assets/readme-slides/slide-53.jpg)

TMOT 평균은 올랐고 실내 두 녹화는 낮아졌습니다.


## 6. ONNX 변환과 M1 양자화

### 54. 학습한 모델을 M1에서 실행하기까지

![학습한 모델을 M1에서 실행하기까지](assets/readme-slides/slide-54.jpg)

학습 → ONNX → INT8 보정·컴파일 → DXNN 실행 순서입니다.

### 55. ONNX로 내보낼 때 무엇을 확인했나

![ONNX로 내보낼 때 무엇을 확인했나](assets/readme-slides/slide-55.jpg)

공개 변환 예시에서 ONNX 출력과 PyTorch 출력을 비교했습니다.

### 56. INT8 양자화와 보정은 무엇을 하나

![INT8 양자화와 보정은 무엇을 하나](assets/readme-slides/slide-56.jpg)

보정 입력으로 값의 범위를 관찰하고 정수 연산에 맞춰 변환합니다.

### 57. 모델마다 보정 자료와 입력이 달랐다

![모델마다 보정 자료와 입력이 달랐다](assets/readme-slides/slide-57.jpg)

모델별 보정 이미지 수와 설정을 구분했습니다.

### 58. DXNN 출력에서 사람 박스까지

![DXNN 출력에서 사람 박스까지](assets/readme-slides/slide-58.jpg)

DXNN의 여섯 출력을 서버에서 풀어 NMS와 추적에 넘깁니다.

### 59. 외형 모델의 ONNX·INT8 변환 예시

![외형 모델의 ONNX·INT8 변환 예시](assets/readme-slides/slide-59.jpg)

공개된 OTP2 RepVGG의 ONNX·256 crop 보정 예시입니다.

### 60. FastTrackTr을 3개 그래프로 나눠 변환했다

![FastTrackTr을 3개 그래프로 나눠 변환했다](assets/readme-slides/slide-60.jpg)

FastTrackTr을 AE·B0·B1 세 그래프로 분리해 변환했습니다.

### 61. 변환 후 어떤 검증까지 했나

![변환 후 어떤 검증까지 했나](assets/readme-slides/slide-61.jpg)

변환 기록, 장치 동작과 정확도 정합을 따로 확인해야 합니다.

### 62. M1에서 처리량을 높인 방법

![M1에서 처리량을 높인 방법](assets/readme-slides/slide-62.jpg)

저장 영상에서 검출과 추적·외형 추출을 겹쳐 처리량을 높였습니다.

### 63. 학습한 검출기의 M1 적용

![학습한 검출기의 M1 적용](assets/readme-slides/slide-63.jpg)

검출기를 INT8으로 변환해 M1에서 시험했습니다.

### 64. M1에서 s와 m의 정확도·호출 시간을 비교했다

![M1에서 s와 m의 정확도·호출 시간을 비교했다](assets/readme-slides/slide-64.jpg)

후속 장치 시험에서 s·m의 정확도와 호출 시간을 비교했습니다.

### 65. 실제 운영 화면에서 검출과 ID를 확인했다

![실제 운영 화면에서 검출과 ID를 확인했다](assets/readme-slides/slide-65.jpg)

실제 운영 화면과 별도 녹화의 M1 출력을 보여줍니다.


## 7. 짐벌 제어

### 66. 화면 오차로 짐벌 제어하기

![화면 오차로 짐벌 제어하기](assets/readme-slides/slide-66.jpg)

화면 중심 오차를 팬·틸트 명령으로 연결했습니다.

### 67. 왜 PID 설정과 불감대를 바꿨나

![왜 PID 설정과 불감대를 바꿨나](assets/readme-slides/slide-67.jpg)

실제 장치와 가상 표적 시험을 바탕으로 설정을 골랐습니다. 일반 참고: [PID 튜닝](https://www.nt.ntnu.no/users/skoge/publications/2003/tuningPID/finalpaper.pdf).

### 68. 가림으로 사람을 놓쳤을 때 대응 기능을 추가했다

![가림으로 사람을 놓쳤을 때 대응 기능을 추가했다](assets/readme-slides/slide-68.jpg)

가림 중 위치 유지와 대상 보호 설정을 적용했습니다.

### 69. 불감대를 바꾸고 짐벌 응답을 측정했다

![불감대를 바꾸고 짐벌 응답을 측정했다](assets/readme-slides/slide-69.jpg)

상하 반전은 줄었지만 별도 가로 시험의 뒤처짐은 늘었습니다.

### 70. 같은 FLIR 영상에서 가림 전과 재등장 뒤를 비교했다

![같은 FLIR 영상에서 가림 전과 재등장 뒤를 비교했다](assets/readme-slides/slide-70.jpg)

같은 FLIR 영상의 가림 전과 재등장 뒤입니다.


## 남은 검증

### 71. 결과와 남은 과제

![결과와 남은 과제](assets/readme-slides/slide-71.jpg)

확인한 결과와 더 필요한 자료를 구분했습니다.
