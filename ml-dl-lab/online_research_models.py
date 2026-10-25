"""Run ten ML/statistical model demonstrations on openly licensed online datasets.

Data are downloaded at run time from UCI. Nothing from these datasets is committed
to the repository. See ONLINE_DATA_SOURCES.md for attribution and licensing.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import tempfile
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import genpareto
from sklearn.covariance import LedoitWolf
from sklearn.decomposition import PCA
from sklearn.ensemble import (
    HistGradientBoostingRegressor,
    IsolationForest,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LogisticRegression, PoissonRegressor
from sklearn.metrics import (
    accuracy_score,
    adjusted_rand_score,
    f1_score,
    mean_absolute_error,
    mean_poisson_deviance,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

WINE_URL = "https://archive.ics.uci.edu/static/public/186/wine+quality.zip"
BIKE_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"
WINE_SOURCE = "UCI Machine Learning Repository: Wine Quality, DOI 10.24432/C56S3T, CC BY 4.0"
BIKE_SOURCE = "UCI Machine Learning Repository: Bike Sharing, DOI 10.24432/C5W894, CC BY 4.0"
SEED = 42
MAX_DOWNLOAD_BYTES = 20_000_000


def _cache_dir() -> Path:
    override = os.environ.get("QUANTIX_DATA_CACHE")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "quantix-online-data"


def _download_zip(url: str, filename: str, *, max_bytes: int = MAX_DOWNLOAD_BYTES) -> Path:
    """Download a fixed HTTPS dataset archive safely into a user cache."""
    if not url.startswith("https://archive.ics.uci.edu/"):
        raise ValueError("Only the configured official UCI HTTPS dataset hosts are allowed.")
    cache = _cache_dir()
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / filename
    if destination.exists():
        try:
            if destination.stat().st_size <= max_bytes and zipfile.is_zipfile(destination):
                return destination
        except OSError:
            pass
        destination.unlink(missing_ok=True)

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Quantix-Research-Lab/1.0 (open dataset download)"},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        advertised = response.headers.get("Content-Length")
        if advertised and int(advertised) > max_bytes:
            raise ValueError(f"Dataset archive is larger than the configured limit: {advertised} bytes")
        payload = response.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise ValueError("Dataset archive exceeded the configured download size limit.")
    if not zipfile.is_zipfile(io.BytesIO(payload)):
        raise ValueError("The source did not return a valid ZIP archive; refusing to cache it.")

    with tempfile.NamedTemporaryFile(dir=cache, prefix=filename + ".", suffix=".tmp", delete=False) as tmp:
        temporary = Path(tmp.name)
        tmp.write(payload)
    temporary.replace(destination)

    manifest_path = cache / "download_manifest.json"
    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            manifest = {}
    manifest[filename] = {
        "source_url": url,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return destination


def _member_name(archive: zipfile.ZipFile, wanted: str) -> str:
    candidates = [name for name in archive.namelist() if Path(name).name.lower() == wanted.lower()]
    if len(candidates) != 1:
        raise ValueError(f"Expected one {wanted} member in archive; found {len(candidates)}.")
    return candidates[0]


def load_wine_quality() -> pd.DataFrame:
    """Load and combine the official red/white Wine Quality tables."""
    archive_path = _download_zip(WINE_URL, "uci_wine_quality.zip")
    with zipfile.ZipFile(archive_path) as archive:
        red_name = _member_name(archive, "winequality-red.csv")
        white_name = _member_name(archive, "winequality-white.csv")
        red = pd.read_csv(io.BytesIO(archive.read(red_name)), sep=";")
        white = pd.read_csv(io.BytesIO(archive.read(white_name)), sep=";")
    for frame, color in ((red, "red"), (white, "white")):
        frame.columns = [str(col).strip().lower().replace(" ", "_") for col in frame.columns]
        frame["wine_color"] = color
    result = pd.concat([red, white], ignore_index=True)
    if "quality" not in result or len(result) < 1000:
        raise ValueError("Wine Quality download does not match the expected dataset schema.")
    return result


def load_bike_sharing() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load hourly and daily records from UCI Bike Sharing."""
    archive_path = _download_zip(BIKE_URL, "uci_bike_sharing.zip")
    with zipfile.ZipFile(archive_path) as archive:
        hour_name = _member_name(archive, "hour.csv")
        day_name = _member_name(archive, "day.csv")
        hourly = pd.read_csv(io.BytesIO(archive.read(hour_name)))
        daily = pd.read_csv(io.BytesIO(archive.read(day_name)))
    for frame in (hourly, daily):
        frame.columns = [str(col).strip().lower() for col in frame.columns]
        if "dteday" in frame:
            frame["dteday"] = pd.to_datetime(frame["dteday"], errors="raise")
    if not {"cnt", "dteday"}.issubset(hourly.columns) or len(hourly) < 1000:
        raise ValueError("Bike Sharing hourly download does not match the expected dataset schema.")
    if not {"cnt", "dteday"}.issubset(daily.columns) or len(daily) < 300:
        raise ValueError("Bike Sharing daily download does not match the expected dataset schema.")
    return hourly.sort_values("dteday").reset_index(drop=True), daily.sort_values("dteday").reset_index(drop=True)


def _wine_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    if "quality" not in df.columns:
        raise ValueError("Wine dataframe requires a quality target column.")
    y = pd.to_numeric(df["quality"], errors="raise").astype(int)
    features = df.drop(columns=["quality"]).copy()
    features = pd.get_dummies(features, columns=[c for c in ("wine_color",) if c in features], dtype=float)
    features = features.apply(pd.to_numeric, errors="raise").astype(float)
    return features, y


def _bike_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    required = {"cnt", "dteday", "temp", "atemp", "hum", "windspeed", "season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit"}
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError("Bike dataframe missing columns: " + ", ".join(missing))
    feature_cols = ["temp", "atemp", "hum", "windspeed", "season", "yr", "mnth", "holiday", "weekday", "workingday", "weathersit"]
    if "hr" in df.columns:
        feature_cols.append("hr")
    x = df[feature_cols].copy()
    categorical = [c for c in ("season", "yr", "mnth", "hr", "holiday", "weekday", "workingday", "weathersit") if c in x]
    for col in categorical:
        x[col] = x[col].astype(str)
    x = pd.get_dummies(x, columns=categorical, dtype=float)
    y = pd.to_numeric(df["cnt"], errors="raise").astype(float)
    dates = pd.to_datetime(df["dteday"], errors="raise")
    return x.astype(float), y, dates


def _chronological_split(x: pd.DataFrame, y: pd.Series, dates: pd.Series, fraction: float = 0.20):
    order = np.argsort(pd.to_datetime(dates).to_numpy(), kind="stable")
    split_at = max(1, int(len(order) * (1.0 - fraction)))
    if split_at >= len(order):
        raise ValueError("Not enough samples for a chronological holdout split.")
    train_idx, test_idx = order[:split_at], order[split_at:]
    return x.iloc[train_idx], x.iloc[test_idx], y.iloc[train_idx], y.iloc[test_idx]


def run_logistic_wine(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, quality = _wine_features(wine)
    y = (quality >= 7).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, class_weight="balanced", random_state=seed))
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {"model": "01 Logistic Regression — wine quality class", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_accuracy": float(accuracy_score(y_test, predictions)),
        "test_macro_f1": float(f1_score(y_test, predictions, average="macro")),
        "test_roc_auc": float(roc_auc_score(y_test, probabilities)),
        "positive_class_rule": "quality >= 7",
        "n_test": int(len(y_test)),
    }}


def run_random_forest_wine(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, quality = _wine_features(wine)
    y = (quality >= 7).astype(int)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    model = RandomForestClassifier(n_estimators=220, min_samples_leaf=2, class_weight="balanced", n_jobs=1, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    prob = model.predict_proba(x_test)[:, 1]
    return {"model": "02 Random Forest — wine quality class", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_macro_f1": float(f1_score(y_test, pred, average="macro")),
        "test_roc_auc": float(roc_auc_score(y_test, prob)),
        "n_test": int(len(y_test)),
    }}


def run_gradient_boosting_quality(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, y = _wine_features(wine)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model = HistGradientBoostingRegressor(max_iter=140, learning_rate=0.07, l2_regularization=1.0, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"model": "03 Histogram Gradient Boosting — wine quality regression", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "test_r2": float(r2_score(y_test, pred)),
        "n_test": int(len(y_test)),
    }}


def run_random_forest_quality(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, y = _wine_features(wine)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model = RandomForestRegressor(n_estimators=180, min_samples_leaf=2, n_jobs=1, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"model": "04 Random Forest — wine quality regression", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "test_r2": float(r2_score(y_test, pred)),
        "n_test": int(len(y_test)),
    }}


def run_pca_wine(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, _ = _wine_features(wine)
    x_train, x_test = train_test_split(x, test_size=0.25, random_state=seed)
    scaler = StandardScaler().fit(x_train)
    train_scaled, test_scaled = scaler.transform(x_train), scaler.transform(x_test)
    pca = PCA(n_components=0.95, svd_solver="full")
    pca.fit(train_scaled)
    reconstructed = pca.inverse_transform(pca.transform(test_scaled))
    return {"model": "05 PCA — dimensionality and reconstruction", "dataset": "UCI Wine Quality (online)", "metrics": {
        "input_features": int(x.shape[1]),
        "components_for_95pct_variance": int(pca.n_components_),
        "explained_variance_ratio_sum": float(np.sum(pca.explained_variance_ratio_)),
        "test_reconstruction_mse": float(mean_squared_error(test_scaled, reconstructed)),
        "n_test": int(len(x_test)),
    }}


def run_gmm_wine(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, quality = _wine_features(wine)
    quality_group = np.select([quality <= 4, quality <= 6], [0, 1], default=2)
    x_train, x_test, group_train, group_test = train_test_split(x, quality_group, test_size=0.25, random_state=seed, stratify=quality_group)
    scaler = StandardScaler().fit(x_train)
    train_scaled, test_scaled = scaler.transform(x_train), scaler.transform(x_test)
    model = GaussianMixture(n_components=3, covariance_type="full", n_init=3, random_state=seed, reg_covar=1e-5)
    model.fit(train_scaled)
    clusters = model.predict(test_scaled)
    return {"model": "06 Gaussian Mixture — unsupervised wine segmentation", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_adjusted_rand_index_vs_quality_groups": float(adjusted_rand_score(group_test, clusters)),
        "n_components": 3,
        "n_test": int(len(x_test)),
    }}


def run_isolation_forest_wine(wine: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, _ = _wine_features(wine)
    x_train, x_test = train_test_split(x, test_size=0.25, random_state=seed)
    scaler = StandardScaler().fit(x_train)
    model = IsolationForest(contamination=0.04, n_estimators=200, random_state=seed, n_jobs=1)
    model.fit(scaler.transform(x_train))
    prediction = model.predict(scaler.transform(x_test))
    scores = model.decision_function(scaler.transform(x_test))
    return {"model": "07 Isolation Forest — anomaly screening", "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_rows_flagged_as_anomalies": int(np.sum(prediction == -1)),
        "test_rows": int(len(prediction)),
        "test_anomaly_fraction": float(np.mean(prediction == -1)),
        "minimum_decision_score": float(np.min(scores)),
        "note": "No ground-truth anomaly labels are supplied; these are unsupervised flags, not accuracy claims.",
    }}


def run_poisson_bike(bike_hour: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, y, dates = _bike_features(bike_hour)
    x_train, x_test, y_train, y_test = _chronological_split(x, y, dates)
    model = make_pipeline(StandardScaler(), PoissonRegressor(alpha=0.2, max_iter=1500))
    model.fit(x_train, y_train)
    pred = np.maximum(model.predict(x_test), 1e-8)
    return {"model": "08 Poisson Regression — hourly bike demand", "dataset": "UCI Bike Sharing hourly records (online)", "metrics": {
        "test_mean_poisson_deviance": float(mean_poisson_deviance(y_test, pred)),
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "train_end_date": str(dates.iloc[:len(x_train)].max().date()),
        "test_start_date": str(dates.iloc[len(x_train):].min().date()),
        "n_test": int(len(y_test)),
    }}


def run_quantile_bike(bike_hour: pd.DataFrame, seed: int = SEED) -> dict[str, Any]:
    x, y, dates = _bike_features(bike_hour)
    x_train, x_test, y_train, y_test = _chronological_split(x, y, dates)
    alpha = 0.90
    model = HistGradientBoostingRegressor(loss="quantile", quantile=alpha, max_iter=140, learning_rate=0.08, max_leaf_nodes=15, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    residual = y_test.to_numpy() - pred
    pinball = np.maximum(alpha * residual, (alpha - 1.0) * residual)
    return {"model": "09 Quantile Gradient Boosting — 90th-percentile demand", "dataset": "UCI Bike Sharing hourly records (online)", "metrics": {
        "target_quantile": alpha,
        "test_pinball_loss": float(np.mean(pinball)),
        "empirical_test_coverage": float(np.mean(y_test.to_numpy() <= pred)),
        "test_mae_to_observed_count": float(mean_absolute_error(y_test, pred)),
        "n_test": int(len(y_test)),
    }}


def run_evt_bike_daily(bike_day: pd.DataFrame) -> dict[str, Any]:
    """Fit a Peaks-over-Threshold GPD to the upper tail of public daily demand."""
    counts = pd.to_numeric(bike_day["cnt"], errors="raise").to_numpy(dtype=float)
    threshold_probability = 0.90
    threshold = float(np.quantile(counts, threshold_probability))
    exceedances = counts[counts > threshold] - threshold
    if len(exceedances) < 20:
        raise ValueError("Too few daily demand exceedances for a stable demonstration; require at least 20.")
    shape, loc, scale = genpareto.fit(exceedances, floc=0.0)
    unconditional_probability = 0.99
    conditional_probability = (unconditional_probability - threshold_probability) / (1.0 - threshold_probability)
    q99 = threshold + float(genpareto.ppf(conditional_probability, c=shape, loc=0.0, scale=scale))
    return {"model": "10 EVT Peaks-over-Threshold / Generalized Pareto", "dataset": "UCI Bike Sharing daily records (online)", "metrics": {
        "threshold_quantile": threshold_probability,
        "threshold_demand": threshold,
        "exceedance_count": int(len(exceedances)),
        "gpd_shape_estimate": float(shape),
        "gpd_scale_estimate": float(scale),
        "estimated_99th_percentile_daily_bike_demand": float(q99),
        "note": "This is a tail-analysis illustration on bike demand, not an insurance loss or financial risk estimate.",
    }}


def run_online_models(
    wine: pd.DataFrame | None = None,
    bike_hour: pd.DataFrame | None = None,
    bike_day: pd.DataFrame | None = None,
    seed: int = SEED,
) -> dict[str, Any]:
    """Run all ten experiments. Missing dataset arguments are fetched online."""
    if wine is None:
        wine = load_wine_quality()
    if bike_hour is None or bike_day is None:
        loaded_hour, loaded_day = load_bike_sharing()
        bike_hour = bike_hour if bike_hour is not None else loaded_hour
        bike_day = bike_day if bike_day is not None else loaded_day
    runners = [
        lambda: run_logistic_wine(wine, seed),
        lambda: run_random_forest_wine(wine, seed),
        lambda: run_gradient_boosting_quality(wine, seed),
        lambda: run_random_forest_quality(wine, seed),
        lambda: run_pca_wine(wine, seed),
        lambda: run_gmm_wine(wine, seed),
        lambda: run_isolation_forest_wine(wine, seed),
        lambda: run_poisson_bike(bike_hour, seed),
        lambda: run_quantile_bike(bike_hour, seed),
        lambda: run_evt_bike_daily(bike_day),
    ]
    results = [runner() for runner in runners]
    if len(results) != 10:
        raise RuntimeError("Expected exactly ten online-dataset model results.")
    return {
        "title": "Quantix Online Data: Ten Statistical and ML Models",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sources": [
            {"name": WINE_SOURCE, "url": "https://archive.ics.uci.edu/dataset/186/wine+quality", "license": "CC BY 4.0"},
            {"name": BIKE_SOURCE, "url": "https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset", "license": "CC BY 4.0"},
        ],
        "data_note": "Real public datasets fetched online. Reported scores are benchmark results for these datasets, not insurance/actuarial business performance.",
        "results": results,
    }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="", help="Optional JSON output path; data files are never written into the repository.")
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    report = run_online_models(seed=args.seed)
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
