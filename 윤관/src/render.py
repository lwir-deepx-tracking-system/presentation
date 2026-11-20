"""Renders the built deck with Playwright (Chromium): 발표_전체흐름.pdf (index.html), 발표_전체근거.pdf (all-slides.html),
assets/readme-slides/slide-NN.jpg (index.html, 1280x720) and a layout check (src/render_check.json).
usage: python src/render.py [--no-pdf] [--check-only]"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent

CHECK = r"""() => {
  const out = [];
  document.querySelectorAll('section.slide').forEach((s, i) => {
    const sb = s.getBoundingClientRect(), probs = [];
    const art = s.querySelector('.content-slide');
    s.querySelectorAll('*').forEach(e => {
      if (e.closest('.team-footer') || e === art) return;
      const st = getComputedStyle(e);
      if (st.display === 'none' || st.visibility === 'hidden') return;
      const r = e.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      const tag = e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : '');
      if (r.right > sb.right + 1 || r.bottom > sb.bottom - 22 || r.left < sb.left - 1 || r.top < sb.top - 1)
        probs.push('outside ' + tag + ' ' + (e.textContent || '').trim().slice(0, 40));
      if (['text', 'tspan'].includes(e.tagName.toLowerCase())) return;
      const own = [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (own && (e.scrollWidth > e.clientWidth + 2 || e.scrollHeight > e.clientHeight + 2) && st.overflow !== 'visible')
        probs.push('clipped ' + tag + ' ' + e.textContent.trim().slice(0, 40));
      if (own) {
        const px = parseFloat(st.fontSize) * 1.5;   // slides are drawn at 1280x720 and scaled x1.5 to 1920x1080
        if (px < 21) probs.push('small ' + Math.round(px) + 'px ' + tag + ' ' + e.textContent.trim().slice(0, 30));
      }
    });
    s.querySelectorAll('img').forEach(im => { if (!im.complete || im.naturalWidth === 0) probs.push('image missing ' + im.getAttribute('src')); });
    out.push({page: i + 1, title: s.getAttribute('aria-label'), problems: [...new Set(probs)]});
  });
  return out;
}"""


def run(name, pdf, shots, check, pw):
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    errors = []
    pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errors.append(str(e)))
    pg.goto((ROOT / name).as_uri())
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    fonts = pg.evaluate("[...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight)")
    res = pg.evaluate(CHECK) if check else []
    if shots:
        pg.emulate_media(media='print')
        out = ROOT / 'assets' / 'readme-slides'
        out.mkdir(parents=True, exist_ok=True)
        for old in out.glob('slide-*.jpg'):
            old.unlink()
        for i, s in enumerate(pg.query_selector_all('section.slide'), 1):
            s.screenshot(path=str(out / ('slide-%02d.jpg' % i)), type='jpeg', quality=82, scale='css')
        pg.emulate_media(media='screen')
    if pdf:
        pg.emulate_media(media='print')
        pg.pdf(path=str(ROOT / pdf), width='1920px', height='1080px', print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
    b.close()
    return {'file': name, 'errors': errors, 'fonts': fonts, 'slides': res}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    no_pdf = '--no-pdf' in sys.argv
    check_only = '--check-only' in sys.argv
    with sync_playwright() as pw:
        a = run('index.html', None if (no_pdf or check_only) else '발표_전체흐름.pdf', not check_only, True, pw)
        b = run('all-slides.html', None if (no_pdf or check_only) else '발표_전체근거.pdf', False, True, pw)
    (SRC / 'render_check.json').write_text(json.dumps([a, b], ensure_ascii=False, indent=1), encoding='utf-8', newline='\n')
    for r in (a, b):
        bad = [s for s in r['slides'] if s['problems']]
        print(r['file'], 'errors', len(r['errors']), 'fonts', r['fonts'], 'slides with problems', len(bad), '/', len(r['slides']))
        for s in bad[:60]:
            print('  %02d %s: %s' % (s['page'], s['title'], '; '.join(s['problems'][:4])))


if __name__ == '__main__':
    main()
