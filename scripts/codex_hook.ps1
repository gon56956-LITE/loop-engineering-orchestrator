param(
  [string]$EventName = "unknown"
)
$ErrorActionPreference = "SilentlyContinue"
$cwd = (Get-Location).Path
$agentWork = Join-Path $cwd "html_report\agent_work"
if (-not (Test-Path -Path $agentWork)) {
  $agentWork = Join-Path $cwd "agent_work"
}
if (-not (Test-Path -Path $agentWork)) {
  exit 0
}
$log = Join-Path $agentWork "hooks_log.md"
$stamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
Add-Content -Path $log -Value "- $stamp event=$EventName cwd=$cwd"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$check = Join-Path $scriptDir "orchestrator_check.py"
$dashboard = Join-Path $agentWork "last_dashboard.md"
if (Test-Path -Path $check) {
  $output = $null
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) {
    $output = & $python.Source $check $agentWork 2>&1
    if ($LASTEXITCODE -ne 0) {
      $output = $null
    }
  }
  if ($null -eq $output) {
    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
      $output = & $pyLauncher.Source -3 $check $agentWork 2>&1
      if ($LASTEXITCODE -ne 0) {
        $output = $null
      }
    }
  }
  if ($null -ne $output) {
    Set-Content -Path $dashboard -Value $output -Encoding UTF8
  }
}
exit 0
