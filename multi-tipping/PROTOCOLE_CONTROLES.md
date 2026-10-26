# Protocole — Tous les flux en contrôle, à tour de rôle (GELÉ le 25 oct. 2026 ~19 h 55 HAE)

Confirmation utilisateur (25 oct. 2026, 19 h 49 HAE) : pipeline harmonique v1,
périmètre COMPLET (35 runs).

Objectif : relancer le protocole de la conversation multi-tipping (vague 1, vague 2,
porte D) en passant CHAQUE flux en colonne de contrôle à tour de rôle, le contrôle
étant toujours EXCLU des flux analysés (règle porte D généralisée).

## Pipeline et réglages (identiques à la conversation, sauf le fichier si confirmé)
- Pipeline : pipeline_autonome_v3_3_harmonic_v1.py (uploadé le 25 oct. 2026),
  guidage harmonique à son défaut (HARMONIC_PROB = 0,45 dans le module).
- Mode stable, test cohen_d, w_size 80, graine 42, aveugle (aucune température
  en entrée), bootstrap activé (mode stable).

## Jeux et contrôles
- AT principal (at_fluxes.csv, L=28, graine 42) : 6 contrôles
  (magnetization_s, magnetization_tau, magnetization_prod, energy, flip_rate,
  local_variance).
- AT réplications (s7, s123, L=36) : 6 contrôles × 3 jeux = 18 runs.
- Horloge q=6 (clock6_fluxes.csv) : 5 contrôles
  (magnetization, energy, flip_rate, vortex_density, local_variance).
- Nul B2 AT (at_null2_fluxes.csv, flux décorrélés) : 6 contrôles.
- Total protocole complet : 35 runs. Variante réduite : AT principal + horloge = 11 runs.
- Le nul B1 (lignes mélangées) n'est PAS rejoué : invalide par construction (vague 2).

## Mapping et monotonie
- Axe de progression = rang du contrôle choisi (pas toujours energy).
- T mappée = moyenne des températures des lignes autour de la frontière de rang
  du contrôle (bande ±1,5 %), à partir du fichier température du jeu (nul : aucune).
- Diagnostic joint : corrélation de Spearman contrôle vs T par jeu (un contrôle
  non monotone en T est attendu comme peu informatif, pas comme un échec du pipeline).

## Critères gelés (jugés en température mappée, pas en %)
Précision pré-lot (notée avant tout run horloge du lot, après le pilote AT/energy) :
fenêtres T horloge = T1 [0,62 ; 0,80], T2 [0,82 ; 0,98] — équivalent en T des
fenêtres % de la vague 2 (30–46 % / 52–68 % en rang d'energy).
- AT : T1 attendu [4,6 ; 4,9] (spin), T2 attendu [5,2 ; 5,6] (produit).
  Attendus par contrôle : energy → global vers T1 (comme vagues 1–2) ;
  m_s / m_tau → global vers T1 ; m_prod / flip_rate → global vers T2 ;
  local_variance → aucune attente (diagnostic).
  Par flux (dans chaque run) : m_s / m_tau doivent pointer vers T1,
  m_prod / flip_rate vers T2, quel que soit le contrôle.
- Horloge : T1 = 0,70, T2 = 0,88 (littérature, fenêtres tolérantes vu BKT et L=24).
- Nul B2 : scores par flux effondrés, seuils dispersés, stabilité dégradée
  (pas de VERY STABLE) — configuration sans contrôle-as-flux.
- Échec pré-enregistré : contrôle avec moins de 80 valeurs valides = échec mesuré
  (aucun ici, données complètes) ; run en erreur = échec mesuré, le lot continue.

## Sorties par run
run_summary.json, verdict.json (seuils global + par flux, T mappées, stabilité,
zones du paysage), per_flux_thresholds.csv, scan_curve.csv, threshold_scan.png,
noise_diagnostic.png, text_report.txt, pipeline_results.json.
Lot résumable : un run déjà terminé et vérifié n'est pas relancé.

## Livrables
Rapport complet + PDF complet (même format que le PDF du 25 oct. 2026) :
démarche, données, résultats par contrôle et par jeu, figures, annexes.
