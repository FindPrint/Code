# -*- coding: utf-8 -*-
"""Lot contrôles — 35 runs, 2 travailleurs en parallèle, résumable.
Un job déjà terminé (verdict.json + run_summary.json présents) est sauté.
Chaque job : run_ctrl.py puis analyse_ctrl.py. Les échecs sont consignés,
jamais bloquants pour le lot. Journal : controles/batch_status.jsonl
"""
import json, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

B = Path('/home/hatch/workspace/multi-tipping')
OUT = B / 'controles'
OUT.mkdir(exist_ok=True)
AT_CTRLS = ['magnetization_s', 'magnetization_tau', 'magnetization_prod',
            'energy', 'flip_rate', 'local_variance']
CLOCK_CTRLS = ['magnetization', 'energy', 'flip_rate', 'vortex_density', 'local_variance']
AT_WIN = ('50,60', '62,73', '4.6,4.9', '5.2,5.6')
CLOCK_WIN = ('30,46', '52,68', '0.62,0.80', '0.82,0.98')

jobs = []
for ds, fluxes, temp in [('at', 'at_fluxes.csv', 'at_temperature.csv'),
                         ('at_s7', 'vague2/data/at_s7_fluxes.csv', 'vague2/data/at_s7_temperature.csv'),
                         ('at_s123', 'vague2/data/at_s123_fluxes.csv', 'vague2/data/at_s123_temperature.csv'),
                         ('at_L36', 'vague2/data/at_L36_fluxes.csv', 'vague2/data/at_L36_temperature.csv')]:
    for c in AT_CTRLS:
        jobs.append((ds, fluxes, temp, c, AT_WIN))
for c in CLOCK_CTRLS:
    jobs.append(('clock', 'clock6_fluxes.csv', 'clock6_temperature.csv', c, CLOCK_WIN))
for c in AT_CTRLS:
    jobs.append(('null2', 'vague2/data/at_null2_fluxes.csv', 'none', c, AT_WIN))

lock = threading.Lock()
status_path = OUT / 'batch_status.jsonl'

def log(rec):
    with lock:
        with open(status_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(json.dumps(rec, ensure_ascii=False), flush=True)

def done(od):
    return (od / 'verdict.json').exists() and (od / 'run_summary.json').exists()

def run_job(job):
    ds, fluxes, temp, ctrl, (w1, w2, t1, t2) = job
    od = OUT / ds / ctrl
    if done(od):
        log({'job': f'{ds}/{ctrl}', 'status': 'SKIP déjà terminé'})
        return
    od.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    try:
        with open(od / 'driver.log', 'w') as lf:
            subprocess.run([sys.executable, 'run_ctrl.py', fluxes, ctrl, str(od)],
                           cwd=B, stdout=lf, stderr=subprocess.STDOUT, check=True)
        with open(od / 'analyse.log', 'w') as lf:
            subprocess.run([sys.executable, 'analyse_ctrl.py', fluxes, ctrl, temp, str(od),
                            w1, w2, t1, t2],
                           cwd=B, stdout=lf, stderr=subprocess.STDOUT, check=True)
        v = json.load(open(od / 'verdict.json'))
        log({'job': f'{ds}/{ctrl}', 'status': 'OK', 'duree_s': round(time.time() - t0, 1),
             'global_pct': v['global_mc_pct'], 'global_T': v['global_mc_T'],
             'global_hit_T': v['global_hit_T'], 'stabilite': v['stabilite']})
    except subprocess.CalledProcessError as e:
        log({'job': f'{ds}/{ctrl}', 'status': 'ECHEC', 'duree_s': round(time.time() - t0, 1),
             'detail': str(e)})

if __name__ == '__main__':
    print(f'{len(jobs)} jobs, 2 travailleurs', flush=True)
    with ThreadPoolExecutor(max_workers=2) as ex:
        list(ex.map(run_job, jobs))
    print('LOT TERMINE', flush=True)
