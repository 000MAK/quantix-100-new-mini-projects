# Quantix 100 New Mini Projects — Audit Report

- Standalone projects: 100 (expected 100)
- Each project includes main.py, test_main.py, sample input/output, README, LICENSE, SECURITY.md, CONTRIBUTING.md, CLAUDE.md, and .gitignore.
- Runtime dependencies: Python standard library only.
- Network activity: none in the individual utility implementations.
- Automated marketplace browsing, bidding, messaging, and delivery: not included.

## Test evidence

- The aggregate runner loads every individual test module in one process, preventing `main` import-name collisions.
- Each project has a sample regression test and an invalid-root-input test; password/token generators use property tests and invalid-parameter tests.
- GitHub Actions is configured for Python 3.10–3.13 using Node 24-compatible `actions/checkout@v7` and `actions/setup-python@v7`.
- The test suite and compile check were run locally in the build environment; Windows PowerShell and remote GitHub workflows have not been run here.
- The publishing scripts require `gh auth login`; no GitHub repositories have been created or pushed by this package build.

## Project index

001. `mini-archive-member-check` — Archive Member Safety Check
002. `mini-base64-tool` — Base64 Encoder Decoder
003. `mini-break-even-calculator` — Break-Even Units Calculator
004. `mini-budget-splitter` — Budget Splitter
005. `mini-business-day-adder` — Business Day Adder
006. `mini-changelog-entry` — Changelog Entry Generator
007. `mini-character-frequency` — Character Frequency
008. `mini-code-line-stats` — Code Line Stats
009. `mini-compound-interest` — Compound Interest Calculator
010. `mini-config-type-validator` — Config Type Validator
011. `mini-contingency-table` — Contingency Table
012. `mini-csv-column-selector` — CSV Column Selector
013. `mini-csv-deduplicator` — CSV Deduplicator
014. `mini-csv-formula-guard` — CSV Formula Guard
015. `mini-csv-header-normalizer` — CSV Header Normalizer
016. `mini-csv-header-renamer` — CSV Header Renamer
017. `mini-csv-quality-report` — CSV Quality Report
018. `mini-csv-row-filter` — CSV Row Filter
019. `mini-csv-splitter` — CSV Splitter
020. `mini-csv-to-json` — CSV to JSON
021. `mini-currency-converter` — Currency Converter (Offline)
022. `mini-date-difference` — Date Difference
023. `mini-date-range` — Date Range Generator
024. `mini-directory-tree` — Directory Tree Formatter
025. `mini-discount-calculator` — Discount Price Calculator
026. `mini-duplicate-content-finder` — Duplicate Content Finder
027. `mini-duration-formatter` — Duration Formatter
028. `mini-email-masker` — Email Masker
029. `mini-env-auditor` — Environment File Auditor
030. `mini-epoch-to-utc` — Epoch to UTC
031. `mini-extension-allowlist` — Extension Allowlist
032. `mini-extension-report` — File Extension Report
033. `mini-frequency-table` — Frequency Table
034. `mini-gitignore-generator` — Gitignore Generator
035. `mini-habit-streak` — Habit Streak Calculator
036. `mini-header-allowlist` — Header Allowlist Checker
037. `mini-hex-tool` — Hex Encoder Decoder
038. `mini-human-file-size` — Human File Size
039. `mini-interval-overlap` — Interval Overlap Checker
040. `mini-invoice-draft` — Invoice Draft Generator
041. `mini-iso-week` — ISO Week Number
042. `mini-json-array-deduplicator` — JSON Array Deduplicator
043. `mini-json-field-masker` — JSON Field Masker
044. `mini-json-flattener` — JSON Flattener
045. `mini-json-key-sorter` — JSON Key Sorter
046. `mini-json-object-merger` — JSON Object Merger
047. `mini-json-path-getter` — JSON Path Getter
048. `mini-json-pretty-printer` — JSON Pretty Printer
049. `mini-json-required-keys` — JSON Required Keys
050. `mini-json-to-csv` — JSON to CSV
051. `mini-json-type-report` — JSON Type Report
052. `mini-jsonl-validator` — JSONL Validator
053. `mini-kanban-summary` — Kanban Summary
054. `mini-line-decorator` — Line Decorator
055. `mini-line-deduplicator` — Line Deduplicator
056. `mini-line-ending-normalizer` — Line Ending Normalizer
057. `mini-line-sorter` — Line Sorter
058. `mini-linear-regression` — Linear Regression
059. `mini-meeting-action-items` — Meeting Action Extractor
060. `mini-microtask-estimator` — Microtask Workload Estimator
061. `mini-minmax-normalizer` — Min-Max Normalizer
062. `mini-month-calendar` — Month Calendar
063. `mini-moving-average` — Moving Average
064. `mini-net-hourly-rate` — Net Hourly Rate Calculator
065. `mini-numeric-stats` — Numeric Statistics
066. `mini-password-generator` — Password Generator
067. `mini-password-strength` — Password Strength Heuristic
068. `mini-path-traversal-check` — Path Traversal Check
069. `mini-pearson-correlation` — Pearson Correlation
070. `mini-percentile-calculator` — Percentile Calculator
071. `mini-personal-budget-summary` — Personal Budget Summary
072. `mini-phone-masker` — Phone Masker
073. `mini-platform-fee-calculator` — Platform Fee Calculator
074. `mini-pomodoro-planner` — Pomodoro Planner
075. `mini-quote-estimator` — Freelance Quote Estimator
076. `mini-reading-time` — Reading Time Calculator
077. `mini-record-quality-report` — Record Quality Report
078. `mini-requirements-auditor` — Requirements Auditor
079. `mini-roi-calculator` — ROI Calculator
080. `mini-safe-filename` — Safe Filename
081. `mini-safe-relative-path` — Safe Relative Path Validator
082. `mini-secret-redactor` — Secret Redactor
083. `mini-secure-token-generator` — Secure Token Generator
084. `mini-semver-compare` — Semantic Version Compare
085. `mini-sensitive-field-report` — Sensitive Field Scanner
086. `mini-sha256-text` — SHA-256 Text Hash
087. `mini-simple-interest` — Simple Interest Calculator
088. `mini-slug-generator` — Slug Generator
089. `mini-study-scheduler` — Weighted Study Scheduler
090. `mini-task-priority-sorter` — Task Priority Sorter
091. `mini-time-entry-sum` — Time Entry Sum
092. `mini-title-case` — Title Case Converter
093. `mini-url-parser` — URL Parser
094. `mini-uuid-validator` — UUID Validator
095. `mini-whitespace-normalizer` — Whitespace Normalizer
096. `mini-word-budget` — Word Budget Planner
097. `mini-word-counter` — Word Counter
098. `mini-word-reverser` — Word Reverser
099. `mini-word-set-diff` — Word Set Diff
100. `mini-zscore-outlier-detector` — Z-Score Outlier Detector
