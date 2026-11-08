# Démo minute — le run synthétique 31/31 de la v5.9.0f

**Date :** 8 novembre 2026
**Auteur :** TagPrint (Muse), pour Zackary Drasse-Ménard
**Format :** texte à dire en 60 secondes environ (~155 mots), avec ce qu'on montre à l'écran à chaque temps. Les chiffres sont ceux de la synthèse étape 1, vérifiés run par run.

## Le texte (à dire)

**[0–10 s]** Trente et un runs, six modes, une seule graine : 42. C'est le test synthétique de la version 5.9.0f — le banc d'essai avant les vraies données Ising.

**[10–25 s]** Résultat : 31 sur 31. Vingt-neuf runs passent, et les deux seuls échecs sont voulus : une série trop courte, et un fichier manquant — deux cas limites que le pipeline doit refuser.

**[25–40 s]** Le seuil de cascade, T_0, ne bouge pas : 49,42 % sur tout le jeu de base, quel que soit le mode. Le seuil Monte Carlo, lui, dépend du mode : 56,73 % en fast, 68,03 % en full, 54,38 % en analyze et en stable.

**[40–52 s]** Et comparé à la version précédente, la 5.4.0 : tous les seuils sont identiques, run par run — mais tous les runs sont plus lents, de 2 à 74 %. La promesse « plus vite » ne tient pas sur cette étape.

**[52–60 s]** La suite : un gros run décisif sur données Ising dira si le ralentissement se confirme au long cours. Trente et un sur trente et un — la base est solide, la vitesse reste à prouver.

## Ce qu'on montre à l'écran

| Temps | À l'écran |
|---|---|
| 0–10 s | Le protocole : 31 runs, 6 modes (fast, full, predict, analyze, stable, robust), graine 42. |
| 10–25 s | Le journal : 31 END, 29 rc=0, 2 rc=1 attendus (D_short, D_missing_file). |
| 25–40 s | Le tableau des seuils : T_0 = 49,42 % partout ; MC 56,73 / 68,03 / 54,38 % selon le mode. |
| 40–52 s | Le tableau comparatif v5.9.0f vs v5.4.0 : seuils identiques, durées +2 % à +74 %. |
| 52–60 s | L'étape 2 : un run full/fliprate, référence 5 679 s. |

## Sources des chiffres

- Synthèse étape 1 : `workspace/ising-v59/SYNTHESE_ETAPE1_2026-11-08.md` (§ durées et seuils).
- Journal : `workspace/ising-v59/synth/run.log` (31 END).
- Durée totale des runs synth : 5 557 s (somme des durées, ~1 h 33).
- Référence v5.4.0 : `workspace/ising-v54/SYNTHESE_PARTIELLE_2026-11-08.md` (synth 31/31, T_0 49,42 %, mêmes MC).
