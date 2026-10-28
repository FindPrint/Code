# Ising 2D — Extension dérivés : factoriel complet + famille rollmean + nuls × v3.5.4-H1 (Q6-A)

**28 octobre 2026. Lot `ising-derived-ext`.** Protocole gelé avant construction et runs :
`PROTOCOLE_DERIVED_EXT.md`. Provenance complète : `PROVENANCE_DERIVED_EXT.md`.
Synthèse vérifiée : `synthese_derived_ext.py` → `synthese_derived_ext.json`.
Dossier diagnostique par run : `diagnostic_runs_ext.py` → `diagnostic_runs_ext.json`
(23 runs : 16 dérivés + 7 nuls, lots 1 et EXT poolés).
Pipeline `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A), SHA-256
`b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`.
Le pipeline ne voit jamais T ni Tc ; la traduction en T se fait après le run,
dans le harnais, sans retour dans aucun paramètre ; la comparaison à Tc est
un jugement descriptif post-hoc. Question garder/retirer la comparaison à Tc
des rapports : toujours ouverte.

## Verdict

**12/12 runs OK, 0 échec, 0 avertissement, 0 repli. Aucune deuxième masse
nulle part.** Chacun des 8 runs dérivés de l'extension n'a qu'un seul groupe
de pics forts. Les deux familles se confirment et se complètent :

- **Moyenne (expmean ×2 + rollmean ×4) → T = 2,2565 (ΔT −0,013)**, scores
  0,760–0,767, tous VERY STABLE : la moyenne expansive et la moyenne
  glissante lisent le même point, la bande Tc. La mémoire de construction
  ne fait pas le seuil.
- **Variance (rollvar ×2) → T = 1,77–1,84 (ΔT −0,43 à −0,50)**, scores
  0,772–0,871 : le pied du régime de fluctuations, plus bas encore que le
  lot 1 (1,84–1,98). La variance glissante descend plus bas que la variance
  expansive sur la même base.
- **Nuls (×4) : 2 normaux (scores 0,56–0,60, UNSTABLE) et 2 alarmants
  (0,7095 et 0,7218, MODERATELY STABLE, bootstrap en accord avec le MC).**
  Le score global seul ne distingue pas le réel du nul. Trois loupes le
  font, proprement, sur les 23 runs : amplitude du scan, Q4, proxy de bruit
  (voir § Dossier diagnostique).
- **Attribution poolée (16 dérivés + 7 nuls, règles R1–R5) : un seul
  candidat secondaire dans les 23 runs** — T = 2,6739, 1 seul run dérivé,
  présent dans 3 nuls, absent sous construction glissante : **artefact
  confirmé**. Aucun candidat ne survit à R1+R2+R3. Pas de deuxième point
  critique.

## Données et protocole

Dataset `data/ising_derived_ext.csv` : 960 lignes × 29 colonnes, 0 NaN,
SHA-256 `bae505d4c5e5e0f4faff2571515b872c67eb01545ebb367ff1203735cded34b4`.
Construit par `gen_derived_ext.py` (SHA-256
`6170c25c78a961be32f7a214c28b4a2521d910f443407d2292962f12c5abbd0b`) depuis
`data/ising_derived.csv` (SHA-256 `10563d4d…`), **sans aucune valeur de T**
(une seule lecture CSV, la source ; porte E6). Les 17 colonnes du lot 1 sont
préservées **octet pour octet** (porte E2, après correction d'un round-trip
de formatage flottant) ; les 12 colonnes ajoutées sont des transformations
déterministes, sans réinitialisation pour les glissantes, avec reset par bloc
de 40 pour les expansives. Formules : `expmean` = moyenne expansive par bloc ;
`rollvar_40` = variance glissante arrière, fenêtre 40, ddof=1, première valeur
→ 0,0 ; `rollmean_40` = moyenne glissante arrière, fenêtre 40, première valeur
= X[0] ; nuls = permutation `default_rng(1234)` de la série entière, mêmes
indices que le lot 1 (vérifié : Spearman nul/source ≈ 0, mêmes valeurs
triées). Portes E1–E7 toutes passées.

Exclusions (gelées, raisons mesurées) : `flip` (= 1024 × `fliprate`
exactement, rangs identiques) ; `susceptibility` comme base (Spearman vs T
+0,3860, non monotone — reste flux analysé) ; racines des variances (rangs
identiques, Spearman 1,0) ; autres fenêtres (variation de paramètre, pas une
famille). Monotonie descriptive des bases : fliprate +0,9986, energy +0,9787,
localvar +0,9770, magnetization −0,8758.

Paramètres : mode stable, w80, cohen_d, graine 42, HARMONIC_PROB 0,45,
Theiler 1/φ planché (source fixe). Analysés fixés aux 6 originaux (χ incluse,
jamais contrôle). Harnais `run_one_derived_ext.py` (copie de
`run_one_derived.py`, seuls les chemins changent). Max 2 en parallèle.
Lot total 22 min 25 s (13:01:09–13:23:25 EDT), 205–226 s par run.

**Anomalie de métadonnées (sans effet sur les runs) :** les champs
`famille`/`construction` des `run_summary.json` sont vides et `nul` vaut
`false` partout — les tableaux associatifs bash du script de lot ne sont pas
exportés aux sous-shells `xargs`. Les runs ne sont pas affectés (le contrôle
est passé par nom, la famille n'entre dans aucun calcul). La synthèse et le
dossier diagnostique re-dérivent la famille du préfixe du nom de contrôle
(vérifié). À corriger dans le harnais du prochain lot, pas en cours de lot.

## Seuils Monte Carlo par contrôle (extension)

| Contrôle | Famille | Seuil MC % | Score | Règle | Stabilité | Moy. ± std | T au seuil | ΔT vs Tc |
|---|---|---|---|---|---|---|---|---|
| expmean_fliprate | expmean | 35,60 | 0,7659 | uniform | VERY STABLE | 36,28 ± 2,15 | 2,2565 | −0,013 |
| expmean_localvar | expmean | 35,60 | 0,7636 | VERY STABLE | 35,86 ± 2,31 | 2,2565 | −0,013 |
| rollvar_fliprate_40 | rollvar | 9,50 | 0,7721 | uniform | MODERATELY STABLE | 7,70 ± 3,49 | 1,8391 | −0,430 |
| rollvar_localvar_40 | rollvar | 5,83 | 0,8710 | uniform | UNSTABLE | 18,59 ± 27,18 | 1,7696 | −0,500 |
| rollmean_energy_40 | rollmean | 35,17 | 0,7607 | uniform | VERY STABLE | 35,72 ± 2,05 | 2,2565 | −0,013 |
| rollmean_magnetization_40 | rollmean | 63,37 | 0,7618 | uniform | VERY STABLE | 64,20 ± 2,18 | 2,2565 | −0,013 |
| rollmean_fliprate_40 | rollmean | 35,17 | 0,7667 | uniform | VERY STABLE | 34,85 ± 2,03 | 2,2565 | −0,013 |
| rollmean_localvar_40 | rollmean | 35,17 | 0,7601 | uniform | VERY STABLE | 34,96 ± 2,11 | 2,2565 | −0,013 |
| null_expmean_fliprate | nul | 88,12 | 0,7218 | uniform | MODERATELY STABLE | 85,84 ± 3,80 | 2,2565 | −0,013 |
| null_rollvar_fliprate | nul | 38,50 | 0,5642 | uniform | UNSTABLE | 46,98 ± 25,40 | 2,3957 | +0,127 |
| null_rollmean_mag | nul | 21,69 | 0,5965 | uniform | UNSTABLE | 20,70 ± 24,10 | 2,5348 | +0,266 |
| null_rollmean_localvar | nul | 87,34 | 0,7095 | uniform | MODERATELY STABLE | 84,87 ± 3,91 | 2,1870 | −0,082 |

Source : `monte_carlo` partout. Deux passes MC par run. Les seuils par
défaut sont dispersés (5,12 % à 86,83 %) et ne sont jamais utilisés.

## Paysage et attribution (R1–R5, 23 runs poolés)

Pics forts = maxima locaux de la courbe de scan à rel ≥ 0,90. **Aucun run
dérivé des deux lots (16/16) n'a de masse secondaire séparée** (≥ 0,20 du
groupe principal, règle R1). Les groupes principaux : familles moyenne =
bande 2,12–2,40 centrée sur Tc ; familles variance = bande unique 1,77–1,98.

| Candidat | Runs dérivés | Présent dans les nuls (R3) | Sous glissant, même base (R2) | Verdict |
|---|---|---|---|---|
| T = 2,6739 | 1 (expvar_energy) | 3/7 (null_susceptibility, null_rollvar_mag, null_rollvar_fliprate) | absent (rollvar_energy_40 : [1,8391] seul) | **Artefact** — échoue R1, R2 et R3 |

Les 3 nuls du lot 1 présentaient déjà ce point isolé ; l'extension en ajoute
un troisième (null_rollvar_fliprate). Les autres candidats secondaires
détectés sont tous dans des runs nuls uniquement (1,9783 ; 2,2565 ;
2,7435) — aucun ne satisfait R1. **R4 : aucun candidat réel à confirmer
par L=64 + 2e graine.** R5 : tout est rapporté, aucun paramètre touché
après les résultats.

## Seuils propres par flux analysé (températures médianes, extension)

Les 5 flux non-χ ont un seuil propre égal au seuil MC du run dans les 8
runs dérivés (même T, à un pas de grille près pour expmean_fliprate et
rollmean_localvar_40 sur fliprate/flip : 2,3261). χ comme flux analysé ne
suit jamais le seuil du run (T 2,1174–2,3261).

Sous les nuls, les seuils propres se dispersent — sauf
null_rollmean_localvar, dont 5/6 flux s'accordent à T 2,1870, égale au
seuil MC : l'accord seuils propres = MC ne sépare donc pas ce nul-là (voir
§ suivant : ce sont l'amplitude du scan, Q4 et le proxy de bruit qui le
trahissent).

Matrice complète (lignes = flux analysés, colonnes = contrôles) :
`synthese_derived_ext.json`, clés `matrice_temperatures_seuils_propres` et
`matrice_seuils_propres_pct`.

## Dossier diagnostique : Q, bruit, F1/F2 — réel contre nul, loupe par loupe

Pour chaque run : profil du flux contrôle, scan, Q1–Q6-A, test de bruit
(proxy de variance + dérives par estimateur), F1/F2 avant/après seuil, flux
témoins (même base / même famille / autre famille). Fichier :
`diagnostic_runs_ext.json` (23 runs). Résumé :

| Loupe | Dérivés (16 runs) | Nuls (7 runs) | Sépare ? |
|---|---|---|---|
| Score MC | 0,672–0,871 | 0,556–0,722 | **Non** (chevauchement ; 2 nuls > 0,70) |
| Amplitude max du scan | 0,735–3,772 | 0,184–0,328 | **Oui, proprement** |
| Q4 (persistance) | 0,367–1,587 | 0,112–0,168 | **Oui, proprement** |
| Proxy de bruit (moyenne) | 0,609–0,836 | 0,319–0,435 | **Oui, proprement** |
| Q1 | 0,415–2,223 | 0,326–0,570 | Partiel (chevauchement bas) |
| Q2 | 0,000–14,275 | 0,956–1,945 | Non (moyenne fragile, dominée par quelques colonnes extrêmes) |
| Q5 | 6,668–11,629 | 8,862–15,897 | Non (nuls plus hauts) |
| Q6-A | 37,4–220,7 | 56,1–118,8 | Non (chevauchement) |
| F1/F2 changements de signe | 102–163 | 158–176 | Partiel (chevauchement 158–163) |
| Libellé de stabilité | 2 UNSTABLE / 14 stables | 2 MODERATELY STABLE / 5 UNSTABLE | Non |

**Lecture :** le score global, Q5, Q6-A et le libellé de stabilité ne
calibrent pas le réel contre le nul. L'amplitude du scan (le paysage est
plat sous permutation), Q4 et le proxy de bruit, oui — sur les 23 runs sans
exception. Les F1/F2 appuient (les nuls flippent partout : 158–176
changements de signe), sans séparer seuls.

**Cas rollvar_fliprate_40** (demande explicite) : flux en bosse, Spearman
vs T +0,14, médianes par bande 0,0000 / 0,0002 / 0,0004 / 0,0001 — il mesure
l'allumage des fluctuations. Seuil propre unanime des 5 flux non-χ à
9,50 % / T 1,8391. Témoins : expvar_fliprate 1,9087 (même point),
rollvar_energy/localvar 1,84/1,77 (même famille), expmean/rollmean_fliprate
2,2565 (après). Q2 3,454 (tension la plus haute), proxy 0,609 (le plus bas
des dérivés), 112 changements de signe (le plus bas des deux lots).
**Onset avant, lu par toute la famille variance.**

**Cas rollvar_localvar_40** (UNSTABLE, score le plus haut 0,871) : même
lecture de famille (témoins variance au même point, moyennes après), mais
bootstrap 18,59 ± 27,18 et Q2 = 0,0 — la question tension est morte, 148
changements de signe. L'instabilité n'est pas une signature unique : elle
se lit run par run.

## Opinion

1. **Pas de deuxième point critique** — confirmé sur 16 loupes dérivées,
   4 familles, 2 constructions, 7 nuls. Le théorème tient, l'instrument
   aussi.
2. **Deux lectures, un seul système** : les moyennes lisent la transition
   (T 2,2565), les variances lisent son pied (T 1,77–1,98). Changer de
   moment change le seuil lu ; ce n'est ni un artefact ni un second seuil,
   c'est la triangulation par les moments.
3. **Le score global ne suffit plus comme critère** : 2 nuls sur 7
   dépassent 0,70 avec bootstrap en accord. La calibration réel-vs-nul doit
   passer par l'amplitude du scan, Q4 et le proxy de bruit — loupe par
   loupe, comme demandé pour les 29 estimateurs.
4. **χ reste un flux analysé, jamais un contrôle sans mention du biais**
   (fenêtre expansive à mémoire ; son seuil propre ne suit jamais le run).
5. Suite logique inchangée : L=64 + 2e graine (mesurer si l'écart
   onset↔Tc se resserre), puis réel-vs-nul loupe par loupe sur les 29
   estimateurs depuis les sorties sauvées.

## Limites et fichiers

Lecture descriptive seulement. Une seule taille (L=32), une seule graine
(42), une seule fenêtre glissante (40). Comparaison à Tc descriptive.
Fichiers : `PROTOCOLE_DERIVED_EXT.md`, `PROVENANCE_DERIVED_EXT.md`,
`RAPPORT_DERIVED_EXT.md`, `synthese_derived_ext.json`,
`diagnostic_runs_ext.json`, `gen_derived_ext.py`, `run_one_derived_ext.py`,
`run_lot_ext.sh`, `synthese_derived_ext.py`, `diagnostic_runs_ext.py`,
`data/ising_derived_ext.csv`, `runs_ext/<contrôle>/` (11 fichiers par run),
`figures_ext/`. Le lot 1 reste dans `ising-derived/` (`runs/`, `figures/`).
