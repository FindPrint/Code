# Banc « multi-tipping » — simulations type Ising à PLUSIEURS points critiques

Question de Zackary (22 oct. 2026) : une simulation comme Ising, mais avec
plusieurs points de bascule dans UN seul balayage, pour y passer le pipeline
(v3.3 uploadé le même jour) — au lieu du Tc unique d'Ising (2,269).

Protocole commun (même recette que les bancs Ising) :
- le paramètre de contrôle externe (T) est gardé dans un fichier séparé,
  repère de vérification seulement, jamais donné au pipeline ;
- contrôle du pipeline = `energy` (monotone en T) ;
- verdict pré-enregistré suggéré : le seuil rendu tombe-t-il près d'UN des
  seuils attendus ? Et le paysage de scan (courbe complète, pas que l'optimum)
  montre-t-il le SECOND seuil ? Le pipeline v3.3 ne cherche qu'un seuil :
  sur ces bancs, « choisir » est déjà un résultat — lequel des deux il choisit,
  et si l'autre reste visible dans le paysage.

## 1. Ashkin-Teller (J=1, U=2) — PRÊT, signal vérifié le 22 oct. 2026
Deux Ising couplés par une interaction à 4 spins. Quand U > J, la transition
unique se fend en deux transitions nettes de type Ising (prouvé : Pfister ;
Duminil-Copin–Raoufi–Tassion) :
- phase de Baxter (s, τ et sτ ordonnés) → **T_spin** : s et τ se désordonnent,
  le produit sτ reste ordonné (phase partielle <sτ>) → **T_prod** : sτ se
  désordonne → paramagnétique.
- Mesuré sur le jeu généré (L=28, 1224 lignes, T de 2,0 à 7,0 par pas de 0,10) :
  chute de magnetization_s entre T≈4,6–4,9 ; chute de magnetization_prod
  entre T≈5,2–5,6. Séparation ≈ 0,7 en T.
- Positions attendues en fraction de lignes : **seuil 1 ≈ 55–57 %**,
  **seuil 2 ≈ 66–69 %**.
- Fichiers : `gen_ashkin_teller.py`, `at_fluxes.csv`, `at_temperature.csv`,
  `at_dataset.csv`. Génération : ~12 s.

## 2. Modèle d'horloge q=6 (clock) — PRÊT, test dur (transitions molles)
Cousin direct d'Ising (q=2 → q=6 états). Un balayage en T traverse DEUX
transitions BKT : **T1 ≈ 0,70** (ferro → phase critique) et **T2 ≈ 0,88**
(phase critique → paramagnétique) ; littérature : T1 = 0,70 et T2 = 0,88
(CTMRG), fourchettes MC 0,68–0,75 / 0,88–0,92.
- Positions attendues (grille 0,40–1,20) : **≈ 37 %** et **≈ 60 %** des lignes.
- Honnêteté : transitions d'ordre infini (BKT) — pas de chute nette de
  l'aimantation ; signature surtout dans vortex_density (décollement des
  vortex vers T≈0,9–1,0 sur le jeu généré, L=24) et les pentes des flux.
  C'est le test « paysage » par excellence, pas un test de précision.
- Fichiers : `gen_clock6.py`, `clock6_fluxes.csv`, `clock6_temperature.csv`,
  `clock6_dataset.csv` (984 lignes). Génération : ~6 s.

## 3. ANNNI — générateur à écrire si choisi
Ising à interactions concurrentes (proches voisins ferro + seconds voisins
antiferro le long d'un axe). Diagramme riche : ferro → phases modulées
(séquence infinie de phases commensurables près du point multiphase,
κ = -J2/J1 = 1/2 à T=0) → paramagnétique ; en 2D, une phase critique
flottante entre ferro et para, séparée par deux transitions BKT.
Vérité terrain plus floue, simulation plus délicate (phases modulées,
effets de taille) — à réserver en deuxième vague.

## 4. Blume-Capel / Blume-Emery-Griffiths — générateur à écrire si choisi
Ising spin-1 (s = -1, 0, +1) avec champ cristallin D. Point TRICRITIQUE où
les lignes de transition du 1er et du 2e ordre se rejoignent ; versions
avec réentrance : un balayage en T traverse DEUX fois la frontière
(ordonné → désordonné → ordonné). La réentrance dépend du réseau et des
paramètres — à calibrer avant de geler le protocole.

## 5. Hors réseau : carte logistique — cascade INFINIE, seuils exacts
x -> r·x·(1-x). Doublements de période aux seuils connus au chiffre près :
r = 3,00000 ; 3,44949 ; 3,54409 ; 3,56441 ; 3,56876 … accumulation
r∞ ≈ 3,56995 (chaos). C'est la version littérale de « des seuils avant et
après, à l'infini ». Flux possibles : variance, autocorrélation lag-1,
entropie, amplitude, exposant de Lyapunov estimé. Pas « comme Ising »,
mais vérité terrain parfaite et coût ~1 s.
