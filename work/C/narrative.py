"""Connect observed problems, design choices and measured outcomes."""
import re
from visual_layouts import scene, mini


def conclusion(slide, text):
    body,count=re.subn(r'<div class="v-take">.*?</div>', lambda _: '<div class="v-take">'+text+'</div>', slide['body'], count=1, flags=re.S)
    assert count==1,slide['title']
    slide['body']=body


def refine_narrative(slides):
    by_title={s['title']:s for s in slides}

    s=by_title['팀 구성 및 역할']
    s['body']=s['body'].replace('<p>적외선 모델 학습</p><p>경량화 · 최신 모델 조사</p>',
                                '<p>적외선 모델 학습·경량화</p><p>짐벌 튜닝·응답 실측</p>')
    s['spoken']=s['spoken'].replace('윤관 팀원은 적외선 모델 학습과 경량화를 맡았습니다.',
                                    '윤관 팀원은 적외선 모델 학습과 경량화, 짐벌 튜닝과 응답 실측을 맡았습니다.')

    s=by_title['상체 검출 결과']
    conclusion(s,'혼합 라벨 E10과 상체 라벨 E10 비교 · 박스 AP 상승, 재현율 하락')
    s['spoken']='상체와 전신 라벨이 섞인 이전 E10을 현장 650장의 상체 라벨로 학습한 E10과 비교했습니다. OTP2 934장에서 박스 AP는 10.24포인트 올랐고 재현율은 2.61포인트 낮았습니다. 관절 AP도 시작 모델 F보다 낮았습니다.'
    s['quick_cues']=['박스 범위 혼재','상체 기준 통일','AP 36.04→46.28%']

    s=by_title['후속 학습 채택 판단']
    conclusion(s,'증강 후보의 박스·관절·추적 결과를 비교해 기준 E10 유지')
    s['spoken']='이후 증강 조건을 바꿔 추가 개선을 시도했습니다. 표준 증강은 박스 AP가 1.88포인트 높았지만 관절 AP는 1.04포인트 낮았습니다. 실내와 실외 추적을 함께 개선한 후보도 없어 이 비교에서는 E10을 유지했습니다. 이어지는 추가 모델 비교에서는 장치에서 실제로 같은 사람을 얼마나 잘 연결하는지까지 평가 기준을 넓혔습니다.'
    s['quick_cues']=['증강 후보 비교','관절·추적 절충','기준 E10 유지']

    s=by_title['검출기 추가 비교']
    s['body']=s['body'].replace('추가 학습 모델 · own9e','추천 모델 · own9e')
    s['body']=s['body'].replace('장치 재생에서 IDF1 상승','장치 재생 IDF1을 선정 근거로 사용').replace('정확도와 관절 사용 조건을 함께 확인','조준은 상체 박스 기준으로 계산')
    s['body']=s['body'].replace('<b>검출·추적</b>','<b>추천 근거</b>').replace('<b>모델 선정</b>','<b>조준 설계</b>')
    conclusion(s,'장치 재생의 ID 연결 개선으로 own9e 추천 · 어깨 관절 신뢰도는 하락')
    s['spoken']='추가 모델 own9e는 모델 9와 장치 INT8 분할 모드로 녹화 18편을 비교했습니다. IDF1은 4.50퍼센트포인트 높아져 추천 모델로 바뀌었고, 번호 변경 차이는 0회였습니다. 다만 양쪽 어깨 신뢰도 기준을 충족한 비율은 92에서 9퍼센트로 낮아졌습니다. 현재 가까운 사람의 조준은 상체 박스를 사용합니다. 이 추천의 근거는 장치 녹화 재생 결과이며 실제 보행 짐벌 효과는 별도 확인 대상입니다.'
    s['quick_cues']=['장치 재생 18편','IDF1 +4.50%p로 추천','박스 조준·관절 절충']
    s['condition']+=' / own9e 추천은 검출 단독 점수와 구분한 장치 재생 추적 결과. close_aim의 박스 사용은 S27과 같은 커밋의 인계 원문(S26 스냅샷)에 근거. 실제 보행 짐벌 검증 완료를 의미하지 않는다.'
    s['seconds']=40

    s=by_title['외형 모델 비교']
    conclusion(s,'검색 정답률과 실제 ID 연결을 함께 평가해 기본 RVGGA0 선정')
    s['spoken']='외형 모델은 검색 정답률과 장치 처리 시간을 먼저 비교했습니다. RepVGG 계열은 ViT-lite보다 처리 시간이 짧았지만, 검색 정답률 0.892를 낸 OTP2 학습판에서는 실제 ID 연결 문제가 있었습니다. 녹화 9편의 추적 비교까지 확인해 기본 RVGGA0를 추천했습니다. 화면의 속도 수치는 각 과거 학습판의 측정값입니다.'
    s['quick_cues']=['검색·속도 비교','OTP2판 ID 연결 문제','기본 RVGGA0 선정']

    s=by_title['가림 위치 예측']
    conclusion(s,'공개 TMOT 검증 위치 오차: Kalman 0.352, GRU 0.223 → GRU 적용')
    s['spoken']='공개 검증에서 가림 뒤 위치 오차가 줄어 GRU를 적용했습니다. 최근 20프레임의 상자·속도·관절을 보고 최대 15프레임 동안 칼만의 위치 예측을 보정합니다.'
    s['quick_cues']=['공개 검증에서 GRU 적용','최근 20프레임 관측','최대 15프레임 보정']

    s=by_title['번호 유지 보완']
    old=mini([('위치 오차','Kalman이 14편 중 10편에서 낮음'),('IDF1 · GRU/Kalman','74.7% / 74.1%'),('가드 전후 IDF1','82.3%로 동일')])
    new=mini([('장치 재생 1편 · IDF1','Kalman 71.81% / GRU 75.36%'),('번호 복귀의 부작용','KeepID 적용 시 장기 뺏김 19→20회'),('연결 조건 보완','비용·외형 가드로 장기 뺏김 20→17회')])
    assert old in s['body']
    s['body']=s['body'].replace(old,new)
    conclusion(s,'자체 14편 위치 오차는 Kalman 우세 · 장치 재생 1편 IDF1은 GRU 우세')
    s['spoken']='자체 영상 14편에서 위치 오차는 칼만이 더 낮았습니다. 장치 재생 한 편에서는 IDF1이 GRU 75.36퍼센트, 칼만 71.81퍼센트였고 당시에는 수정 GRU를 유지했습니다. 별도 9편에서 KeepID는 번호 변경을 줄였지만 장기 뺏김은 늘었습니다. 가드를 추가하니 뺏김은 20회에서 17회로 줄었습니다.'
    s['quick_cues']=['자체 14편 위치 오차','장치 1편 IDF1','KeepID·가드']
    s['condition']+=' / 자체 14편은 개발에 사용한 위치 예측 비교다. 칼만 전환 규칙 포함 GRU 위치 오차는 0.118이다. 1편 IDF1은 seq_018의 장치 재생이며, KeepID·가드는 별도 9편 PC 시험이다.'
    s['seconds']=40

    s=by_title['두 NPU 동시 타일 처리']
    conclusion(s,'한 프레임을 두 NPU에 나눠 맡겨 같은 시점의 검출 결과를 함께 회수')
    s['spoken']='지연을 줄이기 위해 NPU에 일을 나누는 단위를 바꿨습니다. 기존에는 연속 프레임을 두 NPU에 번갈아 맡겼습니다. 새 방식은 한 프레임을 폭 384픽셀의 좌우 타일로 나눠 동시에 처리합니다. 가운데 128픽셀을 겹쳐 경계의 사람을 포함하고, 좌표를 복원한 뒤 중복 검출을 합칩니다. 다음 두 장에서 모델 변환과 같은 조건의 지연 비교를 보여드리겠습니다.'
    s['quick_cues']=['프레임 교대의 지연','같은 프레임 좌우 분할','좌표 복원·중복 병합']

    s=by_title['주요 성과']
    rows=[
        ('검출','상체·전신 박스 범위 혼재','상체 기준 통일·현장 학습','박스 AP 36.04 → 46.28%','OTP2 934장 · E10 비교'),
        ('추적','ID 변경·연결 품질의 절충','BoT-SORT 선정·매칭 기준 조정','ID 변경 1,001 → 566회','동일 PC · BoT-SORT 설정 비교'),
        ('NPU 처리','프레임 처리 결과의 지연','같은 프레임을 두 NPU로 분할','p95 40.47 → 25.71 ms','서버 시험 · 각 65초 · 분할에서 1장 버림'),
        ('짐벌 제어','정지 뒤 반복 반전','작은 오차를 무시하는 범위 확대','상하 반전 4 → 1회','조건별 1회 · 별도 가로 시험은 뒤처짐 증가'),
    ]
    table='<table class="n-outcomes"><thead><tr><th>분야</th><th>문제</th><th>선택한 설계</th><th>확인한 성과</th></tr></thead><tbody>'
    for area,problem,choice,result,scope in rows:
        table+=f'<tr><th>{area}</th><td>{problem}</td><td>{choice}</td><td><b>{result}</b><span>{scope}</span></td></tr>'
    table+='</tbody></table>'
    s['body']=scene(table,'현장 데이터와 비교 시험을 바탕으로 검출·추적·처리·제어를 연결')
    s['spoken']='마지막으로 문제와 설계 선택을 연결해 정리하겠습니다. 현장 상체 E10의 박스 AP는 46.28퍼센트였고, 후속 own9e는 장치 재생에서 IDF1 개선을 확인했습니다. 추적은 BoT-SORT를 선정하고 매칭 기준을 조정해 ID 변경을 줄였습니다. 처리는 한 프레임을 두 NPU로 나눠 서버 지연을 낮췄습니다. 제어는 PD와 불감대 조정으로 정지 뒤 반복 반전을 줄였습니다. 각 비교 시험을 바탕으로 표적 선택부터 추종·수동 전환까지 이어지는 시스템을 구현했습니다. 감사합니다.'
    s['quick_cues']=['상체 기준·현장 학습','BoT-SORT·매칭 조정','동시 타일·PD 조정']
    s['refs']=list(dict.fromkeys([*s['refs'],'S24','S17','S26','S27']))
    s['condition']+=' / 네 행은 각각 독립된 비교이며 하나의 최종 장치 실행 결과로 합치지 않는다. 반전 감소와 가로 뒤처짐 증가의 절충은 제어 시험 장과 출처에 보존한다.'
    s['seconds']=45

    # Keep tracker selection together, followed immediately by occlusion design
    # and its measured result. All other topic boundaries retain their order.
    position=by_title['가림 위치 예측']
    result=[s for s in slides if s is not position]
    at=next(i for i,s in enumerate(result) if s['title']=='BoT-SORT 최종 설정')+1
    result.insert(at,position)
    return result
