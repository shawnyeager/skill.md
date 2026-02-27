# skill.md

Claude Code skills I build and use.

## Install

Copy any skill directory into your project:

```bash
# clone and copy what you need
git clone https://github.com/shawnyeager/skill.md.git
cp -r skill.md/sideband-hero your-project/.claude/skills/

# or grab a single skill with degit
npx degit shawnyeager/skill.md/sideband-hero .claude/skills/sideband-hero
```

Skills activate automatically when Claude Code detects matching intent from the `description` field in the SKILL.md frontmatter.

## Skills

### [sideband-hero](sideband-hero/SKILL.md)

Generates hero images for the [Sideband](https://sideband.pub) newsletter. Reads a post, analyzes its register (tension, discovery, warning, convergence, erosion, threshold), selects from a library of ten spectrogram signal patterns, builds a constrained prompt, and calls [FLUX.2 Pro](https://replicate.com/black-forest-labs/flux-2-pro) on Replicate.

Most of the skill is prohibitions — every constraint exists because FLUX generated an image that failed in that specific way.

**Requires:** `REPLICATE_API_TOKEN` env var ([get one](https://replicate.com/account/api-tokens))
**Cost:** ~$0.05/image
**Trigger:** `/sideband-hero`, "hero image", "generate an image for this post"
