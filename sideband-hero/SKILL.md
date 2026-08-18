---
name: sideband-hero
description: Use when the user asks for a Sideband hero image, post image, /sideband-hero, or a spectrogram for a Sideband post.
---

# Sideband Hero

Every hero is a spectrogram. Horizontal = time. Vertical = frequency. Brightness = amplitude. Cyan `#0EA5C9` is the signal. Amber `#A97C40` is the stakes. Green `#5B9B84` appears only where they meet. Navy `#1D2733` is the field.

Look at existing files in `Heroes/` before a roll. No single file is the style. Do not add new bans after a fail.

`REPLICATE_API_TOKEN` must already be in the environment. Cost is about $0.05 per roll.

## Loop

1. Read the post.
2. Open two or three files in `Heroes/` with the Read tool. Calibrate. Pick a `--ref` only when one hero already tells this post's story.
3. Pick register, color emphasis, and 1–2 events. Stay silent.
4. Write the short prompt below. Swap only the story.
5. From the sideband.pub repo root, run the skill script. Never raw `curl`.

```bash
python3 .claude/skills/sideband-hero/generate.py <slug> [--ref Heroes/<analog>.webp] <<'PROMPT'
<prompt>
PROMPT
xdg-open Heroes/<slug>.webp
```

Slug comes from the post title: lowercase, hyphens, no punctuation. Output is always `Heroes/<slug>.webp`.

6. Read the new file. Apply the gates. A fail is a fail — do not present it as a texture note.
7. On fail, re-roll the **same** prompt. Do not lengthen it. Stop after 3 rolls and show the closest attempt.

## Prompt

Four parts. Nothing else.

```
This image contains absolutely no text, no numbers, no letters, no labels, no axes, no tick marks, no legends, no characters of any kind.

Deep navy #1D2733. 16:9. Edge to edge. A spectrogram. Horizontal is time. Brightness is amplitude.

{{STORY — 2–3 sentences. Which color dominates where, left to right. Both cyan #0EA5C9 and amber #A97C40. Green #5B9B84 only where they meet. Write "harmonic lines", never "band".}}

{{EMPHASIS — one of:
Cyan #0EA5C9 lines are brighter and more prominent than amber
Amber #A97C40 lines are brighter and more prominent than cyan
Cyan and amber lines compete at roughly equal brightness}}
```

The script rejects these words in the prompt: `paper`, `printed`, `crt`, `readout`, `software`, `interface`, `sweater`, `striation`, `generous`, `fft`.

## Gates

Look at the render. Compare it to the `Heroes/` set. Reject if any of these are true:

| Fail | What you see |
|---|---|
| Text | Numbers, letters, axes, sidebar, scale, UI |
| Stamp | A boxed strip floating in empty navy |
| Coil | Heating-coil, barcode, or knit wrapping the frame |
| Sweater | Soft woven hash with no horizontal harmonic structure |
| Ribbons | Flat solid stripes with no amplitude texture |
| Copy | A clone of the `--ref` file |

Pass looks like a Sideband hero: spectrogram, both cyan and amber, navy field, no text.

## Events

Use these for the story only. Rewrite into harmonic-line language. Do not paste them.

**BROADBAND SPIKE** — Discovery, sudden arrival. Quiet speckle, then a bright cyan column, then elevated cyan lines with amber underneath.

**CLEAN CARRIER** — Clarity, something working. Steady cyan mid-frequency lines. Narrower amber below. Navy between. Green only at the closest edges.

**INTERFERENCE** — Extraction drowning the signal. Amber lines spread and brighten to the right. Cyan narrows. Green in the overlap. Amber wins.

**CONVERGENCE** — Two things merging. Cyan above, amber below, closing toward the right. Green where they meet.

**DIVERGENCE** — Split. Green on the left becomes cyan up and amber down. Gap widens.

**FADE** — Loss. Bright cyan on the left thins to a ghost. Amber speckle shows as cyan dies.

**EMERGENCE** — Threshold. Dark field. A narrow cyan line appears lower-right. Amber speckle elsewhere.

**HARMONICS** — Stacking. Strong cyan fundamental below. Fainter cyan copies above. Amber lines between.

**JAMMING** — Hostile takeover. Dense amber across most frequencies. A thin cyan line still visible.

**SIGNAL IN NOISE** — Tension. Amber speckle everywhere. A coherent cyan line holds through the middle.

Compose two events when the post turns. Write the stitch yourself.

## After a pass

Report event, one-sentence rationale, and `Heroes/<slug>.webp`. Offer a different event. If only a small detail is wrong, edit with FLUX Kontext. Do not re-roll the whole shape.
