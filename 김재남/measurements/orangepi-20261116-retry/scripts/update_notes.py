"""Keep presentation notes consistent with the controlled-load replacement of P1/P2."""
from pathlib import Path
import json,re,html
root=Path('/home/user/workspace/mypresentaion/v4');d=root/'measurements/orangepi-20261116-retry'
s=json.loads((d/'replay-summary.json').read_text());r={(x['tag'],x['case']):x for x in s['summary']}
a=r[('replay120','serial640')];b=r[('replay120','async6')]
intro='''# 실측 성능 비교 P1–P4

추가 성능 슬라이드 4장의 발표 원고다. 기존 담당 슬라이드와 별도로 취합·시간을 조정한다. 측정일은 2026년 11월 16일, 보드 main 0fe016f다. P1·P2는 제어 입력 재시험, P3·P4는 원래 실카메라 시험 결과다.

## P1 · 일정한 입력 부하로 처리 능력 측정 · 약 40초

실카메라만 연결한 첫 시험에서는 입력이 30fps에 못 미쳐 비동기 처리 능력을 비교하기 어려웠습니다. 그래서 실제 카메라에서 저장한 16-bit 프레임을 메모리에 올리고 30, 60, 120fps로 공급했습니다. 입력 경로만 바꾸고 NPU 추론과 추적은 그대로 실행했습니다. 각 조건을 5초 준비한 뒤 15초씩 세 번 측정했고, 공급 FPS와 실제 시각까지 기록했습니다. 처리량뿐 아니라 누락률과 평균, p95, 관측 max를 함께 비교했습니다.

발표자 확인

- 제어 입력 12조건 × 3회 = 36회다. 앞선 SDK·입력 크기 실카메라 30회와 구분한다.
- 저장 파일 20장은 SHA256이 같아 단일 고정 장면 반복에 해당한다. 검출 객체가 없는 장면이며 다양한 장면·NMS·추적 부하는 대표하지 않는다.
- 매 실행 실제 입력 FPS가 요청값의 2% 이내인지 검증했다. 예정/실제 공급 시각은 replay-source.csv에 있다.
- 지연은 입력 준비 완료부터 추적 완료까지다. 센서·카메라 SDK·네트워크·PC 표시 지연은 제외한다.
- 지연과 FPS는 15초 구간 전체를 사용한다. 누락률만 SIGINT 직전 취소 영향을 피하려고 마지막 0.5초를 제외한 입력 프레임 집합으로 계산한다.
- 평균·p95는 반복별 값의 평균, max는 해당 조건 세 번 전체 관측 최댓값이다. 장시간 지연 상한의 보장은 아니다.

## P2 · 비동기 요청으로 입력 부하에 대응 · 약 50초

같은 모델에서 매번 완료를 기다리는 조건과 비동기 제출을 비교하고, inflight를 1, 4, 6으로 바꿨습니다. 30fps 입력에서는 네 조건 모두 처리할 수 있었지만, 부하를 높이자 차이가 나타났습니다. 120fps 입력에서 완료 대기는 약 {serial:.1f}fps, inflight 6은 약 {async6:.1f}fps를 완료했습니다. inflight 4와 6은 높은 입력 부하를 따라가도록 요청을 중첩할 수 있었습니다. 이 선택은 처리량만 보고 결정하지 않고 누락률과 지연 분포까지 함께 확인했습니다.

발표자 확인

- 완료 대기는 같은 submit_async 경로에서 매 제출 후 wait_idle을 호출한다. 별도 SDK Run API와의 비교가 아니다.
- max_inflight는 애플리케이션의 미완료 요청 상한이며 코어 수나 buffer_count와 구분한다. 모두 NPU_ALL을 사용했다.
- 120fps는 시험한 입력 속도다. 최대 처리 가능 FPS를 확정했다고 표현하지 않는다.
- 과부하에서 버려진 프레임에는 완료 지연이 없다. 지연 수치와 누락률을 반드시 함께 평가한다.
- 30fps 재생 시험 통과는 실카메라·GUI·짐벌을 모두 켠 통합 운용 30fps 달성의 증거가 아니다.

'''.format(serial=a['tracking_fps'],async6=b['tracking_fps'])
p=root/'speaker-notes.md';text=p.read_text();prefix=text.split('# 실측 성능 비교 P1–P4')[0];old=text[text.index('## P3 · SDK 가속과 최악 지연'):]
p.write_text(prefix+intro+old)
parts=[]
for block in p.read_text().strip().split('\n\n'):
 if block.startswith('# '):parts.append('<h1>'+html.escape(block[2:])+'</h1>')
 elif block.startswith('## '):parts.append('<h2>'+html.escape(block[3:])+'</h2>')
 elif block.startswith('- '):parts.append('<ul>'+''.join('<li>'+html.escape(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
 else:parts.append('<p>'+html.escape(block).replace('\n','<br>')+'</p>')
(root/'speaker-notes.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>v4 발표 노트</title><style>@font-face{font-family:Pretendard;src:url(assets/Pretendard-Regular.woff2)}body{font-family:Pretendard,"Noto Sans KR",sans-serif;max-width:1000px;margin:40px auto;padding:0 28px;color:#202B3A;line-height:1.8}h1,h2{color:#002F6D}h1{border-bottom:2px solid #002F6D;padding-bottom:12px;margin-top:52px}li{margin-bottom:8px}</style>'+''.join(parts)+'</html>')
p=root/'README.md';text=p.read_text().split('\n# 제어 입력 부하 재시험')[0]
text+='\n# 제어 입력 부하 재시험\n\n카메라 입력 부하가 부족했던 P1·P2를 실제 저장 프레임의 30·60·120fps 메모리 재생 36회 결과로 교체했다. 입력 경로만 실험용으로 바꾸고 NPU 추론·추적은 실제로 수행했다. P3·P4는 기존 실카메라 결과를 유지한다. 재시험 조건·누락률·p95·max와 한계는 measurements/orangepi-20261116-retry/report.md에 있다. 실카메라 수신 30fps 확보 문제는 미해결이며, 제어 입력 결과와 구분한다.\n'
p.write_text(text)
p=root/'sources.md';text=p.read_text().split('\n# 제어 입력 재시험')[0];text+='\n# 제어 입력 재시험\n\nP1·P2의 수치는 measurements/orangepi-20261116-retry/replay-summary.csv와 replay-summary.json에서 가져왔다. 36회 실행의 원본 CSV·YAML·로그·maps·hash·소스 공급 예정/실제 시각을 보존했다. 검증 결과는 replay-validation.json이다. 입력 교체·계측 소스와 재현 스크립트는 해당 폴더 source 및 scripts에 포함한다. 마지막 0.5초 경계 보호는 누락률에만 적용하며 지연 max는 전체 측정 구간에서 완료된 프레임을 사용한다.\n';p.write_text(text)
print('Updated notes, README and sources')
