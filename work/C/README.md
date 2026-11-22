# C안 · 최신 통합 발표

2026-11-22 작성. 자료 기준 presentation `4836142`(11/21 23:13 KST). B안 `9819922` 이후의 검출·외형·ID·서버·짐벌 근거를 반영했습니다. A·B와 팀원 원본은 보존합니다.

본문 **39장**, 예비 **37장**. 설명 17분+실제 데모 3분의 **목표**이며 낭독 리허설은 하지 않았습니다.

시작은 **표지 → 목차 → 팀 소개 → 프로젝트 소개** 순서입니다. 목차는 소개·검출·추적·NPU 처리·짐벌 운용·통합 시연과 주요 성과의 6개 항목입니다. 마무리는 현재 성과 중심이며, 거리·현장 ID 검증 계획은 예비자료에 보존했습니다.

- [발표 PDF](presentation.pdf) / [발표 HTML](index.html)
- [전체 미리보기](previews/slide-overview.png)
- [발표 대본](speaker-notes.html) / [Markdown 대본](speaker-notes.md) / [큐시트](cue-sheet.md)
- [예비 PDF](appendix.pdf) / [예비 HTML](appendix.html) / [예비 설명](appendix-notes.md)
- [출처·수치](sources.md) / [질의응답](qa.md) / [통합 인계·장 매핑](integration.md)
- [검증 결과](validation.json) / [원자료 해시](sources/latest-20261121/manifest.json)

새 본문은 외형 모델 비교, 번호 유지, 분할 모델 변환, 장시간·혼잡 조건, 장치 상태 이력, 짐벌 실측·가상 시험·놓침 대응을 설명합니다. 검출 후속 학습·지연 결론·조준 보정도 갱신했습니다. 예비자료에는 원본 CSV 학습 곡선 6개를 보충했습니다. 최신 자료의 조건 충돌은 대본·출처·예비자료에 기록했습니다.

공통 `reference/picture/`의 하드웨어 사진과 팀원 사진을 표지·팀 소개에 반영했습니다. 사진은 C/assets에도 복사해 보존하고, 재생성 시 공통 폴더의 사진을 동기화합니다. [사진 해시](picture-manifest.json)를 함께 기록합니다.

실제 앱 캡처·통합 영상·거리/현장 ID 결과·최종 실행 설정은 미확보입니다. 시연 영상은 **37장**, `assets/rooftop-demo.mp4`입니다. 기존 25.71 ms나 PC ID 비교를 현재 장치의 통합 성능으로 제시하지 않습니다.

```powershell
python work/C/build.py
python work/C/render.py
```

방향키·Space 이동, Home/End 처음·끝, G 모아보기, F 전체화면. 편집 기준은 [DESIGN.md](../DESIGN.md), 현재 인계는 [integration.md](integration.md)입니다. 최신화는 `build.py`를 수정합니다. `seed.json`과 `sources/`는 동결 근거입니다.
