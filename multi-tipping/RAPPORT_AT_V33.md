# Rapport — pipeline v3.3 sur Ashkin-Teller (deux points de bascule)

Date : 22 oct. 2026 · Run : 213,6 s, mode stable, graine 42, 1 224 points, 6 flux
Pipeline : `pipeline_autonome_v3_3_fixed.py` tel quel, via pilote `run_v33_at.py`
Protocole gelé avant le run : `PROTOCOLE_AT.md`

## VERDICT

**Les deux seuils attendus sont retrouvés — chacun porté par ses propres flux.**

- Le seuil **global** du pipeline tombe sur le **seuil 1 (spin)** :
  MC **54,93 % → T = 4,77 ± 0,12** (attendu : T≈4,6–4,9, fenêtre 50–60 %). HIT.
- Le **seuil 2 (produit)** n'apparaît dans la courbe de scan globale que comme
  une **épaule soutenue** (pas de pic séparé) — mais le scan **par flux**
  (fonction du pipeline, configuration MC) le résout nettement :
  `magnetization_prod` → **64,95 % → T = 5,29 ± 0,15** (attendu : T≈5,2–5,6,
  fenêtre 62–73 %). HIT.

Lecture : le seuil unique global choisit la première transition ; la seconde
est portée par les flux produit. C'est la démonstration mesurée de la règle
« chaque flux son propre seuil » : à un seul seuil global, le seuil 2 se perd ;
par flux, il est là.

## Seuils critiques attendus (formulation explicite)

- **Seuil critique attendu n°1 (spin)** : désordre de s et τ, T≈4,6–4,9,
  soit 50–60 % de l'axe de progression (rang d'énergie).
- **Seuil critique attendu n°2 (produit)** : désordre de sτ, T≈5,2–5,6,
  soit 62–73 % de l'axe de progression.
  (Vérité terrain : générateur AT, J=1, U=2, L=28 — chutes mesurées sur les
  moyennes par T le 22 oct. ; transitions prouvées distinctes quand U > J.)

## Seuils globaux rendus par le pipeline

| Lecture | Seuil % | T mappée (± fenêtre ±1,5 %) |
|---|---|---|
| Monte Carlo (traité) | **54,93** (score 0,765 ; w=137, 660 candidats, min_grp=3) | **4,77 ± 0,12** |
| Défaut (traité) | 53,66 | 4,68 ± 0,09 |
| Monte Carlo (brut) | 54,16 | 4,72 ± 0,11 |
| Défaut (brut) | 52,20 | 4,60 ± 0,09 |
| Témoin grille 1001 | 54,9 | ≈ 4,77 |
| Stabilité (7 fenêtres 50–220) | moy 54,89, écart-type 1,94, min 52,81, max 58,12 — **VERY STABLE** | 4,77 ± 0,12 |

Aveuglement vérifié : l'entrée `at_fluxes.csv` ne contient aucune température ;
`control_label = energy` dans le JSON de sortie ; T utilisée seulement ici,
après coup, pour le mapping (méthode du test Ising du 17 oct. : température
des lignes autour de la frontière de rang d'énergie).

## Seuils propres à chaque flux (scan du pipeline, config MC : w=137, 660 candidats)

| Flux | Seuil propre % | Score max | T mappée | Fenêtre |
|---|---|---|---|---|
| magnetization_s | 52,50 | 5,399 | 4,62 ± 0,08 | **1 (spin) ✓** |
| magnetization_tau | 53,41 | 5,454 | 4,67 ± 0,10 | **1 (spin) ✓** |
| magnetization_prod | 64,95 | 4,972 | 5,29 ± 0,15 | **2 (produit) ✓** |
| flip_rate | 64,95 | 4,701 | 5,29 ± 0,15 | **2 (produit) ✓** |
| energy | 61,00 | 4,800 | 5,03 ± 0,12 | entre les deux |
| local_variance | 39,76 | 2,227 | 3,97 ± 0,13 | avant le seuil 1 |

Notes honnêtes :
- `energy` est à la fois contrôle et flux : son seuil propre (61,0 %) tombe
  entre les deux transitions — son paysage mélange les deux chutes.
- `local_variance` pointe tôt (39,8 %, score nettement plus faible, 2,23) :
  aucune troisième transition n'est connue dans ce modèle vers T≈4,0 ;
  lecture prudente = montée des fluctuations locales en approche du seuil 1,
  pas un troisième point critique.
- Top-3 candidats par flux : s [52,5 ; 53,4 ; 54,9], tau [53,4 ; 54,9 ; 52,5],
  prod [64,9 ; 64,6 ; 67,5], flip_rate [64,9 ; 66,8 ; 64,8],
  energy [61,0 ; 58,4 ; 60,7], local_variance [39,8 ; 40,5 ; 40,2].

## Paysage de scan global (courbe complète, pas seulement l'optimum)

Courbe traitée (défaut) : max **3,848 à 54,9 %**. Scores moyens par zone :
45–50 % : 3,196 · 50–60 % : 3,630 · **62–73 % : 3,193** · 75–85 % : 2,238 ·
88–97 % : 1,770. Meilleur candidat de la fenêtre 2 : 62,2 % à **93 % du max
global**. Courbe brute : même forme (max 4,090 à 52,2 % ; fenêtre 2 à 88 %).

Donc : entre les deux seuils, le score global ne retombe PAS au niveau de
base — il forme un plateau/épaule qui ne s'effondre qu'après ~73 %.
Le seuil 2 est présent dans le paysage global comme épaule, et comme pic
net dès qu'on scanne les flux séparément.

## Dérivés post-seuil F1/F2 (au seuil global 54,93 %)

Lecture « Tous » : le pipeline classe la transition en **2e ordre** pour les
cinq estimateurs.

| Estimateur | F1 (Tous) | F2 (Tous) |
|---|---|---|
| Higuchi | +0,00142 | −0,00011 |
| DFA | +0,00563 | −0,00060 |
| Katz | +0,00096 | +0,00004 |
| Hurst | −0,00419 | +0,00039 |
| SampleEn | +0,00902 | +0,00082 |

Par flux (F1 / F2) :

| Flux | Higuchi | DFA | Katz | Hurst | SampleEn |
|---|---|---|---|---|---|
| magnetization_s | +0,00151 / −0,00016 | +0,01102 / −0,00068 | +0,00106 / +0,00003 | −0,00751 / +0,00062 | +0,00575 / +0,00090 |
| magnetization_tau | +0,00111 / −0,00020 | +0,00847 / −0,00096 | +0,00102 / +0,00003 | −0,00568 / +0,00099 | +0,00589 / +0,00098 |
| magnetization_prod | +0,00233 / −0,00035 | +0,01198 / −0,00038 | +0,00134 / +0,00001 | −0,00891 / +0,00015 | +0,02118 / +0,00028 |
| energy | +0,00047 / +0,00006 | −0,00971 / −0,00172 | −0,00001 / −0,00000 | +0,00308 / +0,00052 | +0,00040 / +0,00003 |
| flip_rate | +0,00274 / −0,00008 | +0,00623 / −0,00007 | +0,00148 / +0,00008 | −0,00273 / +0,00002 | +0,01195 / +0,00150 |
| local_variance | +0,00033 / +0,00007 | +0,00580 / +0,00017 | +0,00088 / +0,00012 | −0,00341 / +0,00004 | +0,00893 / +0,00124 |

Fichier complet : `results_at_v33/transition_F1F2.csv` (35 lignes).

## Diagnostic de bruit et scores par flux

Étiquette : « Proxy de variance modéré — plusieurs flux agissent comme
proxies de variance résiduelle ».

| Flux | proxy | Q5 cand | Hurst moy | Δcorr | pente spectrale après |
|---|---|---|---|---|---|
| magnetization_s | 0,750 | 10,78 | 0,801 | −0,179 | −0,574 |
| magnetization_tau | 0,750 | 10,76 | 0,801 | −0,083 | −0,515 |
| magnetization_prod | 0,750 | 47,63 | 0,749 | −0,536 | −0,778 |
| energy | 0,750 | 13,05 | 0,923 | −0,064 | −1,781 |
| flip_rate | 0,750 | 24,65 | 1,016 | −0,094 | −1,061 |
| local_variance | 0,630 | 2,47 | 0,825 | −0,114 | −0,199 |

Signatures dominantes : Q1 — magnetization_tau DFA 9,378, tau Hurst 6,519,
s DFA 6,398 · Q2 — local_variance Higuchi 6,809, s Higuchi 6,538 ·
Q4 — energy Higuchi 3,281. Détail complet : `numerical_results.csv`.

## Spectre d'ancres (T_log, quatre classes, sans moyenne — médianes des dimensions, lecture)

Le saut pre → post au seuil global est porté par la classe **divergence**
sur presque tous les flux (ex. s : 4,00 → 6,45 ; prod : 3,36 → 6,10 ;
energy : 5,29 → 6,30) et par la **criticité** (s : 1,04 → 2,36 ;
tau : 1,04 → 2,48 ; prod : 2,25 → 2,07, déjà haute avant le seuil car le
produit est encore ordonné des deux côtés du seuil 1). Saturation et nulle
restent ≈ stables (1,03 et ~1,0). Détail : `anchor_spectrum_flat.csv`.

## Limites

- Taille finie L=28 : les transitions sont étalées (les fenêtres attendues
  en tiennent compte) ; le mapping % → T hérite de la dispersion d'énergie
  à T fixe (±0,08 à ±0,15).
- Mesure, pas interprétation : ce rapport dit où le pipeline a mis ses
  seuils et ce que chaque flux porte. La décision de ce que ça signifie
  pour la suite (loupe multi-seuils ?) se prend ensemble.
