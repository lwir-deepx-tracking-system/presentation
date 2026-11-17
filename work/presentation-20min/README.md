# LWIR 표적 추적 시스템 · 20분 발표 취합 초안

본문 **18장**, 발표 **17분 + 데모 3분 = 20분**의 목표 시간표입니다. 발표자가 실제로 읽은 시간은 재지 않았습니다. 원고와 그림 지시·전환을 포함해 리허설로 시간을 조정해야 합니다.

최종 옥상 후보 두 모델은 정확한 이름을 임의로 정하지 않았습니다. 최종 모델·운용 결과·영상만 교체할 수 있도록 표시했습니다. 실제 데모 파일은 포함되어 있지 않습니다.

## 바로 볼 파일

| 파일 | 용도 |
|---|---|
| [index.html](index.html) | 본 발표 18장. 로컬 폰트·이미지 사용 |
| [presentation.pdf](presentation.pdf) | 본문 PDF, 1920×1080 기준 한 장에 한 페이지 |
| [speaker-notes.md](speaker-notes.md) | 통합 대본·장별 시간·조건·확정할 항목 |
| [speaker-notes.html](speaker-notes.html) | 대본을 브라우저에서 읽기 |
| [appendix.html](appendix.html) / [appendix.pdf](appendix.pdf) | 질문 대비 6장, 본문 20분에 미포함 |
| [qa.md](qa.md) | 예상 질문 25개와 근거에 맞춘 답변 |
| [sources.md](sources.md) | 출처·원문 링크·숫자·파생 계산·측정 조건 |
| [integration.md](integration.md) | 취합 결정·옥상 시험 뒤 교체할 곳 |
| [deck.json](deck.json) | 본문 구조·시간·대본을 담은 데이터 |
| [validation.json](validation.json) | 실제 Chromium 출력·글자 경계·이미지·폰트·PDF 확인 |
| [previews/slide-overview.png](previews/slide-overview.png) | 본문 전체 모아보기 |

## 발표 조작

`index.html`을 브라우저에서 엽니다. 좌우 방향키·Page Up/Down·Space로 이동합니다. Home/End로 첫 장과 마지막 장으로 갑니다. `F`는 전체 화면, `G`는 모아보기입니다. 아래 도구에서 발표 타이머와 대본을 열 수 있습니다. 타이머는 경과시간이며 자동으로 슬라이드를 넘기지 않습니다.

영상 17번은 현재 재생 화면 포스터와 ‘옥상 시험 후 삽입’ 안내입니다. `assets/rooftop-demo.mp4`를 넣고 `build.py`의 안내·캡션을 확정 내용으로 바꿔 재생성합니다. 파일을 넣기 전의 빈 영상 경로를 실제 데모 재생 검증으로 해석하지 않습니다.

## 내용 구성

1–4: 목표·팀·실행 구조·평가 기준

5–8: 검출의 정확도/시간 절충·학습·미채택 후보 결과·INT8 배포

9–12: 추적 원리·동일 보드 비교·동일 PC 옵션 비교·외형과 위치 기억

13–16: 제어와 실물 시험·GUI/통신·시스템 지연 비교·검증 범위

17–18: 데모 3분·핵심 성과

원고의 모든 내용이 한 개의 최종 시스템에서 동시에 측정됐다는 뜻은 아닙니다. 각 실험의 조건을 유지했습니다. 특히 보드 IDSW 2964→775와 PC 옵션 비교656→531, NPU 호출시간과 녹화 지연은 구분했습니다.

## 기존 자료 사용과 변경 범위

- presentation `4c38a4e400c3d805b410707d49dc4d3ffa772459`의 팀원 HTML·대본·근거·이미지·폰트를 읽고 취합했습니다.
- 원문 텍스트·HTML·에셋 사본은 `sources/presentation/`에 보존했습니다. 원본 PDF는 다운로드 사본에 포함하지 않았습니다.
- model-bank `6cf676df1c1be72bd6e8220a6240a0d3f1c7127e`의 공개 발표 인계는 `sources/LWIR_PRESENTATION_KO.md`로 보존했습니다.
- 사용자님의 시스템·GUI·제어 자료와 김재남님의 Runtime 설명을 구조 근거로, 윤관님과 정하건님의 실제 비교 결과를 성능 근거로 사용했습니다.
- 각 담당자의 숫자를 다른 조건으로 바꾸거나 가짜 수치를 만들지 않았습니다. 감소율은 원문 집계값에서 산술 계산했습니다.
- 팀원 원본 파일, 실제 Runtime·서버 코드, 장치 설정은 수정하지 않았습니다. 커밋·push·운영 반영도 하지 않았습니다.

## 다시 생성

내용·대본·그림 배치는 `build.py`, 모양은 `slides.css`, 화면 조작은 `slides.js`에서 수정합니다.

```bash
python3 build.py
```

PDF·미리보기 생성은 Playwright와 PyMuPDF가 필요합니다.

```bash
python3 -m pip install playwright pymupdf
python3 -m playwright install chromium
python3 render.py
```

이미 설치된 Chromium을 쓰려면 `LWIR_SLIDE_BROWSER` 환경변수에 실행 파일을 지정합니다. 폰트·이미지는 모두 로컬 파일이며 발표 HTML 실행에는 Python이나 인터넷이 필요하지 않습니다. 출처 링크를 열 때만 인터넷이 필요합니다.

## 이번 확인의 범위

HTML의 실제 Chromium 렌더링, 본문·예비 PDF 출력, 이미지·폰트 로딩, JavaScript 오류, 본문과 출처 영역의 충돌, 키보드 이동을 검사했습니다. 상세 결과는 `validation.json`에 남깁니다.

실제 낭독 20분 리허설·최종 옥상 데모·장치 재시험·원시 결과 재채점은 하지 않았습니다. `sources.md`는 결과의 출처를 추적하는 문서이며 독립적인 재실험 결과가 아닙니다.
