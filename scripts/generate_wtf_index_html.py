import json

def generate_html():
    with open("/Users/brane/Downloads/antigravity-video-studio-transfer/projects/nikhil-kamath-wtf-style/assets/captions.json") as f:
        captions = json.load(f)

    # HTML template
    html = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <title>WTF with Nikhil Kamath Style Short</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800;900&family=JetBrains+Mono:wght@700;800&display=swap" rel="stylesheet">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    html, body {
      margin: 0;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: #090c12;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #fff;
    }
    #root {
      position: relative;
      width: 1080px;
      height: 1920px;
      overflow: hidden;
      background: radial-gradient(circle at 50% 35%, #181d2a 0%, #090c12 75%, #040508 100%);
    }

    /* Ambient Blurred Background Video Layer */
    .bg-video-wrap {
      position: absolute;
      top: -5%;
      left: -5%;
      width: 110%;
      height: 110%;
      overflow: hidden;
      filter: blur(50px) saturate(1.6) brightness(0.32);
      opacity: 0.85;
      transform: scale(1.1);
      pointer-events: none;
    }
    .bg-video-wrap video {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* Subtle Studio Lighting Orbs */
    .glow-orb-1 {
      position: absolute;
      top: 15%;
      left: -100px;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(34, 197, 94, 0.18) 0%, rgba(0,0,0,0) 70%);
      pointer-events: none;
    }
    .glow-orb-2 {
      position: absolute;
      bottom: 25%;
      right: -100px;
      width: 600px;
      height: 600px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 230, 0, 0.14) 0%, rgba(0,0,0,0) 70%);
      pointer-events: none;
    }

    /* Top Podcast Badge */
    .top-badge-container {
      position: absolute;
      top: 65px;
      left: 0;
      width: 1080px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 60px;
      z-index: 50;
    }
    .podcast-pill {
      display: inline-flex;
      align-items: center;
      gap: 14px;
      padding: 14px 26px;
      background: rgba(18, 24, 38, 0.85);
      border: 1.5px solid rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      backdrop-filter: blur(20px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .live-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #ef4444;
      box-shadow: 0 0 12px #ef4444;
      animation: pulseDot 1.5s infinite;
    }
    @keyframes pulseDot {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .podcast-title {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #fff;
    }
    .podcast-title span {
      color: #ffe600;
    }

    /* Equalizer Sound Waves */
    .eq-bars {
      display: flex;
      align-items: flex-end;
      gap: 4px;
      height: 22px;
    }
    .eq-bar {
      width: 4px;
      background: #22c55e;
      border-radius: 2px;
    }

    .topic-pill {
      display: inline-flex;
      align-items: center;
      padding: 12px 22px;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 999px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: rgba(255, 255, 255, 0.7);
    }

    /* Main Video Frame (The Speaker) */
    .speaker-frame-outer {
      position: absolute;
      top: 165px;
      left: 54px;
      width: 972px;
      height: 1160px;
      border-radius: 40px;
      overflow: hidden;
      background: #000;
      border: 2px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 40px 100px rgba(0, 0, 0, 0.9), inset 0 0 0 1px rgba(255, 255, 255, 0.08);
      z-index: 20;
    }
    .speaker-video-inner {
      width: 100%;
      height: 100%;
      transform-origin: center center;
      will-change: transform;
    }
    .speaker-video-inner video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    /* Subtle Frame Gradient Shadows */
    .frame-vignette {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0) 30%, rgba(0,0,0,0) 70%, rgba(0,0,0,0.4) 100%);
      pointer-events: none;
    }

    /* Lower Third / Subtitle Deck */
    .subtitle-stage {
      position: absolute;
      top: 1375px;
      left: 50px;
      width: 980px;
      height: 290px;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 60;
      text-align: center;
      pointer-events: none;
    }

    .caption-chunk {
      position: absolute;
      width: 100%;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 16px 20px;
      opacity: 0;
      will-change: transform, opacity;
    }

    .word-token {
      display: inline-block;
      font-size: 64px;
      font-weight: 900;
      letter-spacing: -0.02em;
      text-transform: uppercase;
      color: #ffffff;
      -webkit-text-stroke: 3.5px #05070a;
      paint-order: stroke fill;
      text-shadow: 0 10px 30px rgba(0, 0, 0, 0.95), 0 2px 6px rgba(0,0,0,1);
      transform-origin: center center;
      will-change: transform, color, filter;
      transition: none;
    }

    /* Bottom Scrubber & Call to Action */
    .bottom-cta-wrap {
      position: absolute;
      bottom: 70px;
      left: 0;
      width: 1080px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 22px;
      z-index: 50;
    }

    .cta-button-pill {
      display: inline-flex;
      align-items: center;
      gap: 14px;
      padding: 16px 36px;
      background: linear-gradient(135deg, #ffe600 0%, #22c55e 100%);
      border-radius: 999px;
      color: #05070a;
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      box-shadow: 0 12px 35px rgba(34, 197, 94, 0.35);
    }
    .cta-arrow {
      font-size: 28px;
    }

    .progress-bar-rail {
      width: 960px;
      height: 8px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 4px;
      overflow: hidden;
    }
    .progress-bar-fill {
      width: 0%;
      height: 100%;
      background: linear-gradient(90deg, #ffe600, #22c55e);
      border-radius: 4px;
      will-change: width;
    }
  </style>
</head>
<body>
  <div
    id="root"
    data-composition-id="main"
    data-start="0"
    data-duration="61.34"
    data-width="1080"
    data-height="1920"
  >
    <audio id="masterAudio" class="clip" data-start="0" data-duration="61.34" src="assets/mixed_audio.mp3"></audio>

    <!-- Background Ambient Video -->
    <div class="bg-video-wrap">
      <video id="bgVideo" src="assets/talking_head.mp4" muted playsinline></video>
    </div>

    <div class="glow-orb-1"></div>
    <div class="glow-orb-2"></div>

    <!-- Top Badge -->
    <div class="top-badge-container">
      <div class="podcast-pill">
        <div class="live-dot"></div>
        <div class="podcast-title">WTF <span>//</span> MASTERCLASS</div>
        <div class="eq-bars">
          <div class="eq-bar" id="eq1" style="height: 18px;"></div>
          <div class="eq-bar" id="eq2" style="height: 12px;"></div>
          <div class="eq-bar" id="eq3" style="height: 22px;"></div>
          <div class="eq-bar" id="eq4" style="height: 14px;"></div>
        </div>
      </div>
      <div class="topic-pill">EP. 42 // REAL WEALTH</div>
    </div>

    <!-- Main Talking Head Speaker Frame -->
    <div class="speaker-frame-outer">
      <div class="speaker-video-inner" id="speakerZoom">
        <video id="talkVideo" class="clip" data-start="0" data-duration="61.34" src="assets/talking_head.mp4" muted playsinline></video>
      </div>
      <div class="frame-vignette"></div>
    </div>

    <!-- Subtitle Deck -->
    <div class="subtitle-stage">
"""

    # Inject caption chunks
    chunk_htmls = []
    for c_idx, c in enumerate(captions):
        words_html = []
        for w_idx, w in enumerate(c["words"]):
            w_id = f"w_{c_idx}_{w_idx}"
            words_html.append(f'<span class="word-token" id="{w_id}">{w["text"]}</span>')
        chunk_str = f'      <div class="caption-chunk" id="chunk_{c_idx}">\n        ' + "\n        ".join(words_html) + '\n      </div>'
        chunk_htmls.append(chunk_str)

    html += "\n".join(chunk_htmls)

    html += """
    </div>

    <!-- Bottom CTA & Progress Bar -->
    <div class="bottom-cta-wrap">
      <div class="cta-button-pill">
        <span>JOIN MY MASTERCLASS TODAY</span>
        <span class="cta-arrow">➔</span>
      </div>
      <div class="progress-bar-rail">
        <div class="progress-bar-fill" id="progressBar"></div>
      </div>
    </div>
  </div>

  <script>
    const tl = gsap.timeline({ paused: true });

    // Sync HTML5 videos with timeline
    const v1 = document.getElementById("talkVideo");
    const v2 = document.getElementById("bgVideo");
    tl.to([v1, v2], {
      currentTime: 61.34,
      duration: 61.34,
      ease: "none"
    }, 0);

    // Progress bar
    tl.to("#progressBar", {
      width: "100%",
      duration: 61.34,
      ease: "none"
    }, 0);

    // Dynamic Zoom Punch-ins on speaker frame (Nikhil Kamath Signature Style)
    // 0 -> 12.3: scale 1.0
    // 12.3 -> 15.2: PUNCH-IN on "AI CANNOT AUTOMATE THIS!"
    tl.to("#speakerZoom", { scale: 1.12, duration: 0.15, ease: "power2.out" }, 12.3);
    tl.to("#speakerZoom", { scale: 1.0, duration: 0.2, ease: "power2.out" }, 15.2);

    // 20.8 -> 26.0: PUNCH-IN on "ONLY 60 PAISE!"
    tl.to("#speakerZoom", { scale: 1.10, duration: 0.15, ease: "power2.out" }, 20.8);
    tl.to("#speakerZoom", { scale: 1.0, duration: 0.2, ease: "power2.out" }, 26.0);

    // 36.3 -> 39.5: PUNCH-IN on "REGISTER FOR MY MASTERCLASS!"
    tl.to("#speakerZoom", { scale: 1.12, duration: 0.15, ease: "power2.out" }, 36.3);
    tl.to("#speakerZoom", { scale: 1.0, duration: 0.2, ease: "power2.out" }, 39.5);

    // 45.8 -> 48.5: PUNCH-IN on "NO AI CAN EVER AUTOMATE!"
    tl.to("#speakerZoom", { scale: 1.10, duration: 0.15, ease: "power2.out" }, 45.8);
    tl.to("#speakerZoom", { scale: 1.0, duration: 0.2, ease: "power2.out" }, 48.5);

    // 54.7 -> 57.0: PUNCH-IN on "10X RETURNS BACK!"
    tl.to("#speakerZoom", { scale: 1.15, duration: 0.15, ease: "power2.out" }, 54.7);
    tl.to("#speakerZoom", { scale: 1.0, duration: 0.2, ease: "power2.out" }, 57.0);

    // 59.8 -> 61.2: PUNCH-IN on "START NOW!"
    tl.to("#speakerZoom", { scale: 1.20, duration: 0.15, ease: "power2.out" }, 59.8);

    // Animated Equalizer bars
    const eqBars = ["#eq1", "#eq2", "#eq3", "#eq4"];
    for (let t = 0; t < 61; t += 0.4) {
      eqBars.forEach((bar, idx) => {
        const h = 8 + Math.sin(t * 5 + idx * 1.5) * 7 + (idx % 2 === 0 ? 4 : 2);
        tl.to(bar, { height: h + "px", duration: 0.35, ease: "sine.inOut" }, t);
      });
    }
"""

    # Inject GSAP caption animations
    for c_idx, c in enumerate(captions):
        chunk_id = f"#chunk_{c_idx}"
        start_t = c["start"]
        end_t = c["end"]
        
        # Chunk entrance
        html += f'\n    // Chunk {c_idx}: [{start_t}s -> {end_t}s]\n'
        html += f'    tl.fromTo("{chunk_id}", {{ opacity: 0, y: 30, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1.0, duration: 0.2, ease: "back.out(1.5)" }}, {start_t});\n'
        
        # Word highlight pops
        for w_idx, w in enumerate(c["words"]):
            w_id = f"#w_{c_idx}_{w_idx}"
            w_start = w["start"]
            w_dur = max(0.15, round(w["end"] - w["start"], 2))
            col = w.get("color", "#FFE600")
            
            # Word pop
            html += f'    tl.to("{w_id}", {{ scale: 1.22, color: "{col}", filter: "drop-shadow(0 0 20px {col})", duration: 0.15, ease: "back.out(2)" }}, {w_start});\n'
            # Settle slightly
            html += f'    tl.to("{w_id}", {{ scale: 1.08, duration: {w_dur}, ease: "power1.out" }}, {round(w_start + 0.15, 2)});\n'

        # Chunk exit
        html += f'    tl.to("{chunk_id}", {{ opacity: 0, y: -25, scale: 0.95, duration: 0.15, ease: "power2.in" }}, {round(end_t - 0.05, 2)});\n'

    html += """
    window.__timelines = window.__timelines || {};
    window.__timelines["main"] = tl;
    tl.seek(0);
  </script>
</body>
</html>
"""

    with open("/Users/brane/Downloads/antigravity-video-studio-transfer/projects/nikhil-kamath-wtf-style/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("Successfully generated index.html for nikhil-kamath-wtf-style!")

if __name__ == "__main__":
    generate_html()
