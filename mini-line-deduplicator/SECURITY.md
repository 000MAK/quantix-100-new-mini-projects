# Security Policy

These small examples are educational, not security-audited products. Report a suspected vulnerability privately to the repository maintainer before public disclosure.

## Safe-use principles
- Do not commit secrets, customer data, tokens, real logs, or production databases.
- Treat user-provided JSON/CSV/path values as untrusted.
- The projects do not perform network requests or execute external code by default.
- File/path checking helpers are heuristics; do not use them as the sole boundary for high-risk extraction or file access.
- Formula-neutralization is a defensive output transformation, not a universal guarantee across every spreadsheet application.
