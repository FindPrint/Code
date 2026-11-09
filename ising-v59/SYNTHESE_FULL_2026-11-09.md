# Synthèse full v5.9.0f — mode full 6/6 terminé, comparaison v5.4.0

**Date :** lundi 9 novembre 2026, rédigée 08h15 (heure de Montréal)
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Statut :** lot full TERMINÉ 6/6 — synthèse préparée pour le bilan du soir (cron `bilan-soir-v59-2026-11-09`, 17h05). Ne pas livrer avant 17h : Zackary travaille lun.–jeu. 2h–17h.

## 0. Verdict

**v5.9.0f ≡ v5.4.0 en mode full, seuils identiques point par point, durées à ±1 min près.**
Total full v5.9.0f : **35 345 s** (9 h 49 min). Total full v5.4.0 : **35 333 s** (9 h 48 min 53 s). Écart total : **+12 s** sur 6 runs, moyenne +2 s par run, extrêmes −58 s à +57 s.
Le ralentissement mesuré à l'étape 1 (+19 à +26 % en fast Ising, +2 à +74 % en synth) **ne se confirme pas en full** — il est expliqué par le diagnostic du ralentissement (voir §3) : surcoût fixe par run, invisible en full (<1 %).

## 1. Provenance

- **Originaux (jamais modifiés) :** v5.4.0 `workspace/user/files/UNIVERSAL_x5f_LOG_x5f_v5.4_0_1c23.py`, SHA `c1115e1c…` ; v5.9.0f `workspace/user/files/universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py`, SHA `4f80f6a7…`.
- **Protocole gelé :** `workspace/ising-v59/PROTOCOLE.md` (mêmes données, graine 42). Étape 3 décidée sous délégation de Zackary (8 nov., « À toi de voir ») : mode full seulement, 5 runs restants après l'étape 2.
- **Source de vérité des durées :** `workspace/ising-v59/ising/run.log`, lignes `END full/<contrôle> rc=0 duree_s=…`, revérifiées le 9 nov. 08h07 (heure de Montréal) : les 6 lignes END sont présentes, « FULL DONE » écrit à 07h21 (12:21 UTC), aucun processus du pipeline en cours.
- **Seuils :** relus dans chaque `master_results.json` (dossier `ising/full/<contrôle>/`) et dans les messages de fin de run ; MC et T_0 repris tels quels, sans traduction en T, sans comparaison à Tc.
- **Références v5.4.0 :** durées full du lot v5.4.0 (7–8 nov.), mêmes contrôles, même graine.

## 2. Tableau full 6/6 — v5.9.0f vs v5.4.0

| Contrôle | Fin (Montréal, 9 nov. sauf fliprate 8 nov.) | Durée v5.9.0f | Réf. v5.4.0 | Écart | MC | T_0 cascade | Brut T_0 | L7a | L7b |
|---|---|---|---|---|---|---|---|---|---|
| fliprate | 8 nov. 18h28 | 5 690 s | 5 679 s | +11 s | 28,90 % | 33,32 % | 0,16224609375 ambigu | UP 45,96 % | FRAGILE |
| flip | 20h58 | 5 573 s | 5 631 s | −58 s | 28,90 % | 33,32 % | 166,14 ambigu | UP 44,62 % | FRAGILE |
| energy | 9 nov. 01h09 | 5 845 s | 5 802 s | +43 s | 27,88 % | 73,26 % | −0,87109375 ambigu | UP 40,20 % | FRAGILE |
| magnetization | 03h11 | 5 984 s | 5 927 s | +57 s | 72,62 % | 13,05 % | 0,033203125 ambigu | DOWN 40,19 % | FRAGILE |
| localvar | 05h13 | 5 694 s | 5 708 s | −14 s | 27,38 % | 60,64 % | 0,5751350308641976 ambigu | UP 39,83 % | FRAGILE |
| susceptibility | 07h21 | 6 559 s | 6 586 s | −27 s | 15,84 % | 2,60 % | 0,0265495715130023 ambigu | DOWN 22,17 % | FRAGILE |

**Constats :**
- **Seuils identiques à v5.4.0 point par point** sur les 6 contrôles, en MC comme en T_0, et identiques au fast du même lot (étape 1) : la cascade T_0 ne bouge pas avec le mode.
- **Les 6 contrôles sont signalés non monotones** (test strict v5.4/v5.9) : toutes les valeurs brutes sont ambiguës (min/max/spread dans les sorties). Lire les T_0 en % comme des repères de progression, pas comme des valeurs uniques du contrôle.
- **L7b FRAGILE partout** (6/6 full, comme 143/143 sur l'ensemble du lot) : rappel — c'est la construction du check (axe renormalisé par fenêtre glissante, dérive 89 → 20 attendue géométriquement), pas une fragilité de l'instrument. Note : `workspace/ising-v59/NOTE_CALIBRATION_L7B_2026-11-08.md`. Confirmation par nul permuté encore à faire.
- **L7a** : UP sur fliprate, flip, energy, localvar ; DOWN sur magnetization, susceptibility — vote interne, ne prouve rien seul.

## 3. Diagnostic du ralentissement — terminé 9 nov. 07h52

Rapport : `workspace/ising-v59/DIAGNOSTIC_RALENTISSEMENT_2026-11-09.md` (sous-agent, copies seulement, originaux intacts SHA revérifiés).
- **Cause : multi-horizons v5.6 par défaut 1..12** — L1/L3/L5 recalculés 12 fois. Mesuré sur copies (cas A_single_fast_off, 13 runs) : v5.4.0 63 s, v5.9.0f défaut 101 s (+38 s), `--horizons "7"` 65 s, seuils identiques (MC 56,73 %, T_0 49,42 %). Loi : 65 s + 3,3 s × (n_horizons − 1).
- **Innocentés par la mesure :** walk-forward ~2 s, dashboard ~1 s, télémétrie ~1 s, poids de régime ~1 s, L7b-light ~0 s ; workers 3 vs 4 sans effet en fast (MC séquentiel).
- **Pourquoi le full ne ralentit pas :** surcoût fixe par run (~+40 s), <1 % d'un run de ~95 min.
- **Recommandation :** `--horizons "7"` pour les balayages fast/synth, rien à changer en full. Bonus cosmétique : `v590f.py --help` plante (% non échappé).

## 4. Nuit des redémarrages

Redémarrages VM pendant l'étape 3 (d'après run.log et les vérifications d'uptime) : ~21h16, ~23h26, ~01h26, ~03h27, ~05h26 (heures de Montréal, 8–9 nov.) — chacun a tué le run en cours, chacun suivi d'une relance durable depuis le fil principal, processus vérifié actif à chaque fois. Aucun run terminé perdu : les 6 END rc=0 sont intacts.
**9e redémarrage ~07h27, après « FULL DONE » (07h21) :** uptime 40 min vérifié à 08h07, aucun processus, rien perdu — aucun run n'était en cours. La surveillance `ising-v59-watch` (15 min, signale seulement) reste en place ; le lot est terminé, elle n'a plus rien à surveiller — à désactiver au bilan, sauf si une reprise est décidée.

## 5. Ce qui reste — décisions à Zackary (bilan du soir, pas sous délégation)

1. **Lancer les 24 runs restants** (predict/analyze/stable/robust, ~24 × 95 min ≈ 38 h de calcul pur, plus redémarrages) **ou clore le lot à full 6/6 ?**
2. **Publier les résultats full sur le dépôt privé FindPrint/Code ?** (diagnostic + cette synthèse + protocoles ; sorties brutes ~672 Mo hors push, comme pour l'étape 1.)
3. **Lancer la confirmation L7b par nul permuté ?** (dérive attendue si c'est la géométrie.)
4. **Garder le défaut 12 horizons, ou figer `--horizons "7"` dans les lanceurs fast/synth ?**

## 6. Ce qui ne fait pas partie de ce bilan

- Emploi : Isabelle Poirier / Lac Taureau — aucun courriel d'elle depuis le 7 nov. (à revérifier au bilan) ; seul Zackary sait si elle a appelé ; question oui/non déjà envoyée le 8 nov. au soir, relance prête si elle n'a pas appelé — **ne pas reposer la question**. Spirit Ridge (Osoyoos) — fiche questionnaire prête depuis le 6 nov., rien envoyé sans son go, pas de date limite.
- Good morning « buttercup » du lundi 9 nov. : déjà livré dans la série 9–15 nov. (8 nov. au soir).
- Playlist IY : 13 titres proposés (6 + 7), choix à lui.
- Cough Syrup / réponse à Marie : fil ouvert du side chat Musique, 3 chansons proposées, choix à lui — ne pas presser.
- Aucune traduction des seuils en T, aucune comparaison à Tc, aucun verdict final sur l'instrument.
