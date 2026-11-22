"""Present tracker comparisons as the path to the selected BoT-SORT model."""
import copy
from visual_layouts import scene,mini


def finalize_tracking(slides,backup):
    for item in backup:
        if item['title']=='추적기 카탈로그 및 교체':
            item['body']=item['body'].replace('종합 지표 기준 기본 추천','최종 선정 알고리즘').replace('ID 연결·재현율 장점','비교 후보 · ID 연결·재현율')
    output=[]
    for item in slides:
        title=item['title']
        if title=='장치 상태 이력':
            archived=copy.deepcopy(item)
            archived.update(number=len(backup)+1,seconds=0,section='예비자료')
            backup.append(archived)
            continue
        if title=='추적 알고리즘 구성':
            item['title']='추적 알고리즘 선정 과정'
            item['body']=item['body'].replace('<small>01</small>','<small>01 · 기준 알고리즘</small>').replace('<small>02</small>','<small>02 · 개선 후보</small>').replace('<small>03</small>','<small>03 · 최종 선정</small>')
            item['body']=item['body'].replace('공통 C++ 인터페이스 · GUI에서 3종 선택','ByteTrack·OC-SORT 비교를 거쳐 BoT-SORT 선정')
            item['spoken']='ByteTrack을 기준으로 삼고, 가림 뒤 연결을 보완하는 OC-SORT와 박스 상태·매칭을 보완하는 BoT-SORT를 비교했습니다. 세 알고리즘을 C++ 공통 인터페이스로 구현해 평가했고, 최종 추적 알고리즘은 BoT-SORT로 선정했습니다. 다음 두 장에서 후보별 장단점과 선정 결과를 설명하겠습니다.'
            item['quick_cues']=['기준 ByteTrack','개선 후보 OC-SORT','최종 BoT-SORT']
        elif title=='추적 연속성 비교':
            item['spoken']='같은 PC에서 OC-SORT와 BoT-SORT의 ID 연결을 비교했습니다. OC-SORT의 ID 변경은531회로 BoT-SORT566회보다35회 적고, 재현율도87.7퍼센트로 높았습니다. 이 결과는 후보의 장점으로 기록하고, 검출과 연결을 함께 평가하는 HOTA와IDF1까지 종합해 최종 알고리즘을 선정했습니다.'
            item['quick_cues']=['동일 PC 후보 비교','OC-SORT ID 변경531','종합 지표로 선정']
        elif title=='추적 품질 및 선택 기준':
            item['title']='최종 추적기 선정'
            item['body']=item['body'].replace('기본 추천 <b>BoT-SORT</b>','최종 선정 <b>BoT-SORT</b>').replace('가림이 잦은 장면 <b>OC-SORT</b>','선정 기준 <b>종합 추적 품질</b>')
            item['spoken']='같은 PC 평가에서 BoT-SORT는 HOTA60.7, IDF1 67.5퍼센트로 OC-SORT보다 높았습니다. 정밀도89.5퍼센트와MOTA74.7퍼센트도 함께 확인했습니다. ID 변경 횟수와 재현율의 절충을 포함해 종합 추적 품질을 기준으로 BoT-SORT를 최종 선정했습니다.'
            item['quick_cues']=['HOTA60.7','IDF1 67.5%','BoT-SORT 최종 선정']
        elif title=='GUI 조작 순서':
            item['body']=item['body'].replace('<h3>추적기 선택</h3>','<h3>추적기 설정</h3>').replace('ByteTrack · OC-SORT · BoT-SORT','최종 알고리즘 · BoT-SORT')
            item['spoken']='최종 운용 알고리즘은 BoT-SORT입니다. PC에서 추적기 설정과 완료 응답을 확인한 뒤 추적할 ID를 선택합니다. 선택한 사람을 자동 추종하고, 수동 조작과정지로 운용자가 개입할 수 있습니다.'
            item['quick_cues']=['BoT-SORT 설정','표적 ID 선택','추종·수동·정지']
        elif title=='시연 구성':
            item['body']=item['body'].replace('모델·추적기·제어','모델·BoT-SORT·제어')
            item['spoken']='최종 알고리즘 BoT-SORT를 기준으로 검출 모델과 제어 설정을 맞춥니다. 표적 선택, 이동과가림 구간의 추종을 보여주고, 수동 전환과정지로 마무리합니다. 실제 시연 영상과 촬영 조건은 해당 실행에 맞춰 설명합니다.'
        elif title=='주요 성과':
            item['body']=item['body'].replace('<strong>3종 C++ 추적기</strong>','<strong>BoT-SORT 선정</strong>').replace('BoT-SORT HOTA 60.7<br>PC에서 추적기 선택·변경','HOTA 60.7 · IDF1 67.5%<br>3종 C++ 구현·비교 후 최종 선정')
            item['spoken']='현장650장의 상체 기준을 정리하고 E10을 학습해 OTP2 박스 AP46.28퍼센트를 확보했습니다. 세 추적기를 C++로 구현하고 비교해 BoT-SORT를 최종 선정했습니다. 처리에서는 동시 타일과 C++ 보완을 적용하고, 짐벌은 실제 응답과 가상 시험으로 제어를 평가했습니다. 검출부터 추적, 처리와제어까지 구현하고 비교한 것이 이번 프로젝트의 성과입니다. 감사합니다.'
        output.append(item)
        if title=='추적 품질 및 선택 기준':
            output.append(parameter_slide())
    return output


def parameter_slide():
    rows=[('기본 설정',1001),('new 0.5',723),('+ match 0.9',575),('+ unconfirmed 0.6',566)]
    drawing='<svg viewBox="0 0 780 430" role="img" aria-label="같은 PC의 BoT-SORT ID 변경 횟수: 기본1001, 새ID기준0.5는723, 매칭0.9추가575, 미확정매칭0.6추가566"><text x="10" y="30" class="v-chart-title">BoT-SORT · PC 평가 · ID 변경 횟수 ↓</text>'
    for tick in [0,600,1200]:
        x=235+430*tick/1200
        drawing+=f'<line x1="{x}" x2="{x}" y1="54" y2="360" stroke="#dce2ea"/><text x="{x}" y="397" text-anchor="middle" class="v-axis">{tick}</text>'
    for n,(label,value) in enumerate(rows):
        y=72+n*75;width=430*value/1200;color='#002f6d' if n==3 else '#9fb2c5'
        drawing+=f'<text x="218" y="{y+30}" text-anchor="end" class="v-plot-label">{label}</text><rect x="235" y="{y}" width="{width}" height="43" fill="{color}"/><text x="{245+width}" y="{y+30}" class="v-plot-value">{value:,}</text>'
    drawing+='</svg>'
    body=scene('<div class="v-tracker-config"><div>'+drawing+'</div><div class="v-explain"><h3>최종 설정</h3><ol><li>새 ID 생성 기준 0.5</li><li>1차 매칭 기준 0.9</li><li>미확정 트랙 매칭 0.6</li></ol><div class="v-emphasis">HOTA 60.7<br>IDF1 67.5% · IDSW 566</div></div></div>'+mini([('검출 점수','high 0.25 · low 0.10'),('트랙 유지','buffer 30 · n_init 2'),('2차 매칭','threshold 0.5')]),'새 ID 생성과 매칭 기준을 조정해 ID 변경1,001→566회')
    return dict(title='BoT-SORT 최종 설정',body=body,spoken='BoT-SORT를 선정한 뒤 파라미터를 조정했습니다. 같은 PC 평가에서 기본 ID 변경1,001회가 새ID 기준0.5에서723회, 매칭0.9를 함께 적용했을 때575회, 미확정 트랙 매칭0.6까지 조정했을 때566회로 줄었습니다. 새사람 출력이 늦어지거나 재현율이 떨어지는 후보와 비교해 이조합을 최종 설정으로 선택했습니다.',refs=['S14','S24'],condition='동일 PC의 BoT-SORT 설정 비교. 단계는 선정된 설정 조합이며 ByteTrack·OC-SORT의 다른 환경 수치와 연결하지 않는다. 최종 BoT-SORT 선정은 사용자 확인을 반영했다. 해당 비교의 CMC·ReID 미사용 조건은 유지한다.',pending=[],section='추적기 선정',seconds=35,base_number=None,quick_cues=['기본1001','조합별 조정','최종566'],presenter_cue='기본 → 조정 → 최종')
