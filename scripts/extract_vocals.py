#!/usr/bin/env python3
"""
Demucs Vocal Stem Extractor
Extracts clean vocal tracks from an audio file to enable perfect lyric transcription.
"""

import argparse
import os
import subprocess
import sys

def separate_vocals(audio_path, output_dir="separated"):
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at '{audio_path}'")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] Separating stems for: {audio_path}")
    
    cmd = [
        sys.executable, "-m", "demucs.separate",
        "-n", "htdemucs",
        "--two-stems=vocals",
        "-o", output_dir,
        audio_path
    ]
    
    result = subprocess.run(cmd)
    if result.returncode == 0:
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        vocal_path = os.path.join(output_dir, "htdemucs", base_name, "vocals.wav")
        print(f"[+] Vocal stem isolated: {vocal_path}")
        return vocal_path
    else:
        print("[-] Demucs separation failed.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Isolate vocals from a song using Demucs.")
    parser.add_argument("audio", help="Path to input audio file (.mp3, .wav, etc.)")
    parser.add_argument("--output", default="separated", help="Directory to store separated tracks")
    args = parser.parse_args()
    separate_vocals(args.audio, args.output)
