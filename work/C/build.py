"""Build C from its frozen B seed and the team evidence through 8a195d7.

All inputs are local to C. B and the team originals are never written.
"""
from pathlib import Path
import copy
import hashlib
import html
import json
import re
import shutil
from editorial import clarify_terms, polish, polish_dates
from visual_layouts import enrich
from tracking_story import finalize_tracking
from revision_20261122 import apply_revision
from narrative import refine_narrative

BASE = Path(__file__).resolve().parent
PICTURES = BASE.parents[1]/'reference/picture'
asset_records=[]
for name in ['hardware.png','윤오름.png','김재남.png','윤관.png','정하건.png','홍정호.png']:
    source=PICTURES/name
    target=BASE/'assets'/name
    if source.exists():
        shutil.copy2(source,target)
    if target.exists():
        asset_records.append(dict(file=name,source='reference/picture/'+name,sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(BASE/'picture-manifest.json').write_text(json.dumps(dict(files=asset_records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
SEED = json.loads((BASE/'seed.json').read_text(encoding='utf-8'))
SOURCES = copy.deepcopy(SEED['sources'])
SOURCES['S25']=dict(title='그림·실측 그래프 재구성 원자료',url='sources/visual-reference/manifest.json')
SOURCES['S26']=dict(title='11/22 비교 결과·절충 정정',url='sources/revision-20261122/manifest.json')
SOURCES['S27']=dict(title='11/22 모델뱅크 추천 원문',url='sources/revision-20261122/model-bank-recommended.json')
SNAP = 'sources/latest-20261121/'
for key, title, path in [
    ('S17', '11/20–21 추가 실험·장치 상태', '윤관/근거_최신_20261120.md'),
    ('S18', '외형 모델 학습·교사 정정', '윤관/학습기록_외형모델.md'),
    ('S19', '상체 모델 학습·재현 기록', '윤관/학습기록_상체검출기.md'),
    ('S20', '위치 예측 학습 기록', '윤관/학습기록_위치예측.md'),
    ('S21', 'FastTrackTr 학습 기록', '윤관/학습기록_FastTrackTr.md'),
    ('S22', '11/21 슬라이드·장치 비교 근거', '윤관/근거_슬라이드별.md'),
    ('S23', '11/20 추적기 대본 개정', '정하건/정하건_v3/발표노트.md'),
    ('S24', '추적기 비교 원표·CMC 미사용', '정하건/정하건_v3/근거_비교표.md'),
]:
    SOURCES[key] = dict(title=title, url=SNAP+path)

def esc(text):
    return html.escape(str(text))

def table(headers, rows):
    return '<table class="c-table"><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'

def flow(items):
    return '<div class="c-flow">'+'<b class="c-arrow">→</b>'.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in items)+'</div>'

def cards(items):
    return '<div class="c-cards">'+''.join(f'<article><h3>{a}</h3><strong>{b}</strong><p>{c}</p></article>' for a,b,c in items)+'</div>'

def chart(title, labels, values, maximum, unit='', highlight=-1):
    # Each chart has a shared, zero-based axis. Different metrics use separate charts.
    count = len(labels)
    height = 125 + 76*count
    out = f'<div class="c-chart"><h3>{title}</h3><svg viewBox="0 0 800 {height}" role="img" aria-label="{esc(title)}">'
    for tick in [0, maximum/2, maximum]:
        x=235+450*tick/maximum
        out += f'<line x1="{x}" x2="{x}" y1="12" y2="{height-64}" stroke="#dce2ea"/><text x="{x}" y="{height-26}" text-anchor="middle" fill="#667085" font-size="22">{tick:g}</text>'
    for i,(label,value) in enumerate(zip(labels,values)):
        y=30+i*76
        color='#002f6d' if i==highlight else '#9fb2c5'
        width=450*value/maximum
        out += f'<text x="220" y="{y+30}" text-anchor="end" font-size="24" fill="#202b3a">{esc(label)}</text><rect x="235" y="{y}" width="{width}" height="42" fill="{color}"/><text x="{245+width}" y="{y+30}" font-size="25" fill="#002f6d">{value:g}{unit}</text>'
    return out+'</svg></div>'

def scene(content, takeaway='', caption=''):
    return '<div class="scene b-scene c-scene">'+content+(f'<div class="c-take">{takeaway}</div>' if takeaway else '')+f'<div class="scene-caption">{caption}</div></div>'

slides = copy.deepcopy(SEED['slides'])
by = {s['base_number']:s for s in slides}
changes=[]
evidence=[]

def update(n, body=None, spoken=None, refs=None, cues=None, title=None, condition=None):
    s=by[n]
    if body is not None:s['body']=body
    if spoken is not None:s['spoken']=spoken
    if refs is not None:s['refs']=refs
    if cues is not None:s['quick_cues']=cues
    if title is not None:s['title']=title
    if condition is not None:s['condition']=condition
    s['presenter_cue']=' → '.join(s['quick_cues'])
    changes.append((n,s['title']))
    return s

insertions={}
def insert(after, title, body, spoken, refs, cues, condition=''):
    s=dict(title=title,body=body,spoken=spoken,refs=refs,quick_cues=cues,presenter_cue=' → '.join(cues),condition=condition,pending=[],section='최신 결과',seconds=30,base_number=None)
    insertions.setdefault(after,[]).append(s)
    return s

def record(title, values, condition, limit, refs):
    evidence.append(dict(title=title,values=values,condition=condition,limit=limit,refs=refs))

# Existing sections: correct the interpretation as well as adding new results.
update(4, body=scene(cards([
    ('시간','30 Hz','입력 주기 약33.3 ms'),
    ('처리','모든 프레임','33 ms 이내 · 입력 버림0 · 순서 오류0'),
    ('운용','선택 ID','재포착 · 수동 개입 · 정지'),
]),
    'p95와 처리량만으로 모든 프레임의 시간 목표를 판정하지 않음',
    '33 ms는 후속 서버 시험의 판정 기준 · 거리·현장 ID 유지 기준은 미확정'),
    spoken='입력 목표는 30헤르츠, 약 33.3밀리초 주기입니다. 후속 서버 시험에서는 모든 프레임이 33밀리초 이내이고 입력 버림과 순서 오류가 없어야 통과하는 기준을 썼습니다. p95가 이보다 낮아도 긴 지연이 남으면 전체 통과는 아닙니다. 검출 거리와 실제 현장 ID 유지의 정량 기준은 아직 확정 자료가 없습니다.', refs=['S1','S17'], cues=['30Hz 입력','모든 프레임 기준','거리·ID는 미확정'])
update(6, spoken=by[6]['spoken']+' 이후 모델뱅크 서버에서도 NPU 제출과 회수, 전후처리 일부를 C++로 옮긴 시험이 추가됐습니다. 이것을 여기의 공통 C++ Runtime 전체와 같은 구현으로 합치지 않습니다. 최종 시연에서 사용할 실행 경로는 별도로 고정해야 합니다.', refs=['S3','S4','S14','S17'])
update(9, spoken='상체 모델은 공개 자세 모델의 F 가중치에서 현장 650장으로 10 epoch 학습한 갈래입니다. 검수한 상체와 관절만 감독하고, 미표기 인물의 분류 손실은 제외했습니다. seed 0, batch 4, AdamW 초기 학습률 2e-5, FP32 조건이 추가 기록으로 확인됐습니다. OTP2 검증 934장과 별도 시험 2,151장은 구분합니다. FLIR 검출기의 30 epoch는 다른 학습 이력입니다.', refs=['S15','S19'])
update(11, title='후속 학습 채택 판단', body=scene(
    '<div class="c-two">'+chart('OTP2 박스 AP50–95 ↑',['운영 E10','표준 증강','강한 증강','직각 회전'],[46.28,48.16,45.37,44.68],60,'%',0)+
    '<div class="c-panel"><h3>박스만 보고 교체하지 않음</h3><p>표준 증강: 박스 +1.88%p<br>관절 78.35 → 77.31%</p><p>실내·실외 추적에서<br>함께 앞선 후보 없음</p><h3>운영 E10 유지</h3></div></div>',
    '추가 3 epoch·CLAHE·관절 보정도 운영 교체 근거 부족',
    'OTP2 934장 · 자체 703장 분할은 E10 학습 노출이 있어 독립 비교로 사용하지 않음'),
    spoken='후속 학습에서는 표준 증강의 박스 AP가 48.16으로 운영 E10보다 1.88퍼센트포인트 높았습니다. 하지만 관절 AP는 1.04포인트 내려갔고, 실내와 실외 추적에서 함께 이긴 후보는 없었습니다. 자체 시험에는 E10이 이미 본 장면도 많아 독립 비교로 쓸 수 없습니다. 추가 3 epoch와 CLAHE까지 확인했지만 운영 모델 교체는 보류했습니다.', refs=['S17','S19'], cues=['표준 증강 박스 향상','관절·추적 절충','E10 유지'])
record('검출기 후보','박스 AP 46.28 / 48.16 / 45.37 / 44.68%; 표준 증강 관절 AP 77.31%','OTP2 검증 934장','독립 현장 시험 아님; 자체 분할은 학습 노출 존재',['S17','S19'])
update(12, body=scene(flow([('학습·선택','가중치와 시험 분리'),('ONNX → INT8','입력·출력·보정 확인'),('배포·재설치','모델과 실행 경로 확인')]),'추천 모델 · 장치 선택 모델 · 시험용 모델을 따로 기록', '재설치 뒤 실행 경로가 달라진 기록 존재 · 뒤의 장치 상태 장에서 구분'),
    spoken='배포는 모델 파일을 복사하는 것으로 끝나지 않습니다. 변환 뒤 정확도와 속도를 확인하고, 재설치 뒤에도 해당 모델과 실행 경로가 유지되는지 확인해야 합니다. 새 기록에는 추천 모델, 장치가 고른 모델, 시험용 모델이 서로 다른 사례가 나옵니다. 이 상태를 하나의 최종 설정으로 묶지 않겠습니다.', refs=['S11','S17','S18'], cues=['변환 검증','재설치 확인','추천·선택·시험 구분'])

insert(12,'외형 모델 비교',scene('<div class="c-two">'+
    chart('OTP2 몸 1순위 정답 ↑',['ViT-lite FT','ViT-lite 증류','RepVGG OTP2','RepVGG 검수264'],[.616,.672,.892,.764],1,'',2)+
    chart('M1 NPU 처리 시간 ↓',['ViT-lite FT','ViT-lite 증류','RepVGG OTP2','RepVGG 검수264'],[5.03,5.02,1.26,1.28],6,' ms',3)+'</div>',
    'RepVGG는 약 4배 빠름 · 검수264판과 OTP2판의 정확도를 구분',
    '같은 M1 INT8 시험 · 검수264판 장치 선택 기록 · 실내 질의 176개는 참고값'),
    '가림 뒤 같은 사람을 잇는 외형 모델도 비교했습니다. 같은 M1 INT8 조건에서 ViT-lite는 약 5밀리초, RepVGG는 약 1.3밀리초였습니다. 공개 OTP2 몸 정답률도 RepVGG 계열이 높았습니다. 다만 OTP2 학습판 0.892와 장치 선택 기록이 있는 검수264판 0.764는 다른 모델입니다. RepVGG가 모든 장면에서 검증됐다는 뜻은 아닙니다.',
    ['S18','S22'],['같은 M1 비교','모델별 정확도','RepVGG 사용'])
record('외형 모델 M1 비교','정답 0.616 / 0.672 / 0.892 / 0.764; 시간 5.03 / 5.02 / 1.26 / 1.28 ms','ViT-lite FT·증류, RepVGG OTP2·검수264 순; 동일 M1 INT8','장치 선택·추천과 학습판을 구분; 실내 질의176',['S18','S22'])

update(14, spoken='ByteTrack은 검출 점수로 두 단계 매칭을 하고, OC-SORT는 실제 관측과 이동 방향을 활용합니다. BoT-SORT는 박스 추정과 매칭을 보완하고 일반적으로 카메라 움직임 보정도 지원해 짐벌 시스템의 후보가 됩니다. 다만 이 팀의 HOTA·IDF1 비교에서는 CMC와 ReID를 껐습니다. 일반 알고리즘의 기능과 해당 비교의 실행 설정은 구분해야 합니다.',refs=['S14','S23','S24'], cues=['세 추적기','일반 CMC 기능','비교에서는 미사용'])
update(16, spoken=by[16]['spoken']+' 짐벌로 카메라가 움직이므로 BoT-SORT의 카메라 움직임 보정은 적용 검토 이유가 되지만, 이 수치 비교는 CMC와 ReID를 끈 결과입니다. 이 표로 보정 효과를 입증한 것은 아닙니다.',refs=['S14','S23','S24'])
insert(16,'번호 유지 보완',scene('<div class="c-two">'+chart('놓침 위치 오차 / 사람 키 ↓',['Kalman','GRU 수정 전','GRU 수정 후','Mamba 재학습'],[.110,.336,.122,.127],.4,'',2)+
    '<div class="c-panel"><h3>번호 복구와 보호</h3>'+table(['같은 녹화 비교','끔','켬'],[['KeepID 번호 변경','47','43'],['가드: 0.5초 초과 뺏김','20','17']])+'<p>위치 예측과 신원 연결은<br>서로 다른 평가</p></div></div>',
    'GRU는 Kalman 수준으로 회복 · 번호 복구·가드는 제한적인 개선',
    '위치: 14편·놓침238건 · 번호: 라벨9편 PC FP32 · 개발에 쓴 녹화이며 장치 효과 미측정'),
    '번호 유지는 위치 예측과 신원 연결을 나눠 봤습니다. GRU 오류를 고쳐 오차가 0.336에서 0.122로 줄었지만 Kalman 0.110을 넘지는 못했습니다. 별도 라벨 녹화 비교에서 KeepID의 번호 변경은 47에서 43, 가드의 오래 지속된 번호 뺏김은 20에서 17로 줄었습니다. 같은 개발 녹화를 썼고 장치 효과는 재지 않아 현장 보장으로 설명하지 않습니다.',
    ['S17','S20','S22'],['위치 예측','번호 복구·가드','개발 녹화 한계'])
record('번호 유지','GRU 0.336→0.122, Kalman0.110; KeepID47→43; 가드20→17','위치14편 놓침238건; 번호9편3877장 PC','개발 노출; 장치 효과 미측정',['S17','S20','S22'])

insert(18,'분할 모델 변환',scene(flow([('타일 그래프','480×384 입력<br>가중치 유지'),('INT8 보정','264장 × 좌·우<br>528조각'),('DX-COM','NPU 그래프 1개<br>CPU 부분 0'),('좌표·병합','오른쪽 x +256<br>중심320 → NMS')])+table(['변환 진단','전체 화면','분할'],[['맞힌 사람 수 · FP32','445','457']]),
    '입력 모양과 병합 규칙까지 검증 · 독립 정확도 평가는 별도',
    '검수264 E10·학습에 쓴264장 진단 · 현장650 E10 분할판 정확도 보장 아님'),
    '분할은 단순히 영상을 자르는 작업만은 아닙니다. 같은 가중치로 입력 폭을 384로 바꾸고 그래프 모양 상수를 고쳤습니다. 검수264장의 좌우 타일 528조각으로 INT8을 보정했고 확인한 파일은 NPU 그래프 하나, CPU 부분은 없었습니다. 오른쪽 좌표에 256을 더하고 중심 320 기준으로 후보를 골라 NMS를 합니다. 맞힌 사람 445와 457은 학습264장 FP32 진단이므로 독립 정확도 근거로 쓰지 않습니다.',
    ['S17','S19'],['입력 그래프','INT8 보정','좌표·정확도 범위'])
update(19, spoken=by[19]['spoken']+' 이때 사용한 것은 E10+3 시험 모델이며 11월20일 재설치 전 기록입니다. 현재 장치 상태를 대표하는 값으로 쓰지 않습니다.',refs=['S15','S17'],condition='11/19 E10+3 시험 모델·모드별65초·수신→추적완료·동시 타일 큐 버림1')
by[19]['body']=by[19]['body'].replace('11-19 · 모드별 65초 1회','11-19 · E10+3 시험 모델 · 재설치 전 · 모드별 65초 1회')
insert(19,'장시간·혼잡 조건',scene(cards([
    ('장시간 실카메라','18,497장','33 ms 초과 5장<br>최대 44.582 ms'),
    ('4명 녹화','p95 27.16 ms','805장 · 초과 4장<br>최대 57.19 ms'),
    ('고밀도 녹화','p95 42.52 ms','592장 · 초과 217장<br>최대 66.87 ms'),
]),'C++ 이식 뒤 사람이 있는 실카메라 시험은 확보되지 않음',
    '장시간 입력 버림·순서 오류0 · 사람 있는 두 녹화는 C++ 이식 전 · 세 조건은 별도 실행'),
    '후속 결과는 긴 지연이 남는다는 것을 보여줍니다. 장시간 실카메라 18,497장에서 33밀리초 초과가 다섯 장, 최대는 44.582밀리초였습니다. 사람 있는 고밀도 녹화에서는 p95도 42.52밀리초였습니다. 오른쪽 두 녹화는 C++ 이식 전이고 장시간 시험과 조건이 다릅니다. C++ 이식 뒤 사람이 있는 실카메라 검증은 아직 없습니다.',
    ['S17'],['긴 지연 잔존','사람 수 영향','후속 실카메라 필요'])
record('후속 지연','18497장 초과5·최대44.582ms; 4명 p95 27.16·초과4/805; 고밀도 p95 42.52·초과217/592','별도 서버; 사람 녹화는 C++ 이식 전','세 조건 별도; 최종 Runtime 종단 아님',['S17'])
insert(19,'장치 상태 이력',scene(flow([
    ('11/19 시험','동시 타일·E10+3<br>p95 25.71 ms'),
    ('11/20 재설치','일부 로컬 코드 누락<br>전체 화면 실행 기록'),
    ('11/20~21 추가','분할 재연결 작업<br>가드·추천·보정 변경'),
])+table(['구분','확인된 기록'],[['재설치 직후 12분','33 ms 초과 14,803 / 21,579장 (68.6%)'],['현재 최종 시연','모델·실행 경로·스위치의 일치 확인 필요']]),
    '과거 시험값과 최종 시연 설정을 한 성능으로 연결하지 않음',
    '11/20 오전 전체 화면 실행 기록 · 후속 분할 모델 파일 확인과 최종 실행 검증은 구분'),
    '장치 상태도 달라졌습니다. 11월20일 main에서 재설치하며 로컬 분할 연결과 KeepID 번호 복구가 빠진 기록이 있습니다. 그 직후 사람 없는 12분 관찰에서는 68.6퍼센트가 33밀리초를 넘었습니다. 이후 분할 모델과 가드, 박스 보정이 다시 추가됐지만 마지막 시연 경로가 어느 구성인지 확인한 자료는 없습니다. 앞의 25.71밀리초를 현재 성능이라고 말하지 않겠습니다.',
    ['S17'],['재설치 누락','후속 변경','최종 구성 확인'])

update(20, spoken=by[20]['spoken']+' 후속 코드에서는 상체 박스 보정을 항상 켜도록 바꿨습니다. 실내 세 녹화의 키 변화 상위1퍼센트는 0.071에서 0.043으로 줄었지만 조준 떨림은 0.0195로 같았습니다. 코드 기본값 변경과 실제 장치 반영은 구분하며 조준 성능 개선으로 확대하지 않습니다.',refs=['S15','S17'])
insert(23,'짐벌 응답 실측',scene('<div class="c-two">'+chart('가로 속도 실측 ↑',['SPD 10','SPD 20','SPD 30'],[305,630,930],1200,' px/s',2)+
    '<div class="c-panel"><h3>명령 뒤 실제 반응</h3><strong class="c-big">108 ms</strong><p>속도 90% 도달 158 ms<br>STOP 효과 64 ms</p><p>SPD·방향별 2~3회<br>세로·SPD30 초과 미측정</p></div></div>',
    '실측 속도·지연을 넣어 짐벌 모형을 수정',
    '11/15 실제 짐벌·카메라 직접 속도 명령 · 실제 사람 자동 추종 시험과 구분'),
    '짐벌 자체 반응도 직접 쟀습니다. 가로 속도는 SPD10, 20, 30에서 약 305, 630, 930픽셀 매초였고 명령 뒤 화면 반응까지 108밀리초였습니다. 이 값으로 예전 모형의 잘못된 속도 상한을 고쳤습니다. 다만 가로 직접 속도 명령 시험이며 세로와 높은 SPD, 실제 사람 자동 추종은 별도입니다.',
    ['S17'],['가로 실측','108ms 반응','모형 수정'])
insert(23,'가상 카메라 시험',scene(flow([
    ('열화상 녹화','TMOT·PTB-TIR·BU-TIV'),('확대·자르기','가상 카메라 입력'),('장치 처리','검출·추적·KeepID'),('짐벌 모형','실측 속도·지연'),
])+ '<div class="c-feedback">← 짐벌 명령만큼 잘라낼 창 이동 · 정답 라벨로 같은 사람 / 바뀜 / 놓침 채점</div>'+cards([
    ('제어값 비교','112회','Kp 30 유지'),('예측 앞당김','이득 없음','마지막 기록 lead200 켬과 불일치'),('넓게 훑기','두 차례 보류','정한 재포착 기준 미통과'),
]),'같은 장면을 반복해 비교 · 실제 사람·실제 짐벌 검증은 별도',
    '확대한 열화상 녹화 · 시험 판단과 장치에 켠 설정을 분리'),
    '짐벌 튜닝은 같은 장면을 반복하는 가상 카메라로 시험했습니다. 녹화를 확대해 자른 영상을 장치에 넣고 실제 처리와 제어 코드를 돌립니다. 실측 반응을 넣은 짐벌 모형이 창을 이동시키고 정답으로 재포착과 번호 변경을 셉니다. 제어값112회에서 Kp30을 유지했습니다. 예측 앞당김은 이득이 없었지만 마지막 기록의 lead200 켬과 달라 최종 설정 확인이 필요합니다.',
    ['S17','S22'],['닫힌 반복 구조','정답 채점','시험·설정 구분'])
insert(23,'놓침 대응과 절충',scene('<div class="c-two">'+
    '<div class="c-panel"><h3>예측 자리 따라가기</h3>'+table(['가상 재포착 차이','95% 구간'],[['vel: +20%p','+7 ~ +32%p'],['장치 기록 fused: +6%p','−11 ~ +21%p']])+'<p>vel 이득을 fused 성과로<br>옮겨 설명하지 않음</p></div>'+
    '<div class="c-panel"><h3>가속·탐색의 대가</h3><p>가속150: 추종 가능 속도<br>약750 → 900 px/s</p><p>원거리 이득1.6: 급정지<br>지나침 11 → 35 px</p><p>넓게·좌우 훑기: 보류<br>좁게 보기: 기능 시험만</p></div></div>',
    '기능을 켠 기록과 실제 사람 재포착 성능 입증을 구분',
    '재포착은 가상 비교 · 속도·지나침은 PC 모의시험의 서로 다른 조건'),
    '놓친 자리 따라가기는 방식별로 봐야 합니다. 가상시험의 vel은 재포착이20퍼센트포인트 늘었지만 장치 기록의 fused는6포인트이고 불확실 구간이0을 포함합니다. 가속과 원거리 이득도 빠른 사람을 따라가는 대신 급정지 지나침을 키웠습니다. 넓게 훑기와 좌우 훑기는 보류했고 좁게 보기는 기능 시험만 있습니다. 실제 사람 재포착률은 아직 확보되지 않았습니다.',
    ['S17'],['vel·fused 구분','가속 절충','실제 재포착 미평가'])
record('짐벌','SPD10/20/30=305/630/약930px/s; 명령반응108ms; vel+20%p·fused+6%p','속도 직접실측; 재포착 가상시험 별도','fused95%구간−11~+21%p; 실제사람 종단 미측정',['S17'])

update(27, body=scene(flow([('설정 고정','모델·추적기·제어'),('실제 동작','선택 → 추종 → 가림'),('운용 확인','수동 전환 → 정지')]),'시연 화면·설정·측정 기록을 같은 실행으로 맞추기', '실제 앱 캡처·통합 영상·최종 설정은 미확보'),spoken='시연은 먼저 모델 파일, 추적기와 제어 스위치를 고정하고 같은 실행의 영상과 설정 기록으로 설명합니다. 표적 선택과 추종, 가림 뒤 동작을 보인 다음 수동 전환과 정지를 확인합니다. 현재 자료에는 이 세 가지가 맞춰진 최종 시연 묶음이 없어 영상 자리를 남겼습니다.', refs=['S14','S17'], cues=['같은 실행의 설정','선택·추종·가림','수동·정지'])
update(30, body=scene(cards([('PC 개발 비교','근거 확보','IDSW·KeepID·가드 비교'),('최종 장치','검증 필요','가림·재포착·오인 연결'),('현장 판정','기준 확정 필요','유지 시간·허용 끊김·반복')]),'PC에서 줄어든 번호 변경을 현장 ID 유지율로 환산하지 않음', '동일 시연 경로·정답 라벨·반복 결과 필요'), spoken='PC 녹화의 ID 변경과 가드 결과는 확보했지만 최종 장치의 현장 ID 유지 검증은 남았습니다. 같은 사람을 잇는지, 다른 사람으로 넘어가는지, 얼마나 끊겼는지를 정답과 비교해야 합니다. 유지시간과 허용 끊김 기준도 아직 없습니다. PC의 47에서43을 현장 유지율로 바꾸어 말하지 않습니다.', refs=['S17','S20','S22'], cues=['PC 근거 확보','현장 정답 비교','시간·끊김 기준'])
update(31, body=scene(flow([('카메라·입력','지연 일부 추정'),('서버 수신 → 결과','개별 시험 수치 확보'),('화면·물리 짐벌','최종 종단 미측정')])+table(['판정 범위','현재 확보한 내용'],[['짧은 시험','p95 25.71 ms · 큐 버림1 · 전 프레임 통과 아님'],['장시간 시험','18,497장 중 초과5 · 최종 시연 경로와 구분']]),'30 Hz 처리량 · p95 · 모든 프레임 · 종단 지연을 따로 판정', '최종 모델·사람 있는 조건·화면·실제 짐벌을 포함한 반복 측정 필요'), spoken='시간 검증은 경계별로 정리하겠습니다. 별도 서버에서 짧은 시험과 장시간 시험을 했지만 모든 프레임33밀리초 목표를 통과하지는 못했습니다. 카메라 입력부터 화면과 실제 짐벌 반응까지의 최종 종단 지연도 없습니다. 짐벌 반응 약190에서210밀리초는 과거 구간을 합친 추정값이며 실측 종단값으로 표시하지 않습니다.', refs=['S17'], cues=['계측 경계','초과 프레임 잔존','종단 미측정'])
update(32, body=scene(cards([('찾기','상체 E10','현장650장 · OTP2 AP46.28%<br>추가 후보 운영 교체 보류'),('이어가기','3종 추적·RepVGG','번호 복구·가드 개발 비교<br>현장 ID 검증은 별도'),('제때 반응','분할·C++ 보완','서버 지연 개선·긴 지연 잔존<br>최종 통합 측정 필요')]),'단계별 근거 확보 · 최종 시연 설정과 현장 검증으로 연결', '서로 다른 모델·구현·시험 조건의 결과를 단일 시스템 동시 성능으로 합치지 않음'),spoken='상체 기준을 정리해 현장650장 E10을 만들었고, 추적기와 외형 모델을 비교해 선택 근거를 확보했습니다. 분할과 C++ 보완으로 서버 지연도 줄였지만 긴 지연과 현장 검증은 남아 있습니다. 각 결과의 조건을 유지한 채 최종 시연 설정을 고정하고 검출 거리, ID 유지와 실제 짐벌까지 검증하는 것이 다음 단계입니다.',refs=['S14','S17','S18','S19','S20'],cues=['검출','ID 연결','지연·통합 검증'])

# Additional detail stays in the appendix so the main deck keeps a 20-minute target.
backup=copy.deepcopy(SEED['appendix'])
backup[5]['body']=scene(table(['갈래','후속 판정'],[['GRU·Mamba','GRU 수정후0.122, Kalman0.110; 더 낫지는 않음'],['FastTrackTr','TMOT6편 IDF1 15.3→27.1; 시험 선택지'],['SOLIDER 증류E','라벨9편 IDF1 82.4%; 기존83.0%; 시험용'],['CLAHE','별도OTP2 시험: E10 46.0, 대조44.4, CLAHE45.2']]),'채택과 보류는 같은 조건의 비교로 판단', 'FastTrackTr와 기존 추적기 점수는 동일 실행 전후가 아님')
backup[5]['refs']=['S18','S19','S20','S21']
backup[6]['body']=scene(table(['놓침 위치 오차 / 사람 키 ↓','값'],[['Kalman','0.110'],['GRU 수정 전 / 후','0.336 / 0.122'],['Mamba 재학습','0.127']]),'위치 예측 오차와 신원 연결 지표를 분리', '자체14편·놓침238건 · 이전 자료의0.118과 표본·수정을 혼합하지 않음')
backup[6]['refs']=['S20','S22']
backup[4]['spoken']='이전 v27의 각도 표시는 명령 기반 추정이다. 11/20 짐벌이 보고한 각도 눈금 기능은 미적용 기록이므로 실측 각도로 확정하지 않는다.'
def aux(title,content,spoken,refs,caption=''):
    backup.append(dict(title=title,body=scene(content,'',caption),spoken=spoken,refs=refs,seconds=0,section='예비자료',pending=[],condition=caption))

aux('검출기 후속 비교',table(['후보','박스 AP','관절 AP'],[['운영 E10','46.28%','78.35%'],['표준 증강E10','48.16%','77.31%'],['강한 증강E04','45.37%','78.86%'],['직각 회전E08','44.68%','79.27%'],['전체 재학습E10','45.96%','78.11%']]),'자체703장 중578학습·63검증·62시험. 기존 E10이 검증54/63, 시험61/62장을 학습에서 봤다. 자체시험의 E10 우위를 독립 근거로 쓰지 않는다. 실내·외 추적 양쪽을 이긴 후보가 없어 E10 유지.',['S17','S19'],'OTP2 검증934장 · 후보 E숫자는 각 학습의 epoch')
aux('학습 재현 기록',table(['학습 갈래','자료와 학습 순서'],[['별도 FLIR 검출 실험','COCO 모델 → 도로 열화상 30회 학습'],['현장 상체 검출','공개 자세 모델 → 현장 650장으로 10회 추가 학습']])+table(['현장 650장 모델 설정','값'],[['seed / batch / AMP','0 / 4 / 끔(FP32)'],['AdamW 초기 lr','2e-5'],['검증 / 별도 시험','OTP2 934 / 2,151장']]),'FLIR 검출기와 공개 자세 모델은 별도 출발점이다. 공개 C의3번째 epoch가 F, 코드 파일명은 C_control_v1_epoch2.pt이다. 별도OTP2시험에서 E10 46.0, 재현 대조44.4, CLAHE45.2로 CLAHE 차이는 재현 오차보다 작았다.',['S19'],'학습 파일·가중치·자료8,128개 검증 기록 · 학습로그 CSV는 스냅샷에 보존')
aux('SOLIDER 교사와 증류',table(['시기·모델','출발·역할'],[['11/10·11/15 교사','공개 열화상 재식별 ThermalTrack 가중치'],['11/20 파인튜닝 시작','LUPerson RGB 자기지도 원본'],['검수264 증류B','11/10 실내 튜닝 SOLIDER ep3 고정 교사'],['11/20 증류E','RepVGG 시험 선택지; 기본 교체 아님']]),'LUPerson 원본과11/10·15 증류 교사 파일은 다르다. SOLIDER 직접교체 비교는 기존 근거에 있으나 원본 RESULT_KO 파일을 최신 조사에서 다시 찾지 못했다. 기존 PC 1회 IDF1 66.74→66.57은 잠정 인용이며 장치 효과 근거로 쓰지 않는다.',['S18'],'교사 정정05e223f · 직접교체 원본 결과 재확인 한계 보존')
aux('외형 학습과 시험용 E',table(['9편 PC FP32','장기 뺏김','번호 변경','IDF1'],[['기본RVGGA0','12','33','83.0%'],['검수264 RepVGG','13','37','83.0%'],['증류E','15','42','82.4%']]),'SOLIDER 파인튜닝은5구성·한시드이고 선택점수의 정점 후 하락했다. 교사 원본 대비 이득은 있으나 한 사람의 사전 규칙 위반으로 판단불가. 학생3종도 사전 규칙상 더 좋지 않음. E는 실내4명에서51.1→61.2%이나 전체는 불리해 시험 선택지로만 추가. NPU 정확도·속도 미측정.',['S18','S17'],'진단 코사인0.982는 장치 추적 정확도가 아님')
aux('모델 추천과 선택 기록',table(['구분','기록','주의'],[['추천 파일','검출 검수264 E10 / 외형 RVGGA0','RECOMMENDED.json의 추천'],['장치 선택','검수264 RepVGG','일부 과거모델 삭제 뒤 남은 선택'],['현장650 E10','별도학습·기존운영 기록','검수264 E10과 다른 모델'],['SOLIDER 증류E','선택 가능 시험 모델','기본 교체 아님']]),'이 표는11/20~21 시점 기록의 구분이다. 현재 실행중인 모델은 이번 편집에서 조회하지 않았다. 최종 장치 명령줄과 파일 해시를 받아야 단일 운용 구성으로 확정할 수 있다.',['S17','S18'],'추천·선택·시험 추가·실제 실행을 구분')
aux('서버 C++ 이식 비교',table(['변경·실카메라 무인','p95 전 / 후','최대 전 / 후'],[['DX-RT C API','26.33 / 24.86 ms','40.514 / 34.367 ms'],['두 코어 병렬 회수','23.61 / 23.63 ms','34.648 / 29.158 ms'],['입력 C++·버퍼 재사용','24.07 / 23.25 ms','36.256 / 39.262 ms']]),'각 약1800장·무인 실카메라 별도 비교. 출력·좌표 복원, KeepID 위치 계산, GRU입력도 C++로 보완했지만 모두 같은 전체 지연 실행이 아니다. p95 감소와 최대 증가를 같이 표시한다.',['S17'],'모델뱅크 서버 일부 C++화 · 팀 공통 C++ Runtime과 별도')
aux('지연 대안과 보류',table(['고밀도592장','p95','최대','33 ms 초과'],[['기준','42.52','66.87','217'],['후처리 먼저','41.95','78.10','293'],['CPU 코어 분리','49.04','78.73','391'],['입력512×384','30.45','63.09','16']]),'단위ms. 512입력은 지연이 줄었지만 INT8 정확도 평가가 없었다. 공유메모리는 최대35.637ms로 파이프30.155보다 나빴다. 이 대안들을 최종 장치 채택 성능으로 요약하지 않는다.',['S17'],'고밀도 녹화 · 정확도와 실행 조건이 달라 현재 시연 보장으로 사용하지 않음')
aux('INT8 컴파일 옵션', '<div class="c-two">'+chart('평균 NPU 시간 ↓',['옵션 전','aggressive'],[29.10,21.92],40,' ms',1)+chart('FLIR 사람 AP ↑',['옵션 전','aggressive'],[43.71,43.69],60,'%',1)+'</div>', '10/29 FLIR학습YOLO26s·3749프레임 M1 INT8의 aggressive_partitioning 결과다. 약24.7% 빨라졌으나 현장E10 분할은 CPU부분0이라 해당옵션을 쓰지 않았다. 새 분할 지연 개선의 원인으로 이 옵션을 설명하지 않는다.',['S17'],'10/29 과거 별도모델 · 현재 분할 파일에는 옵션 미사용')
aux('번호 가드 설정',table(['9편PC','장기 뺏김','번호 변경','IDF1'],[['끔','20','43','82.3%'],['cost_first','18','41','83.2%'],['둘 다','17','42','82.3%'],['merge_split','24','59','74.4%']]),'cost_first와feat_guard는 코드기본끔이지만11/20 17:56 장치재시작 뒤 켬기록이 있다. 장치재생효과·CPU비용은 미측정. depth_order는번호변경43→54여서끔. pre_capture도끄기로함. KeepID복구와이두가드는별도기능이다.',['S17','S22'],'개발 라벨9편 PC FP32 · IDF1 최고와 뺏김 최소 설정은 다름')
aux('박스 보정과 표시',table(['항목','결과·상태'],[['상체 박스 보정','11/20 body 기본 → 11/21 항상 켬 코드'],['키 변화 상위1%','0.071 → 0.043'],['조준 떨림','0.0195 → 0.0195'],['전신 표시','ID매칭·평가·짐벌 조준 좌표와 분리']]),'보정은 실내3편 녹화 결과. 키안정화가조준떨림개선으로이어지지않았다. 항상켬은코드상태이며장치반영기록없음. 전신투영190개는모두발목관측표본이라하체가림fallback독립성능미확인.',['S17','S15'],'코드 기본값·표시 범위·실제 적용을 구분')
aux('짐벌 설정과 검증 범위',table(['기능','마지막 기록','확보 근거'],[['가속150·원거리1.6','켬','PC 모의시험·직접응답실측'],['예측fused·guard v2','켬','vel과 같은 이득 주장 불가'],['좁게보기·하향제한','켬','기능·회귀시험; 현장재포착 미측정'],['lead200','켬','가상비교는 이득없음'],['search·seek','끔','오인·재포착 기준 미통과']]),'기본PD는최고속도10에서고른값이고운영100기록이있다. 결과즉시제어의약8ms간격명령이실제짐벌에서받아지는지미확인. 190~210ms는장면부터반응의추정합이며실측종단아님. 최종실행설정은추가확인.',['S17'],'11/15~20 과거 상태 기록 · 현재 장치를 이번 편집에서 재시험하지 않음')
aux('FastTrackTr 학습 이력',flow([('NPU 구조 포팅','53 ms → 겹치기28 ms'),('DanceTrack 흑백','36편·6 epoch<br>ID손실 붕괴 수정'),('TMOT 이어 학습','3 epoch<br>IDF1 15.3 → 27.1')]),'검출과번호를한모델로처리하는후보다. TMOT6편평균IDF1이올랐으나기존검출+추적수준에못미쳐11/15중단하고시험선택지로유지했다. 추적기v3표와동일실행전후가아니다. 정식성능달성사례로쓰지않는다.',['S21'],'번호 손실·학습곡선 원본 CSV 보존 · 배포 선택지와 기본 모델 구분')

def plot_pair(left_title,left,right_title,right):
    return '<div class="c-two">'+''.join(f'<div><h3>{title}</h3><img class="c-training" src="assets/{file}" alt="{title} 원본 CSV 곡선"></div>' for title,file in [(left_title,left),(right_title,right)])+'</div>'

aux('상체·외형 학습 곡선',plot_pair('650장 재현 · 상자 손실','training-e10.png','검수264 RepVGG · 손실','training-repvgg.png'),
    '원본 CSV의 epoch별 기록을 그렸다. 왼쪽 대조와 CLAHE의 학습 손실이 줄어드는 것만으로 독립 검출 성능 향상을 판정하지 않는다. 오른쪽도 학습 쌍에 대한 손실로 일반화 근거가 아니다. 상세 설정과 최종 시험은 학습 기록을 따른다.', ['S18','S19'], '원본 로그 관측점 연결 · 0 기준 축 · 손실 감소와 독립 성능을 구분')
aux('SOLIDER 선택 곡선',plot_pair('교사 파인튜닝 · 선택 점수','training-solider.png','증류 학생 · 선택 점수','training-student.png'),
    'A~E는 서로 다른 파인튜닝 구성이다. 선택용 점수의 이른 정점 뒤 하락과 최종 시험 판정을 구분한다. 학생 a_A, b_START, e_E의 선택 점수도 독립 시험 성능이 아니다. 단일 시드 비교이며 선택 점수 우위로 장치 채택을 주장하지 않는다.', ['S18'], 'CHOOSE 선택에 사용한 기록 · 독립 시험 점수와 별도')
aux('위치·통합 모델 학습 곡선',plot_pair('위치 예측 · val-A 선택 점수','training-position.png','FastTrackTr · ID 손실 수정 뒤','training-fasttrack.png'),
    '왼쪽은 원본 CSV에 기록된 첫 세 실행을 각자 epoch 기준으로 비교한다. val-A는 선택용이며 다른 자료의 최종 위치 오차와 섞지 않는다. 오른쪽은 DanceTrack의 손실 수정 뒤 단계만 따로 그렸으며 로그의 누적 평균이다. 서로 다른 단계와 재시작 로그를 이어 가상의 연속 곡선을 만들지 않았다.', ['S20','S21'], '위치 val-A: 선택용 · FastTrackTr: dance_ep3-5_idfix 기록만')

# Opening roadmap and an achievement-focused close.
toc_items = [
    '팀 및 프로젝트 소개',
    '열화상 검출과 모델 선정',
    '추적 알고리즘과 ID 유지',
    'NPU 처리와 지연 개선',
    '짐벌 제어와 운용',
    '통합 시연과 주요 성과',
]
toc = insert(1, '목차',
    scene('<div class="c-agenda">'+''.join(
        f'<div><span>{n:02d}</span><h2>{title}</h2></div>'
        for n, title in enumerate(toc_items, 1))+'</div>'),
    '팀과 프로젝트를 소개한 뒤, 열화상 검출 모델과 추적 알고리즘을 설명하겠습니다. 이어 NPU 처리와 지연 개선, 짐벌 제어와 운용을 보여드리고, 통합 시연과 주요 성과로 마무리하겠습니다.',
    ['S1'], ['소개', '검출·추적', '처리·제어', '시연·성과'])
toc['section'] = '발표 안내'
toc['seconds'] = 15
by[1]['spoken'] = by[1]['spoken'].replace('먼저 팀원 역할을 소개하겠습니다.', '발표 순서부터 안내하겠습니다.')

# Keep measurement plans for Q&A instead of ending the talk with future tasks.
for base_number in [29, 30]:
    item = copy.deepcopy(by[base_number])
    item.update(number=len(backup)+1, seconds=0, section='예비자료')
    backup.append(item)

update(31, title='처리 성능 정리', body=scene(cards([
    ('동시 타일 · p95','25.71 ms','프레임 교대 40.47 ms 대비<br>실카메라 · 각 65초'),
    ('DX-RT C API · p95','24.86 ms','기존 호출 26.33 ms 대비<br>무인 실카메라 · 별도 시험'),
    ('장시간 실행','18,497장','입력 버림·순서 오류 0<br>33 ms 초과 5장'),
]), '분할 처리와 C++ 보완으로 서버 처리 지연 개선',
    '세 수치는 별도 시험 · 서버 수신→추적 완료 기준 · 화면·물리 짐벌 종단 성능과 구분'),
    spoken='처리 성과를 정리하겠습니다. 같은 프레임을 나누는 동시 타일 시험에서는 p95가 40.47에서 25.71밀리초로 줄었습니다. 별도 C API 비교에서도 26.33에서 24.86밀리초로 낮아졌습니다. 장시간 18,497장을 처리하는 동안 입력 버림과 순서 오류는 없었습니다. 다만 33밀리초 초과는 다섯 장이 있었고, 각 수치는 서로 다른 서버 시험 결과입니다.',
    refs=['S15','S17'], cues=['동시 타일', 'C API 보완', '장시간 실행'])
update(32, title='주요 성과', body=scene(cards([
    ('검출 모델','현장 650장','상체 기준 정리·E10 학습<br>OTP2 박스 AP 46.28%'),
    ('추적·운용','3종 C++ 추적기','BoT-SORT HOTA 60.7<br>PC에서 추적기 선택·변경'),
    ('처리·제어','분할 처리·실측','동시 타일 서버 p95 25.71 ms<br>짐벌 응답 실측·가상 시험'),
]), '열화상 검출부터 ID 유지·NPU 처리·짐벌 운용까지 구현과 비교 근거 확보',
    '검출: OTP2 검증 · 추적: 동일 PC 비교 · 지연: 별도 서버 시험 · 각 지표의 평가 조건은 다름'),
    spoken='현장650장의 상체 기준을 정리하고 E10을 학습해 OTP2 박스 AP46.28퍼센트를 확보했습니다. 세 가지 추적기를 C++로 구현하고 PC에서 선택·변경할 수 있게 했으며, 같은 PC 비교에서 BoT-SORT HOTA60.7을 얻었습니다. 처리에서는 동시 타일과 C++ 보완을 적용했고, 짐벌은 실제 응답을 측정해 가상 시험의 근거로 사용했습니다. 검출부터 추적, 처리와 제어까지 구현하고 비교한 것이 이번 프로젝트의 성과입니다. 감사합니다.',
    refs=['S14','S15','S17','S19'], cues=['현장 모델', '추적·운용 구현', '처리·제어 성과'])

# Main ordering and exact target budget (17 minutes speech plus 3 minute demo).
ordered=[]
for s in slides:
    if s['base_number'] in [29, 30]:
        continue
    ordered.append(s)
    ordered.extend(insertions.get(s['base_number'],[]))
slides=ordered
polish(slides)
polish(backup,appendix=True)
slides,visual_usage=enrich(slides,backup)
slides=finalize_tracking(slides,backup)
slides=apply_revision(slides,backup)
slides=refine_narrative(slides)
polish_dates(slides)
polish_dates(backup)
clarify_terms(slides, backup)
assert len(slides)==43
spoken=[s for s in slides if s['base_number']!=28 and s is not toc]
weights=[s['seconds'] for s in spoken]
speech_budget=1020-toc['seconds']
allocation=[int(speech_budget*w/sum(weights)) for w in weights]
for i in sorted(range(len(weights)), key=lambda i:speech_budget*weights[i]/sum(weights)-allocation[i], reverse=True)[:speech_budget-sum(allocation)]: allocation[i]+=1
for s,t in zip(spoken,allocation):s['seconds']=t
for i,s in enumerate(slides,1):
    s['number']=i
    s['transition']='다음: '+slides[i]['title'] if i<len(slides) else '감사합니다.'
    s['presenter_cue']=' → '.join(s['quick_cues'])
assert sum(s['seconds'] for s in slides)==1200

def source_links(refs):
    return ' · '.join(f'<a href="{esc(SOURCES[k]["url"])}">{k} {esc(SOURCES[k]["title"])}</a>' for k in refs)

def slide_html(s,n,total,cover=False):
    heading='' if cover else f'<h1>{esc(s["title"])}</h1>'
    return f'<section class="slide{" cover-slide" if cover else ""}" id="slide-{n:02d}" data-number="{n}" data-seconds="{s["seconds"]}" aria-label="{esc(s["title"])}"><header>{heading}<img class="logo" src="assets/lig-logo.png" alt="LIG D&A"></header><main>{s["body"]}</main><div class="slide-source"></div><footer><span>{n:02d} / {total}</span></footer></section>'

def document(items,title,appendix=False):
    nav='<nav class="toolbar"><button id="prev" aria-label="이전 장">←</button><span id="page"></span><button id="next" aria-label="다음 장">→</button><span id="clock">00:00 / 20:00</span><button id="timer">타이머 시작</button><button id="overview">모아보기</button><a href="speaker-notes.html">대본</a><a href="index.html">본문</a><a href="appendix.html">예비자료</a></nav>'
    return '<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><link rel="stylesheet" href="slides.css"><link rel="stylesheet" href="latest.css"><link rel="stylesheet" href="visuals.css"></head><body'+(' class="appendix"' if appendix else '')+'>'+''.join(slide_html(s,i,len(items),not appendix and i==1) for i,s in enumerate(items,1))+nav+'<script src="slides.js"></script></body></html>'

# Use user supplied photos/video automatically when present; preserve honest placeholders otherwise.
photo=next((p for p in [BASE/'assets/hardware.png',BASE/'assets/hardware-photo.jpg'] if p.exists()),None)
if photo:
    slides[0]['body']=re.sub(r'<div class="cover-hardware hardware-placeholder">.*?</div>', f'<figure class="cover-hardware"><img src="assets/{photo.name}" alt="실제 하드웨어"></figure>',slides[0]['body'],flags=re.S)
    slides[0]['pending']=[]
if (BASE/'assets/rooftop-demo.mp4').exists():
    demo=next(s for s in slides if s['base_number']==28)
    demo['body']=demo['body'].replace('현재 실제 영상 파일 미수령 · 최종 설정과 일치하는 녹화 또는 실시간 시연으로 교체 필요','실제 영상 파일 포함 · 영상의 최종 모델·제어 설정 일치 확인 필요')

(BASE/'index.html').write_text(document(slides,'LWIR 표적 추적 · C안'),encoding='utf-8')
(BASE/'appendix.html').write_text(document(backup,'LWIR 표적 추적 · C안 예비자료',True),encoding='utf-8')
manifest=dict(title='LWIR 표적 추적 · C안',date='2026-11-22',source_commit='8a195d7',base_commit='9819922',total_seconds=1200,demo_seconds=180,spoken_target_seconds=1020,slides=[{k:v for k,v in s.items() if k!='body'} for s in slides],appendix_count=len(backup),sources=SOURCES)
(BASE/'deck.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def clock(t):return f'{t//60:02d}:{t%60:02d}'
md=['# C안 발표 대본','',f'2026-11-22 개정 · 자료 기준8a195d7(11/22) · 본문{len(slides)}장 · 설명17분+데모3분 목표. 실제 낭독 리허설 미실시.','']
cue=['# C안 큐시트','','설명17분+데모3분 목표 · 실제 리허설 후 재배분.','']
note_html=[]
elapsed=0
for s in slides:
    interval=f'{clock(elapsed)}–{clock(elapsed+s["seconds"])} / {s["seconds"]}초'
    md += [f'## {s["number"]:02d}. {s["title"]}','',interval,'',s['spoken'],'','진행: '+s['presenter_cue'],'','근거: '+', '.join(s['refs'])]
    if s['condition']:md += ['','조건: '+s['condition']]
    if s['pending']:md += ['','남은 입력: '+' / '.join(s['pending'])]
    md += ['']
    cue += [f'## {s["number"]:02d}. {s["title"]}',interval,s['presenter_cue'],s['transition'],'']
    note_html.append(f'<article><small>{interval}</small><h2>{s["number"]:02d}. {esc(s["title"])}</h2><p>{esc(s["spoken"])}</p><p>{esc(s["presenter_cue"])}</p><small>{source_links(s["refs"])}</small></article>')
    elapsed+=s['seconds']
(BASE/'speaker-notes.md').write_text('\n'.join(md),encoding='utf-8')
(BASE/'cue-sheet.md').write_text('\n'.join(cue),encoding='utf-8')
(BASE/'speaker-notes.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>C안 대본</title><style>@font-face{font-family:P;src:url(assets/Pretendard-Regular.woff2)}body{font:21px/1.8 P,sans-serif;max-width:1000px;margin:50px auto;color:#202b3a}article{border-top:1px solid #ccd6e0;padding:25px 0}h1,h2,a{color:#002f6d}small{font-size:16px}</style><h1>C안 발표 대본</h1>'+f'<p>{len(slides)}장 · 목표20분(데모3분 포함) · 실제 낭독 미측정</p>'+''.join(note_html)+'</html>',encoding='utf-8')
apnotes=['# C안 예비자료 설명','']
for n,s in enumerate(backup,1):apnotes += [f'## {n:02d}. {s["title"]}','',s['spoken'] or '원표·조건은 해당 장과 아래 출처를 함께 확인한다.','',s.get('condition',''),'',source_links(s['refs']),'']
(BASE/'appendix-notes.md').write_text('\n'.join(apnotes),encoding='utf-8')

src=['# C안 출처·수치 추적표','','기준: 로컬 presentation8a195d7(2026-11-22 21:13 KST). B 기준9819922에서 갱신. 장치·학습·성능 시험은 재실행하지 않았다.','','## 출처','']
src += [f'- **{k}** [{v["title"]}]({v["url"]})' for k,v in SOURCES.items()]
src += ['','## C안 장별 출처','','| 장 | 제목 | 근거 |','|---|---|---|']
src += [f'| {s["number"]} | {s["title"]} | {", ".join(s["refs"])} |' for s in slides]
src += ['', '## 그림·그래프 재구성', '', '| C안 장 | 활용한 원자료 |', '|---|---|']
src += [f'| {title} | {", ".join(files)} |' for title,files in visual_usage]
src += ['', '원본 HTML의 SVG·실제 라벨링·장치 재생 이미지를 선택해 C안의 장별 설명 구조로 재배치했다. 그림별 SHA256과 원본 경로는 S25에 보존했다. 소스 PDF 전체 페이지를 슬라이드 이미지로 복사하지 않았다. 짐벌 응답 곡선은 실측 요약값 기반의 모형으로 표시하고, 실측 시계열은 불감대 시험 파형에만 사용한다.']
src += ['','## 최신 수치와 조건','','| 항목 | 값 | 조건 | 한계 | 출처 |','|---|---|---|---|---|']
src += ['| '+' | '.join([v['title'],v['values'],v['condition'],v['limit'],','.join(v['refs'])])+' |' for v in evidence]
src += ['', '## 11/22 추가 반영 — 기존 기록보다 우선', '', '- 검출 추천은 own9e 시드 1. 모델9 대비 장치 INT8·분할 녹화18편 IDF1 +4.50%p(보고 구간 +1.26~+10.26), 번호 변경 차이0회(−9~+10). 구간의 신뢰 수준은 원문 미기재. 어깨 신뢰도 기준 충족률은92→9%.', '- 외형 추천은 기본 RVGGA0_REID2C256. 과거 OTP2 학습판의 검색 정답률0.892와 속도를 현재 추천 모델의 성능으로 대입하지 않는다.', '- 최초 GRU 적용 근거: 공개 val-B 위치 오차 TMOT 0.352→0.223, DanceTrack 0.295→0.213(Kalman→GRU). 자체 14편 위치 오차는 Kalman 0.110, 수정 GRU 0.122, 칼만 전환 규칙 포함 0.118. 자체 14편의 IDF1 차이는 +0.6%p(90% 구간 −0.8~+2.3%p). 장치 seq_018 한 편의 IDF1은 Kalman 71.81%, GRU 75.36%. [장치 재생 근거](https://github.com/lwir-deepx-tracking-system/model-bank/blob/0e3dd540ff8a9953a6e7725f59393c782a3d9d5a/HANDOFF.md#L1261).', '- KeepID: 번호 변경47→43, 장기 뺏김19→20. 두 가드 추가 시 뺏김20→17, IDF1 82.3% 동일.', '- 학습264장 FP32 타일 진단: 누락230→218, 일부 관절 위치 오차 증가. 독립 INT8 정확도 평가와 구별.', '- 박스 보정은 기본 body, 변환표 부재 시 size이며 오류 시 자동 비활성화 가능. 장치 적용은 별도 확인.', '- 시각자료19개 HTML을 최신 원본에서 동기화했다. 하드웨어·팀원 사진6개 및 라벨링 등 이미지8개는 기존 원본과 동일하다.', '- sources/revision-20261122는 두 커밋의 근거22개와 모델뱅크 원문2개를 SHA256으로 보존한다.']
src += ['','## 보존한 근거와 해석','','- 25.71ms는11/19 E10+3·재설치 전·모드별65초의 서버 p95. 큐버림1; 전프레임·종단 통과 아님.','- 11/20 재설치 뒤 전체화면 기록에서33ms초과14803/21579=68.6%. 이 시점 수치를 후속 분할 상태로 확대하지 않는다.','- 추적기 CMC:11/20 새 대본은 일반 기능을 설명하지만 동일PC 비교 원표는 CMC·ReID 미사용. 효과를 입증했다고 서술하지 않는다.','- SOLIDER 직접교체 원본 RESULT_KO는11/21 학습기록 조사에서 재확인 못함. 기존66.74→66.57은 예비자료의 잠정 참고로만 보존.','- 가상 재포착 vel+0.20의95%구간0.07~0.32, fused+0.06의−0.11~0.21을 구분한다.','- RepVGG 시간 비교:5.02/1.28≈3.92배; 검수264와OTP2판 정확도를 서로 대입하지 않는다.','- 출처 스냅샷 SHA256은 sources/latest-20261121/manifest.json에 보존. 비공개 개인실험 파일은 팀원이 기록한 주장으로 인용하며 원본을 새로 확인한 것으로 표시하지 않는다.','', '## 이전 B안 수치 원표','', '아래는 B안 원문 보존이며 장 번호는 B 기준이다. C안 장별 매핑과 최신 해석을 우선한다.','',SEED['base_sources_text']]
src += ['', '## 발표용 모델 이름', '',
        '- 공개 자세 모델 = F. 이전 혼합 라벨 모델 = 1,056장 E10. 현장 650장 모델 = 650장 E10(공개 자세 모델에서 10 epoch 추가 학습).',
        '- 자체 영상 추가 학습 모델 = own9e 시드 1. 이 모델과 비교한 기존 장치 모델 = 모델 9. 두 모델의 장치 재생 비교는 S26·S27.',
        '- 실카메라 지연 시험용 추가 학습 모델 = E10+3. 65초씩 진행한 해당 시험은 S15·S17.']
(BASE/'sources.md').write_text('\n'.join(src),encoding='utf-8')

questions = [
    ('최신 추천 검출기와 외형 모델은 무엇인가요?', '11/22 모델뱅크 추천은 own9e 시드1과 기본 RVGGA0_REID2C256입니다. own9e는 장치 재생18편에서 IDF1 +4.50%p였으나 어깨 신뢰도 기준 충족률은92→9%였습니다. E10 AP46.28%는 앞선 별도 평가 결과입니다.', 'S26, S27'),
    ('최종 추적 알고리즘은 무엇인가요?', '최종 알고리즘은 BoT-SORT입니다. ByteTrack과 OC-SORT는 구현·평가한 비교 후보로 설명합니다. 동일 PC에서 HOTA 60.7, IDF1 67.5%, MOTA 74.7%를 확인하고, 최종 파라미터 조합을 선정했습니다. OC-SORT의 ID 변경531회와 재현율87.7%는 후보 장점으로 남깁니다.', 'S24'),
    ('30 Hz 목표를 달성했나요?', '일부 시험의 p95는 33 ms 아래지만 모든 프레임 기준은 통과하지 못했습니다. 장시간 18,497장 중 5장이 초과했고 최대 44.582 ms입니다. 최종 시스템 종단 30 Hz 성능을 입증하지 않았습니다.', 'S17'),
    ('현재 장치도 25.71 ms인가요?', '11/19 E10+3 모델로 재설치 전에 잰 65초 서버 시험입니다. 재설치 뒤에는 전체 화면 실행과 높은 초과율이 기록됐고, 이후에도 복구·변경이 있어 최종 실행을 별도로 확인해야 합니다.', 'S17'),
    ('CMC 때문에 BoT-SORT가 좋았나요?', '해당 v3 수치 비교에서는 CMC와 ReID를 사용하지 않았습니다. 카메라가 움직이는 시스템에서 적용을 검토할 이유와 해당 시험의 성능 원인을 구분합니다.', 'S24'),
    ('표준 증강 AP가 높은데 왜 E10을 유지했나요?', 'OTP2 박스 AP는 48.16%로 높지만 관절은 77.31%로 낮고, 실내·실외 추적을 함께 이긴 후보가 없었습니다. 자체 시험에는 E10 학습 노출이 있어 그 점수로 일반화 우위를 단정하지 않습니다.', 'S17'),
    ('GRU가 Kalman보다 좋나요?', '공개 검증에서 위치 오차가 낮아 GRU를 적용했습니다. 자체 14편 위치 오차는 Kalman 0.110, 수정 GRU 0.122였고, 장치 재생 한 편 IDF1은 Kalman 71.81%, GRU 75.36%였습니다.', 'S20'),
    ('번호 가드 두 개면 모든 지표가 좋아지나요?', '9편 PC 비교에서 장기 번호 뺏김은 20→17이지만 IDF1은 82.3%로 같고, cost_first만 켠 83.2%보다 낮습니다. 장치 효과와 CPU 비용은 미측정입니다.', 'S17'),
    ('SOLIDER 증류 E가 기본인가요?', '시험용 추가 선택지입니다. 라벨 9편 PC IDF1은 82.4%로 기존 83.0%보다 낮았습니다. 실내 4명 장면의 이득을 전체 성능으로 확대하지 않습니다.', 'S18'),
    ('증류 교사가 LUPerson 원본인가요?', '11/10·15 교사는 ThermalTrack 공개 열화상 재식별 가중치입니다. LUPerson RGB 자기지도 원본은 11/20 파인튜닝 시작점입니다.', 'S18'),
    ('예측 추종이 재포착을 20%p 높였나요?', '가상 비교의 vel 결과입니다. 장치 기록의 fused는 +6%p이고 95% 구간이 0을 포함합니다. 실제 사람·실제 짐벌의 재포착 개선은 입증하지 않았습니다.', 'S17'),
    ('짐벌 지연이 약 200 ms인가요?', '약 190~210 ms는 과거 일부 실측과 추정을 합친 값입니다. 명령부터 화면 반응까지 108 ms는 직접 실측이지만 장면부터 짐벌까지의 최종 종단 실측은 없습니다.', 'S17'),
    ('INT8 aggressive 옵션을 분할 모델에도 썼나요?', '아닙니다. 29.10→21.92 ms는 과거 FLIR YOLO26s 시험이고 분할 파일은 CPU 부분 0, aggressive 미사용입니다.', 'S17'),
    ('박스 보정으로 조준도 좋아졌나요?', '키 변화는 0.071→0.043이지만 조준 떨림은 0.0195로 같았습니다. 기본 body이며 변환표가 없으면 size, 오류 시 자동 비활성화가 가능합니다. 장치 적용과 현장 효과는 별도 확인 대상입니다.', 'S26'),
    ('FastTrackTr를 최종 추적기로 썼나요?', '열화상 이어 학습으로 TMOT 6편 IDF1이 15.3→27.1%로 올랐지만 성능 부족으로 중단해 시험 선택지로만 유지했습니다.', 'S21'),
    ('기본 PD와 새 짐벌 개선의 담당은 누구인가요?', '팀 역할 원문을 따릅니다. 기본 PD·GUI·짐벌 제어는 윤오름, 윤관 자료는 그 위의 모델 학습·튜닝·실측·가상 시험 근거입니다.', 'S13'),
]
qmd=['# C안 예상 질문','','최신 상태·모순을 먼저 정리했다. 아래 기존질문은 새판정과 충돌하지 않는 범위에서 활용한다.','']
for n,(q,a,r) in enumerate(questions,1):qmd += [f'## {n:02d}. {q}','',a,'','근거: '+r,'']
qmd += ['## 기존 설계·운용 질문','']
for block in re.split(r'(?=^## )',SEED['base_qa'],flags=re.M):
    if block.startswith('## ') and any(word in block.splitlines()[0] for word in ['PD','PID','적분','I항','D항','GUI에서 추적기 변경','전신 박스']):
        qmd += [block.strip(),'']
(BASE/'qa.md').write_text('\n'.join(qmd),encoding='utf-8')

demo_number=next(s['number'] for s in slides if s['base_number']==28)
integration=['# C안 통합 인계','','2026-11-22 · 현재 작업본 C. A·B와 팀원 원본은 보존. 자료 기준 8a195d7. 장치 실행은 조회·재시험하지 않았다.','','## 구성','',f'- 본문 {len(slides)}장·예비 {len(backup)}장. 목표 설명 17분+데모 3분. 실제 리허설 미실시.','- seed.json은 B의 본문·예비·출처 동결본, build.py는 C의 최신 해석과 추가 장 생성기.','- sources/latest-20261121은 팀 자료 37개와 SHA256. 과거 B의 sources도 복사 보존.','- A·B의 빌더·소스 폴더를 참조하지 않고 C 내부 입력으로 재생성한다.','- plot_training.py는 동결 CSV를 사용해 학습 곡선 6개를 출력한다. 생성된 PNG가 포함되어 있어 일반 재생성에는 matplotlib가 필요 없다.','','## 변경 장 매핑','','| B장 | C장 | 제목 |','|---|---|---|']
integration += [f'| {s["base_number"] or "추가"} | {s["number"]} | {s["title"]} |' for s in slides]
integration += ['', '## 발표 흐름 개정', '', '- 표지 → 목차 → 팀 소개 → 프로젝트 소개 순서. 목차는 6개 항목이며 15초 배정.', '- 마지막 목차 항목은 통합 시연과 주요 성과. 마무리 장은 현재 구현·측정 성과로 구성한다.', '- 이전 본문의 거리 검증 계획·현장 ID 검증 계획은 예비자료 36·37장으로 이동. 측정 조건과 실제 입력 관리 항목은 대본·출처·인계에 보존한다.']
integration += ['', '## 설계 선택과 성과의 연결', '', '- narrative.py가 라벨 혼재→상체 기준 통일, 증강 후보 비교→E10 유지, 장치 ID 연결 비교→own9e 추천을 연결한다.', '- 추적기 선정·최종 설정 다음에 가림 위치 예측과 번호 유지 평가를 연속 배치한다. GRU의 Kalman 대비 우위나 세 보완 기능의 최종 동시 적용을 단정하지 않는다.', '- 마지막 성과 장은 검출·추적·NPU·짐벌의 문제 / 선택한 설계 / 측정 성과를 같은 행에서 연결한다. 각 행의 비교 환경을 유지한다.', '- 출처 문서의 그림 활용 목록은 장 제목 기준이며, 현재 순서는 deck.json과 장별 매핑을 따른다.']
integration += ['', '## 화면 문구', '', '- editorial.py에서 발표용 문구를 관리한다. 작성자·자료 버전·편집 이력과 긴 하단 캡션을 화면에서 제외한다.', '- 기존 하단 주석은 condition·editorial_notes와 대본·출처에 보존한다. 핵심 평가 조건은 그래프·표 제목에 표시한다.', '- 발표 대본은 구현과 측정 결과를 직접 설명하는 문장으로 정리한다.']
integration += ['', '## 그림 중심 재구성', '', f'- visual_layouts.py가 {len(visual_usage)}개 본문 장을 재구성한다. 추가 장은 학습 데이터 구성·상체 박스 기준·가림·잘림 증강이다.', '- sources/visual-reference/slides의 선택 원자료와 assets/visuals 이미지를 사용한다. prepare_visuals.py는 원자료를 의도적으로 갱신할 때만 실행한다.', '- 그림을 단순 장식으로 추가하지 않고 라벨링→박스 기준→학습→실제 증강→평가, 관측 이력→위치 예측, 장치 영상→타일→병합, 짐벌 실측→제어 파형→가상 반복 시험 순서로 구성한다.', '- 원자료에서 후보명·시험 조건이 혼재한 HOTA 그래프와 모형 응답의 실측 표기는 확인된 조건에 맞춰 조정했다.']
integration += ['', '## 최종 추적기와 운영 이력', '', '- 사용자 확인에 따라 최종 추적 알고리즘은 BoT-SORT로 명시한다. ByteTrack·OC-SORT 비교 → BoT-SORT 선정 → 파라미터 조정의 순서로 설명한다.', '- 비교 후보의 IDSW·재현율 장점은 측정 결과로 유지하고, 장면별 운용 추천으로 표현하지 않는다. 3종 선택·교체 기능은 구현 기능으로 보존한다.', '- tracking_story.py에서 선정 서사·GUI·성과 요약을 맞춘다. 장치 상태 이력은 예비자료 38장으로 이동했다.']
integration += ['', '## 11/22 추가 반영', '', '- revision_20261122.py가 own9e 비교 장과 예비 조건표를 추가하고 GRU·KeepID 그래프, 외형 추천, 타일 진단, 박스 보정 해석을 갱신한다.', '- S26은 팀원 두 커밋의 근거, S27은 모델뱅크 추천 원문이다. 과거 E10 성과와 최신 own9e 추천을 별도로 설명한다.', '- 사진 원본은 기존과 동일하다. 바뀐 원자료 HTML과 그래프를 새로 가져왔으며 기본 빌드는 동결본만 사용한다.']
integration += ['','## 남은 실제 입력','','- 표지 하드웨어 사진: assets/hardware-photo.jpg.','- 실제 GUI 앱 캡처: 기존 재생 이미지는 앱 캡처가 아님.',f'- C {demo_number}장 실제 시연: assets/rooftop-demo.mp4 (180초 이내).','- 최종 검출기·외형 모델 파일 해시, 분할 여부, Runtime/모델뱅크 서버 경로, 추적기, KeepID·가드·lead·보정·제어 인자.','- 거리별 누락·오검출, 가림 뒤 ID 정답·허용 끊김 기준과 현장 반복 결과.','- 사람 있는 최종 장치 경로의 장시간 최대·초과·드롭·순서 오류와 화면·물리 짐벌 종단 측정.','','## 자료 충돌 처리','','- CMC는 일반 기능 설명과 비교 시 미사용 설정을 분리.','- 최신 개인 요약의 vel/fused 혼용, 512 입력 채택 요약, 추천과 장치 선택을 추가 근거의 조건으로 제한.','- SOLIDER 직접 교체 원본 미확인은 예비자료로 한정.','- 반전 4→1은 Ki0·Kd6 고정의 불감대 비교로 유지.','','## 재생성','','```powershell','python work/C/build.py','python work/C/render.py','```','', 'render.py는 PDF·미리보기·레이아웃·글꼴·이미지·페이지 수·키보드 이동을 검증한다. validation.json은 실제 하드웨어 검증을 대신하지 않는다.']
integration_text='\n'.join(integration)
if photo:
    integration_text=integration_text.replace('- 표지 하드웨어 사진: assets/hardware-photo.jpg.','- 표지 하드웨어 사진 반영 완료: reference/picture/hardware.png → C/assets/hardware.png. 팀원 사진 5개도 같은 공통 폴더에서 동기화한다.')
integration_text+='\n\n## 공통 사진 경로\n\n현재 공통 사진은 reference/picture/이다. build.py는 해당 폴더가 있으면 사진을 C/assets로 복사하고, 없으면 C에 포함된 사진을 사용한다. 사진 해시는 picture-manifest.json에 기록한다.\n'
(BASE/'integration.md').write_text(integration_text,encoding='utf-8')
(BASE/'README.md').write_text(f'''# C안 · 최신 통합 발표

2026-11-22 작성. 자료 기준 presentation `8a195d7`(11/22 21:13 KST). B안 `9819922` 이후의 검출·외형·ID·서버·짐벌 근거를 반영했습니다. A·B와 팀원 원본은 보존합니다.

본문 **{len(slides)}장**, 예비 **{len(backup)}장**. 설명 17분+실제 데모 3분의 **목표**이며 낭독 리허설은 하지 않았습니다.

시작은 **표지 → 목차 → 팀 소개 → 프로젝트 소개** 순서입니다. 목차는 소개·검출·추적·NPU 처리·짐벌 운용·통합 시연과 주요 성과의 6개 항목입니다. 마무리는 현재 성과 중심이며, 거리·현장 ID 검증 계획은 예비자료에 보존했습니다.

화면 문구는 `editorial.py`에서 다듬습니다. 작성자·버전 표기와 긴 하단 주석은 대본·출처에 보존하고, 슬라이드는 구현·결과 중심으로 구성했습니다.

`visual_layouts.py`에서 **{len(visual_usage)}개 장**을 그림 중심으로 재구성했습니다. 실제 라벨링·가림 증강, 상체 박스와 GRU 개념도, NPU 타일·병합, 짐벌 실측 파형과 가상 카메라 시험도를 사용합니다. 학습 데이터·박스 기준·증강 예시 3장을 본문에 추가했습니다. [그림 원자료](sources/visual-reference/manifest.json)의 경로·해시를 보존합니다.

최종 추적 알고리즘은 **BoT-SORT**입니다. 비교 후보 평가부터 최종 선정·파라미터 조정으로 이어지며, 장치 상태 이력은 예비자료에 보존했습니다. 이 설명 흐름은 `tracking_story.py`에서 관리합니다.

- [발표 PDF](presentation.pdf) / [발표 HTML](index.html)
- [전체 미리보기](previews/slide-overview.png)
- [발표 대본](speaker-notes.html) / [Markdown 대본](speaker-notes.md) / [큐시트](cue-sheet.md)
- [예비 PDF](appendix.pdf) / [예비 HTML](appendix.html) / [예비 설명](appendix-notes.md)
- [출처·수치](sources.md) / [질의응답](qa.md) / [통합 인계·장 매핑](integration.md)
- [검증 결과](validation.json) / [원자료 해시](sources/latest-20261121/manifest.json)

새 본문은 외형 모델 비교, 번호 유지, 분할 모델 변환, 장시간·혼잡 조건, 장치 상태 이력, 짐벌 실측·가상 시험·놓침 대응을 설명합니다. 검출 후속 학습·지연 결론·조준 보정도 갱신했습니다. 예비자료에는 원본 CSV 학습 곡선 6개를 보충했습니다. 최신 자료의 조건 충돌은 대본·출처·예비자료에 기록했습니다.

공통 `reference/picture/`의 하드웨어 사진과 팀원 사진을 표지·팀 소개에 반영했습니다. 사진은 C/assets에도 복사해 보존하고, 재생성 시 공통 폴더의 사진을 동기화합니다. [사진 해시](picture-manifest.json)를 함께 기록합니다.

실제 앱 캡처·통합 영상·거리/현장 ID 결과·최종 실행 설정은 미확보입니다. 시연 영상은 **{demo_number}장**, `assets/rooftop-demo.mp4`입니다. 기존 25.71 ms나 PC ID 비교를 현재 장치의 통합 성능으로 제시하지 않습니다.

```powershell
python work/C/build.py
python work/C/render.py
```

방향키·Space 이동, Home/End 처음·끝, G 모아보기, F 전체화면. 편집 기준은 [DESIGN.md](../DESIGN.md), 현재 인계는 [integration.md](integration.md)입니다. 최신화는 `build.py`를 수정합니다. `seed.json`과 `sources/`는 동결 근거입니다.
''',encoding='utf-8')
print(f'Built C: {len(slides)} main + {len(backup)} appendix; {elapsed}s target; demo slide {demo_number}')
