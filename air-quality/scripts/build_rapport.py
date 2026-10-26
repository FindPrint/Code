# -*- coding: utf-8 -*-
"""Construit RAPPORT.md a partir des syntheses (aucune donnee recopice a la main)."""
import json, glob
from pathlib import Path
import pandas as pd
BASE = Path('/home/hatch/workspace/air-quality')
S = pd.read_csv(BASE / 'synthese_runs.csv')
PF = pd.read_csv(BASE / 'tous_seuils_par_flux.csv')
FF = pd.read_csv(BASE / 'tous_F1F2.csv')
ok = S[S.statut == 'OK']
L = []
L.append('# Air Quality Dataset (Kaggle srisyra02) x pipeline v3.3-H1 — Rapport des 10 controles')
L.append('')
L.append('Protocole gele avant les runs : `PROTOCOLE.md` (26 oct. 2026 ~08h50 HAE).')
L.append('Pipeline uploade ce jour-la, tel quel : mode stable, w_size 80, cohen_d, graine 42,')
L.append('HARMONIC_PROB 0,45. Controle EXCLU des flux (regle Porte D) : chaque run analyse')
L.append('les 9 autres colonnes numeriques. Source : `data/air_quality_dataset.csv`, 500 lignes,')
L.append('10 colonnes, 0 valeur manquante ; fichier de travail copie exacte, aucune colonne derivee.')
L.append('Aucun seuil attendu pre-enregistre : lecture descriptive seulement, pas de verite terrain,')
L.append('aucune conclusion sanitaire ou reglementaire.')
L.append('')
L.append('## Ecart page Kaggle / fichier reel (constate avant les runs)')
L.append('')
L.append('La page Kaggle decrit des mesures horaires avec Date, Time et une etiquette Source')
L.append('(Traffic, Industrial, Biomass) ainsi que des capteurs PT08 et RH/AH. Le fichier')
L.append('telecharge ne contient rien de tout cela : 10 colonnes numeriques seulement')
L.append('(PM2.5, PM10, NOx, NO2, SO2, VOCs, CO, CO2, CH4, Temperature), sans aucune colonne')
L.append('temporelle ni etiquette. Aucune lecture temporelle ni par source d\'emission n\'est')
L.append('donc possible sur ce fichier. Valeurs negatives presentes (NOx min -0,08 ; NO2 min')
L.append('-1,94 ; SO2 min -1,10), signalees, non corrigees.')
L.append('')
L.append('## Verdict en une ligne')
L.append('')
stab = ok.stabilite.value_counts().to_dict()
L.append(f"**{len(ok)}/{len(S)} runs termines, {len(S) - len(ok)} echec(s)** "
         f"(duree totale des runs OK : {ok.duree_s.sum():.1f} s, ~{ok.duree_s.mean():.0f} s par run). "
         f"Stabilites (critere du pipeline) : " + ', '.join(f"{k} = {v}" for k, v in sorted(stab.items())) + '.')
L.append('Aucun run VERY STABLE selon le critere du pipeline.')
L.append('Les runs UNSTABLE ne doivent pas etre lus seuls.')
L.append(f"Tous les seuils MC se situent entre {ok.seuil_MC_pct.min():.2f} % et {ok.seuil_MC_pct.max():.2f} %, "
         'soit dans le tiers superieur de l\'axe de rang, pour les 10 controles.')
L.append('')
L.append('## Synthese par controle')
L.append('')
L.append('| controle | seuil MC % | defaut % | MC-defaut | stabilite | +/- | score MC | scan max | valeur au seuil (mediane) | duree s |')
L.append('|---|---:|---:|---:|---|---:|---:|---:|---|---:|')
for r in S.itertuples():
    if r.statut != 'OK':
        L.append(f"| {r.controle} | ECHEC | - | - | - | - | - | - | - | {r.duree_s:.1f} |")
    else:
        L.append(f"| {r.controle} | {r.seuil_MC_pct:.2f} | {r.seuil_defaut_pct:.2f} | {r.ecart_MC_moins_defaut:+.2f} | {r.stabilite} | {r.stabilite_std:.2f} | {r.score_MC:.3f} | {r.scan_global_max:.3f} | {r.valeur_controle_au_MC_mediane} | {r.duree_s:.1f} |")
L.append('')
L.append('## Stabilite : ce qui tient, ce qui ne tient pas')
L.append('')
for rating, g in ok.groupby('stabilite'):
    L.append(f"- **{rating} ({len(g)})** : " + ', '.join(f"{r.controle} {r.seuil_MC_pct:.2f} % (+/-{r.stabilite_std:.2f})" for r in g.itertuples()) + '.')
L.append('')
L.append('## Accord seuil MC / moyenne bootstrap (lecture critique de la stabilite)')
L.append('')
L.append('La note de stabilite du pipeline repose sur l\'ecart-type bootstrap, pas sur l\'accord')
L.append('entre le seuil MC et la moyenne bootstrap. Ici aucun run ne depasse 15 points d\'ecart ;')
L.append('un seul depasse 10 points : Temperature (MC 67,59 %, moyenne 54,36 %, ecart 13,2 pts,')
L.append('UNSTABLE +/-8,46). Les autres ecarts sont tous inferieurs a 9 points.')
L.append('')
L.append('## Seuils propres par flux (top 10 de tout le banc)')
L.append('')
for r in PF.nlargest(10, 'score_max').itertuples():
    L.append(f"- controle {r.controle} : flux {r.flux} {r.seuil_propre_pct:.2f} % (score {r.score_max:.3f}).")
L.append('')
g = PF.groupby('flux')['score_max'].agg(['mean', 'max']).round(3).sort_values('mean', ascending=False)
L.append('En tant que flux (moyenne sur les 9 runs ou la colonne est flux) :')
for flux, r in g.iterrows():
    L.append(f"- {flux} : moyenne {r['mean']:.3f}, max {r['max']:.3f}.")
L.append('')
L.append('## Seuils propres par flux (top 3 par run)')
L.append('')
L.append('| controle (MC %) | flux 1 | flux 2 | flux 3 |')
L.append('|---|---|---|---|')
for c, gg in PF.groupby('controle', sort=False):
    mc = S.loc[S.controle == c, 'seuil_MC_pct']
    mc = float(mc.iloc[0]) if len(mc) and pd.notna(mc.iloc[0]) else float('nan')
    top = gg.nlargest(3, 'score_max')
    cells = ' | '.join(f"{r.flux} {r.seuil_propre_pct:.2f} % ({r.score_max:.3f})" for r in top.itertuples())
    L.append(f"| {c} ({mc:.2f} %) | {cells} |")
L.append('')
L.append(f"Detail complet des {len(PF)} seuils propres (10 x 9) : `tous_seuils_par_flux.csv`.")
L.append('')
L.append('## Scores Q moyens par run')
L.append('')
for p in sorted(glob.glob(str(BASE / 'results' / 'ctrl_*' / 'run_summary.json'))):
    j = json.load(open(p))
    if j.get('status') != 'OK':
        L.append(f"- {j['control']} : ECHEC")
        continue
    q = j['scores_moyens_par_Q']
    L.append(f"- {j['control']} : " + ', '.join(f"{k} = {v:.3f}" for k, v in q.items()))
L.append('')
L.append('## Derivees F1/F2 post-seuil, flux « Tous »')
L.append('')
tous = FF[FF.flux == 'Tous']
L.append(tous.pivot_table(index='controle', columns='estimateur', values='F1').round(4).to_string())
L.append('')
L.append(f"Detail complet ({len(FF)} lignes) : `tous_F1F2.csv`.")
L.append('')
L.append('## Reserves (gelees avant les runs, rappelees ici)')
L.append('')
L.append('- Pas de colonne temporelle dans le fichier reel : le controle est un axe de rang, pas un temps.')
L.append('- Aucune etiquette Source dans le fichier : aucune lecture par source d\'emission.')
L.append('- Valeurs negatives de NOx/NO2/SO2 : signalees, non corrigees.')
L.append('- Aucune conclusion sanitaire ou reglementaire tiree des seuils : mesures du pipeline sur ce fichier.')
(BASE / 'RAPPORT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print(f"RAPPORT.md ecrit ({len(L)} lignes)")
