param(
  [Parameter(Mandatory=$true)][string]$Owner,
  [ValidateSet("private", "public")][string]$Visibility = "private",
  [switch]$DryRun
)
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "GitHub CLI (gh) not found. Install it, then run: gh auth login" }
gh auth status
if ($LASTEXITCODE -ne 0) { throw "GitHub CLI is not authenticated." }
$projects = Get-ChildItem -Path $root -Directory | Where-Object { Test-Path (Join-Path $_.FullName "main.py") -and Test-Path (Join-Path $_.FullName "test_main.py") } | Sort-Object Name
foreach ($p in $projects) {
  $repo = "$Owner/$($p.Name)"
  Write-Host "=== $repo ==="
  if ($DryRun) { Write-Host "DRY RUN: would create $Visibility repo and push $($p.FullName)"; continue }
  $remoteExists = $false
  try {
    gh repo view $repo *> $null
    $remoteExists = ($LASTEXITCODE -eq 0)
  } catch { $remoteExists = $false }
  if ($remoteExists) { throw "Remote repository already exists: $repo. Stopping; nothing was overwritten." }
  Push-Location $p.FullName
  try {
    python -m unittest -v
    if ($LASTEXITCODE -ne 0) { throw "Tests failed in $($p.Name)" }
    git init
    git add .gitignore README.md main.py test_main.py sample_input.json sample_output.json LICENSE SECURITY.md CONTRIBUTING.md CLAUDE.md
    git status --short
    git commit -m "Initial release: $($p.Name)"
    if ($LASTEXITCODE -ne 0) { throw "Commit failed in $($p.Name)" }
    $visibilityFlag = "--$Visibility"
    gh repo create $repo $visibilityFlag --source . --remote origin --push
    if ($LASTEXITCODE -ne 0) { throw "Publish failed for $repo" }
  } finally { Pop-Location }
}
Write-Host "Finished publishing $($projects.Count) projects. Verify all remote repos in GitHub." 
