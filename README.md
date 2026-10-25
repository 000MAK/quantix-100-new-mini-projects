# Quantix — 100 Mini Python Projects

[![Python utility tests](https://github.com/000MAK/quantix-100-new-mini-projects/actions/workflows/tests.yml/badge.svg)](https://github.com/000MAK/quantix-100-new-mini-projects/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A collection of 100 small, independent Python command-line utilities created as practical coding and automation demonstrations.

**Independent demonstration collection** · Python 3.10+ · Standard library only for the 100 numbered CLI utilities

## Start here

- [Project index](PROJECT_INDEX.md) — all 100 utilities
- [Curated portfolio](PORTFOLIO.md) — selected projects and scope
- [Applied ML & Deep Learning Lab](ml-dl-lab/README.md) — classification, clustering, PyTorch and Hugging Face examples
- [Privacy-First Ingestion Demo](compliant-ingestion-demo/README.md) — authorized CSV ingestion, dry-run default, minimized review output
- [Contributing](CONTRIBUTING.md) · [Security policy](SECURITY.md) · [Open-source attribution](OPEN_SOURCE_REFERENCES.md)

## Selected utility examples

| Project | What it demonstrates |
|---|---|
| [Mini CSV Cleaner](https://github.com/000MAK/mini-csv-cleaner) | Whitespace cleanup, blank-row skipping, optional duplicate-row removal, and non-destructive output handling |
| [Mini JSON–CSV Converter](https://github.com/000MAK/mini-json-csv-converter) | Converting JSON arrays of objects and CSV records |
| [Mini File Organizer](https://github.com/000MAK/mini-file-organizer) | A dry-run-first file-move plan with an explicit apply option |
| [Mini Log Redactor](https://github.com/000MAK/mini-log-redactor) | Redacting common token-like patterns from diagnostic text before review |
| [Mini Expense Tracker](https://github.com/000MAK/mini-expense-tracker) | Local SQLite expense entries and totals grouped by currency |
| [Mini Freelance Rate Calculator](https://github.com/000MAK/mini-freelance-rate-calculator) | Estimating cost-adjusted hourly return from a fixed-price task |

These are compact learning and utility projects, not claims that every tool is production-ready for every environment. Review each project's own README, constraints, and tests before relying on it.

## Privacy-first ingestion example

The separate [Compliant Ingestion Demo](compliant-ingestion-demo/README.md) is an original, dry-run-first example for CSV exports that an operator is authorized to use. It requires source authorization and consent signals, reports aggregate decisions, and can export only minimal pseudonymous review records with an explicit flag. It does not scrape websites, discover targets, or send messages.

This demo is a safety-oriented starter and **was not extracted from the HONOR MagicPad 2**. It does not certify legal compliance; the operator must verify source permissions, consent, retention, and applicable requirements.

## Applied Machine Learning & Deep Learning Lab

Alongside the 100 standard-library CLI utilities, the repository includes an independent learning track using scikit-learn, NumPy, and PyTorch:

- [Supervised classification](ml-dl-lab/ml_classification.py) — compares Logistic Regression and Random Forest on the built-in Wine dataset.
- [Unsupervised clustering](ml-dl-lab/clustering_demo.py) — K-Means on generated synthetic data, with clustering metrics.
- [Neural-network digit classification](ml-dl-lab/dl_digits_classifier.py) — a PyTorch multilayer perceptron trained on the built-in Digits dataset.


- [Twenty-model online-data benchmark](ml-dl-lab/run_20_models.py) — twenty statistical and ML experiments using online UCI Wine Quality and Bike Sharing data, including classification, regression, PCA, GMM, anomaly screening, Poisson count models, quantile modeling, and EVT.
- [Online Beans image CNN](ml-dl-lab/vision_beans_cnn.py) — downloads the Beans dataset from Hugging Face and trains a small 2-D CNN.
- [Online FSDD audio CNN](ml-dl-lab/audio_fsdd_cnn.py) — downloads the version-tagged Free Spoken Digit Dataset and trains a 1-D CNN for spoken-digit classification.
- [Dataset source and license register](ONLINE_DATA_SOURCES.md) — original source URLs, licenses, model/data attribution, and caveats.
- [Twenty-model and image/audio lab README](ml-dl-lab/README.md) — full setup, usage, test, and limitations guide.

The twenty-model suite and the image/audio projects download public data at runtime. Datasets, downloaded archives, and trained weights are not committed. The Beans dataset card has incomplete information about the original source license; review the source terms before commercial reuse. Audio use is attributed to FSDD under its stated CC BY-SA 4.0 terms. These are demonstrations, not production systems.


### Hugging Face NLP example

- [English sentiment classification](ml-dl-lab/huggingface_sentiment.py) — an original CLI wrapper using Transformers to run the publicly hosted DistilBERT SST-2 model.
- [Setup and usage guide](ml-dl-lab/README.md) — dependencies and commands.
- [Open-source references and attribution](OPEN_SOURCE_REFERENCES.md) — source links, listed model license, and attribution policy.

The Hugging Face example does not redistribute model weights or claim the pretrained model as original work. It downloads model files from the Hub on first run. Check the upstream model card and license before reuse. All examples in this lab are educational, not production systems or claims of real-world model performance.

## Run the 100 utility tests

From the repository root:

    python run_all_tests.py

The GitHub Actions workflow runs the utility test suite and compiles Python files on pushes and pull requests. The ingestion demo's separate policy tests are located in compliant-ingestion-demo/tests/ and have their own dependencies.

## Safety and publication notes

- Use synthetic sample data in public demonstrations.
- Inspect files, dependencies, license terms, and test results before adapting any project for client work.
- Never commit API keys, access tokens, passwords, private datasets, real target lists, or delivery logs.
- Do not present third-party code, model weights, or datasets as original work; document source links and required notices.
- The ingestion example is not a crawler, platform connector, or outbound messaging tool.

## License

MIT for original content in this repository; third-party assets and dependencies may be governed by separate licenses. See [LICENSE](LICENSE) and [OPEN_SOURCE_REFERENCES.md](OPEN_SOURCE_REFERENCES.md).
