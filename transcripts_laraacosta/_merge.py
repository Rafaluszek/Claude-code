from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "_txt"
OUT = ROOT / "_ALL_transcripts.txt"

files = sorted(SRC.glob("*.txt"))
parts = []
for i, f in enumerate(files, 1):
    body = f.read_text(encoding="utf-8")
    parts.append(f"\n\n{'='*80}\n# [{i}/{len(files)}] {f.stem}\n{'='*80}\n\n{body}")

OUT.write_text("".join(parts).lstrip(), encoding="utf-8")
print(f"Merged {len(files)} files -> {OUT} ({OUT.stat().st_size/1024:.1f} KB)")
