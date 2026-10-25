# Quantix Project Portfolio

This page highlights selected Python utilities and learning projects published as independent demonstrations. They illustrate data processing, file-safety, automation, and introductory ML/DL workflows. They are not presented as paid client engagements or as a claim that every project is production-ready.

## Python utilities

### Mini CSV Cleaner
Cleans whitespace, skips blank rows, and optionally removes duplicate rows without overwriting the source file.

- Repository: https://github.com/000MAK/mini-csv-cleaner
- Stack: Python standard library

### Mini JSON–CSV Converter
Converts between JSON arrays of objects and CSV records.

- Repository: https://github.com/000MAK/mini-json-csv-converter
- Stack: Python standard library

### Mini File Organizer
Previews a file-move plan by extension; applying moves requires an explicit option.

- Repository: https://github.com/000MAK/mini-file-organizer
- Stack: Python standard library

## Privacy-first ingestion example

- Repository: [compliant-ingestion-demo](compliant-ingestion-demo/README.md)
- Purpose: validates an operator-provided CSV export against source-authorization and consent attestations, reports aggregate outcomes, and optionally writes a minimal pseudonymous review queue.
- Safety defaults: dry-run unless explicitly applied; no scraping connectors, target discovery, or outbound messaging.
- Data minimization: raw record identifiers are not written to the review queue; the output omits contact data.
- Scope: an educational example, not legal compliance certification. It has not been extracted from the HONOR tablet's unreviewed files.

## Applied ML & Deep Learning Lab

These are educational examples, separate from the 100 numbered CLI utilities.

### Supervised classification
- Code: ml-dl-lab/ml_classification.py
- Methods: Logistic Regression and Random Forest
- Data: scikit-learn's built-in Wine dataset
- Practice: held-out testing, preprocessing pipelines, balanced accuracy, and macro-F1

### Unsupervised clustering
- Code: ml-dl-lab/clustering_demo.py
- Method: K-Means on generated synthetic data
- Practice: feature scaling, silhouette score, and adjusted Rand index

### Neural-network image classification
- Code: ml-dl-lab/dl_digits_classifier.py
- Framework: PyTorch
- Data: scikit-learn's built-in 8×8 Digits dataset
- Practice: separated train/validation/test sets and validation-loss-based early stopping

### Hugging Face sentiment classification
- Code: ml-dl-lab/huggingface_sentiment.py
- Library: Transformers
- Model: distilbert/distilbert-base-uncased-finetuned-sst-2-english
- Task: English positive/negative sentiment classification
- Attribution: the model card lists Apache-2.0; its authors and weights are third-party assets, not my original work
- Setup: see ml-dl-lab/README.md

The sentiment script is original integration code that loads a model from the Hugging Face Hub; model weights are not bundled or mirrored. Model outputs can be wrong and the score is not a calibrated real-world probability. Review the upstream model card, license, and limitations before adapting it.

## Open-source references

See [OPEN_SOURCE_REFERENCES.md](OPEN_SOURCE_REFERENCES.md) for external source links, licenses, and attribution notes. The repository does not claim third-party code or model weights as its own.

## Working approach

My project style emphasizes inspectable code, clear setup instructions, explicit assumptions, and documented limitations. These are learning and utility examples; small teaching datasets do not establish production readiness or generalization to real-world data.

## Contact

[LinkedIn](https://www.linkedin.com/in/mehmet-ali-kaya97/)
