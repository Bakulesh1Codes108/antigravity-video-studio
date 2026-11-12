#!/usr/bin/env bash
# Antigravity Video Studio - Automated Setup Script for macOS
set -e

echo "=========================================================="
echo " Antigravity Video Studio - macOS Setup Script           "
echo " (Zero Cloud Subscriptions, 100% Free & Local Video)    "
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$HOME/video-tools"

mkdir -p "$BASE_DIR/bin"
mkdir -p "$BASE_DIR/models"
mkdir -p "$BASE_DIR/renders"
mkdir -p "$BASE_DIR/projects"

echo ""
echo "[*] Checking Prerequisites on macOS..."

# 1. Check Node.js & npm
if ! command -v node &> /dev/null; then
    echo "[-] Node.js is required. Install from https://nodejs.org or 'brew install node'"
    exit 1
else
    echo "[+] Node.js detected: $(node --version)"
fi

# 2. Check Python 3
PYTHON_CMD=""
for cmd in python3.12 python3.11 python3; do
    if command -v $cmd &> /dev/null; then
        PYTHON_CMD="$cmd"
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "[-] Python 3.11+ is required. Install with 'brew install python@3.12'"
    exit 1
fi
echo "[+] Python detected: $($PYTHON_CMD --version) ($PYTHON_CMD)"

# 3. Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "[!] FFmpeg not found in PATH. Checking /usr/local/bin/ffmpeg or /opt/homebrew/bin/ffmpeg..."
    if [ -x "/usr/local/bin/ffmpeg" ]; then
        export PATH="/usr/local/bin:$PATH"
        echo "[+] Found FFmpeg at /usr/local/bin/ffmpeg"
    elif [ -x "/opt/homebrew/bin/ffmpeg" ]; then
        export PATH="/opt/homebrew/bin:$PATH"
        echo "[+] Found FFmpeg at /opt/homebrew/bin/ffmpeg"
    else
        echo "[!] Please install ffmpeg via: brew install ffmpeg"
    fi
else
    echo "[+] FFmpeg detected: $(ffmpeg -version | head -n 1)"
fi

# 4. Check or install HyperFrames globally
echo ""
echo "[*] Ensuring HyperFrames is installed..."
if ! command -v hyperframes &> /dev/null; then
    echo "[*] Installing hyperframes globally via npm..."
    npm install -g hyperframes
fi
echo "[+] HyperFrames is ready: $(hyperframes --version || echo 'available')"

# 5. Create Python Virtual Environment
VENV_DIR="$SCRIPT_DIR/.venv"
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "[*] Creating Python Virtual Environment at $VENV_DIR..."
    $PYTHON_CMD -m venv "$VENV_DIR"
fi

echo "[*] Installing Python dependencies (pywebview, yt-dlp)..."
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet pywebview yt-dlp

echo ""
echo "=========================================================="
echo " Setup Complete! Antigravity Video Studio is ready on Mac!"
echo " Launch the Studio app with: ./run_studio.sh             "
echo "=========================================================="
