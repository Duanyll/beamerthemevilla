#!/usr/bin/env bash
# Generate ONE illustration via the OpenAI-compatible relay (GPT-Image-2 / -1).
#
#   bash tools/gen-image.sh <prompt-file> <out.png> [model] [size] [quality]
#     model:   gpt-image-2 (default) | gpt-image-1
#     size:    1536x1024 (default, landscape) | 1024x1024 | 1024x1536
#     quality: high (default) | medium | low
#
# Reads OPENAI_BASE / OPENAI_KEY from .env. GPT-Image returns base64 (b64_json),
# which we decode to PNG. SLOW: a single high-quality image takes several minutes.
# Cost is per-token (~high 1536x1024 ≈ a few thousand output tokens); test with low.
set -euo pipefail
PF="${1:?usage: gen-image.sh <prompt-file> <out.png> [model] [size] [quality]}"
OUT="${2:?need output png path}"
MODEL="${3:-gpt-image-2}"; SIZE="${4:-1536x1024}"; QUAL="${5:-high}"
REPO="$(cd "$(dirname "$0")/.." && pwd)"
set -a; source "$REPO/.env"; set +a
echo "[gen-image] model=$MODEL size=$SIZE quality=$QUAL -> $OUT (may take minutes)"
python3 - "$OPENAI_BASE" "$OPENAI_KEY" "$MODEL" "$SIZE" "$QUAL" "$OUT" "$PF" <<'PY'
import sys, json, base64, urllib.request
base, key, model, size, qual, out, pf = sys.argv[1:8]
prompt = open(pf, encoding="utf-8").read()
body = json.dumps({"model": model, "prompt": prompt, "n": 1,
                   "size": size, "quality": qual}).encode()
req = urllib.request.Request(base + "/images/generations", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.load(r)
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode("utf-8", "replace")[:600]); sys.exit(1)
if "data" not in d or not d["data"]:
    print("ERROR no data:", json.dumps(d)[:600]); sys.exit(1)
item = d["data"][0]
if item.get("b64_json"):
    open(out, "wb").write(base64.b64decode(item["b64_json"]))
elif item.get("url"):
    urllib.request.urlretrieve(item["url"], out)
else:
    print("ERROR no image payload:", json.dumps(item)[:300]); sys.exit(1)
print("saved", out, "usage=", d.get("usage"))
PY