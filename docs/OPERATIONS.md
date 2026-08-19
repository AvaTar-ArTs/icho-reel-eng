# Operations

## Daily creator loop

1. Create or copy a content package in `content/`.
2. Validate it before any generation work.
3. Generate a scene plan.
4. Resolve or attach source assets.
5. Generate narration or other missing media only where required.
6. Build the render manifest.
7. Render a preview.
8. Run QC.
9. Review the approval package.
10. Publish or schedule only after approval.
11. Archive the run record and final outputs.

## Local commands

```bash
icho-reel doctor
icho-reel validate content/examples/builder-commentary.json
icho-reel plan content/examples/builder-commentary.json --out runs/builder-plan.json
```

## Status model

Use these states consistently across Python, n8n, dashboards, and future databases:

```text
draft
validated
planning
asset_resolution
media_generation
rendering
qc
ready_for_review
revision_requested
approved
scheduled
published
failed
archived
```

## Approval package

A future production run should collect:

```text
runs/<run-id>/
  input.json
  plan.json
  asset-bindings.json
  render-manifest.json
  captions.srt
  preview.mp4
  metadata.json
  run.json
  logs/
```

The review surface should expose:

- preview video
- title and hook
- caption
- hashtags
- asset provenance
- estimated provider cost
- warnings
- approve / revise / archive actions

## Failure policy

### Retryable

- API timeouts
- temporary 429/5xx provider failures
- delayed render callbacks
- transient download failures

### Non-retryable until operator action

- schema validation errors
- missing required local asset
- invalid credentials
- unsupported media
- empty narration
- render manifest corruption

A retry should resume at the failed stage whenever the prior stage outputs remain valid.

## Cost policy

Before calling a paid generation provider, the workflow should ask:

1. Does a matching personal asset already exist?
2. Can gameplay or screen capture communicate the point better?
3. Can a still image plus motion replace generated video?
4. Is this scene important enough to justify paid generation?
5. Is a cheaper provider/profile sufficient for a draft?

Every paid call should eventually write estimated and actual cost to the run record.

## Asset provenance

Each selected asset should retain enough metadata to answer:

- Where did it come from?
- Is it creator-owned, generated, uploaded, gameplay, or licensed stock?
- Which content runs have used it?
- What prompt or source produced it?
- Is reuse permitted?

## Publishing policy

`approval` is the default. Automatic publishing should be enabled only per series or content class after the production path has proven reliable.

## Secret management

Do not commit tokens, API keys, OAuth refresh tokens, provider credentials, or social publishing secrets. Prefer:

- n8n credentials for n8n-owned calls
- environment variables for local adapters
- a proper secret store for deployed workers

## Backup policy

Keep code and contracts in Git. Keep large source media and rendered outputs in a separate versioned or backed-up media store. Do not use Git history as a video asset database.
