# Quantix — 100 Mini Python Projects

A collection of 100 small, independent Python command-line utilities created as practical coding and automation demonstrations.

**Independent demonstration collection** · Python 3.10+ · Standard library only for the 100 numbered CLI utilities · MIT license

## Highlights

The collection covers small, focused tasks such as text processing, validation, file utilities, date and numeric helpers, and CSV/JSON handling. See the complete [Project Index](PROJECT_INDEX.md) for all 100 entries.

### Selected examples

| Project | What it demonstrates |
|---|---|
| [Mini CSV Cleaner](https://github.com/000MAK/mini-csv-cleaner) | Whitespace cleanup, blank-row skipping, optional duplicate-row removal, and non-destructive output handling |
| [Mini JSON–CSV Converter](https://github.com/000MAK/mini-json-csv-converter) | Converting JSON arrays of objects and CSV records with explicit headers |
| [Mini File Organizer](https://github.com/000MAK/mini-file-organizer) | A dry-run-first file-move plan with an explicit apply option |
| [Mini Log Redactor](https://github.com/000MAK/mini-log-redactor) | Redacting common token-like patterns from diagnostic text before review |
| [Mini Expense Tracker](https://github.com/000MAK/mini-expense-tracker) | Local SQLite expense entries and totals grouped by currency without assuming FX rates |
| [Mini Freelance Rate Calculator](https://github.com/000MAK/mini-freelance-rate-calculator) | Estimating cost-adjusted hourly return from a fixed-price task |

These are compact learning and utility projects, not claims that every tool is production-ready for every environment. Review each project's own README, constraints, and tests before relying on it.

## Applied Machine Learning & Deep Learning Lab

Alongside the 100 standard-library CLI utilities, the repository now includes a **separate learning track** with reproducible ML/DL examples that use scikit-learn, NumPy, and PyTorch:

- [Supervised classification](ml-dl-lab/ml_classification.py) — compares Logistic Regression and Random Forest on scikit-learn's built-in Wine dataset.
- [Unsupervised clustering](ml-dl-lab/clustering_demo.py) — runs K-Means on generated synthetic data and reports clustering metrics.
- [Neural-network digit classification](ml-dl-lab/dl_digits_classifier.py) — trains a PyTorch multilayer perceptron on scikit-learn's built-in Digits dataset with validation-based early stopping.

Read the [ML/DL Lab guide](ml-dl-lab/README.md) for dependencies, commands, and limitations. The additional ML/DL dependencies do not apply to the 100 numbered command-line utilities. These examples are educational baselines, not production models, and their sample-dataset results should not be treated as evidence of real-world performance.

## Curated portfolio

See [PORTFOLIO.md](PORTFOLIO.md) for a curated overview of selected public Quantix demonstration projects and their scope/limitations.

## Requirements

- Python 3.10+
- No third-party runtime packages for the 100 numbered command-line utilities
- A terminal such as PowerShell, Windows Terminal, or a Unix shell

The supplementary ML/DL lab has its own dependency list at ml-dl-lab/requirements.txt.

## Run one project

Choose a project folder from the index, then follow that folder's README. For example, enter the mini-word-counter folder, then run its documented main.py sample_input.json command and unit tests.

For an ML/DL example, from the repository root install ml-dl-lab/requirements.txt and run one of the commands documented in the lab guide.

## Run the collection tests

From the repository root on Windows PowerShell:

    .\run_all_tests.ps1

Or use Python directly:

    python run_all_tests.py

If a particular test command differs, follow the instructions in that project's README.

## Safety and publication notes

- The utilities are designed for local input/output by default.
- The collection does not contain platform scraping, automatic bidding, credential collection, or execution of client-supplied code.
- Use synthetic sample data in public demonstrations.
- Inspect files, dependencies, license terms, and test results before adapting any project for client work.
- Never commit API keys, access tokens, passwords, private datasets, or confidential client materials.

## Repository layout

Each of the 100 numbered project folders is intended to be self-contained with a source file, a README, sample JSON input/output where applicable, and unit tests. See PROJECT_INDEX.md for the full catalog. The supplementary ML/DL examples are kept separately in ml-dl-lab/.

## License

MIT. See LICENSE.
