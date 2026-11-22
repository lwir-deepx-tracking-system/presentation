"""Freeze the two 11/22 team commits separately from earlier evidence."""
from pathlib import Path
import hashlib
import json
import shutil

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
SOURCE=ROOT/'윤관'
DEST=BASE/'sources/revision-20261122'
files=['README.md','notes.md','근거_슬라이드별.md','평가자_검토.md',
       'src/notes/k09_id_keep.md','src/notes/k10_judgement.md','src/notes/m18_e10.md',
       'src/notes/m21b_reid_table.md','src/notes/m23_position_result.md','src/notes/m24_box_stab.md',
       'src/notes/m29b_split_model.md','src/notes/k08_virtual_cam.md','src/notes/k06_gimbal.md',
       'src/notes/m35_speed.md','src/notes/m38_summary.md','src/notes/k05_stability.md',
       'src/sources/k09_id_keep.md','src/sources/k10_judgement.md',
       'src/sources/m18_e10.md','src/sources/m21b_reid_table.md','src/sources/m38_summary.md',
       'src/slides/k10_judgement.html']
records=[]
for relative in files:
    original=SOURCE/relative
    target=DEST/'윤관'/relative
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(original,target)
    records.append(dict(source=original.relative_to(ROOT).as_posix(),file=target.relative_to(BASE).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
for name in ['model-bank-handoff-own9e.md','model-bank-recommended.json']:
    target=DEST/name
    records.append(dict(source='model-bank@0e3dd540/'+name,file=target.relative_to(BASE).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(DEST/'manifest.json').write_text(json.dumps(dict(commits=['4a93594','8a195d7'],model_bank_commit='0e3dd540ff8a9953a6e7725f59393c782a3d9d5a',files=records),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Frozen',len(records),'revision evidence files')
