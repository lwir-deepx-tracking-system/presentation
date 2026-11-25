"""Insert approved Markdown narration into a copy, preserving slide assets.

Edits existing notes body placeholders, creates missing notes-slide parts,
and adds only their relationships/content types. It does not resave slide
shapes through a presentation library, so unsupported effects/media survive.
"""
from pathlib import Path
import argparse
from xml.dom import minidom
import collections,hashlib,json,posixpath,re,zipfile

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
SOURCE=BASE/'E.pptx'
OUTPUT=BASE/'E_발표자노트.pptx'
SCRIPT=ROOT/'work/D/work-pdf-20261125'
CANONICAL_MD=BASE/'speaker-notes.md'
NS_P='http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A='http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS_REL='http://schemas.openxmlformats.org/package/2006/relationships'
NS_CT='http://schemas.openxmlformats.org/package/2006/content-types'
NOTES_TYPE=NS_R+'/notesSlide'

def resolve(part,target):
 return target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(part),target))

def relpath(part):
 return posixpath.join(posixpath.dirname(part),'_rels',posixpath.basename(part)+'.rels')

def xml(data):return minidom.parseString(data)
def serialize(doc):return doc.toxml(encoding='utf-8')
def relationships(doc):return list(doc.getElementsByTagNameNS(NS_REL,'Relationship'))

def document_text(doc):
 return '\n'.join(''.join(c.data for c in t.childNodes if c.nodeType in (c.TEXT_NODE,c.CDATA_SECTION_NODE)) for t in doc.getElementsByTagNameNS(NS_A,'t'))

def body_shape(doc):
 for sp in doc.getElementsByTagNameNS(NS_P,'sp'):
  for ph in sp.getElementsByTagNameNS(NS_P,'ph'):
   if ph.getAttribute('type')=='body':return sp
 return None

def replace_notes(data,text,template):
 doc=xml(data);sp=body_shape(doc)
 if sp is None:
  template_body=body_shape(xml(template));assert template_body is not None
  sp=doc.importNode(template_body,deep=True)
  existing_ids=[int(n.getAttribute('id')) for n in doc.getElementsByTagNameNS(NS_P,'cNvPr')]
  sp.getElementsByTagNameNS(NS_P,'cNvPr')[0].setAttribute('id',str(max(existing_ids,default=1)+1))
  doc.getElementsByTagNameNS(NS_P,'spTree')[0].appendChild(sp)
 bodies=sp.getElementsByTagNameNS(NS_P,'txBody')
 if bodies:body=bodies[0]
 else:
  body=doc.createElementNS(NS_P,'p:txBody');sp.appendChild(body)
  body.appendChild(doc.createElementNS(NS_A,'a:bodyPr'));body.appendChild(doc.createElementNS(NS_A,'a:lstStyle'))
 for child in list(body.childNodes):
  if child.nodeType==child.ELEMENT_NODE and child.namespaceURI==NS_A and child.localName=='p':body.removeChild(child)
 for line in text.split('\n'):
  para=doc.createElementNS(NS_A,'a:p')
  if line:
   run=doc.createElementNS(NS_A,'a:r');props=doc.createElementNS(NS_A,'a:rPr');props.setAttribute('lang','ko-KR')
   run.appendChild(props);t=doc.createElementNS(NS_A,'a:t');t.appendChild(doc.createTextNode(line));run.appendChild(t);para.appendChild(run)
  body.appendChild(para)
 return serialize(doc)

def body_text(data):
 sp=body_shape(xml(data));assert sp is not None
 tx=sp.getElementsByTagNameNS(NS_P,'txBody')[0]
 return '\n'.join(document_text(p) for p in tx.childNodes if p.nodeType==p.ELEMENT_NODE and p.namespaceURI==NS_A and p.localName=='p')

def grams(s):
 s=re.sub('[^가-힣a-zA-Z0-9]','',s).lower()
 return collections.Counter(s[i:i+3] for i in range(max(0,len(s)-2)))

def main():
 global OUTPUT
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',default=OUTPUT.name,help='Output filename under work/E; use a new filename when an older copy is open.')
 args=parser.parse_args()
 assert Path(args.output).name==args.output and args.output.lower().endswith('.pptx')
 OUTPUT=BASE/args.output
 assert OUTPUT.resolve()!=SOURCE.resolve(),'The original E.pptx must not be overwritten.'
 md_bytes=CANONICAL_MD.read_bytes()
 blocks=re.split(r'^## (\d{2})\. (.+)\n',md_bytes.decode('utf-8-sig').replace('\r\n','\n'),flags=re.M)
 entries=[]
 for i in range(1,len(blocks),3):
  number=int(blocks[i]);title=blocks[i+1].strip();text=blocks[i+2]
  spoken=re.split(r'^화면 단서:',text,maxsplit=1,flags=re.M)[0].strip()
  spoken=re.sub(r'^###\s*말할\s*내용\s*\n','',spoken).strip()
  bridge=re.search(r'^넘김: (.+)$',text,re.M)
  spoken=re.sub(r'^넘김: .+$','',spoken,flags=re.M).strip()
  assert spoken,f'Empty narration for page {number}'
  entries.append(dict(pdf_page=number,title=title,pptx_notes=spoken+('\n\n'+bridge.group(1).strip() if bridge else '')))
 assert [e['pdf_page'] for e in entries]==list(range(1,36)),'Expected exactly pages 01 through 35.'
 payload=dict(slides=entries,canonical_sha256=hashlib.sha256(md_bytes).hexdigest())
 source_pdf=json.loads((SCRIPT/'sources/pdf-pages.json').read_text(encoding='utf-8'))
 original_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 with zipfile.ZipFile(SOURCE) as source:
  original={i.filename:source.read(i.filename) for i in source.infolist()}
  infos=source.infolist();archive_comment=source.comment
 pres=xml(original['ppt/presentation.xml'])
 pres_rels={r.getAttribute('Id'):r.getAttribute('Target') for r in relationships(xml(original['ppt/_rels/presentation.xml.rels']))}
 slide_paths=[resolve('ppt/presentation.xml',pres_rels[s.getAttributeNS(NS_R,'id')]) for s in pres.getElementsByTagNameNS(NS_P,'sldId')]
 assert len(slide_paths)==50
 slide_texts=[document_text(xml(original[p])) for p in slide_paths]
 counters=[grams(t) for t in slide_texts]
 alignment=[]
 for i,e in enumerate(payload['slides']):
  counter=grams(source_pdf['pages'][i]['text']);denom=max(1,sum(counter.values()))
  scores=[sum((counter&c).values())/denom for c in counters]
  best=max(range(len(scores)),key=scores.__getitem__)
  assert best==i and scores[i]>.65,f'Slide{ i+1 } alignment ambiguous: best={best+1},score={scores[i]:.3f}'
  alignment.append(dict(page=i+1,title=e['title'],slide_part=slide_paths[i],pdf_overlap=round(scores[i],4)))

 existing_numbers=[int(re.search(r'notesSlide(\d+)\.xml$',p).group(1)) for p in original if re.match(r'ppt/notesSlides/notesSlide\d+\.xml$',p)]
 next_number=max(existing_numbers,default=0)+1
 assert 'ppt/notesSlides/notesSlide1.xml' in original
 template=original['ppt/notesSlides/notesSlide1.xml']
 master_rels=[r for r in relationships(xml(original['ppt/notesSlides/_rels/notesSlide1.xml.rels'])) if r.getAttribute('Type')==NS_R+'/notesMaster']
 assert len(master_rels)==1
 master_path=resolve('ppt/notesSlides/notesSlide1.xml',master_rels[0].getAttribute('Target'))
 assert master_path in original
 ct=xml(original['[Content_Types].xml']);changes={};note_records=[]
 for index,(part,e) in enumerate(zip(slide_paths,payload['slides']),1):
  rp=relpath(part)
  rel_doc=xml(original[rp]) if rp in original else xml(f'<Relationships xmlns="{NS_REL}"/>'.encode())
  linked=[r for r in relationships(rel_doc) if r.getAttribute('Type')==NOTES_TYPE]
  assert len(linked)<=1
  created=not linked
  if linked:
   note_path=resolve(part,linked[0].getAttribute('Target'));note_data=original[note_path]
  else:
   note_path=f'ppt/notesSlides/notesSlide{next_number}.xml';next_number+=1;note_data=template
   ids={r.getAttribute('Id') for r in relationships(rel_doc)};num=1
   while 'rId'+str(num) in ids:num+=1
   rel=rel_doc.createElementNS(NS_REL,'Relationship')
   for k,v in dict(Id='rId'+str(num),Type=NOTES_TYPE,Target=posixpath.relpath(note_path,posixpath.dirname(part))).items():rel.setAttribute(k,v)
   rel_doc.documentElement.appendChild(rel);changes[rp]=serialize(rel_doc)
   nr=xml(f'<Relationships xmlns="{NS_REL}"/>'.encode())
   for rid,typ,target in [('rId1',NS_R+'/notesMaster',master_path),('rId2',NS_R+'/slide',part)]:
    rel=nr.createElementNS(NS_REL,'Relationship')
    for k,v in dict(Id=rid,Type=typ,Target=posixpath.relpath(target,posixpath.dirname(note_path))).items():rel.setAttribute(k,v)
    nr.documentElement.appendChild(rel)
   changes[relpath(note_path)]=serialize(nr)
   override=ct.createElementNS(NS_CT,'Override');override.setAttribute('PartName','/'+note_path)
   override.setAttribute('ContentType','application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml')
   ct.documentElement.appendChild(override)
  changes[note_path]=replace_notes(note_data,e['pptx_notes'],template)
  note_records.append(dict(page=index,note_part=note_path,created=created,characters=len(e['pptx_notes'])))
 changes['[Content_Types].xml']=serialize(ct)
 with zipfile.ZipFile(OUTPUT,'w') as out:
  out.comment=archive_comment
  for info in infos:out.writestr(info,changes.get(info.filename,original[info.filename]))
  for name,data in changes.items():
   if name not in original:out.writestr(name,data,compress_type=zipfile.ZIP_DEFLATED)

 with zipfile.ZipFile(OUTPUT) as out:
  assert out.testzip() is None
  assert len(out.namelist())==len(set(out.namelist()))
  for name,data in original.items():
   if name not in changes:assert out.read(name)==data,name
  assert all(out.read(p)==original[p] for p in slide_paths)
  for record,e in zip(note_records,payload['slides']):
   assert body_text(out.read(record['note_part']))==e['pptx_notes'],record['page']
   for r in relationships(xml(out.read(relpath(record['note_part'])))):
    assert resolve(record['note_part'],r.getAttribute('Target')) in out.namelist()
  assert all(name in out.namelist() for name in original)
 assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==original_hash
 assert CANONICAL_MD.read_bytes()==md_bytes,'Markdown changed during generation; rerun with the latest file.'
 report=dict(source=SOURCE.name,output=OUTPUT.name,source_sha256=original_hash,output_sha256=hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),canonical_md=str(CANONICAL_MD.relative_to(ROOT)),canonical_md_sha256=payload['canonical_sha256'],total_slides=50,main_notes_written=35,new_notes_parts=sum(r['created'] for r in note_records),appendix_slides_preserved=15,all_slide_xml_bytes_unchanged=True,all_untouched_parts_bytes_unchanged=True,original_file_unchanged=True,notes_roundtrip_exact=True,powerpoint_app_open_tested=False,alignment=alignment,notes=note_records)
 (BASE/'notes-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Created {OUTPUT.name}:35 notes; {report["new_notes_parts"]} new note parts;50 slides preserved; original unchanged.')

if __name__=='__main__':main()
