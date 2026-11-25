"""Read the canonical Markdown; derive practice files and PPTX note payloads.

This never rewrites speaker-notes.md or modifies a PPTX. Later note insertion
must first match the latest PPTX slides against the source PDF content/order.
"""
from pathlib import Path
import hashlib,html,json,re

BASE=Path(__file__).resolve().parent
md=(BASE/'speaker-notes.md').read_text(encoding='utf-8')
manifest=json.loads((BASE/'sources/manifest.json').read_text(encoding='utf-8'))
source=json.loads((BASE/'sources/pdf-pages.json').read_text(encoding='utf-8'))
assert source['count']==50 and manifest['main_pages']==list(range(1,36))
assert hashlib.sha256((BASE/'sources/work.pdf').read_bytes()).hexdigest()==manifest['input_sha256']
for item in manifest['evidence']:
 assert hashlib.sha256((BASE/item['path']).read_bytes()).hexdigest()==item['sha256']
blocks=re.split(r'^## (\d{2})\. (.+)\n',md,flags=re.M)
entries=[]
for i in range(1,len(blocks),3):
 n=int(blocks[i]);title=blocks[i+1].strip();text=blocks[i+2]
 # The Markdown goes directly from the page title to narration. Accept the
 # old optional label when reading older drafts; never generate that label.
 narration=text.split('\n화면 단서:',1)[0]
 spoken=re.sub(r'^\s*###\s*말할\s*내용\s*\n','',narration).strip()
 cues=re.search(r'^화면 단서: (.+)$',text,re.M).group(1).split(' → ')
 bridge=re.search(r'^넘김: (.+)$',text,re.M)
 bridge=bridge.group(1).strip() if bridge else ''
 assert len(cues)==3 and spoken and (BASE/f'previews/page-{n:02d}.png').is_file()
 entries.append(dict(pdf_page=n,title=title,spoken=spoken,cues=cues,transition=bridge,pptx_notes=spoken+('\n\n'+bridge if bridge else ''),source_page_text_sha256=hashlib.sha256(source['pages'][n-1]['text'].encode()).hexdigest()))
assert [e['pdf_page'] for e in entries]==list(range(1,36))
weights=[len(re.findall('[가-힣]',e['spoken'])) for e in entries]
exact=[4+(900-4*len(entries))*w/sum(weights) for w in weights];allocated=[int(x) for x in exact]
for i in sorted(range(35),key=lambda i:exact[i]-allocated[i],reverse=True)[:900-sum(allocated)]:allocated[i]+=1
def clock(t):return f'{t//60:02d}:{t%60:02d}'
def esc(s):return html.escape(str(s))
elapsed=0;cue=['# 큐시트 · work.pdf 본문35쪽','','15분 목표·부록 제외·실제 낭독 미측정. 문장 수정은 speaker-notes.md에서 한다.',''];rows=[];articles=[]
for e,t in zip(entries,allocated):
 n=e['pdf_page'];e.update(seconds=t,start_seconds=elapsed,end_seconds=elapsed+t)
 interval=f'{clock(elapsed)}–{clock(elapsed+t)} · {t}초 목표'
 cue += [f'## {n:02d}. {e["title"]}',interval,' → '.join(e['cues'])]
 if e['transition']:cue+=['넘김: '+e['transition']]
 cue+=['']
 rows.append(f'| {n:02d} | {e["title"]} | {clock(elapsed)}–{clock(elapsed+t)} | {t}초 |')
 bridge=f'<p class="bridge"><b>넘김</b> {esc(e["transition"])}</p>' if e['transition'] else ''
 paragraphs=''.join('<p>'+esc(p)+'</p>' for p in e['spoken'].split('\n\n'))
 articles.append(f'<article id="page-{n:02d}"><small>{interval}</small><h2>{n:02d}. {esc(e["title"])}</h2><div class="practice"><div class="scene"><a href="previews/page-{n:02d}.png"><img loading="lazy" src="previews/page-{n:02d}.png" alt="PDF{n}쪽"></a></div><div class="spoken">{paragraphs}<p class="cues">{esc(" → ".join(e["cues"]))}</p>{bridge}</div></div></article>')
 elapsed+=t
assert elapsed==900
(BASE/'cue-sheet.md').write_text('\n'.join(cue).rstrip()+'\n',encoding='utf-8')
(BASE/'timing.md').write_text('# 시간 배정\n\n본문35쪽·900초 목표. 실제 낭독 미측정.\n\n| 쪽 | 제목 | 누적 시간 | 배정 |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n',encoding='utf-8')
payload=dict(date='2026-11-25',canonical_source='speaker-notes.md',canonical_sha256=hashlib.sha256((BASE/'speaker-notes.md').read_bytes()).hexdigest(),source_pdf='sources/work.pdf',source_pdf_sha256=manifest['input_sha256'],total_pdf_pages=50,main_pages=35,excluded_appendix_pages=list(range(36,51)),target_seconds=900,pptx_modified=False,actual_rehearsal_performed=False,slides=entries)
(BASE/'notes-map.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
css='''@font-face{font-family:P;src:url(assets/Pretendard-Regular.woff2)}*{box-sizing:border-box}body{font:21px/1.85 P,sans-serif;max-width:1500px;margin:35px auto;padding:0 28px;color:#202b3a}h1,h2,a{color:#002f6d}h1{font-size:34px}h2{font-size:29px}small{font-size:16px;color:#52687d}.intro{font-size:18px;background:#f1f5f9;padding:18px 24px}nav{display:grid;grid-template-columns:repeat(3,1fr);gap:8px 20px;font-size:16px;margin:25px 0 40px}article{border-top:1px solid #bdcddd;padding:30px 0 42px;scroll-margin-top:15px}.practice{display:grid;grid-template-columns:minmax(300px,.85fr) minmax(450px,1.15fr);gap:35px}.scene{align-self:start;position:sticky;top:15px}.scene img{width:100%;border:1px solid #dce4ee}.spoken p{font-size:23px;line-height:1.95;margin:0 0 24px}.spoken p.cues{font-size:19px;color:#477ba9}.spoken p.bridge{font-size:19px;padding:12px 18px;background:#f1f5f9;border-left:3px solid #477ba9}@media(max-width:950px){.practice{grid-template-columns:1fr}.scene{position:static}nav{grid-template-columns:repeat(2,1fr)}}'''
nav=''.join(f'<a href="#page-{e["pdf_page"]:02d}">{e["pdf_page"]:02d} {esc(e["title"])}</a>' for e in entries)
(BASE/'speaker-notes.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>work.pdf 발표 대본</title><style>'+css+'</style><h1>발표 대본 · work.pdf</h1><p class="intro">본문1~35쪽·15분 목표·부록36~50쪽 제외·낭독 미측정. <a href="speaker-notes.md">MD 원문</a> · <a href="cue-sheet.md">큐시트</a> · <a href="review.md">확인 메모</a></p><nav>'+nav+'</nav>'+''.join(articles)+'</html>',encoding='utf-8')
stats=dict(main_pages=35,excluded_appendix_pages=15,target_seconds=900,hangul_characters=sum(weights),max_hangul_per_target_second=round(max(w/t for w,t in zip(weights,allocated)),2),actual_rehearsal_performed=False,canonical_md_sha256=payload['canonical_sha256'],source_pdf_sha256=manifest['input_sha256'])
(BASE/'validation.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(stats,ensure_ascii=False))
