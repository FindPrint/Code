# Méthodologie — comment le pipeline lit un seuil (résumé)

Résumé pour les pairs, pas un remplacement du code. Toutes les
définitions ci-dessous sont implémentées dans `pipeline/` ; le
protocole gelé est dans `PROTOCOLE.md` / `PROTOCOL.md`.

## 1. Contrôle et flux

- Une colonne est choisie comme **contrôle**. Elle définit l'axe de
  progression : le rang de chaque ligne dans le contrôle, en
  pourcentage (0–100 %).
- Chaque autre colonne numérique est un **flux**. Le contrôle n'est
  jamais parmi les flux analysés (règle Porte D).
- Les flux sont z-scorés avant le scan (NaN remplacés par la moyenne
  du flux). Pour le scan brut, les valeurs originales sont utilisées,
  NaN conservés.

## 2. Scan de seuil

- L'axe de contrôle est découpé en fenêtres glissantes (taille
  `w_size`). Pour chaque seuil candidat (un pourcentage sur l'axe de
  progression), les fenêtres sont séparées en groupes bas/haut selon
  leur progression moyenne.
- Pour chaque flux, les groupes bas/haut sont comparés par Cohen d
  (ou Cliff delta si configuré ; ce lot utilise Cohen d). Les groupes
  de plus de 1 000 valeurs sont sous-échantillonnés à exactement
  1 000 avec une graine fixe (0) — c'est pourquoi le scan rapide peut
  reproduire exactement le scan legacy sans matérialiser les groupes.
- Le score d'un candidat est la moyenne des |Cohen d| sur les flux.
  Le candidat de score maximal est le seuil de scan pour cette
  configuration.

## 3. Monte Carlo guidé harmonique

- 50 itérations échantillonnent (taille de fenêtre, nombre de
  candidats, taille minimale de groupe). Avec probabilité
  HARMONIC_PROB (0,45), l'échantillon est guidé par des constantes
  mathématiques (phi, pi, e, racine de 2, racine de 3) ; sinon il est
  uniforme. Chaque configuration est notée par un composite
  (séparation, stabilité, robustesse, netteté) ; la meilleure est gardée.
- Un scan témoin rigide avec la grille historique à 1001 candidats,
  même fenêtre, est aussi calculé, pour mesurer l'effet de la grille —
  ce n'est pas le seuil retenu.
- Si aucune configuration échantillonnée n'est valide, le seuil par
  défaut est utilisé et le repli est JOURNALISÉ (voir README point 2).
  Idem, séparément, pour le Monte Carlo sur données brutes.

## 4. Stabilité, questions, bruit

- **Stabilité :** le scan est répété pour plusieurs tailles de
  fenêtre ; l'étiquette (ex. UNSTABLE) vient de la dispersion, et doit
  toujours être vérifiée contre la moyenne bootstrap — une étiquette
  UNSTABLE avec une moyenne bootstrap presque égale au seuil Monte
  Carlo est un avertissement de dispersion, pas un désaccord.
- **Questions Q1–Q5 :** signatures de complexité par flux (Higuchi,
  DFA, Katz, Hurst, Sample Entropy et estimateurs liés, calculés sur
  les fenêtres), résumées par question ; voir le code et le
  `numerical_results.csv` de chaque run.
- **Diagnostic bruit :** vérifie si le signal le plus fort se comporte
  comme un proxy de variance colorée (CSD) plutôt que comme un bruit blanc.

## 5. F1/F2 avant et après seuil (v3.4)

- Pour chaque estimateur de complexité et chaque flux (plus `Tous`,
  la moyenne sur les flux), le pipeline ajuste un polynôme de degré 2
  de l'estimateur en fonction de Progress centrée, séparément :
  - **après** seuil : Progress >= seuil (si < 3 points, élargi à
    >= seuil − 10, signalé) ;
  - **avant** seuil : Progress < seuil (si < 3 points, élargi à
    < seuil + 10, signalé).
- F1 = coefficient linéaire (pente au centre du segment), F2 = 2 ×
  coefficient quadratique. Signe/ordre suivent la même règle à 1e-6
  des deux côtés. Les écarts (post − pré) et `sign_change` sont
  enregistrés quand les deux côtés réussissent ; sinon ils valent
  None, jamais 0 par défaut.
- Si un segment a < 3 points même après élargissement, son statut est
  `insufficient_data` avec une raison explicite.

## 6. Lecture des résultats — limites

- Contrôles discrets / nominaux : lire les seuils comme des plateaux
  de rang, pas comme des valeurs de coupure physiques. Un pourcentage
  d'apparence précise surestime ce qu'une coupure sépare pour des
  contrôles discrets.
- Le remplissage des champs décide de ce qu'un seuil peut signifier :
  un signal fort peut décrire comment un fichier a été rempli, pas un
  régime physique — toujours vérifier le manquant et la discrétité
  avant d'interpréter une coupure.
- Aucune décision comestible/vénéneux, aucune affirmation causale,
  aucune affirmation temporelle à partir de ce dataset.
