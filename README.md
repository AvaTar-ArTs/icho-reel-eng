# icho-reel-eng

A personal short-form media compiler for **ichoTaKu**.

`icho-reel-eng` turns structured creator inputs into deterministic production packages for Reels, Shorts, and TikTok while delegating durable asset identity, visual generation, agent routing, and canon/release concerns to the wider AvaTar-ArTs ecosystem.

## What it owns

- short-form content planning
- scene compilation
- archive-first asset resolution
- subtitle/cue contracts
- render manifests
- local FFmpeg-oriented composition boundaries
- ffprobe technical QC
- approval packaging
- publishing orchestration contracts
- final Content Universe provenance handoff

## What it deliberately does not duplicate

- **Content Universe**: durable assets, provenance, lineage, collections, retrieval
- **my-creators**: storyboard/image-generation contracts and local ComfyUI-family execution
- **SuperAgents**: capability routing, agent selection, verification, approval semantics
- **SuperSkills**: curated reusable capability vocabulary
- **agent-skills**: broad authored skill/agent laboratory
- **Creator Camp**: canon, IP, rights, release evidence, adaptation lineage

## Evolved architecture

```text
superSkills
    │
superAgents
    │
Creator input ──► icho-reel-eng
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
content-universe  my-creators  creator-camp
        │           │            │
        └───────────┼────────────┘
                    ▼
             resolved scene pack
                    │
             narration + captions
                    │
                  FFmpeg
                    │
               ffprobe QC
                    │
              approval package
                    │
        Instagram / Shorts / TikTok
                    │
             Content Universe
          provenance registration
```

## v0.3 compiler flow

1. Validate a creator content package.
2. Plan scenes deterministically.
3. Resolve existing assets from Content Universe first.
4. Fall back to local filesystem archives.
5. If no suitable asset exists, emit a my-creators storyboard-generation request.
6. Build subtitle cues with content/scene provenance.
7. Build a vertical render manifest.
8. Route required capabilities through a SuperAgents request envelope.
9. Render with the local media layer.
10. Verify dimensions, duration, video/audio streams, and output presence with ffprobe.
11. Produce an approval package.
12. Publish only after explicit approval through platform adapters.
13. Register the final derived artifact back into Content Universe.
14. For narrative/IP content, attach Creator Camp canon and rights lineage.

## Core modules

```text
src/icho_reel_eng/
├── core.py             # validation, planning, render manifest
├── ecosystem.py        # pinned ecosystem routing and ownership
├── bridges.py          # my-creators + Content Universe handoffs
├── asset_resolver.py   # Content Universe + filesystem resolution
├── compiler.py         # deterministic production-package compiler
├── contracts.py        # subtitles, approval, SuperAgents, Creator Camp
├── qc.py               # ffprobe technical QC
├── publishing.py       # platform-neutral publish contracts
├── providers.py        # provider capability interfaces
└── cli.py              # local operator commands
```

## Archive-first asset strategy

The compiler prefers creator-owned history over needless generation:

```text
Content Universe
      ↓
local archive
      ↓
existing gameplay / screenshots / generated work
      ↓
my-creators generation request
      ↓
external paid generation only when intentionally configured
```

This makes prior ichoTaKu work active creative memory rather than cold storage.

## Approval-first publishing

Publishing is intentionally fail-closed. The provided `DryRunPublisher` is non-destructive, and the n8n v0.3 workflow ends at an approval gate until real platform credentials and explicit publish adapters are configured.

Supported publish contract targets:

- Instagram
- YouTube Shorts
- TikTok

## Content modes

The engine is designed around multiple ichoTaKu modes rather than a fixed avatar/B-roll ratio:

- builder / automation commentary
- ESO and gameplay insight
- DigitalDive knowledge clips
- Heartbreak Alley / Love Is Rubbish / Trashcat anthology
- music and visual experiments
- future mixed-media story adaptations

## Schemas

- `schemas/content.schema.json`
- `schemas/run.schema.json`
- `schemas/approval-package.schema.json`

## n8n

Starter workflows live in `workflows/n8n/`.

The evolved `02_compile_review_publish.json` workflow is intentionally review-first. It creates a normalized run, compiles plan/manifests, then returns an approval gate rather than silently publishing.

## Development

```bash
python -m pip install -e '.[dev]'
pytest
ruff check .
```

FFmpeg and ffprobe are expected for real rendering/QC workflows.

## Design rule

The Reel Engine is a **compiler, not the universe**.

It consumes curated capabilities and creator memory, produces reproducible media artifacts, and hands durable knowledge back to the systems that own it.
