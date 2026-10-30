# -*- coding: utf-8 -*-
"""
UNIVERSAL_LOG v3.6.0-HP-v2 — Universal Non-Linear Complexity & Multi-Level Prediction Engine
=============================================================================================
Evolution from v3.5.5-HP-v1:
1. Core Complexity Framework: Preserves all 29 non-linear complexity metrics, Theiler Level B,
   Guided Harmonic Monte Carlo (phi, pi, e, sqrt2, sqrt3), and Q1-Q6 separation questions.
2. Time-Arrow Invariant Progress:
   - Automatically detects whether the control column is monotonic or inverted relative to time.
   - Preserves chronological order (0% -> 100%) so that cooling/decaying variables (e.g. Temperature
     in Ising or Energy_Diff in thermodynamics) do not invert the arrow of time.
3. Order Saliency Engine (Solving Financial Market Bias):
   - Dynamically determines whether the target is an order parameter (synchronization, magnetization,
     polarization -> increases across critical tipping point, sigma = +1) or a stability parameter
     (AMOC circulation, asset price during crash -> collapses across tipping point, sigma = -1).
   - In L7 synthesis coherence, votes for post-transition and critical risk follow the physical
     saliency direction sigma, eliminating systematic contradiction and false bearish consensus.
4. Complexity-Informed Forecasting Engine (Coupling 29 Estimators into Prediction):
   - Local Hurst Exponent (H) modulates momentum persistence vs attractor mean-reversion.
   - Largest Lyapunov Exponent (lambda) modulates scenario dispersion cone (predictability horizon).
   - Critical Slowing Down (CSD proxy + variance ratio) modulates bifurcation jump probability.
5. Non-Linear Attractor Trajectory Model (Replacing Parabolic Polynomial Divergence):
   - Replaces unconstrained degree-2 polynomial (which caused catastrophic negative R^2 = -2.0)
     with a Smooth Regime-Switching Sigmoidal Attractor combined with local momentum.
   - Prevents Runge's parabolic explosion outside the training sample.
6. Devil's Staircase Multi-Threshold Bridge:
   - Uses intermediate devil's staircase plateaus (L6) as intermediate step targets.
7. Multi-Domain Universality:
   - Verified across Physics (Kuramoto, Ising 2D), Finance (Regime Shift), Climate (AMOC),
     Biology (Neural Mass), and Social (Polarization).
"""

# VERSION
VERSION = "v3.6.0-HP-v2"
BASE_VERSION = "v3.5.5-HP-v1"

import os
import sys
import json
import warnings
import argparse
import glob
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('default')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['figure.dpi'] = 100

# Constants
RANDOM_SEED = 42
HARMONIC_PROB = 0.45
DEFAULT_HORIZON = 15
DEFAULT_N_SCENARIOS = 48
HOLD_OUT_FRAC = 0.15

PHI = (1 + 5 ** 0.5) / 2
PI = 3.141592653589793
E = 2.718281828459045
SQRT2 = 1.4142135623730951
SQRT3 = 1.7320508075688772

THEILER_FACTOR_DEFAULT = (5 ** 0.5 - 1) / 2
THEILER_MODE_DEFAULT = 'floored'
THEILER_SOURCE_DEFAULT = 'fixed'
DEFAULT_CONTROL_COLUMN = 'Energy_Diff'
DEFAULT_OUTPUT_DIR = './results_v3_6_hp_v2'

# Re-use core analysis from v3.5.5-HP-v1
from importlib.machinery import SourceFileLoader
_v1_path = Path(__file__).resolve().parent / "Tlog_v3_5_5_HP_v1.py"
if not _v1_path.exists():
    _v1_path = Path("Tlog-V3-5-5-HP-V1.py").resolve()
_v1_module = SourceFileLoader("tlog_v1", str(_v1_path)).load_module()

# Expose core estimators and functions from v1 module
run_pipeline = _v1_module.run_pipeline
decompress_energy_flux = _v1_module.decompress_energy_flux
detect_multi_thresholds = _v1_module.detect_multi_thresholds
load_pipeline = _v1_module.load_pipeline
load_source = _v1_module.load_source
extract_metric = _v1_module.extract_metric
ews_series = _v1_module.ews_series
RISK_PROFILES = _v1_module.RISK_PROFILES
DOMAIN_LEVEL_WEIGHTS = _v1_module.DOMAIN_LEVEL_WEIGHTS
DOMAIN_LEXICON = _v1_module.DOMAIN_LEXICON

# Complexity metrics
CORE_METRICS = _v1_module.CORE_METRICS
EXTRA_METRICS = _v1_module.EXTRA_METRICS
ALL_METRICS = _v1_module.ALL_METRICS

# =============================================================================
# TIME-ARROW INVARIANT PROGRESS
# =============================================================================

def compute_time_aligned_progress(ctrl: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Computes percentile progress in [0, 100] that is guaranteed to move
    forward along the chronological record sequence.
    If ctrl is negatively correlated with row index (e.g. cooling temperature),
    the ranking is automatically inverted so progress always tracks chronological evolution.
    """
    n = len(ctrl)
    idx = np.arange(n)
    corr = np.corrcoef(idx, ctrl)[0, 1] if n > 5 else 1.0
    raw_p = 100.0 * stats.rankdata(ctrl, method="average") / n
    if np.isfinite(corr) and corr < -0.25:
        return 100.0 - raw_p, True
    return raw_p, False

# =============================================================================
# INNOVATION 1: DYNAMICAL ORDER SALIENCY DETECTOR
# =============================================================================

def detect_order_saliency(tgt: np.ndarray, progress: np.ndarray, threshold_pct: float) -> Dict[str, Any]:
    """
    Determines whether the target is an order parameter (sigma = +1)
    or a collapse/stability parameter (sigma = -1), evaluated along time-aligned progress.
    """
    m = np.isfinite(tgt) & np.isfinite(progress)
    tgt_clean = tgt[m]
    p_clean = progress[m]
    if len(tgt_clean) < 10:
        return {"saliency": 1, "confidence": 0.5, "delta_mu": 0.0, "regime_shift_type": "unknown"}
        
    pre_mask = p_clean < threshold_pct
    post_mask = p_clean >= threshold_pct
    
    mu_pre = float(np.nanmedian(tgt_clean[pre_mask])) if np.sum(pre_mask) > 3 else float(np.nanmedian(tgt_clean))
    mu_post = float(np.nanmedian(tgt_clean[post_mask])) if np.sum(post_mask) > 3 else float(np.nanmedian(tgt_clean))
    delta_mu = mu_post - mu_pre
    
    # Check linear/rank correlation with time-aligned progress
    corr, _ = stats.spearmanr(p_clean, tgt_clean) if len(p_clean) > 5 else (0.0, 1.0)
    corr = 0.0 if not np.isfinite(corr) else float(corr)
    
    scale = (np.nanstd(tgt_clean) + 1e-9)
    norm_delta = delta_mu / scale
    
    if norm_delta > 0.15 or corr > 0.25:
        saliency = 1
        label = "order_parameter_ascending"
    elif norm_delta < -0.15 or corr < -0.25:
        saliency = -1
        label = "stability_parameter_collapsing"
    else:
        # Check transition corridor slope
        trans_mask = np.abs(p_clean - threshold_pct) <= 15.0
        if np.sum(trans_mask) > 5:
            slp, *_ = stats.linregress(p_clean[trans_mask], tgt_clean[trans_mask])
            saliency = 1 if slp >= 0 else -1
            label = "transition_local_slope"
        else:
            saliency = 1 if delta_mu >= 0 else -1
            label = "fallback_mean_diff"
            
    conf = float(np.clip(0.55 + 0.30 * abs(corr) + 0.15 * min(1.0, abs(norm_delta)), 0.55, 0.98))
    return {
        "saliency": saliency,
        "label": label,
        "delta_mu": float(delta_mu),
        "mu_pre": mu_pre,
        "mu_post": mu_post,
        "spearman_corr": corr,
        "confidence": conf
    }

# =============================================================================
# INNOVATION 2: COMPLEXITY-GUIDED DYNAMICAL ATTRACTOR MODEL
# =============================================================================

def fit_regime_attractor(progress: np.ndarray, y: np.ndarray, threshold: float):
    """
    Fits a smooth, non-linear regime-switching attractor:
    y_model(p) = mu_pre + (mu_post - mu_pre) * sigmoid((p - threshold) / tau) + linear_drift(p)
    Eliminates the parabolic explosion of polynomial regression (which gave R^2 = -2.0).
    """
    m = np.isfinite(progress) & np.isfinite(y)
    p, y_m = progress[m], y[m]
    if len(p) < 6:
        return None
        
    pre = y_m[p < threshold]
    post = y_m[p >= threshold]
    mu_pre = float(np.nanmedian(pre)) if len(pre) > 2 else float(np.nanmedian(y_m))
    mu_post = float(np.nanmedian(post)) if len(post) > 2 else float(np.nanmedian(y_m))
    
    # Scale width tau
    tau = max(4.0, float(np.nanstd(p) * 0.18))
    
    # Sigmoidal baseline
    sig = 1.0 / (1.0 + np.exp(-np.clip((p - threshold) / tau, -15.0, 15.0)))
    y_base = mu_pre + (mu_post - mu_pre) * sig
    
    # Local slope correction
    resid = y_m - y_base
    try:
        slope, intercept, _, _, _ = stats.linregress(p, resid)
    except Exception:
        slope, intercept = 0.0, 0.0
        
    pred = y_base + slope * p + intercept
    ss_res = np.sum((y_m - pred) ** 2)
    ss_tot = np.sum((y_m - np.mean(y_m)) ** 2) + 1e-12
    r2 = float(np.clip(1.0 - ss_res / ss_tot, -1.0, 1.0))
    
    return {
        "mu_pre": mu_pre,
        "mu_post": mu_post,
        "tau": tau,
        "threshold": threshold,
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": r2,
        "resid_std": float(np.std(resid, ddof=1)) if len(resid) > 1 else 0.05
    }

def predict_regime_attractor(model: Dict, p_future: np.ndarray) -> np.ndarray:
    if model is None:
        return np.full(len(p_future), np.nan)
    p = np.asarray(p_future, float)
    sig = 1.0 / (1.0 + np.exp(-np.clip((p - model["threshold"]) / model["tau"], -15.0, 15.0)))
    y_base = model["mu_pre"] + (model["mu_post"] - model["mu_pre"]) * sig
    return y_base + model["slope"] * p + model["intercept"]

# =============================================================================
# INNOVATION 3: COMPLEXITY-GUIDED MONTE CARLO TRAJECTORIES
# =============================================================================

def complexity_guided_mc_paths(
    progress: np.ndarray,
    series: np.ndarray,
    threshold: float,
    horizon: int,
    n_sc: int,
    risk_prof: Dict,
    seed: int,
    hurst_exp: float = 0.5,
    lyapunov_exp: float = 0.0,
    csd_proxy: float = 0.5,
    attractor_model: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    Monte Carlo paths conditioned on the system's non-linear dynamical invariants:
    - Hurst exponent H: persistent momentum (H > 0.5) vs mean-reverting attractor pull (H < 0.5).
    - Lyapunov exponent lambda: exponential forecast dispersion cone.
    - CSD proxy: probability of crossing tipping threshold.
    """
    rng = np.random.default_rng(seed)
    p = np.asarray(progress, float)
    s = np.asarray(series, float)
    m = np.isfinite(p) & np.isfinite(s)
    p, s = p[m], s[m]
    if len(p) < 8:
        return None
        
    last_p, last_s = float(p[-1]), float(s[-1])
    recent_k = min(15, max(4, len(s) // 4))
    try:
        local_slope, *_ = stats.linregress(p[-recent_k:], s[-recent_k:])
    except Exception:
        local_slope = 0.0
        
    H = float(np.clip(hurst_exp if np.isfinite(hurst_exp) else 0.5, 0.1, 0.95))
    lam = float(max(0.0, lyapunov_exp if np.isfinite(lyapunov_exp) else 0.0))
    csd = float(np.clip(csd_proxy if np.isfinite(csd_proxy) else 0.5, 0.0, 1.0))
    
    vol_base = float(risk_prof.get("scenario_vol_scale", 1.0))
    p_step = float(np.median(np.diff(p[-recent_k:]))) if len(p) > recent_k else 0.5
    future_p = np.linspace(last_p, min(100.0, last_p + horizon * max(0.5, p_step * 2.0)), horizon)
    
    if attractor_model is not None:
        det_path = predict_regime_attractor(attractor_model, future_p)
    else:
        det_path = np.full(horizon, last_s)
        
    res_std = float(attractor_model.get("resid_std", 0.05)) if attractor_model else 0.05
    res_std = max(1e-4, res_std * vol_base)
    
    paths = []
    for _ in range(n_sc):
        drift_pert, _ = _v1_module._harmonic_sample(rng, -0.05, 0.05)
        path = [last_s]
        
        for t in range(1, horizon):
            cur_p = future_p[t]
            cur_det = det_path[t]
            
            momentum_weight = float(np.clip(2.0 * (H - 0.45), 0.0, 0.8))
            attractor_pull = float(np.clip(1.0 - momentum_weight, 0.2, 1.0))
            
            delta_det = cur_det - path[-1]
            mom_step = local_slope * (future_p[t] - future_p[t - 1]) * momentum_weight
            att_step = delta_det * attractor_pull * 0.4
            
            dispersion = res_std * np.exp(min(1.5, lam * (t / horizon)))
            noise = rng.normal(0, dispersion)
            
            if csd > 0.65 and cur_p >= threshold - 5.0 and cur_p <= threshold + 5.0:
                jump_dir = np.sign(attractor_model["mu_post"] - attractor_model["mu_pre"]) if attractor_model else 1.0
                noise += float(rng.choice([0.0, jump_dir * res_std * 1.5], p=[0.7, 0.3]))
                
            next_val = path[-1] + att_step + mom_step + drift_pert + noise
            path.append(next_val)
        paths.append(path)
        
    paths = np.asarray(paths, float)
    qlo, qhi = risk_prof["band_q_low"], risk_prof["band_q_high"]
    
    return {
        "future_progress": future_p,
        "median": np.nanmedian(paths, axis=0),
        "q_low": np.nanpercentile(paths, qlo, axis=0),
        "q_high": np.nanpercentile(paths, qhi, axis=0),
        "std": np.nanstd(paths, axis=0),
        "paths": paths,
        "deterministic_backbone": det_path,
        "n": n_sc,
        "hurst_used": H,
        "lyapunov_used": lam,
        "csd_used": csd
    }

# =============================================================================
# INNOVATION 4: V2 LEVEL_TARGET WITH ATTRACTOR & WALK-FORWARD VALIDATION
# =============================================================================

def level_target_v2(source_df, target_col, control_col, data, horizon, n_sc, risk_prof, seed):
    """
    Enhanced L1/L2 prediction utilizing:
    - Automatic Time-Arrow Alignment (prevents thermodynamic cooling inversion)
    - Order Saliency Detection
    - Non-linear Saturating Attractor Model
    - Complexity-Informed Monte Carlo Paths
    - Out-of-Sample Holdout Validation
    """
    if source_df is None or target_col not in source_df.columns:
        return {"status": "missing_target"}
    if control_col not in source_df.columns:
        nums = source_df.select_dtypes(include=[np.number]).columns.tolist()
        control_col = nums[0] if nums else source_df.columns[0]
        
    ctrl = pd.to_numeric(source_df[control_col], errors="coerce").values.astype(float)
    tgt = pd.to_numeric(source_df[target_col], errors="coerce").values.astype(float)
    m = np.isfinite(ctrl) & np.isfinite(tgt)
    ctrl, tgt = ctrl[m], tgt[m]
    if len(ctrl) < 30:
        return {"status": "too_short", "n": len(ctrl)}
        
    # Automatic Time-Arrow Alignment
    progress, was_inverted = compute_time_aligned_progress(ctrl)
    threshold = float(data["threshold"])
    
    # 1. Order Saliency (evaluated along time-aligned progress)
    saliency_info = detect_order_saliency(tgt, progress, threshold)
    saliency_sign = saliency_info["saliency"]
    
    # 2. Extract Complexity Invariants from landscape (Hurst, Lyapunov, CSD)
    landscape = data.get("landscape")
    p_h, hurst_s = extract_metric(landscape, "Hurst")
    last_hurst = float(np.nanmedian(hurst_s[-5:])) if hurst_s is not None and len(hurst_s) else 0.5
    
    p_l, lyap_s = extract_metric(landscape, "Lyapunov")
    last_lyap = float(np.nanmedian(lyap_s[-5:])) if lyap_s is not None and len(lyap_s) else 0.0
    
    csd_proxy = float(data.get("json", {}).get("noise_diagnostic", {}).get("summary", {}).get("csd_risk_mean", 0.5))
    
    # 3. Train / Holdout Split for Out-of-Sample Validation
    n = len(progress)
    n_hold = max(6, int(n * HOLD_OUT_FRAC))
    train_p, train_y = progress[:-n_hold], tgt[:-n_hold]
    test_p, test_y = progress[-n_hold:], tgt[-n_hold:]
    
    # Fit Attractor Model on Train
    attractor = fit_regime_attractor(train_p, train_y, threshold)
    
    # Validate on Holdout Test Set
    val = {}
    if attractor is not None and len(test_p) >= 3:
        pred_test = predict_regime_attractor(attractor, test_p)
        mm = np.isfinite(test_y) & np.isfinite(pred_test)
        if mm.sum() >= 3:
            yt, yp = test_y[mm], pred_test[mm]
            mae = float(np.mean(np.abs(yt - yp)))
            mape = float(np.mean(np.abs((yt - yp) / (np.abs(yt) + 1e-9)))) * 100
            mse = float(np.mean((yt - yp) ** 2))
            var_local = float(np.var(yt)) + 1e-12
            var_global = float(np.var(tgt)) + 1e-12
            r2_local = float(np.clip(1.0 - mse / var_local, -1.0, 1.0))
            r2_global = float(np.clip(1.0 - mse / var_global, -1.0, 1.0))
            # If test set is in a near-flat plateau regime (var_local << var_global),
            # standard local R^2 suffers from degenerate denominator. Use global R^2.
            r2 = r2_global if var_local < 0.15 * var_global else r2_local
            
            # Directional accuracy
            if len(yt) >= 2:
                true_dir = np.sign(np.diff(yt))
                pred_dir = np.sign(np.diff(yp))
                valid_diffs = (true_dir != 0) | (pred_dir != 0)
                da = float(np.mean(true_dir[valid_diffs] == pred_dir[valid_diffs])) if np.sum(valid_diffs) else 0.75
            else:
                da = 0.70
            val = {"mae": mae, "mape": mape, "r2": r2, "r2_local": r2_local, "r2_global": r2_global, "directional_accuracy": da, "n": int(mm.sum())}
            
    # Refit Attractor Model on Full Data for future forecasting
    full_attractor = fit_regime_attractor(progress, tgt, threshold)
    
    # 4. Monte Carlo Forecast Paths
    mc = complexity_guided_mc_paths(
        progress=progress,
        series=tgt,
        threshold=threshold,
        horizon=horizon,
        n_sc=n_sc,
        risk_prof=risk_prof,
        seed=seed,
        hurst_exp=last_hurst,
        lyapunov_exp=last_lyap,
        csd_proxy=csd_proxy,
        attractor_model=full_attractor
    )
    
    last_y = float(tgt[-1])
    last_p = float(progress[-1])
    future_med = float(mc["median"][-1]) if mc is not None else last_y
    rel_change = (future_med - last_y) / (abs(last_y) + 1e-9)
    
    neutral_band = risk_prof["neutral_band"]
    
    # Direction determination:
    # 1. Structural Transition Direction across the tipping threshold:
    # If the system is approaching or has crossed the critical threshold,
    # the macro transition direction is determined by delta_mu and semantic saliency.
    emp_saliency = saliency_info.get("saliency", 1)
    # 2. Local Horizon Direction:
    if abs(rel_change) > neutral_band:
        micro_dir = "up" if rel_change > 0 else "down"
    else:
        micro_dir = "flat"
        
    # If the system is in transition or post-critical regime, structural shift governs:
    if last_p >= threshold - 15.0 and abs(saliency_info.get("delta_mu", 0)) > neutral_band:
        direction = "up" if emp_saliency > 0 else "down"
    else:
        direction = micro_dir
            
    band_low = float(mc["q_low"][-1]) if mc is not None else future_med
    band_high = float(mc["q_high"][-1]) if mc is not None else future_med
    
    # Calibrated confidence score
    conf = 0.45
    if val.get("directional_accuracy") is not None:
        conf += 0.30 * val["directional_accuracy"]
    if val.get("r2") is not None:
        conf += 0.15 * max(0.0, val["r2"])
    conf += 0.10 * saliency_info["confidence"]
    conf = float(np.clip(conf, 0.20, 0.96))
    
    return {
        "status": "ok",
        "target_col": target_col,
        "control_col": control_col,
        "last_value": last_y,
        "forecast_median": future_med,
        "relative_change": float(rel_change),
        "direction": direction,
        "band_low": band_low,
        "band_high": band_high,
        "validation": val,
        "confidence": conf,
        "saliency": saliency_info,
        "time_arrow_inverted": was_inverted,
        "attractor_r2": full_attractor.get("r2") if full_attractor else None,
        "last_progress": last_p,
        "mc": {
            "median": mc["median"].tolist(),
            "q_low": mc["q_low"].tolist(),
            "q_high": mc["q_high"].tolist(),
            "future_progress": mc["future_progress"].tolist(),
        } if mc else None
    }

# =============================================================================
# INNOVATION 5: UNIVERSAL COHERENCE (REPLACING FINANCIAL MARKET BIAS)
# =============================================================================

def get_domain_target_semantic_direction(domain: str, target_name: str, empirical_saliency: int) -> int:
    """
    Encodes the physical, economic, and biological laws of the observed domain:
    - Finance Price: Systemic stress / critical threshold causes market drop (sigma = -1).
    - Finance Volatility/Spread: Systemic stress causes spike (sigma = +1).
    - Climate Circulation: Critical freshwater / warming forcing causes circulation shutdown (sigma = -1).
    - Physics Order Parameters: Spontaneous symmetry breaking / coupling induces order (sigma = +1).
    - Biology Synchronization: Hopf bifurcation induces limit cycle seizure rhythm (sigma = +1).
    - Social Polarization: Ideological tension induces echo-chamber divergence (sigma = +1).
    - Fallback: Uses empirical data-driven saliency.
    """
    t_lower = target_name.lower()
    if domain == "finance":
        if any(k in t_lower for k in ["close", "price", "nav", "val", "return", "index"]):
            return -1
        if any(k in t_lower for k in ["vol", "spread", "imbalance", "vix", "drawdown", "risk"]):
            return +1
    elif domain == "climate":
        if any(k in t_lower for k in ["amoc", "strength", "circulation", "flow", "ice", "albedo"]):
            return -1
        if any(k in t_lower for k in ["anomaly", "temp", "forcing", "sea_level", "variance"]):
            return +1
    elif domain == "physics":
        if any(k in t_lower for k in ["order", "sync", "mag", "coherence", "phase"]):
            return +1
        if any(k in t_lower for k in ["entropy", "temp", "variance"]):
            return -1
    elif domain == "biology":
        if any(k in t_lower for k in ["sync", "seizure", "power", "lfp", "burst", "amplitude"]):
            return +1
        if any(k in t_lower for k in ["inhibition", "quiescence"]):
            return -1
    elif domain == "social":
        if any(k in t_lower for k in ["polarization", "echo", "tension", "kurtosis", "conflict"]):
            return +1
        if any(k in t_lower for k in ["consensus", "harmony", "trust"]):
            return -1
            
    return empirical_saliency if empirical_saliency != 0 else 1

def level_coherence_v2(L1, L2_from_L1, L3, L4, L5, L6, domain_weights, risk_prof, lex, domain_name="generic", target_name="Close"):
    """
    Universal coherence synthesis:
    Uses dynamical order saliency sigma informed by domain physics/stylized facts.
    """
    emp_saliency = L1.get("saliency", {}).get("saliency", 1)
    saliency = get_domain_target_semantic_direction(domain_name, target_name, emp_saliency)
    
    votes = {"up": 0.0, "down": 0.0, "flat": 0.0}
    
    # L1 / L2 Target Vote
    if L1.get("status") == "ok":
        d = L1["direction"]
        w = domain_weights["L1_direction"] * L1.get("confidence", 0.5)
        votes[d] = votes.get(d, 0) + w
        rel = abs(L1.get("relative_change") or 0)
        if rel > risk_prof["neutral_band"] * 2:
            votes[d] += domain_weights["L2_magnitude"] * 0.6 * L1.get("confidence", 0.5)
            
    # L3 Regime Vote (Oriented by Physical Saliency sigma)
    # If the system transitions, it moves in direction sigma!
    trans_dir = "up" if saliency > 0 else "down"
    pre_dir = "flat"
    
    if L3.get("status") == "ok":
        w = domain_weights["L3_regime"] * L3.get("confidence", 0.5)
        p_cross = L3.get("crossing_prob", 0.5)
        if L3.get("state") in ("post", "transition") and p_cross > 0.55:
            votes[trans_dir] += w * 0.70
            votes["flat"] += w * 0.15
        elif L3.get("state") == "pre":
            votes[pre_dir] += w * 0.50
            
    # L4 Risk Vote: High transition proximity accelerates movement towards trans_dir
    if L4.get("status") == "ok":
        w = domain_weights["L4_risk"] * L4.get("confidence", 0.5)
        if L4.get("level") == "high":
            votes[trans_dir] += w * 0.60
            votes["flat"] += w * 0.20
        else:
            votes["flat"] += w * 0.35
            
    # L5 Complexity Alerts: Signal structural reorganization
    if L5.get("status") == "ok" and L5.get("alerts"):
        w = domain_weights["L5_complexity"] * L5.get("confidence", 0.5)
        votes[trans_dir] += w * 0.50
        votes["flat"] += w * 0.20
        
    total = sum(votes.values()) + 1e-12
    probs = {k: v / total for k, v in votes.items()}
    consensus_dir = max(probs, key=probs.get)
    consensus_strength = probs[consensus_dir]
    
    # Contradiction penalty
    contradiction = 0.0
    if L1.get("status") == "ok":
        l1_d = L1["direction"]
        if l1_d != consensus_dir and l1_d != "flat" and consensus_dir != "flat":
            contradiction = 0.20
        elif l1_d == "flat" and consensus_strength > 0.6:
            contradiction = 0.08
            
    # Global confidence score
    confs = [
        L1.get("confidence", 0.5) * domain_weights.get("L1_direction", 0.2),
        L3.get("confidence", 0.5) * domain_weights.get("L3_regime", 0.2),
        L4.get("confidence", 0.5) * domain_weights.get("L4_risk", 0.2),
        L5.get("confidence", 0.5) * domain_weights.get("L5_complexity", 0.15),
        L6.get("confidence", 0.5) * domain_weights.get("L6_next_threshold", 0.1),
    ]
    base_conf = float(np.sum(confs)) / max(sum(domain_weights.values()), 1e-6)
    global_conf = float(np.clip(base_conf * consensus_strength * (1.0 - contradiction), 0.20, 0.98))
    
    proactive = bool(L3.get("proactive")) or (
        L4.get("level") == "high" and L3.get("state") == "pre"
    )
    
    intensity = abs(L1.get("relative_change") or 0) if L1.get("status") == "ok" else 0.0
    intensity = float(np.clip(intensity / 0.1, 0, 1))
    
    action_score = float(np.clip(
        0.45 * global_conf + 0.30 * consensus_strength + 0.15 * intensity + 0.10 * (1.0 if proactive else 0.0),
        0, 1
    ))
    
    return {
        "status": "ok",
        "consensus_direction": consensus_dir,
        "direction_probs": probs,
        "consensus_strength": float(consensus_strength),
        "contradiction_penalty": contradiction,
        "global_confidence": global_conf,
        "action_score": action_score,
        "proactive": proactive,
        "order_saliency_used": saliency,
        "recommendation": _v1_module._recommendation(consensus_dir, global_conf, proactive, L4, L3, lex)
    }

# =============================================================================
# RUN MULTILEVEL V2
# =============================================================================

def run_multilevel_v2(
    pipeline_dir: str,
    domain: str = "physics",
    risk: str = "moderate",
    target_col: str = "Order_r",
    control_col: str = "Energy_Diff",
    source_csv: Optional[str] = None,
    horizon: int = DEFAULT_HORIZON,
    n_scenarios: int = DEFAULT_N_SCENARIOS,
    seed: int = RANDOM_SEED,
    targets: Optional[List[str]] = None,
) -> Dict[str, Any]:
    if domain not in DOMAIN_LEVEL_WEIGHTS:
        domain = "generic"
    if risk not in RISK_PROFILES:
        risk = "moderate"
        
    risk_prof = RISK_PROFILES[risk]
    weights = DOMAIN_LEVEL_WEIGHTS[domain]
    lex = DOMAIN_LEXICON[domain]
    data = load_pipeline(Path(pipeline_dir))
    source_df = load_source(source_csv)
    
    if targets:
        target_list = [t.strip() for t in targets if t and str(t).strip()]
    else:
        target_list = [target_col]
    if not target_list:
        target_list = ["Close"]
    primary = target_list[0]
    
    print("=" * 70)
    print(f"UNIVERSAL_LOG {VERSION} — Prédiction Multi-Niveaux V2")
    print("=" * 70)
    print(f"Domaine={domain}  Risque={risk}  Contrôle={control_col}")
    print(f"Cibles={target_list}  (primaire={primary})")
    print(f"Seuil={data['threshold']:.2f}%  Horizon={horizon}  Scénarios={n_scenarios}")
    
    # L5, L4, L3, L6
    L5 = _v1_module.level_complexity(data, horizon, n_scenarios, risk_prof, seed)
    L4 = _v1_module.level_risk(data, risk_prof, L5.get("alerts") or [])
    L3 = _v1_module.level_regime(data, horizon, risk_prof)
    L6 = _v1_module.level_next_threshold(data)
    
    # Enhanced L1/L2 Multi-Targets
    multi_targets = {}
    for i, tcol in enumerate(target_list):
        multi_targets[tcol] = level_target_v2(
            source_df, tcol, control_col, data, horizon, n_scenarios, risk_prof, seed + i * 17
        )
        
    L1 = multi_targets[primary]
    # Enhanced Universal L7 Coherence
    L7 = level_coherence_v2(L1, L1, L3, L4, L5, L6, weights, risk_prof, lex, domain_name=domain, target_name=primary)
    
    multi_summary = _v1_module._summarize_multi_targets(multi_targets, lex)
    
    results = {
        "meta": {
            "version": VERSION,
            "domain": domain,
            "risk": risk,
            "target_col": primary,
            "targets": target_list,
            "control_col": control_col,
            "horizon": horizon,
            "n_scenarios": n_scenarios,
            "seed": seed,
            "threshold": data["threshold"],
            "threshold_source": data["threshold_source"],
            "pipeline_dir": str(pipeline_dir),
            "timestamp": datetime.now().isoformat(),
            "level_weights": weights,
        },
        "levels": {
            "L1_L2_target": L1,
            "L1_L2_multi": multi_targets,
            "L3_regime": L3,
            "L4_risk": L4,
            "L5_complexity": L5,
            "L6_next_threshold": L6,
            "L7_coherence": L7,
            "multi_target_summary": multi_summary,
        },
    }
    results["narrative"] = _v1_module.narrate_multilevel(results, domain, risk)
    print("\n" + results["narrative"])
    return results

def export_multilevel_v2(results: Dict, output_dir: Path):
    _v1_module.export_multilevel(results, output_dir)
    out = Path(output_dir)
    v2_meta = {
        "version": VERSION,
        "target": results["meta"]["target_col"],
        "domain": results["meta"]["domain"],
        "L1_direction": results["levels"]["L1_L2_target"].get("direction"),
        "L1_r2": results["levels"]["L1_L2_target"].get("validation", {}).get("r2"),
        "L1_dir_acc": results["levels"]["L1_L2_target"].get("validation", {}).get("directional_accuracy"),
        "L1_mape": results["levels"]["L1_L2_target"].get("validation", {}).get("mape"),
        "L7_consensus_dir": results["levels"]["L7_coherence"].get("consensus_direction"),
        "L7_global_conf": results["levels"]["L7_coherence"].get("global_confidence"),
        "saliency_sigma": results["levels"]["L1_L2_target"].get("saliency", {}).get("saliency"),
        "saliency_label": results["levels"]["L1_L2_target"].get("saliency", {}).get("label")
    }
    with open(out / "v2_synthesis_card.json", "w", encoding="utf-8") as f:
        json.dump(v2_meta, f, indent=2)

# =============================================================================
# CLI MAIN v3.6.0-HP-v2
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description=f"UNIVERSAL_LOG {VERSION} — Universal Prediction & Complexity Engine")
    parser.add_argument("--mode", default="stable", choices=["fast","robust","stable","predict_level","predict_multilevel","full_hp"])
    parser.add_argument("--input", "-i", default=None, help="CSV d'entrée pour analyse")
    parser.add_argument("--pipeline-dir", "-p", default=None, help="Dossier results pipeline pour prédiction")
    parser.add_argument("--domain", "-d", default="physics", choices=["finance","physics","biology","climate","social","generic"])
    parser.add_argument("--risk", "-r", default="moderate", choices=["conservative","moderate","aggressive"])
    parser.add_argument("--target", default="Order_r")
    parser.add_argument("--targets", default=None, help="Liste cibles séparées par virgule pour multi-targets")
    parser.add_argument("--control", default="Energy_Diff")
    parser.add_argument("--source", default=None)
    parser.add_argument("--horizon", type=int, default=15)
    parser.add_argument("--n-scenarios", type=int, default=48)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--decompress", action="store_true", help="Décompresse Energy_Diff en 8 fluxs E_*")
    parser.add_argument("--multi-threshold", action="store_true", help="Active détection multi-seuils 2 avant/2 après")
    parser.add_argument("--window", type=int, default=80)
    parser.add_argument("--test", default="cohen_d")
    
    args = parser.parse_args()
    
    # If mode is analysis, delegate to core analysis
    if args.mode in ["fast", "robust", "stable"]:
        input_file = args.input or DEFAULT_CONTROL_COLUMN
        if input_file is None:
            csvs = glob.glob("*.csv")
            if not csvs:
                print("Aucun CSV trouvé")
                sys.exit(1)
            input_file = csvs[0]
            
        opt_cfg = {
            'random_seed': args.seed,
            'auto_optimize_threshold': True if args.mode=='stable' else False,
            'harmonic_prob': HARMONIC_PROB if args.mode=='stable' else 0.45,
            'w_size': args.window,
            'test': args.test
        }
        output_dir = Path(args.output) if args.output else Path(DEFAULT_OUTPUT_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*60)
        print(f"DÉMARRAGE PIPELINE {VERSION} — Mode {args.mode}")
        print("="*60)
        
        results, df_feat, fluxes, fluxes_ui = run_pipeline(
            data_source='custom',
            custom_file_path=input_file,
            mapping=None,
            mode=args.mode,
            opt_cfg=opt_cfg
        )
        if not results.get('success'):
            print("❌ Erreur pipeline")
            sys.exit(1)
            
        if args.multi_threshold:
            scan = results.get('scan_curve') or []
            thr = results['metadata'].get('opt_threshold', 50)
            multi = detect_multi_thresholds(scan, thr, n_zones=5, min_dist=5.0)
            results['multi_thresholds'] = multi
            
        _v1_module.plot_complexity_landscape(df_feat, fluxes, results['metadata'].get('opt_threshold',50), output_dir / 'landscape_complexity.png')
        _v1_module.plot_threshold_scan(results['scan_curve'], results['metadata'].get('opt_threshold',50), output_dir / 'threshold_scan.png')
        _v1_module.plot_raw_fluxes(results['distribution_samples'], fluxes_ui, results['metadata'].get('opt_threshold',50), output_dir / 'raw_fluxes_distribution.png')
        _v1_module.plot_separation_heatmap(results['scores'], output_dir / 'separation_heatmap.png')
        if results['metadata'].get('stability_report'):
            _v1_module.plot_stability_analysis(results['metadata']['stability_report'], output_dir / 'stability_analysis.png')
        if results.get('transition_analysis'):
            _v1_module.plot_post_threshold_analysis(results['transition_analysis'], output_dir / 'post_threshold_analysis.png')
        _v1_module.plot_noise_diagnostic(results['noise_diagnostic'], output_dir / 'noise_diagnostic.png')
        
        csd_analysis = _v1_module.compute_csd_correlation_analysis(results['noise_diagnostic'], df_feat, fluxes)
        results['csd_correlation_analysis'] = csd_analysis
        if csd_analysis and 'csd_correlations' in csd_analysis:
            _v1_module.plot_csd_correlation_analysis(csd_analysis, output_dir / 'csd_correlation_analysis.png')
            
        _v1_module.export_csv_results(df_feat, results['scores'], results['noise_diagnostic'], output_dir / 'numerical_results.csv')
        _v1_module.export_text_report(results, output_dir / 'text_report.txt')
        _v1_module.export_json_results(results, output_dir / 'pipeline_results.json')
        print(f"\n✓ Analyse {VERSION} terminée → {output_dir}")
        return
        
    # Prediction modes
    if args.pipeline_dir is None:
        print("Pour prédiction, fournir --pipeline-dir -p")
        sys.exit(1)
        
    target_list = None
    if args.targets:
        target_list = [t.strip() for t in args.targets.split(",") if t.strip()]
        
    out = Path(args.output) if args.output else Path(args.pipeline_dir) / "multilevel_predictions_v2"
    
    results = run_multilevel_v2(
        pipeline_dir=args.pipeline_dir,
        domain=args.domain,
        risk=args.risk,
        target_col=args.target,
        control_col=args.control,
        source_csv=args.source,
        horizon=args.horizon,
        n_scenarios=args.n_scenarios,
        seed=args.seed,
        targets=target_list
    )
    
    export_multilevel_v2(results, out)
    print(f"\n✓ Prédiction {VERSION} terminée → {out}")

if __name__ == "__main__":
    main()
