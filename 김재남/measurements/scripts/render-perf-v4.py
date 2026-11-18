import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from pypdf import PdfReader
from PIL import Image
root=Path('/home/user/workspace/mypresentaion/v4')
checks={}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1360,'height':820},device_scale_factor=1)
 errors=[]; remote=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:remote.append(r.url) if r.url.startswith(('http:','https:')) else None)
 for source,pdfname,count in [('index.html','presentation.pdf',8),('performance.html','performance.pdf',4)]:
  page.emulate_media(media='screen');page.goto((root/source).as_uri(),wait_until='networkidle');page.evaluate('document.fonts.ready')
  for im in page.locator('img').all():im.evaluate('(i)=>i.decode()')
  names=['slide-05.png','slide-08.png','slide-11.png','slide-12.png']+[f'slide-P{i}.png' for i in range(1,5)] if count==8 else [f'slide-P{i}.png' for i in range(1,5)]
  for name,s in zip(names,page.locator('.slide').all()):s.screenshot(path=str(root/name))
  check=page.evaluate('''()=>({fonts:document.fonts.check('24px Pretendard'),images:[...document.images].every(i=>i.complete&&i.naturalWidth>0),slides:[...document.querySelectorAll('.slide')].map(s=>{let r=s.getBoundingClientRect();return {width:s.offsetWidth,height:s.offsetHeight,overflow:[...s.querySelectorAll('*')].filter(e=>{let b=e.getBoundingClientRect();return b.width&&b.height&&(b.left<r.left-.5||b.right>r.right+.5||b.top<r.top-.5||b.bottom>r.bottom+.5)}).map(e=>e.tagName+'.'+e.className)}})})''')
  page.emulate_media(media='print');page.pdf(path=str(root/pdfname),prefer_css_page_size=True,print_background=True,display_header_footer=False)
  pdf=PdfReader(root/pdfname);check['pages']=len(pdf.pages);check['pdf_points']=[[float(x) for x in pg.mediabox[2:]] for pg in pdf.pages];check['text_chars']=[len(pg.extract_text()) for pg in pdf.pages]
  checks[source]=check
  assert check['pages']==count and check['fonts'] and check['images']
  assert all(not s['overflow'] for s in check['slides']),check
  assert all(abs(w-960)<1 and abs(h-540)<1 for w,h in check['pdf_points'])
 browser.close()
checks.update(javascript_errors=errors,remote_requests=remote)
(root/'validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
for name,names in [('overview.png',['slide-05.png','slide-08.png','slide-11.png','slide-12.png']+[f'slide-P{i}.png' for i in range(1,5)]),('performance-overview.png',[f'slide-P{i}.png' for i in range(1,5)])]:
 canvas=Image.new('RGB',(1280,360*((len(names)+1)//2)),'white')
 for i,n in enumerate(names):canvas.paste(Image.open(root/n).resize((640,360)),(640*(i%2),360*(i//2)))
 canvas.save(root/name)
assert not errors and not remote
print(json.dumps(checks,ensure_ascii=False))
