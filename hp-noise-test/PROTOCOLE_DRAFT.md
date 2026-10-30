# PROTOCOLE — BROUILLON (non gelé) — Test du discriminateur bruit-information HP sur le banc Ising

**Statut : BROUILLON du 30 octobre 2026, préparé après le test cascade du même jour.
Il ne devient un protocole gelé que si Zackary le valide (avec ou sans amendements).
AUCUN run lancé sous ce brouillon. Aucune modification du code reçu.**

*DRAFT, 30 Oct. 2026 — not frozen until Zackary approves it. No run launched under it.*

## 1. Question

La fonction `analyze_noise_information_content` de v3.7.0-HP-v3
(consolidée dans `Tlog_v3_7_0_HP_uni_v1.py`, SHA `45dadb94…`)
distingue-t-elle, loupe par loupe, les fluctuations résiduelles
réelles de l'aimantation Ising de leurs nuls — ou retourne-t-elle
« informatif » aussi sur du bruit ?

*Does the v3.7.0 noise-information discriminator separate real Ising
magnetization residuals from their nulls, component by component,
or does it also call noise "informative"?*

## 2. Fonction sous test (lue, jamais modifiée)

- `analyze_noise_information_content(signal_series, fs=1000.0)`,
  paramètres PAR DÉFAUT. `fs` n'est pas un taux d'échantillonnage
  physique des snapshots : il est laissé à 1000,0 et noté comme
  arbitraire pour ce test.
- Règle de verdict du code : `is_informative` = vrai si
  test de Jarque-Bera p < 0,01 (non-gaussianité) OU exposant de
  Hurst (R/S) hors de [0,40 ; 0,60]. Sorties rapportées une par une :
  `is_informative`, `hurst_exponent`, `kurtosis`, `skewness`,
  `jarque_bera_p_value`, `fractal_length_ratio`, `spectral_entropy`.
- Seuil de longueur du code : < 30 points → `series_too_short`,
  `is_informative` faux. Toutes les séries ci-dessous dépassent 30.

## 3. Données (banc validé, pas de nouvelles données)

- `workspace/ising-v354/data/ising_classic_v354.csv` — 960 lignes,
  6 flux, SHA-256
  `9027dfd53767845049b07c458c8713104f7288d8d6ac7b7c50a0ae972627066d`.
- `workspace/ising-v354/data/ising_classic_v354_temperature.csv` —
  960 lignes, SHA-256
  `4863b1de84e358c77faeae2a1e227474b0115e38805bf499df24d3efbc84c5e4`.
- Jointure par ordre des lignes, vérifiée le 30 oct. 2026 : 24 blocs
  de 40 snapshots, T croissant de 1,7 à 3,3. Nature : snapshots
  SIMULÉS, pas mesurés.
- Repère descriptif (lot v3.5.4, PAS règle succès/échec) :
  T = 2,2565, qui est lui-même un point de grille (bloc n° 9).

## 4. Séries (construites par le harnais, hors pipeline)

Canal résiduel : pour chaque bloc de T, aimantation snapshot moins
la moyenne de son bloc. Cela retire la tendance en T ; sans cette
soustraction, la chute de l'aimantation à la transition rendrait
le verdict « informatif » trivial.

- R_all : résidus des 960 snapshots, ordre T croissant.
- R_pre : résidus des blocs T < 2,2565 (320 points).
- R_post : résidus des blocs T > 2,2565 (600 points).
  Le bloc repère (40 points) est exclu de R_pre/R_post pour ne pas
  mélanger la frontière, mais inclus dans R_all.
- Nuls permutation : 20 permutations de R_all, p fixe, graine 1234
  (permutations 0–19, même graine que le test cascade pour
  comparabilité). Le nul conserve les marginales et brise seulement
  l'ordre.
- Nuls gaussiens : 20 tirages gaussiens indépendants, même longueur
  (960), même moyenne et même écart-type que R_all, graine 4321.
- Témoin : la fonction appliquée à un bruit blanc gaussien pur
  (les 20 nuls gaussiens servent aussi de témoin).

## 5. Point de méthode écrit AVANT les runs (à ne pas découvrir après)

Une permutation conserve EXACTEMENT la distribution : kurtosis,
skewness et p de Jarque-Bera sont identiques entre R_all et chacun
de ses 20 nuls permutés. Donc :

- Si R_all est « informatif » par le seul critère Jarque-Bera,
  les 20 nuls permutés le seront aussi, par construction.
- Le verdict booléen seul ne peut donc pas séparer réel et nul
  permuté. Le jugement se fait COMPOSANTE PAR COMPOSANTE :
  Hurst et entropie spectrale (qui, eux, dépendent de l'ordre)
  pour les nuls permutés ; l'ensemble des composantes pour les
  nuls gaussiens.
- Un verdict « informatif » sur les nuls gaussiens serait une
  information sur la fonction (son seuil Hurst/JB), pas sur le
  système — à rapporter comme telle, comme pour la cascade.

## 6. Jugement (écrit avant les runs)

- (a) R_all, R_pre, R_post : chaque composante rapportée, pas
  seulement le booléen.
- (b) Nuls permutés : distribution de Hurst et d'entropie
  spectrale ; le réel se situe-t-il hors de cette distribution ?
- (c) Nuls gaussiens : taux de « informatif » sur 20 ; si ce taux
  est élevé, le discriminateur ne sépare pas le bruit blanc pur.
- (d) Pré vs post : les composantes changent-elles de part et
  d'autre du repère, réel contre nuls ? Aucune conclusion tirée
  d'une seule série.
- (e) Tout retour `series_too_short` ou toute exception est
  rapporté comme tel, jamais comme un verdict.

## 7. Sorties (tout gardé, rien dans /tmp)

- `harness_noise.py` — harnais (lecture seule des sources et données).
- `resultats_noise.json` — sorties complètes par série et par nul.
- `resultats_noise.csv` — synthèse une ligne par série/nul.
- `RAPPORT.md` — verdict réel-vs-nul, composante par composante.
- Publication, si Zackary le décide après le rapport : dépôt privé
  FindPrint/Code, dossier `hp-noise-test/`, fichiers texte seulement.

## 8. Ce que ce test ne fait PAS

- Il ne teste pas la prédiction L1–L7, ni la saliency : chacun aura
  son protocole propre.
- Il ne teste pas le diagnostic de bruit v3.5.4 en 4 étapes
  (`compute_noise_diagnostic`) : c'est une autre loupe, à tester
  séparément si Zackary le demande.
- Il ne valide pas les dossiers PC de Zackary (inaccessibles depuis
  cette VM).
- Il n'utilise le fichier unique consolidé que comme copie de la
  fonction testée ; l'équivalence cascade + discriminateur a déjà
  été vérifiée le 30 oct. 2026 (`verification_uni.json`).
