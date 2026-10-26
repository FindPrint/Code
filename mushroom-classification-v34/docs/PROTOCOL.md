# Frozen protocol — Mushroom Classification × pipeline v3.4-H3
# Lot restarted from zero, 26 October 2026, at the author's request
# (English version — the French reference is PROTOCOLE.md in this folder)

## Request
Download all CSVs from Kaggle dataset `uciml/mushroom-classification`,
merge them into a single CSV, run the pipeline on every column (flux)
as control column, one after another, and deliver all results, data
sources, methodology and information in one PDF including figures.
Pipeline: the NEW pipeline `Tlog_v3_4_harmonic_v3.py`. Lot restarted
from zero: no result from the v3.3 lot is reused in this lot.

## Data source (verified, identical to the 26 Oct 2026 download)
- Kaggle: https://www.kaggle.com/datasets/uciml/mushroom-classification
- `mushroom-classification.zip`, 35,057 bytes,
  SHA-256 `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
- Single CSV inside: `mushrooms.csv` (374,003 bytes, 2019-09-20 in archive),
  SHA-256 `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`.
  Merge is trivial: no other file to join, no row added or removed.
  The working file was NOT re-downloaded for this lot: it was copied
  and its hashes re-verified identical.
- Inventory: 8,124 rows × 23 columns, 0 exact duplicate rows. All columns
  are categorical single-letter codes: class, cap-shape, cap-surface,
  cap-color, bruises, odor, gill-attachment, gill-spacing, gill-size,
  gill-color, stalk-shape, stalk-root, stalk-surface-above-ring,
  stalk-surface-below-ring, stalk-color-above-ring, stalk-color-below-ring,
  veil-type, veil-color, ring-number, ring-type, spore-print-color,
  population, habitat.
- `class`: e=4,208, p=3,916. `stalk-root`: `?` on 2,480 rows (30.5%),
  the only missing marker. `veil-type`: constant (`p` on all rows).

## Encoding (pipeline accepts numeric only)
- Each letter → integer by order of first appearance in the file, per
  column. Full table: `data/mapping_encodage.json`. Examples: class
  p=0, e=1; odor p=0, a=1, l=2, n=3, f=4, c=5, y=6, s=7, m=8;
  veil-type p=0 (only value).
- `?` in stalk-root is NOT a category: encoded as true missing (NaN).
  As control, the pipeline drops those rows (5,644 valid for stalk-root);
  as flux, the pipeline replaces NaN by the flux mean before z-score.
- Working file `data/mushrooms_pipeline.csv` (8,124 × 23, numeric),
  SHA-256 `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
  Original preserved in `data/raw/`.

## Pipeline (frozen before any run of this lot)
- File: `pipeline/Tlog_v3_4_harmonic_v3.py`
  SHA-256 `81092eb61d612d0dea50f9fca6bfa12f6dbd2388c4e52a24ab064d09e61dc7f8`
  (corrected 26 Oct: NaN window-start). Derived from
  `pipeline_autonome_v3_3_harmonic_v1.py` (v3.3-H1, intact).
- v3.4-H3 changes: fast scan with identical results; Monte Carlo
  fallback logged; F1/F2 before AND after threshold; robust JSON export.
  See README and `VERIFICATION.md`.
- Settings: stable mode, initial w_size 80, Cohen d, seed 42,
  HARMONIC_PROB 0.45 (file default, not overridden),
  full_triangulation False.
- 23 runs, one per column as control, in file order, control EXCLUDED
  from analysed fluxes (Door D rule), original row order (the pipeline
  ranks the control itself).

## Resumable design and failure rules
- A run with `run_summary.json` is skipped; a run killed mid-way
  (VM restart, voluntary stop) is discarded and relaunched from
  scratch, never counted. Empty folders of interrupted v3.3 runs are
  not reused.
- Pre-registered failure rule: control with <80 valid values = measured
  failure (none expected here: minimum 5,644 valid, stalk-root).
- The veil-type run is attempted like the others; its outcome is
  recorded as-is, never read as a detector (constant flux).

## Interpretation reserves (frozen)
- Encoded codes are nominal labels, not magnitudes: a threshold is a
  rank cut on an arbitrary (appearance) order, read as rank plateaus.
- NEVER a rule to decide whether a mushroom is edible. The PDF will
  state this explicitly.
- No temporal/causal reading (no time column).
- Descriptive reading only: real data, no ground truth, no expected
  threshold claimed.
- Full detail required in reports: thresholds on all fluxes, F1/F2
  derivatives before and after threshold, MC / default / raw /
  rigid-1001 thresholds, stability checked against the bootstrap mean.

## v3.3 lot stopped (traceability)
- The v3.3 lot started 14:56 was stopped 26 Oct ~16:28 at the request
  to restart from zero with v3.4. Runs cap-shape, cap-surface,
  cap-color, bruises, odor, gill-attachment were killed before any
  output file (empty folders): nothing lost, nothing reused. The v3.3
  `class` pilot (finished 14:35) is kept separately for comparison
  only, outside this lot.

## Deliverables (this repository)
- Per control: `results/ctrl_<column>/` (run_summary, scan_curve,
  per_flux_thresholds, transition_F1F2 with pre+post, text_report,
  pipeline_results.json, threshold_scan and noise_diagnostic figures).
- Synthesis: `synthese_runs.csv`, `tous_seuils_par_flux.csv`,
  `tous_F1F2.csv`, `plateaux_controles.csv`.
- Final: `Mushroom_Classification_v34_Resultats_complets.pdf`,
  `RAPPORT.md`, results zip (pipeline_results.json excluded from the
  zip, kept in results/).
