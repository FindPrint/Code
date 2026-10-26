# Methodology — how the pipeline reads a threshold (summary)

This is a short peer summary, not a replacement for the pipeline code.
All definitions below are implemented in `pipeline/`; the frozen
protocol is in `PROTOCOL.md` / `PROTOCOLE.md`.

## 1. Control and fluxes

- One column is chosen as the **control**. It defines the progression
  axis: each row's rank in the control (as a percentage, 0–100%).
- Every other numeric column is a **flux**. The control is never among
  the analysed fluxes (Door D rule).
- Fluxes are z-scored before scanning (NaNs replaced by the flux mean).
  For the raw scan, original values are used, NaNs kept.

## 2. Threshold scan

- The control axis is cut into sliding windows (window size `w_size`).
  For each candidate threshold (a percentage on the progression axis),
  windows are split into low/high groups by their mean progression.
- For each flux, the low/high groups are compared with Cohen d
  (or Cliff delta if configured; this lot uses Cohen d). Groups larger
  than 1,000 values are downsampled to exactly 1,000 with a fixed
  seed (0) — this is why the fast scan can reproduce the legacy scan
  exactly without materialising the groups.
- The candidate score is the mean absolute Cohen d across fluxes.
  The candidate with the highest score is the scan threshold for that
  configuration.

## 3. Monte Carlo, harmonic-guided

- 50 iterations sample (window size, number of candidates, min group
  size). With probability HARMONIC_PROB (0.45), the sample is guided by
  mathematical constants (phi, pi, e, sqrt2, sqrt3); otherwise it is
  uniform. Each sampled configuration is scored by a composite
  (separation, stability, robustness, sharpness); the best is kept.
- A rigid witness scan with the historical 1001-candidate grid, same
  window, is also computed, to measure the grid effect — it is not the
  retained threshold.
- If no sampled configuration is valid, the default scan threshold is
  used and the fallback is LOGGED (see README point 2). The same
  applies, separately, to the raw-data Monte Carlo.

## 4. Stability, questions, noise

- **Stability:** the threshold scan is repeated for several window
  sizes; the label (e.g. UNSTABLE) comes from dispersion, and must
  always be checked against the bootstrap mean — a UNSTABLE label with
  a bootstrap mean almost equal to the Monte Carlo threshold is a
  dispersion warning, not a disagreement.
- **Questions Q1–Q5:** per-flux complexity signatures (Higuchi, DFA,
  Katz, Hurst, Sample Entropy and related estimators, computed on
  windows) are summarised per question; see the pipeline code and the
  per-run `numerical_results.csv`.
- **Noise diagnostic:** checks whether the strongest signal behaves
  like a coloured-variance proxy (CSD) rather than white noise.

## 5. F1/F2 before and after threshold (v3.4)

- For each complexity estimator and each flux (plus `Tous`, the mean
  across fluxes), the pipeline fits a degree-2 polynomial of the
  estimator vs centred Progress, separately:
  - **after** threshold: Progress >= threshold (if <3 points, expanded
    to >= threshold − 10, flagged);
  - **before** threshold: Progress < threshold (if <3 points, expanded
    to < threshold + 10, flagged).
- F1 = linear coefficient (slope at the segment centre), F2 = 2 ×
  quadratic coefficient. Sign/order follow the same 1e-6 rule on both
  sides. Deltas (post − pre) and `sign_change` are recorded when both
  sides succeed; otherwise they are None, never 0 by default.
- If a segment has <3 points even after expansion, its status is
  `insufficient_data` with an explicit reason.

## 6. Reading the results — limits

- Discrete / nominal controls: read thresholds as rank plateaus, not
  as physical cut values. A precise-looking percentage overstates what
  a cut separates for discrete controls.
- Missingness decides what a threshold can mean: a strong signal can
  describe how a file was filled, not a physical regime — always check
  missingness and discreteness before interpreting a cut.
- No edible/poisonous decision, no causal claim, no temporal claim
  from this dataset.
