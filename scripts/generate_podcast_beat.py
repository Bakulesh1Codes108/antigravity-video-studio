import numpy as np
import scipy.io.wavfile as wav
import subprocess

def generate_podcast_beat(filename, duration=62.0, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = np.zeros_like(t)

    # BPM = 84 (classic relaxed podcast / chillhop tempo)
    bpm = 84.0
    beat_sec = 60.0 / bpm
    total_beats = int(duration / beat_sec)

    # Warm mellow chords: progression [Dm9, G13, Cmaj9, Am9]
    # Dm9: D3 (146.8), F3 (174.6), A3 (220.0), C4 (261.6), E4 (329.6)
    # G13: G2 (98.0), F3 (174.6), B3 (246.9), E4 (329.6)
    # Cmaj9: C3 (130.8), E3 (164.8), G3 (196.0), B3 (246.9), D4 (293.7)
    # Am9: A2 (110.0), C3 (130.8), E3 (164.8), G3 (196.0), B3 (246.9)
    progressions = [
        [146.83, 174.61, 220.00, 261.63, 329.63], # Dm9
        [98.00, 174.61, 246.94, 329.63, 392.00],  # G13
        [130.81, 164.81, 196.00, 246.94, 293.66], # Cmaj9
        [110.00, 130.81, 164.81, 196.00, 246.94]  # Am9
    ]

    chord_dur = beat_sec * 4 # 1 bar per chord
    for i in range(int(duration / chord_dur) + 1):
        c_start = i * chord_dur
        c_notes = progressions[i % len(progressions)]
        
        idx_start = int(c_start * sample_rate)
        idx_end = min(len(t), int((c_start + chord_dur) * sample_rate))
        t_segment = t[idx_start:idx_end] - c_start
        
        if len(t_segment) == 0:
            continue
            
        # Envelope: soft attack, gentle decay
        env = (1.0 - np.exp(-t_segment * 6.0)) * np.exp(-t_segment * 0.45)
        
        chord_wave = np.zeros_like(t_segment)
        for freq in c_notes:
            # Warm electric piano / Rhodes synthesis (fundamental + gentle 2nd harmonic)
            harm1 = np.sin(2 * np.pi * freq * t_segment)
            harm2 = 0.3 * np.sin(2 * np.pi * freq * 2.0 * t_segment)
            harm3 = 0.1 * np.sin(2 * np.pi * freq * 3.0 * t_segment)
            chord_wave += (harm1 + harm2 + harm3)
            
        audio[idx_start:idx_end] += chord_wave * env * 0.18

    # Smooth sub bass (fundamental tracking chords)
    bass_notes = [73.42, 49.00, 65.41, 55.00] # D2, G1, C2, A1
    for i in range(int(duration / chord_dur) + 1):
        c_start = i * chord_dur
        b_freq = bass_notes[i % len(bass_notes)]
        idx_start = int(c_start * sample_rate)
        idx_end = min(len(t), int((c_start + chord_dur) * sample_rate))
        t_segment = t[idx_start:idx_end] - c_start
        if len(t_segment) > 0:
            env = (1.0 - np.exp(-t_segment * 8.0)) * np.exp(-t_segment * 0.25)
            bass = np.sin(2 * np.pi * b_freq * t_segment) + 0.2 * np.sin(2 * np.pi * b_freq * 2.0 * t_segment)
            audio[idx_start:idx_end] += bass * env * 0.22

    # Beats: subtle kick on 1 and 3.5, smooth snare/rim on 2 and 4, hi-hat on every 8th note
    for b in range(total_beats):
        b_time = b * beat_sec
        # Kick on beat 0 and beat 2.5 of each 4-beat bar
        bar_beat = b % 4
        # Snare/rim on beat 1 and 3 (0-indexed: 1 and 3)
        if bar_beat in [1, 3]:
            idx_start = int(b_time * sample_rate)
            snare_len = int(0.18 * sample_rate)
            idx_end = min(len(t), idx_start + snare_len)
            t_hit = (np.arange(idx_end - idx_start)) / sample_rate
            snare = (np.random.normal(0, 1, len(t_hit)) * 0.8 + np.sin(2 * np.pi * 180 * t_hit) * 0.5) * np.exp(-t_hit * 28.0)
            audio[idx_start:idx_end] += snare * 0.10

        # Kick on beat 0
        if bar_beat == 0:
            idx_start = int(b_time * sample_rate)
            kick_len = int(0.28 * sample_rate)
            idx_end = min(len(t), idx_start + kick_len)
            t_hit = (np.arange(idx_end - idx_start)) / sample_rate
            freq_pitch = 110.0 * np.exp(-t_hit * 30.0) + 42.0
            phase = 2 * np.pi * np.cumsum(freq_pitch) / sample_rate
            kick = np.sin(phase) * np.exp(-t_hit * 12.0)
            audio[idx_start:idx_end] += kick * 0.15

    # Subtle vinyl texture / room ambience
    crackle = np.random.normal(0, 0.008, len(t))
    # Low-pass filter crackle
    audio += crackle

    # Normalize gently
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.85

    # Save to temp wav and convert to mp3
    temp_wav = "/tmp/podcast_beat.wav"
    wav.write(temp_wav, sample_rate, (audio * 32767).astype(np.int16))
    
    cmd = ["ffmpeg", "-y", "-i", temp_wav, "-b:a", "192k", filename]
    subprocess.run(cmd, check=True)
    print(f"Generated podcast music bed at: {filename}")

if __name__ == "__main__":
    generate_podcast_beat("/Users/brane/Downloads/antigravity-video-studio-transfer/projects/nikhil-kamath-wtf-style/assets/bg_music.mp3")
