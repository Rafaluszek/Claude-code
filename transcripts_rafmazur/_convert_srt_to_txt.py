import os, re, glob
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "_txt"
OUT.mkdir(exist_ok=True)

TS_LINE = re.compile(r"^\d{2}:\d{2}:\d{2}[,.]\d{3} --> \d{2}:\d{2}:\d{2}[,.]\d{3}")
TAGS = re.compile(r"<[^>]+>")
SEQ = re.compile(r"^\d+$")

def srt_to_text(path: Path) -> str:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    out = []
    last = None
    for ln in lines:
        s = ln.strip()
        if not s: continue
        if TS_LINE.match(s): continue
        if SEQ.match(s): continue
        s = TAGS.sub("", s)
        s = re.sub(r"\s+", " ", s).strip()
        if not s: continue
        if s == last: continue
        out.append(s)
        last = s
    return "\n".join(out)

files = sorted(ROOT.glob("*.srt"))
groups = {}
for f in files:
    m = re.match(r"(.*) \[([A-Za-z0-9_-]{11})\]\.([a-zA-Z-]+)\.srt$", f.name)
    if not m: continue
    title, vid, lang = m.group(1), m.group(2), m.group(3)
    groups.setdefault(vid, {"title": title, "langs": {}})
    groups[vid]["langs"][lang] = f

# Polish channel — prefer pl-orig, fallback pl, then en
LANG_PREF = ["pl-orig", "pl", "en-orig", "en-US", "en-GB", "en"]

count = 0
for vid, info in groups.items():
    chosen = None
    for L in LANG_PREF:
        if L in info["langs"]:
            chosen = (L, info["langs"][L])
            break
    if not chosen: continue
    lang, src = chosen
    text = srt_to_text(src)
    out_name = f"{info['title']} [{vid}].txt"
    (OUT / out_name).write_text(
        f"# {info['title']}\n# https://www.youtube.com/watch?v={vid}\n# lang: {lang}\n\n{text}\n",
        encoding="utf-8"
    )
    count += 1

print(f"Wrote {count} .txt files to {OUT}")
