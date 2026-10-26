# Mushroom Classification × Tlog pipeline v3.4-H3

**English version — [Version française](README.fr.md)**

Descriptive regime-threshold analysis of the Kaggle Mushroom Classification
dataset, run with the autonomous Tlog pipeline v3.4-H3, one column at a time
as the control column. This repository is the trace, memory and proof of
that execution: code, data, frozen protocol, scripts, verification, and
— as they complete — results and figures.

> **Status (26 Oct 2026, ~16:35 EDT):** v3.4 lot restarted from zero.
> First pair running: `class` + `cap-shape`. 0/23 runs complete in this
> lot. Results will be pushed here at each checkpoint and at completion.
> The earlier v3.3 lot was stopped before any output file (see
> `docs/PROTOCOLE.md` for traceability); the v3.3 `class` pilot is kept
> separately for comparison only and is NOT counted in this lot.

## What this is — and is not

- **What:** a descriptive measurement. For each control column, the
  pipeline scans for a critical threshold (Monte Carlo, harmonic-guided),
  reports stability (bootstrap), per-flux thresholds, and F1/F2
  derivatives before AND after the threshold.
- **What not:** this is NOT a rule to decide whether a mushroom is
  edible. Encoded codes are nominal labels, not magnitudes; a threshold
  is a rank cut on an arbitrary (first-appearance) order, read as rank
  plateaus. No temporal or causal reading (there is no time column).
- **No ground truth claimed:** real data, no expected threshold asserted.

## Quick start (test in minutes)

```bash
python3 -m pip install -r requirements.txt
# Fast demo: 1 control, fast mode, 10 Monte Carlo iterations
python3 scripts/demo.py
# Full lot (23 controls, stable mode, ~hours): see scripts/batch_v34.sh
bash scripts/batch_v34.sh
# One control, e.g. class, stable mode:
python3 scripts/run_one_v34.py class results/ctrl_class
```

`scripts/demo.py` runs on the provided data with fast mode; it is the
quick peer test. The full lot uses stable mode, seed 42, Cohen d,
initial window 80, harmonic probability 0.45 (see `docs/PROTOCOL.md`).

## Repository layout

```
pipeline/   Tlog_v3_4_harmonic_v3.py      (French, reference)
            Tlog_v3_4_harmonic_v3_en.py   (English, logic identical)
data/       mushrooms_pipeline.csv        (encoded working file, 8124x23)
            mapping_encodage.json         (letter -> integer, first appearance)
            raw/mushrooms.csv             (original Kaggle CSV)
docs/       PROTOCOL.md / PROTOCOLE.md    (frozen protocol, EN/FR)
            METHODOLOGY.md / METHODOLOGIE.md
            VERIFICATION.md               (scan + fallback + F1/F2 checks)
            TRACEABILITY.md               (systematic trace rule for all projects)
scripts/    run_one_v34.py, batch_v34.sh, synthese.py, demo.py
results/    per-control outputs (added as the lot progresses)
```

## Data source

- Kaggle dataset `uciml/mushroom-classification`:
  https://www.kaggle.com/datasets/uciml/mushroom-classification
- Downloaded file: `mushroom-classification.zip` (35,057 bytes),
  SHA-256 `4e688bc1234b8f56d5abcbafc64f50983465066dd0036082714ff911c0a35081`
- The zip contains a SINGLE CSV (`mushrooms.csv`, 374,003 bytes,
  SHA-256 `f0284c7a4210c4b0793713de9c45841d66f9bb27f6408f8bfedb6b34e6d6f53c`),
  so the "merge" is trivial: no other file to join, no row added or removed.
- Working file `mushrooms_pipeline.csv`, SHA-256
  `fa6e5cebe8e26faaa803873c7cd01f9d9f4c6b9bafe2884270572a0002fda0ee`.
- 8,124 rows × 23 categorical single-letter columns. `class`: e=4,208,
  p=3,916. `stalk-root`: `?` on 2,480 rows (30.5%), encoded as true
  missing (NaN). `veil-type`: constant (`p` on all rows).

## Pipeline v3.4-H3 — what changed vs v3.3-H1

1. **Fast scan, identical results.** The v3.3 scan concatenated all
   sliding windows (~n_windows × w_size values per flux per candidate)
   although `separation_score()` then kept only 1,000 draws (seed 0).
   The fast scan recovers each drawn value by index arithmetic
   (window = index // w_size, offset = index % w_size; NaN case via
   valid-values array and per-window cumulatives) and reproduces the
   exact draw, including the rng(0) sequence shared by the two groups.
   Verified: treated pilot, threshold 52.75%, max score difference
   0.0 on 801 candidates, 5.8 s vs ~48 s per scan; raw `stalk-root`
   alone, difference 0.0 after a NaN-window-start correction
   (see `docs/VERIFICATION.md`).
2. **Monte Carlo fallback, logged.** When Monte Carlo yields no valid
   configuration, the default threshold was already used, but silently
   in several places (raw case, text report, failed iterations
   uncounted, 52.5% emergency value in the noise diagnostic). Now every
   fallback is printed (stdout + stderr), logged, and recorded in
   metadata (`threshold_source`, `threshold_warnings`) and in the text
   report. A fallback threshold can no longer pass as a Monte Carlo
   threshold.
3. **F1/F2 before AND after threshold.** `transition_analysis` previously
   computed only post-threshold derivatives. v3.4 adds, with the same
   method (degree-2 polynomial fit on centred Progress), pre-threshold
   `first_derivative_pre` / `second_derivative_pre`, plus post-minus-pre
   deltas and `sign_change`. Post fields are unchanged for v3.3
   compatibility.
4. **Robust JSON export** (tuples, sets, numpy arrays sanitised).

Pipeline file SHA-256 (French, corrected 26 Oct):
`81092eb61d612d0dea50f9fca6bfa12f6dbd2388c4e52a24ab064d09e61dc7f8`

## Environment

Python 3.12.3, numpy 1.26.4, pandas 2.1.4, scipy 1.11.4,
matplotlib 3.6.3 (plus seaborn). See `requirements.txt`.
Machine used for the lot: 2 vCPU, 7.7 GB RAM container, no swap —
hence the fast scan and the resumable batch design (a run with
`run_summary.json` is skipped; an interrupted run is discarded and
relaunched from scratch, never counted).

## License — pending author decision

No license file is included yet on purpose: the author has not chosen
one. Until then, this private repository is shared for reading, testing
and reproduction by invited peers only — no redistribution, no
commercial use, no public mirroring without the author's written
permission. See `LICENSE-NOTE.md`.

## Traceability (systematic rule)

From 26 Oct 2026, this traceability pattern applies to ALL code,
executions and projects done with Muse, not just this lot — see
`docs/TRACEABILITY.md`: frozen protocol before runs, code + data hashes,
per-run outputs, synthesis, PDF, and repository updates at checkpoints
and at completion, as memory and proof.
