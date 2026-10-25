# Privacy-First Authorized Ingestion Demo

This is a small, original safety-oriented example of importing an explicitly authorized CSV export. It is **not extracted from the HONOR tablet** and does not implement scraping adapters, platform bypass, target discovery, or automated messaging.

## What it does

- Reads a CSV export provided by the operator.
- Requires an explicit source-authorization flag and an allowed consent status for each row.
- Validates locale and ISO-style 3-letter currency metadata.
- Reports aggregate acceptance/rejection counts without printing input rows.
- By default, runs in dry-run mode and writes nothing.
- With an explicit apply flag, writes a minimal human-review queue with pseudonymous references; it does not include names, emails, phone numbers, profile URLs, message bodies, or other contact fields.

The source authorization and consent columns are attestations supplied by the data owner; this tool cannot independently establish that consent is legally valid or that a source's terms permit a particular use. Obtain data through documented APIs, licensed feeds, or exports you are authorized to use. Respect applicable laws, privacy notices, platform terms, rate limits, and deletion requests.

## Quick start

Python 3.10+ is recommended.

    python -m pip install -r compliant-ingestion-demo/requirements.txt

From the repository root, inspect the included synthetic example (no real people or accounts):

    python compliant-ingestion-demo/ingest.py --config compliant-ingestion-demo/config.example.yaml

The default is a dry run. It prints counts only and does not write the output CSV.

To create the minimal review queue, set a local pseudonymization secret and explicitly pass --apply. Do not commit the secret:

PowerShell:

    $env:INGEST_PSEUDONYM_KEY = [guid]::NewGuid().ToString() + [guid]::NewGuid().ToString()
    python compliant-ingestion-demo/ingest.py --config compliant-ingestion-demo/config.example.yaml --apply

macOS/Linux:

    export INGEST_PSEUDONYM_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
    python compliant-ingestion-demo/ingest.py --config compliant-ingestion-demo/config.example.yaml --apply

Output is written to the path configured under output_path. The HMAC key is required for applying results so that raw record identifiers are not written to the review queue. Use an organization-managed secret and retention policy for real systems; the example key generation is for local demonstration only.

## Input schema

The CSV needs these columns:

- record_id: internal identifier from an authorized source. It is not written to the output.
- source: a short source label.
- source_authorized: true/yes/1 only when the operator has verified the source and permitted use.
- consent_status: one of the configured allowed values, such as granted or explicit_opt_in.
- locale: locale identifier such as en-US or tr-TR.
- currency: three-letter uppercase currency code such as USD or TRY.

Additional input columns are ignored by the output mapper, but avoid placing unnecessary personal data in the input. Rejected rows are reported only by reason counts, never by row content.

## Scope and boundaries

This is an ingestion and minimization example, not a compliance certification. It has no crawler, platform connector, account automation, message sender, or anti-bot evasion. For a real integration, use a documented API or permissioned export, obtain required consent, minimize fields, add access controls and retention/deletion workflows, and require human review before any action affecting people.

## Files

- config.example.yaml — local paths and acceptance policy.
- ingest.py — schema validation, aggregate-only reporting, pseudonymous output.
- data/example_authorized_export.csv — synthetic demonstration rows only.
- tests/test_ingest.py — validation and minimization tests.
- requirements.txt — YAML parser dependency.
