#!/usr/bin/env python3
"""
Antigravity Video Studio - Cross-Platform Desktop Application (macOS & Windows)
Powered by pywebview (WebKit on macOS / WebView2 on Windows) & Local AI Pipeline.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import webview

class VideoStudioAPI:
    def __init__(self, window=None):
        self.window = window
        if sys.platform == "win32":
            self.base_dir = r"D:\AI-models\video-tools"
            if not os.path.exists(self.base_dir):
                self.base_dir = os.path.expanduser("~/video-tools")
        else:
            self.base_dir = os.path.expanduser("~/video-tools")
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "renders"), exist_ok=True)
        os.makedirs(os.path.join(self.base_dir, "projects"), exist_ok=True)

    def select_audio_file(self):
        """Open native file picker for audio."""
        try:
            file_types = ('Audio Files (*.mp3;*.wav;*.flac;*.m4a)', 'All Files (*.*)')
            result = self.window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
            if result and len(result) > 0:
                return result[0]
        except Exception as e:
            print(f"[-] File dialog error: {e}")
        return None

    def generate_video(self, params):
        """Pipeline execution triggered from UI."""
        try:
            audio_path = params.get("audio_path")
            lyrics = params.get("lyrics", "")
            style = params.get("style", "")
            model = params.get("model", "qwen3:8b")
            aspect = params.get("aspect", "9:16")

            # Project directory
            project_dir = os.path.join(self.base_dir, "projects", "studio-render")
            os.makedirs(project_dir, exist_ok=True)
            assets_dir = os.path.join(project_dir, "assets")
            os.makedirs(assets_dir, exist_ok=True)

            # Auto-detect audio if not provided
            repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if not audio_path or not os.path.exists(audio_path):
                macarena_audio = os.path.join(repo_root, "macarena.mp3")
                if os.path.exists(macarena_audio):
                    audio_path = macarena_audio
                else:
                    candidates = [
                        os.path.join(repo_root, "assets", "demo_song.mp3"),
                        os.path.expanduser("~/video-tools/assets/song.mp3")
                    ]
                    for c in candidates:
                        if os.path.exists(c):
                            audio_path = c
                            break

            if audio_path and os.path.exists(audio_path):
                shutil.copyfile(audio_path, os.path.join(assets_dir, "song.mp3"))

            # Build index.html
            width = 1080 if aspect == "9:16" else 1920
            height = 1920 if aspect == "9:16" else 1080

            # Parse lyric lines
            lines = [l.strip() for l in lyrics.splitlines() if l.strip()]
            if not lines:
                lines = ["pal-pal", "jeena", "muhaal", "mera", "bina"]

            # Construct HTML & GSAP
            words_html = ""
            gsap_tweens = ""
            step_duration = 1.3
            current_time = 0.5

            for i, line in enumerate(lines[:12]):
                wid = f"w{i+1}"
                dur = step_duration
                words_html += f'        <span id="{wid}" class="word clip" data-start="{current_time:.2f}" data-duration="{dur:.2f}" data-track-index="{i+2}">{line.lower()}</span>\n'
                
                # GSAP
                gsap_tweens += f"""
      tl.fromTo("#{wid}", {{ opacity: 0, scale: 0.8, y: 35 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.25, ease: "back.out(1.5)" }}, {current_time:.2f})
        .to("#{wid}", {{ opacity: 0, scale: 1.15, y: -25, duration: 0.2, ease: "power2.in" }}, {(current_time + dur - 0.2):.2f});
"""
                current_time += dur

            total_duration = max(8, int(current_time + 1.0))

            template_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={width}, height={height}" />
    <title>Video Studio Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      :root {{
        --bg-start: #0a1128;
        --bg-end: #3b092b;
      }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        margin: 0;
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        background: #000;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      }}
      #root {{
        position: relative;
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at 50% 45%, var(--bg-start), var(--bg-end));
      }}
      .orb {{
        position: absolute;
        width: 700px;
        height: 700px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, rgba(0, 0, 0, 0) 70%);
        pointer-events: none;
      }}
      .badge {{
        position: absolute;
        top: 200px;
        padding: 14px 34px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.8);
        font-size: 28px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .lyric-box {{
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 900px;
        height: 400px;
      }}
      .word {{
        position: absolute;
        font-size: 110px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.04em;
        text-transform: lowercase;
        opacity: 0;
        text-align: center;
        will-change: transform, opacity;
      }}
      .footer-note {{
        position: absolute;
        bottom: 160px;
        color: rgba(255, 255, 255, 0.4);
        font-size: 28px;
        letter-spacing: 0.06em;
      }}
    </style>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="{total_duration}"
      data-width="{width}"
      data-height="{height}"
    >
      <audio id="audio-track" class="clip" data-start="0" data-duration="{total_duration}" src="assets/song.mp3"></audio>
      <div id="orb" class="orb clip" data-start="0" data-duration="{total_duration}" data-track-index="0"></div>
      <div id="badge" class="badge clip" data-start="0" data-duration="{total_duration}" data-track-index="1">Antigravity Video Studio</div>
      
      <div class="lyric-box">
{words_html}      </div>

      <div id="footer" class="footer-note clip" data-start="0" data-duration="{total_duration}" data-track-index="10">Antigravity • HyperFrames macOS</div>
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.to("#orb", {{ scale: 1.35, opacity: 0.85, duration: 4, yoyo: true, ease: "sine.inOut" }}, 0);
{gsap_tweens}
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
            index_path = os.path.join(project_dir, "index.html")
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(template_html)

            # Create package.json
            pkg = {
                "name": "studio-video",
                "version": "1.0.0",
                "dependencies": { "gsap": "^3.15.0" }
            }
            with open(os.path.join(project_dir, "package.json"), "w") as f:
                json.dump(pkg, f, indent=2)

            # Setup PATH environment
            env = os.environ.copy()
            extra_paths = [
                "/usr/local/bin",
                "/usr/bin",
                "/bin",
                "/opt/homebrew/bin",
                os.path.expanduser("~/.nvm/versions/node/v24.22.1/bin"),
                os.path.join(self.base_dir, "ffmpeg", "bin"),
                os.path.join(self.base_dir, "bin")
            ]
            current_path = env.get("PATH", "")
            for p in extra_paths:
                if os.path.exists(p) and p not in current_path:
                    current_path = f"{p}:{current_path}"
            env["PATH"] = current_path

            if sys.platform == "win32":
                render_cmd = ["cmd.exe", "/c", "npx --yes hyperframes render"]
            else:
                npx_bin = shutil.which("hyperframes", path=env["PATH"])
                if npx_bin:
                    render_cmd = [npx_bin, "render"]
                else:
                    npx_bin = shutil.which("npx", path=env["PATH"]) or "npx"
                    render_cmd = [npx_bin, "--yes", "hyperframes", "render"]

            print(f"[*] Executing render command: {' '.join(render_cmd)} in {project_dir}")
            subprocess.run(render_cmd, cwd=project_dir, env=env, check=True)

            # Find rendered video in renders/
            renders_dir = os.path.join(project_dir, "renders")
            if os.path.exists(renders_dir):
                files = [os.path.join(renders_dir, f) for f in os.listdir(renders_dir) if f.endswith(".mp4")]
                if files:
                    files.sort(key=os.path.getmtime, reverse=True)
                    latest_video = files[0]
                    # Also copy to permanent output
                    out_final = os.path.join(self.base_dir, "renders", os.path.basename(latest_video))
                    os.makedirs(os.path.dirname(out_final), exist_ok=True)
                    shutil.copyfile(latest_video, out_final)
                    return {"success": True, "video_path": out_final}

            return {"success": False, "error": "No rendered video found in output directory."}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def show_in_folder(self, file_path):
        """Highlight the file in file manager."""
        if os.path.exists(file_path):
            if sys.platform == "darwin":
                subprocess.run(["open", "-R", os.path.normpath(file_path)])
            elif sys.platform == "win32":
                subprocess.run(f'explorer /select,"{os.path.normpath(file_path)}"')
            else:
                subprocess.run(["xdg-open", os.path.dirname(file_path)])

    def play_video(self, file_path):
        """Open in default system media player."""
        if os.path.exists(file_path):
            if sys.platform == "darwin":
                subprocess.run(["open", file_path])
            elif sys.platform == "win32":
                os.startfile(file_path)
            else:
                subprocess.run(["xdg-open", file_path])

def start_app():
    api = VideoStudioAPI()
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui.html")
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")

    window = webview.create_window(
        title="Antigravity Video Studio (macOS)",
        url=f"file:///{html_path.replace(os.sep, '/')}",
        js_api=api,
        width=1280,
        height=820,
        min_size=(1024, 680),
        background_color="#0a0d14",
    )
    api.window = window
    webview.start(debug=False)

if __name__ == "__main__":
    start_app()
