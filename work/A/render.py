"""HTML을 실제 Chromium으로 검증하고 PDF·미리보기를 출력한다.

의존성: playwright, pymupdf. 브라우저: playwright install chromium.
브라우저 실행 파일은 LWIR_SLIDE_BROWSER 환경변수로 지정할 수 있다.
"""
from pathlib import Path
import json
import os
import re
from playwright.sync_api import sync_playwright
import pymupdf

BASE=Path(__file__).resolve().parent
OUT=BASE/'previews'
OUT.mkdir(exist_ok=True)

def render(name, pdfname, prefix):
 errors=[]
 with sync_playwright() as p:
  kwargs={'headless':True,'args':['--no-sandbox','--disable-dev-shm-usage']}
  if os.environ.get('LWIR_SLIDE_BROWSER'):kwargs['executable_path']=os.environ['LWIR_SLIDE_BROWSER']
  elif Path('C:/Program Files/Google/Chrome/Application/chrome.exe').exists():kwargs['executable_path']='C:/Program Files/Google/Chrome/Application/chrome.exe'
  browser=p.chromium.launch(**kwargs)
  page=browser.new_page(viewport={'width':1920,'height':1180},device_scale_factor=1)
  page.on('pageerror',lambda err:errors.append(str(err)))
  page.goto((BASE/name).as_uri(),wait_until='networkidle')
  page.evaluate('document.fonts.ready')
  page.emulate_media(media='print')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  page.wait_for_timeout(300)
  checks=page.evaluate('''() => [...document.querySelectorAll('.slide')].map((s,i)=>{
   const box=s.getBoundingClientRect(), source=s.querySelector('.slide-source').getBoundingClientRect();
   const problems=[];
   for(const el of s.querySelectorAll('main p, main li, main h2, main h3, main table, main figure, main .flow, main .takeaway, main .team-strip, main .closing, main .demo-cues')){
    const r=el.getBoundingClientRect();
    if(r.width&&r.height&&(r.right>box.right-70||r.left<box.left+65||r.bottom>source.top-9))problems.push({tag:el.tagName,text:el.textContent.slice(0,70),right:r.right-box.left,bottom:r.bottom-box.top,limit:source.top-box.top});
   }
   return {slide:i+1,width:box.width,height:box.height,title:s.querySelector('h1').textContent,problems};
  })''')
  images=page.evaluate('''()=>[...document.images].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0}))''')
  fonts=page.evaluate("document.fonts.check('32px Pretendard')")
  page.pdf(path=str(BASE/pdfname),prefer_css_page_size=True,print_background=True)
  doc=pymupdf.open(BASE/pdfname)
  # PDF를 다시 이미지로 만들어 실제 출력 산출물을 확인한다.
  for i,pdfpage in enumerate(doc):
   pdfpage.get_pixmap(matrix=pymupdf.Matrix(0.8,0.8),alpha=False).save(OUT/f'{prefix}-{i+1:02d}.png')
  cols=3; cellw=480; cellh=300; rows=(len(doc)+cols-1)//cols
  contact=pymupdf.open(); sheet=contact.new_page(width=cols*cellw,height=rows*cellh)
  for i,pdfpage in enumerate(doc):
   x=(i%cols)*cellw;y=(i//cols)*cellh
   sheet.show_pdf_page(pymupdf.Rect(x+6,y+6,x+cellw-6,y+cellh-24),doc,i)
   sheet.insert_text((x+12,y+cellh-8),f'{i+1:02d}',fontsize=12,color=(.1,.15,.2))
  sheet.get_pixmap(alpha=False).save(OUT/f'{prefix}-overview.png')
  dimensions=[[round(pg.rect.width,2),round(pg.rect.height,2)] for pg in doc]
  page.emulate_media(media='screen');page.set_viewport_size({'width':1280,'height':800})
  page.wait_for_timeout(200)
  if name=='index.html':
   page.keyboard.press('Home');page.keyboard.press('ArrowRight')
   navigation=page.locator('.slide.active').get_attribute('data-number')=='2'
   page.keyboard.press('End');navigation= navigation and page.locator('.slide.active').get_attribute('data-number')==str(page.locator('.slide').count())
   page.keyboard.press('Home');page.screenshot(path=str(OUT/'screen-1280.png'))
  else:navigation=None
  browser.close()
 report={'html':name,'pdf':pdfname,'slides':len(checks),'pdf_pages':len(doc),'page_points':dimensions,'fonts_loaded':fonts,'images':images,'javascript_errors':errors,'layout':checks,'keyboard_navigation':navigation,'demo_included':(BASE/'assets/rooftop-demo.mp4').exists()}
 doc.close();return report

reports=[render('index.html','presentation.pdf','slide')]
if (BASE/'appendix.html').exists():reports.append(render('appendix.html','appendix.pdf','appendix'))
manifest=json.loads((BASE/'deck.json').read_text(encoding='utf-8'))
report={'target_seconds':sum(s['seconds'] for s in manifest['slides']),'demo_slot_seconds':manifest['demo_seconds'],'spoken_hangul_chars':sum(len(re.findall('[가-힣]',s['spoken'])) for s in manifest['slides'] if s['section']!='통합 데모 · 3분'),'actual_rehearsal_performed':False,'reports':reports}
(BASE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in reports:
 print(r['html'],r['slides'],'slides /',r['pdf_pages'],'PDF pages / layout issues',sum(len(x['problems']) for x in r['layout']),'JS errors',len(r['javascript_errors']))
print('Target',report['target_seconds'],'seconds. Actual speaking time not measured. Demo file present:',reports[0]['demo_included'])
assert report['target_seconds']==1200 and manifest['demo_seconds']==180
assert [r['pdf_pages'] for r in reports]==[len(manifest['slides']),18]
for r in reports:
 assert r['slides']==r['pdf_pages']
 assert r['fonts_loaded'] and all(i['ok'] for i in r['images'])
 assert not r['javascript_errors']
 assert not any(x['problems'] for x in r['layout']), 'Layout problems recorded in validation.json'
 assert all(w==1440 and h==810 for w,h in r['page_points'])
assert reports[0]['keyboard_navigation']
