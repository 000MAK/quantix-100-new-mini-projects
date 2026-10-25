"""Compare two supervised-learning baselines on scikit-learn's Wine dataset.

Educational example only. The preprocessing pipeline is fit on training data
only; the held-out test split is used for the final comparison.
"""
from __future__ import annotations

from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def main() -> None:
    dataset = load_wine()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=0.20,
        random_state=42,
        stratify=dataset.target,
    )

    models = {
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=3000, random_state=42),
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
        ),
    }

    print("Wine dataset: supervised classification demo")
    print(f"Train samples: {len(y_train)} | Test samples: {len(y_test)}")
    print("Metrics are calculated on the same held-out test split.\n")

    for name, model in models.items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        print(f"=== {name} ===")
        print(f"Balanced accuracy: {balanced_accuracy_score(y_test, predictions):.3f}")
        print(f"Macro-F1:          {f1_score(y_test, predictions, average='macro'):.3f}")
        print(
            classification_report(
                y_test,
                predictions,
                labels=list(range(len(dataset.target_names))),
                target_names=list(dataset.target_names),
                zero_division=0,
            )
        )


if __name__ == "__main__":
    main()
