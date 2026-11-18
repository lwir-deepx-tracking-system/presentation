# LWIR 프로젝트 발표자료

표지·팀 소개·운용 시나리오와 담당 기술 내용을 하나의 발표자료로 통합했습니다. 전체 목차의 1·2·3·4·5·10·11·12·13번, 총 9장입니다. 페이지 번호는 전체 발표 목차 기준을 유지합니다.

## 파일

- [index.html](index.html): 통합 발표자료. 브라우저에서 열어 미리보고 방향키 좌우 또는 Page Up/Down으로 이동합니다.
- [presentation.pdf](presentation.pdf): 통합 PDF 9페이지, 한 페이지에 슬라이드 한 장.
- [notes.md](notes.md): 슬라이드별 발표 노트·근거·확인할 자료.
- `slides.css`: 폰트·공통 디자인·슬라이드 레이아웃·화면 축소·인쇄 스타일.
- `previews/slide-01.png` 등: 9장 개별 미리보기. `previews/validation.json`은 출력 검증 결과입니다.
- `render-presentation.py`: 설치된 Chrome과 Python `playwright`, `pypdf`로 PDF·미리보기를 재생성하고 출력 상태를 확인합니다.
- [model-bank-GUI-제어-비교분석.md](model-bank-GUI-제어-비교분석.md): 기존 Qt 앱과 모델뱅크 웹 GUI·제어의 비교 근거.

저장소 루트에서 다시 출력:

```powershell
python 윤오름/render-presentation.py
```

## 에셋

- `assets/team/`: `reference/human/`에서 복사한 팀원 5명의 누끼 사진. 홍정호도 실제 제공 사진입니다.
- `assets/model-bank-web-gui.png`: model-bank `5ea5b64`의 `tracking_server/images/interface_8090.png`. 12번의 웹 GUI 미리보기입니다. 합성 영상·예시 수치·장치 연결 없음이라는 원본 표시를 유지했습니다.
- `assets/gui-mock-h264.png`: 이전 Qt 앱 모의 시험 캡처를 보관한 참고 파일. 현재 슬라이드에서는 사용하지 않습니다.
- `assets/Signature_PNG/`: 제공된 공식 로고. 현재는 Blue 축약형을 사용합니다.
- `assets/Pretendard-*.woff2`, `FONT-LICENSE.txt`: 로컬 폰트와 라이선스.
- `assets/0000_프로젝트계획서(천준호).pdf`: 프로젝트명·계획 참고 원본.

## 내용과 확인 범위

5번은 브라우저–Python 서버–C++ 브리지–짐벌 구성, 10번은 공개 스크립트의 PD·설정 조준점, 11번은 웹 JPEG·선택적 Picture First, 12번은 웹 GUI, 13번은 시스템별 시험 근거 구분을 설명합니다. 모델뱅크 실제 서버의 v25/v27·환경변수·활성 옵션은 미조회 상태이며 공개 기본값과 구분합니다.

성능 원본 로그가 반영되지 않은 항목은 측정·결과 반영 예정으로 표시했습니다. 11번은 다른 담당자의 파이프라인 자료와 대조할 공동 설명 초안입니다. 12번 미리보기의 예시 숫자는 성능 결과가 아닙니다.

도식은 운용 개념이며 실제 장치 사진이나 실측 성과를 대신하지 않습니다. 최종본에서는 실제 운용 GUI 캡처와 동일 설정의 로그를 반영해야 합니다.

## 제작·검증 기준

1920×1080px, 흰색 배경, LIG 블루 `#002F6D`, Pretendard 폰트를 사용합니다. 공식 로고 너비는 180px이며 원본 비율과 색상을 유지합니다. 화면에서만 축소하고 인쇄 크기는 유지합니다.

출력 검증: 폰트·로고·인물·GUI 이미지 로딩, JavaScript 오류 없음, 1280px 화면 축소 표시, 본문과 출처·푸터 경계, 슬라이드 순서, PDF 9페이지·1440×810pt(1920×1080px 상당)를 확인합니다.

수동 인쇄 시 머리글/바닥글 끄기, 배경 그래픽 켜기, 여백 없음으로 설정합니다.

구성·공통 규격: [Notion 발표자료 준비](https://app.notion.com/p/4169de3f14a280ee9e05cec320dfb929).
