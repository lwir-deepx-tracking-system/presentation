# work.pdf 기준 대본 · 2026-11-25

**[speaker-notes.md](speaker-notes.md)가 수정 원본**이다. 말할 문장은 이 파일 한 곳에서 고친다. 부록을 제외한 본문35쪽에15분을 목표로 배정했다. 실제 낭독 시간은 아직 재지 않았다. E.pptx와장별내용을대조해 [노트입력사본](../../E/E_발표자노트_피드백반영.pptx)을만들었으며원본은보존했다.

- [MD 원문](speaker-notes.md) / [화면과 함께 보기](speaker-notes.html)
- [큐시트](cue-sheet.md) / [시간 배정](timing.md)
- [슬라이드 확인 메모](review.md)
- [원본 PDF](sources/work.pdf) / [동결 출처](sources/manifest.json)

## 다음 작업

1. MD로 소리 내어 연습하며 말투·길이를 조정한다.
2. 아래 명령으로 읽기용 화면·큐시트·노트 매핑을 갱신한다.
3. 최신 PPTX를 받으면 실제 슬라이드의 제목·본문과 매핑을 대조한다.
4. MD의 ‘말할 내용’과 필요한 전환 문장만 발표자 노트에 넣은 사본을 만든다. 슬라이드와 기존 공동편집 원본은 덮어쓰지 않는다.

```powershell
python work/D/work-pdf-20261125/build_notes.py
```

notes-map.json은 PPTX노트용 텍스트와 대응 근거다. PDF쪽 번호만 보고 이전39장PPTX에 그대로 넣지 않는다. 검토 메모·미확인 수치·출처 목록은 발표자 노트 문장에 자동으로 끼워 넣지 않는다. 부록36~50쪽은 이번 본문 노트 대상에서 제외한다.

이전ㅇ.pdf 기준32쪽 대본은 ../practice-15min/에 보존한다. C·final과팀원 원본은 수정하지 않는다.
