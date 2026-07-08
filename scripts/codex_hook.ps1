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
$py = "C:\Users\gon56956\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$check = "C:\Users\gon56956\.codex\skills\loop-engineering-orchestrator\scripts\orchestrator_check.py"
$dashboard = Join-Path $agentWork "last_dashboard.md"
if ((Test-Path -Path $py) -and (Test-Path -Path $check)) {
  $output = & $py $check $agentWork 2>&1
  Set-Content -Path $dashboard -Value $output -Encoding UTF8
}
exit 0
