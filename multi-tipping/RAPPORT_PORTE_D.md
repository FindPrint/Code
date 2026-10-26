# RAPPORT PORTE D — AT et nul B2 sans energy-as-flux (config standard 17 oct.)

2026-10-22 ~14h20 HAE. Protocole gelé avant les runs : `PROTOCOLE_PORTE_D.md`.
Pipeline v3.3 tel quel, mode stable, graine 42, aveugle, contrôle = energy
EXCLUE des flux analysés (runner `run_v33_generic_noEflux.py`, analyse
`analyse_generic_noE.py`). 2 runs, ~193 s chacun, sorties 0.

## D1 — AT réel (`at_fluxes.csv` → `vague2/noE_real/`)
- Global MC : **54,16 % → fenêtre 1 ✓** (vague 1 avec energy-as-flux : 54,93 %),
  VERY STABLE, score 0,763.
- Par flux (sans energy) : m_s 53,22 % (T 4,647) ✓f1, m_tau 54,16 % (T 4,724) ✓f1,
  **m_prod 66,76 % (T 5,389) ✓f2, flip_rate 67,83 % (T 5,443) ✓f2**,
  local_variance 40,88 % (score 2,20, hors fenêtres — même lecture qu'en vague 1).
- Les deux seuils se résolvent encore, chacun par ses flux, SANS le signal
  energy-as-flux. La discrimination par flux ne dépendait pas de l'artefact.

## D2 — nul B2 (`at_null2_fluxes.csv` → `vague2/noE_null2/`)
- Global MC : **84,85 %, MODERATELY STABLE (std 4,87)** — contre 58,30 %,
  VERY STABLE (std 1,43) avec energy-as-flux. Le critère B d'origine
  (« pas de VERY STABLE sur nul ») est maintenant SATISFAIT.
- Par flux : scores 0,179–0,333 (effondrés, comme en vague 2 : 0,18–0,30),
  seuils dispersés 52,82 / 93,43 / 67,16 / 89,14 / 55,36 ; max courbe
  globale 0,124 (contre 0,85 avec energy-as-flux, 3,5–3,9 en réel).

## Verdict
La réserve du verdict vague 2 était un **artefact de configuration**, pas une
propriété de l'instrument. Mécanisme mesuré : energy-as-flux contribue un
score de séparation constant (~3,28 sur Q4, identique réel/nul) qui étaye à
lui seul la stabilité du seuil global sur données décorrélées. Sans elle :
**le seuil global discrimine lui aussi** (VERY STABLE sur réel → MODERATELY
STABLE à un seuil aberrant sur nul), et la lecture par flux discrimine
toujours (~20× d'écart de scores).

Corollaire vérifié sur pièce (`workspace/user/files/results_ising_energy_test/` :
contrôle energy, flux analysés = magnetization/flip_rate/cluster_size/
local_variance, AUCUNE colonne energy_*) : la campagne Ising standard des
17–19 oct. (20/25 paires → Tc) utilisait déjà cette configuration saine —
**ses résultats ne sont pas contaminés par l'artefact.**

Règle instrumentale établie : le contrôle ne doit jamais figurer parmi les
flux analysés (auto-séparation tautologique). C'est le réglage du 17 oct.,
décidé par l'utilisateur — validé par mesure ce soir.
