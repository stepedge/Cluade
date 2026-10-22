# StepEdge Dell setup: installs the main tools used on the HP work PC.
# Run: right-click Start > Terminal (Admin), then:
#   Set-ExecutionPolicy -Scope Process Bypass -Force; & "$env:USERPROFILE\Downloads\setup-dell.ps1"
# Add -Mobile to also install the Android/Flutter tools for the handheld app (large download, ~10 GB).
# Safe to run again: anything already installed is skipped.

param([switch]$Mobile)

$ErrorActionPreference = 'Continue'
$results = @()

function Add-Result($name, $ok, $note = '') {
    $script:results += [pscustomobject]@{ Item = $name; Status = $(if ($ok) { 'OK' } else { 'FAILED' }); Note = $note }
}

function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}

if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Warning 'Please run this from an Administrator terminal (right-click Start > Terminal (Admin)).'
    exit 1
}
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warning 'winget is missing. Install "App Installer" from the Microsoft Store, then run this again.'
    exit 1
}

# 1. Programs (winget IDs)
$apps = [ordered]@{
    'Git.Git'                    = 'Git (code history, GitHub)'
    'GitHub.cli'                 = 'GitHub command line'
    'Python.Python.3.12'         = 'Python 3.12'
    'OpenJS.NodeJS.LTS'          = 'Node.js LTS (IBMS backend, back office, till build)'
    'Microsoft.VisualStudioCode' = 'VS Code editor'
    'Google.Chrome'              = 'Chrome (Claude in Chrome)'
    'Anthropic.Claude'           = 'Claude desktop app'
    'Gyan.FFmpeg'                = 'FFmpeg (videos)'
    'Microsoft.PowerShell'       = 'PowerShell 7'
    'Microsoft.WindowsTerminal'  = 'Windows Terminal'
    '7zip.7zip'                  = '7-Zip'
}
if ($Mobile) {
    $apps['Microsoft.OpenJDK.17'] = 'Java 17 (Android builds)'
    $apps['Google.AndroidStudio'] = 'Android Studio + SDK'
}

foreach ($id in $apps.Keys) {
    Write-Host "`n=== $($apps[$id]) [$id]" -ForegroundColor Cyan
    $listed = winget list --id $id --exact --accept-source-agreements 2>$null | Out-String
    if ($listed -match [regex]::Escape($id)) { Add-Result $apps[$id] $true 'already installed'; continue }
    winget install --id $id --exact --silent --accept-package-agreements --accept-source-agreements
    Add-Result $apps[$id] ($LASTEXITCODE -eq 0) $(if ($LASTEXITCODE -ne 0) { "winget exit $LASTEXITCODE" } else { '' })
}
Refresh-Path

# 2. Python packages
Write-Host "`n=== Python packages" -ForegroundColor Cyan
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if ($py) {
    $pkgs = 'pip', 'Pillow', 'imageio-ffmpeg', 'playwright', 'requests', 'openpyxl', 'pandas', 'python-docx', 'pypdf'
    & $py.Source -m pip install --upgrade @pkgs
    Add-Result 'Python packages' ($LASTEXITCODE -eq 0) ($pkgs -join ', ')
    & $py.Source -m playwright install chromium
    Add-Result 'Playwright Chromium' ($LASTEXITCODE -eq 0)
} else { Add-Result 'Python packages' $false 'Python not found on PATH; open a new terminal and run again' }

# 3. Claude Code command line
Write-Host "`n=== Claude Code CLI" -ForegroundColor Cyan
if (Get-Command npm -ErrorAction SilentlyContinue) {
    npm install -g @anthropic-ai/claude-code
    Add-Result 'Claude Code CLI' ($LASTEXITCODE -eq 0)
} else { Add-Result 'Claude Code CLI' $false 'npm not found; open a new terminal and run again' }

# 4. Flutter (handheld app) - only with -Mobile
if ($Mobile) {
    Write-Host "`n=== Flutter SDK" -ForegroundColor Cyan
    $flutter = 'C:\dev\flutter'
    if (-not (Test-Path $flutter)) {
        New-Item -ItemType Directory -Force -Path 'C:\dev' | Out-Null
        git clone https://github.com/flutter/flutter.git -b stable $flutter
    }
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    if ($userPath -notlike "*$flutter\bin*") {
        [Environment]::SetEnvironmentVariable('Path', "$userPath;$flutter\bin", 'User')
    }
    Refresh-Path
    Add-Result 'Flutter SDK' (Test-Path "$flutter\bin\flutter.bat") 'run "flutter doctor" afterwards'
}

# Summary
Write-Host "`n================ SUMMARY ================" -ForegroundColor Green
$results | Format-Table -AutoSize
Write-Host 'Next: sign in to OneDrive, Chrome and the Claude app (same account), then restart the laptop.'
