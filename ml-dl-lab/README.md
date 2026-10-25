# Quantix Applied Statistics, Machine Learning & Deep Learning Lab

A reproducible research portfolio for applied statistics, actuarial-risk methods, quantitative finance, machine learning, computer vision, and audio signal classification.

**Data policy:** all new model experiments use deterministic synthetic data generated locally at runtime. They do not download, bundle, or redistribute customer datasets, market data, image collections, or audio recordings.

**Scope:** independent demonstrations for learning and engineering review. They are not certified actuarial, regulatory, medical, investment, or production decision systems. Metrics reported by the new experiments are measured on synthetic holdout sets and are not evidence of real-world predictive performance.

## Ten statistical and machine-learning models

Install dependencies from the repository root:

    python -m pip install -r ml-dl-lab/requirements-research.txt

Run all ten model demonstrations:

    python ml-dl-lab/research_models.py

| # | Model | Why it fits this portfolio | Main diagnostic |
|---:|---|---|---|
| 1 | Tweedie GLM | Zero-heavy aggregate loss / pure-premium modeling concept | MAE and Tweedie deviance |
| 2 | Poisson Regression | Claim-frequency modeling with count outcomes | Mean Poisson deviance and MAE |
| 3 | Logistic Regression | Binary claim-occurrence risk baseline | ROC-AUC and probability MAE |
| 4 | Random Forest Regression | Nonlinear severity modeling baseline | MAE and RMSE |
| 5 | Gradient Boosting Quantile Regression | Upper-quantile risk/reserving illustration | Pinball loss and empirical coverage |
| 6 | Isolation Forest | Unsupervised anomaly-screening demonstration | Precision/recall against synthetic labels |
| 7 | Gaussian Mixture Model | Regime segmentation on synthetic multivariate observations | Adjusted Rand Index |
| 8 | Peaks-over-Threshold / Generalized Pareto Distribution | Extreme-value tail modeling illustration | Fitted shape/scale and synthetic 99% tail quantile |
| 9 | Long-only Minimum-Variance Portfolio | Portfolio construction using Ledoit–Wolf covariance shrinkage | Weight constraints and estimated volatility |
| 10 | Principal Component Analysis | Dimensionality reduction and reconstruction diagnostic | Explained variance and test reconstruction MSE |

The insurance tasks use generated covariates and generated claim counts/losses. The GPD demonstration generates heavy-tailed synthetic losses. Portfolio returns are generated locally, not downloaded from an exchange. Synthetic results must not be used to price real insurance, estimate actual reserves, or recommend investments.

## Deep learning demos: vision and audio

### A. Synthetic Shape Recognition — 2-D CNN

    python ml-dl-lab/vision_shapes_cnn.py --samples 360 --epochs 8

Trains a small convolutional neural network to recognize horizontal bars, vertical bars, and diagonal shapes in procedurally generated grayscale images with noise. No image dataset or pretrained weights are downloaded.

### B. Synthetic Audio Signal Classification — 1-D CNN

    python ml-dl-lab/audio_signal_cnn.py --samples 420 --epochs 8

Trains a 1-D convolutional network to distinguish synthetic noisy low-, mid-, and high-frequency tone mixtures. The signal is generated in memory; the demo does not access a microphone, use real recordings, or infer speech, identity, health, or emotion.

Both demos use fixed random seeds and held-out test splits. Their accuracy measures learning on synthetic patterns only. They do not demonstrate performance on real-world images or recordings.

## Existing lab examples

- ml_classification.py — Logistic Regression and Random Forest using scikit-learn's bundled Wine dataset. Source and attribution notes are in ../OPEN_SOURCE_REFERENCES.md.
- clustering_demo.py — K-Means on reproducibly generated synthetic clusters.
- dl_digits_classifier.py — PyTorch MLP using scikit-learn's bundled 8×8 Digits dataset. See the attribution notes before redistributing data.
- huggingface_sentiment.py — optional English sentiment inference with an external pretrained model; requires separate dependencies and can download model files on first use. See the attribution file and upstream model card.

## Tests

From the repository root, after installing research dependencies:

    python -m unittest discover -s ml-dl-lab -p 'test_*.py' -v

These tests exercise the ten model outputs and portfolio weight constraints, validate the synthetic data shapes, and run tiny CPU smoke tests for both CNNs. No external network calls are made by these new tests.

## Reproducibility and safety

- Random seeds are explicit and can be changed in each command-line interface.
- Model metrics are calculated on held-out synthetic data.
- The code does not publish model weights or save generated training data.
- The demos do not access APIs, collect personal data, or execute client-provided code.
- Review assumptions and output quality before extending any example to real datasets.

## Attribution and licensing

- Original scripts and synthetic-data generation in this lab are released under the repository-level MIT license in ../LICENSE.
- NumPy: BSD-3-Clause; upstream license: https://github.com/numpy/numpy/blob/main/LICENSE.txt.
- SciPy: BSD-3-Clause; upstream license: https://github.com/scipy/scipy/blob/main/LICENSE.txt.
- scikit-learn: BSD-3-Clause; upstream license: https://github.com/scikit-learn/scikit-learn/blob/main/COPYING.
- PyTorch: BSD-style license; upstream license: https://github.com/pytorch/pytorch/blob/main/LICENSE.
- No external dataset, image, audio recording, or pretrained model is bundled for the new synthetic-data experiments.
- For the pre-existing Hugging Face sentiment demo, see ../OPEN_SOURCE_REFERENCES.md and the upstream model card. The pretrained model and its weights are not represented as original work.

## Suggested next step for real research

Only after the synthetic baselines are reviewed should a separate licensed dataset adapter be added. It should document data provenance, exact license/terms, input schema, an explicit train/validation/test protocol, leakage checks, calibration and baseline comparisons, and domain review. Keep synthetic demonstration metrics separate from any future real-world performance claims.
