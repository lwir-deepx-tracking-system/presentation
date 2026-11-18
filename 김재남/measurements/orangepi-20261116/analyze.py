"""실제 runtime sidecar와 manifest를 집계한다. 진단·실패 실행은 주 비교에서 제외한다."""
import csv,json,math,statistics,sys
from collections import defaultdict
from pathlib import Path

def percentile(values,p):
    """정렬된 표본에서 선형 보간 백분위수를 구한다."""
    if not values:return None
    a=sorted(values);x=(len(a)-1)*p;i=int(x);return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)

def summarize(directory):
    """동일 측정 구간의 처리량과 capture-cohort 지연·누락을 집계한다."""
    m=json.loads((directory/'manifest.json').read_text())
    if not m.get('valid') or m['tag'] not in ['on-on','off-on','on-off','off-off','restore','gui']:return None
    rows=list(csv.DictReader((directory/'telemetry.csv').open()))
    lo,hi=m['window_start_ns'],m['window_end_ns'];dur=(hi-lo)/1e9
    result={'run_id':directory.name,'tag':m['tag'],'case':m['case'],'rep':m['rep'],'duration_s':dur,'model_sha256':m['model_sha256']}
    for stage in ['camera','submit','detection','tracking']:
        stage_rows=[r for r in rows if r['stage']==stage]
        result[stage+'_fps']=sum(lo<=int(r['done_ns'])<hi for r in stage_rows)/dur
    camera_ids={r['frame_id'] for r in rows if r['stage']=='camera' and lo<=int(r['capture_ns'])<hi}
    all_tracking={r['frame_id'] for r in rows if r['stage']=='tracking'}
    result.update(captured_frames=len(camera_ids),dropped_frames=len(camera_ids-all_tracking),drop_pct=100*len(camera_ids-all_tracking)/len(camera_ids) if camera_ids else None)
    tracked=[r for r in rows if r['stage']=='tracking' and r['frame_id'] in camera_ids]
    latency=[(int(r['done_ns'])-int(r['capture_ns']))/1e6 for r in tracked]
    result.update(tracking_frames=len(latency),e2e_mean_ms=statistics.mean(latency) if latency else None,e2e_p50_ms=percentile(latency,.5),e2e_p95_ms=percentile(latency,.95),e2e_max_ms=max(latency) if latency else None,over_33ms_pct=100*sum(x>1000/30 for x in latency)/len(latency) if latency else None)
    det=[r for r in rows if r['stage']=='detection' and r['frame_id'] in camera_ids]
    for field in ['preprocess_ms','latency_ms','postprocess_ms','npu_ms','input_format_us','output_format_us','cpu_task_us']:
        values=[float(r[field]) for r in det if field!='cpu_task_us' or float(r['cpu_valid'])==1]
        result[field]=statistics.mean(values) if values else None
    samples=[s for s in m.get('process_samples',[]) if lo<=s['ns']<hi]
    if len(samples)>=2:
        first,last=samples[0],samples[-1]
        result['cpu_core_pct']=100*(last['cpu_ticks']-first['cpu_ticks'])/m.get('clock_ticks_per_second',100)/((last['ns']-first['ns'])/1e9)
        result['rss_mean_mib']=statistics.mean(s['rss_kb'] for s in samples)/1024
        result['rss_peak_mib']=max(s['rss_kb'] for s in samples)/1024
        result['soc_temp_max_c']=max(v for s in samples for v in s['temps_mC'])/1000
    return result

def write_csv(path,rows):
    """집계 표를 헤더가 포함된 CSV로 보존한다."""
    if not rows:return
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fields);writer.writeheader();writer.writerows(rows)

def main(root):
    """반복 실행별 값과 반복 간 평균·표준편차를 별도 산출한다."""
    runs=[];failures=[]
    for path in sorted((root/'results').glob('*/manifest.json')):
        m=json.loads(path.read_text())
        if not m.get('valid'):failures.append({'run':path.parent.name,'error':m.get('error')})
        value=summarize(path.parent)
        if value:runs.append(value)
    write_csv(root/'per-run.csv',runs)
    groups=defaultdict(list)
    for r in runs:groups[(r['tag'],r['case'])].append(r)
    summary=[]
    for (tag,case),items in sorted(groups.items()):
        row={'tag':tag,'case':case,'repeats':len(items)}
        for k in items[0]:
            if k in ['run_id','tag','case','rep','model_sha256']:continue
            values=[x[k] for x in items if isinstance(x.get(k),(int,float))]
            row[k]=(max(values) if k=='e2e_max_ms' else statistics.mean(values)) if values else None
            if k in ['tracking_fps','e2e_p95_ms','cpu_core_pct']:row[k+'_sd']=statistics.stdev(values) if len(values)>1 else 0
        summary.append(row)
    write_csv(root/'summary.csv',summary)
    (root/'summary.json').write_text(json.dumps({'runs':runs,'summary':summary,'failed_runs':failures},indent=2))
    for r in summary:print(r['tag'],r['case'],'n',r['repeats'],'fps',round(r['tracking_fps'],2),'p95',round(r['e2e_p95_ms'],2),'CPU',round(r.get('cpu_core_pct',0),1))
if __name__=='__main__':main(Path(sys.argv[1]))
