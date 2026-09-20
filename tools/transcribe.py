# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8")
from faster_whisper import WhisperModel
wav = sys.argv[1]; out = sys.argv[2]
model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe(wav, language="vi", vad_filter=True,
                                  vad_parameters=dict(min_silence_duration_ms=500))
lines = []
with open(out, "w", encoding="utf-8") as f:
    for s in segments:
        t = f"[{int(s.start//60):02d}:{int(s.start%60):02d}] {s.text.strip()}"
        f.write(t + "\n")
        print(t, flush=True)
