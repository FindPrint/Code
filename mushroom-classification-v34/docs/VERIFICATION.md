# Verification / Vérifications (v3.4-H3, 26 Oct 2026)

All checks below were run before the v3.4 lot was launched, on the same
data file as the lot (`data/mushrooms_pipeline.csv`). They are the reason
the fast scan is trusted to replace the legacy scan without changing
results — and the reason one bug was caught before the lot.

## 1. Treated scan — identical / Scan traité — identique

- Control `class`, treated fluxes (z-scored, NaNs imputed by mean),
  w_size 861, 801 candidates, min_grp 2, Cohen d.
- Fast scan (v3.4 module): 5.8–7.9 s, threshold 52.75%.
- Reference: v3.3 pilot `scan_curve.csv` (same settings).
- **Max score difference: 0.0 on all 801 candidates. Argmax identical.**

## 2. Raw scan — bug found, fixed, re-verified / Scan brut — bug trouvé, corrigé, re-vérifié

- Raw fluxes (original encoded values, `stalk-root` NaNs kept),
  w_size 1034, 801 candidates, min_grp 5.
- Legacy raw scan: 782.1 s, threshold 62.5%.
- Fast raw scan (before fix): 8.0 s, threshold 62.5%, **but max
  difference 0.0149** — same threshold, different scores.
- Cause: a window STARTING with a NaN. The fast scan computed the
  window's first valid index as `valid_pos[window_start]`, which is -1
  when the window starts with NaN, shifting that window's sample.
  Treated scans were unaffected (NaNs imputed before scanning),
  which is why check 1 was perfect.
- Fix (in `scan_fast.py` and in `Tlog_v3_4_harmonic_v3.py`, and in the
  EN copy): first valid index = first valid >= window start, found by
  `searchsorted` over valid positions, checked to lie inside the window.
- Re-verification, single flux, same settings:
  - `stalk-root` alone: legacy 32.9 s vs fast 0.9 s, **max difference
    0.0**, argmax identical (73.25%).
  - `odor` alone (no NaN): legacy 36.1 s vs fast 0.4 s, **max
    difference 0.0**, argmax identical (60.875%).
- Conclusion: since every flux individually matches, and the global
  score is the mean of per-flux scores, the full raw curve is identical
  by construction. The v3.4 lot was restarted with the fixed code;
  the earlier v3.4 pilot (treated only, main threshold unaffected)
  was stopped and discarded.

## 3. Monte Carlo fallback — forced failure test / Repli Monte Carlo — test d'échec forcé

- Synthetic 300-row dataset, fast mode, 10 Monte Carlo iterations,
  `_sample_harmonic_guided` monkeypatched to return None (all draws
  invalid).
- Result: `threshold_source = default_fallback_mc_failed`,
  `opt_threshold = default_threshold = 19.1667%`,
  diagnostics `n_failed = 10/10` with failed iteration numbers,
  warnings recorded in metadata for both raw and treated data,
  and the text report contains a `THRESHOLD FALLBACK ALERT` section
  with the source and the warnings. Warnings also appear on stdout,
  stderr and in the Python log. Before v3.4, the raw case and the
  report were silent.

## 4. F1/F2 before and after threshold / F1/F2 avant et après seuil

- Same synthetic test, normal (unpatched) Monte Carlo, threshold
  18.67%, source `monte_carlo`.
- Example entry (`Higuchi` / `Tous`):
  - Post: F1 = 0.000958, F2 = -0.0000448
  - Pre: F1 = -0.000609, F2 = -0.000217
  - Deltas (post − pre): delta_F1 = 0.001567, delta_F2 = 0.000172,
    `sign_change = True`
- Both derivatives exist on both sides, computed with the same method
  (degree-2 fit on centred Progress). Post fields are unchanged from
  v3.3; pre fields are additions, not replacements.

## 5. English pipeline copy / Copie anglaise du pipeline

- `pipeline/Tlog_v3_4_harmonic_v3_en.py`: same logic, translated
  docstrings/comments/user-facing messages for the v3.4 sections and
  the most visible messages. Legacy v3.3 comments not translated in
  this pass remain in French (marked in the EN header).
- Verified: compiles, imports, treated pilot scan identical
  (threshold 52.75%, max difference 0.0, 4.7 s).

## What is NOT yet verified

- The full 23-control lot (in progress at repo creation). Its
  per-control summaries, stability labels, per-flux thresholds and
  F1/F2 tables will be compared control by control when complete,
  and the final PDF will be built from verified synthesis files only.
- The English copy has not yet run a full lot; the French copy is the
  lot reference. A full EN lot run is a follow-up, not a claim made here.
