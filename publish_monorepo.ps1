param([Parameter(Mandatory=$true)][string]$Owner,[ValidateSet("private","public")][string]$Visibility="private")
$ErrorActionPreference="Stop"
$root=Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "Install GitHub CLI and run gh auth login first." }
python "$root\run_all_tests.py"; if ($LASTEXITCODE -ne 0) { throw "Tests failed; refusing to publish." }
Push-Location $root
try {
  if (-not (Test-Path (Join-Path $root ".git"))) { git init }
  git add .
  git status --short
  Write-Host "Review the staged changes above. Then commit and create the remote repository manually if preferred."
  $answer=Read-Host "Create/push new repository $Owner/quantix-100-new-mini-projects ($Visibility)? Type YES to continue"
  if ($answer -ne "YES") { Write-Host "Cancelled; no remote repository created."; exit 0 }
  git commit -m "Initial release: 100 safe mini Python projects"
  if ($LASTEXITCODE -ne 0) { throw "Commit failed. Check whether there is anything to commit." }
  $visibilityFlag = "--$Visibility"
  gh repo create "$Owner/quantix-100-new-mini-projects" $visibilityFlag --source . --remote origin --push
  if ($LASTEXITCODE -ne 0) { throw "Publish failed." }
} finally { Pop-Location }
