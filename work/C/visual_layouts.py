"""Adapt selected source diagrams into the integrated presentation layout."""
from pathlib import Path
import html
import re

BASE=Path(__file__).resolve().parent
REFERENCE=BASE/'sources/visual-reference/slides'


def svg(name,index=0,edits=None):
    source=(REFERENCE/(name+'.html')).read_text(encoding='utf-8')
    root=re.search(r'<article[^>]+id="([^"]+)"',source).group(1)
    original_root=root
    if name=='k09_id_keep':root+=f'-figure-{index}'
    drawing=re.findall(r'<svg\b.*?</svg>',source,re.S)[index]
    for before,after in (edits or {}).items():
        assert before in drawing,(name,before)
        drawing=drawing.replace(before,after)
    drawing=drawing.replace('assets/','assets/visuals/')
    styles='\n'.join(re.findall(r'<style>(.*?)</style>',source,re.S))
    if root!=original_root:styles=styles.replace('#'+original_root,'#'+root)
    shared=f'#{root} .v-label{{font:600 20px Pretendard;fill:#263c55}}#{root} .v-small{{font:16px Pretendard;fill:#526277}}#{root} .v-value{{font:600 22px Pretendard;fill:#002f6d}}'
    return f'<div class="v-drawing" id="{root}"><style>{styles}{shared}</style>{drawing}</div>'


def photo(file,alt,cls=''):
    return f'<img class="{cls}" src="assets/visuals/{file}" alt="{alt}">'


def take(text):return f'<div class="v-take">{text}</div>'
def scene(content,message=''):return '<div class="scene b-scene v-scene">'+content+(take(message) if message else '')+'</div>'
def mini(items):return '<div class="v-mini">'+''.join(f'<div><b>{a}</b><span>{b}</span></div>' for a,b in items)+'</div>'


def grouped_candidate_chart():
    labels=['운영 E10','표준 증강','강한 증강','직각 회전']
    ap=[46.28,48.16,45.37,44.68];pose=[78.35,77.31,78.86,79.27]
    out='<svg viewBox="0 0 1168 340" role="img" aria-label="OTP2 934장 후보별 박스 AP와 관절 AP"><text x="220" y="26" class="v-chart-title">박스 AP50–95 (%)</text><text x="760" y="26" class="v-chart-title">관절 AP50–95 (%)</text>'
    for start,maximum in [(220,60),(760,100)]:
        for value in [0,maximum/2,maximum]:
            x=start+320*value/maximum
            out+=f'<line x1="{x}" x2="{x}" y1="46" y2="296" stroke="#dce2ea"/><text x="{x}" y="326" text-anchor="middle" class="v-axis">{value:g}</text>'
    for i,(label,a,p) in enumerate(zip(labels,ap,pose)):
        y=60+i*60
        out+=f'<text x="202" y="{y+27}" text-anchor="end" class="v-plot-label">{label}</text>'
        for start,value,maximum in [(220,a,60),(760,p,100)]:
            color='#002f6d' if i==0 else '#41817d' if i==1 else '#9fb2c5'
            width=value/maximum*320
            out+=f'<rect x="{start}" y="{y}" width="{width}" height="36" fill="{color}"/><text x="{start+width+9}" y="{y+27}" class="v-plot-value">{value:.2f}</text>'
    return out+'</svg>'


def data_chart():
    rows=[('FLIR','도로 열화상 검출',10491),('OTP2','근거리 열화상 자세',8846),('COCO 흑백','다양한 자세',30000),('MOT17 흑백','군중·가림',2536),('LLVIP-Pose','야간·중거리',6851),('자체 카메라','현장 상체 기준',650)]
    out='<div class="v-data-rows"><div class="v-data-head"><span>데이터</span><span>주요 용도</span><span>학습 장수 · 0–30,000장</span></div>'
    for name,use,count in rows:
        out+=f'<div class="v-data-row"><b>{name}</b><span>{use}</span><div><i style="width:{max(count/30000*240,5):.2f}px"></i><strong>{count:,}</strong></div></div>'
    return out+'</div>'


def enrich(slides,backup):
    usage=[]
    by_title={s['title']:s for s in slides}

    def replace(title,body,files,spoken=None,cues=None,condition=''):
        s=by_title[title]
        s['body']=body
        if spoken:s['spoken']=spoken
        if cues:s['quick_cues']=cues
        if condition:s['condition']=' / '.join(filter(None,[s.get('condition',''),condition]))
        s['refs']=list(dict.fromkeys([*s['refs'],'S25']))
        s['visual_sources']=files
        usage.append((title,files))
        return s

    def addition(title,body,files,spoken,cues,refs,condition):
        usage.append((title,files))
        return dict(title=title,body=body,spoken=spoken,quick_cues=cues,presenter_cue=' → '.join(cues),refs=[*refs,'S25'],condition=condition,pending=[],section='그림·실험 설명',seconds=30,base_number=None,visual_sources=files)

    replace('현장 데이터 구축',scene(
        '<div class="v-label-layout"><div class="v-label-pair"><figure><div class="v-label-shot indoor">'+photo('실제_라벨링_실내.png','가림이 있는 실내 영상의 박스·관절 라벨 편집')+'</div><figcaption>실내 · 가림과 관절 검수</figcaption></figure>'
        '<figure><div class="v-label-shot outdoor">'+photo('실제_라벨링_야외.png','거리별 사람의 박스와 관절 라벨 편집')+'</div><figcaption>야외 · 거리별 박스 검수</figcaption></figure></div>'
        +mini([('439장','새 현장 영상'),('+ 211장','기존 검수 영상'),('650장','상체 모델 학습'),('743개','상체 정답 상자')])+'</div>',
        '실제 촬영 영상의 박스·관절을 검수해 상체 학습 자료 구축'),
        ['m13_labeling.html','실제_라벨링_실내.png','실제_라벨링_야외.png'],
        '실내에서는 책상과 노트북에 가려진 사람을, 야외에서는 거리가 다른 사람을 직접 검수했습니다. 사람의 ID와 상체 박스, 관절을 확인하고 모호하거나 중복된 후보를 정리했습니다. 새 현장439장과 기존 검수211장을 합쳐650장, 상체 정답743개를 학습에 사용했습니다.',
        ['실내 가림','야외 거리','650장 학습'])

    public=addition('학습 데이터 구성',scene(
        '<div class="v-data-grid">'+data_chart()+'<figure>'+photo('openthermalpose2-official-example.png','OTP2 공개 열화상 박스·관절 예시')+'<figcaption>OTP2 · 열화상 사람 박스와 17관절</figcaption></figure></div>',
        '공개 데이터로 자세·가림을 학습하고 자체 영상으로 현장에 적응'),
        ['m09_data.html','openthermalpose2-official-example.png'],
        '학습에는 목적별 공개 데이터를 활용했습니다. FLIR는 도로 열화상 검출, OTP2는 근거리 자세, 흑백 COCO와MOT17은 다양한 자세와 가림, LLVIP-Pose는 야간과 중거리에 사용했습니다. 이들은 여러 모델과 학습 단계에 쓰인 자료이며, 현장650장 학습은 별도로 진행했습니다.',
        ['데이터별 역할','열화상·흑백','현장 적응'],['S19'], '데이터 장수는 여러 학습 갈래의 사용량. 단일 실행의 합계가 아님. OTP2 공개 예시의 라이선스를 assets/visuals에 보존.')
    box=addition('상체 박스 기준',scene(
        '<div class="v-body-grid"><div>'+svg('m14_body_box')+'</div><div class="v-explain"><h3>관절에서 상체 범위 계산</h3><ol><li>보이는 관절 확인</li><li>골격의 크기·회전·위치 추정</li><li>머리 꼭대기~골반 상자 생성</li></ol><div class="v-emphasis">가림 전후에 같은<br>상체 기준 유지</div></div></div>',
        '보이는 부분의 크기보다 일관된 상체 범위로 추적·조준 기준 설정'),
        ['m14_body_box.html'],
        '상체 박스는 머리 꼭대기부터 골반까지로 정의했습니다. 그림처럼 하체가 책상에 가려져도 같은 몸 범위를 기준으로 삼습니다. 보이는 관절로 공통 골격의 크기와 회전, 위치를 맞추고 상체 박스를 계산해 라벨 범위와 조준 기준이 바뀌는 문제를 줄였습니다.',
        ['전신·가림 비교','관절 기반 상자','같은 상체 기준'],['S19'],'상체 박스 구성 방법의 개념도. 가림 장면 전체의 성능 보장으로 사용하지 않는다.')

    replace('상체 모델 학습',scene(
        '<div class="v-lineage">'+svg('m10_pose_lineage')+'</div>'
        +mini([('공개 모델 F','공개 자세·가림 학습'),('650장 · 10 epoch','현장 상체 미세조정'),('OTP2 934장','박스·관절·재현율 검증')]),
        '공개 자세 모델에서 현장650장 상체 모델로 이어지는 학습 경로'),
        ['m10_pose_lineage.html'],
        '공개 자세 모델에 OTP2와흑백자료, 군중·야간 자료를 단계별로 더했습니다. 그림의 범용F가 현장 상체 모델의 출발점입니다. F에서650장으로10 epoch 미세조정하고 OTP2 934장에서 박스와관절, 재현율을 평가했습니다. 별도 학습 갈래인 FLIR 검출기와 구체적인 설정은 예비자료에 정리했습니다.',
        ['공개 학습 단계','범용 F','현장650장 E10'])
    aug=addition('가림·잘림 증강',scene(
        '<div class="v-augmentation">'+''.join('<figure><h3>'+title+'</h3><svg viewBox="'+str(n*400)+' 0 400 400" role="img" aria-label="'+title+'"><defs><clipPath id="aug-'+str(n)+'"><rect x="'+str(n*400)+'" y="0" width="400" height="400"/></clipPath></defs><image clip-path="url(#aug-'+str(n)+')" href="assets/visuals/m11-occlusion-aug.jpg" x="0" y="0" width="1200" height="400"/></svg></figure>' for n,title in enumerate(['강한 가림 · 머리만 관측','배경 조각으로 가림','확대 · 화면 밖 잘림']))+'</div>'
        +'<div class="v-legend"><span class="box">정답 상체 박스</span><span class="point">보이는 관절</span><span class="hidden">가려진 관절</span><b>OTP2 실제 증강 출력</b></div>'
        +mini([('가림·잘림','보이는 부분을 다양화'),('박스·관절','원래 위치 정보 유지'),('미표기 인물','분류 손실에서 제외')]),
        '가려지거나 잘린 학습 영상에서도 몸의 위치를 배우도록 구성'),
        ['m11_occlusion_aug.html','m11-occlusion-aug.jpg'],
        '실제 학습 입력 예시입니다. 왼쪽은 몸 대부분을 가리고 머리만 남긴 경우, 가운데는 배경 조각으로 사람을 가린 경우, 오른쪽은 확대해 화면 밖으로 잘린 경우입니다. 가려진 관절과 몸 박스의 원래 위치를 정답에 남겨 일부만 보이는 사람의 몸 구조를 학습시켰습니다.',
        ['가림','잘림','정답 위치 유지'],['S19'],'예시는 공개 자세 모델의 OTP2 증강 출력. 현장650 E10은 별도 증강 확률을 사용한다. 공개 단계50% 설정을 E10 설정으로 옮기지 않는다.')

    replace('상체 검출 결과',scene(
        '<div class="v-result-grid"><div>'+svg('m18_e10')+'</div><div class="v-result-stack"><div><small>상체 박스 AP</small><b>+10.24%p</b><span>36.04 → 46.28%</span></div><div class="tradeoff"><small>박스 재현율</small><b>−2.61%p</b><span>71.70 → 69.09%</span></div><div><small>관절 AP</small><b>+1.07%p</b><span>77.28 → 78.35%</span></div></div></div>',
        'OTP2 934장 · 상체 박스 품질 향상과 재현율의 절충을 함께 확인'),
        ['m18_e10.html'],condition='시작 F / 이전 E10(1056장) / 현장 E10(650장)의 공개 검증 비교. 변화량은 이전 E10 대비.')
    replace('후속 학습 채택 판단',scene(
        '<div class="v-plot-heading">OTP2 934장 · 같은 후보의 박스·관절 AP 비교</div><div class="v-candidate-plot">'+grouped_candidate_chart()+'</div>'
        +mini([('표준 증강','박스 +1.88%p · 관절 −1.04%p'),('실내·실외 추적','두 환경의 결과를 함께 평가'),('운영 선택','현장650장 E10 유지')]),
        '박스 품질·관절 정확도·추적 결과를 종합해 모델 선택'),
        ['m19_retrain.html'],condition='후보 절대값은 근거_최신_20261120.md의 OTP2 표를 사용. 원자료의 후보 명칭이 혼재한 HOTA 그래프는 가져오지 않았다.')

    replace('모델 배포 과정',scene(
        '<div class="v-deploy-flow"><div><h3>PyTorch</h3><p>학습 가중치</p><div class="v-matrix fp">0.31　−0.72<br>0.18　 0.54</div></div><b>→</b><div><h3>ONNX</h3><p>그래프 내보내기</p><svg viewBox="0 0 250 125" aria-label="연산 그래프 개념도"><path d="M28 62H220 M80 62L142 22 M80 62L142 102" fill="none" stroke="#7d9bb5" stroke-width="3"/><g fill="#e1edf5" stroke="#002f6d" stroke-width="2"><rect x="10" y="42" width="45" height="40" rx="5"/><rect x="75" y="42" width="45" height="40" rx="5"/><rect x="140" y="3" width="45" height="40" rx="5"/><rect x="140" y="82" width="45" height="40" rx="5"/><rect x="200" y="42" width="45" height="40" rx="5"/></g></svg></div><b>→</b><div><h3>DX-COM</h3><p>대표 영상으로 INT8 보정</p>'+photo('openthermalpose2-official-example.png','INT8 보정용 대표 영상의 예시')+'</div><b>→</b><div><h3>DXNN · M1</h3><p>NPU에서 실행</p><div class="v-chip">INT8</div></div></div>'
        +mini([('변환 전후 출력','좌표·관절·특징 확인'),('장치 실행','처리 시간 측정'),('보정 자료','모델별 대표 입력 사용')]),
        '입력 해상도·출력 형식·보정 자료를 맞춰 장치 모델로 변환'),
        ['m27_int8.html','openthermalpose2-official-example.png'],condition='행렬·연산 그래프는 개념도이며 실제 가중치 수치를 나타내지 않는다. 보정 예시는 설명용.')
    replace('외형 모델 비교',scene('<div class="v-reid-plot">'+svg('m21b_reid_table')+'</div>'
        +'<div class="v-feature-path"><b>사람 조각</b><span>→</span><b>RepVGG</b><span>→</span><div class="v-feature-vector">128차원 특징　▁ ▃ ▆ ▂ ▅ ▇ ▂ ▄</div><span>→</span><b>같은 사람 연결</b></div>',
        'M1 INT8 · RepVGG 계열은 ViT-lite 대비 약 4배 빠른 처리'),
        ['m21b_reid_table.html'],condition='특징 막대는 구조를 설명하는 개념도. OTP2 학습판과 검수264판의 성능을 그래프에서 각각 표시.')

    position=replace('표적 가림과 ID 유지',scene('<div class="v-position-diagram">'+svg('m22_position')+'</div>'
        +mini([('관측 이력','상자·속도·17관절'),('가림 1~15프레임','Kalman 경로를 GRU로 보정'),('16프레임부터','Kalman 예측 사용')]),
        '관측된 움직임과 관절 이력으로 가려진 동안의 표적 위치 예측'),
        ['m22_position.html'],
        '사람이 보이는 동안 최근20프레임의 상자와속도, 관절을 기록합니다. 가려지면 Kalman이 예상한 경로에 GRU가 중심과크기 보정을 더합니다. 보정은최대15프레임까지이고 이후에는 Kalman 예측을 사용합니다. 다음 장들에서 추적기의 신원 연결과 위치 보완 결과를 함께 설명하겠습니다.',
        ['20프레임 이력','15프레임 보정','Kalman 경로'])
    position['title']='가림 위치 예측'
    position['refs']=list(dict.fromkeys([*position['refs'],'S20']))

    replace('두 NPU 동시 타일 처리',scene('<div class="v-tile-grid"><div>'+svg('m29_split',0)+'</div><div class="v-explain"><h3>같은 프레임을 좌우로 분할</h3><ol><li>640×480 입력</li><li>좌우384 px · 가운데128 px 겹침</li><li>NPU0·1에서 동시 검출</li><li>오른쪽 좌표 x+256 복원</li><li>경계 후보 선택 후 NMS</li></ol><div class="v-emphasis">전체 프레임을 기다리는<br>처리 단위를 타일로 변경</div></div></div>',
        '실제 열화상 재생 화면 위에 타일 범위와 겹침 구간 표시'),
        ['m29_split.html','20261119-real-upper-replay.jpg'])
    replace('분할 모델 변환',scene(
        mini([('ONNX 타일','입력 폭384 · 가중치 유지'),('INT8 보정','264장 × 좌·우 =528조각'),('DX-COM','NPU 그래프1개 · CPU0'),('출력 병합','x+256 → 중심320 → NMS')])
        +'<div class="v-tile-diagnostic">'+svg('m29b_split_model')+'</div>',
        '검수264 학습 영상 · FP32 진단으로 타일 변환과 출력 병합 확인'),
        ['m29b_split_model.html'],condition='445/457 TP,230/218 FN,251/242 FP는 검수264 학습 영상의 FP32 진단이다. 현장650 분할판 독립 정확도로 확대하지 않는다.')
    replace('장시간·혼잡 조건',scene('<div class="v-tail-grid"><div><h3>무인 실카메라 · 항목별 최대 지연 비교</h3>'+svg('m30_tail')+'</div><div class="v-tail-results"><div><b>18,497장</b><p>장시간 실행 · 입력 버림0<br>33 ms 초과5 · 최대44.582 ms</p></div><div><b>4명 녹화</b><p>p95 27.16 ms<br>초과4 / 805장</p></div><div><b>고밀도 녹화</b><p>p95 42.52 ms<br>초과217 / 592장</p></div></div></div>',
        'NPU 제출·회수와 메모리 처리를 보완하고 장시간·혼잡 조건의 지연 확인'),
        ['m30_tail.html'],condition='최대 지연 그래프의 항목별 전후는 별도 실행. 혼잡 녹화는 C++ 이식 전 결과. 각 실험을 단일 연속 개선 곡선으로 합치지 않는다.')

    replace('추적 좌표와 조준점',scene('<div class="v-control-loop">'+svg('m31_gimbal_loop')+'</div>'
        +mini([('입력','선택 ID의 상체 관측'),('오차','조준점 − 화면 목표점'),('출력','Pan·Tilt 방향과 SPD')]),
        '추적 결과가 들어올 때마다 오차를 계산하고 카메라 방향에 반영'),
        ['m31_gimbal_loop.html'])
    replace('짐벌 제어 시험',scene(
        mini([('Kp 30 · Ki 0 · Kd 6','PD 고정'),('불감대0.04 / 0.06','설정당1회 비교'),('실제 짐벌 + 가상 표적','2.5초에서 표적 정지')])
        +'<div class="v-pd-plot">'+svg('m32_pd')+'</div>',
        '정지 뒤 반전4→1회 · 가로 뒤처짐14.3→18.6 px'),
        ['m32_pd.html','gimbal-s7-actual.svg'],condition='불감대 비교의 실제 수직 오차 로그. Ki0·Kd6 고정이며 적분항 제거만의 효과로 서술하지 않는다.')
    response=svg('m33_plant',edits={'명령 뒤 화면 속도 · 11회 중앙값':'실측 지연·속도로 구성한 응답 모형'})
    response=re.sub(r'<rect x="388".*?/>','',response)
    response=re.sub(r'<text x="450".*?</text>','',response)
    replace('짐벌 응답 실측',scene('<div class="v-response-plot">'+response+'</div>'
        +mini([('가로 SPD10·20·30','305 · 630 · 약930 px/s'),('명령→움직임','0.108초'),('STOP 효과','0.064초')]),
        '가로 속도·출발 지연·정지 지연을 실측해 가상 시험 모형에 반영'),
        ['m33_plant.html'],condition='왼쪽은 직접 속도 명령 실측값. 오른쪽 곡선은 원자료가 지연·속도 요약값으로 구성한 응답 모형이며 원시 시계열 실측 곡선으로 제시하지 않는다.')
    replace('가상 카메라 시험',scene('<div class="v-virtual-diagram">'+svg('k08_virtual_cam')+'</div>'
        +mini([('제어값 비교','112회 · Kp30 유지'),('정답으로 채점','같은 사람 · 바뀜 · 놓침'),('반복 시험','같은 장면·조건 재현')]),
        '실제 녹화 → 가상 카메라 → 장치 처리 → 짐벌 모형의 닫힌 시험 구조'),
        ['k08_virtual_cam.html'])
    replace('상체 추적과 전신 표시',scene(
        '<div class="v-display-pair"><figure><h3>상체 · 추적과 조준에 사용</h3>'+photo('20261119-real-upper-replay.jpg','상체 표시 재생 예시 A')+'<figcaption>재생 예시 A</figcaption></figure><figure><h3>전신 범위 · 화면 표시</h3>'+photo('20261119-real-full-replay.jpg','전신 표시 재생 예시 B')+'<figcaption>재생 예시 B</figcaption></figure></div>'
        +'<div class="v-fullbody-low"><div class="v-explain"><h3>발 위치 계산</h3><div class="v-foot-rule">발목 → 무릎 → 신체 비율</div><p>상체 관측은 ID 연결·조준에 사용</p></div><div>'+svg('m25_fullbody')+'</div></div>',
        '관절 위치를 이용해 상체 추적 박스에서 전신 표시 범위 계산'),
        ['m25_fullbody.html','20261119-real-upper-replay.jpg','20261119-real-full-replay.jpg'],
        condition='사진은 같은 녹화의 서로 다른 프레임. 전신 표시 IoU 중앙값은 반올림0.43/0.74이며 증가량은 반올림차이0.31로 제시. 56장190개 상자·모두 발목관측 표본.')
    # Fix the rounded delta in the reused source chart instead of copying +0.32.
    by_title['상체 추적과 전신 표시']['body']=by_title['상체 추적과 전신 표시']['body'].replace('+0.32','+0.31')

    # Three additional explanation steps; keep the established beginning and close.
    result=[]
    for item in slides:
        result.append(item)
        if item['title']=='현장 데이터 구축':result.extend([public,box])
        if item['title']=='상체 모델 학습':result.append(aug)
    return result,usage
