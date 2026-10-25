# Quantix — 100 Mini Python Projects

A collection of 100 small, independent Python command-line utilities created as practical coding and automation demonstrations.

**Independent demonstration collection** · Python 3.10+ · Standard library only for the 100 numbered CLI utilities · MIT license

## Highlights

The collection covers small, focused tasks such as text processing, validation, file utilities, date and numeric helpers, and CSV/JSON handling. See the complete Project Index for all 100 entries.

### Selected utility examples

| Project | What it demonstrates |
|---|---|
| [Mini CSV Cleaner](https://github.com/000MAK/mini-csv-cleaner) | Whitespace cleanup, blank-row skipping, optional duplicate-row removal, and non-destructive output handling |
| [Mini JSON–CSV Converter](https://github.com/000MAK/mini-json-csv-converter) | Converting JSON arrays of objects and CSV records |
| [Mini File Organizer](https://github.com/000MAK/mini-file-organizer) | A dry-run-first file-move plan with an explicit apply option |
| [Mini Log Redactor](https://github.com/000MAK/mini-log-redactor) | Redacting common token-like patterns from diagnostic text before review |
| [Mini Expense Tracker](https://github.com/000MAK/mini-expense-tracker) | Local SQLite expense entries and totals grouped by currency |
| [Mini Freelance Rate Calculator](https://github.com/000MAK/mini-freelance-rate-calculator) | Estimating cost-adjusted hourly return from a fixed-price task |

## Applied Machine Learning & Deep Learning Lab

Alongside the 100 standard-library CLI utilities, the repository includes an independent learning track using scikit-learn, NumPy, and PyTorch:

- [Supervised classification](ml-dl-lab/ml_classification.py) — compares Logistic Regression and Random Forest on the built-in Wine dataset.
- [Unsupervised clustering](ml-dl-lab/clustering_demo.py) — K-Means on generated synthetic data, with clustering metrics.
- [Neural-network digit classification](ml-dl-lab/dl_digits_classifier.py) — a PyTorch multilayer perceptron trained on the built-in Digits dataset.

### Hugging Face NLP example

- [English sentiment classification](ml-dl-lab/huggingface_sentiment.py) — an original CLI wrapper using Transformers to run the publicly hosted DistilBERT SST-2 model.
- [Setup and usage guide](ml-dl-lab/README.md) — dependencies and commands.
- [Open-source references and attribution](OPEN_SOURCE_REFERENCES.md) — source links, listed model license, and attribution policy.

The Hugging Face example does not redistribute model weights or claim the pretrained model as original work. It downloads model files from the Hub on first run. Check the upstream model card and license before reuse. All examples in this lab are educational, not production systems or claims of real-world model performance.

## Curated portfolio

See [PORTFOLIO.md](PORTFOLIO.md) for selected projects, their scope, and limitations.

## Requirements

- Python 3.10+
- No third-party runtime packages for the 100 numbered command-line utilities
- A terminal such as PowerShell, Windows Terminal, or a Unix shell

The supplementary ML/DL lab has its own dependency files under ml-dl-lab/.

## Tests

From the repository root on Windows PowerShell:

    .\run_all_tests.ps1

Or use Python directly:

    python run_all_tests.py

Follow each project's README when its test command differs.

## Safety and publication notes

- The utilities use local input/output by default.
- Use synthetic sample data in public demonstrations.
- Inspect files, dependencies, license terms, and test results before adapting any project for client work.
- Never commit API keys, access tokens, passwords, private datasets, or confidential client materials.
- Do not present third-party code, model weights, or datasets as original work; document source links and required notices.

## Repository layout

Each of the 100 numbered project folders is intended to be self-contained with a source file, a README, sample JSON input/output where applicable, and tests. See Project Index for the full catalog. The supplementary ML/DL examples are kept separately in ml-dl-lab/.

## License

MIT. See LICENSE for this repository's original project content. Third-party assets and dependencies may be governed by separate licenses; see OPEN_SOURCE_REFERENCES.md.
