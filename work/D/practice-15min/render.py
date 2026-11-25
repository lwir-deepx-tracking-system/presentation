"""Print the spoken draft and check the reader locally with Chromium."""
from pathlib import Path
from urllib.parse import unquote
import json,re
import pymupdf
from playwright.sync_api import sync_playwright

BASE=Path(__file__).resolve().parent
data=json.loads((BASE/'script.json').read_text(encoding='utf-8'))
assert [s['pdf_page'] for s in data['slides']]==list(range(1,33))
assert sum(s['seconds'] for s in data['slides'])==900
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 page=browser.new_page(viewport={'width':1500,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((BASE/'speaker-notes.html').as_uri(),wait_until='networkidle')
 page.locator('img').evaluate_all('(xs)=>xs.forEach(i=>i.loading="eager")')
 page.evaluate('document.fonts.ready');page.wait_for_load_state('networkidle')
 assert page.locator('article').count()==32 and page.locator('article details').count()==32
 assert page.locator('#page-33').count()==0
 images=page.locator('img').evaluate_all('(xs)=>xs.map(i=>({src:i.getAttribute("src"),ok:i.complete&&i.naturalWidth>0}))')
 assert len(images)==32 and all(i['ok'] for i in images)
 assert page.evaluate('document.fonts.check("23px P")')
 page.emulate_media(media='print')
 page.pdf(path=str(BASE/'practice-script.pdf'),prefer_css_page_size=True,print_background=True)
 doc=pymupdf.open(BASE/'practice-script.pdf');txt='\n'.join(p.get_text() for p in doc)
 for n in range(1,33):assert f'PDF {n:02d}.' in txt,n
 assert 'PDF 33.' not in txt and '확인 메모 · 낭독 제외' not in txt
 pdf_pages=len(doc);doc.close()
 page.emulate_media(media='screen')
 checked_links=0
 for href in page.locator('a').evaluate_all('(xs)=>xs.map(a=>a.getAttribute("href"))'):
  if href.startswith('#'):assert page.locator(href).count()==1
  elif not href.startswith('http'):
   assert (BASE/unquote(href.split('#')[0])).is_file(),href
   checked_links+=1
 for n in [1,15,25,32]:
  page.goto((BASE/'speaker-notes.html').as_uri()+f'#page-{n:02d}',wait_until='networkidle')
  page.evaluate(f'document.getElementById("page-{n:02d}").scrollIntoView()')
  page.wait_for_timeout(200)
  if n==25:
   page.locator('#page-25 summary').click()
   assert page.locator('#page-25 details').get_attribute('open') is not None
  page.screenshot(path=str(BASE/f'previews/reader-{n:02d}.png'))
 assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
 page.set_viewport_size({'width':800,'height':1000})
 assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
 assert not errors;browser.close()
report=json.loads((BASE/'validation.json').read_text(encoding='utf-8'))
report.update(browser=dict(articles=32,images=32,details=32,local_links=checked_links,javascript_errors=errors,fonts_loaded=True,desktop_and_mobile_horizontal_overflow=False),printed_script_pdf_pages=pdf_pages,printed_script_excludes_review_notes=True)
(BASE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Validated32 main entries /900s /32 images / local links and fonts / no JS errors; print PDF{pdf_pages}pages. No real rehearsal performed.')
