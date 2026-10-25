from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier, ExtraTreesRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error, mean_squared_error, r2_score, roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR

from online_research_models import SEED, _bike_features, _chronological_split, _wine_features


def _classification_result(name: str, x: pd.DataFrame, y: pd.Series, model: Any, seed: int) -> dict[str, Any]:
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed, stratify=y)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    if hasattr(model, "predict_proba"):
        score = model.predict_proba(x_test)[:, 1]
    elif hasattr(model, "decision_function"):
        score = model.decision_function(x_test)
    else:
        score = pred
    return {"model": name, "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_accuracy": float(accuracy_score(y_test, pred)),
        "test_macro_f1": float(f1_score(y_test, pred, average="macro")),
        "test_roc_auc": float(roc_auc_score(y_test, score)),
        "n_test": int(len(y_test)),
    }}


def _regression_result(name: str, x: pd.DataFrame, y: pd.Series, model: Any, seed: int) -> dict[str, Any]:
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=seed)
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    return {"model": name, "dataset": "UCI Wine Quality (online)", "metrics": {
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "test_r2": float(r2_score(y_test, pred)),
        "n_test": int(len(y_test)),
    }}


def run_additional_models(wine: pd.DataFrame, bike_hour: pd.DataFrame, seed: int = SEED) -> list[dict[str, Any]]:
    """Run models 11-20, complementing the first ten in online_research_models.py."""
    x, quality = _wine_features(wine)
    y_binary = (quality >= 7).astype(int)
    output: list[dict[str, Any]] = []

    output.append(_classification_result(
        "11 Support Vector Classifier — wine quality class", x, y_binary,
        make_pipeline(StandardScaler(), SVC(C=1.0, kernel="rbf", class_weight="balanced", probability=True, random_state=seed)), seed))
    output.append(_classification_result(
        "12 K-Nearest Neighbors — wine quality class", x, y_binary,
        make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=11, weights="distance")), seed))
    output.append(_classification_result(
        "13 Extra Trees — wine quality class", x, y_binary,
        ExtraTreesClassifier(n_estimators=180, min_samples_leaf=2, class_weight="balanced", n_jobs=1, random_state=seed), seed))
    output.append(_classification_result(
        "14 Gaussian Naive Bayes — wine quality class", x, y_binary,
        make_pipeline(StandardScaler(), GaussianNB()), seed))
    output.append(_classification_result(
        "15 Linear Discriminant Analysis — wine quality class", x, y_binary,
        make_pipeline(StandardScaler(), LinearDiscriminantAnalysis()), seed))
    output.append(_classification_result(
        "16 AdaBoost — wine quality class", x, y_binary,
        AdaBoostClassifier(n_estimators=90, learning_rate=0.5, random_state=seed), seed))

    output.append(_regression_result(
        "17 Ridge Regression — wine quality score", x, quality,
        make_pipeline(StandardScaler(), Ridge(alpha=2.0)), seed))
    output.append(_regression_result(
        "18 Support Vector Regression — wine quality score", x, quality,
        make_pipeline(StandardScaler(), SVR(C=3.0, epsilon=0.15, kernel="rbf")), seed))
    output.append(_regression_result(
        "19 K-Nearest Neighbors — wine quality regression", x, quality,
        make_pipeline(StandardScaler(), KNeighborsRegressor(n_neighbors=15, weights="distance")), seed))

    bike_x, bike_y, bike_dates = _bike_features(bike_hour)
    x_train, x_test, y_train, y_test = _chronological_split(bike_x, bike_y, bike_dates)
    model = ExtraTreesRegressor(n_estimators=140, min_samples_leaf=2, n_jobs=1, random_state=seed)
    model.fit(x_train, y_train)
    pred = np.maximum(model.predict(x_test), 0.0)
    output.append({"model": "20 Extra Trees — hourly bike demand forecast", "dataset": "UCI Bike Sharing hourly records (online)", "metrics": {
        "test_mae": float(mean_absolute_error(y_test, pred)),
        "test_rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "test_r2": float(r2_score(y_test, pred)),
        "n_test": int(len(y_test)),
        "note": "Chronological holdout; historical time effects may not generalize to future periods.",
    }})
    if len(output) != 10:
        raise RuntimeError("Expected ten additional model experiments.")
    return output
