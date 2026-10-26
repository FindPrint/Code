# Porte D — Ashkin-Teller et nul B2 SANS energy-as-flux (config standard 17 oct.)

Gelé le 2026-10-22 ~14h15 HAE, avant tout run. Motif : le verdict vague 2
(porte B2) a établi que, dans la configuration « contrôle = energy ET flux »,
le seuil global du nul sort VERY STABLE (58,30 %) parce qu'energy, triée par
son propre rang, se sépare trivialement d'elle-même (score Q4 ~3,28 identique
réel/nul, seul inchangé). La configuration standard du banc Ising (17 oct.,
à la demande de l'utilisateur, vérifiée) est : contrôle = energy, flux = les
autres (energy EXCLUE des flux analysés). La porte D aligne le banc AT sur
cette configuration et rejoue les deux cas critiques.

## Runs (pipeline v3.3 tel quel, mode stable, graine 42, aveugle, w_size 80)
- D1 : `at_fluxes.csv` (AT réel, L=28, graine 42) → `vague2/noE_real/`
- D2 : `vague2/data/at_null2_fluxes.csv` (nul B2 : chaque flux permuté
  indépendamment, energy fixe comme contrôle) → `vague2/noE_null2/`
- Différence avec vagues 1-2 : `flux_mapping` exclut la colonne de contrôle
  (runner `run_v33_generic_noEflux.py`) ; l'analyse par flux
  (`analyse_generic_noE.py`) exclut aussi energy des scans individuels.

## Critères gelés
- D1-réel : le seuil global MC doit retomber dans la fenêtre 1 (50–60 %) ;
  les scans par flux (sans energy) doivent encore séparer seuil 1
  (m_s/m_tau → 50–60 %) et seuil 2 (m_prod/flip_rate → 62–73 %).
- D2-nul : le seuil global ne doit PLUS être VERY STABLE (le critère B
  d'origine : pas de VERY STABLE sur nul) ; les scores par flux doivent
  rester effondrés et dispersés.
- Interprétation fixée d'avance : si D2 sort encore VERY STABLE sans
  energy-as-flux, la réserve du verdict vague 2 devient une propriété de
  l'instrument, pas un artefact de configuration — et elle s'applique
  alors aussi au banc Ising standard. Si D2 perd sa stabilité, la
  configuration standard (17 oct.) est validée comme le réglage sain,
  et le verdict vague 2 se lit : discrimination par flux OK dans les
  deux configurations, seuil global fiable uniquement hors energy-as-flux.

Références : PROTOCOLE_VAGUE2.md, RAPPORT_VAGUE2.md,
`workspace/multi-tipping/vague2/` (runs), memory 2026-10-17 (config standard).
