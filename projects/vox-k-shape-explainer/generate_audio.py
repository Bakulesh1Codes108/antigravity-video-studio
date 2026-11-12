#!/usr/bin/env python3
"""
Generate Vox-style voiceover and tension documentary audio bed.
"""
import os
import subprocess
import numpy as np
from scipy.io import wavfile

audio_dir = "/Users/brane/Downloads/antigravity-video-studio-transfer/projects/vox-k-shape-explainer/audio"
os.makedirs(audio_dir, exist_ok=True)

scripts = [
    ("scene1", "We were promised an equitable recovery. Instead, the global economy fractured into a brutal K-shape. For asset owners and tech monopolies, wealth has surged to unprecedented heights. But for the working majority, real wages and economic security are in free fall."),
    ("scene2", "At the center of this chasm is artificial intelligence. Unlike previous industrial revolutions that displaced manual workers, generative AI directly hollows out middle-class cognitive labor. Every productivity gain is captured by compute capital, while entry-level jobs vanish overnight."),
    ("scene3", "Globally, the consequences are grave. A new digital imperialism is dividing nations. The United States and China are monopolizing advanced chips, energy grids, and data centers. The Global South is left trapped on the downward slope, crushed by sovereign debt and technological dependency."),
    ("scene4", "When an algorithmic elite captures the gains of civilization and leaves billions behind, the social contract breaks. The K-shaped world is not an accident. It is an engineered divergence. And unless we democratize compute, the chasm will only widen.")
]

voice_files = []
durations = []

for name, text in scripts:
    aiff_path = os.path.join(audio_dir, f"{name}.aiff")
    wav_path = os.path.join(audio_dir, f"{name}.wav")
    
    # Run macOS say with Daniel (clean British documentary voice)
    cmd = ["say", "-v", "Daniel", "-r", "165", text, "-o", aiff_path]
    subprocess.run(cmd, check=True)
    
    # Convert to wav
    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    sr, data = wavfile.read(wav_path)
    dur = len(data) / sr
    durations.append(dur)
    voice_files.append(wav_path)
    print(f"[+] {name}: duration = {dur:.2f}s")

# Calculate spacing and total time
# Give 1.0s intro, 1.2s between scenes, 2.0s outro
scene_starts = [1.0]
for d in durations[:-1]:
    scene_starts.append(scene_starts[-1] + d + 1.2)

total_duration = scene_starts[-1] + durations[-1] + 2.0
print(f"[+] Total Duration: {total_duration:.2f}s")
print(f"[+] Scene Starts: {[round(s, 2) for s in scene_starts]}")

# Generate Full Voice Track with precise placement
sr = 44100
total_samples = int(total_duration * sr) + sr
full_voice = np.zeros((total_samples, 2), dtype=np.float32)

for wav_p, start_t in zip(voice_files, scene_starts):
    _, vdata = wavfile.read(wav_p)
    vdata_float = vdata.astype(np.float32) / 32768.0
    start_samp = int(start_t * sr)
    end_samp = start_samp + len(vdata_float)
    full_voice[start_samp:end_samp] += vdata_float

# Synthesize Tension Documentary Soundtrack Bed (Minimalist Vox Tension)
# 105 BPM rhythmic tick + 55 Hz sub-bass pulse + subtle dark harmonic pad
bpm = 105.0
beat_len = 60.0 / bpm
t = np.linspace(0, total_duration, total_samples, endpoint=False)

# 1. Dark Sub-Bass Pulse (55Hz and 110Hz with slow filter sweep)
bass_freq = 55.0
bass = 0.22 * np.sin(2 * np.pi * bass_freq * t) + 0.12 * np.sin(2 * np.pi * (bass_freq * 2) * t)
# Rhythmically gate the bass every 2 beats
bass_gate = 0.5 + 0.5 * np.cos(2 * np.pi * (1.0 / beat_len) * t)
bass *= np.power(bass_gate, 3)

# 2. Tension Clockwork Ticks on every 8th note
tick_interval = int((beat_len / 2.0) * sr)
ticks = np.zeros(total_samples, dtype=np.float32)
for i in range(0, total_samples - 4000, tick_interval):
    # short resonant click
    click_t = np.linspace(0, 0.04, int(0.04 * sr), endpoint=False)
    click = np.sin(2 * np.pi * 1800 * click_t) * np.exp(-click_t * 90) * 0.16
    ticks[i:i+len(click)] += click

# 3. Ambient Dark Pad (E-minor chord 164.81Hz, 196.0Hz, 246.94Hz)
pad = 0.08 * np.sin(2 * np.pi * 164.81 * t) + 0.06 * np.sin(2 * np.pi * 196.00 * t) + 0.06 * np.sin(2 * np.pi * 246.94 * t)
# Subtle slow breathing modulation (LFO)
lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t)
pad *= lfo

# Stereo Bed
bed_mono = bass + ticks + pad
# Slight stereo widening
bed_left = bed_mono * 0.95
bed_right = bed_mono * 1.05
bed_stereo = np.column_stack([bed_left, bed_right])

# Master Mix: Voice + Music Bed
# Voice takes center stage, bed provides atmospheric suspense
final_mix = full_voice * 0.92 + bed_stereo * 0.35

# Soft limiter
peak = np.max(np.abs(final_mix))
if peak > 0.95:
    final_mix = final_mix / peak * 0.95

# Export to WAV & MP3
out_wav = os.path.join(audio_dir, "master_narration_bed.wav")
out_mp3 = os.path.join(audio_dir, "song.mp3")

wavfile.write(out_wav, sr, (final_mix * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-i", out_wav, "-b:a", "192k", out_mp3], check=True)
print(f"[+] Master audio generated at: {out_mp3}")

# Save timestamps metadata JSON
import json
meta = {
    "total_duration": round(total_duration, 1),
    "scene_starts": [round(s, 2) for s in scene_starts],
    "scene_durations": [round(d, 2) for d in durations]
}
with open(os.path.join(audio_dir, "timing.json"), "w") as f:
    json.dump(meta, f, indent=2)
print(f"[+] Timings saved to timing.json")
