# Protocole vague 2 — gelé le 22 oct. 2026 (avant tout run)

Objectif : transformer le résultat AT (preuve de potentiel) en résultat
qui survit aux trois objections : (1) un seul jeu de données, une seule
graine ; (2) fenêtres attendues mesurées sur le même jeu que celui testé ;
(3) pas de contrôle nul sur ce format.

## A. Réplication AT indépendante
- Générateur inchangé (J=1, U=2, L=28), **graines nouvelles : 7 et 123** ;
  plus une taille différente : **L=36, graine 42**.
- Fenêtres de hit = CELLES DE LA VAGUE 1, inchangées :
  seuil 1 (spin) **50–60 %**, seuil 2 (produit) **62–73 %**.
- Pipeline v3.3, mode stable, contrôle energy, aveugle, même pilote.
- Critère : seuil global dans la fenêtre 1 ET seuil propre de
  magnetization_prod dans la fenêtre 2, sur au moins 2 des 3 jeux.

## B. Contrôle nul AT
- `at_fluxes.csv` (vague 1) avec les **lignes mélangées** (graine 99) :
  mêmes distributions, ordre détruit, aucune transition réelle.
- Même run complet. Attendu si l'instrument est sain : stabilité dégradée
  (pas de VERY STABLE), scores plus bas, seuils par flux dispersés
  sans regroupement dans les fenêtres 50–60 / 62–73.

## C. Horloge q=6 — vérité terrain INDÉPENDANTE (littérature)
- Valeurs publiées, pas mesurées sur mon générateur :
  **T1 = 0,70 et T2 = 0,88** (CTMRG ; fourchettes MC 0,68–0,75 / 0,88–0,92).
- Jeu déjà généré (L=24, grille 0,40–1,20, 984 lignes, contrôle energy).
- Fenêtres (fraction de lignes, élargies car transitions BKT molles) :
  seuil 1 **30–46 %**, seuil 2 **52–68 %**.
- Critère adapté, gelé : succès si le seuil global OU au moins deux seuils
  propres par flux tombent dans les fenêtres, ou si le paysage montre une
  épaule nette dans la fenêtre 2. Un échec ici ne contredit pas la vague 1 :
  il borne l'instrument sur les transitions d'ordre infini.

Coût estimé : ~3,5 min de pipeline par run, 5 runs ≈ 20 min en séquentiel.
