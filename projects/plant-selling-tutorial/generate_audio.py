#!/usr/bin/env python3
"""
Generate voiceover and upbeat chillhop/groove tutorial audio bed.
"""
import os
import subprocess
import numpy as np
from scipy.io import wavfile

audio_dir = "/Users/brane/Downloads/antigravity-video-studio-transfer/projects/plant-selling-tutorial/audio"
os.makedirs(audio_dir, exist_ok=True)

scripts = [
    ("scene1", "Did you know you can turn a small plant investment into a profitable monthly side hustle? While most hobbyists constantly spend money on aquariums, smart aquascapers buy rare mother plants like Bucephalandra Blue and Anubias once, replicate them, and sell them for ten times the return."),
    ("scene2", "Here is how the biological multiplication works: epiphyte plants grow through creeping rhizomes. When your Buce grows ten to twelve healthy leaves, use a sterile blade to slice between the root nodes, keeping four leaves per cutting. One rare mother clump splits into eight to ten rooted pieces in just two months."),
    ("scene3", "To generate fast weekly cash flow while your rare rhizomes mature, add tissue culture cups like Bacopa Monnieri and surface floaters like Water Lettuce. A single tissue cup gives you thirty stems that double biomass every three weeks. Top them, replant the cuttings, and harvest fresh bundles weekly."),
    ("scene4", "Packaging is simple. Wrap roots in damp paper towels, seal in airtight zipper pouches or blister clamshells, and sell directly to local hobbyists, WhatsApp aquarium groups, and online marketplaces. Your hobby pays for itself, and you build a thriving green business from home!")
]

voice_files = []
durations = []

for name, text in scripts:
    aiff_path = os.path.join(audio_dir, f"{name}.aiff")
    wav_path = os.path.join(audio_dir, f"{name}.wav")
    
    cmd = ["say", "-v", "Daniel", "-r", "175", text, "-o", aiff_path]
    subprocess.run(cmd, check=True)
    
    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, "-ar", "44100", "-ac", "2", wav_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    sr, data = wavfile.read(wav_path)
    dur = len(data) / sr
    durations.append(dur)
    voice_files.append(wav_path)
    print(f"[+] {name}: duration = {dur:.2f}s")

scene_starts = [0.8]
for d in durations[:-1]:
    scene_starts.append(scene_starts[-1] + d + 1.0)

total_duration = scene_starts[-1] + durations[-1] + 1.8
print(f"[+] Total Duration: {total_duration:.2f}s")
print(f"[+] Scene Starts: {[round(s, 2) for s in scene_starts]}")

sr = 44100
total_samples = int(total_duration * sr) + sr
full_voice = np.zeros((total_samples, 2), dtype=np.float32)

for wav_p, start_t in zip(voice_files, scene_starts):
    _, vdata = wavfile.read(wav_p)
    vdata_float = vdata.astype(np.float32) / 32768.0
    start_samp = int(start_t * sr)
    end_samp = start_samp + len(vdata_float)
    full_voice[start_samp:end_samp] += vdata_float

# Upbeat Lo-Fi / Groove Background Bed (112 BPM)
bpm = 112.0
beat_len = 60.0 / bpm
t = np.linspace(0, total_duration, total_samples, endpoint=False)

# 1. Warm bassline (F-major / D-minor progression)
f_root = 43.65 # F1
bass = 0.20 * np.sin(2 * np.pi * f_root * t) + 0.10 * np.sin(2 * np.pi * (f_root * 2) * t)
# Rhythmic kick pulse on quarter notes
kick_interval = int(beat_len * sr)
kicks = np.zeros(total_samples, dtype=np.float32)
for i in range(0, total_samples - 5000, kick_interval):
    kt = np.linspace(0, 0.08, int(0.08 * sr), endpoint=False)
    k_env = np.exp(-kt * 45)
    k_wave = np.sin(2 * np.pi * (65 - 35 * kt) * kt) * k_env * 0.28
    kicks[i:i+len(k_wave)] += k_wave

# Snare / rimshot on 2 and 4
snare_interval = kick_interval
snares = np.zeros(total_samples, dtype=np.float32)
for i in range(int(kick_interval / 2), total_samples - 5000, kick_interval):
    st = np.linspace(0, 0.05, int(0.05 * sr), endpoint=False)
    s_wave = (np.random.rand(len(st)) * 2 - 1) * np.exp(-st * 70) * 0.14
    snares[i:i+len(s_wave)] += s_wave

# Chords (warm lush electric piano chords: Fmaj7 -> Dm7 -> Bbmaj7 -> C7)
chord_pad = 0.06 * (np.sin(2 * np.pi * 174.61 * t) + np.sin(2 * np.pi * 220.0 * t) + np.sin(2 * np.pi * 261.63 * t) + np.sin(2 * np.pi * 329.63 * t))
# Subtle filter sweep
lfo = 0.6 + 0.4 * np.sin(2 * np.pi * (1.0 / (beat_len * 4)) * t)
chord_pad *= lfo

music_bed = bass + kicks + snares + chord_pad
bed_stereo = np.column_stack([music_bed * 0.95, music_bed * 1.05])

# Final Mix: Voice + Music Bed
final_mix = full_voice * 0.95 + bed_stereo * 0.32
peak = np.max(np.abs(final_mix))
if peak > 0.95:
    final_mix = final_mix / peak * 0.95

out_wav = os.path.join(audio_dir, "master_narration_bed.wav")
out_mp3 = os.path.join(audio_dir, "song.mp3")
dest_mp3 = "/Users/brane/Downloads/antigravity-video-studio-transfer/projects/plant-selling-tutorial/assets/song.mp3"

wavfile.write(out_wav, sr, (final_mix * 32767).astype(np.int16))
subprocess.run(["ffmpeg", "-y", "-i", out_wav, "-b:a", "192k", out_mp3], check=True)
subprocess.run(["ffmpeg", "-y", "-i", out_wav, "-b:a", "192k", dest_mp3], check=True)
print(f"[+] Master audio generated at: {dest_mp3}")

import json
meta = {
    "total_duration": round(total_duration, 1),
    "scene_starts": [round(s, 2) for s in scene_starts],
    "scene_durations": [round(d, 2) for d in durations]
}
with open(os.path.join(audio_dir, "timing.json"), "w") as f:
    json.dump(meta, f, indent=2)
print(f"[+] Timings saved to timing.json")
