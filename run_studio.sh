#!/usr/bin/env bash
# Antigravity Video Studio Launcher for macOS
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "[!] Virtual environment not found. Running setup.sh first..."
    bash "$SCRIPT_DIR/setup.sh"
fi

export PATH="/usr/local/bin:/opt/homebrew/bin:$HOME/.nvm/versions/node/v24.22.1/bin:$PATH"
echo "[*] Launching Antigravity Video Studio Desktop UI on macOS..."
exec "$VENV_PYTHON" "$SCRIPT_DIR/app/main.py"
