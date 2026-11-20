"""Preview a few slides without touching the built files: writes _preview_<name>.html next to index.html (so slides.css and
assets/ resolve), screenshots each slide to <out dir>/<key>.png and prints a layout check. Delete the html afterwards
(the script does it unless --keep).
usage: python src/preview.py <name> <out dir> <key> [<key> ...] [--keep]"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402
import render  # noqa: E402

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    name, out, keys = args[0], Path(args[1]), args[2:]
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for k in keys:
        body = (SRC / 'slides' / (k + '.html')).read_text(encoding='utf-8').strip()
        import re
        m = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        rows.append({'part': 'main', 'key': k, 'body': body, 'title': re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else k, 'note': ''})
    page = ROOT / ('_preview_%s.html' % name)
    page.write_text(build.page(rows, 'preview', 'preview'), encoding='utf-8', newline='\n')
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 1920, 'height': 1080})
            errors = []
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            pg.goto(page.as_uri())
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(400)
            res = pg.evaluate(render.CHECK)
            pg.emulate_media(media='print')
            for k, s in zip(keys, pg.query_selector_all('section.slide')):
                s.screenshot(path=str(out / (k + '.png')), scale='css')
            b.close()
    finally:
        if '--keep' not in sys.argv:
            page.unlink(missing_ok=True)
    for k, r in zip(keys, res):
        words = None
        print('%s: %s' % (k, '; '.join(r['problems']) if r['problems'] else 'ok'))
    if errors:
        print('console errors:', errors)
    print('screenshots in', out)


if __name__ == '__main__':
    main()
