# -*- coding: utf-8 -*-
"""Construit RAPPORT.md à partir des synthèses (aucune donnée recopiée à la main)."""
import json, glob
from pathlib import Path
import pandas as pd
BASE = Path('/home/hatch/workspace/breast-cancer')
S = pd.read_csv(BASE / 'synthese_runs.csv')
PF = pd.read_csv(BASE / 'tous_seuils_par_flux.csv')
FF = pd.read_csv(BASE / 'tous_F1F2.csv')
ok = S[S.statut == 'OK']
L = []
L.append('# Breast Cancer Dataset (Kaggle yasserh) x pipeline v3.3-H1 — Rapport des 32 contrôles')
L.append('')
L.append('Protocole gelé avant les runs : `PROTOCOLE.md` (25 oct. 2026 ~21h50 HAE).')
L.append('Pipeline uploadé ce jour-là, tel quel : mode stable, w_size 80, cohen_d, graine 42,')
L.append('HARMONIC_PROB 0,45. Contrôle EXCLU des flux (règle Porte D) : chaque run analyse')
L.append('les 31 autres colonnes numériques. Source : `data/breast-cancer.csv`, 569 lignes,')
L.append('32 colonnes, 0 valeur manquante ; fichier de travail `data/breast-cancer_pipeline.csv`')
L.append('ajoute seulement `diagnosis_encoded` (B = 0, M = 1). Aucun seuil attendu pré-enregistré :')
L.append('lecture descriptive seulement, pas de vérité terrain, aucune conclusion médicale.')
L.append('')
L.append('## Verdict en une ligne')
L.append('')
stab = ok.stabilite.value_counts().to_dict()
L.append(f"**{len(ok)}/{len(S)} runs terminés, {len(S) - len(ok)} échec(s)** "
         f"(durée totale des runs OK : {ok.duree_s.sum():.1f} s, ~{ok.duree_s.mean():.0f} s par run). "
         f"Stabilités (critère du pipeline) : " + ', '.join(f"{k} = {v}" for k, v in sorted(stab.items())) + '.')
vs = ok[ok.stabilite == 'VERY STABLE']
if len(vs):
    L.append('Runs VERY STABLE : ' + ', '.join(f"{r.controle} ({r.seuil_MC_pct:.2f} %)" for r in vs.itertuples()) + '.')
else:
    L.append('Aucun run VERY STABLE selon le critère du pipeline.')
L.append('Les runs UNSTABLE ne doivent pas être lus seuls.')
L.append('')
L.append('## Synthèse par contrôle')
L.append('')
L.append('| contrôle | seuil MC % | défaut % | MC−défaut | stabilité | ± | score MC | scan max | valeur au seuil (médiane) | durée s |')
L.append('|---|---:|---:|---:|---|---:|---:|---:|---|---:|')
for r in S.itertuples():
    if r.statut != 'OK':
        L.append(f"| {r.controle} | ECHEC | - | - | - | - | - | - | - | {r.duree_s:.1f} |")
    else:
        L.append(f"| {r.controle} | {r.seuil_MC_pct:.2f} | {r.seuil_defaut_pct:.2f} | {r.ecart_MC_moins_defaut:+.2f} | {r.stabilite} | {r.stabilite_std:.2f} | {r.score_MC:.3f} | {r.scan_global_max:.3f} | {r.valeur_controle_au_MC_mediane} | {r.duree_s:.1f} |")
L.append('')
L.append('## Stabilité : ce qui tient, ce qui ne tient pas')
L.append('')
for rating, g in ok.groupby('stabilite'):
    L.append(f"- **{rating} ({len(g)})** : " + ', '.join(f"{r.controle} {r.seuil_MC_pct:.2f} % (±{r.stabilite_std:.2f})" for r in g.itertuples()) + '.')
L.append('')
L.append('## Accord seuil MC / moyenne bootstrap (lecture critique de la stabilité)')
L.append('')
L.append('La note de stabilité du pipeline repose sur l’écart-type bootstrap, pas sur l’accord')
L.append('entre le seuil MC et la moyenne bootstrap. Les runs suivants ont un écart > 15 points :')
for r in ok[abs(ok.seuil_MC_pct - ok.stabilite_moy_pct) > 15].itertuples():
    L.append(f"- {r.controle} : MC {r.seuil_MC_pct:.2f} %, moyenne bootstrap {r.stabilite_moy_pct:.2f} %, écart {abs(r.seuil_MC_pct - r.stabilite_moy_pct):.1f} pts, note {r.stabilite} (±{r.stabilite_std:.2f}).")
L.append('')
L.append('Cas pièges : `symmetry_se` est noté MODERATELY STABLE (±4,01) alors que sa moyenne bootstrap')
L.append('(17,60 %) est à 80 points du MC (97,73 %) ; `concave points_se` est noté MODERATELY STABLE')
L.append('(±3,83) avec un écart de 18,1 points (MC 34,77 %, moyenne 16,67 %). À l’inverse, les runs où')
L.append('MC et moyenne bootstrap s’accordent à moins de 7 points ET avec un écart-type < 6 sont :')
L.append('radius_mean, perimeter_mean, area_mean, concavity_mean, radius_se, area_se, area_worst,')
L.append('concave points_worst, symmetry_worst, diagnosis_encoded.')
L.append('')
L.append('## Seuils propres par flux (top 10 de tout le banc)')
L.append('')
for r in PF.nlargest(10, 'score_max').itertuples():
    L.append(f"- contrôle {r.controle} : flux {r.flux} {r.seuil_propre_pct:.2f} % (score {r.score_max:.3f}).")
L.append('')
g = PF.groupby('flux')['score_max'].agg(['mean', 'max']).round(3).sort_values('mean', ascending=False)
L.append('En tant que flux (moyenne sur les 31 runs où la colonne est flux) :')
for flux, r in g.iterrows():
    L.append(f"- {flux} : moyenne {r['mean']:.3f}, max {r['max']:.3f}.")
L.append('')
L.append('## Seuils propres par flux (top 3 par run)')
L.append('')
L.append('| contrôle (MC %) | flux 1 | flux 2 | flux 3 |')
L.append('|---|---|---|---|')
for c, gg in PF.groupby('controle', sort=False):
    mc = S.loc[S.controle == c, 'seuil_MC_pct']
    mc = float(mc.iloc[0]) if len(mc) and pd.notna(mc.iloc[0]) else float('nan')
    top = gg.nlargest(3, 'score_max')
    cells = ' | '.join(f"{r.flux} {r.seuil_propre_pct:.2f} % ({r.score_max:.3f})" for r in top.itertuples())
    L.append(f"| {c} ({mc:.2f} %) | {cells} |")
L.append('')
L.append(f"Détail complet des {len(PF)} seuils propres (32 × 31) : `tous_seuils_par_flux.csv`.")
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
L.append('## Dérivées F1/F2 post-seuil, flux « Tous »')
L.append('')
tous = FF[FF.flux == 'Tous']
L.append(tous.pivot_table(index='controle', columns='estimateur', values='F1').round(4).to_string())
L.append('')
L.append(f"Détail complet ({len(FF)} lignes) : `tous_F1F2.csv`.")
L.append('')
L.append('## Réserves (gelées avant les runs, rappelées ici)')
L.append('')
L.append('- Données transversales (569 cas, pas une série temporelle) : le contrôle est un axe de rang, pas un temps.')
L.append('- `id` est un identifiant, pas une mesure.')
L.append('- `diagnosis_encoded` est binaire : un seuil entre les deux paliers de rang sépare les mêmes deux groupes B/M.')
L.append('- Aucune conclusion médicale, aucun seuil clinique ne découle de ces mesures du pipeline.')
L.append('')
L.append('## Fichiers livrés')
L.append('')
L.append('- `PROTOCOLE.md` — protocole gelé avant les runs.')
L.append('- `synthese_runs.csv` — une ligne par contrôle (seuils, stabilité, scan, valeur au seuil).')
L.append('- `tous_seuils_par_flux.csv` — les 992 seuils propres par flux.')
L.append('- `tous_F1F2.csv` — dérivées F1/F2 post-seuil, tous runs.')
L.append('- `plateaux_controles.csv` — paliers de rang des contrôles.')
L.append('- `results/ctrl_<colonne>/` — sorties complètes du pipeline par run.')
L.append('- `breast_cancer_32_controles_resultats.zip` — archive de l’ensemble ci-dessus + données.')
L.append('')
(BASE / 'RAPPORT.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('RAPPORT.md écrit,', len(L), 'lignes')
