"""Freeze selected team diagrams and images before adapting their layouts."""
from pathlib import Path
import hashlib
import json
import shutil

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
SOURCE=ROOT/'윤관'
DEST=BASE/'sources/visual-reference'
slides=['k09_id_keep','m09_data','m13_labeling','m11_occlusion_aug','m14_body_box','m10_pose_lineage','m18_e10','m19_retrain','m21b_reid_table',
        'm22_position','m29_split','m29b_split_model','m30_tail','m31_gimbal_loop',
        'm32_pd','m33_plant','k08_virtual_cam','m25_fullbody','m27_int8']
assets=['실제_라벨링_실내.png','실제_라벨링_야외.png','m11-occlusion-aug.jpg',
        'openthermalpose2-official-example.png','OPENTHERMALPOSE-LICENSE.txt',
        '20261119-real-upper-replay.jpg','20261119-real-full-replay.jpg',
        'gimbal-s7-actual.svg']
records=[]
for name in slides:
    source=SOURCE/'src/slides'/f'{name}.html'
    target=DEST/'slides'/source.name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    records.append(dict(source=source.relative_to(ROOT).as_posix(),file=target.relative_to(BASE).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
for name in assets:
    source=SOURCE/'assets'/name
    target=BASE/'assets/visuals'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    records.append(dict(source=source.relative_to(ROOT).as_posix(),file=target.relative_to(BASE).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
(DEST/'manifest.json').write_text(json.dumps(dict(files=records,method='Selected source SVGs and photographs adapted into C layouts.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Frozen',len(slides),'source diagrams and',len(assets),'visual assets')
