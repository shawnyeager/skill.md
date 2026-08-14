---
name: sideband-hero
description: Generate hero images for Sideband newsletter posts. Triggers on "hero image", "post image", "generate an image for this post", "make a hero". End-to-end — analysis, prompt, API call, download.
---

# Sideband Hero Image Generator

Every hero image is a spectrogram. Same instrument, different reading. Horizontal = time. Vertical = frequency. Color = amplitude. After a few posts, readers recognize the format instantly.

## Prerequisites

`REPLICATE_API_TOKEN` must be in the shell environment BEFORE launching Claude Code.
- Add to `~/.zshrc` or `~/.bashrc`: `export REPLICATE_API_TOKEN=r8_...`
- Or use `.claude/settings.local.json`: `{"env":{"REPLICATE_API_TOKEN":"r8_..."}}`
- Restart terminal, then launch Claude Code.

## Workflow

### 1. Get post text
User pastes, gives file path, or URL.

### 2. Analyze (silent)

- **Register**: Tension / Discovery / Warning / Convergence / Erosion / Threshold
- **Color Emphasis**: Cyan-dominant / Amber-dominant / Balanced
- **Narrative**: What's the left-to-right story? What state does the spectrogram start in, what happens, where does it end? Think in terms of contrast and transition — silence→explosion, order→chaos, buried→clear.
- **Signal Events**: Pick 1-2 from the library below. Single events work for simple posts. For posts with a pivot or transformation, compose two events into a sequence (e.g., silence on the left via one event, dense structure on the right via another). When composing, write a custom description that stitches them together — don't just concatenate the stock text.

### 3. Build prompt

CRITICAL RULES FOR PROMPT CONSTRUCTION:
- The FIRST line of every prompt must be the anti-text line. Always.
- NEVER use the word "paper" anywhere in the prompt.
- NEVER use the word "printed" anywhere in the prompt.
- NEVER use the word "CRT" anywhere in the prompt.
- NEVER say "matte paper", "dark paper", "thermal paper" — the model renders a literal photograph of paper on a table.
- NEVER say "vertical smearing", "film grain across the entire image", "heavy grain", "dense vertical-streak texture", or "striations filling every band". Each of these renders the fuzzy sweater — every band woven from thousands of tiny hairs.
- The image must fill the frame edge to edge. No borders, no margins, no visible edges.

DO NOT re-derive the style each roll. The structure paragraph below is locked. Swap ONLY the signal narrative.

WHAT MAKES IT READ AS A SPECTROGRAM (non-negotiable):
- MANY fine, thin, SHARP, high-contrast parallel horizontal harmonic lines stacked closely, brightest and densest in the center rows, fading toward the top and bottom of the zone, with dark navy visible between individual lines.
- Fine sharp vertical striations THROUGH the lines = amplitude changing across time.
- GENEROUS empty flat dark navy negative space above and below the signal zone. The signal is a horizontal band, NOT wall-to-wall.
- Crisp, thin, sharp, high contrast — like an FFT readout.

FAILURE MODES (each is a real past miss):
- Wall-to-wall soft striation covering the whole frame = fuzzy sweater.
- Flat uninterrupted solid ribbons or stripes = doesn't read as a spectrogram.
- Glossy 3D tubes, pipes, or vector shapes = overcorrection.
- Hard full-height vertical seam = split screen. A THIN, low-contrast green handover marker is fine and matches `the-real-tokenomics.webp`. Do NOT try to "fix" it by asking for a shorter zone-height marker: FLUX renders that as a saturated pure-green bar that becomes the brightest object in the frame, ignores off-center placement, and loses the thin-line structure. Leave it alone.

PROMPT TEMPLATE:

```
This image contains absolutely no text, no numbers, no letters, no labels, no axes, no tick marks, no legends, no characters of any kind.

A real audio spectrogram / FFT frequency analysis readout on a deep flat navy #1D2733 background, 16:9, filling the frame edge to edge with no borders. Horizontal direction is time, vertical direction is frequency, brightness is amplitude.

The signal occupies a horizontal zone across the middle of the frame, with GENEROUS empty flat dark navy negative space above and below it. The zone is built from MANY fine, thin, SHARP, high-contrast parallel horizontal harmonic lines stacked closely on top of one another, brightest and densest in the center rows and fading out toward the top and bottom edges of the zone, with dark navy visible between the individual lines. Fine sharp vertical striations run through the lines giving the sense of amplitude changing across time, some columns brighter, some quieter. Crisp and detailed like a frequency analysis readout, not soft, not blurry.

{{SIGNAL_NARRATIVE — 3-4 sentences. Which color dominates where, and the green overlap. Adapt the chosen Signal Event(s) from the library below into harmonic-line language: say "cyan #0EA5C9 harmonic lines dominate the LEFT" rather than "a cyan band". Always BOTH cyan #0EA5C9 AND amber #A97C40. Green #5B9B84 only at the overlap.}}

{{COLOR_EMPHASIS — "Cyan #0EA5C9 lines are brighter and more prominent than amber" OR "Amber #A97C40 lines are brighter and more prominent than cyan" OR "Cyan and amber lines compete at roughly equal brightness"}}

The lines are crisp, thin, and sharp with strong contrast against the dark navy. No soft fuzz, no woven or knitted fabric texture, no sweater, no flat uninterrupted solid ribbons or stripes, no blur, no haze, no glow, no bloom, no shine, no reflective surfaces, no rounded 3D tubes or cables. At most a barely perceptible film grain.

Absolutely no text, numbers, letters, axis labels, tick marks, grid lines, legends, UI elements, or any readable characters anywhere in the image. No hard full-height vertical seam splitting the image in two. No people, faces, or devices. Abstract only. 16:9 aspect ratio.
```

GOLD-STANDARD REFERENCES: `Heroes/the-real-tokenomics.webp` and `Heroes/cuda-is-the-x86-of-ai.webp`. Look at one before rolling.

### 4. Call API

Output goes to `Heroes/<post-slug>.webp` in the sideband.pub repo — never next to the source markdown, never a timestamped name in the current directory. Derive the slug from the post title (lowercase, hyphens, drop apostrophes and punctuation), matching the existing files in `Heroes/`.

Use python, not `curl -d`. The prompt contains quotes and newlines that break shell quoting.

```bash
python3 - <<'PY'
import json, os, urllib.request

prompt = """PASTE_THE_BUILT_PROMPT_HERE"""
slug = "post-slug-here"

body = json.dumps({"input": {"prompt": prompt, "aspect_ratio": "16:9",
                             "output_format": "webp", "output_quality": 95}}).encode()
req = urllib.request.Request(
    "https://api.replicate.com/v1/models/black-forest-labs/flux-2-pro/predictions",
    data=body,
    headers={"Authorization": "Bearer " + os.environ["REPLICATE_API_TOKEN"],
             "Content-Type": "application/json", "Prefer": "wait"})
r = json.load(urllib.request.urlopen(req, timeout=300))
out = r.get("output")
url = out if isinstance(out, str) else (out[0] if isinstance(out, list) and out else None)
print("status:", r.get("status"), "| error:", r.get("error"))
if not url: raise SystemExit("no output url")
dest = f"Heroes/{slug}.webp"
urllib.request.urlretrieve(url, dest)
print("saved:", dest, os.path.getsize(dest), "bytes")
PY
```

Before overwriting an existing hero, copy it to the scratchpad first. A re-roll changes the whole composition, and the previous render is often the better one.

### 5. Present result

1. `xdg-open Heroes/<slug>.webp` — always open it.
2. Read the file back with the Read tool and LOOK at it before saying anything about it. Never describe a render you have not viewed.
3. Report: signal event used, 1-sentence rationale, file path, and any flaw you can actually see.

Offer to try a different event. If the composition is good and only the texture or a detail is wrong, prefer a FLUX Kontext edit over a re-roll — a text-to-image re-roll rerolls the whole shape.

## Signal Event Library

These are building blocks, not final descriptions. Use one directly for straightforward posts. Compose two into a custom narrative for posts with a turn or transformation — write the stitched description yourself, emphasizing contrast and dynamic range between the two states.

IMPORTANT: these blocks supply the NARRATIVE only — which color goes where and what happens across time. The STRUCTURE always comes from the locked template above. Where a block says "band", write "harmonic lines" in the actual prompt. Never paste a block in verbatim.

### BROADBAND SPIKE
When: Discovery, sudden arrival, instant capability, "something just happened"
```
The left portion shows quiet low-level noise — faint speckle of cyan #0EA5C9 and amber #A97C40 scattered at random. Then a sudden bright vertical column of cyan #0EA5C9 erupts across all frequencies simultaneously. To the right of the spike, strong horizontal bands of cyan continue at elevated levels with clear harmonic structure. Amber #A97C40 bands are visible in the lower frequencies, running beneath the dominant cyan signal.
```

### CLEAN CARRIER
When: Confidence, clarity, something working as designed
```
A strong steady horizontal band of cyan #0EA5C9 runs across the middle frequencies, consistent left to right. Below it, a narrower amber #A97C40 band runs parallel at lower frequencies, steady but dimmer. The two bands maintain separation with dark navy between them. Faint green #5B9B84 appears at the edges where the bands are closest. The rest of the spectrum is dark and quiet.
```

### INTERFERENCE
When: Erosion, extraction overriding empowerment, something being drowned
```
A cyan #0EA5C9 signal band runs horizontally across mid-frequencies. A broader amber #A97C40 band encroaches from above and below, spreading across adjacent frequencies, overlapping the cyan. Where they overlap, muddy green #5B9B84 appears. The amber grows brighter and wider toward the right side while the cyan narrows and dims. The amber is winning.
```

### CONVERGENCE
When: Two things merging, alignment, agreement
```
Two distinct horizontal bands — cyan #0EA5C9 in the upper frequencies and amber #A97C40 in the lower frequencies — run from left to right. Moving rightward, the bands curve toward each other, closing the gap. On the far right they nearly touch, and bright green #5B9B84 appears between them. Two signals becoming one.
```

### DIVERGENCE
When: Splitting, things pulling apart, fracture
```
A single band of green #5B9B84 on the left side. Moving rightward, it splits — cyan #0EA5C9 curving up to higher frequencies, amber #A97C40 curving down to lower frequencies. The gap widens toward the right edge. Green disappears as the split completes. One signal becoming two.
```

### FADE
When: Erosion, loss, something weakening
```
On the left, strong bright cyan #0EA5C9 fills several frequency bands with structure and harmonics. Moving right, the signal dims — amplitude dropping, bands thinning. By the right third, only a faint ghost remains. Amber #A97C40 speckle in the noise floor becomes more visible as the cyan fades. The signal is dying.
```

### EMERGENCE
When: Threshold, new signal appearing, early detection
```
Mostly dark noise floor with faint ambient speckle. In the lower-right area, a new cyan #0EA5C9 band materializes out of the noise — narrow, faint, but distinctly present. Scattered amber #A97C40 noise at various frequencies elsewhere. Something new is starting to transmit. It's barely there but it's real.
```

### HARMONICS
When: Proliferation, building on foundation, stacking
```
A strong fundamental cyan #0EA5C9 band in the lower frequencies. Above it at regular intervals, progressively fainter harmonic bands stack upward — each thinner and dimmer than the one below. Amber #A97C40 bands sit between the harmonics at their own distinct frequencies. The pattern fills the vertical space with an alternating ladder of cyan and amber.
```

### JAMMING
When: Warning, hostile takeover, extraction at scale
```
Dense bright amber #A97C40 fills most of the spectrogram across nearly all frequencies. A thin cyan #0EA5C9 band is barely visible running through the middle, mostly buried. The amber is too uniform to be natural noise — this is deliberate interference. The cyan signal persists but you have to look for it.
```

### SIGNAL IN NOISE
When: Tension, clarity persisting through chaos
```
Dense amber #A97C40 speckle fills the entire spectrogram at moderate levels. Through the middle frequencies, a narrow cyan #0EA5C9 band cuts horizontally — not much brighter than the noise but coherent and continuous where the noise is random. You can follow the cyan line left to right even though the amber tries to obscure it.
```

## Brand Constraints

- Background: solid navy #1D2733, edge to edge
- Cyan #0EA5C9 = primary signal, empowerment, clarity
- Amber #A97C40 = interference, extraction, stakes
- Green #5B9B84 = overlap only, where cyan and amber interact
- EVERY image must include BOTH cyan and amber. Never mono-color.
- Format: spectrogram — horizontal=time, vertical=frequency, color=amplitude
- NO text, axis labels, grid lines, numbers, letters — ever
- NO glow, bloom, neon, light emission
- NO paper, borders, margins, edges, frames, surfaces
- 16:9 aspect ratio

## Cost
~$0.05/image via Replicate FLUX.2 Pro.
