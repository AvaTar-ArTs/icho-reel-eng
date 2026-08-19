# n8n Workflows

n8n is the orchestration layer, not the media engine itself.

## Planned workflow set

```text
01_ingest_validate
02_content_plan
03_asset_resolve
04_audio_prepare
05_visual_prepare
06_render
07_qc
08_approval
09_publish
10_archive_notify
11_error_handler
```

The initial starter workflow in this folder implements the first contract boundary: webhook intake -> persisted JSON package -> Python validation/planning command -> response.

## Environment assumptions

The n8n worker that executes local commands must have:

- this repository mounted or cloned
- Python environment with `icho-reel-eng` installed
- a writable run directory

Do not put provider tokens or social credentials inside exported workflow JSON. Use n8n credentials or deployment secrets.

## Webhook contract

POST a content package matching `schemas/content.schema.json`.

Expected processing path:

```text
Webhook
  -> assign run ID
  -> write input JSON
  -> `icho-reel validate`
  -> `icho-reel plan`
  -> store plan path
  -> continue to future asset-resolution workflow
```

## Error workflow contract

Every production workflow should surface at minimum:

```json
{
  "run_id": "...",
  "content_id": "...",
  "stage": "planning",
  "retryable": false,
  "message": "...",
  "timestamp": "..."
}
```

Retryable stages should resume from durable prior outputs rather than restarting paid generation work.

## Approval-first rule

The publish workflow must check `publishing.mode` and should require an explicit approved run state unless the content profile has deliberately opted into automatic publishing.
