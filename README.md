# 100 New Mini Python Projects — Safe GitHub Starter Pack

100 independent, small Python command-line utilities. Each project is self-contained in its own folder with `main.py`, `README.md`, sample JSON input/output, and unit tests.

- Python 3.10+
- Standard library only; no runtime pip packages
- Local-only input/output by default
- No platform scraping, automated bids, credential collection, or client-code execution
- Includes GitHub Actions CI and Claude Code instructions

## Quick start

Run one project:

```bash
cd mini-word-counter
python main.py sample_input.json
python -m unittest -v
```

Run the full test suite from the root:

```powershell
.\run_all_tests.ps1
```

or cross-platform:

```bash
python run_all_tests.py
```

## The 100 projects

See [`PROJECT_INDEX.md`](PROJECT_INDEX.md) for the full catalog. All names are unique to this pack and separate from the prior 10-project starter pack.

## Publish strategy

Recommended first: publish this collection as one repository named `quantix-100-new-mini-projects`. It is easier to maintain and avoids creating 100 nearly empty repositories at once. If you choose to split them into separate repositories, use `publish_all.ps1` only after `gh auth login`; it intentionally checks for name collisions and stops rather than overwriting an existing remote repository.

The publication script defaults to **private** repositories. Use `-Visibility public` only after reviewing the code and license. A GitHub account and authenticated GitHub CLI session are required; this package does not contain credentials.

## License

MIT. See `LICENSE`.
