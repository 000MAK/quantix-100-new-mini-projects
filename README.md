# Quantix — 100 Mini Python Projects

A collection of 100 small, independent Python command-line utilities created as practical coding and automation demonstrations.

**Independent demonstration collection** · Python 3.10+ · Standard library only for runtime · MIT license

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

## Curated portfolio

See [PORTFOLIO.md](PORTFOLIO.md) for a curated overview of selected public Quantix demonstration projects and their scope/limitations.

## Requirements

- Python 3.10+
- No third-party runtime packages for the included command-line utilities
- A terminal such as PowerShell, Windows Terminal, or a Unix shell

## Run one project

Choose a project folder from the index, then follow that folder's README. For example:

```bash
cd mini-word-counter
python main.py sample_input.json
python -m unittest -v
```

## Run the collection tests

From the repository root on Windows PowerShell:

```powershell
.\run_all_tests.ps1
```

Or use Python directly:

```bash
python run_all_tests.py
```

If a particular test command differs, follow the instructions in that project's README.

## Safety and publication notes

- The utilities are designed for local input/output by default.
- The collection does not contain platform scraping, automatic bidding, credential collection, or execution of client-supplied code.
- Use synthetic sample data in public demonstrations.
- Inspect files, dependencies, license terms, and test results before adapting any project for client work.
- Never commit API keys, access tokens, passwords, private datasets, or confidential client materials.

## Repository layout

Each of the 100 project folders is intended to be self-contained with a source file, a README, sample JSON input/output where applicable, and unit tests. See [PROJECT_INDEX.md](PROJECT_INDEX.md) for the full catalog.

## License

MIT. See [LICENSE](LICENSE).
