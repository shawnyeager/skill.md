#!/usr/bin/env python3
"""Generate a Sideband hero. cwd must be the sideband.pub repo.

Usage:
  python3 generate.py <slug> <<'PROMPT'
  ...prompt text...
  PROMPT
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import sys
import time
import urllib.request
from pathlib import Path

BANNED = (
    "paper",
    "printed",
    "crt",
    "readout",
    "software",
    "interface",
    "sweater",
    "striation",
    "generous",
    "fft",
)
REF = Path("Heroes/the-real-tokenomics.webp")
SCRATCH = Path("/tmp/sideband-hero-scratch")
API = "https://api.replicate.com/v1/models/black-forest-labs/flux-2-pro/predictions"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: generate.py <slug>")
    slug = sys.argv[1]
    prompt = sys.stdin.read().strip()
    if not prompt:
        raise SystemExit("empty prompt on stdin")

    hits = [w for w in BANNED if w in prompt.lower()]
    if hits:
        raise SystemExit("banned word in prompt: " + ", ".join(hits))

    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        raise SystemExit("REPLICATE_API_TOKEN is not set")
    if not REF.is_file():
        raise SystemExit(f"missing reference: {REF} (cwd must be sideband.pub)")

    dest = Path("Heroes") / f"{slug}.webp"
    dest.parent.mkdir(exist_ok=True)
    if dest.exists():
        SCRATCH.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dest, SCRATCH / dest.name)
        print("scratch:", SCRATCH / dest.name)

    data_uri = "data:image/webp;base64," + base64.b64encode(REF.read_bytes()).decode()
    body = json.dumps(
        {
            "input": {
                "prompt": prompt,
                "input_images": [data_uri],
                "aspect_ratio": "16:9",
                "output_format": "webp",
                "output_quality": 95,
            }
        }
    ).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
    )
    r = json.load(urllib.request.urlopen(req, timeout=60))
    pred_id = r.get("id")
    get_url = r.get("urls", {}).get("get") or f"https://api.replicate.com/v1/predictions/{pred_id}"
    print("created:", pred_id, "status:", r.get("status"))

    deadline = time.time() + 280
    while r.get("status") in ("starting", "processing"):
        if time.time() > deadline:
            raise SystemExit(f"timed out waiting for {pred_id}")
        time.sleep(5)
        req = urllib.request.Request(get_url, headers={"Authorization": "Bearer " + token})
        r = json.load(urllib.request.urlopen(req, timeout=60))
        print("poll:", r.get("status"))

    out = r.get("output")
    url = out if isinstance(out, str) else (out[0] if isinstance(out, list) and out else None)
    print("status:", r.get("status"), "| error:", r.get("error"))
    if not url:
        raise SystemExit("no output url")
    urllib.request.urlretrieve(url, dest)
    print("saved:", dest, dest.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
