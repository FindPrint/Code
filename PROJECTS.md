# Projects / Projets — FindPrint/Code

One folder per project/post, most recent first. This repository is the
trace, memory and proof archive for work done with Muse (see
`mushroom-classification-v34/docs/TRACEABILITY.md` for the systematic rule).

Un dossier par projet/post, les plus récents d'abord. Ce dépôt est
l'archive de trace, mémoire et preuve des travaux faits avec Muse.

## Projects / Projets

- `mushroom-tests-diagnostics/` — 3 diagnostic tests on the mushroom
  lot (encoding / null / correlations), 27 Oct 2026, protocol frozen
  before runs. Test 1: 3/3 encoding-sensitive. Test 2: 3/3 null scores
  beat the real scores. Test 3: dominant fluxes strongly correlated
  (Spearman up to 0.934, Cramér's V up to 0.978). Text archive here:
  protocol, provenance, report, synthesis CSVs, per-run text results,
  scripts, null data + permutation record. PDF (33 pages, 4.8 MB),
  figures and results zip via browser upload / in chat.
- `mushroom-classification-v34/` — Mushroom Classification × pipeline
  Tlog v3.4-H3, lot restarted from zero 26 Oct 2026, COMPLETED
  26 Oct 2026 18:56 EDT (23/23 runs, 22 Monte Carlo thresholds, 1
  measured failure: veil-type, constant column, all thresholds NaN).
  Code FR+EN, protocol FR/EN, data with hashes, verification, scripts,
  full report (RAPPORT.md), synthesis CSVs, per-run text results.
  PDF (106 pages, 15.2 MB, with figures) via browser upload; results
  zip (26 MB, over the 25 MB web limit) via Release.
- `food-costs-2016/` — Food_Costs 2016 × pipeline v3.3-H1, 14 controls,
  completed 26 Oct 2026. Text archive here: protocol, report, synthesis
  CSVs, data (small CSVs/JSON), scripts. PDF (6.8 MB), zip (6.0 MB) and
  figures (PNG, see `food-costs-2016/figures/README.md`) are NOT in this
  text push — they are delivered in chat and kept in the local archive.
  See the figures README for the list and how to add them via GitHub web
  upload if wanted.
- `food-costs-2015/`, `food-costs-2014/`, `food-costs-2013/` — same
  pattern, 14 controls each, completed 26 Oct 2026. Text archive only
  (protocol, report, synthesis CSVs, data, scripts); PDF/zip/PNG listed
  in each `figures/README.md`, delivered in chat, kept locally.

## What is NOT in this text push / Ce qui n'est PAS dans ce push texte

- Binaries: PDF, zip, PNG figures. The GitHub connector snapshot push
  accepts UTF-8 text files only (<16 MB total per push, <2,000 files).
  Binaries are therefore NOT pushed by Muse; they are delivered in chat
  (PDF with figures embedded, plus figures separately at final delivery)
  and kept in the local workspace archive. To add a PNG/PDF to GitHub,
  upload it via the GitHub website into the corresponding `figures/`
  folder, or ask for a Release asset.
- The root `README.md` ("# Code") and `pipeline_autonome_v3_3_harmonic_v1.py`
  already in this repository are left untouched by these pushes.

- `air-quality/` — Air Quality × pipeline v3.3-H1, 10 controls,
  completed 26 Oct 2026. Text archive only (protocol, report, synthesis
  CSVs, data, scripts); PDF/zip/PNG listed in `figures/README.md`,
  delivered in chat, kept locally.
- `breast-cancer/` — Breast Cancer × pipeline v3.3-H1, 32 controls,
  completed 25–26 Oct 2026. Text archive only (protocol, report,
  synthesis CSVs, data, scripts); PDF/zip/PNG listed in
  `figures/README.md`, delivered in chat, kept locally.

- `earthquake-tsunami-v33h1/` — Earthquake/Tsunami × pipeline v3.3-H1,
  13 controls, completed 25 Oct 2026. Key descriptive finding, in the
  report: the Year ~2013 cut describes the file's field-filling history,
  not a seismic regime. Text archive only.
- `earthquake-tsunami-v33fixed/` — same protocol, pipeline v3.3 FIXED
  (classic Monte Carlo, no harmonic guidance), 13 controls, completed
  25 Oct 2026, with informational fluxes kept in a separate CSV.
  Text archive only.

- `multi-tipping/` — Multi-tipping benches (Ashkin-Teller + clock q=6,
  22 Oct 2026) + Controls batch (35 runs, 25 Oct 2026): protocols,
  reports, bench data CSVs, control synthesis, scripts. Text archive
  only; PDFs (3.2 + 5.3 MB), per-run figures and zips listed in
  `figures/README.md`, delivered in chat, kept locally.

## Next backfills (most recent first) / Prochains dépôts (plus récents d'abord)

Older projects (USGS, heart-attack, diabetes, quantum-ai, etc.) on
request, most recent first. — then
Earthquake/Tsunami, Controls batch, Multi-tipping, in that order, on
request / as checkpoints allow. Each backfill follows the same pattern:
protocol + report + synthesis CSVs + data + scripts (text only), with a
figures README listing the PNGs.
