# Synthèse PARTIELLE du lot v5.4.0 — Ising 13/36, synth 31/31

**Date :** 8 novembre 2026, ~11h45 HNE.
**Statut : PARTIELLE.** Lot arrêté sur ordre de Zackary (« arrêter les run et faire
l'analyse correctement sans les autres restant des 13/36 car on en aura pour
encore des jours », 8 nov. 11h38). Ce n'est pas le lot complet (36 runs Ising
prévus) et ce n'est pas un verdict final sur l'instrument.

## 0. Verdict

- **Synth : 31/31 terminés** (29 rc=0 + 2 rc=1 attendus : D_short série trop
  courte, D_missing_file fichier manquant).
- **Ising : 13/36 terminés rc=0** — fast 6/6, full 6/6, predict 1/6 (fliprate).
- **Arrêt vérifié 11h39 : 0 processus.** predict/flip tué en cours (rc=143,
  475 s) ; predict/energy démarré par le lanceur après le premier kill puis tué
  à 22 s (START sans END, dossier vide). Aucun run ne tourne plus.
- **Surveillance `ising-v54-watch` supprimée** (cron retiré 11h41) : elle aurait
  signalé un faux « run mort » au passage suivant, alors que l'arrêt est
  volontaire.
- **Restent non mesurés : 23 runs** — predict 5/6, analyze 6/6, stable 6/6,
  robust 6/6. Les lanceurs sont résumables (SKIP des 13 terminés) : une reprise
  repartirait à predict/flip. Reprise = décision de Zackary, rien n'est relancé.

## 1. Pourquoi des jours : les durées mesurées

| Mode | Durées Ising mesurées (s) | Ordre de grandeur |
|---|---|---|
| fast | 203, 205, 212, 274, 211, 268 | ~3–5 min |
| full | 5 679, 5 631, 5 802, 5 927, 5 708, 6 586 | ~95–110 min |
| predict | 5 637 (fliprate) | ~94 min, comme full |

23 runs restants × ~95 min ≈ **36 h de calcul pur**, sans compter les
redémarrages VM — la nuit du 7 au 8 nov. en a compté 5 (00h25, 00h44, 02h33,
04h29, 06h27), et chaque redémarrage tue le run en cours qui repart de zéro
(full/energy a ainsi été tué à 02h33 après 92 min, à ~3 min de la fin). En mur,
c'est bien plusieurs jours. L'ordre d'arrêt est cohérent avec ces chiffres.

## 2. Résultats Ising — les 13 runs terminés

MC = `run_pipeline.threshold_metadata.opt_threshold` (%).
T_0 = `five_threshold_cascade.T_0_Monte_Carlo_Central` (%).
Brut = `five_threshold_cascade.thresholds_in_control_units.T_0_Monte_Carlo_Central`
(`control_value_raw`, `ambiguous`).

### fast 6/6

| Contrôle | Durée (s) | MC (%) | T_0 (%) | Brut | Ambigu |
|---|---|---|---|---|---|
| fliprate | 203 | 37,01 | 33,32 | 0,16224609375 | oui |
| flip | 205 | 37,01 | 33,32 | 166,14 | oui |
| energy | 212 | 37,17 | 73,26 | −0,87109375 | oui |
| magnetization | 274 | 64,23 | 13,05 | 0,033203125 | oui |
| localvar | 211 | 37,50 | 60,64 | 0,5751350308641976 | oui |
| susceptibility | 268 | 27,27 | 2,60 | 0,0265495715130023 | oui |

### full 6/6

| Contrôle | Durée (s) | MC (%) | T_0 (%) | Brut | Ambigu |
|---|---|---|---|---|---|
| fliprate | 5 679 | 28,90 | 33,32 | 0,16224609375 | oui |
| flip | 5 631 | 28,90 | 33,32 | 166,14 | oui |
| energy | 5 802 | 27,88 | 73,26 | −0,87109375 | oui |
| magnetization | 5 927 | 72,62 | 13,05 | 0,033203125 | oui |
| localvar | 5 708 | 27,38 | 60,64 | 0,5751350308641976 | oui |
| susceptibility | 6 586 | 15,84 | 2,60 | 0,0265495715130023 | oui |

### predict 1/6

| Contrôle | Durée (s) | MC (%) | T_0 (%) | Brut | Ambigu |
|---|---|---|---|---|---|
| fliprate | 5 637 | 28,90 | 33,32 | 0,16224609375 | oui |

**Constat 1 — la cascade T_0 ne bouge pas avec le mode.** Pour chaque contrôle,
T_0 est identique en fast, full et predict (fliprate 33,32 ; flip 33,32 ;
energy 73,26 ; magnetization 13,05 ; localvar 60,64 ; susceptibility 2,60).
Comme en v4.2.5 : le mode change le scan, pas la cascade.

**Constat 2 — les valeurs brutes sont toutes ambiguës en Ising.** Les 13 runs
portent `ambiguous=True`. Exemple : susceptibility, brut 0,02655, étalement
0,0000–0,0437 sur les 5 points les plus proches. Le % reste un repère de
progression, pas une valeur unique du contrôle (voir §4).

## 3. Comparaison v4.4.2 — point par point

Références v4.4.2 (lot figé à 37/67) : fast MC 37,07 / 37,07 / 37,56 / 63,41 /
37,80 / 21,22 % ; T_0 33,32 / 33,32 / 73,26 / 13,05 / 60,64 / 2,60 %.

### fast : T_0 identiques, MC proches sauf susceptibility

| Contrôle | MC v5.4.0 | MC v4.4.2 | Écart (pts) | T_0 v5.4.0 | T_0 v4.4.2 |
|---|---|---|---|---|---|
| fliprate | 37,01 | 37,07 | −0,06 | 33,32 | 33,32 |
| flip | 37,01 | 37,07 | −0,06 | 33,32 | 33,32 |
| energy | 37,17 | 37,56 | −0,39 | 73,26 | 73,26 |
| magnetization | 64,23 | 63,41 | +0,82 | 13,05 | 13,05 |
| localvar | 37,50 | 37,80 | −0,30 | 60,64 | 60,64 |
| susceptibility | 27,27 | 21,22 | **+6,05** | 2,60 | 2,60 |

La cascade fast est inchangée entre v4.4.2 et v5.4.0. Le scan fast bouge peu
(≤ 0,82 pt) sauf sur susceptibility (+6,05 pts) — le seul écart notable du
mode fast.

### full : données nouvelles, et identiques au robust v4.2.9

v4.4.2 n'a **jamais terminé un run full** (full/fliprate tué à ~67 min sans
aucune sortie). Les 6 full v5.4.0 sont donc des données nouvelles — et elles
reproduisent **point par point le robust v4.2.9** (lot arrêté à 34/36) :

| Contrôle | MC full v5.4.0 | MC robust v4.2.9 | T_0 full v5.4.0 | T_0 robust v4.2.9 |
|---|---|---|---|---|
| fliprate | 28,90 | 28,90 | 33,32 | 33,32 |
| flip | 28,90 | 28,90 | 33,32 | 33,32 |
| energy | 27,88 | 27,88 | 73,26 | 73,26 |
| magnetization | 72,62 | 72,62 | 13,05 | 13,05 |
| localvar | 27,38 | — (jamais terminé) | 60,64 | — |
| susceptibility | 15,84 | — (jamais lancé) | 2,60 | — |

Le mode full de v5.4.0 donne le même scan que le mode robust de v4.2.9 sur les
4 contrôles comparables. localvar et susceptibility full n'ont aucun équivalent
robust terminé.

### predict : premier point, identique à full

v4.4.2 n'a jamais lancé predict en Ising. predict/fliprate v5.4.0 (28,90 % /
33,32 %, 5 637 s) est **identique à full/fliprate** (28,90 % / 33,32 %,
5 679 s). Un seul point : on ne peut pas conclure que predict = full en
général, mais sur fliprate les deux modes coïncident, et predict coûte comme
full (~94 min), pas comme fast.

## 4. Nouveautés v5.4.0 — ce qui a été mesuré

### 4.1 Valeurs brutes de cascade (item 21)

Présentes pour les 13 runs (`thresholds_in_control_units`). **Toutes
ambiguës** en Ising. Seule exception du lot entier : D_const en synthétique
(contrôle constant 5,0, `ambiguous=False`). La valeur brute accompagne le %,
elle ne le remplace pas — l'en-tête du JSON le dit explicitement
(`unit_note` : « valeur brute du controle, a cote du % (ne remplace pas le %) »).

### 4.2 Avertissement contrôle non monotone (item 20) — les 6 contrôles Ising

**Fait mesuré : les 6 contrôles Ising sont signalés NON MONOTONES**
(`metadata.control_monotonicity.monotone=False`, `warning_issued=True`), sur les
13 runs — 13 blocs `[AVERTISSEMENT-CONTROLE-NON-MONOTONE]` dans `ising/run.log`.
Spearman ordre vs valeur (960 lignes) :

| Contrôle | Spearman r | Sens |
|---|---|---|
| fliprate | +0,9977 | croissant |
| flip | +0,9977 | croissant |
| energy | +0,9776 | croissant |
| magnetization | −0,8755 | décroissant |
| localvar | +0,9760 | croissant |
| susceptibility | +0,3890 | faible — pic attendu (monte puis descend) |

**Lecture :** le test est strict, ligne par ligne, sur la série brute : 960
lignes = 24 températures × 40 snapshots, et les valeurs fluctuent d'un snapshot
à l'autre à température fixée — la stricte monotonie ligne à ligne échoue donc
même pour des contrôles monotones en moyenne par température. La magnétisation
décroît avec T (r négatif, attendu physiquement) mais n'est pas strictement
monotone ligne à ligne ; la susceptibilité, qui pique à la transition, ne peut
pas l'être par construction (r = 0,39).

**Conséquence au regard du décret** (« le contrôle doit être monotone en T ») :
tel qu'implémenté, le test ne valide **aucun** des 6 contrôles Ising. Ce n'est
pas une propriété nouvelle des données — c'est le comportement de l'instrument
sur une série bruitée par snapshots. Les % restent des repères de progression ;
toute lecture d'une valeur brute unique du contrôle est à écarter sur ce lot.
Si un jour le test doit valider ces contrôles, c'est sa définition (moyennes
par température ? tolérance aux fluctuations ?) qui devra être gelée d'abord —
pas les données.

### 4.3 Cible fixe (item 19) — politique confirmée, diagonale signalée

- `target_policy = "fixed"` confirmé dans `controls_summary.json` (C_multi et
  C_all, synthétique) ; cible globale résolue : ControlA.
- Cas diagonal : quand la cible fixée égale le contrôle (ControlA), repli
  **explicite** vers la première colonne différente (Target), signalé par 3
  blocs `[CIBLE-FIXE-DIAGONALE]` dans `synth/run.log` — « Ce run diagonal
  n'est PAS comparable aux autres ».
- D_target_eq_control (synth, cas diagonal) : MC 56,73 %, T_0 49,42 %, brut
  48,8433 ambigu — **identique au fast de base** : le repli ne change pas le
  seuil sur ce jeu.
- En Ising single, `target_policy`/`target_resolution` sont absents des
  `threshold_metadata` (la politique ne s'exerce qu'en multi/all) — attendu.

### 4.4 Synthétique 31/31 — rappel

T_0 de cascade quasi constant **49,42 %** sur tout le jeu de base ; valeurs
brutes ambiguës partout sauf D_const (5,0, non ambigu). En multi/all, chaque
contrôle donne son propre seuil (ControlA 56,73/49,42 ; Flux1 9,68/44,41 ;
Flux2 14,42/87,60 ; Target 62,50/25,83 en fast). D_seed7_horizon5 : T_0 49,68 %
(léger écart). D_2000_fast_off : MC 49,79 %, T_0 48,63 %.

## 5. Ce qui n'est pas dans cette synthèse

- **Aucune traduction en T, aucune comparaison à Tc.** Par règle : la
  traduction se fait après le run, dans le harnais, sans retour dans les
  paramètres — et la question de garder/retirer la comparaison Tc des rapports
  reste OUVERTE. Rien n'est jugé ici contre Tc.
- **Aucun verdict final sur l'instrument.** Il manque 23 runs, dont tous les
  analyze/stable/robust. Les constats ci-dessus portent sur fast/full/predict
  partiel seulement.
- **Q5 inchangé** (« Reporté » en en-tête v5.4.0) ; la question du patch
  v5.4.1 (CONTROL_MODE, livrée le 7 nov.) reste sans réponse de Zackary.
- Les 29 estimateurs fractals (diagnostic après seuil) n'ont pas été relus
  loupe par loupe dans cette synthèse — ils dorment dans les JSON.

## 6. Provenance

- Code : `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py`,
  10 675 lignes, SHA
  `c1115e1c4803bc56d330e37e1adb7a6697ea5393c9a42678111dd76162fb05be`,
  jamais modifié. `VERSION = "v5.4"`,
  `VERSION_MASTER = "v5.4-CibleFixeNonSilencieuse"`.
- Données Ising : `workspace/ising-v354/data/ising_classic_v354.csv`, 960
  lignes, 6 colonnes, SHA `9027dfd5…`, L=32, T = linspace(1.7, 3.3, 24),
  40 snapshots/T, graine 42. Fichier température séparé, jamais lu par le
  pipeline.
- Données synth : `workspace/ising-v425-all-options/data/`, graine 42.
- Protocole : `workspace/ising-v54/PROTOCOLE.md` (gelé 7 nov. 14h15,
  amendement §6 : piège CONTROL_MODE, `--control-mode single` explicite
  partout ; §7 : lecture des résultats).
- Journaux : `workspace/ising-v54/synth/run.log` (31 END),
  `workspace/ising-v54/ising/run.log` (14 END : 13 rc=0 + 1 rc=143 tué par
  l'arrêt). Marqueur « V54 DONE » jamais écrit (le maître `run_v54.sh` n'a pas
  été lancé ; la phase Ising tournait seule) — ne pas le chercher.
- Extraction : `workspace/ising-v54/extract_partiel.py` (lit chaque
  `master_results.json`, sorties vérifiées une par une).
- Arrêt : ordre de Zackary 8 nov. 11h38 ; processus tués 11h39, 0 processus
  vérifié ; surveillance supprimée 11h41.
