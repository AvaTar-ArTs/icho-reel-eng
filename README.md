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
- Existing AvaTar-ArTs repositories keep authority over the domains they already model well.
- Cross-repository integrations use pinned commits and narrow interchange contracts rather than copy/paste coupling.

## Core pipeline

```text
content JSON
  -> validate
  -> normalize
  -> capability / ecosystem plan
  -> plan scenes
  -> resolve assets
  -> optional storyboard / generated visuals
  -> narration / audio
  -> composition manifest
  -> FFmpeg render
  -> QC
  -> approval package
  -> publish adapter
  -> archive + provenance + release metadata
```

## Ecosystem position

The evolved engine is the **short-form production compiler** inside the larger AvaTar-ArTs creator stack.

```text
content-universe   durable assets, provenance, lineage, creative graph
agent-skills       broad authored skill and agent source ecosystem
superSkills        curated reusable capability catalog
superAgents        deterministic agent routing, approvals, execution audit
creator-camp       canon-to-release and rights-aware creator workflow
my-creators        local storyboard/image generation and adapter training
icho-reel-eng      short-form planning, composition, QC, approval, publishing
n8n                orchestration and event transport
FFmpeg             deterministic audiovisual render foundation
```

Pinned source commits and capability/authority boundaries live in `config/ecosystem/sources.json`.

See `docs/ECOSYSTEM_AUDIT_2026-08-19.md` for the cross-repository audit and integration decisions.

## Repository map

```text
config/
  brands/           visual identity profiles
  ecosystem/        pinned source catalog + capability mappings
content/            example content packages
docs/               architecture, operations, audit, and brand documentation
schemas/            JSON Schema contracts
src/icho_reel_eng/  Python engine, ecosystem planner, and bridge contracts
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

## Cross-repository bridges

`src/icho_reel_eng/bridges.py` currently defines two narrow handoff contracts:

1. **my-creators storyboard bridge**
   - compiles a reel scene into a shot-manifest shaped record
   - preserves project/scene/shot identity, duration, style profile, seed policy, references, and generation metadata

2. **Content Universe artifact bridge**
   - emits a narrow registration envelope for rendered video assets
   - preserves typed asset identity, SHA-256, parent lineage, brand profile, structure mode, and content identity

These are intentionally adapters, not local copies of either repository's internal model.

## Default brand profiles

- `ichotaku_default`
- `digitaldive`
- `heartbreak_alley`
- `eso_gaming`

See `config/brands/` and `docs/BRAND_GUIDE.md`.

## Safety rails

The v1 engine defaults to `approval` publishing mode. Publishing adapters are deliberately kept outside the render core, and secrets are never stored in content JSON or committed workflow exports.

The ecosystem integration adds two more rules:

- agent selection never implies permission to execute an external write
- broad `agent-skills` content is not promoted directly into production without curation/validation

## Current status

Foundation plus ecosystem-integration evolution. Validation, planning, manifests, provider protocols, pinned ecosystem sources, capability selection, local storyboard handoffs, provenance handoffs, sample content, tests, CI, and n8n integration contracts are included.

The next vertical slice is:

```text
JSON
 -> validate
 -> ecosystem capability plan
 -> scene plan
 -> Content Universe/local asset resolution
 -> my-creators visual shot handoff where needed
 -> narration/captions
 -> FFmpeg render
 -> ffprobe QC
 -> approval package
 -> platform publish
 -> Content Universe registration
```

See `docs/ROADMAP.md`, `docs/ECOSYSTEM_AUDIT_2026-08-19.md`, and `CHANGELOG.md`.
