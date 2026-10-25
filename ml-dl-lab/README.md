# Quantix Applied Statistics, Machine Learning & Deep Learning Lab

A reproducible portfolio of statistical modeling, actuarial-risk methods, online-data benchmarks, computer vision, and audio classification.

**Data policy:** the new online experiments retrieve public datasets at runtime. Dataset files and model weights are not committed to this repository. Attribution, license notes, URLs, and caveats are documented in the repository-level ONLINE_DATA_SOURCES.md.

**Scope:** independent research and educational demonstrations. These projects are not certified actuarial, regulatory, medical, investment, or production decision systems. Results on public benchmark datasets do not establish business performance.

## Twenty statistical and machine-learning experiments

Run the combined suite. It downloads UCI data on first use and caches the archives outside the repository:

    python -m pip install -r ml-dl-lab/requirements-online.txt
    python ml-dl-lab/run_20_models.py --output results/online_model_report.json

The JSON report contains source links, license metadata, model names, and test diagnostics. The data archives are cached under ~/.cache/quantix-online-data, or in the path named by QUANTIX_DATA_CACHE.

### Models 1–10: core statistical / ML suite

| # | Model | Online source | Main diagnostic |
|---:|---|---|---|
| 1 | Logistic Regression — quality class | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 2 | Random Forest — quality class | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 3 | Histogram Gradient Boosting — quality score | UCI Wine Quality | MAE, RMSE, R² |
| 4 | Random Forest Regression — quality score | UCI Wine Quality | MAE, RMSE, R² |
| 5 | PCA — dimensionality reduction | UCI Wine Quality | 95% explained variance and reconstruction MSE |
| 6 | Gaussian Mixture Model — segmentation | UCI Wine Quality | Adjusted Rand Index versus score-derived groups |
| 7 | Isolation Forest — anomaly screening | UCI Wine Quality | Flag rate and decision-score range; no true anomaly labels are supplied |
| 8 | Poisson Regression — hourly count demand | UCI Bike Sharing | Poisson deviance and MAE, chronological holdout |
| 9 | Quantile Gradient Boosting — upper demand quantile | UCI Bike Sharing | Pinball loss and empirical coverage, chronological holdout |
| 10 | Peaks-over-Threshold / Generalized Pareto | UCI Bike Sharing | Tail-quantile and exceedance diagnostics; not insurance loss data |

### Models 11–20: additional model comparisons

| # | Model | Online source | Main diagnostic |
|---:|---|---|---|
| 11 | Support Vector Classifier | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 12 | K-Nearest Neighbors Classifier | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 13 | Extra Trees Classifier | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 14 | Gaussian Naive Bayes | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 15 | Linear Discriminant Analysis | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 16 | AdaBoost Classifier | UCI Wine Quality | Accuracy, macro-F1, ROC-AUC |
| 17 | Ridge Regression | UCI Wine Quality | MAE, RMSE, R² |
| 18 | Support Vector Regression | UCI Wine Quality | MAE, RMSE, R² |
| 19 | K-Nearest Neighbors Regression | UCI Wine Quality | MAE, RMSE, R² |
| 20 | Extra Trees — hourly count forecast | UCI Bike Sharing | MAE, RMSE, R², chronological holdout |

Wine Quality features support classification, regression, anomaly screening, and dimensionality diagnostics. The label rules are documented in code. Bike Sharing supports count-demand modeling and an extreme-value illustration. None of these public datasets represents real insurance claims; actuarial concepts in this collection are methods demonstrations, not premium or reserve calculations.

## Deep learning project 21: online bean-leaf image classification

Source: [AI-Lab-Makerere/beans on Hugging Face](https://huggingface.co/datasets/AI-Lab-Makerere/beans).

The script downloads the public three-class image dataset at run time, resizes images, trains a small 2-D CNN, selects the best checkpoint by validation loss, and evaluates it on the dataset's test split. Images and weights are not committed.

    python ml-dl-lab/vision_beans_cnn.py --epochs 3 --max-train 800 --output results/beans_cnn.json

The Hugging Face dataset card metadata declares MIT, but its licensing-information section says the original source requires more detail. The demo does not redistribute images; review the original collection and its terms before commercial adaptation. This educational classifier is not a validated plant-disease diagnostic service.

## Deep learning project 22: online spoken-digit audio classification

Source: [Jakobovski/free-spoken-digit-dataset](https://github.com/Jakobovski/free-spoken-digit-dataset), pinned to tag v1.0.10 in the downloader. The source repository states that recording indices 0–4 are the test split and 5–49 are the training split and lists CC BY-SA 4.0.

The script downloads the tagged archive, extracts WAV files only into a local cache, converts recordings to fixed-length waveforms, trains a small 1-D CNN, and reports held-out test metrics. It does not capture microphone audio or upload recordings.

    python ml-dl-lab/audio_fsdd_cnn.py --epochs 5 --max-train 1200 --output results/audio_cnn.json

The official split may contain the same speakers in train and test, so this demo does not claim speaker-independent recognition. The downloaded recordings are not committed or redistributed.

## Existing compact demos

- ml_classification.py — Logistic Regression and Random Forest on scikit-learn's bundled Wine dataset.
- clustering_demo.py — K-Means on reproducibly generated synthetic data.
- dl_digits_classifier.py — PyTorch classifier using scikit-learn's bundled 8×8 Digits dataset.
- huggingface_sentiment.py — optional English sentiment inference using an external pretrained model. See ONLINE_DATA_SOURCES.md and OPEN_SOURCE_REFERENCES.md before commercial reuse.

These provide smaller offline/educational options, separate from the new online-data workflow.

## Tests

Install research dependencies and run all lab tests without internet dataset downloads:

    python -m pip install -r ml-dl-lab/requirements-online.txt
    python -m unittest discover -s ml-dl-lab -p 'test_*.py' -v

The tests inject small local DataFrames into all twenty statistical/ML runners, check neural-network output shapes, and create temporary local WAV files to test the audio split/loader. They do not download Beans, UCI archives, FSDD, or pretrained model weights.

## Reproducibility and safety

- Fixed random seeds are available in the scripts.
- The Wine and Bike downloads are fetched from the official UCI archive URLs over HTTPS and are size-limited/cached outside the repo.
- FSDD downloads use a version tag and an archive size limit; only expected WAV files are extracted, with path traversal names rejected.
- The Beans dataset is downloaded by Hugging Face Datasets; use its upstream source and license notes before reuse.
- No dataset files, trained model weights, access tokens, or client data are committed.
- Time-ordered bike-demand models use chronological holdouts; random-split wine models use held-out test splits.
- Review data provenance, leakage, class balance, calibration, and baseline performance before extending these experiments to a new domain.

## Attribution

Read the top-level ONLINE_DATA_SOURCES.md for dataset URLs, original creator/source notes, dataset licenses, dependency licenses, and reuse caveats. The repository code is MIT licensed, but that does not change the licenses of external datasets or dependencies.
