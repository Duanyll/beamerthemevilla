#!/usr/bin/env python3
"""Generate ONE illustration via the OpenAI-compatible relay (GPT-Image-2 / -1).

Usage:
    python3 tools/gen-image.py <prompt-file> <out.png> \
        [--model gpt-image-2] [--size 1536x1024] [--quality high] [--n 1]

Reads OPENAI_BASE / OPENAI_KEY from the repo-root .env (an OpenAI-compatible
relay; env vars of the same name override). POSTs to {OPENAI_BASE}/images/
generations and decodes the returned base64 (b64_json) to <out.png>.

SLOW: a high-quality 1536x1024 image takes minutes; cost is per output-token,
so test with --quality low. Full API schema + key troubleshooting:
    .claude/skills/make-slides/references/gpt-image.md

Stdlib only (urllib) — runs under plain `python3` or `uv run python …`.
"""
import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

REPO = pathlib.Path(__file__).resolve().parent.parent


def load_dotenv(path):
    """Minimal KEY=VALUE reader (ignores blanks / # comments / surrounding quotes)."""
    env = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def main():
    ap = argparse.ArgumentParser(
        description="Generate one image via the OpenAI-compatible GPT-Image relay.")
    ap.add_argument("prompt_file", help="path to a text file holding the prompt")
    ap.add_argument("out", help="output .png path")
    ap.add_argument("--model", default="gpt-image-2",
                    help="gpt-image-2 (default) | gpt-image-1.5 | gpt-image-1")
    ap.add_argument("--size", default="1536x1024",
                    help="1536x1024 (default, landscape) | 1024x1024 | 1024x1536 | WxH")
    ap.add_argument("--quality", default="high",
                    choices=["low", "medium", "high", "auto"],
                    help="high (default); use low to test cheaply")
    ap.add_argument("--n", type=int, default=1, help="number of images (default 1)")
    args = ap.parse_args()

    env = load_dotenv(REPO / ".env")
    base = os.environ.get("OPENAI_BASE") or env.get("OPENAI_BASE")
    key = os.environ.get("OPENAI_KEY") or env.get("OPENAI_KEY")
    if not base or not key:
        sys.exit("error: OPENAI_BASE / OPENAI_KEY not found (set them in the repo-root .env)")

    prompt = pathlib.Path(args.prompt_file).read_text(encoding="utf-8")
    print(f"[gen-image] model={args.model} size={args.size} quality={args.quality} "
          f"-> {args.out} (may take minutes)")

    body = json.dumps({"model": args.model, "prompt": prompt, "n": args.n,
                       "size": args.size, "quality": args.quality}).encode()
    req = urllib.request.Request(
        base.rstrip("/") + "/images/generations", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")

    items = data.get("data") or []
    if not items:
        sys.exit(f"error: no image data in response: {json.dumps(data)[:600]}")
    item = items[0]
    out = pathlib.Path(args.out)
    if item.get("b64_json"):
        out.write_bytes(base64.b64decode(item["b64_json"]))
    elif item.get("url"):
        urllib.request.urlretrieve(item["url"], out)
    else:
        sys.exit(f"error: no image payload (b64_json/url): {json.dumps(item)[:300]}")
    print(f"saved {out}  usage={data.get('usage')}")


if __name__ == "__main__":
    main()
