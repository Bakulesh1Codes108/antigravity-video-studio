#!/usr/bin/env python3
"""
Local AI Video Director
Automated code-to-video generator powered by Local LLMs (Ollama / Llama / Qwen / LM Studio).
100% Free, 100% Offline, Zero Cloud APIs.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

DEFAULT_OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

SYSTEM_PROMPT = """You are an expert HyperFrames & GSAP video code director.
Your goal is to generate clean, valid HTML5 and GSAP animation code for a 9:16 vertical video.

RULES:
1. Output ONLY the raw HTML code inside a ```html ... ``` block. No markdown chatter outside.
2. The root container MUST have:
   id="root" data-composition-id="main" data-start="0" data-duration="{duration}" data-width="1080" data-height="1920"
3. All timed visual elements MUST have:
   class="clip" and data-start="X" and data-duration="Y"
4. Audio tag MUST have:
   <audio id="audio-track" class="clip" data-start="0" data-duration="{duration}" src="assets/song.mp3"></audio>
5. Use GSAP 3:
   const tl = gsap.timeline({ paused: true });
   window.__timelines = window.__timelines || {};
   window.__timelines["main"] = tl;
   tl.seek(0);
6. Style for 1080x1920 vertical mobile view. Include clean, modern CSS with high contrast.
"""

def query_local_ollama(prompt, model="qwen3:8b", host=DEFAULT_OLLAMA_HOST):
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": False
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    print(f"[*] Querying local model '{model}' at {host}...")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("response", "")
    except urllib.error.URLError as e:
        print(f"[-] Could not connect to Ollama at {host}: {e}")
        print("    Ensure Ollama is running (`ollama serve`).")
        return None

def extract_html(raw_response):
    if "```html" in raw_response:
        parts = raw_response.split("```html")
        code = parts[1].split("```")[0].strip()
        return code
    elif "```" in raw_response:
        parts = raw_response.split("```")
        return parts[1].strip()
    return raw_response.strip()

def create_video_project(project_dir, song_path, lyrics, style, model="qwen3:8b", duration=10):
    os.makedirs(project_dir, exist_ok=True)
    assets_dir = os.path.join(project_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Copy audio file
    import shutil
    dest_song = os.path.join(assets_dir, "song.mp3")
    if song_path and os.path.exists(song_path):
        shutil.copyfile(song_path, dest_song)
        print(f"[+] Audio copied to {dest_song}")

    # Build prompt for local LLM
    prompt = f"""Create a 9:16 vertical animated lyric video.
DURATION: {duration} seconds
STYLE: {style}
LYRICS / SCRIPT:
{lyrics}

Generate the full index.html file with GSAP animations, eye-catching backgrounds, and perfectly timed typography clips.
"""

    response = query_local_ollama(prompt, model=model)
    if not response:
        print("[-] Generation failed. Using fallback template.")
        return False

    html_code = extract_html(response)
    html_path = os.path.join(project_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_code)
    print(f"[+] Composition generated at: {html_path}")

    # Create meta.json and hyperframes.json
    pkg_json = {
        "name": "local-ai-video",
        "version": "1.0.0",
        "scripts": { "render": "hyperframes render" }
    }
    with open(os.path.join(project_dir, "package.json"), "w") as f:
        json.dump(pkg_json, f, indent=2)

    print(f"[+] Project ready in: {project_dir}")
    print(f"    To preview: cd {project_dir} && npx hyperframes dev")
    print(f"    To render:  cd {project_dir} && npx hyperframes render")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate videos with Local LLMs (Ollama / Llama)")
    parser.add_argument("--model", default="qwen3:8b", help="Ollama model name (e.g. qwen3:8b, llama3.2, mistral)")
    parser.add_argument("--song", help="Path to input audio/song file")
    parser.add_argument("--lyrics", help="Lyrics or text script")
    parser.add_argument("--lyrics-file", help="Path to text file containing lyrics")
    parser.add_argument("--style", default="Epic kinetic typography, dark duotone gradient, film grain", help="Visual style description")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--output", default="my-local-video", help="Output project directory")
    args = parser.parse_args()

    lyrics_text = args.lyrics or ""
    if args.lyrics_file and os.path.exists(args.lyrics_file):
        with open(args.lyrics_file, "r", encoding="utf-8") as lf:
            lyrics_text = lf.read()

    create_video_project(args.output, args.song, lyrics_text, args.style, model=args.model, duration=args.duration)
