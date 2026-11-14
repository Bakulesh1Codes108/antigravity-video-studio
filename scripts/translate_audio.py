import numpy as np
import scipy.io.wavfile as wav
import json
from faster_whisper import WhisperModel

def main():
    sr, data = wav.read("/Users/brane/Downloads/whatsapp_16k.wav")
    audio_float = data.astype(np.float32) / 32768.0

    print("Translating to English with faster-whisper...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_float, task="translate", word_timestamps=True)

    sentences = []
    words = []

    for s in segments:
        sentences.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()})
        if s.words:
            for w in s.words:
                words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})

    with open("/Users/brane/Downloads/transcription_english.json", "w", encoding="utf-8") as f:
        json.dump({"sentences": sentences, "words": words}, f, indent=2)

    print(f"English Translation Sentences count: {len(sentences)}")
    for s in sentences:
        print(f"[{s['start']}s -> {s['end']}s]: {s['text']}")

if __name__ == "__main__":
    main()
