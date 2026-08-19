# Roadmap

## Phase 0 — Foundation

- [x] Repository structure
- [x] Creator-facing content JSON Schema
- [x] Deterministic planner
- [x] Render manifest starter
- [x] Brand profiles
- [x] Example content packages
- [x] CLI validation / planning
- [x] Tests and CI
- [x] n8n orchestration boundary

## Phase 1 — Local vertical slice

Goal: one content package produces a reviewable 9:16 MP4 without paid video generation.

- [ ] Asset binding contract
- [ ] Local filesystem asset index
- [ ] Narration input adapter
- [ ] SRT/VTT caption generation
- [ ] FFmpeg scene rendering
- [ ] FFmpeg concat / audio mixing
- [ ] Brand-safe title and CTA cards
- [ ] ffprobe QC checks
- [ ] Approval package directory
- [ ] Golden-media regression fixture

Definition of done:

```text
JSON -> validate -> plan -> bind assets -> render -> QC -> preview package
```

## Phase 2 — n8n production orchestration

- [ ] Webhook intake workflow
- [ ] Batch intake workflow
- [ ] Run-state persistence
- [ ] Stage-specific retries
- [ ] Error workflow / dead-letter queue
- [ ] Webhook callbacks for asynchronous providers
- [ ] Approval notification flow
- [ ] Manual resume after revision

## Phase 3 — Provider adapters

Add providers only behind capability interfaces.

### Voice
- [ ] OpenAI TTS adapter
- [ ] ElevenLabs adapter
- [ ] creator-recorded voice path

### Avatar
- [ ] HeyGen optional adapter
- [ ] mascot / image-driven alternative

### Image / video
- [ ] OpenAI image adapter
- [ ] local ComfyUI adapter
- [ ] generated-video adapter selected per need

### Rendering
- [ ] FFmpeg production renderer
- [ ] optional Shotstack / Creatomate adapter

## Phase 4 — Asset intelligence

- [ ] Asset metadata schema
- [ ] SQLite/Postgres asset catalog
- [ ] semantic tags
- [ ] duplicate detection
- [ ] visual/style tags
- [ ] creator project / series relationships
- [ ] reuse history
- [ ] provenance / licensing fields
- [ ] archive-first resolver scoring

## Phase 5 — Brand systems

- [ ] ichoTaKu default motion kit
- [ ] DigitalDive information-card kit
- [ ] Heartbreak Alley / Trashcat anthology kit
- [ ] ESO gameplay overlay kit
- [ ] subtitle style registry
- [ ] intro / outro registry
- [ ] lower-third registry
- [ ] safe-zone validation

## Phase 6 — Publishing

- [ ] Meta / Instagram publishing adapter
- [ ] YouTube Shorts adapter
- [ ] TikTok adapter where account/API access permits
- [ ] platform-specific caption packages
- [ ] schedule state
- [ ] publish receipt storage
- [ ] retry / idempotency protection

## Phase 7 — Feedback loop

- [ ] performance metric ingestion
- [ ] content-family analytics
- [ ] hook / duration / visual density comparisons
- [ ] asset reuse performance
- [ ] cost per published short
- [ ] human notes on why edits were accepted/rejected
- [ ] optional recommendation agent

## North star

The mature system should be able to transform any useful ichoTaKu source object, including a script, gameplay discovery, project update, lore fragment, image series, code demo, or archive item, into one or more intentional short-form media packages while preserving creator control and source provenance.
