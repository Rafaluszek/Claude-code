import sys, time
from pathlib import Path
from faster_whisper import WhisperModel

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(r"C:/Users/laea1/Downloads/2. LinkedIn Outreach-20260510T115859Z-3-001/2. LinkedIn Outreach")
OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

videos = sorted(ROOT.rglob("*.mp4"))
print(f"Found {len(videos)} videos", flush=True)

print("Loading model: base (CPU, int8)...", flush=True)
t0 = time.time()
model = WhisperModel("base", device="cpu", compute_type="int8")
print(f"Model loaded in {time.time()-t0:.1f}s", flush=True)

for i, vid in enumerate(videos, 1):
    rel = vid.relative_to(ROOT)
    safe_stem = rel.with_suffix("").as_posix().replace("/", " __ ")
    out_txt = OUT / f"{safe_stem}.txt"
    if out_txt.exists() and out_txt.stat().st_size > 0:
        print(f"[{i}/{len(videos)}] SKIP (exists): {rel}", flush=True)
        continue
    print(f"[{i}/{len(videos)}] {rel}", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(
        str(vid),
        language="en",
        vad_filter=True,
        beam_size=1,
    )
    lines = []
    for seg in segments:
        text = seg.text.strip()
        if text:
            lines.append(text)
    body = "\n".join(lines)
    header = f"# {rel.as_posix()}\n# duration: {info.duration:.1f}s\n# language: {info.language} (p={info.language_probability:.2f})\n\n"
    out_txt.write_text(header + body + "\n", encoding="utf-8")
    print(f"  -> {out_txt.name}  ({time.time()-t0:.1f}s, {len(lines)} segments)", flush=True)

print("DONE", flush=True)
