import subprocess
import json
import numpy as np
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel

def main():
    wav_in = "/Users/brane/Downloads/whatsapp_audio.wav"
    wav_16k = "/Users/brane/Downloads/whatsapp_16k.wav"
    out_json = "/Users/brane/Downloads/transcription_words.json"

    print("Converting to 16kHz mono PCM...")
    cmd = ["ffmpeg", "-y", "-i", wav_in, "-ar", "16000", "-ac", "1", "-f", "wav", wav_16k]
    subprocess.run(cmd, check=True)

    sr, data = wav.read(wav_16k)
    audio_float = data.astype(np.float32) / 32768.0
    print(f"Loaded audio: shape={audio_float.shape}, duration={len(audio_float)/16000:.2f}s")

    print("Running WhisperModel...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_float, word_timestamps=True)

    print(f"Detected language: {info.language} (p={info.language_probability:.2f})")

    words_data = []
    sentences_data = []

    for segment in segments:
        sentences_data.append({
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        })
        if segment.words:
            for word in segment.words:
                words_data.append({
                    "word": word.word.strip(),
                    "start": round(word.start, 2),
                    "end": round(word.end, 2)
                })

    output = {
        "duration": info.duration,
        "language": info.language,
        "sentences": sentences_data,
        "words": words_data
    }

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Done! Extracted {len(words_data)} words and {len(sentences_data)} sentences.")
    for s in sentences_data:
        print(f"[{s['start']}s -> {s['end']}s]: {s['text']}")

if __name__ == "__main__":
    main()
