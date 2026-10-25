# Applied Machine Learning & Deep Learning Lab

A small, reproducible learning track that complements the Quantix command-line utilities. It contains three independent examples using built-in or synthetic datasets; no private data or external dataset download is required.

## Projects

### 1. Supervised classification — `ml_classification.py`

Compares Logistic Regression and Random Forest in scikit-learn on the built-in Wine dataset. Preprocessing is placed inside a pipeline to avoid fitting the scaler on the test set. Reports balanced accuracy, macro-F1, and a classification report.

### 2. Unsupervised clustering — `clustering_demo.py`

Runs K-Means on reproducibly generated synthetic blobs. Reports silhouette score and adjusted Rand index. The known synthetic labels are used only to evaluate the clustering, not as model inputs.

### 3. Neural network image classification — `dl_digits_classifier.py`

Trains a small PyTorch multilayer perceptron on scikit-learn's built-in 8×8 handwritten-digits dataset. Uses train/validation/test splits, a fixed random seed, and validation-loss-based early stopping.

## Requirements

- Python 3.10+
- scikit-learn
- NumPy
- PyTorch (for the deep-learning example)

The core Quantix CLI utilities remain separate and are designed to use the Python standard library. These ML/DL demos need the additional packages listed in `requirements.txt`.

## Run locally

From the repository root, create and activate a virtual environment, then install the lab dependencies:

    python -m venv .venv
    # Windows PowerShell:
    .venv\Scripts\Activate.ps1
    # macOS/Linux:
    # source .venv/bin/activate
    python -m pip install -r ml-dl-lab/requirements.txt

Run any example from the repository root:

    python ml-dl-lab/ml_classification.py
    python ml-dl-lab/clustering_demo.py
    python ml-dl-lab/dl_digits_classifier.py

The neural-network example runs on CPU by default and does not download pretrained weights.

## Scope and limitations

These are educational baselines, not production systems. Results depend on the dataset, split, dependencies, and random seed. The Wine and Digits datasets are small built-in teaching datasets; performance on them does not imply generalization to real-world data. Review the code and environment before adapting examples to another task.
