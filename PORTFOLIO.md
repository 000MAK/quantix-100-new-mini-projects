# Quantix Project Portfolio

This page highlights selected small Python utilities and learning projects published as independent demonstrations. They illustrate focused data-processing, file-safety, validation, automation, and introductory ML/DL workflows. They are not presented as paid client engagements or as a claim that every project is production-ready for every use case.

## Selected Python utilities

### 1. Mini CSV Cleaner
Trims leading and trailing whitespace, skips fully blank rows, and optionally removes duplicate rows after trimming. It keeps the source file intact and refuses to overwrite an existing destination.

- Repository: https://github.com/000MAK/mini-csv-cleaner
- Stack: Python 3.10+, Python standard library
- Useful for: small, deterministic CSV cleanup tasks

### 2. Mini JSON–CSV Converter
Converts JSON arrays of objects to CSV and CSV records to a JSON array. It uses encountered object keys to construct the CSV columns.

- Repository: https://github.com/000MAK/mini-json-csv-converter
- Stack: Python 3.10+, Python standard library
- Useful for: straightforward interchange between common data formats

### 3. Mini Duplicate Line Finder
Reports repeated non-empty lines and their occurrence counts.

- Repository: https://github.com/000MAK/mini-duplicate-line-finder
- Stack: Python 3.10+, Python standard library
- Useful for: quick text-file diagnostics

### 4. Mini File Organizer
Builds a proposed file-move plan by file extension. It previews the plan by default; file moves require the explicit --apply flag.

- Repository: https://github.com/000MAK/mini-file-organizer
- Stack: Python 3.10+, Python standard library
- Safety note: review the dry-run output before applying moves

### 5. Mini Log Redactor
Redacts common token-like patterns from diagnostic logs before sharing. Output still requires manual review because pattern-based redaction cannot guarantee that every secret is removed.

- Repository: https://github.com/000MAK/mini-log-redactor
- Stack: Python 3.10+, Python standard library
- Useful for: first-pass log hygiene before review

### 6. Mini Expense Tracker
Stores basic expense records locally in SQLite and totals amounts by currency without assuming an exchange rate.

- Repository: https://github.com/000MAK/mini-expense-tracker
- Stack: Python 3.10+, Python standard library, SQLite
- Useful for: a compact local CLI and database example

### 7. Mini Freelance Rate Calculator
Estimates cost-adjusted earnings per hour from an example fixed-price task using the provided inputs.

- Repository: https://github.com/000MAK/mini-freelance-rate-calculator
- Stack: Python 3.10+, Python standard library
- Useful for: transparent task-pricing arithmetic

## Applied ML & Deep Learning Lab

These are introductory educational examples, kept separate from the 100 numbered CLI utilities.

### 1. Supervised classification
- Code: [ml_classification.py](ml-dl-lab/ml_classification.py)
- Methods: Logistic Regression and Random Forest
- Data: scikit-learn's built-in Wine dataset
- Practice: train/test separation, preprocessing pipelines, balanced accuracy, and macro-F1

### 2. Unsupervised clustering
- Code: [clustering_demo.py](ml-dl-lab/clustering_demo.py)
- Method: K-Means
- Data: reproducibly generated synthetic blobs
- Practice: scaling, silhouette score, and adjusted Rand index

### 3. Neural-network image classification
- Code: [dl_digits_classifier.py](ml-dl-lab/dl_digits_classifier.py)
- Framework: PyTorch
- Data: scikit-learn's built-in 8×8 Digits dataset
- Practice: train/validation/test splits, a multilayer perceptron, validation-loss-based early stopping, and a held-out test report

Install the additional packages using [ml-dl-lab/requirements.txt](ml-dl-lab/requirements.txt). See the [lab guide](ml-dl-lab/README.md) for run instructions. These small datasets are useful for learning and reproducibility, not for claiming production performance or generalization to real-world data.

## Larger collection

The [Quantix 100 Mini Python Projects](https://github.com/000MAK/quantix-100-new-mini-projects) repository indexes 100 small command-line utilities. Review the per-project README and tests before relying on any utility in a production workflow.

## Approach

My project style favors small, inspectable utilities, explicit inputs, deterministic transformations where applicable, non-destructive output handling, and clear statements of limitations. For data-cleaning work, ambiguous records should be flagged rather than silently interpreted. For ML/DL examples, preprocessing and evaluation are documented so that the educational scope is clear.

## Contact and freelance scope

I am interested in well-defined Python data-processing tasks, spreadsheet/CSV cleanup, simple format conversion, and small automation utilities. Project scope, input requirements, validation rules, and deliverables should be agreed before work starts.

All linked items are independent demonstration projects unless explicitly stated otherwise. No customer data or confidential code should be included in public repositories.
