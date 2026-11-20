"""Builds the 윤관 deck from src/: index.html (발표 흐름), all-slides.html (발표 흐름 + 근거 자료), notes.md (대본) and
README.md (slide list). Edit src/slides/*.html, src/notes/*.md, src/deck.txt and src/readme_head.md, never the outputs.
usage: python src/build.py"""
import html as H
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent


def deck():
    rows = []
    for line in (SRC / 'deck.txt').read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        part, key = line.split(None, 1)
        assert part in ('main', 'appendix'), line
        body = (SRC / 'slides' / (key + '.html')).read_text(encoding='utf-8').strip()
        m = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        assert m, 'no <h1> in ' + key
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        note = SRC / 'notes' / (key + '.md')
        rows.append({'part': part, 'key': key, 'body': body, 'title': title,
                     'note': note.read_text(encoding='utf-8').strip() if note.exists() else ''})
    return rows


def clean(body):
    # team rule (work/DESIGN.md): no per-slide source-link row and no team/project text in the footer
    return re.sub(r'<footer>.*?</footer>', '', body, flags=re.S)


def page(rows, title, nav):
    n = len(rows)
    out = ['<!doctype html><html lang="ko"><head><meta charset="utf-8">'
           '<meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>%s</title><link rel="stylesheet" href="slides.css"></head><body>' % H.escape(title),
           '<nav class="team-nav" aria-label="자료 선택">%s</nav><main>' % nav]
    for i, r in enumerate(rows, 1):
        out.append('<section class="slide" data-page="%02d" aria-label="%s">%s'
                   '<div class="team-footer"><span></span><span>%02d / %02d</span></div></section>'
                   % (i, H.escape(r['title']), clean(r['body']), i, n))
    out.append('</main><div class="slide-control" aria-label="발표 이동"><button id="slide-prev" type="button">← 이전</button>'
               '<span id="slide-count"></span><button id="slide-next" type="button">다음 →</button>'
               '<button type="button" onclick="window.print()">인쇄</button></div><script src="slides.js"></script></body></html>')
    return '\n'.join(out) + '\n'


def speak_seconds(text):
    # Korean read aloud at about 300 syllables per minute; Latin words and numbers count as about 2 syllables each
    hangul = len(re.findall(r'[가-힣]', text))
    other = len(re.findall(r'[A-Za-z0-9][A-Za-z0-9.,%]*', text))
    return (hangul + 2 * other) / 5.0


def first_sentence(text):
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.match(r'(.+?[다요]\.)(\s|$)', text)
    return m.group(1) if m else text[:160]


def main():
    rows = deck()
    main_rows = [r for r in rows if r['part'] == 'main']
    (ROOT / 'index.html').write_text(page(main_rows, '윤관 · 발표 흐름',
        '<a href="all-slides.html">근거 자료까지 보기</a> · 윤관 발표 흐름 %d장' % len(main_rows)), encoding='utf-8', newline='\n')
    (ROOT / 'all-slides.html').write_text(page(rows, '윤관 · 발표 흐름과 근거 자료',
        '<a href="index.html">발표 흐름만 보기</a> · 1–%d장 발표 흐름, %d–%d장 근거 자료' % (len(main_rows), len(main_rows) + 1, len(rows))),
        encoding='utf-8', newline='\n')
    secs = [speak_seconds(r['note']) for r in main_rows]
    notes = ['# 윤관 발표 대본', '',
             '발표 흐름 %d장과 같은 순서입니다. 소리 내어 읽는 속도(분당 약 300음절)로 어림하면 약 %d분입니다. 실제 리허설 시간이 아닙니다.'
             % (len(main_rows), round(sum(secs) / 60)),
             '세부 조건과 원문은 [sources.md](sources.md)와 [슬라이드별 근거](근거_슬라이드별.md), 근거 장은 [all-slides.html](all-slides.html)에 있습니다.', '']
    for i, (r, sec) in enumerate(zip(main_rows, secs), 1):
        notes += ['## %02d · %s' % (i, r['title']), '', r['note'] or '(대본 없음)', '', '*약 %d초*' % round(sec), '']
    src = ['# 슬라이드별 근거', '', '발표 흐름 각 장의 숫자와 주장이 어디에서 왔는지 적었습니다. `src/sources/`에서 생성합니다.', '']
    for i, r in enumerate(main_rows, 1):
        f = SRC / 'sources' / (r['key'] + '.md')
        src += ['## %02d · %s' % (i, r['title']), '', f.read_text(encoding='utf-8').strip() if f.exists() else '(근거 없음)', '']
    (ROOT / '근거_슬라이드별.md').write_text('\n'.join(src), encoding='utf-8', newline='\n')
    (ROOT / 'notes.md').write_text('\n'.join(notes), encoding='utf-8', newline='\n')
    readme = [(SRC / 'readme_head.md').read_text(encoding='utf-8').rstrip(), '']
    section = None
    for i, r in enumerate(main_rows, 1):
        m = re.search(r'data-section="([^"]+)"', r['body'])
        if m and m.group(1) != section:
            section = m.group(1)
            readme += ['## ' + section, '']
        readme += ['### %02d. %s' % (i, r['title']), '',
                   '![%s](assets/readme-slides/slide-%02d.jpg)' % (r['title'], i), '',
                   first_sentence(r['note']) if r['note'] else '', '']
    (ROOT / 'README.md').write_text('\n'.join(readme).rstrip() + '\n', encoding='utf-8', newline='\n')
    print('built: %d main + %d appendix slides' % (len(main_rows), len(rows) - len(main_rows)))


if __name__ == '__main__':
    main()
