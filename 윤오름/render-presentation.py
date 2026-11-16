"""Render the nine-slide draft with installed Chrome and check layout/assets."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from pypdf import PdfReader

root = Path(__file__).resolve().parent
out = root / 'previews'
out.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', headless=True)
    page = browser.new_page(viewport={'width': 2040, 'height': 1240}, device_scale_factor=1)
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto((root / 'index.html').as_uri(), wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    assets = page.evaluate("""() => ({images:[...document.images].map(i=>({src:i.getAttribute('src'),ok:i.complete&&i.naturalWidth>0})),font:document.fonts.check('36px Pretendard')})""")
    assert all(i['ok'] for i in assets['images']), assets
    assert assets['font'], assets
    checks = page.evaluate("""() => [...document.querySelectorAll('.slide')].map(s=>{
      const r=s.getBoundingClientRect(), source=(s.querySelector('.source')||s.querySelector('.slide-footer')).getBoundingClientRect();
      const outside=[...s.querySelectorAll('.content *, .cover-copy, .cover-figure, .scenario-intro, .operation-flow, .feedback-loop, .scenario-note')].filter(e=>{const b=e.getBoundingClientRect();return b.width&&b.height&&(b.left<r.left-1||b.right>r.right+1||b.bottom>source.top-5)}).map(e=>({tag:e.tagName,text:e.textContent.slice(0,65),bottom:Math.round(e.getBoundingClientRect().bottom-r.top)}));
      return {page:s.dataset.page,outside};
    })""")
    for slide in page.locator('.slide').all():
        slide.screenshot(path=str(out / ('slide-' + slide.get_attribute('data-page') + '.png')))
    page.emulate_media(media='print')
    page.pdf(path=str(root / 'presentation.pdf'), print_background=True, prefer_css_page_size=True, display_header_footer=False)
    # Verify a small browser viewport uses scaling without horizontal overflow.
    page.emulate_media(media='screen')
    page.set_viewport_size({'width': 1280, 'height': 900})
    page.wait_for_timeout(200)
    responsive = page.evaluate('document.documentElement.scrollWidth <= innerWidth')
    browser.close()

pdf = PdfReader(root / 'presentation.pdf')
assert len(pdf.pages) == 9, len(pdf.pages)
assert [c['page'] for c in checks] == ['01', '02', '03', '04', '05', '10', '11', '12', '13']
for i, pg in enumerate(pdf.pages):
    assert abs(float(pg.mediabox.width) - 1440) < 1
    assert abs(float(pg.mediabox.height) - 810) < 1
    assert len(pg.extract_text()) > 100, i
report = {'slides': 9, 'pdf_pages': len(pdf.pages), 'pdf_size_points': [1440, 810], 'assets': assets, 'layout': checks, 'responsive_1280': responsive, 'javascript_errors': errors}
(out / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=True, indent=2))
assert responsive and not errors
assert not any(c['outside'] for c in checks), 'Content overlaps source or exceeds slide; inspect validation.json'
