"""최신 B안의 공통 장과 담당 기술 장을 조합해 개인 발표자료를 생성한다."""
from pathlib import Path
import json
import re
import shutil
import html

BASE=Path(__file__).resolve().parent
SHARED=BASE.parent/'work/B'
assets=BASE/'assets';assets.mkdir(exist_ok=True)
for name in ['slides.css','slides.js']:
 shutil.copy2(SHARED/name,BASE/name)
for name in ['lig-logo.png','Pretendard-Regular.woff2','Pretendard-SemiBold.woff2','FONT-LICENSE.txt','윤오름.png','김재남.png','윤관.png','정하건.png','홍정호.png','hardware-photo.jpg']:
 if (SHARED/'assets'/name).exists():shutil.copy2(SHARED/'assets'/name,assets/name)
shared_html=(SHARED/'index.html').read_text(encoding='utf-8')
sections=re.findall(r'<section class="slide\b.*?</section>',shared_html,re.S)
shared_deck=json.loads((SHARED/'deck.json').read_text(encoding='utf-8'))
slides=[]
def shared(number,scope_number):
 section=sections[number-1]
 body=re.search(r'<main>(.*?)</main>',section,re.S).group(1)
 d=dict(shared_deck['slides'][number-1]);d.update(body=body,scope_number=scope_number)
 slides.append(d)
def chain(items):
 return '<div class="b-chain">'+''.join('<div><small>'+str(i+1).zfill(2)+'</small><h3>'+h+'</h3><p>'+t+'</p></div>'+('<b>→</b>' if i<len(items)-1 else '') for i,(h,t) in enumerate(items))+'</div>'
def own(title,scope_number,seconds,body,spoken,cues,condition=''):
 slides.append(dict(title=title,scope_number=scope_number,seconds=seconds,body='<div class="scene b-scene">'+body+(f'<div class="scene-caption">{condition}</div>' if condition else '')+'</div>',spoken=spoken,quick_cues=cues,presenter_cue=' → '.join(cues),refs=['정하건 v3 · 7249d7b'],pending=[]))

for n in range(1,6):shared(n,n)
shared(20,10)
slides[-1]['title']='표적 선택 및 짐벌 제어'
slides[-1]['seconds']=65
slides[-1]['spoken']='사용자가 선택한 Track ID의 최신 위치에서 조준점을 정하고 화면 목표점과의 오차를 계산합니다. 이 오차가 두 축 제어의 입력입니다. 제어기에서는 불감대와 속도 제한을 적용해 짐벌 명령으로 연결합니다. 추적기 선택과 추적 대상 ID 선택은 별개입니다. 추적기 교체 뒤 선택 ID를 어떻게 처리할지는 최종 운용 설정과 맞춥니다. 공개된 다른 실행 스크립트의 제어값이나 단축키를 현재 장치 설정으로 옮겨 설명하지 않습니다.'
own('영상·메타데이터 통신',11,65,
 chain([('Runtime','검출 · 추적 결과 생성'),('영상 · BBox 전송','RTP/UDP 영상 · UDP 메타데이터'),('PC 표시','영상·상자 대응 · 선택 ID')])+'<div class="ribbon">TCP 제어·상태 경로와 영상·메타데이터 경로 분리</div><div class="b-keywords"><span>JPEG · H.264 수신</span><span>FPS · 지연 · 연결 상태 계측</span></div>',
 '제 담당은 Runtime의 전체 파이프라인 구현보다 PC와 보드 사이의 통신 경계입니다. PC 앱은 RTP/UDP 영상과 UDP 메타데이터를 수신하고 영상과 사람 상자를 대응해 표시합니다. JPEG와 H.264 수신 및 FPS, 지연, 연결 상태의 계측 기능을 구현했습니다. 명령과 상태 확인은 TCP 경로로 분리합니다. 파이프라인과 추적기 내부 구현은 각 담당자의 설명으로 이어가고, 여기서는 PC 수신과 표시, 제어 요청의 연결을 설명합니다.',
 ['영상·메타데이터','같은 프레임 대응','제어·계측 경계'],
 'PC 앱 개발 기여 및 팀원 v3의 PC–Runtime TCP 구조 기준 · 실제 데모의 코덱·전송 설정은 최종 캡처와 맞춤')
own('추적기 선택 및 변경 확인',12,70,
 chain([('PC GUI','3종 추적기 중 선택'),('변경 요청','TCP로 추적기 번호 전송'),('Runtime 교체','설정 생성 · 프레임 경계'),('상태 확인','Accepted → Completed')])+'<div class="b-keywords"><span>1 ByteTrack</span><span>2 OC-SORT</span><span>3 BoT-SORT</span></div><div class="ribbon">생성 실패 시 기존 추적기 유지</div>',
 '정하건 팀원의 최신 자료에 따르면 GUI에서 ByteTrack, OC-SORT, BoT-SORT를 선택할 수 있습니다. GUI가 보내는 것은 추적기 번호이고 Runtime은 카탈로그에서 해당 설정을 찾습니다. 새 추적기를 생성한 뒤 다음 프레임 경계에서 교체합니다. 접수 응답과 완료 응답을 구분해 변경 결과를 확인하고, 생성 실패 시에는 기존 추적기를 유지합니다. 이 장은 GUI와 Runtime 사이의 요청·응답 경계를 설명하며, 세 알고리즘의 구조와 튜닝 결과는 정하건 팀원 파트에서 설명합니다. 실제 화면은 데모 앱의 캡처가 확보되면 추가합니다.',
 ['추적기 번호 선택','프레임 경계 교체','접수·완료·실패 유지'],
 '정하건 v3 · tracking_catalog 1/2/3 · 조회 0x02/0x82 · 변경 0x04/0x84')
own('연동 및 검증 범위',13,60,
 '<table><thead><tr><th>확인 대상</th><th>최신 자료에 반영한 동작</th></tr></thead><tbody><tr><td>추적기 선택</td><td>3종 카탈로그와 GUI의 번호 선택</td></tr><tr><td>변경 성공</td><td>Accepted → 프레임 경계 교체 → Completed</td></tr><tr><td>생성 실패</td><td>기존 추적기 유지 · 실패 결과 확인</td></tr><tr><td>실제 시연</td><td>사용 앱·선택 추적기·ID 처리·영상 설정 고정</td></tr></tbody></table><div class="ribbon">기능 연동 근거와 실제 현장 측정은 구분</div>',
 '연동에서는 요청이 도착했다는 것과 실제 변경됐다는 것을 구분해서 확인합니다. 팀원 자료의 접수·완료 응답과 생성 실패 시 기존 추적기 유지가 그 기준입니다. 성능 비교에서 기본 추천은 BoT-SORT이며, OC-SORT는 ID 변경과 재현율에 강점이 있어 함께 남겼습니다. 비교 조건과 세부 수치는 추적 알고리즘 파트에서 설명합니다. 최종 시연에서는 실제 앱과 선택한 추적기, 교체 후 ID 처리, 영상 설정을 맞추고 동작과 계측 결과를 확인합니다. 이번 자료 개정은 팀원 제공 문서에 따른 것으로, 제가 장치 시험을 새로 수행한 결과는 아닙니다.',
 ['변경 성공','실패 유지','최종 설정·측정'],
 '기능·비교 근거: 정하건 v3. 실제 현장 FPS·표시 지연·짐벌 반응은 같은 설정의 로그로 별도 반영.')

for i,d in enumerate(slides,1):d['number']=i
def slide_html(d):
 n=d['number'];cover=n==1
 return f'<section class="slide{" cover-slide" if cover else ""}" id="slide-{n:02d}" data-number="{n}" data-seconds="{d["seconds"]}" aria-label="{html.escape(d["title"])}"><header>'+('' if cover else '<h1>'+html.escape(d['title'])+'</h1>')+'<img class="logo" src="assets/lig-logo.png" alt="LIG D&amp;A"></header><main>'+d['body']+'</main><div class="slide-source" aria-hidden="true"></div><footer><span>'+f'{n:02d} / {len(slides):02d}'+'</span></footer></section>'
head='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>윤오름 · 시스템·PC 통신·제어 발표</title><link rel="stylesheet" href="slides.css"></head><body>'
toolbar='<nav class="toolbar"><button id="prev">←</button><span id="page">1 / 9</span><button id="next">→</button><span id="clock" hidden></span><button id="timer" hidden></button><button id="overview">모아보기</button><a href="notes.md">대본</a><a href="presentation.pdf">PDF</a></nav><script src="slides.js"></script></body></html>'
(BASE/'index.html').write_text(head+''.join(map(slide_html,slides))+toolbar,encoding='utf-8')
manifest=dict(title='윤오름 담당 발표',slides=[{k:v for k,v in d.items() if k!='body'} for d in slides],total_seconds=sum(d['seconds'] for d in slides),source_commit='7249d7b',demo_seconds=0)
(BASE/'deck.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
notes=['# 윤오름 담당 발표 노트','','2026-11-18 개정. 정하건 v3(7249d7b)를 팀원 제공 근거로 반영했다. 장치·Runtime·GUI 재시험은 하지 않았다.','', '## 설명 범위', '', '- 중심: 전체 시스템 및 PC 통신·표시·계측, 표적 선택과 짐벌 제어, 추적기 변경 요청·상태 확인.', '- 정하건 파트: 세 추적기의 내부 구조·튜닝·성능 비교. 본 자료에서 알고리즘 개발을 윤오름 단독 기여로 설명하지 않는다.', '- 김재남·홍정호 파트: Runtime 파이프라인·멀티스레드·NPU 가속·최적화. PC 송수신·계측 경계와 구분한다.', '- 웹 GUI·HTTP·Picture First·브라우저 단축키는 발표 본문에서 제외했다. 실제 운용 앱 캡처·설정은 최종 반영한다.', '- 팀원 자료를 믿고 통합하되, 문서 편집이 새 장치 검증을 의미하지는 않는다.','']
for d in slides:
 notes += [f'## {d["number"]:02d}. {d["title"]}',f'전체 목차 담당 주제: {d["scope_number"]:02d} / 목표 {d["seconds"]}초','',d['spoken'],'','화면 진행: '+' → '.join(d['quick_cues']),'']
notes += ['## 출처와 조건','','- [정하건 v3 발표 노트](../정하건/정하건_v3/발표노트.md)', '- [추적 비교·통신 명령 근거](../정하건/정하건_v3/근거_비교표.md)','- [최신 팀 역할](../work/B/team-roles.md)','- [공통 디자인 기준](../work/DESIGN.md)','- [이전 웹 GUI·제어 비교 분석](model-bank-GUI-제어-비교분석.md): 과거 조사 보관용. 현재 데모 구성의 근거로 자동 적용하지 않는다.','','비교 요약: BoT-SORT HOTA 60.7·IDF1 67.5%·IDSW 566, OC-SORT HOTA 59.1·IDF1 66.7%·IDSW 531. 둘은 같은 PC 조건이다. ByteTrack 2,964회는 Orange Pi 결과이므로 동일 하드웨어의 전후 비교로 합치지 않는다. CMC·BoT-SORT ReID는 이번 비교에서 사용하지 않았다.','', '교체 후 선택 ID 유지·해제와 단축키·제어값·실제 코덱은 최종 앱·장치 설정에 맞춘다. 과거 가상 표적 시험이나 공개 PD 기본값을 실제 현장 성공률로 설명하지 않는다.']
(BASE/'notes.md').write_text('\n'.join(notes)+'\n',encoding='utf-8')
print(f'Built personal deck: {len(slides)} slides, {manifest["total_seconds"]} target seconds')
