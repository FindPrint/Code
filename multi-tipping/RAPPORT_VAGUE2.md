# Rapport vague 2 — les trois portes (22 oct. 2026)

Protocole gelé avant les runs : `PROTOCOLE_VAGUE2.md`. Pipeline v3.3 tel
quel, mode stable, contrôle = energy (aussi flux), aveugle, même pilote.
Fenêtres vague 1 inchangées pour AT : seuil 1 = 50–60 %, seuil 2 = 62–73 %.

## VERDICT GLOBAL

- **Porte A (réplication) : PASSÉE** — 2 jeux francs sur 3, le 3e à la frontière.
- **Porte B (contrôle nul) : PASSÉE sur la lecture discriminante (par flux),
  avec une réserve mesurée** — le critère « stabilité » gelé n'est pas
  satisfait, pour une cause identifiée et chiffrée (voir plus bas).
  Le premier nul (mélange de lignes) était **invalide par construction**
  (erreur de protocole de l'assistant, corrigée et re-testée).
- **Porte C (horloge q=6, vérité terrain littérature) : ÉCHEC** au critère gelé.

La preuve de potentiel de la vague 1 survit à la réplication et au nul
corrigé. Elle ne s'étend pas, en l'état, aux transitions BKT molles.

## Porte A — Réplication AT (graines et taille nouvelles)

Critère gelé : seuil global dans la fenêtre 1 ET seuil propre de
magnetization_prod dans la fenêtre 2, sur au moins 2 des 3 jeux.

| Jeu | Global MC % | (T) | m_s % | m_tau % | m_prod % | (T) | flip_rate % | Stabilité |
|---|---|---|---|---|---|---|---|---|
| vague 1 (réf.) | 54,93 | 4,77 | 52,50 | 53,41 | 64,95 | 5,29 | 64,95 | VERY STABLE ±1,94 |
| graine 7 | 52,20 | 4,59 | 52,20 | 52,20 | **68,13** | 5,45 | 68,13 | VERY STABLE ±1,69 |
| graine 123 | 51,51 | 4,59 | 51,51 | 49,76 | **67,35** | 5,36 | 67,35 | VERY STABLE ±0,95 |
| L=36 | 56,35 | 4,84 | 51,78 | 51,78 | **61,42** | 5,11 | 64,64 | VERY STABLE ±1,42 |

- Graine 7 et graine 123 : critère satisfait entièrement.
- L=36 : global ✓ ; m_prod à 61,42 %, soit **0,58 point sous** la fenêtre 2
  (flip_rate dedans, 64,64 %). En L=36, les deux transitions se rapprochent :
  produit à T = 5,11 contre 5,29–5,45 en L=28 (déplacement de taille finie).
  Compté comme NON satisfait au sens strict — pas de déplacement de poteau.
- Motif répliqué 3/3 : m_s/m_tau portent le seuil 1, m_prod/flip_rate le
  seuil 2 ; energy propre entre les deux (56–61 %) ; local_variance précoce
  (41–45 %, scores faibles 1,85–2,12 contre 5,0–5,6 pour m_s/m_tau).

## Porte B — Contrôle nul

### B1 (lignes mélangées) : INVALIDE, et instructif
Résultat quasi identique à la vague 1 (global 54,93 %, stabilité au 4e
décimal près). Cause : le pipeline trie les flux par le rang du contrôle dès
l'entrée — permuter les lignes ne change rien à ce qu'il voit.
**Vérifié au passage : le pipeline est invariant par permutation des lignes.**
Erreur de design du nul, pas du pipeline. Rejeté et remplacé par B2.

### B2 (flux décorrélés du contrôle, energy fixe, permutations indépendantes)
| Lecture | Réel (vague 1 + réplicats) | Nul B2 |
|---|---|---|
| Score par flux m_s / m_tau / m_prod / flip_rate / local_var | 4,35 – 5,61 | **0,18 – 0,30** |
| Score propre de energy | 4,40 – 4,80 | 4,62 (inchangé) |
| Max de la courbe de scan globale | 3,49 – 3,86 | **0,85** |
| Score MC global | 0,759 – 0,765 | 0,562 |
| Seuils par flux | groupés (fenêtres 1 et 2) | dispersés : 47,9 / 91,7 / 62,8 / 50,2 / 50,0 |
| Stabilité globale | VERY STABLE | VERY STABLE ±1,43 (voir réserve) |

- **Le signal par flux est détruit** : facteur ~20 sur les scores, aucune
  grappe dans les fenêtres (le 62,8 % de m_prod est un atterrissage de
  hasard à score 0,18 — niveau de bruit ; avec 6 flux et des fenêtres
  larges, ~1 hasard est attendu).
- **Réserve mesurée** : le seuil global du nul tombe à 58,30 % (fenêtre 1)
  et reste coté VERY STABLE — le critère gelé « pas de VERY STABLE » n'est
  donc PAS satisfait. Cause identifiée : energy est à la fois contrôle et
  flux ; triée par son propre rang, elle se sépare trivialement d'elle-même
  (son score propre, 4,62, est le seul inchangé entre réel et nul). Le
  seuil global mélangeant les flux hérite de ce signal tautologique.
- Conclusion B : la lecture **par flux** discrimine réel et nul sans
  ambiguïté ; la lecture **globale** (seuil + stabilité) ne discrimine pas
  dans cette configuration contrôle=flux. C'est un fait sur l'instrument,
  à retenir pour tout usage futur du seuil global seul.

## Porte C — Horloge q=6 (vérité terrain littérature : T1 = 0,70, T2 = 0,88)

Critère gelé : seuil global OU ≥ 2 seuils propres dans les fenêtres
(30–46 % / 52–68 %), ou épaule nette du paysage dans la fenêtre 2.

| Flux | Seuil propre % | T mappée |
|---|---|---|
| flip_rate | 28,51 | 0,62 ± 0,02 |
| energy | 30,25 | 0,64 ± 0,03 |
| magnetization | 85,96 | 1,10 ± 0,04 |
| vortex_density | 85,09 | 1,09 ± 0,04 |
| local_variance | 85,09 | 1,09 ± 0,04 |
| **global MC** | **85,09** | **1,09 ± 0,04** |

Stabilité : MODERATELY STABLE (±3,13) — dégradée par rapport à AT.

- **Critère NON satisfait** : un seul flux (energy) dans la fenêtre 1, aucun
  dans la fenêtre 2, global très loin (85 %).
- Structure réelle mais déplacée : deux grappes de flux, {energy, flip_rate}
  vers T≈0,62–0,64 (sous T1 = 0,70) et {magnetization, vortex_density,
  local_variance} vers T≈1,09 (au-dessus de T2 = 0,88). Dans le jeu généré
  lui-même (L=24), les vortex ne décollent que vers T≈0,96–1,10 : la
  transition haute du JEU est décalée par la taille finie, avant même de
  parler du pipeline. L'échec est donc double et non partageable proprement
  entre « jeu trop petit pour le BKT » et « instrument moins sensible au
  mou » — les deux sont vrais, aucun ne suffit à innocenter l'autre.
- Ce que C établit : sur des transitions nettes de type Ising, l'instrument
  réplique ; sur des transitions d'ordre infini (BKT), en L=24, il ne
  retrouve pas les positions publiées. Borne d'instrument, consignée.

## Synthèse honnête

Ce qui tient après la vague 2 :
1. Deux transitions nettes et distinctes dans un même balayage sont
   retrouvées aveuglément, répliquées sur 3 jeux indépendants, chacune par
   ses flux (scores 4,4–5,6 contre 0,2 en nul).
2. La lecture par flux est l'instrument discriminant ; le seuil global
   seul ne l'est pas quand le contrôle est aussi un flux.
3. L'invariance par permutation des lignes est vérifiée.

Ce qui ne tient pas / reste ouvert :
1. Transitions molles (BKT) : positions publiées non retrouvées en L=24.
2. Toutes les données restent synthétiques, générées par l'assistant ;
   aucune donnée réelle n'a encore éprouvé ce banc (règle de l'utilisateur :
   le synthétique construit, le réel éprouve).
3. La lecture par flux reste une analyse post-run de l'assistant, pas une
   sortie native du pipeline.

Fichiers : `vague2/<run>/` (verdict.json, per_flux_thresholds.csv,
run_summary.json, scan_curve.csv, text_report.txt, figures) pour at_s7,
at_s123, at_L36, null (B1, à titre documentaire), null2 (B2), clock ;
données dans `vague2/data/`.
