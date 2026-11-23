# C안 출처·수치 추적표

기준: 로컬 presentation8a195d7(2026-11-22 21:13 KST). B 기준9819922에서 갱신. 장치·학습·성능 시험은 재실행하지 않았다.

## 출처

- **S1** [공통 목차·20분·제작 규격](https://app.notion.com/p/4169de3f14a280ee9e05cec320dfb929)
- **S2** [윤오름 · 시스템·제어·GUI 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md)
- **S3** [윤오름 · GUI·제어 구현 비교](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/model-bank-GUI-제어-비교분석.md)
- **S4** [김재남 · Runtime·전후처리·통신 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/김재남/speaker-notes.md)
- **S5** [윤관 · 학습·평가·제어 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/notes.md)
- **S6** [윤관 · 결과 그림·측정 조건](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/index.html)
- **S7** [윤관 · 실험 원문 출처](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md)
- **S8** [정하건 · 추적 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/긴버전/발표노트.md)
- **S9** [정하건 · 추적 근거 비교표](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md)
- **S10** [model-bank · 11-17 공개 발표 근거](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md)
- **S11** [11-18 검출 학습·평가 원본 대조](https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md)
- **S12** [실제 NPU 메모리 재생 부하 시험](https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/김재남/measurements/orangepi-20261116-retry/report.md)
- **S16** [11-10 PID 후보 비교·PD 선택 근거](sources/pd-selection/PID_TUNING_RECORD_20261110.md)
- **S15** [윤관 11-19 · 상체 E10·표시·실카메라 NPU](https://github.com/lwir-deepx-tracking-system/presentation/blob/afa734f399a2c2e53171abd3131fffddc64351b3/윤관/근거_최신_20261119.md)
- **S14** [정하건 v3 · 3종 추적·GUI 교체·성능](https://github.com/lwir-deepx-tracking-system/presentation/blob/7249d7b/정하건/정하건_v3/근거_비교표.md)
- **S13** [팀원 담당 업무 · 사용자 제공](team-roles.md)
- **S25** [그림·실측 그래프 재구성 원자료](sources/visual-reference/manifest.json)
- **S26** [11/22 비교 결과·절충 정정](sources/revision-20261122/manifest.json)
- **S27** [11/22 모델뱅크 추천 원문](sources/revision-20261122/model-bank-recommended.json)
- **S28** [모델뱅크 스레드·큐 코드 동결본](sources/pipeline-20261123/manifest.json)
- **S29** [김재남 Runtime·모델뱅크 파이프라인 대조](sources/pipeline-20261123/comparison.md)
- **S17** [11/20–21 추가 실험·장치 상태](sources/latest-20261121/윤관/근거_최신_20261120.md)
- **S18** [외형 모델 학습·교사 정정](sources/latest-20261121/윤관/학습기록_외형모델.md)
- **S19** [상체 모델 학습·재현 기록](sources/latest-20261121/윤관/학습기록_상체검출기.md)
- **S20** [위치 예측 학습 기록](sources/latest-20261121/윤관/학습기록_위치예측.md)
- **S21** [FastTrackTr 학습 기록](sources/latest-20261121/윤관/학습기록_FastTrackTr.md)
- **S22** [11/21 슬라이드·장치 비교 근거](sources/latest-20261121/윤관/근거_슬라이드별.md)
- **S23** [11/20 추적기 대본 개정](sources/latest-20261121/정하건/정하건_v3/발표노트.md)
- **S24** [추적기 비교 원표·CMC 미사용](sources/latest-20261121/정하건/정하건_v3/근거_비교표.md)

## C안 장별 출처

| 장 | 제목 | 근거 |
|---|---|---|
| 1 | 프로젝트 소개 | S1, S2 |
| 2 | 목차 | S1 |
| 3 | 팀 구성 및 역할 | S13 |
| 4 | 프로젝트 소개 | S2, S5, S8 |
| 5 | 시스템 요구사항 | S1, S17 |
| 6 | 시스템 구성 | S2, S3, S4, S14 |
| 7 | 소프트웨어 구성 | S3, S4, S14, S17 |
| 8 | 멀티스레드 파이프라인 | S28, S29 |
| 9 | 큐와 전달 정책 | S28, S29 |
| 10 | 열화상 검출 과제 | S5, S11 |
| 11 | 현장 데이터 구축 | S5, S11, S15, S25 |
| 12 | 학습 데이터 구성 | S19, S25 |
| 13 | 상체 박스 기준 | S19, S25 |
| 14 | 상체 모델 학습 | S15, S19, S25 |
| 15 | 가림·잘림 증강 | S19, S25 |
| 16 | 상체 검출 결과 | S6, S15, S25, S26 |
| 17 | 후속 학습 채택 판단 | S17, S19, S25, S26 |
| 18 | 검출기 추가 비교 | S26, S27 |
| 19 | 모델 배포 과정 | S11, S17, S18, S25 |
| 20 | 외형 모델 비교 | S18, S22, S25, S26 |
| 21 | 추적 알고리즘 선정 과정 | S14, S23, S24 |
| 22 | 추적 연속성 비교 | S8, S9, S14 |
| 23 | 최종 추적기 선정 | S14, S23, S24 |
| 24 | BoT-SORT 최종 설정 | S14, S24 |
| 25 | 가림 위치 예측 | S8, S9, S25, S20 |
| 26 | 번호 유지 보완 | S17, S20, S22, S26 |
| 27 | 처리 지연 요인 | S4, S12 |
| 28 | 두 NPU 동시 타일 처리 | S12, S15, S25 |
| 29 | 분할 모델 변환 | S17, S19, S25, S26 |
| 30 | 실카메라 지연 측정 | S15, S17 |
| 31 | 장시간·혼잡 조건 | S17, S25 |
| 32 | 추적 좌표와 조준점 | S15, S17, S25 |
| 33 | PD 제어 선택 근거 | S3, S16 |
| 34 | 수동 전환 및 정지 | S2, S3 |
| 35 | 짐벌 제어 시험 | S5, S6, S11, S16, S25 |
| 36 | 짐벌 응답 실측 | S17, S25 |
| 37 | 가상 카메라 시험 | S17, S22, S25, S26 |
| 38 | 놓침 대응과 절충 | S17 |
| 39 | 상체 추적과 전신 표시 | S2, S3, S4, S14, S15, S25 |
| 40 | GUI 조작 순서 | S2, S3, S14 |
| 41 | 추적기 변경 및 응답 | S3, S4, S10, S14 |
| 42 | 시연 구성 | S14, S17 |
| 43 | 통합 시연 | S1, S2, S6 |
| 44 | 처리 성능 정리 | S15, S17 |
| 45 | 주요 성과 | S14, S15, S17, S19, S26, S24, S27 |

## 그림·그래프 재구성

| C안 장 | 활용한 원자료 |
|---|---|
| 현장 데이터 구축 | m13_labeling.html, 실제_라벨링_실내.png, 실제_라벨링_야외.png |
| 학습 데이터 구성 | m09_data.html, openthermalpose2-official-example.png |
| 상체 박스 기준 | m14_body_box.html |
| 상체 모델 학습 | m10_pose_lineage.html |
| 가림·잘림 증강 | m11_occlusion_aug.html, m11-occlusion-aug.jpg |
| 상체 검출 결과 | m18_e10.html |
| 후속 학습 채택 판단 | m19_retrain.html |
| 모델 배포 과정 | m27_int8.html, openthermalpose2-official-example.png |
| 외형 모델 비교 | m21b_reid_table.html |
| 표적 가림과 ID 유지 | m22_position.html |
| 두 NPU 동시 타일 처리 | m29_split.html, 20261119-real-upper-replay.jpg |
| 분할 모델 변환 | m29b_split_model.html |
| 장시간·혼잡 조건 | m30_tail.html |
| 추적 좌표와 조준점 | m31_gimbal_loop.html |
| 짐벌 제어 시험 | m32_pd.html, gimbal-s7-actual.svg |
| 짐벌 응답 실측 | m33_plant.html |
| 가상 카메라 시험 | k08_virtual_cam.html |
| 상체 추적과 전신 표시 | m25_fullbody.html, 20261119-real-upper-replay.jpg, 20261119-real-full-replay.jpg |

원본 HTML의 SVG·실제 라벨링·장치 재생 이미지를 선택해 C안의 장별 설명 구조로 재배치했다. 그림별 SHA256과 원본 경로는 S25에 보존했다. 소스 PDF 전체 페이지를 슬라이드 이미지로 복사하지 않았다. 짐벌 응답 곡선은 실측 요약값 기반의 모형으로 표시하고, 실측 시계열은 불감대 시험 파형에만 사용한다.

## 최신 수치와 조건

| 항목 | 값 | 조건 | 한계 | 출처 |
|---|---|---|---|---|
| 검출기 후보 | 박스 AP 46.28 / 48.16 / 45.37 / 44.68%; 표준 증강 관절 AP 77.31% | OTP2 검증 934장 | 독립 현장 시험 아님; 자체 분할은 학습 노출 존재 | S17,S19 |
| 외형 모델 M1 비교 | 정답 0.616 / 0.672 / 0.892 / 0.764; 시간 5.03 / 5.02 / 1.26 / 1.28 ms | ViT-lite FT·증류, RepVGG OTP2·검수264 순; 동일 M1 INT8 | 장치 선택·추천과 학습판을 구분; 실내 질의176 | S18,S22 |
| 번호 유지 | GRU 0.336→0.122, Kalman0.110; KeepID47→43; 가드20→17 | 위치14편 놓침238건; 번호9편3877장 PC | 개발 노출; 장치 효과 미측정 | S17,S20,S22 |
| 후속 지연 | 18497장 초과5·최대44.582ms; 4명 p95 27.16·초과4/805; 고밀도 p95 42.52·초과217/592 | 별도 서버; 사람 녹화는 C++ 이식 전 | 세 조건 별도; 최종 Runtime 종단 아님 | S17 |
| 짐벌 | SPD10/20/30=305/630/약930px/s; 명령반응108ms; vel+20%p·fused+6%p | 속도 직접실측; 재포착 가상시험 별도 | fused95%구간−11~+21%p; 실제사람 종단 미측정 | S17 |

## 11/23 스레드·큐 대조

- 신규8·9장은 모델뱅크549324c 실카메라 Feed 경로의 코드 구조다. 김재남의 팀 C++ Runtime 도식을 참고하고 실제 스레드·큐 정책으로 재구성했다.
- 입력대기 최대3·밀리면 최신1, 제출결과 순서 소비, 짐벌 미전송 관측 슬롯1을 구별한다. lossless 재생·신원전환 증거 경로는 예외다.
- S28은 코드 동결·SHA256, S29는 Runtime과 모델뱅크 대조표다. 실제 데모 활성 설정과 성능은 새로 검증하지 않았다.

## 11/22 추가 반영 — 기존 기록보다 우선

- 검출 추천은 own9e 시드 1. 모델9 대비 장치 INT8·분할 녹화18편 IDF1 +4.50%p(보고 구간 +1.26~+10.26), 번호 변경 차이0회(−9~+10). 구간의 신뢰 수준은 원문 미기재. 어깨 신뢰도 기준 충족률은92→9%.
- 외형 추천은 기본 RVGGA0_REID2C256. 과거 OTP2 학습판의 검색 정답률0.892와 속도를 현재 추천 모델의 성능으로 대입하지 않는다.
- 최초 GRU 적용 근거: 공개 val-B 위치 오차 TMOT 0.352→0.223, DanceTrack 0.295→0.213(Kalman→GRU). 자체 14편 위치 오차는 Kalman 0.110, 수정 GRU 0.122, 칼만 전환 규칙 포함 0.118. 자체 14편의 IDF1 차이는 +0.6%p(90% 구간 −0.8~+2.3%p). 장치 seq_018 한 편의 IDF1은 Kalman 71.81%, GRU 75.36%. [장치 재생 근거](https://github.com/lwir-deepx-tracking-system/model-bank/blob/0e3dd540ff8a9953a6e7725f59393c782a3d9d5a/HANDOFF.md#L1261).
- KeepID: 번호 변경47→43, 장기 뺏김19→20. 두 가드 추가 시 뺏김20→17, IDF1 82.3% 동일.
- 학습264장 FP32 타일 진단: 누락230→218, 일부 관절 위치 오차 증가. 독립 INT8 정확도 평가와 구별.
- 박스 보정은 기본 body, 변환표 부재 시 size이며 오류 시 자동 비활성화 가능. 장치 적용은 별도 확인.
- 시각자료19개 HTML을 최신 원본에서 동기화했다. 하드웨어·팀원 사진6개 및 라벨링 등 이미지8개는 기존 원본과 동일하다.
- sources/revision-20261122는 두 커밋의 근거22개와 모델뱅크 원문2개를 SHA256으로 보존한다.

## 보존한 근거와 해석

- 25.71ms는11/19 E10+3·재설치 전·모드별65초의 서버 p95. 큐버림1; 전프레임·종단 통과 아님.
- 11/20 재설치 뒤 전체화면 기록에서33ms초과14803/21579=68.6%. 이 시점 수치를 후속 분할 상태로 확대하지 않는다.
- 추적기 CMC:11/20 새 대본은 일반 기능을 설명하지만 동일PC 비교 원표는 CMC·ReID 미사용. 효과를 입증했다고 서술하지 않는다.
- SOLIDER 직접교체 원본 RESULT_KO는11/21 학습기록 조사에서 재확인 못함. 기존66.74→66.57은 예비자료의 잠정 참고로만 보존.
- 가상 재포착 vel+0.20의95%구간0.07~0.32, fused+0.06의−0.11~0.21을 구분한다.
- RepVGG 시간 비교:5.02/1.28≈3.92배; 검수264와OTP2판 정확도를 서로 대입하지 않는다.
- 출처 스냅샷 SHA256은 sources/latest-20261121/manifest.json에 보존. 비공개 개인실험 파일은 팀원이 기록한 주장으로 인용하며 원본을 새로 확인한 것으로 표시하지 않는다.

## 이전 B안 수치 원표

아래는 B안 원문 보존이며 장 번호는 B 기준이다. C안 장별 매핑과 최신 해석을 우선한다.

# 출처·수치 추적표

확인 스냅샷: presentation `4c38a4e400c3d805b410707d49dc4d3ffa772459`. 원자료는 `../A/sources/presentation/`에 보존했다. 통합본에서 원본 슬라이드를 수정하거나 팀원의 파일을 덮어쓰지 않았다.

## 출처 식별자

- **S1** [공통 목차·20분·제작 규격](https://app.notion.com/p/4169de3f14a280ee9e05cec320dfb929)
- **S2** [윤오름 · 시스템·제어·GUI 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/notes.md)
- **S3** [윤오름 · GUI·제어 구현 비교](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤오름/model-bank-GUI-제어-비교분석.md)
- **S4** [김재남 · Runtime·전후처리·통신 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/김재남/speaker-notes.md)
- **S5** [윤관 · 학습·평가·제어 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/notes.md)
- **S6** [윤관 · 결과 그림·측정 조건](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/index.html)
- **S7** [윤관 · 실험 원문 출처](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/윤관/sources.md)
- **S8** [정하건 · 추적 대본](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/긴버전/발표노트.md)
- **S9** [정하건 · 추적 근거 비교표](https://github.com/lwir-deepx-tracking-system/presentation/blob/4c38a4e400c3d805b410707d49dc4d3ffa772459/정하건/근거_비교표.md)
- **S10** [model-bank · 11-17 공개 발표 근거](https://github.com/lwir-deepx-tracking-system/model-bank/blob/6cf676df1c1be72bd6e8220a6240a0d3f1c7127e/tracking_server/research/LWIR_PRESENTATION_KO.md)
- **S11** [11-18 검출 학습·평가 원본 대조](https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/윤관/sources.md)
- **S12** [실제 NPU 메모리 재생 부하 시험](https://github.com/lwir-deepx-tracking-system/presentation/blob/7ade544b92ebda3a715ffd09bcf2f044136ff52f/김재남/measurements/orangepi-20261116-retry/report.md)
- **S16** [11-10 PID 후보 비교·PD 선택 근거](sources/pd-selection/PID_TUNING_RECORD_20261110.md)
- **S15** [윤관 11-19 · 상체 E10·표시·실카메라 NPU](https://github.com/lwir-deepx-tracking-system/presentation/blob/afa734f399a2c2e53171abd3131fffddc64351b3/윤관/근거_최신_20261119.md)
- **S14** [정하건 v3 · 3종 추적·GUI 교체·성능](https://github.com/lwir-deepx-tracking-system/presentation/blob/7249d7b/정하건/정하건_v3/근거_비교표.md)
- **S13** [팀원 담당 업무 · 사용자 제공](team-roles.md)

## 본문 주요 숫자

| 장 | 지표 | 값 | 단위 | 출처 | 조건 | 한계 |
|---|---|---|---|---|---|---|
| 이전 장치 비교 · 예비 10 | 사람 AP50–95 | YOLO26s 42.32 / m 45.79 | % | S6 | 11-06 M1 INT8, FLIR 8편 3,749프레임, 각1회 | 크기만의 인과효과 아님 |
| 이전 장치 비교 · 예비 10 | NPU 호출 p50 | 19.02 / 27.12 | ms | S6 | 같은 장치 비교의 호출시간 | 종단 지연 아님 |
| 예비 12 | 60 epoch 사람 AP FT/KD | 44.8575 / 44.2334 | % | S11 | FLIR 4196장 · seed202 · checkpoint 별도 평가 | m급·장치 AP와 구분 |
| 예비 11 | m급 1/30 epoch 사람 AP | 43.7461 / 50.6209 | % | S11 | FLIR 검증1144장 · 원본 epoch CSV | 최적 epoch·INT8 성능으로 해석하지 않음 |
| 예비 13 | 호출 p50/p95 | 24.43 / 31.22 | ms | S6 | 11-04 임의 입력300회 | 실카메라 별도 |
| 예비 13 | 실카메라 처리량 | 23.9–24.5 | fps | S6 | 11-09 모델당 약20초 | 현재 운용값 아님 |
| 예비 03 · 과거 보드 비교 | 보드 IDSW | 2964 / 775 | 회 | S9 | 자체18편 동일검출 Orange Pi | 개발 비교 |
| 예비 03 · 과거 보드 비교 | 보드 IDF1 | 49.56 / 64.10 | % | S9 | 같은 보드 비교 | PC 531과 분리 |
| 예비 15 | PC IDSW | 656 / 531 | 회 | S9 | IoU0.2 기준 옵션 대조 | 같은 검출 PC 재실행 |
| 예비 15 | PC Frag | 2164 / 1832 | 회 | S9 | 같은 옵션 대조 | 헛출력 절충 |
| 예비 15 | PC 정밀도 | 84.1 / 83.0 | % | S9 | 같은 옵션 대조 | −1.1%p |
| 이전 C++ 부하 시험 · 예비 16 | 60fps 재생 완료 FPS / 누락 | 50.22→60.00 / 16.17→0 | fps / % | S12 | inflight1/4 · 15초×3 | 객체0개 · GUI/짐벌 제외 |
| 이전 C++ 부하 시험 · 예비 16 | 60fps 재생 p95 | 74.42 / 22.75 | ms | S12 | 입력 준비→추적 완료 | 실카메라·브라우저 종단 지연 아님 |
| 본문 23 / 예비 17 | 상하 정지뒤 반전 | 4 / 1 | 회 | S5,S6,S7 | 실물+가상표적 조건별1회 | 과거 속도상한10·aim0.3 |
| 본문 23 / 예비 17 | 별도 가로 뒤처짐 | 14.3 / 18.6 | px | S5,S6,S7 | 별도 가로시험 | 악화 결과도 함께 보고 |
| 예비 18 | 녹화 입력→결과 p95 | 240.53 / 52.80 | ms | S10 | 11-13 212장×4 ABBA 동일서버 시청1 | 브라우저·실카메라 아님 |
| 예비 18 | 녹화 출력간격 p95 | 51.90 / 50.79 | ms | S10 | 같은 ABBA | 33.3ms 목표 미달 |
| 본문 15–16 / 예비 19 | 동일 PC OC-SORT / BoT-SORT HOTA | 59.1 / 60.7 | 점 | S14 | 동일 검출·PC bench_mot17·18편 | 종합 품질 |
| 본문 15–16 / 예비 19 | 동일 PC IDF1 | 66.7 / 67.5 | % | S14 | 같은 PC 비교 | +0.8%p |
| 본문 15–16 / 예비 19 | 동일 PC IDSW | 531 / 566 | 회 | S14 | 같은 PC 비교 | OC-SORT가 더 적음 |
| 본문 10 | 상체 박스 AP / 재현율 | 36.04→46.28 / 71.70→69.09 | % | S15 | OTP2 934장 | 공개 검증셋 |
| 본문 11 | E10 / 추가대조 / 시간손실 AP | 46.28 / 40.23 / 40.21 | % | S15 | 같은 추가3ep 조건 | 운영 교체 보류 |
| 본문 19·31 | 프레임 교대 / 동시 타일 p95 | 40.47 / 25.71 | ms | S15 | 실카메라 각65초·수신→추적완료 | 큐 버림0/1·순서오류0/0 |

## 계산한 파생값

- 본문19 Runtime 지연 p95 감소율: (74.42−22.75)/74.42×100 = 69.43%, 그래프 69.4%. 다른 ABBA 비교의 78.0%와 별개.

- AP 차이: 45.79 − 42.32 = 3.47%p.
- 호출 차이: 27.12 − 19.02 = 8.10ms.
- 보드 IDSW 감소율: (2964−775)/2964×100 = 73.85%, 과거 보드 비교 73.9%.
- 보드 IDF1 차이: 64.10−49.56 = 14.54%p.
- PC IDSW 감소율: (656−531)/656×100 = 19.05%, 본문 19.1%.
- PC Frag 감소율: (2164−1832)/2164×100 = 15.34%, 본문 15.3%.
- 녹화 결과 지연 p95 감소율: (240.53−52.80)/240.53×100 = 78.05%, 본문 78.0%.

위 감소율은 기재된 집계값의 산술 계산이며 독립 반복 실험의 신뢰구간이 아니다. 막대그래프는 모두 0부터 시작하는 선형 스케일을 사용한다.

## 개정 근거 보관

2026-11-18 개정 자료는 ../A/sources/revision-20261118/에 보존했다. manifest.json의 커밋과 SHA256으로 원본을 추적한다. 새 부하 수치를 Python 웹 서버의 내부 성능으로 옮기지 않는다.

## 에셋과 인용 범위

- 인물 사진·로고·폰트·열화상·학습곡선·GUI는 발표 저장소의 제공 파일을 복사했다. 제공 원본의 성격을 캡션에 표시했다.
- 운영 재생 화면을 실카메라 옥상 시연으로, 합성 미리보기 수치를 성과로 사용하지 않았다.
- 외부 영상이나 실제 라벨 데이터를 새로 수집하거나 공개하지 않았다.
- 이번 작업은 기존 결과를 취합한 것이며 장치 시험과 학습·평가를 재실행하지 않았다.
- Notion 출처가 달린 원문 실험의 모든 원시 로그를 재검증하지는 않았다.
- 수치·실험 조건은 위 담당자의 문서와 공개 인계에 근거한다.


## 발표용 모델 이름

- 공개 자세 모델 = F. 이전 혼합 라벨 모델 = 1,056장 E10. 현장 650장 모델 = 650장 E10(공개 자세 모델에서 10 epoch 추가 학습).
- 자체 영상 추가 학습 모델 = own9e 시드 1. 이 모델과 비교한 기존 장치 모델 = 모델 9. 두 모델의 장치 재생 비교는 S26·S27.
- 실카메라 지연 시험용 추가 학습 모델 = E10+3. 65초씩 진행한 해당 시험은 S15·S17.