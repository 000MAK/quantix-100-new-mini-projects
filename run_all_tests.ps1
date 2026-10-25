$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$root\run_all_tests.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
