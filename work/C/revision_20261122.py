"""Apply the measured tradeoffs and model recommendations from 11/22."""
from visual_layouts import scene,mini,svg


def own9e_slide():
    chart='<svg viewBox="0 0 760 330" role="img" aria-label="양쪽 어깨 신뢰도 0.5 이상 비율: 모델9 92%, own9e 9%"><text x="10" y="26" class="v-chart-title">양쪽 어깨 신뢰도 ≥ 0.5 비율 (%)</text>'
    for value in [0,50,100]:
        x=180+440*value/100
        chart+=f'<line x1="{x}" x2="{x}" y1="64" y2="260" stroke="#dce2ea"/><text x="{x}" y="297" text-anchor="middle" class="v-axis">{value}</text>'
    for y,label,value,color in [(95,'모델 9',92,'#9fb2c5'),(182,'own9e',9,'#b57436')]:
        width=value/100*440
        chart+=f'<text x="163" y="{y+32}" text-anchor="end" class="v-plot-label">{label}</text><rect x="180" y="{y}" width="{width}" height="48" fill="{color}"/><text x="{190+width}" y="{y+32}" class="v-plot-value">{value}%</text>'
    chart+='</svg>'
    body=scene('<div class="v-own-header"><b>11/22 추천 · own9e 시드 1</b><span>모델 9와 장치 INT8·분할 재생 18편 비교</span></div>'
        '<div class="v-own-grid"><div class="v-own-gains"><div><small>IDF1 변화</small><strong>+4.50%p</strong><p>보고 구간 +1.26~+10.26%p</p></div><div><small>번호 변경 차이</small><strong>0회</strong><p>보고 구간 −9~+10회</p></div></div><div>'+chart+'</div></div>'
        +mini([('검출·추적','장치 재생에서 IDF1 상승'),('관절 출력','어깨 신뢰도 기준 충족률 하락'),('모델 선정','정확도와 관절 사용 조건을 함께 확인')]),
        'own9e: 추적 점수 향상과 관절 신뢰도의 절충을 확인')
    return dict(title='검출기 추가 비교',body=body,spoken='11월22일 추천 검출기는 own9e 시드1입니다. 모델9와장치 INT8 분할 모드로18편을 재생해 비교했을 때 IDF1은4.50퍼센트포인트 올랐습니다. 번호 변경 차이는0회였고 보고 구간은마이너스9에서플러스10회였습니다. 양쪽 어깨 신뢰도가0.5 이상인 비율은92에서9퍼센트로 낮아졌습니다. 추적 점수와관절 출력의 절충을 함께 확인한 결과입니다.',refs=['S26','S27'],condition='11/22 model-bank@0e3dd540의 추천·장치 재생 기록. IDF1·IDSW 변화 구간의 신뢰 수준은 원문에 명시되지 않아 보고 구간으로 표기. 관절 미표기 인물의 신뢰도를0으로 학습한 점이 인계 원문에 원인으로 기록됨. 걷기 짐벌 시험 미실시.',pending=[],section='검출기 비교',seconds=35,base_number=None,quick_cues=['own9e 추천','IDF1 +4.50%p','어깨92→9%'],presenter_cue='추천 변경 → 추적 점수 → 관절 출력')


def apply_revision(slides,backup):
    output=[]
    for s in slides:
        title=s['title']
        if title=='상체 검출 결과':
            s['body']=s['body'].replace('<small>관절 AP</small><b>+1.07%p</b><span>77.28 → 78.35%</span>', '<small>관절 AP</small><b>78.35%</b><span>이전77.28% · 시작F84.35%</span>')
            s['spoken']='현장650장 E10의11월19일 적용 결과입니다. OTP2 934장에서 이전 E10 대비 박스 AP는10.24퍼센트포인트 올랐고 재현율은2.61포인트 낮아졌습니다. 관절 AP78.35퍼센트는 이전 E10보다1.07포인트 높고 시작F보다6.00포인트 낮았습니다. 라벨 기준을 정리한 학습의 효과와절충을 함께 비교했습니다.'
        elif title=='후속 학습 채택 판단':
            s['body']=s['body'].replace('운영 E10','기준 E10').replace('운영 선택','11/19 선택').replace('현장650장 E10 유지','현장650장 E10 유지')
            s['spoken']='이 비교는 현장650장 E10의 후속 학습 후보를 평가한 이력입니다. 표준 증강에서 박스 AP는1.88퍼센트포인트 높았지만 관절 AP는1.04포인트 낮았습니다. 실내·실외 추적 결과도 함께 비교해 당시에는 E10을 유지했습니다. 다음 장은11월22일에 추가된 추천 검출기의 비교입니다.'
        elif title=='외형 모델 비교':
            s['body']=s['body'].replace('M1 INT8 · RepVGG 계열은 ViT-lite 대비 약 4배 빠른 처리','11/22 외형 추천: 기본 RVGGA0 · 장치 재생 추적 결과로 선정')
            s['body']=s['body'].replace('OTP2 몸 1순위 정답 (높을수록 좋음)','과거 학습판 비교 · OTP2 537질의')
            s['spoken']='그림은 과거 학습판들을 같은 M1 INT8에서 비교한 결과입니다. OTP2 537질의의 몸1순위 정답률은 ViT-lite가0.616과0.672, RepVGG OTP2판은0.892, 검수264판은0.764였습니다. 처리 시간은약5밀리초와1.3밀리초였습니다. 0.892를 낸 과거OTP2판은ID 연결 문제로 장치 목록에서 제외했고, 11월22일 추천 외형은기본RVGGA0입니다. 최종 추천은9편의추적 비교를 기준으로 합니다.'
            s['condition']+=' / OTP2 검색537질의와실내176질의는별도. 기본RVGGA0의처리시간을1.26/1.28로대입하지않는다. 과거검수264의장치선택과현재추천RVGGA0를구별.'
        elif title=='번호 유지 보완':
            s['body']=scene('<div class="v-id-compare"><div><h3>위치 예측 · 자체 14편·놓침 238건</h3>'+svg('k09_id_keep',0)+'</div><div><h3>번호 연결 · 9편 PC 재생</h3>'+svg('k09_id_keep',1)+'</div></div>'
                +mini([('위치 오차','Kalman이 14편 중 10편에서 낮음'),('IDF1 · GRU/Kalman','74.7% / 74.1%'),('가드 전후 IDF1','82.3%로 동일')]),
                'KeepID: 번호 변경 감소·장기 뺏김 증가 → 가드 추가 후 뺏김 감소')
            s['spoken']='자체 14편에서 Kalman 위치 오차는 0.110, 수정 GRU는 0.122였고 14편 중 10편에서 Kalman이 낮았습니다. GRU와 Kalman의 IDF1은 74.7과 74.1퍼센트였고 차이의 90퍼센트 구간은 마이너스 0.8에서 플러스 2.3포인트였습니다. 별도 9편에서 KeepID는 번호 변경 47에서 43, 장기 뺏김 19에서 20으로 바뀌었습니다. 가드 두 개를 더하면 뺏김 20에서 17, IDF1은 82.3퍼센트로 같았습니다.'
            s['quick_cues']=['Kalman 오차 우세','KeepID 47→43·19→20','가드20→17·IDF1 동일']
            s['refs']=list(dict.fromkeys([*s['refs'],'S26']))
        elif title=='분할 모델 변환':
            s['body']=s['body'].replace('검수264 학습 영상 · FP32 진단으로 타일 변환과 출력 병합 확인','학습264장 FP32 진단: 누락230→218 · 일부 관절 위치 오차 증가')
            s['spoken']='E10 가중치를 유지하고 폭 384 타일 그래프로 변환했습니다. 검수 264장의 좌우 528조각으로 INT8을 보정하고 좌표 복원과 경계 선택, NMS로 결과를 합쳤습니다. 학습에 쓴 같은 264장 FP32 진단에서 맞힌 사람은 445에서 457, 누락은 230에서 218로 바뀌었고 일부 관절 위치 오차는 커졌습니다. 분할 INT8의 독립 정답 평가는 추가 확인 대상입니다.'
        elif title=='가상 카메라 시험':
            s['spoken']='확대한 열화상 녹화의 창을 가상 카메라로 사용하고 실제 검출·추적·제어 코드를 연결해 같은 장면을 반복했습니다. 제어값 112회 비교 뒤 Kp30을 유지했습니다. 재포착 비교에서 속도 방식은 20퍼센트포인트, 장치 적용 fused는 6포인트 높았고 fused의 95퍼센트 구간은 마이너스 11에서 21포인트였습니다. 실제 짐벌 비교는 14분에 중단됐고 fused가 짐벌을 움직이는 재포착 사례는 관찰되지 않았습니다.'
        elif title=='주요 성과':
            s['body']=s['body'].replace('상체 기준 정리·E10 학습<br>OTP2 박스 AP 46.28%','상체 E10 · OTP2 AP 46.28%<br>own9e 추가 비교·추천 갱신')
            s['spoken']=s['spoken'].replace('현장650장의 상체 기준을 정리하고 E10을 학습해 OTP2 박스 AP46.28퍼센트를 확보했습니다.', '현장650장의상체기준을정리하고E10을학습해OTP2박스AP46.28퍼센트를확보했습니다. 이후own9e의장치재생비교와관절출력까지확인했습니다.')
        s['refs']=list(dict.fromkeys([*s['refs'],'S26'])) if title in ['상체 검출 결과','후속 학습 채택 판단','외형 모델 비교','분할 모델 변환','가상 카메라 시험','주요 성과'] else s['refs']
        output.append(s)
        if title=='후속 학습 채택 판단':output.append(own9e_slide())

    for s in backup:
        title=s['title']
        if title=='박스 보정과 표시':
            s['body']=s['body'].replace('11/20 body 기본 → 11/21 항상 켬 코드','기본 body · 변환표가 없으면 size')
            s['spoken']='11월21일코드에서일반끄기옵션을제거했습니다. 기본body, 변환표가없으면size이며오류시자동비활성화가가능합니다. PC녹화에서키변화상위1퍼센트는0.071→0.043, 조준떨림은0.0195로같았습니다. 코드의장치반영과실촬영효과는별도확인이필요합니다.'
        elif title=='모델 추천과 선택 기록':
            s['body']=s['body'].replace('검출 검수264 E10 / 외형 RVGGA0','11/22 검출 own9e / 외형 RVGGA0').replace('검출 검수 264장 E10 / 외형 RVGGA0','11/22 검출 own9e / 외형 RVGGA0').replace('장치 선택 모델','과거 장치 선택').replace('검수264 RepVGG','검수264 RepVGG · 적용 이력')
        elif title=='외형 및 위치 기억':
            s['spoken']='자체14편·놓침238건에서Kalman0.110, 수정GRU0.122이며10편에서Kalman이낮았습니다. IDF1차이는+0.6%p,90%구간−0.8~+2.3%p였습니다. 개발에사용한자료의비교입니다.'
        if title in ['박스 보정과 표시','모델 추천과 선택 기록','외형 및 위치 기억']:
            s['refs']=list(dict.fromkeys([*s['refs'],'S26']))

    details=scene('<div class="v-plot-heading">11/22 own9e 시드1 · 모델9 대비 장치 재생18편</div><table class="c-table"><tr><th>항목</th><th>변화·비교</th><th>원문 보고 구간</th></tr><tr><td>IDF1</td><td>+4.50%p</td><td>+1.26~+10.26</td></tr><tr><td>번호 변경 차이</td><td>0회</td><td>−9~+10</td></tr><tr><td>양쪽 어깨 신뢰도 ≥0.5</td><td>모델9 92% / own9e 9%</td><td>기준 충족 비율</td></tr><tr><td>실행 조건</td><td>장치 INT8·분할</td><td>녹화18편 재생</td></tr></table>', '검출 추천 own9e · 외형 추천 기본 RVGGA0')
    backup.append(dict(title='own9e 비교 조건',body=details,seconds=0,section='예비자료',refs=['S26','S27'],spoken='모델뱅크0e3dd540의11월22일추천갱신과장치재생비교입니다. 관절미표기인물의신뢰도를0으로학습한점이낮은관절신뢰도의원인으로기록됐습니다. close_aim은상자기준이어서해당관절신뢰도하락의직접영향이없다는코드설명과실제보행짐벌미시험을함께기록합니다. 이슬라이드는실측종단이나새현장독립성능을보장하지않습니다.',condition='추천·적용 기록은11/22시점. 원문보고구간의신뢰수준을임의로95%로표기하지않음.',pending=[]))
    return output
