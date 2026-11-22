# C안 예비자료 설명

## 01. 최종 모델 선정 기준

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

빈 칸은 실제 측정 전이다. 기존 s/m·F/NF 결과를 이 표에 대입하지 않는다.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md">S7 윤관 · 실험 원문 출처</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a>

## 02. 평가 지표 정의

원표·조건은 해당 장과 아래 출처를 함께 확인한다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/긴버전/발표노트.md">S8 정하건 · 추적 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a> · <a href="https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md">S10 model-bank · 11-17 공개 발표 근거</a>

## 03. 추적 성능 원표

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

공식 기본값의 IDSW가 적어도 누락이 매우 많았다. PC 기준 재현의 IDSW 784와 보드775의 차이도 원문에 기록되어 있다.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a>

## 04. PC 통신 인터페이스

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

윤오름 담당 PC 앱 구현 자료 기준. 최종 데모에 쓰는 앱·전송 설정은 별도 확인.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/model-bank-GUI-제어-비교분석.md">S3 윤오름 · GUI·제어 구현 비교</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/김재남/speaker-notes.md">S4 김재남 · Runtime·전후처리·통신 대본</a>

## 05. 조준점 및 제어 명령

이전 v27의 각도 표시는 명령 기반 추정이다. 11/20 짐벌이 보고한 각도 눈금 기능은 미적용 기록이므로 실측 각도로 확정하지 않는다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/model-bank-GUI-제어-비교분석.md">S3 윤오름 · GUI·제어 구현 비교</a>

## 06. 후속 모델 실험

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

FastTrackTr와 기존 추적기 점수는 동일 실행 전후가 아님

<a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a> · <a href="sources/latest-20261121/윤관/학습기록_상체검출기.md">S19 상체 모델 학습·재현 기록</a> · <a href="sources/latest-20261121/윤관/학습기록_위치예측.md">S20 위치 예측 학습 기록</a> · <a href="sources/latest-20261121/윤관/학습기록_FastTrackTr.md">S21 FastTrackTr 학습 기록</a>

## 07. 외형 및 위치 기억

자체14편·놓침238건에서Kalman0.110, 수정GRU0.122이며10편에서Kalman이낮았습니다. IDF1차이는+0.6%p,90%구간−0.8~+2.3%p였습니다. 개발에사용한자료의비교입니다.

자체14편·놓침238건 · 이전 자료의0.118과 표본·수정을 혼합하지 않음

<a href="sources/latest-20261121/윤관/학습기록_위치예측.md">S20 위치 예측 학습 기록</a> · <a href="sources/latest-20261121/윤관/근거_슬라이드별.md">S22 11/21 슬라이드·장치 비교 근거</a> · <a href="sources/revision-20261122/manifest.json">S26 11/22 비교 결과·절충 정정</a>

## 08. 공개·혼합 학습 비교

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

자세·상자 모델의 과거 후보 비교. 본문 검출기 FT/KD나 최종 현장 후보와 혼합하지 않는다.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/notes.md">S5 윤관 · 학습·평가·제어 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md">S7 윤관 · 실험 원문 출처</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md">S11 11-18 검출 학습·평가 원본 대조</a>

## 09. 시간 요구사항 및 계측 구간

원표·조건은 해당 장과 아래 출처를 함께 확인한다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md">S7 윤관 · 실험 원문 출처</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a> · <a href="https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md">S10 model-bank · 11-17 공개 발표 근거</a>

## 10. 검출 성능 및 호출 시간

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

두 모델의 학습 이력이 다르므로 크기만의 효과로 단정하지 않는다. NPU 호출시간은 종단 지연이 아니다.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/notes.md">S5 윤관 · 학습·평가·제어 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/index.html">S6 윤관 · 결과 그림·측정 조건</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md">S7 윤관 · 실험 원문 출처</a>

## 11. 검출 모델 학습 기록

원표·조건은 해당 장과 아래 출처를 함께 확인한다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md">S11 11-18 검출 학습·평가 원본 대조</a>

## 12. 전체 학습과 증류 비교

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

YOLO26s · FLIR 4,196장 · seed 202 · 각 60 epoch. 체크포인트의 별도 평가값이며 학습 CSV의 전체 클래스 지표와 구분.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md">S11 11-18 검출 학습·평가 원본 대조</a>

## 13. INT8 배포 및 장치 성능

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

이 배포 사례의 보정 자료는 8장. 모든 모델의 보정 조건으로 일반화하지 않는다. 동일 입력 FP32↔INT8 정확도는 별도 확인 대상.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/notes.md">S5 윤관 · 학습·평가·제어 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/index.html">S6 윤관 · 결과 그림·측정 조건</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md">S7 윤관 · 실험 원문 출처</a>

## 14. OC-SORT 동작 원리

원표·조건은 해당 장과 아래 출처를 함께 확인한다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/긴버전/발표노트.md">S8 정하건 · 추적 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a>

## 15. PC 추적 옵션 비교

원표·조건은 해당 장과 아래 출처를 함께 확인한다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/긴버전/발표노트.md">S8 정하건 · 추적 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md">S9 정하건 · 추적 근거 비교표</a>

## 16. Runtime 부하 시험

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

YOLO26-640 · 조건별 15초×3회 · 객체 0개로 확인한 저장 프레임 20장 반복. 실제 NPU 사용, GUI·짐벌 제외. inflight는 코어 개수가 아님.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/김재남/measurements/orangepi-20261116-retry/report.md">S12 실제 NPU 메모리 재생 부하 시험</a>

## 17. 짐벌 제어 상세

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

조건별 각 1회. 가로 지표 악화도 함께 보고.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/model-bank-GUI-제어-비교분석.md">S3 윤오름 · GUI·제어 구현 비교</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md">S11 11-18 검출 학습·평가 원본 대조</a>

## 18. 영상 출력 지연 시험

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

같은 서버의 녹화 재생 ABBA 비교. 실카메라·브라우저 종단 지연 결과가 아니며, 출력 간격 p95 33.3ms 목표는 미달.

<a href="https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md">S10 model-bank · 11-17 공개 발표 근거</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a>

## 19. 최신 추적기 비교

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

동일 YOLO26s 검출·18편. ByteTrack은 보드, 나머지는 PC이므로 동일 하드웨어 전후 비교로 표현하지 않는다. BoT-SORT ReID·CMC 미사용.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7249d7b/정하건/정하건_v3/근거_비교표.md">S14 정하건 v3 · 3종 추적·GUI 교체·성능</a>

## 20. 추적기 카탈로그 및 교체

원표·조건은 해당 장과 아래 출처를 함께 확인한다.

새 추적기는 다음 프레임 경계에서 교체. 생성 실패 시 기존 추적기를 유지한다. BoT-SORT 최종: new 0.5 · match 0.9 · unconfirmed 0.6. 근거는 팀원 v3 문서이며 이번 편집에서 장치 재시험은 하지 않았다.

<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7249d7b/정하건/정하건_v3/근거_비교표.md">S14 정하건 v3 · 3종 추적·GUI 교체·성능</a>

## 21. 검출기 후속 비교

자체703장 중578학습·63검증·62시험. 기존 E10이 검증54/63, 시험61/62장을 학습에서 봤다. 자체시험의 E10 우위를 독립 근거로 쓰지 않는다. 실내·외 추적 양쪽을 이긴 후보가 없어 E10 유지.

OTP2 검증934장 · 후보 E숫자는 각 학습의 epoch / OTP2 검증934장 · 후보 E숫자는 각 학습의 epoch

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a> · <a href="sources/latest-20261121/윤관/학습기록_상체검출기.md">S19 상체 모델 학습·재현 기록</a>

## 22. 학습 재현 기록

FLIR 검출기와 공개 자세 모델은 별도 출발점이다. 공개 C의3번째 epoch가 F, 코드 파일명은 C_control_v1_epoch2.pt이다. 별도OTP2시험에서 E10 46.0, 재현 대조44.4, CLAHE45.2로 CLAHE 차이는 재현 오차보다 작았다.

학습 파일·가중치·자료8,128개 검증 기록 · 학습로그 CSV는 스냅샷에 보존 / 학습 파일·가중치·자료8,128개 검증 기록 · 학습로그 CSV는 스냅샷에 보존

<a href="sources/latest-20261121/윤관/학습기록_상체검출기.md">S19 상체 모델 학습·재현 기록</a>

## 23. SOLIDER 교사와 증류

LUPerson 원본과11/10·15 증류 교사 파일은 다르다. SOLIDER 직접교체 비교는 기존 근거에 있으나 원본 RESULT_KO 파일을 최신 조사에서 다시 찾지 못했다. 기존 PC 1회 IDF1 66.74→66.57은 잠정 인용이며 장치 효과 근거로 쓰지 않는다.

교사 정정05e223f · 직접교체 원본 결과 재확인 한계 보존 / 교사 정정05e223f · 직접교체 원본 결과 재확인 한계 보존

<a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a>

## 24. 외형 모델 학습 비교

SOLIDER 파인튜닝은5구성·한시드이고 선택점수의 정점 후 하락했다. 교사 원본 대비 이득은 있으나 한 사람의 사전 규칙 위반으로 판단불가. 학생3종도 사전 규칙상 더 좋지 않음. E는 실내4명에서51.1→61.2%이나 전체는 불리해 시험 선택지로만 추가. NPU 정확도·속도 미측정.

진단 코사인0.982는 장치 추적 정확도가 아님 / 진단 코사인0.982는 장치 추적 정확도가 아님

<a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a> · <a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 25. 모델 추천과 선택 기록

이 표는11/20~21 시점 기록의 구분이다. 현재 실행중인 모델은 이번 편집에서 조회하지 않았다. 최종 장치 명령줄과 파일 해시를 받아야 단일 운용 구성으로 확정할 수 있다.

추천·선택·시험 추가·실제 실행을 구분 / 추천·선택·시험 추가·실제 실행을 구분

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a> · <a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a> · <a href="sources/revision-20261122/manifest.json">S26 11/22 비교 결과·절충 정정</a>

## 26. 서버 C++ 이식 비교

각 약1800장·무인 실카메라 별도 비교. 출력·좌표 복원, KeepID 위치 계산, GRU입력도 C++로 보완했지만 모두 같은 전체 지연 실행이 아니다. p95 감소와 최대 증가를 같이 표시한다.

모델뱅크 서버 일부 C++화 · 팀 공통 C++ Runtime과 별도 / 모델뱅크 서버 일부 C++화 · 팀 공통 C++ Runtime과 별도

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 27. 지연 대안과 보류

단위ms. 512입력은 지연이 줄었지만 INT8 정확도 평가가 없었다. 공유메모리는 최대35.637ms로 파이프30.155보다 나빴다. 이 대안들을 최종 장치 채택 성능으로 요약하지 않는다.

고밀도 녹화 · 정확도와 실행 조건이 달라 현재 시연 보장으로 사용하지 않음 / 고밀도 녹화 · 정확도와 실행 조건이 달라 현재 시연 보장으로 사용하지 않음

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 28. INT8 컴파일 옵션

10/29 FLIR학습YOLO26s·3749프레임 M1 INT8의 aggressive_partitioning 결과다. 약24.7% 빨라졌으나 현장E10 분할은 CPU부분0이라 해당옵션을 쓰지 않았다. 새 분할 지연 개선의 원인으로 이 옵션을 설명하지 않는다.

10/29 과거 별도모델 · 현재 분할 파일에는 옵션 미사용 / 10/29 과거 별도모델 · 현재 분할 파일에는 옵션 미사용

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 29. 번호 가드 설정

cost_first와feat_guard는 코드기본끔이지만11/20 17:56 장치재시작 뒤 켬기록이 있다. 장치재생효과·CPU비용은 미측정. depth_order는번호변경43→54여서끔. pre_capture도끄기로함. KeepID복구와이두가드는별도기능이다.

개발 라벨9편 PC FP32 · IDF1 최고와 뺏김 최소 설정은 다름 / 개발 라벨9편 PC FP32 · IDF1 최고와 뺏김 최소 설정은 다름

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a> · <a href="sources/latest-20261121/윤관/근거_슬라이드별.md">S22 11/21 슬라이드·장치 비교 근거</a>

## 30. 박스 보정과 표시

11월21일코드에서일반끄기옵션을제거했습니다. 기본body, 변환표가없으면size이며오류시자동비활성화가가능합니다. PC녹화에서키변화상위1퍼센트는0.071→0.043, 조준떨림은0.0195로같았습니다. 코드의장치반영과실촬영효과는별도확인이필요합니다.

코드 기본값·표시 범위·실제 적용을 구분 / 코드 기본값·표시 범위·실제 적용을 구분

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/afa734f399a2c2e53171abd3131fffddc64351b3/윤관/근거_최신_20261119.md">S15 윤관 11-19 · 상체 E10·표시·실카메라 NPU</a> · <a href="sources/revision-20261122/manifest.json">S26 11/22 비교 결과·절충 정정</a>

## 31. 짐벌 설정과 검증 범위

기본PD는최고속도10에서고른값이고운영100기록이있다. 결과즉시제어의약8ms간격명령이실제짐벌에서받아지는지미확인. 190~210ms는장면부터반응의추정합이며실측종단아님. 최종실행설정은추가확인.

11/15~20 과거 상태 기록 · 현재 장치를 이번 편집에서 재시험하지 않음 / 11/15~20 과거 상태 기록 · 현재 장치를 이번 편집에서 재시험하지 않음

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 32. FastTrackTr 학습 이력

검출과번호를한모델로처리하는후보다. TMOT6편평균IDF1이올랐으나기존검출+추적수준에못미쳐11/15중단하고시험선택지로유지했다. 추적기v3표와동일실행전후가아니다. 정식성능달성사례로쓰지않는다.

번호 손실·학습곡선 원본 CSV 보존 · 배포 선택지와 기본 모델 구분 / 번호 손실·학습곡선 원본 CSV 보존 · 배포 선택지와 기본 모델 구분

<a href="sources/latest-20261121/윤관/학습기록_FastTrackTr.md">S21 FastTrackTr 학습 기록</a>

## 33. 상체·외형 학습 곡선

원본 CSV의 epoch별 기록을 그렸다. 왼쪽 대조와 CLAHE의 학습 손실이 줄어드는 것만으로 독립 검출 성능 향상을 판정하지 않는다. 오른쪽도 학습 쌍에 대한 손실로 일반화 근거가 아니다. 상세 설정과 최종 시험은 학습 기록을 따른다.

원본 로그 관측점 연결 · 0 기준 축 · 손실 감소와 독립 성능을 구분 / 원본 로그 관측점 연결 · 0 기준 축 · 손실 감소와 독립 성능을 구분

<a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a> · <a href="sources/latest-20261121/윤관/학습기록_상체검출기.md">S19 상체 모델 학습·재현 기록</a>

## 34. SOLIDER 선택 곡선

A~E는 서로 다른 파인튜닝 구성이다. 선택용 점수의 이른 정점 뒤 하락과 최종 시험 판정을 구분한다. 학생 a_A, b_START, e_E의 선택 점수도 독립 시험 성능이 아니다. 단일 시드 비교이며 선택 점수 우위로 장치 채택을 주장하지 않는다.

CHOOSE 선택에 사용한 기록 · 독립 시험 점수와 별도 / CHOOSE 선택에 사용한 기록 · 독립 시험 점수와 별도

<a href="sources/latest-20261121/윤관/학습기록_외형모델.md">S18 외형 모델 학습·교사 정정</a>

## 35. 위치·통합 모델 학습 곡선

왼쪽은 원본 CSV에 기록된 첫 세 실행을 각자 epoch 기준으로 비교한다. val-A는 선택용이며 다른 자료의 최종 위치 오차와 섞지 않는다. 오른쪽은 DanceTrack의 손실 수정 뒤 단계만 따로 그렸으며 로그의 누적 평균이다. 서로 다른 단계와 재시작 로그를 이어 가상의 연속 곡선을 만들지 않았다.

위치 val-A: 선택용 · FastTrackTr: dance_ep3-5_idfix 기록만 / 위치 val-A: 선택용 · FastTrackTr: dance_ep3-5_idfix 기록만

<a href="sources/latest-20261121/윤관/학습기록_위치예측.md">S20 위치 예측 학습 기록</a> · <a href="sources/latest-20261121/윤관/학습기록_FastTrackTr.md">S21 FastTrackTr 학습 기록</a>

## 36. 검출 거리 검증

현장에서는 먼저 거리별 검출을 확인합니다. 모델과 해상도, 장소를 고정하고 사람이 얼마나 작아지는지와 누락, 오검출을 함께 기록합니다. 몇 미터부터 몇 미터까지를 요구할지와 통과 기준은 아직 확정 전입니다. 기존 AP 점수를 거리 성능으로 대신 적지 않고 같은 현장에서 측정해야 합니다.



<a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md">S2 윤오름 · 시스템·제어·GUI 대본</a> · <a href="https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md">S11 11-18 검출 학습·평가 원본 대조</a>

## 37. ID 유지 검증

PC 녹화의 ID 변경과 가드 결과는 확보했지만 최종 장치의 현장 ID 유지 검증은 남았습니다. 같은 사람을 잇는지, 다른 사람으로 넘어가는지, 얼마나 끊겼는지를 정답과 비교해야 합니다. 유지시간과 허용 끊김 기준도 아직 없습니다. PC의 47에서43을 현장 유지율로 바꾸어 말하지 않습니다.

동일 시연 경로·정답 라벨·반복 결과 필요

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a> · <a href="sources/latest-20261121/윤관/학습기록_위치예측.md">S20 위치 예측 학습 기록</a> · <a href="sources/latest-20261121/윤관/근거_슬라이드별.md">S22 11/21 슬라이드·장치 비교 근거</a>

## 38. 장치 상태 이력

재설치 전후의 실행 구성을 추적한 기록입니다. 11월20일 재설치 때 로컬 분할 연결과 KeepID 번호 복구 코드가 빠져 전체 화면 방식으로 실행됐습니다. 그 직후 무인 실카메라12분에서33밀리초 초과 비율은68.6퍼센트였습니다. 이후 분할 연결과 가드·박스 보정이 추가돼 운영 모델과 실행 경로를 함께 관리했습니다.

11/20 오전 전체 화면 실행 기록 · 후속 분할 모델 파일 확인과 최종 실행 검증은 구분

<a href="sources/latest-20261121/윤관/근거_최신_20261120.md">S17 11/20–21 추가 실험·장치 상태</a>

## 39. 추가 검출 모델 비교 조건

모델뱅크0e3dd540의11월22일추천갱신과장치재생비교입니다. 관절미표기인물의신뢰도를0으로학습한점이낮은관절신뢰도의원인으로기록됐습니다. close_aim은상자기준이어서해당관절신뢰도하락의직접영향이없다는코드설명과실제보행짐벌미시험을함께기록합니다. 이슬라이드는실측종단이나새현장독립성능을보장하지않습니다.

추천·적용 기록은11/22시점. 원문보고구간의신뢰수준을임의로95%로표기하지않음.

<a href="sources/revision-20261122/manifest.json">S26 11/22 비교 결과·절충 정정</a> · <a href="sources/revision-20261122/model-bank-recommended.json">S27 11/22 모델뱅크 추천 원문</a>
