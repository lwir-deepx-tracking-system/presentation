import os,sys,time,json,subprocess,signal,hashlib
from pathlib import Path
import yaml
ROOT=Path('/tmp/lwir-perf-20261116');SRC=ROOT/'source';BANK=Path('/home/orangepi/workspace/model-bank/tracking_server/models/detect')
def prepare():
 (ROOT/'configs').mkdir(exist_ok=True)
 for model,h in [('y26',640),('y26',480),('y8',640)]:
  c=yaml.safe_load((SRC/'config/model'/('yolo26s.yaml' if model=='y26' else 'yolov8n.yaml')).read_text());c['input']['height']=h
  if model=='y8':
   c['postprocess']['num_classes']=16;c['postprocess']['class_names']=c['postprocess']['class_names'][:16]
  c['model']['path']=str(BANK/('yolo26s/yolo26s_nms_640x%d.dxnn'%h if model=='y26' else 'yolov8/yolov8n_nms_640x640.dxnn'))
  (ROOT/'configs'/f'{model}-{h}.yaml').write_text(yaml.safe_dump(c,allow_unicode=True,sort_keys=False))
def proc(pid):
 try:
  fields=Path(f'/proc/{pid}/stat').read_text().split(')')[1].split();status=Path(f'/proc/{pid}/status').read_text()
  return {'ns':time.monotonic_ns(),'cpu_ticks':int(fields[11])+int(fields[12]),'rss_kb':int(status.split('VmRSS:')[1].split()[0]),'temps_mC':[int(p.read_text()) for p in sorted(Path('/sys/class/thermal').glob('thermal_zone*/temp'))]}
 except FileNotFoundError:return None

def run(case,tag='on-on',rep=1,duration=15,warm=5,lib=None):
 model,h,flight,serial,ort={'serial640':('y26',640,6,True,False),'async1':('y26',640,1,False,False),'async4':('y26',640,4,False,False),'async6':('y26',640,6,False,False),'rect6':('y26',480,6,False,False),'ort8':('y8',640,6,False,True),'npu8':('y8',640,6,False,False)}[case]
 run_id=f'{tag}-{case}-r{rep}';d=ROOT/'results'/run_id;d.mkdir(parents=True,exist_ok=False)
 c=yaml.safe_load((SRC/'config/runtime.yaml').read_text());mp=ROOT/'configs'/f'{model}-{h}.yaml';c['model']['config']=str(mp);c['model_catalog']=[{'id':1,'config':str(mp)}]
 c['tracking']['id']=1;c['tracking_catalog']=[{'id':1,'config':str(SRC/'config/tracking/bytetrack.yaml')}]
 c['control']['enabled']=False;c['gui']['enabled']=False;c['gui']['command']['enabled']=False;c['gui']['metadata']['enabled']=False;c['logging']['level']='info';c['measurement']={'enabled':True,'output_root':str(d/'results')};c['detection'].update(max_inflight=flight,buffer_count=6,use_ort=ort)
 if os.environ.get('LWIR_PERF_GUI'):
  c['gui']['enabled']=True;c['gui']['metadata']['enabled']=True
 (d/'runtime.yaml').write_text(yaml.safe_dump(c,allow_unicode=True,sort_keys=False));env=os.environ.copy();env['LWIR_PERF_DIR']=str(d)
 if serial:env['LWIR_PERF_SERIAL']='1'
 if lib:env['LD_LIBRARY_PATH']=str(lib)+':'+env.get('LD_LIBRARY_PATH','')
 (d/'device-before.txt').write_text(subprocess.run(['dxcli','-s'],capture_output=True,text=True,timeout=10).stdout)
 log=open(d/'runtime.log','w');p=subprocess.Popen([str(ROOT/'build/lwir_runtime'),str(d/'runtime.yaml')],cwd=SRC,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 m={'case':case,'tag':tag,'rep':rep,'pid':p.pid,'duration_s':duration,'warm_s':warm,'clock_ticks_per_second':os.sysconf('SC_CLK_TCK'),'source_commit':'0fe016f7edd069900457a746dc4cc787569c5ae6','model_sha256':hashlib.sha256(Path(yaml.safe_load(mp.read_text())['model']['path']).read_bytes()).hexdigest()}
 try:
  timeout=time.monotonic()+45
  while not (d/'ready').exists() and p.poll() is None and time.monotonic()<timeout:time.sleep(.1)
  if not (d/'ready').exists():raise RuntimeError('camera not ready: '+(d/'runtime.log').read_text()[-1800:])
  while (d/'ready').stat().st_size==0:time.sleep(.01)
  first=int((d/'ready').read_text());start=first+int(warm*1e9);end=start+int(duration*1e9);m.update(first_camera_ns=first,window_start_ns=start,window_end_ns=end)
  maps=Path(f'/proc/{p.pid}/maps').read_text();(d/'maps.txt').write_text(maps)
  libs=sorted(set(line.split()[-1] for line in maps.splitlines() if 'libdxrt.so' in line or 'libonnxruntime.so' in line));m['loaded_libraries']=libs;m['library_sha256']={s:hashlib.sha256(Path(s).read_bytes()).hexdigest() for s in libs}
  samples=[]
  while time.monotonic_ns()<end:
   if p.poll() is not None:raise RuntimeError('runtime exited before end')
   sample=proc(p.pid)
   if sample:samples.append(sample)
   time.sleep(.2)
  m['process_samples']=samples;p.send_signal(signal.SIGINT)
  try:p.wait(timeout=25)
  except subprocess.TimeoutExpired:p.kill();p.wait();raise RuntimeError('SIGINT drain timeout')
  m['exit_code']=p.returncode
  if p.returncode!=0:raise RuntimeError('runtime failed')
  m['valid']=(d/'telemetry.csv').exists()
 except Exception as e:
  m['valid']=False;m['error']=str(e)
  if p.poll() is None:
   p.send_signal(signal.SIGINT)
   try:p.wait(timeout=15)
   except subprocess.TimeoutExpired:p.kill();p.wait()
 finally:
  log.close();(d/'device-after.txt').write_text(subprocess.run(['dxcli','-s'],capture_output=True,text=True,timeout=10).stdout);(d/'manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps({'run':run_id,'valid':m.get('valid'),'error':m.get('error'),'libs':m.get('loaded_libraries')},ensure_ascii=False),flush=True)
 return m.get('valid',False)
if __name__=='__main__':
 prepare();case=sys.argv[1];tag=sys.argv[2] if len(sys.argv)>2 else 'on-on';rep=int(sys.argv[3]) if len(sys.argv)>3 else 1;duration=int(sys.argv[4]) if len(sys.argv)>4 else 15
 sys.exit(0 if run(case,tag,rep,duration,lib=os.environ.get('PERF_SDK_LIB')) else 1)
