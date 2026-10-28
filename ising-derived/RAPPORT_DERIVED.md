# Lot Ising dérivés × v3.5.4 — flux type susceptibility, témoins et nuls

**Date :** 28 octobre 2026, 12:15:00–12:32:34 EDT (17 min 34 s).
**Protocole gelé avant construction et runs :** `PROTOCOLE_DERIVED.md`.
**Provenance :** `PROVENANCE_DERIVED.md` (règle permanente : provenance toujours nommée).
**Pipeline :** `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A), SHA-256
`b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`.
**Ce qui est DANS le pipeline :** les 6 flux originaux analysés, les 29 estimateurs,
les questions Q1–Q6, le scan, le MC. **Ce qui est apporté (hors pipeline) :**
les flux dérivés et nuls (construction CSV), la traduction en T (harnais,
après les runs), la comparaison descriptive à Tc, les règles d'attribution R1–R5.
Le pipeline ne voit jamais T ni Tc (0 occurrence vérifiée dans le code v3.5.4).

## Verdict

**Pas de deuxième seuil critique.** Les 8 runs dérivés n'ont chacun qu'**une seule
masse** de pics forts. Le « plus » que le pipeline trouve sans le présenter,
c'est le plateau et les pics forts — une seule frontière étalée, pas deux.

**Attribution, règles R1–R5 gelées :**

| Fait mesuré | Attribution |
|---|---|
| Famille basse (T 1,84–1,98) sous les 6 contrôles de variance (expvar + rollvar) | **Lecture réelle de la loupe** : les contrôles second-moment lisent le pied du régime de fluctuations, pas le centre de la transition. La mémoire expansive n'en est PAS la cause (rollvar sans mémoire donne la même lecture) — R2 réfute l'hypothèse construction pour la masse basse. |
| Famille Tc (T 2,2565) sous les 2 contrôles de moyenne expansive | **Lecture réelle de la loupe** : les contrôles premier-moment retrouvent le seuil du lot original (ΔT −0,013). |
| Pic isolé à T = 2,6739 (run expvar_energy uniquement) | **Artefact** : échoue R1 (1 seul run dérivé), présent dans 2 nuls (R3 : machinerie), absent sous rollvar (R2 : construction). Pas un seuil. |
| Seuils sur les 3 nuls (scores 0,556–0,567, UNSTABLE, T dispersées) | **Machinerie** : le pipeline produit un seuil même sur contrôle permuté. Calibration : un seuil isolé à score ~0,56 et UNSTABLE ne prouve rien ; les seuils réels se distinguent par score + stabilité + accord inter-contrôles. |

## Données

`data/ising_derived.csv` : 960 lignes × 17 colonnes, 0 NaN, SHA-256
`10563d4d1405d09dac4eb468c1e44b59a27a028036ba1f6f729389fc55809c7b`.
6 originaux bit-identiques au lot ising-v354 (SHA `9027dfd5…`) + 8 dérivés + 3 nuls.
Construction **sans T** (le constructeur ne lit jamais le fichier température ;
une seule lecture CSV, la source — vérifié). Blocs = 24 blocs de 40 lignes
consécutives (position, pas de valeurs de T). Formules gelées :

- `expvar_<X>` (X ∈ energy, magnetization, fliprate, localvar) : variance
  expansive ddof=1 par bloc, k=0 → 0,0.
- `expmean_<X>` (X ∈ energy, magnetization) : moyenne expansive par bloc.
- `rollvar_<X>_40` (X ∈ magnetization, energy) : variance glissante arrière,
  fenêtre 40, min_periods=1, ddof=1, sans réinitialisation, première valeur → 0,0.
- Nuls : permutation `default_rng(1234)` de la série entière
  (`null_susceptibility`, `null_expvar_mag`, `null_rollvar_mag`).

Portes D1–D5 passées (dimensions, originaux intacts, réinitialisations par bloc,
nuls = permutations exactes, température copiée SHA vérifié `4863b1de…`).
Lignes = snapshots SIMULÉS (Ising 2D, L=32, graine 42). Tc = 2,2692 (Onsager,
réseau infini ; L=32 fini → transition arrondie) — vérité terrain du GÉNÉRATEUR,
jamais vue par le pipeline.

## Runs

11 runs, mode stable, w80, cohen_d, graine 42, HARMONIC_PROB 0,45, Theiler 1/φ
planché (source fixe), max 2 en parallèle, harnais `run_one_derived.py`.
Analysés FIXÉS aux 6 originaux (χ incluse, jamais contrôle). 11/11 OK,
0 échec, 0 repli, 0 avertissement. Durées 128–220 s/run.

| Contrôle | Famille | Seuil MC % | Score MC | Règle (2e passe) | Stabilité | Bootstrap (moyenne ± écart-type) | T au seuil MC | ΔT vs Tc |
|---|---|---|---|---|---|---|---|---|
| expvar_energy | expvar | 19,82 | 0,7060 | sqrt2 | VERY STABLE | 13,03 ± 2,62 | 1,9783 | −0,291 |
| expvar_magnetization | expvar | 18,63 | 0,7131 | uniform | VERY STABLE | 18,07 ± 1,86 | 1,9087 | −0,361 |
| expvar_fliprate | expvar | 16,39 | 0,6722 | uniform | MODERATELY STABLE | 14,52 ± 3,21 | 1,9087 | −0,361 |
| expvar_localvar | expvar | 10,53 | 0,8153 | uniform | UNSTABLE | 20,37 ± 26,38 | 1,8391 | −0,430 |
| expmean_energy | expmean | 35,60 | 0,7619 | uniform | MODERATELY STABLE | 35,08 ± 2,71 | 2,2565 | −0,013 |
| expmean_magnetization | expmean | 63,24 | 0,7630 | uniform | VERY STABLE | 63,68 ± 2,12 | 2,2565 | −0,013 |
| rollvar_magnetization_40 | rollvar | 20,38 | 0,7415 | uniform | MODERATELY STABLE | 19,65 ± 3,36 | 1,9783 | −0,291 |
| rollvar_energy_40 | rollvar | 9,50 | 0,8243 | uniform | VERY STABLE | 12,11 ± 2,09 | 1,8391 | −0,430 |
| null_susceptibility | nul | 79,48 | 0,5670 | uniform | UNSTABLE | 58,68 ± 25,24 | 2,5348 | +0,266 |
| null_expvar_mag | nul | 18,05 | 0,5558 | uniform | UNSTABLE | 15,97 ± 7,97 | 2,3261 | +0,057 |
| null_rollvar_mag | nul | 18,20 | 0,5653 | uniform | UNSTABLE | 57,53 ± 27,23 | 2,6043 | +0,335 |

Notes : le libellé de stabilité mesure la dispersion bootstrap, pas l'accord
avec le MC (ex. expvar_energy : VERY STABLE mais bootstrap à 6,8 pts du MC).
Deux passes MC par run ; la 2e passe ne monte pas toujours le score
(null_susceptibility : 1re passe 0,651 → 2e passe 0,567). Scores réels
0,672–0,824 ; scores nuls 0,556–0,567 — écart net, sans chevauchement.

## Paysage : une seule masse par run

Pics forts (rel ≥ 0,90), groupes séparés par > 2 pas de grille (0,1391) :

| Contrôle | Pics forts | Groupe principal (T) | Masse secondaire ≥ 0,20 ? |
|---|---|---|---|
| expvar_energy | 2 | [1,9783] | 1 point isolé [2,6739] — voir attribution |
| expvar_magnetization | 12 | [1,8391–1,9783] | non |
| expvar_fliprate | 4 | [1,8391–1,9087] | non |
| expvar_localvar | 6 | [1,7696–1,8391] | non |
| expmean_energy | 31 | [2,1174–2,3957] | non |
| expmean_magnetization | 34 | [2,1870–2,3957] | non |
| rollvar_magnetization_40 | 19 | [1,9087–2,0478] | non |
| rollvar_energy_40 | 1 | [1,8391] | non |
| null_susceptibility | 6 | [2,3957–2,5348] | 2 groupes ([2,1174], [2,7435–2,8130]) — nul, dispersé |
| null_expvar_mag | 3 | [2,3261–2,3609] | non |
| null_rollvar_mag | 13 | [2,3261–2,6739] | non (groupe unique large, dispersé) |

Application des règles au candidat 2,6739 : R1 — présent dans 1 seul run
dérivé (il en faut ≥ 2) ; R2 — absent sous rollvar_energy_40 (pics forts :
[1,8391] uniquement) → signature construction ; R3 — présent dans
null_susceptibility et null_rollvar_mag → signature machinerie. **Rejeté.**

## Seuils propres par flux analysé

Les 5 flux non-χ ont un seuil propre **identique au seuil MC du run**
(même % à 2 décimales) dans les 8 runs dérivés — le scan par flux, sur l'ordre
des lignes, culmine à la même coupure pour tous les flux qui transitent
ensemble. Sous les nuls, les seuils propres se dispersent (ex. null_rollvar_mag :
fliprate 32,93 % contre energy 62,11 %).

χ comme flux analysé ne suit JAMAIS le seuil du run : seuils propres
27,48–93,55 %, T 2,1174–2,4652, dispersés dans tous les runs (dérivés comme
nuls). Sa coupure propre est haute et instable — χ lue comme flux analysé a
sa propre lecture, distincte de la coupure du run.

## Diagnostics

- **F1/F2** : changements de signe 102–135 (dérivés) contre 158–162 (nuls) —
  les nuls sont plus bruyants. Réfractaires : famille dimensions +
  SingularityFmax saturée (comme au lot original).
- **Q5/Q6-A** : Q6-A moyennes 39–221 (dérivés) contre 87–119 (nuls) —
  chevauchement, ne sépare pas réel et nul. Q5 : 6,7–11,6 (dérivés) contre
  11,1–15,9 (nuls) — les nuls sont PLUS hauts. Ni Q5 ni Q6-A ne calibrent
  le réel contre le nul ici.
- **Bruit** : libellé « proxy de variance modéré » sur les 11 runs ; dérives
  bruit blanc médianes 4,0–8,0, aucune référence dégénérée.
- **NaN df_feat** : ~0 % (comme au lot original) — la métastabilité des liens
  ne se déclenche presque pas sur données continues.

## Opinion

1. **Il n'y a pas de deuxième seuil critique dans ces données.** Ising 2D à
   champ nul n'a qu'un seul point critique (théorème) ; le lot le confirme
   par l'absence de toute deuxième masse séparée sous 8 loupes dérivées.
2. **La famille basse est une vraie lecture, pas un artefact.** Six contrôles
   de variance, avec ou sans mémoire expansive, placent le seuil à
   T 1,84–1,98 : c'est le pied du régime de fluctuations — là où la variance
   commence à monter — et non le centre de la transition. Changer la loupe
   (premier moment → second moment) change le seuil lu, comme la philosophie
   du pipeline le prévoit.
3. **χ comme contrôle (lot original, T 2,1174) se situe entre les deux
   familles** — cohérent : χ est une variance normalisée par T, une loupe
   hybride entre variance brute et premier moment.
4. **Le nul calibre l'instrument** : seuil trouvé même sur contrôle permuté,
   score ~0,56, UNSTABLE, T dispersées. Un seuil isolé à ce niveau ne prouve
   rien. Les seuils réels (0,67–0,82, stables, concordants entre contrôles
   de même famille) s'en distinguent nettement.
5. **Suite logique** : L=64 + 2e graine pour confirmer la famille basse et
   mesurer si l'écart −0,29/−0,43 se resserre (effet de taille finie) ;
   puis réel-vs-nul loupe par loupe sur les 29 estimateurs. Ne pas chercher
   un deuxième point critique dans Ising 2D : la question est close pour ce
   système ; la famille basse est un onset, pas une seconde transition.

## Limites

Lecture descriptive seulement, aucune règle succès/échec importée. Une seule
taille (L=32), une seule graine (42). Comparaison à Tc = jugement descriptif
post-hoc. Question garder/retirer la comparaison Tc des rapports : toujours
ouverte (redirection de l'utilisateur du 28 oct. 2026, non tranchée).

## English summary

No second critical threshold exists in this data: all 8 derived-control runs
show a single strong-peak mass. Variance-family controls (expanding or
rolling) read the fluctuation onset at T 1.84–1.98; mean-family controls read
Tc at T 2.2565. The isolated 2.674 peak is an artifact (fails R1, present in
nulls, absent under rolling variance). Null controls still yield thresholds
(scores 0.56, UNSTABLE, scattered T), calibrating what noise looks like.

## Vérification

Synthèse : `synthese_derived.py` (traduction T recalculée indépendamment,
exclusion du contrôle vérifiée par assert, identité flip/fliprate vérifiée).
Sortie : `synthese_derived.json`. Chaque run : 11 fichiers sous
`runs/<controle>/`, `run_summary.json` OK.
