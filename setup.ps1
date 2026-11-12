# Antigravity Video Studio - Automated Setup Script
# 100% Free & Local: Configures FFmpeg, Whisper.cpp, Python Venv, Ollama check, and Antigravity Skills

param (
    [string]$InstallDrive = "D:"
)

$ErrorActionPreference = "Stop"
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Antigravity Video Studio - 100% Local & Free Installer    " -ForegroundColor Cyan
Write-Host " (Zero Cloud Subscriptions, Local Whisper, Demucs, Ollama) " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Target Directory Setup
$BaseDir = "$InstallDrive\AI-models\video-tools"
if (-not (Test-Path $InstallDrive)) {
    Write-Host "[!] Drive $InstallDrive not found, falling back to C:\video-tools" -ForegroundColor Yellow
    $BaseDir = "$env:USERPROFILE\video-tools"
}

New-Item -ItemType Directory -Force -Path "$BaseDir\bin" | Out-Null
New-Item -ItemType Directory -Force -Path "$BaseDir\models" | Out-Null
New-Item -ItemType Directory -Force -Path "$BaseDir\renders" | Out-Null

# Create junction if on external drive
$JunctionPath = "$env:USERPROFILE\video-tools"
if ($BaseDir -ne $JunctionPath -and -not (Test-Path $JunctionPath)) {
    cmd.exe /c "mklink /J `"$JunctionPath`" `"$BaseDir`""
    Write-Host "[+] Created junction: $JunctionPath -> $BaseDir" -ForegroundColor Green
}

# 2. Check System Tools
Write-Host "`n[*] Checking Prerequisites..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
$python = Get-Command python -ErrorAction SilentlyContinue
$ollama = Get-Command ollama -ErrorAction SilentlyContinue

if (-not $node) { Write-Host "[-] Node.js 22+ is required. Install from https://nodejs.org" -ForegroundColor Red }
else { Write-Host "[+] Node.js: $(node --version)" -ForegroundColor Green }

if (-not $python) { Write-Host "[-] Python 3.11+ is required. Install from https://python.org" -ForegroundColor Red }
else { Write-Host "[+] Python: $(python --version)" -ForegroundColor Green }

if ($ollama) { 
    Write-Host "[+] Ollama detected: $(ollama --version) (Ready for offline local LLMs!)" -ForegroundColor Green 
} else {
    Write-Host "[i] Ollama not found. If you want 100% local prompt direction, install from https://ollama.com" -ForegroundColor Yellow
}

# 3. Install Antigravity Skills
Write-Host "`n[*] Installing Antigravity Skills..." -ForegroundColor Yellow
cmd.exe /c "npx --yes skills add heygen-com/hyperframes -g -y -a antigravity"
cmd.exe /c "npx --yes skills add lemomo-ai/lemo-opuscar -g -y -a antigravity"

# 4. Download FFmpeg
$FfmpegBin = "$BaseDir\ffmpeg\bin"
if (-not (Test-Path "$FfmpegBin\ffmpeg.exe")) {
    Write-Host "`n[*] Downloading FFmpeg Essentials..." -ForegroundColor Yellow
    $ffmpegZip = "$BaseDir\ffmpeg.zip"
    curl.exe -k -L -o $ffmpegZip "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    Expand-Archive -Path $ffmpegZip -DestinationPath "$BaseDir" -Force
    $extracted = Get-ChildItem -Directory "$BaseDir\ffmpeg-*" | Select-Object -First 1
    Rename-Item -Path $extracted.FullName -NewName "$BaseDir\ffmpeg" -Force
    Remove-Item -Path $ffmpegZip -Force
    Write-Host "[+] FFmpeg installed to $FfmpegBin" -ForegroundColor Green
} else {
    Write-Host "[+] FFmpeg already installed." -ForegroundColor Green
}

# 5. Download Whisper.cpp
$WhisperCli = "$BaseDir\bin\whisper-cli.exe"
if (-not (Test-Path $WhisperCli)) {
    Write-Host "`n[*] Downloading Whisper.cpp..." -ForegroundColor Yellow
    $whisperZip = "$BaseDir\whisper.zip"
    curl.exe -k -L -o $whisperZip "https://github.com/ggml-org/whisper.cpp/releases/download/b5454/whisper-bin-x64.zip"
    Expand-Archive -Path $whisperZip -DestinationPath "$BaseDir\whisper_temp" -Force
    Copy-Item "$BaseDir\whisper_temp\Release\*" "$BaseDir\bin\" -Force
    Copy-Item "$BaseDir\bin\whisper-cli.exe" "$BaseDir\bin\whisper-cpp.exe" -Force
    Remove-Item "$BaseDir\whisper_temp" -Recurse -Force
    Remove-Item $whisperZip -Force
    Write-Host "[+] Whisper.cpp installed to $BaseDir\bin" -ForegroundColor Green
} else {
    Write-Host "[+] Whisper.cpp already installed." -ForegroundColor Green
}

# 6. Download Whisper ggml-large-v3 Model
$ModelFile = "$BaseDir\models\ggml-large-v3.bin"
if (-not (Test-Path $ModelFile)) {
    Write-Host "`n[*] Downloading Whisper ggml-large-v3 model (~2.88 GB)..." -ForegroundColor Yellow
    curl.exe -k -L -C - -o $ModelFile "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin"
    Write-Host "[+] Model downloaded to $ModelFile" -ForegroundColor Green
} else {
    Write-Host "[+] Model already exists at $ModelFile" -ForegroundColor Green
}

# 7. Setup Python Venv
$VenvDir = "$BaseDir\venv"
if (-not (Test-Path "$VenvDir\Scripts\python.exe")) {
    Write-Host "`n[*] Creating Python Virtual Environment..." -ForegroundColor Yellow
    python -m venv $VenvDir
    & "$VenvDir\Scripts\pip.exe" install torch torchaudio librosa demucs kokoro-onnx soundfile
    Write-Host "[+] Python venv configured with audio AI packages." -ForegroundColor Green
} else {
    Write-Host "[+] Python venv already configured." -ForegroundColor Green
}

# 8. Add to User PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$NewPaths = @("$BaseDir\ffmpeg\bin", "$BaseDir\bin")
$PathUpdated = $false
foreach ($p in $NewPaths) {
    if (-not $UserPath.Contains($p)) {
        $UserPath = "$p;$UserPath"
        $PathUpdated = $true
    }
}
if ($PathUpdated) {
    [Environment]::SetEnvironmentVariable("Path", $UserPath, "User")
    Write-Host "[+] Updated User PATH with FFmpeg and Whisper binaries." -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " Setup Complete! 100% Free & Local AI Video Pipeline Ready! " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
