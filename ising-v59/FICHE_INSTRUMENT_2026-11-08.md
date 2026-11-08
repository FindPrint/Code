# Fiche instrument — pipeline universel v5.9.0f (L7a/L7b)

**Date :** 8 novembre 2026
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Statut :** une page, à lire sans le code. Les chiffres cités sont ceux du lot en cours ; le détail vit dans les synthèses.

## Ce que c'est

Un détecteur aveugle de changement de régime. Il prend des séries (flux), il rend des seuils — un seuil Monte Carlo par flux, et un seuil de cascade T_0. Il ne voit jamais la température, ni la valeur critique : la traduction en T se fait après le run, dans le harnais, sans retour dans aucun paramètre.

## Les règles qui le définissent

- **Deux flux minimum pour détecter**, chaque flux son propre seuil. Un seul flux ne détecte rien.
- **Le découvreur ne valide jamais.** Le contrôle ne figure jamais parmi les flux analysés et doit être monotone en T.
- **Un seuil n'est critique que s'il influence le système.** Un seuil isolé à score moyen, instable, dispersé, ne prouve rien.
- **Les flux retirés deviennent des témoins dormants** : codés, OFF par défaut, réactivables en expérience explicite. Un témoin ne se détruit jamais.
- **Aucun changement de version ni de protocole en cours de lot** sans go explicite. Les originaux ne sont jamais modifiés ; on travaille sur des copies.

## Ce qu'il mesure

- **Scan Monte Carlo** : seuil optimal par flux, avec score et incertitude bootstrap.
- **Cascade à cinq seuils** : T_0, le seuil central, identique d'un mode à l'autre sur les lots mesurés (fast = full = predict).
- **Scores Q1–Q6** : calme/chaos, tension au seuil, agressivité, persistance, actif/réactif, et Q6-A (mise à l'échelle sans centrage, non calibrée).
- **29 estimateurs fractals** (loupes) : ils décrivent un seuil après qu'il est choisi ; ils ne le choisissent pas. Lecture du 8 nov. 2026 : **26 signaux distincts** (3 paires duplicata : Hurst/Hurst2mH, CorrelationD2/GrassbergerProcaccia, SpectralBeta/SpectralDimension) ; saturation à 2 estimateurs en Ising, 4–5 en synthétique ; **Lyapunov est un artefact** (2 paliers, pas un signal).
- **L7a-COHERENCE** : le vote interne UP/DOWN/FLAT, inchangé depuis v5.6.
- **L7b-ROBUSTESSE** (nouveau) : audit, ne vote jamais. En mode light : FRAGILE sur 143/143 cas du lot — **ce n'est pas une fragilité de l'instrument** : le check walk-forward compare des seuils exprimés dans des fenêtres différentes à axe renormalisé, et la dérive mesurée est la signature géométrique attendue d'une transition unique (note de calibration du 8 nov. 2026).

## Ce qu'il ne fait pas

- Il ne traduit pas en T et ne compare pas à Tc : c'est le harnais, après, en jugement descriptif.
- Il ne déclare rien sur l'instrument entier à partir d'une seule loupe : un verdict exige la comparaison réel contre nul, loupe par loupe.
- Il ne vend rien : l'instrument reste strictement privé, jamais exposé ni commercialisé.

## État du test en cours (8 nov. 2026)

- **Version :** v5.9.0f, fichier `universal_x5f_log_x5f_L7a_x5f_L7b_x5f_v5.9.0f_0_j1p1.py`, 13 013 lignes, SHA `4f80f6a7d0809e802cbc9ec30c0bed552c1c8a95eb58687fd78e4ffd8e808260`, jamais modifié. Cécité vérifiée (12 occurrences temperature/onsager, toutes hors analyse).
- **Étape 1 terminée (13h51) :** synth 31/31 + fast Ising 6/6, 35 runs rc=0 — **tous plus lents que v5.4.0** (+2 % à +74 % en synth, +19 % à +26 % en fast Ising), **tous les seuils identiques**.
- **Étape 2 en cours :** un run full/fliprate décisif (référence v5.4.0 : 5 679 s). Première tentative tuée par redémarrage VM ~14h39, relancée 14h52:51, fin attendue ~16h30.
- **Étape 3 (30 runs restants) :** décision selon le résultat de l'étape 2.

## Provenance

- Données synthétiques : `workspace/ising-v425-all-options/data/`, graine 42. Données Ising : `workspace/ising-v354/data/ising_classic_v354.csv`, SHA `9027dfd5…` (L=32, T 1,7–3,3, 40 snapshots/T, graine 42).
- Protocole gelé : `workspace/ising-v59/PROTOCOLE.md`. Synthèse étape 1 : `workspace/ising-v59/SYNTHESE_ETAPE1_2026-11-08.md`. Note de calibration L7b : `workspace/ising-v59/NOTE_CALIBRATION_L7B_2026-11-08.md`. Lecture des estimateurs : `workspace/ising-v59/LECTURE_ESTIMATEURS_2026-11-08.md`.
- Référence de comparaison : v5.4.0, SHA `c1115e1c…`, lot arrêté à 13/36 le 8 nov. 11h38 (synthèse partielle : `workspace/ising-v54/SYNTHESE_PARTIELLE_2026-11-08.md`).
