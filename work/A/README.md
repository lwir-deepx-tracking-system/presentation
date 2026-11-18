# LWIR 표적 추적 시스템 · 20분 발표 개정본

2026-11-18 개정. 기존 작업본을 갱신했으며 팀원 원본 자료는 수정하지 않았습니다.

**발표의 중심:** 열영상에서 사람을 찾고 같은 표적을 유지하며 사용자가 선택한 대상을 짐벌로 추종하는 시스템을 구현했다.

## 볼 파일

- [index.html](index.html) / [presentation.pdf](presentation.pdf): 본문 14장.
- [speaker-notes.md](speaker-notes.md) / [읽기용 대본](speaker-notes.html): 장별 메시지·대본·전환·진행 메모·시간표.
- [appendix.html](appendix.html) / [appendix.pdf](appendix.pdf): 질문 대비 18장. 본문 시간에 미포함.
- [전체 미리보기](previews/slide-overview.png), [예비 미리보기](previews/appendix-overview.png).
- [integration.md](integration.md): 이번 취합 결정과 최종 시험 뒤 교체할 곳.
- [sources.md](sources.md): 숫자·측정 조건·출처 추적표.
- [qa.md](qa.md): 예상 질문과 답변.

## 시간과 상태

본문 발표 17분 + 데모 슬롯 3분 = **목표 20분**입니다. 실제 낭독·영상 리허설은 하지 않았습니다. 데모 mp4가 없으므로 12번은 실제 영상 삽입 안내 상태입니다.

최종 후보·실제 브리지·제어·영상 모드·현장 결과는 확인 전입니다. 과거 모델 비교·가상 표적·재생 입력 결과로 빈칸을 채우지 않았습니다.

## 발표 흐름

운용 장면 → 팀 소개 → 전체 구조 → 사람 찾기 → ID 유지 → 제때 반응하기 → 2축 제어 → GUI → 데모 → 현장 검증 → 마무리.

- 본문은 큰 그림·개념도·핵심 비교 중심으로 재편집했습니다.
- 학습곡선, FT/KD, 배포, 추적 원리·옵션, 제어 상세, 지연 상세는 예비자료로 옮겼습니다.
- 대본은 새 그림과 순서에 맞춰 수정했습니다. 실제 녹화 화면·합성 미리보기·개념도를 각각 표시합니다.
- 실제 현장 영상과 운용 캡처는 수령 후 교체해야 합니다.

## 근거 보존

기존 자료는 sources/presentation/과 sources/LWIR_PRESENTATION_KO.md에 보존합니다. 최신 개정 자료는 sources/revision-20261118/에 선별 복사했고 manifest.json에 기준 커밋과 SHA256을 기록했습니다. 증빙 원본을 갱신할 때 기존 결과의 조건을 유지합니다.

## 재생성과 조작

```powershell
python work/A/build.py
python work/A/render.py
```

Python playwright·pymupdf가 필요합니다. 설치된 Windows Chrome을 자동으로 찾으며 다른 브라우저는 LWIR_SLIDE_BROWSER 환경변수로 지정할 수 있습니다. 발표 HTML 실행에는 Python·인터넷이 필요 없습니다.

방향키·Page Up/Down·Space로 이동, Home/End는 처음/끝, F는 전체 화면, G는 모아보기입니다. 타이머는 실제 경과시간을 표시하며 자동으로 넘기지 않습니다.

내용·대본·시간은 build.py에서 함께 수정합니다. deck.json·HTML·대본을 따로 편집하면 재생성 때 덮어써집니다. 스타일은 slides.css, 조작은 slides.js입니다.

## 검증 범위

render.py는 본문 18·예비 8페이지, 1920×1080 비율, 이미지·폰트·JavaScript·글자 경계·키 이동과 목표 1200초를 확인합니다. 결과는 validation.json에 남깁니다. 실제 말하기 시간, 데모 재생, 하드웨어·학습·평가 재시험을 수행했다는 뜻은 아닙니다.
