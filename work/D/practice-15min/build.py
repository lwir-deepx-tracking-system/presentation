"""Build a rehearsal draft from local, frozen inputs only."""
from pathlib import Path
import html,json,hashlib,re
from script_data import ROWS,NOTES

BASE=Path(__file__).resolve().parent
manifest=json.loads((BASE/'sources/manifest.json').read_text(encoding='utf-8'))
source=json.loads((BASE/'sources/pdf-pages.json').read_text(encoding='utf-8'))
assert len(ROWS)==32 and [r[0] for r in ROWS]==list(range(1,33))
assert source['count']==47 and manifest['excluded_appendix_pages']==list(range(33,48))
assert hashlib.sha256((BASE/'sources/input.pdf').read_bytes()).hexdigest()==manifest['source_sha256']
for f in manifest['evidence']:
 assert hashlib.sha256((BASE/f['path']).read_bytes()).hexdigest()==f['sha256']

# Four seconds per page for pointing/transition, remaining time by spoken
# length. This is a rehearsal budget and does not measure real speaking pace.
weights=[len(re.findall('[가-힣]',r[3])) for r in ROWS]
exact=[4+(900-4*len(ROWS))*w/sum(weights) for w in weights]
seconds=[int(x) for x in exact]
for i in sorted(range(32),key=lambda i:exact[i]-seconds[i],reverse=True)[:900-sum(seconds)]:seconds[i]+=1
def clock(t):return f'{t//60:02d}:{t%60:02d}'
def esc(s):return html.escape(str(s))

intro='ㅇ.pdf 本文1~32쪽 기준 · 부록33~47쪽 제외 · 설명·화면 지시·전환을 포함한15분 목표 · 실제 낭독은 미측정'
intro=intro.replace('本文','본문')
guide='이번 초안은 현재 화면 순서를 따라 연습하는 용도입니다. 말할 내용은 본문, 그림을 짚는 순서는 화면 단서, 연결 문장은 선택 전환으로 나눴습니다. 확인 메모는 읽지 않습니다. 실제 시연 시간은 따로 넣지 않았습니다.'
md=['# 15분 연습용 발표 대본','',intro,'',guide,'','## 연습 방법','','처음에는 사진과 대본을 함께 보고, 두 번째부터 큐시트의 세 단서만 보고 설명합니다. 대표 수치는 화면을 보며 읽어도 됩니다. 페이지별 막힌 지점과 실제 소요 시간을 기록한 뒤 다음 초안에서 조정합니다.','']
cue=['# 15분 큐시트','',intro,'']
articles=[];entries=[];elapsed=0
for row,sec in zip(ROWS,seconds):
 n,title,_,spoken,cues,bridge=row
 assert len(cues)==3 and spoken
 interval=f'{clock(elapsed)}–{clock(elapsed+sec)} · {sec}초 목표'
 note=NOTES.get(n,'기준 PDF의 해당 장을 설명한다. 새로운 장치 실행·원실험 재측정은 수행하지 않았다.')
 entries.append(dict(pdf_page=n,title=title,seconds=sec,start_seconds=elapsed,end_seconds=elapsed+sec,spoken=spoken,cues=cues,transition=bridge,review_note=note))
 md += [f'## PDF {n:02d}. {title}','',interval,'','### 말할 내용','',spoken,'','화면 단서: '+' → '.join(cues)]
 if bridge:md += ['','넘김(선택): '+bridge]
 md += ['','확인 메모(낭독 제외): '+note,'']
 cue += [f'## {n:02d}. {title}',interval,' → '.join(cues)]
 if bridge:cue += ['넘김: '+bridge]
 cue += ['']
 bridge_html=f'<p class="bridge"><b>넘김(선택)</b> {esc(bridge)}</p>' if bridge else ''
 articles.append(f'<article id="page-{n:02d}"><header><small>{interval}</small><h2>PDF {n:02d}. {esc(title)}</h2></header><div class="practice"><div class="scene"><a href="previews/page-{n:02d}.png" target="_blank"><img loading="lazy" src="previews/page-{n:02d}.png" alt="PDF {n:02d} {esc(title)}"></a><p>PDF 실제{n}쪽 · 그림을 누르면 크게 보기</p></div><div class="spoken"><p>{esc(spoken)}</p><p class="cues"><b>화면 단서</b><br>{esc(" → ".join(cues))}</p>{bridge_html}<details><summary>확인 메모 · 낭독 제외</summary><p>{esc(note)}</p><p><a href="sources/input.pdf#page={n}">원본 PDF 해당 쪽</a> · <a href="review.md">확인 항목</a> · <a href="sources/manifest.json">동결 근거</a></p></details></div></div></article>')
 elapsed+=sec
assert elapsed==900
(BASE/'speaker-notes.md').write_text('\n'.join(md).rstrip()+'\n',encoding='utf-8')
(BASE/'cue-sheet.md').write_text('\n'.join(cue).rstrip()+'\n',encoding='utf-8')
(BASE/'script.json').write_text(json.dumps(dict(date='2026-11-24',input_pdf='sources/input.pdf',input_sha256=manifest['source_sha256'],main_pdf_pages=list(range(1,33)),excluded_appendix_pages=list(range(33,48)),total_target_seconds=900,actual_rehearsal_performed=False,slides=entries),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
css='''@font-face{font-family:P;src:url(assets/Pretendard-Regular.woff2)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{font:20px/1.9 P,sans-serif;color:#202b3a;max-width:1500px;margin:35px auto;padding:0 28px}h1,h2,a{color:#002f6d}h1{font-size:34px}h2{font-size:29px;line-height:1.5}small{color:#52687d;font-size:16px}.intro{background:#f1f5f9;padding:20px 25px;font-size:18px}.intro p{margin:5px 0}nav{display:grid;grid-template-columns:repeat(3,1fr);gap:6px 18px;font-size:16px;line-height:1.7;margin:25px 0 40px}nav a{text-decoration:none}article{padding:28px 0 45px;border-top:1px solid #bdcddd;scroll-margin-top:18px}.practice{display:grid;grid-template-columns:minmax(300px,.85fr) minmax(450px,1.15fr);gap:35px}.scene{align-self:start;position:sticky;top:18px}.scene img{width:100%;height:auto;border:1px solid #dce4ee}.scene p{font-size:15px;color:#52687d;margin:3px 0}.spoken>p{font-size:23px;line-height:1.95;margin:0 0 25px}.spoken p.cues{font-size:19px;color:#477ba9}.spoken p.bridge{font-size:19px;border-left:3px solid #477ba9;background:#f1f5f9;padding:14px 20px}details{font-size:16px;color:#52687d}summary{cursor:pointer}details p{margin:10px 0}.resources{font-size:18px}@media(max-width:950px){.practice{grid-template-columns:1fr}.scene{position:static}nav{grid-template-columns:repeat(2,1fr)}}@page{size:A4;margin:16mm}@media print{nav,.scene,details,.resources,.guide{display:none}.practice{display:block}article{break-inside:avoid;padding:16px 0 20px}body{margin:0;padding:0;font-size:12pt}.intro{padding:8px;font-size:10pt}h1{font-size:20pt}h2{font-size:15pt}.spoken>p{font-size:12pt;line-height:1.8;margin-bottom:10px}.spoken p.cues,.spoken p.bridge{font-size:10pt;margin:8px 0}small{font-size:9pt}}'''
nav=''.join(f'<a href="#page-{r[0]:02d}">{r[0]:02d} {esc(r[1])}</a>' for r in ROWS)
doc='<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>15분 연습 대본 · 본문32쪽</title><style>'+css+'</style></head><body><h1>15분 연습용 발표 대본</h1><div class="intro"><p>'+esc(intro)+'</p><p class="guide">'+esc(guide)+'</p></div><p class="resources"><a href="practice-script.pdf">인쇄용 대본 PDF</a> · <a href="cue-sheet.md">큐시트</a> · <a href="review.md">확인 항목</a> · <a href="sources/input.pdf">기준 PDF</a></p><nav>'+nav+'</nav>'+''.join(articles)+'</body></html>'
(BASE/'speaker-notes.html').write_text(doc,encoding='utf-8')
stats=dict(main_pages=32,excluded_appendix_pages=15,target_seconds=elapsed,actual_rehearsal_performed=False,hangul_characters=sum(len(re.findall('[가-힣]',s['spoken'])) for s in entries),max_hangul_per_target_second=round(max(len(re.findall('[가-힣]',s['spoken']))/s['seconds'] for s in entries),2),source_sha256=manifest['source_sha256'])
(BASE/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
