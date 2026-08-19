# icho-reel-eng

Personal short-form media automation engine for **ichoTaKu**.

`icho-reel-eng` turns structured creator content into a deterministic production plan that can be orchestrated by n8n, rendered locally with FFmpeg, enriched by optional AI providers, reviewed, archived, and eventually published to Instagram Reels, YouTube Shorts, TikTok, and other destinations.

This repository is intentionally **creator-first** rather than content-farm-first. It prefers existing personal assets, gameplay, reusable brand media, and local rendering before spending money on generative APIs.

## Design principles

- Adaptive formats instead of a fixed avatar/B-roll ratio.
- Local-first media processing with cloud providers as replaceable adapters.
- JSON Schema contracts before expensive generation.
- Approval-first publishing by default.
- Every run is reproducible, inspectable, and archiveable.
- Brand profiles separate visual identity from workflow logic.
- n8n orchestrates; Python plans, validates, and prepares deterministic media work.

## Core pipeline

```text
content JSON
  -> validate
  -> normalize
  -> plan scenes
  -> resolve assets
  -> narration / audio
  -> composition manifest
  -> FFmpeg render
  -> QC
  -> approval package
  -> publish adapter
  -> archive + analytics metadata
```

## Repository map

```text
config/             brand and provider configuration
content/            example content packages
docs/               architecture and operator documentation
schemas/            JSON Schema contracts
src/icho_reel_eng/  Python engine
scripts/             command-line helpers
workflows/n8n/      n8n workflow contracts and importable starters
tests/               deterministic regression tests
.github/workflows/  CI
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
icho-reel validate content/examples/builder-commentary.json
icho-reel plan content/examples/builder-commentary.json --out runs/example-plan.json
```

FFmpeg is optional for validation/planning but required for local rendering.

```bash
ffmpeg -version
```

## Content modes

The initial contract supports:

- `builder_commentary`
- `gameplay_insight`
- `anthology_lore`
- `voiceover_broll`
- `music_visual`

Each content package chooses a `structure_mode`, `brand_profile`, target platforms, script, and asset strategy. The planner converts that into scenes without forcing a universal 30/70 format.

## Default brand profiles

- `ichotaku_default`
- `digitaldive`
- `heartbreak_alley`
- `eso_gaming`

See `config/brands/` and `docs/BRAND_GUIDE.md`.

## Safety rails

The v1 engine defaults to `approval` publishing mode. Publishing adapters are deliberately kept outside the render core, and secrets are never stored in content JSON or committed workflow exports.

## Current status

Foundation / MVP vertical-slice architecture. Validation, planning, manifests, local render-command generation, sample content, tests, CI, and n8n integration contracts are included. Provider-specific credential wiring and production social publishing remain opt-in deployment work.

See `docs/ROADMAP.md` and `CHANGELOG.md`.
