# RAPPORT — Test de la cascade 5 seuils v3.7.0-HP-v3 sur le banc Ising

**Test exécuté le 30 octobre 2026, protocole gelé avant les runs
(`PROTOCOLE.md`). Code reçu, jamais modifié. Données : banc Ising v3.5.4
validé (L=32, T 1.7–3.3, 24 valeurs, 40 snapshots par T, graine 42).**

## Verdict d'abord

- La cascade pointe près de la transition sur la série réelle
  (T_0 = 2,3261), un pas de grille au-dessus du repère du lot v3.5.4
  (2,2565) et de Tc d'Onsager (2,2692).
- Mais elle ne sépare PAS le réel du nul : sur 20 nuls par permutation,
  T_0 s'étale de 1,84 à 3,16 (médiane 2,7087), le réel se classe 6e sur
  21, et un nul tombe exactement sur 2,2565. La structure « 5 zones
  ordonnées » apparaît sur 19 nuls sur 20 : elle est algorithmique, pas
  probante.
- Attribution E_thermal : son T_0 (2,3261, identique à celui de M) est
  piloté par M, pas par T seul — mélanger M le déplace à 2,7435,
  mélanger T ne le déplace qu'à 2,3957. La crainte « T déguisé » est
  réfutée pour T_0 ; E_thermal n'apporte en revanche aucune information
  indépendante au-delà de M (même T_0).
- Conclusion, loupe par loupe : la cascade seule ne prouve pas la
  transition sur ce banc. Elle est cohérente avec elle, mais
  indistinguable du nul sur T_0. C'est exactement pour cela que
  l'instrument compte 29 estimateurs, 6 questions, une analyse de bruit
  et des dérivées : la preuve, si elle vient, viendra de l'attribution
  multi-loupe, pas d'une loupe seule.

## Résultats complets

Repère descriptif (lot v3.5.4) : T = 2,2565. Tc d'Onsager : 2,2692.
Pas de grille : 0,0696. Conversion %→T par le harnais, descriptive.

| Série | T_0 (%) | T_0 (T) | Zones ordonnées | Statut |
|---|---|---|---|---|
| V1 aimantation / T | 41,67 | **2,3261** | oui | ok |
| V1b aimantation snapshots | 39,64 | — | non (T_+1 = T_+2) | ok |
| V2 E_thermal réel | 41,67 | **2,3261** | oui | ok |
| V3 E_thermal, M mélangé (g7) | 66,67 | 2,7435 | oui | ok |
| V4 E_thermal, T mélangé (g8) | 45,83 | 2,3957 | oui | ok |
| V5 nuls ×20 (g1234) | 12,5–91,67 | 1,8391–3,1609, médiane 2,7087 | 19/20 | ok |

Zones V1 (en %) : [4,17 ; 25,00 ; 41,67 ; 54,17 ; 91,67].
Zones V2 (en %) : [4,17 ; 25,00 ; 41,67 ; 58,33 ; 100,00].
Nul n°10 : T_0 = 2,2565 exactement (le repère lui-même, sur du bruit
permuté). Nul n°18 : T_0 = 2,1174 (valeur du flux susceptibility dans
le lot v3.5.4, là aussi sur du bruit permuté).

## Ce que le test corrige dans l'avis du 30 octobre

- L'avis disait : « E_thermal = T déguisé ». C'était trop fort. Ce qui
  est vérifié dans le code, c'est la formule (E_thermal = T/4 ×
  (1−M+0,2), calculée à partir de la colonne Temperature) — pas la
  nature du seuil. Le test tranche pour T_0 : le seuil est piloté par
  le facteur (1−M), qui s'effondre à la transition, pas par T seul.
  Correction enregistrée : un flux construit à partir de T n'est pas
  automatiquement un artefact de T ; l'attribution se mesure (V3/V4),
  elle ne se décrète pas.
- Un artefact est une information : les nuls qui « trouvent » un T_0
  informent sur la cascade (elle retourne toujours un T_0, même sur du
  bruit), et les zones ordonnées sur 19/20 nuls informent sur sa
  construction (les règles pré/post ordonnent les zones par
  construction, sauf égalité comme en V1b). Ces informations-là
  servent : elles disent ce que cette loupe ne peut pas prouver seule.

## Limites du test (dites, pas cachées)

- Résolution : 24 points seulement, T_0 ne peut tomber que sur un
  point de grille (±0,0696 au mieux). Lissage sigma = 3,0 sur 24 points
  : très lourd, F1 large, T_0 peu précis par construction.
- La cascade n'a été testée ici que sur l'aimantation et E_thermal,
  pas sur les 5 autres flux du banc, ni sur la prédiction L1–L7, ni
  sur le discriminateur bruit-information, ni sur la saliency.
- Les preuves et dossiers sur le PC de Zackary n'ont pas été testés
  (inaccessibles depuis cette VM) : ce test valide la loupe cascade
  sur le banc disponible ici, rien de plus.

## Fichiers

- `PROTOCOLE.md` (gelé avant runs), `harness_cascade.py`,
  `resultats_cascade.json`, `resultats_cascade.csv`,
  `sources/` (3 fichiers HP, SHA vérifiés, originaux intacts dans
  `workspace/user/files/`).
- Sorties complètes par run dans `resultats_cascade.json`.
