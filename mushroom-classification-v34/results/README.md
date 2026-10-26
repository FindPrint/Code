# Results / Résultats

Status at completion (26 Oct 2026, 18:56 EDT): v3.4 lot COMPLETE,
23/23 runs with a `run_summary.json` (22 Monte Carlo thresholds, 1
measured failure).

Per-control folders (`results/ctrl_<column>/`) contain, when the run
produced them: `run_summary.json`, `scan_curve.csv`,
`per_flux_thresholds.csv`, `transition_F1F2.csv` (F1/F2 pre+post),
`text_report.txt`, `landscape_peaks.csv`. Figures
(`threshold_scan.png`, `noise_diagnostic.png`) and the large
`pipeline_results.json` files are kept in the local lot folder and in
the final PDF/zip (snapshot pushes accept text files only, not
binaries or very large files); they are not in this text tree.

Synthesis files at the project root: `synthese_runs.csv`,
`tous_seuils_par_flux.csv`, `tous_F1F2.csv`, `plateaux_controles.csv`,
`qs_par_run.csv`, plus `RAPPORT.md` (full report, in French) and
`Mushroom_Classification_v34_Resultats_complets.pdf` (106 pages, with
figures) — the PDF and the results zip are uploaded via the browser;
the zip (26 MB, over the 25 MB web-upload limit) goes to a Release.

Measured failure (pre-registered): `veil-type` is a constant column
(`p` on every row) — MC, default, raw and rigid thresholds all NaN,
score 0.0, stability UNKNOWN, 2 recorded warnings. Its 52.5 %
noise-diagnostic value is an emergency fallback, explicitly NOT a
detected threshold. It is never read as a detector.

Key stability finding (reported as measured): only 9/22 runs have
|MC − bootstrap mean| within 1 bootstrap std; 7 of the 10 VERY STABLE
runs do not (odor gap 97.69 pts, gill-attachment 46.06,
veil-color 41.75). The label measures bootstrap tightness, not
agreement with the MC.

État à l'achèvement (26 oct. 2026, 18h56 HAE) : lot v3.4 TERMINÉ,
23/23 runs avec `run_summary.json` (22 seuils Monte Carlo, 1 échec
mesuré). Voir `RAPPORT.md` pour le rapport complet.
