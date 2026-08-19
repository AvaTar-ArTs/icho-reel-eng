# Architecture

## Purpose

`icho-reel-eng` is a personal creator-media engine for ichoTaKu. It separates orchestration, deterministic planning, rendering, provider integrations, publishing, and archival concerns so each can evolve independently.

## System boundaries

```text
                       +----------------------+
                       |  Content source(s)   |
                       | JSON / webhook / UI  |
                       +----------+-----------+
                                  |
                                  v
+----------------+      +---------+----------+      +---------------------+
| n8n orchestration | -> | Python contract core | -> | Provider adapters   |
| triggers / state  |    | validate / plan     |    | voice / image/video |
+--------+-----------+    +---------+----------+      +----------+----------+
         |                          |                            |
         |                          v                            |
         |               +----------+-----------+                |
         +-------------> | Asset resolver       | <--------------+
                         | archive-first policy |
                         +----------+-----------+
                                    |
                                    v
                         +----------+-----------+
                         | Render manifest      |
                         +----------+-----------+
                                    |
                                    v
                         +----------+-----------+
                         | FFmpeg render / QC   |
                         +----------+-----------+
                                    |
                                    v
                         +----------+-----------+
                         | Approval package     |
                         +-----+-----------+----+
                               |           |
                               v           v
                         publish adapter   archive
```

## Core rules

1. **Schema first.** Invalid content packages fail before any paid provider call.
2. **Archive first.** Existing creator-owned assets are preferred before stock or generation.
3. **Adaptive composition.** No universal avatar/B-roll ratio exists. Scene strategy depends on content type.
4. **Approval first.** The default publish mode is `approval`.
5. **Provider isolation.** Provider-specific request and response shapes do not leak into the content contract.
6. **Deterministic manifests.** A render run should be explainable from its content package, plan, asset bindings, and render manifest.
7. **No secrets in Git.** Credentials remain in n8n credential stores, environment configuration, or a secret manager.

## Layers

### 1. Content contract

`schemas/content.schema.json` defines the creator-facing request. It describes intent, not vendor APIs.

### 2. Planning core

`src/icho_reel_eng/core.py` validates content, flattens scripts into narrative units, allocates duration, assigns visual strategies, and produces a scene plan.

The first planner intentionally uses simple deterministic heuristics. Later planners can add model-assisted shot planning while preserving the same output contract.

### 3. Asset resolver

The resolver will bind scene `asset_query` values to actual media. Source precedence should remain:

1. local archive
2. existing gameplay / project assets
3. uploaded content
4. generated personal media
5. licensed stock
6. new paid generation

The resolver should eventually use asset metadata rather than filenames alone.

### 4. Provider adapters

Adapters should implement narrow capabilities such as:

- narration synthesis
- talking avatar generation
- image generation
- video generation
- transcription
- hosted rendering

A provider is a replaceable implementation, not a workflow architecture.

### 5. Render manifest

The plan is transformed into an explicit timeline. The manifest eventually carries:

- scene timing
- bound asset paths
- crop / scale policy
- captions
- motion transforms
- overlays
- audio tracks
- ducking
- transitions
- brand template IDs

### 6. Render engine

FFmpeg is the default local renderer. A hosted renderer may be added through the same render-manifest boundary for workloads where template APIs are more convenient.

### 7. QC

QC should fail closed before publishing. Planned checks include:

- 1080x1920 output
- expected duration tolerance
- H.264/AAC compatibility
- non-silent narration where expected
- caption presence and safe-zone checks
- no missing scene media
- no zero-byte or corrupt outputs

### 8. Approval and publishing

Publishing is downstream of rendering and QC. A future publish adapter can target Meta, YouTube, TikTok, or archival-only destinations. The render engine does not need platform credentials.

## Run state

Every execution should eventually write a run record containing:

```json
{
  "run_id": "uuid",
  "content_id": "icho-builder-0001",
  "workflow_version": "1",
  "status": "ready_for_review",
  "provider_usage": [],
  "assets": [],
  "cost": {"currency": "USD", "estimated": 0.0},
  "outputs": [],
  "errors": [],
  "timestamps": {}
}
```

Run state makes retries, auditability, analytics, and cost tracking possible without hiding logic inside n8n execution history.

## Suggested future packages

```text
src/icho_reel_eng/
  adapters/
    voice/
    image/
    video/
    publish/
  assets/
  captions/
  planner/
  render/
  qc/
  storage/
```

The repository starts smaller on purpose. Split packages when actual implementation pressure justifies them.
