"""Ten reproducible statistical/ML demonstrations on generated synthetic data.

All numbers are synthetic and are intended for education and software testing,
not for real insurance pricing, underwriting, reserving, investment, or regulatory use.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from scipy.optimize import minimize
from scipy.stats import genpareto
from sklearn.covariance import LedoitWolf
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingRegressor, IsolationForest, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, PoissonRegressor, TweedieRegressor
from sklearn.metrics import (
    adjusted_rand_score,
    mean_absolute_error,
    mean_poisson_deviance,
    mean_squared_error,
    mean_tweedie_deviance,
    roc_auc_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

SEED = 42


def _insurance_synthetic(n: int = 900, seed: int = SEED) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return synthetic risk features, count, severity, exposure, and pure premium."""
    rng = np.random.default_rng(seed)
    age = rng.uniform(18.0, 85.0, n)
    vehicle_age = rng.uniform(0.0, 20.0, n)
    region_risk = rng.integers(0, 3, n).astype(float)
    exposure = rng.uniform(0.25, 1.0, n)
    x = np.column_stack((age / 100.0, vehicle_age / 20.0, region_risk / 2.0, exposure))
    log_frequency = -1.55 + 0.95 * (1.0 - age / 85.0) + 0.45 * vehicle_age / 20.0 + 0.25 * region_risk / 2.0
    frequency_rate = np.exp(log_frequency) * exposure
    counts = rng.poisson(frequency_rate).astype(int)
    individual_severity = rng.lognormal(mean=7.4 + 0.18 * region_risk + 0.006 * (age - 45), sigma=0.45, size=n)
    aggregate_loss = counts * individual_severity
    pure_premium = aggregate_loss / np.maximum(exposure, 0.05)
    return x, counts, individual_severity, exposure, pure_premium


def run_tweedie_pure_premium(seed: int = SEED) -> dict[str, Any]:
    """1. Tweedie GLM for non-negative, zero-heavy aggregate pure premium."""
    x, _, _, _, y = _insurance_synthetic(seed=seed)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model = TweedieRegressor(power=1.5, alpha=0.1, max_iter=2000, link="log")
    model.fit(x_train, y_train)
    pred = np.maximum(model.predict(x_test), 1e-8)
    return {"model": "Tweedie GLM — pure premium", "metrics": {
        "test_mean_absolute_error": float(mean_absolute_error(y_test, pred)),
        "test_mean_tweedie_deviance": float(mean_tweedie_deviance(y_test, pred, power=1.5)),
        "n_test": int(len(y_test)),
    }}


def run_poisson_claim_frequency(seed: int = SEED) -> dict[str, Any]:
    """2. Poisson regression for synthetic claim counts with exposure included as a feature."""
    x, counts, _, _, _ = _insurance_synthetic(seed=seed + 1)
    x_train, x_test, y_train, y_test = train_test_split(x, counts, test_size=0.25, random_state=seed)
    model = make_pipeline(StandardScaler(), PoissonRegressor(alpha=0.05, max_iter=1000))
    model.fit(x_train, y_train)
    pred = np.maximum(model.predict(x_test), 1e-8)
    return {"model": "Poisson regression — claim frequency", "metrics": {
        "test_mean_poisson_deviance": float(mean_poisson_deviance(y_test, pred)),
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "n_test": int(len(y_test)),
    }}


def run_logistic_claim_risk(seed: int = SEED) -> dict[str, Any]:
    """3. Logistic regression for whether a synthetic policy has one or more claims."""
    x, counts, _, _, _ = _insurance_synthetic(seed=seed + 2)
    y = (counts > 0).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1500, random_state=seed))
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    return {"model": "Logistic regression — claim occurrence", "metrics": {
        "test_roc_auc": float(roc_auc_score(y_test, probability)),
        "test_mae_probability": float(mean_absolute_error(y_test, probability)),
        "n_test": int(len(y_test)),
    }}


def run_random_forest_severity(seed: int = SEED) -> dict[str, Any]:
    """4. Random forest regression for synthetic positive claim severity."""
    x, counts, severity, _, _ = _insurance_synthetic(n=1500, seed=seed + 3)
    selected = counts > 0
    x, y = x[selected], severity[selected]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model = RandomForestRegressor(n_estimators=100, min_samples_leaf=4, random_state=seed, n_jobs=1)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"model": "Random forest — claim severity", "metrics": {
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "n_test": int(len(y_test)),
    }}


def run_quantile_reserving(seed: int = SEED) -> dict[str, Any]:
    """5. Gradient boosting quantile regression for a synthetic upper loss quantile."""
    x, _, _, _, y = _insurance_synthetic(n=1100, seed=seed + 4)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model = GradientBoostingRegressor(loss="quantile", alpha=0.90, n_estimators=70, max_depth=2, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"model": "Gradient boosting — 90th percentile", "metrics": {
        "test_pinball_loss": float(np.mean(np.maximum(0.90 * (y_test - pred), (0.90 - 1.0) * (y_test - pred)))),
        "empirical_test_coverage": float(np.mean(y_test <= pred)),
        "target_quantile": 0.90,
        "n_test": int(len(y_test)),
    }}


def run_isolation_forest(seed: int = SEED) -> dict[str, Any]:
    """6. Isolation Forest for synthetic anomaly detection."""
    rng = np.random.default_rng(seed + 5)
    normal = rng.normal(0.0, 1.0, size=(500, 4))
    anomalies = rng.normal(4.2, 0.7, size=(30, 4))
    x = np.vstack((normal, anomalies))
    y = np.r_[np.zeros(len(normal), dtype=int), np.ones(len(anomalies), dtype=int)]
    indices = rng.permutation(len(y))
    x, y = x[indices], y[indices]
    x_train, x_test, _, y_test = train_test_split(x, y, test_size=0.30, random_state=seed, stratify=y)
    model = IsolationForest(contamination=0.055, random_state=seed, n_estimators=150)
    model.fit(x_train)
    predicted_anomaly = (model.predict(x_test) == -1).astype(int)
    true_positive = int(np.sum((predicted_anomaly == 1) & (y_test == 1)))
    precision = true_positive / max(int(np.sum(predicted_anomaly == 1)), 1)
    recall = true_positive / max(int(np.sum(y_test == 1)), 1)
    return {"model": "Isolation Forest — anomaly screening", "metrics": {
        "test_anomaly_precision": float(precision),
        "test_anomaly_recall": float(recall),
        "n_test": int(len(y_test)),
    }}


def run_gmm_regimes(seed: int = SEED) -> dict[str, Any]:
    """7. Gaussian mixture segmentation for two synthetic operating regimes."""
    rng = np.random.default_rng(seed + 6)
    labels = rng.integers(0, 2, size=700)
    centers = np.array([[-1.8, -0.8, 0.5], [1.8, 0.9, -0.5]])
    x = centers[labels] + rng.normal(0, 0.65, size=(len(labels), 3))
    x_train, x_test, _, y_test = train_test_split(x, labels, test_size=0.25, random_state=seed, stratify=labels)
    model = make_pipeline(StandardScaler(), GaussianMixture(n_components=2, covariance_type="full", random_state=seed, n_init=3))
    model.fit(x_train)
    predicted = model.predict(x_test)
    return {"model": "Gaussian mixture — regime segmentation", "metrics": {
        "test_adjusted_rand_index": float(adjusted_rand_score(y_test, predicted)),
        "n_components": 2,
        "n_test": int(len(y_test)),
    }}


def run_evt_tail_model(seed: int = SEED) -> dict[str, Any]:
    """8. Peaks-over-threshold Generalized Pareto fit on synthetic heavy-tail losses."""
    rng = np.random.default_rng(seed + 7)
    synthetic_losses = genpareto.rvs(c=0.22, loc=0.0, scale=100.0, size=2500, random_state=rng)
    threshold_probability = 0.85
    threshold = float(np.quantile(synthetic_losses, threshold_probability))
    exceedances = synthetic_losses[synthetic_losses > threshold] - threshold
    shape, loc, scale = genpareto.fit(exceedances, floc=0.0)
    conditional_tail_probability = (0.99 - threshold_probability) / (1.0 - threshold_probability)
    var_99 = threshold + float(genpareto.ppf(conditional_tail_probability, c=shape, loc=0.0, scale=scale))
    return {"model": "Extreme Value Theory — POT/GPD tail", "metrics": {
        "threshold": threshold,
        "exceedance_count": int(len(exceedances)),
        "estimated_shape": float(shape),
        "estimated_scale": float(scale),
        "synthetic_var_99": float(var_99),
    }}


def run_min_variance_portfolio(seed: int = SEED) -> dict[str, Any]:
    """9. Long-only minimum-variance portfolio using Ledoit-Wolf covariance shrinkage."""
    rng = np.random.default_rng(seed + 8)
    vols = np.array([0.010, 0.014, 0.019, 0.024])
    corr = np.array([[1.0, .25, .18, .12], [.25, 1.0, .31, .16], [.18, .31, 1.0, .28], [.12, .16, .28, 1.0]])
    covariance = np.outer(vols, vols) * corr
    means = np.array([0.00025, 0.00035, 0.00045, 0.00055])
    returns = rng.multivariate_normal(means, covariance, size=900)
    x_train, _ = train_test_split(returns, test_size=0.25, random_state=seed, shuffle=False)
    cov = LedoitWolf().fit(x_train).covariance_
    n_assets = cov.shape[0]
    objective = lambda w: float(w @ cov @ w)
    result = minimize(objective, np.full(n_assets, 1 / n_assets), method="SLSQP", bounds=[(0.0, 1.0)] * n_assets,
                      constraints=[{"type": "eq", "fun": lambda w: float(np.sum(w) - 1.0)}],
                      options={"maxiter": 1000, "ftol": 1e-12})
    if not result.success:
        raise RuntimeError(f"Portfolio optimizer failed: {result.message}")
    weights = np.clip(result.x, 0.0, 1.0)
    weights = weights / weights.sum()
    annual_volatility = float(np.sqrt(weights @ cov @ weights * 252.0))
    annualized_training_mean = float(weights @ np.mean(x_train, axis=0) * 252.0)
    return {"model": "Minimum-variance portfolio — shrinkage covariance", "metrics": {
        "weights": [float(w) for w in weights],
        "weight_sum": float(np.sum(weights)),
        "annualized_volatility_estimate": annual_volatility,
        "annualized_in_sample_mean_estimate": annualized_training_mean,
        "n_assets": int(n_assets),
    }}


def run_pca_structure(seed: int = SEED) -> dict[str, Any]:
    """10. PCA for dimensionality-reduction diagnostics on synthetic factors."""
    rng = np.random.default_rng(seed + 9)
    latent = rng.normal(size=(650, 4))
    loadings = rng.normal(size=(4, 14))
    x = latent @ loadings + rng.normal(0.0, 0.35, size=(650, 14))
    x_train, x_test = train_test_split(x, test_size=0.25, random_state=seed)
    scaler = StandardScaler().fit(x_train)
    x_train_scaled, x_test_scaled = scaler.transform(x_train), scaler.transform(x_test)
    pca = PCA(n_components=0.90, svd_solver="full", random_state=seed).fit(x_train_scaled)
    reduced = pca.transform(x_test_scaled)
    reconstructed = pca.inverse_transform(reduced)
    return {"model": "PCA — dimensionality reduction", "metrics": {
        "input_features": int(x.shape[1]),
        "components_for_90pct_variance": int(pca.n_components_),
        "explained_variance_ratio_sum": float(np.sum(pca.explained_variance_ratio_)),
        "test_reconstruction_mse": float(mean_squared_error(x_test_scaled, reconstructed)),
        "n_test": int(len(x_test)),
    }}


def run_all_models(seed: int = SEED) -> list[dict[str, Any]]:
    """Run ten synthetic demonstrations and return JSON-serializable summaries."""
    runners = [
        run_tweedie_pure_premium,
        run_poisson_claim_frequency,
        run_logistic_claim_risk,
        run_random_forest_severity,
        run_quantile_reserving,
        run_isolation_forest,
        run_gmm_regimes,
        run_evt_tail_model,
        run_min_variance_portfolio,
        run_pca_structure,
    ]
    results = [runner(seed=seed) for runner in runners]
    if len(results) != 10 or any("model" not in item or "metrics" not in item for item in results):
        raise RuntimeError("Unexpected research model output structure")
    return results


if __name__ == "__main__":
    import json
    print(json.dumps(run_all_models(), indent=2))
