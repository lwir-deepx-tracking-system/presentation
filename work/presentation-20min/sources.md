# 출처·수치 추적표

확인 스냅샷: presentation `4c38a4e400c3d805b410707d49dc4d3ffa772459`. 원자료는 `sources/presentation/`에 보존했다. 통합본에서 원본 슬라이드를 수정하거나 팀원의 파일을 덮어쓰지 않았다.

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

## 본문 주요 숫자

| 장 | 지표 | 값 | 단위 | 출처 | 조건 | 한계 |
|---|---|---|---|---|---|---|
| 05 | 사람 AP50–95 | YOLO26s 42.32 / m 45.79 | % | S6 | 11-06 M1 INT8, FLIR 8편 3,749프레임, 각1회 | 크기만의 인과효과 아님 |
| 05 | NPU 호출 p50 | 19.02 / 27.12 | ms | S6 | 같은 장치 비교의 호출시간 | 종단 지연 아님 |
| 07 | 야외 검출률 F/NF | 97.45 / 95.55 | % | S5,S6 | 과거 자체 학습 후보별1회 | 옥상 후보의 최종 수치 아님 |
| 07 | 실내 FP F/NF | 0.068 / 0.152 | 건/프레임 | S5,S6 | 해당 실내 평가 | 거리별 다른 지표와 혼합하지 않음 |
| 08 | 호출 p50/p95 | 24.43 / 31.22 | ms | S6 | 11-04 임의 입력300회 | 실카메라 별도 |
| 08 | 실카메라 처리량 | 23.9–24.5 | fps | S6 | 11-09 모델당 약20초 | 현재 운용값 아님 |
| 10 | 보드 IDSW | 2964 / 775 | 회 | S9 | 자체18편 동일검출 Orange Pi | 개발 비교 |
| 10 | 보드 IDF1 | 49.56 / 64.10 | % | S9 | 같은 보드 비교 | PC 531과 분리 |
| 11 | PC IDSW | 656 / 531 | 회 | S9 | IoU0.2 기준 옵션 대조 | 같은 검출 PC 재실행 |
| 11 | PC Frag | 2164 / 1832 | 회 | S9 | 같은 옵션 대조 | 헛출력 절충 |
| 11 | PC 정밀도 | 84.1 / 83.0 | % | S9 | 같은 옵션 대조 | −1.1%p |
| 12 | 놓친 위치 오차 GRU/Kalman | 0.118 / 0.110 | 사람 키 비율 | S10 | 자체라벨14편 | 오류분석에 TEST 사용 |
| 12 | 녹화 IDF1 GRU/Kalman | 75.36 / 71.81 | % | S10 | seq018 1069프레임 각2회 | 한 영상 결과 |
| 13 | 상하 정지뒤 반전 | 4 / 1 | 회 | S5,S6,S7 | 실물+가상표적 조건별1회 | 과거 속도상한10·aim0.3 |
| 13 | 별도 가로 뒤처짐 | 14.3 / 18.6 | px | S5,S6,S7 | 별도 가로시험 | 악화 결과도 함께 보고 |
| 15 | 녹화 입력→결과 p95 | 240.53 / 52.80 | ms | S10 | 11-13 212장×4 ABBA 동일서버 시청1 | 브라우저·실카메라 아님 |
| 15 | 녹화 출력간격 p95 | 51.90 / 50.79 | ms | S10 | 같은 ABBA | 33.3ms 목표 미달 |

## 계산한 파생값

- AP 차이: 45.79 − 42.32 = 3.47%p.
- 호출 차이: 27.12 − 19.02 = 8.10ms.
- 보드 IDSW 감소율: (2964−775)/2964×100 = 73.85%, 본문 73.9%.
- 보드 IDF1 차이: 64.10−49.56 = 14.54%p.
- PC IDSW 감소율: (656−531)/656×100 = 19.05%, 본문 19.1%.
- PC Frag 감소율: (2164−1832)/2164×100 = 15.34%, 본문 15.3%.
- 녹화 결과 지연 p95 감소율: (240.53−52.80)/240.53×100 = 78.05%, 본문 78.0%.

위 감소율은 기재된 집계값의 산술 계산이며 독립 반복 실험의 신뢰구간이 아니다. 막대그래프는 모두 0부터 시작하는 선형 스케일을 사용한다.

## 에셋과 인용 범위

- 인물 사진·로고·폰트·열화상·학습곡선·GUI는 발표 저장소의 제공 파일을 복사했다. 제공 원본의 성격을 캡션에 표시했다.
- 운영 재생 화면을 실카메라 옥상 시연으로, 합성 미리보기 수치를 성과로 사용하지 않았다.
- 외부 영상이나 실제 라벨 데이터를 새로 수집하거나 공개하지 않았다.
- 이번 작업은 기존 결과를 취합한 것이며 장치 시험과 학습·평가를 재실행하지 않았다.
- Notion 출처가 달린 원문 실험의 모든 원시 로그를 재검증하지는 않았다.
- 수치·실험 조건은 위 담당자의 문서와 공개 인계에 근거한다.
