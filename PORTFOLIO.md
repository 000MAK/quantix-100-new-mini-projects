# Project Portfolio

A curated entry point to selected public projects by Mehmet Ali Kaya. The repositories cover research prototypes, applied ML/DL demonstrations, and practical Python utilities. Each project README describes its current scope and limitations.

## Research projects

### BIOGAS RS-PIM Engine
A research/academic Python pipeline exploring biogas plant output modeling, regime detection, extreme-value tail fitting, risk metrics, and report generation.

- Repository: https://github.com/000MAK/biogas-rspim-engine
- Technologies described in the repository: Python, stochastic-process modeling, HMM/GMM regime analysis, EVT, Streamlit, and report exports
- Data: users supply their own CSV time series; the repository does not include proprietary or client data
- Current limitation: full runtime against real data is not verified; review the code and inputs before relying on outputs

### PXU030 Portfolio Optimization
A portfolio-optimization research and visualization artifact associated with daily data covering 2020-01-01 through 2022-12-02.

- Repository: https://github.com/000MAK/PXU030Portfoliooptimization
- Artifact: min-var.html
- Current limitation: published material does not yet document the full data source, preprocessing, optimization constraints, or an end-to-end reproduction path. It should not be used to support performance claims without that work.

## Applied machine learning and deep learning

### Applied ML & Deep Learning Lab
A separate educational learning track with four examples.

- [Lab guide and run instructions](ml-dl-lab/README.md)
- Supervised classification: Logistic Regression and Random Forest on the scikit-learn Wine dataset
- Unsupervised learning: K-Means on synthetic data, with clustering metrics
- Deep learning: a PyTorch multilayer perceptron for the built-in Digits dataset
- Hugging Face inference: a small English sentiment CLI that uses a third-party pretrained model with source attribution

These are educational examples, not claims of production performance or real-world generalization. External models and libraries remain attributed to their respective owners.

## Data privacy and safe ingestion

### Privacy-First Ingestion Demo
An original dry-run-first example for validating an operator-provided CSV export before creating a minimal, pseudonymous review queue.

- [Source and usage guide](compliant-ingestion-demo/README.md)
- Checks source-authorization and consent attestations
- Reports aggregate outcomes rather than printing raw row contents
- Writes no output by default; an explicit flag and local HMAC key are required for export
- No crawler, platform connector, target discovery, or automated messaging
- Educational example only; not a legal compliance certification

## Python developer utilities

| Repository | Purpose |
|---|---|
| [Mini CSV Cleaner](https://github.com/000MAK/mini-csv-cleaner) | Trim whitespace, skip blank rows, and optionally deduplicate rows without overwriting the input |
| [Mini JSON–CSV Converter](https://github.com/000MAK/mini-json-csv-converter) | Convert between JSON arrays of objects and CSV records |
| [Mini File Organizer](https://github.com/000MAK/mini-file-organizer) | Preview file-move plans before applying changes |
| [Mini Log Redactor](https://github.com/000MAK/mini-log-redactor) | Best-effort pattern-based redaction for common secret-like values; manual review is still required |
| [Quantix 100 Mini Python Projects](https://github.com/000MAK/quantix-100-new-mini-projects) | Index of 100 independent command-line utilities |

## Engineering approach

- Document the expected inputs, setup steps, and constraints.
- Keep demonstration data synthetic or appropriately licensed.
- Avoid committing secrets, credentials, private datasets, target lists, or delivery logs.
- Attribute upstream libraries, pretrained models, and third-party material.
- Describe research outputs honestly and distinguish code compilation from full runtime validation.

## Contact

[LinkedIn](https://www.linkedin.com/in/mehmet-ali-kaya97/) · [GitHub profile](https://github.com/000MAK)
