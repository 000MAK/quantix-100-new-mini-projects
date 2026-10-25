# Applied Machine Learning & Deep Learning Lab

A small learning track that complements the Quantix command-line utilities. It contains original demonstration code using built-in or synthetic datasets, plus one optional NLP example that uses a third-party pretrained model with explicit attribution.

## Projects

### 1. Supervised classification — ml_classification.py

Compares Logistic Regression and Random Forest in scikit-learn on the built-in Wine dataset. Preprocessing is placed inside a pipeline to avoid fitting the scaler on the test set. Reports balanced accuracy, macro-F1, and a classification report.

### 2. Unsupervised clustering — clustering_demo.py

Runs K-Means on reproducibly generated synthetic blobs. Reports silhouette score and adjusted Rand index. The known synthetic labels are used only to evaluate the clustering, not as model inputs.

### 3. Neural network image classification — dl_digits_classifier.py

Trains a small PyTorch multilayer perceptron on scikit-learn's built-in 8×8 handwritten-digits dataset. Uses train/validation/test splits, a fixed random seed, and validation-loss-based early stopping.

### 4. Hugging Face NLP — huggingface_sentiment.py

Runs English positive/negative sentiment inference with DistilBERT fine-tuned on SST-2 via the Transformers pipeline API. The small CLI wrapper is original; the third-party model is linked and attributed in OPEN_SOURCE_REFERENCES.md. The script does not upload or mirror model weights.

The model is English-focused. Its output score is not a calibrated real-world probability and should not be used as a general-purpose moderation or high-stakes decision system.

## Requirements

- Python 3.10+
- scikit-learn
- NumPy
- PyTorch for the deep-learning examples
- Transformers for the optional Hugging Face example

The core Quantix CLI utilities remain separate and use the Python standard library. These ML/DL demos need additional packages listed in the requirements files.

## Run locally

From the repository root, create and activate a virtual environment.

Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

macOS/Linux:

    python -m venv .venv
    source .venv/bin/activate

Install dependencies for the built-in/synthetic examples:

    python -m pip install -r ml-dl-lab/requirements.txt

Run one of those examples from the repository root:

    python ml-dl-lab/ml_classification.py
    python ml-dl-lab/clustering_demo.py
    python ml-dl-lab/dl_digits_classifier.py

For the optional Hugging Face sentiment example, install its additional requirements:

    python -m pip install -r ml-dl-lab/requirements-hf.txt

Then run it with a short English sentence:

    python ml-dl-lab/huggingface_sentiment.py "The explanation was clear and useful."

The first run downloads the model from Hugging Face and caches it locally. The model then runs through the local Transformers pipeline; it is not an API call to a hosted inference endpoint. Internet access is needed for the initial download unless the model is already cached.

## Third-party attribution

See [OPEN_SOURCE_REFERENCES.md](../OPEN_SOURCE_REFERENCES.md) for model origin, listed license, libraries, and further-reading links. Third-party assets are not presented as original work, and no model weights are bundled in this repository.

## Scope and limitations

These are educational baselines, not production systems. Results depend on data, splits, dependency versions, and random seeds. Small teaching datasets do not establish real-world generalization. Check each upstream model card, license, and applicable notices before adapting an asset, especially for commercial use.
