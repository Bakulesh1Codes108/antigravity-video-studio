#!/usr/bin/env python3
"""
Whisper-CLI Word-Level Lyric Timestamp Extractor
Uses whisper.cpp with ggml-large-v3 to generate high-precision JSON timing for lyric videos.
"""

import argparse
import json
import os
import subprocess
import sys

def transcribe_with_words(audio_path, model_path=None, whisper_bin=None, output_json=None):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at '{audio_path}'")
        sys.exit(1)

    # Auto-detect tools if not provided
    if not whisper_bin:
        whisper_bin = os.environ.get("WHISPER_BIN", "whisper-cli")
    if not model_path:
        default_model = os.path.expanduser("~/video-tools/models/ggml-large-v3.bin")
        model_path = os.environ.get("WHISPER_MODEL", default_model)

    if not os.path.exists(model_path):
        print(f"[-] Whisper model not found at '{model_path}'")
        print("    Download it using setup.ps1 or set WHISPER_MODEL environment variable.")
        sys.exit(1)

    out_prefix = os.path.splitext(audio_path)[0] if not output_json else os.path.splitext(output_json)[0]

    cmd = [
        whisper_bin,
        "-m", model_path,
        "-f", audio_path,
        "-oj",           # output json
        "-sow",          # split on word
        "--max-len", "1",
        "-of", out_prefix
    ]

    print(f"[*] Transcribing '{audio_path}' with whisper.cpp...")
    res = subprocess.run(cmd)
    
    json_path = f"{out_prefix}.json"
    if res.returncode == 0 and os.path.exists(json_path):
        print(f"[+] Word timings saved to: {json_path}")
        return json_path
    else:
        print("[-] Transcription failed.")
        sys.exit(res.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract word-level timestamps using whisper.cpp")
    parser.add_argument("audio", help="Input audio file")
    parser.add_argument("--model", help="Path to ggml-large-v3.bin")
    parser.add_argument("--bin", help="Path to whisper-cli executable")
    parser.add_argument("--out", help="Output JSON path")
    args = parser.parse_args()

    transcribe_with_words(args.audio, args.model, args.bin, args.out)
