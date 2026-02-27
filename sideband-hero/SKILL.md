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
- The image must fill the frame edge to edge. No borders, no margins, no visible edges.

PROMPT TEMPLATE:

```
This image contains absolutely no text, no numbers, no letters, no labels, no axes, no tick marks, no legends, no characters of any kind.

Abstract digital artwork of a spectrogram visualization filling the entire frame edge to edge. Navy #1D2733 background covers the full canvas with no borders or margins. Horizontal direction represents time. Vertical direction represents frequency. Brightness represents amplitude.

{{SIGNAL_EVENT — 3-4 sentences from the library below. Always mention BOTH cyan #0EA5C9 AND amber #A97C40 explicitly. Green #5B9B84 only where they overlap.}}

{{COLOR_EMPHASIS — "Cyan #0EA5C9 bands are brighter and more prominent than amber" OR "Amber #A97C40 bands are brighter and more prominent than cyan" OR "Cyan and amber bands compete at roughly equal brightness"}}

The visualization has subtle horizontal scan line texture and slight vertical smearing where signals are strong. Colors are flat and opaque. No glow, no bloom, no light emission, no luminosity, no shine, no reflective surfaces. Film grain across the entire image.

Absolutely no text, numbers, letters, axis labels, tick marks, grid lines, legends, UI elements, or any readable characters anywhere in the image. No people, faces, or devices. Abstract only. 16:9 aspect ratio.
```

### 4. Call API

```bash
RESULT=$(curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d '{
    "input": {
      "prompt": "YOUR_PROMPT_HERE",
      "aspect_ratio": "16:9",
      "output_format": "webp",
      "output_quality": 95
    }
  }' \
  https://api.replicate.com/v1/models/black-forest-labs/flux-2-pro/predictions)

IMAGE_URL=$(echo "$RESULT" | python3 -c "import sys,json; r=json.load(sys.stdin); o=r.get('output',''); print(o if isinstance(o,str) else o[0] if isinstance(o,list) else '')" 2>/dev/null)

FILENAME="hero-$(date +%Y%m%d-%H%M%S).webp"
curl -s -o "$FILENAME" "$IMAGE_URL"
echo "Downloaded: $FILENAME"
```

### 5. Present result
Signal event used, 1-sentence rationale, file path. Offer to try different event.

## Signal Event Library

These are building blocks, not final descriptions. Use one directly for straightforward posts. Compose two into a custom narrative for posts with a turn or transformation — write the stitched description yourself, emphasizing contrast and dynamic range between the two states.

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
