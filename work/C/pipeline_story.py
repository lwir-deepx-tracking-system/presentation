"""Two code-audited pipeline slides, following the software overview.

The original 43-slide spoken draft runs first. Insertions are title-anchored,
then all numbering and the 20-minute target are updated here.
"""
from copy import deepcopy


def pipeline_slides(slides):
    assert len(slides) == 43
    anchor = next(i for i, s in enumerate(slides) if s['title'] == '소프트웨어 구성')
    template = slides[anchor]
    common = dict(base_number=None, section='시스템 소개', refs=['S28', 'S29'],
                  pending=[], delivery_note='', transition='', seconds=35)
    def item(title, body, spoken, cues, condition):
        s = deepcopy(template)
        s.update(common, title=title, body=body, spoken=spoken, quick_cues=cues,
                 presenter_cue=' → '.join(cues), condition=condition)
        return s

    # Timeline is deliberately qualitative: width is not a measured duration.
    diagram = '''<div class="scene b-scene pipeline-scene">
<div class="pipeline-context">모델뱅크 서버 · 실카메라 분할 입력 · 처리 흐름 개념도</div>
<div class="pipeline-chart">
<div class="pipeline-axis">동작 순서 <span>시간 →</span></div>
<div class="pipeline-lane"><div class="pipeline-label">카메라 수신<small>수신 스레드</small></div><div class="pipeline-cells"><b class="f-a">영상 A</b><b class="f-b">영상 B</b><b class="f-c">영상 C</b><i></i><i></i><i></i></div></div>
<div class="pipeline-lane"><div class="pipeline-label">검출 입력·회수<small>npu-feed 스레드</small></div><div class="pipeline-cells"><i></i><b class="f-a span2">A 준비 · 두 NPU 실행·회수</b><b class="f-b span2">B 준비 · 두 NPU 실행·회수</b><i></i></div></div>
<div class="pipeline-lane"><div class="pipeline-label">ID 연결<small>메인 처리 루프</small></div><div class="pipeline-cells"><i></i><i></i><i></i><b class="f-a">A 추적</b><i></i><b class="f-b">B 추적</b></div></div>
<div class="pipeline-lane"><div class="pipeline-label">짐벌 전달<small>브리지 쓰기 스레드</small></div><div class="pipeline-cells"><i></i><i></i><i></i><i></i><b class="f-a">A 관측 전달</b><i></i></div></div>
</div>
<div class="pipeline-summary"><strong>이전 영상의 ID를 연결하는 동안<br>다음 영상의 검출을 진행</strong><p>짐벌 상태는 별도 읽기 스레드로 수신</p></div>
</div>'''
    first = item('멀티스레드 파이프라인', diagram,
        '단계마다 기다리는 원인이 달라 작업을 나눴습니다. 위에서부터 카메라 수신, 검출 입력과 결과 회수, ID 연결, 짐벌 전달입니다. 색이 같은 칸은 같은 영상입니다. A의 ID를 연결하는 동안 검출 스레드는 B를 처리할 수 있습니다. 짐벌에 쓰거나 상태를 읽는 작업도 별도 스레드로 분리했습니다.',
        ['위에서 아래로 작업 분담', '같은 색은 같은 영상', 'A 추적과 B 검출의 겹침'],
        '모델뱅크 549324c 코드 확인. 실카메라 Feed 활성·tile 경로: camera_link.lv_reader, frame_feed.Feed._run, app 메인 추적, gimbal_link.gb_writer/gb_reader. 시간표는 동작 관계를 설명하는 개념도이며 칸 폭·겹침 길이는 실측 시간이 아니다. Feed는 모드·환경에 따라 비활성 또는 다른 경로로 대체될 수 있다. C++ Runtime의 단계별 스레드와 구분한다. 두 NPU 결과의 C++ 병렬 wait는 별도 설정일 때만 활성화된다.')
    first['delivery_note'] = '같은 색의 A를 따라 내려간 뒤, A 추적과 B 검출이 나란히 있는 부분을 짚는다. 칸 너비로 속도 향상 배수를 설명하지 않는다.'

    policies = '''<div class="scene b-scene pipeline-scene">
<div class="pipeline-context">모델뱅크 서버 · 실카메라 경로</div>
<div class="queue-policy"><article><div class="queue-heading"><span>01 · 입력 대기</span><strong>최신 영상 우선</strong></div><div class="queue-picture"><b class="queue-old">A</b><b class="queue-old">B</b><b class="queue-new">C</b><span>→</span><b class="queue-new">C</b></div><p>최대 3개 보관<br>밀릴 때 대기 영상은 최신 1개로 정리</p></article>
<article><div class="queue-heading"><span>02 · 추적으로 전달</span><strong>프레임 순서 유지</strong></div><div class="queue-picture"><b>A</b><span>→</span><b>B</b><span>→</span><b>C</b></div><p>제출한 순서대로 결과를 소비<br>이전·다음 관측을 이어 ID 갱신</p></article>
<article><div class="queue-heading"><span>03 · 짐벌로 전달</span><strong>최신 관측으로 갱신</strong></div><div class="queue-picture"><b class="queue-old">이전</b><span>→</span><b class="queue-new">최신</b></div><p>미전송 관측은 최신 한 건으로 교체<br>선택·정지 명령은 별도 경로로 처리</p></article></div>
<div class="pipeline-summary"><strong>추적은 순서 · 제어는 최신성</strong><p>오래된 입력의 누적을 줄이고 프레임 버림을 함께 계측</p></div>
</div>'''
    second = item('큐와 전달 정책', policies,
        '큐에는 모든 데이터를 같은 방식으로 쌓지 않았습니다. 입력은 최대 세 장을 보관하지만 실시간 처리가 밀리면 대기 중인 최신 한 장을 남깁니다. 검출에 제출한 결과는 순서대로 가져와 ID를 갱신합니다. 짐벌에는 보내지 못한 관측을 최신 한 건으로 교체하고 선택과 정지 명령을 별도로 처리합니다. 오래된 결과의 누적을 줄이는 대신 버린 프레임도 함께 셉니다.',
        ['입력: 최대3·밀리면 최신1', '추적: 제출 순서', '짐벌: 최신 관측·명령 분리'],
        '모델뱅크 549324c 실카메라 경로 코드 정책. 입력 app.py deque(maxlen=3), camera_link 수신 시 초과 제거, frame_feed._run의 바쁜 코어/auto 분기에서 최신1로 정리. lossless 재생은 프레임 버림 예외다. 제출 결과 Feed.out append/popleft와 seq 검사를 확인. 짐벌 GB.wframe은 일반 관측 미전송 슬롯1이며 선택/신원전환 증거 프레임·관측 barrier는 별도 보존 경로가 있다. 명령 wq는 별도 경로이며 모든 삽입에 공통 최대64가 보장되는 것은 아니다. 김재남 Runtime의 입력2·GUI2 정책을 모델뱅크에 대입하지 않는다. 실제 장치 활성 설정·성능 효과를 새로 검증한 것은 아니다.')
    second['transition'] = '이 구조 위에서, 먼저 열화상에서 사람을 찾는 검출을 설명하겠습니다.'
    slides[anchor]['transition'] = '이 기능들을 실제 실행에서는 어떻게 나눠 처리하는지 보겠습니다.'
    slides[anchor + 1:anchor + 1] = [first, second]

    # Keep the new explanation at 70 seconds, demo 180 and contents 15.
    existing = [s for s in slides if s is not first and s is not second
                and s['base_number'] != 28 and s['title'] != '목차']
    target = 1020 - 15 - first['seconds'] - second['seconds']
    total = sum(s['seconds'] for s in existing)
    exact = [target * s['seconds'] / total for s in existing]
    allocated = [int(t) for t in exact]
    for i in sorted(range(len(exact)), key=lambda i: exact[i] - allocated[i], reverse=True)[:target-sum(allocated)]:
        allocated[i] += 1
    for s, seconds in zip(existing, allocated):
        s['seconds'] = seconds
    for n, s in enumerate(slides, 1):
        s['number'] = n
    assert len(slides) == 45 and sum(s['seconds'] for s in slides) == 1200
    return slides
