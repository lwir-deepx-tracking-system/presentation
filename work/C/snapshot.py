"""Freeze the supplied team evidence; run only when intentionally refreshing sources."""
from pathlib import Path
import hashlib
import json
import shutil

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
dest = BASE / 'sources/latest-20261121'
dest.mkdir(exist_ok=True)
files = (list((ROOT/'윤관').glob('*.md'))
         + list((ROOT/'윤관/학습로그').glob('*.csv'))
         + [ROOT/'정하건/정하건_v3/발표노트.md', ROOT/'정하건/정하건_v3/근거_비교표.md',
            ROOT/'윤관/발표_전체근거.pdf'])
manifest = []
for file in files:
    target = dest / file.relative_to(ROOT)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, target)
    manifest.append(dict(path=file.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
(dest/'manifest.json').write_text(json.dumps(dict(commit='4836142', files=manifest), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Snapshotted {len(files)} evidence files')
