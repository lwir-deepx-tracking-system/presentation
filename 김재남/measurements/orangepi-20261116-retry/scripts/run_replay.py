"""Run balanced, repeated actual-frame load tests; no inference output is fabricated."""
import os,sys
sys.path.insert(0,'/tmp/lwir-perf-20261116')
import runner
runner.prepare()
os.environ['LWIR_REPLAY_DIR']='/tmp/lwir-perf-20261116/samples'
for rep in range(1,4):
 rates=[30,60,120];rates=rates[rep-1:]+rates[:rep-1]
 for fps in rates:
  os.environ['LWIR_REPLAY_FPS']=str(fps)
  cases=['serial640','async1','async4','async6'];cases=cases[(rep-1)%4:]+cases[:(rep-1)%4]
  for case in cases:
   if not runner.run(case,f'replay{fps}',rep):raise SystemExit(1)
