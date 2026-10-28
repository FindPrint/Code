# PROTOCOLE — Ising classique 2D × pipeline v3.5.4-H1 (Q6-A)

**Gel : 28 octobre 2026, avant toute génération et tout run. Aucune
modification de ce protocole après le gel sans nouvelle version datée.**

*Frozen protocol — classical 2D Ising × v3.5.4-H1 pipeline (Q6-A).
Frozen 28 Oct. 2026, before any generation or run.*

## 1. Question

Le pipeline v3.5.4-H1 (29 estimateurs intégrés, Q6-A : mise à l'échelle
seule, Theiler Niveau B 1/φ planché) détecte-t-il un seuil critique sur
un système physique simulé à transition connue (Ising 2D, Tc d'Onsager
= 2,2692), et que dit chaque flux en tant que contrôle ? Rotation
complète : chaque flux sert de contrôle à tour de rôle, les 5 autres
étant les flux analysés. Le contrôle est EXCLU des flux (règle Porte D,
décret permanent).

*Does the pipeline detect a critical threshold on a simulated system
with known transition (2D Ising, Onsager Tc = 2.2692), and what does
each flux say as control? Full rotation: each flux is control in turn,
the other 5 are the analysed fluxes. Control excluded from fluxes.*

## 2. Générateur (données simulées, PAS mesurées)

- Fichier : `gen_ising_classic_v354.py` (adapté de
  `workspace/gen_ising_proxy.py`, mêmes `sweep`, `energy_per_spin`,
  `local_variance` — code éprouvé, graine identique).
- Modèle : Ising 2D carré, L = 32 (N = 1 024 spins), J = 1, conditions
  périodiques, Metropolis checkerboard (damier, 2 sous-réseaux).
- Graine : `default_rng(42)`. Initialisation aléatoire neuve à chaque T.
- Températures : `linspace(1.7, 3.3, 24)` (pas ≈ 0,0696), ordre croissant.
  Tc = 2,2692 est encadré avec marge des deux côtés.
- Équilibration : 1 500 sweeps par T. Mesure : 40 snapshots par T,
  séparés par GAP = 50 sweeps. Lignes : 24 × 40 = **960**.
- Ordre des lignes : ordre de simulation (T croissante). Le pipeline
  trie de toute façon par rang du contrôle (`rankdata`) ; l'ordre des
  lignes ne fait que préserver l'histoire temporelle.

## 3. Les 6 flux (une ligne = un snapshot)

Ordre des colonnes gelé : `fliprate, flip, energy, magnetization,
localvar, susceptibility`.

| Flux | Définition (par snapshot, après les GAP sweeps) |
|---|---|
| `flip` | Nombre moyen de spins retournés acceptés par sweep, moyenné sur les 50 sweeps du GAP (flottant). |
| `fliprate` | `flip / N` (fraction de sites retournés par sweep). Proportionnel exact à `flip` — redondance voulue par la demande, lue comme telle. |
| `energy` | Énergie par spin, J = 1, chaque liaison comptée une fois (`roll(1,0) + roll(1,1)`). |
| `magnetization` | \|aimantation\| par spin : `abs(spins.mean())`. Valeur absolue = paramètre d'ordre usuel (la valeur signée changerait de signe sous Tc et ne serait pas monotone en T). |
| `localvar` | Variance du voisinage 3×3, moyennée sur les sites (`uniform_filter`, mode `wrap`) — définition reprise de `gen_ising_proxy.py`. |
| `susceptibility` | χ = N · Var(m_signée) / T, variance (ddof=1) sur fenêtre EXPANSIVE des snapshots du même bloc T (snapshots 0..k) ; k=0 → 0,0. La m signée est interne au générateur, jamais une colonne. |

- Fichier données : `data/ising_classic_v354.csv` (6 colonnes, 960 lignes,
  aucun NaN attendu, aucune colonne température).
- Fichier température SÉPARÉ : `data/ising_classic_v354_temperature.csv`
  (une colonne `temperature`, 960 lignes, même ordre — pour analyse
  après coup, jamais lu par le pipeline).
- Nature des lignes : **snapshots simulés** (Metropolis, graine 42),
  pas des spécimens mesurés. Vérité terrain : Tc = 2,2692 (Onsager,
  réseau carré infini ; L = 32 fini → transition arrondie, pic de χ
  décalé/élargi, attendu).

## 4. Runs — rotation des contrôles

- Pipeline : `Tlog_v3_5_4_harmonic_v1.py` (v3.5.4-H1, Q6-A),
  SHA-256 `b54fcf66a0f0e90941108e1a2b11a1f0c2679044eda1be2b0a875e4ed4bd165d`,
  original intact, jamais modifié pendant le lot.
- 6 runs, un par contrôle : `fliprate`, `flip`, `energy`,
  `magnetization`, `localvar`, `susceptibility`. Dans chaque run :
  contrôle = le flux nommé, flux analysés = les 5 autres
  (`flux_mapping` explicite, contrôle exclu).
- Paramètres gelés (identiques au lot mushroom / pilote v3.5) :
  mode `stable`, `w_size` = 80, test `cohen_d`, graine 42,
  `HARMONIC_PROB` = 0,45 (défaut du module), `full_triangulation` =
  False, Theiler défauts v3.5.3 (facteur 1/φ, mode planché,
  source fixe). Groupes actif/réceptif : défauts positionnels du
  pipeline (2 premiers / 2 suivants dans l'ordre des colonnes hors
  contrôle) — règle identique pour les 6 runs, memberships
  documentés par run dans `run_summary.json`.
- Parallélisme : max 2 runs simultanés (plafond VM). Harnais durable
  `run_one_ising.py` (adapté de `pilote/run_one_v35.py`, mêmes exports
  + `run_summary.json` + seuils propres par flux + paysage + F1/F2).
  Reprise : un run avec `run_summary.json` est sauté, un run partiel
  est relancé de zéro, jamais compté.
- Sorties par run : `runs/<controle>/` — `pipeline_results.json`,
  `numerical_results.csv`, `text_report.txt`, `threshold_scan.png`,
  `noise_diagnostic.png`, `scan_curve.csv`, `per_flux_thresholds.csv`,
  `landscape_peaks.csv`, `transition_F1F2.csv`, `run_summary.json`.

## 5. Portes de vérification physique (AVANT les runs)

La génération s'arrête ici si une porte échoue — aucun run lancé :
- P1 : la moyenne par bloc de `magnetization` chute de plus de 0,15
  entre deux T consécutives quelque part, et Tc = 2,2692 est encadré
  par la zone de chute (même critère que `gen_ising_proxy.py`).
- P2 : la moyenne par bloc de `energy` croît avec T (corrélation de
  Spearman > 0,9 sur les 24 moyennes).
- P3 : la moyenne par bloc de `susceptibility` atteint son maximum à
  moins d'un pas de grille de Tc (|T_pic − 2,2692| ≤ 0,15).
- P4 : 960 lignes, 6 colonnes, 0 NaN, 0 doublon exact ; température
  séparée : 960 lignes, ordre identique (vérifié par hachage conjoint
  des deux fichiers et recomptage).

## 6. Lecture attendue (descriptive, sans conclusion importée)

- Seuil MC par run (%, score, stabilité bootstrap + moyenne/écart-type),
  seuils propres par flux, paysage (pics locaux), Q1–Q6 moyennes,
  F1/F2 avant/après seuil, diagnostic de bruit.
- Traduction température : pour chaque seuil (%), la température
  médiane des lignes dont le rang du contrôle encadre le seuil
  (fichier température séparé, lecture après coup uniquement).
- Comparaison descriptive au Tc d'Onsager : écart en T entre le seuil
  traduit et 2,2692, par contrôle. Aucune règle « succès/échec »
  importée : le paysage complet est rapporté, pas un seul point.
- Limites gelées : L = 32 fini (transition arrondie) ; χ par fenêtre
  expansive (biais de début de bloc) ; `flip`/`fliprate` exactement
  proportionnels ; contrôles discrets/à paliers lus en rangs.

## 7. Traçabilité et publication

- `PROVENANCE.md` : source du générateur (adaptation, auteur, date),
  SHA-256 du générateur, des deux CSV, du code pipeline, nature des
  lignes (simulées), comment chaque valeur a été produite, ce qui
  manque (pas de mesures réelles, pas de champ magnétique, pas de
  tailles L multiples).
- Synthèse vérifiée d'abord (`RAPPORT.md`), puis PDF + zip des
  résultats complets, puis publication GitHub (dépôt privé FindPrint/
  Code : texte par snapshot, binaires par Release, vérifiés par
  relecture) selon la règle permanente.
- Aucun run, aucune version, aucun paramètre ne change en cours de lot
  sans go explicite de l'utilisateur.
