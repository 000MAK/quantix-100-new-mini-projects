# Claude Code Rules

You are assisting on a collection of 100 independent Python mini-projects. Before editing, read the root README and PROJECT_INDEX.md.

- Never claim a test passed unless you ran it and saw the result.
- Preserve the standard-library-only runtime design unless the user explicitly requests otherwise.
- Never add credentials, `.env` secrets, personal data, client files, logs, or local database files to Git.
- Do not add scraping, marketplace automation/bidding, spam outreach, payment handling, or code execution from untrusted client input.
- Each project is standalone: `main.py`, `README.md`, `sample_input.json`, `sample_output.json`, `test_main.py`.
- Validate with `python run_all_tests.py` and `python -m compileall -q .`.
- Do not overwrite an existing remote repository. Review `git status` and the publication script before publishing.
