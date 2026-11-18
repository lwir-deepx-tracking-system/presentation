"""Validate and summarize measured replay inputs, frame cohorts and observed latency maxima."""
import csv,json,statistics,sys
from pathlib import Path
sys.path.insert(0,'/tmp/lwir-perf-20261116')
import analyze
root=Path(sys.argv[1])
runs=[]
for manifest in sorted((root/'results').glob('replay*/manifest.json')):
 d=manifest.parent
 m=json.loads((d/'manifest.json').read_text())
 if not m.get('valid'):raise RuntimeError(f'failed run {d}: {m.get("error")}')
 # The shared analyzer only accepts its original source labels.
 rows=list(csv.DictReader((d/'telemetry.csv').open()))
 lo,hi=m['window_start_ns'],m['window_end_ns']
 for stage in ['camera','submit','detection','tracking']:
  part=[r for r in rows if r['stage']==stage];ids=[int(r['frame_id']) for r in part]
  assert len(ids)==len(set(ids)),(d,stage,'duplicate frame IDs')
  assert all(int(r['done_ns'])>=int(r['capture_ns']) for r in part),(d,'negative latency')
 sets={s:{r['frame_id'] for r in rows if r['stage']==s} for s in ['camera','submit','detection','tracking']}
 metrics=[]
 for metric_file in (d/'results').rglob('metrics.csv'):
  metrics.extend(csv.DictReader(metric_file.open()))
 native={x['frame_id']:float(x['e2e_ms']) for x in metrics if x['stage']=='tracking' and x['e2e_ms']}
 assert native,(d,'native runtime tracking metrics missing')
 differences=[abs((int(x['done_ns'])-int(x['capture_ns']))/1e6-native[x['frame_id']]) for x in rows if x['stage']=='tracking']
 assert max(differences)<2,(d,'native CSV and sidecar disagree',max(differences))

 assert sets['tracking']<=sets['detection']<=sets['submit']<=sets['camera'],d
 # Run shared aggregation without mutating the recorded manifest.
 source=Path(analyze.__file__).read_text().replace("'restore','gui'","'restore','gui','replay30','replay60','replay120'")
 ns={'__name__':'replay_analysis_shared'};exec(compile(source,'shared-analysis','exec'),ns)
 r=ns['summarize'](d);r['requested_fps']=m['requested_fps'];r['drop_cohort_duration_s']=m['duration_s']-.5;r['native_csv_max_difference_ms']=max(differences)
 # Only drop-rate accounting excludes shutdown cancellation; latency/max keep the full 15s window.
 drop_ids={x['frame_id'] for x in rows if x['stage']=='camera' and lo<=int(x['capture_ns'])<hi-500_000_000}
 r['drop_cohort_frames']=len(drop_ids);r['dropped_frames']=len(drop_ids-sets['tracking'])
 r['drop_pct']=100*r['dropped_frames']/len(drop_ids)
 releases=list(csv.DictReader((d/'replay-source.csv').open()))
 release=[x for x in releases if lo<=int(x['actual_ns'])<hi]
 late=[(int(x['actual_ns'])-int(x['planned_ns']))/1e6 for x in release]
 r.update(source_lateness_p95_ms=analyze.percentile(late,.95),source_lateness_max_ms=max(late),source_late_over_period_pct=100*sum(x>1000/r['requested_fps'] for x in late)/len(late))
 assert abs(r['camera_fps']/r['requested_fps']-1)<.02,(d,'input rate outside 2 percent',r['camera_fps'])
 assert r['model_sha256']==runs[0]['model_sha256'] if runs else True
 if runs:assert m['library_sha256']==library_sha256,(d,'SDK library changed')
 library_sha256=m['library_sha256']
 runs.append(r)
from collections import defaultdict
groups=defaultdict(list)
for r in runs:groups[(r['tag'],r['case'])].append(r)
summary=[]
for (tag,case),items in sorted(groups.items()):
 out={'tag':tag,'case':case,'repeats':len(items)}
 for k in items[0]:
  if k in ['run_id','tag','case','rep','model_sha256']:continue
  vals=[x[k] for x in items if isinstance(x.get(k),(int,float))]
  if vals:out[k]=max(vals) if k.endswith('_max_ms') or k=='rss_peak_mib' else statistics.mean(vals)
  if vals and k in ['tracking_fps','e2e_p95_ms','cpu_core_pct']:out[k+'_sd']=statistics.stdev(vals) if len(vals)>1 else 0
 summary.append(out)
analyze.write_csv(root/'replay-per-run.csv',runs);analyze.write_csv(root/'replay-summary.csv',summary)
(root/'replay-summary.json').write_text(json.dumps({'runs':runs,'summary':summary},indent=2))
for r in summary:
 print(r['tag'],r['case'],'n',r['repeats'],'input',round(r['camera_fps'],2),'out',round(r['tracking_fps'],2),'drop',round(r['drop_pct'],2),'p95',round(r['e2e_p95_ms'],2),'max',round(r['e2e_max_ms'],2),'CPU',round(r.get('cpu_core_pct',0),1),'src-late-max',round(r['source_lateness_max_ms'],2))
(root/'replay-validation.json').write_text(json.dumps({'valid_runs':len(runs),'unique_stage_frame_ids':True,'nonnegative_timestamps':True,'stage_frame_sets_consistent':True,'actual_input_within_2_percent':True,'same_model_sha256':runs[0]['model_sha256'] if runs else None,'same_library_sha256':library_sha256 if runs else {},'native_runtime_csv_difference_under_2ms':True,'native_runtime_csv_max_difference_ms':max(x['native_csv_max_difference_ms'] for x in runs) if runs else None,'max_is_global_observed_max':True,'drop_rate_end_guard_ms':500,'fps_latency_window_s':15,'drop_cohort_s':14.5},indent=2))
