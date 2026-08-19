# AvaTar-ArTs Ecosystem Audit for icho-reel-eng

Date: 2026-08-19

## Purpose

This audit compares `icho-reel-eng` with the surrounding AvaTar-ArTs repositories and turns the strongest existing capabilities into explicit integration boundaries instead of duplicating them.

Audited repositories:

- `AvaTar-ArTs/content-universe`
- `AvaTar-ArTs/agent-skills`
- `AvaTar-ArTs/superAgents`
- `AvaTar-ArTs/superSkills`
- `AvaTar-ArTs/creator-camp`
- `AvaTar-ArTs/my-creators`

`content-universe` appeared twice in the request and is treated once as a single authoritative source.

## Executive conclusion

The original `icho-reel-eng` foundation was directionally correct but too self-contained. The larger ecosystem already contains richer ownership boundaries for provenance, agent routing, skill curation, story/canon workflow, and local visual generation.

The evolved architecture therefore changes from:

```text
icho-reel-eng = planner + asset resolver + generation + render + archive + publishing
```

to:

```text
icho-reel-eng = short-form production compiler and orchestration domain

content-universe = durable asset identity + provenance + lineage + creative graph
my-creators     = local storyboard/image generation + adapter training
superAgents     = agent routing + approval + execution envelope
superSkills     = curated capability catalog
agent-skills    = broad authored source ecosystem
creator-camp    = canon-to-release workflow for story/IP content
n8n             = external orchestration and event transport
FFmpeg          = deterministic local audiovisual compositor
```

This avoids a new monolith and lets the reel engine become the short-form projection layer of the broader creator ecosystem.

## Repository audit

### content-universe

Role: durable creative graph, recovery/catalog substrate, provenance and lineage authority.

Strongest reusable ideas:

- generation, response, asset, collection, and profile identities remain distinct
- typed entity keys prevent cross-namespace collisions
- provenance survives enrichment and replacement
- lineage relationships are conservative and evidence-backed
- JSON/JSONL/SQLite/graph outputs support both local operation and later automation
- CreativeOS direction already separates provider operations from recovery adapters
- recent work includes workflow provenance and audiovisual shot-manifest interchange

Integration decision:

- `icho-reel-eng` must not invent a competing long-term asset database
- rendered Reels, generated scenes, source clips, captions, audio, prompts, and publish outputs should eventually register back into Content Universe
- use narrow interchange records and adapters, not internal database coupling

### agent-skills

Role: broad authored ecosystem of agents, specialist skills, references, reports, and experimental material.

Verified audit strengths include structured asset production, workspace ecosystem auditing, verification-before-completion, engineering/studio agents, research, and skill authoring.

Important boundary:

- this is not a clean unrestricted runtime package
- large authored and vendored surfaces should not be recursively imported into a production reel workflow
- use curated projections where possible

Integration decision:

- reference specialist workflows and IDs
- do not copy the 1,000+ file ecosystem into `icho-reel-eng`
- promotion into production should flow through SuperSkills/SuperAgents

### superSkills

Role: authoritative curated skill layer.

Current curated primitives map well to the reel engine:

- brainstorming
- test-driven development
- verification before completion
- structured asset pipeline
- source-backed research
- MCP development
- catalog synchronization
- changelog discipline

Integration decision:

- reel stages should declare required capabilities using stable IDs rather than embedding copied skill bodies
- future reel-specific skills should be proposed upstream to SuperSkills instead of becoming private one-off conventions

Recommended future curated skills:

- `creative.short-form-scene-planning`
- `creative.caption-timing`
- `creative.reel-quality-control`
- `creative.asset-reuse-ranking`
- `distribution.social-publish-approval`
- `creative.vertical-video-composition`

### superAgents

Role: deterministic routing, agent selection, approval policy, execution envelope, and verification.

Its current router already separates selection from execution and weights capability matches more strongly than loose tag matches.

Integration decision:

- use SuperAgents as the future control-plane contract when `icho-reel-eng` needs specialized planners, asset curators, visual directors, QC reviewers, or publishers
- publishing and costly provider calls remain approval-sensitive operations
- agent selection must never automatically imply authorization to mutate external systems

Recommended reel agent roles:

- Reel Director
- Archive Curator
- Visual Continuity Director
- Gameplay Clip Analyst
- Caption Editor
- Render QC Reviewer
- Distribution Publisher
- Cost Governor

### creator-camp

Role: original-IP workflow, canon, publishing, release evidence, rights-aware packaging, and adaptation planning.

Its key architectural strength is repository boundary discipline: specialized repositories own implementation while Creator Camp coordinates the creator workflow.

Integration decision:

- `anthology_lore` and future narrative Reel modes should accept canon references and scene contracts from Creator Camp/choTaku rather than treating generated narration as isolated social copy
- story-derived Reels should carry IP ID, canon version, source scene, release status, and rights status
- short-form video becomes another artifact/output surface in the broader IP pipeline

### my-creators

Role: local open-source visual AI lab centered on ComfyUI-compatible storyboarding, separate style/character adapters, reproducible shot manifests, and training metadata.

Strong reusable ideas:

- explicit shot manifests
- separate style, character, environment, and motion adapters
- reference-driven consistency controls
- fixed/derived seed policies
- human review before final boards
- Python owns planning and metadata while ComfyUI owns model execution

Integration decision:

- `icho-reel-eng` scene plans compile into `my-creators` shot-manifest shaped records for generated visual scenes
- the reel engine should not learn ComfyUI node graphs directly
- visual generation remains replaceable and can fall back to archive imagery or motion-treated stills

## Gap analysis against the original icho-reel-eng foundation

### 1. Asset management was underspecified

Original state:

- asset queries existed only as scene tags
- no durable external identity/provenance contract

Evolution:

- Content Universe becomes the asset system of record
- new bridge records preserve typed asset identity, hash, parent lineage, brand profile, and structure mode

### 2. Visual generation boundary was too generic

Original state:

- `ImageProvider` and `VideoProvider` protocols existed, but no storyboard-level interchange contract

Evolution:

- scenes can compile into `my-creators` shot manifests
- style/reference/seed/backend metadata can travel through a stable contract

### 3. Agentic execution was implicit

Original state:

- n8n + Python were the only explicit control layers

Evolution:

- SuperAgents becomes the future route/approval/verification control plane
- n8n remains the event/workflow conductor, not the semantic agent registry

### 4. Skills were embedded as architecture assumptions

Original state:

- no explicit skill catalog relationship

Evolution:

- SuperSkills provides curated reusable capability IDs
- agent-skills stays upstream and broad

### 5. Narrative/lore content lacked canon lineage

Original state:

- `anthology_lore` was a stylistic mode only

Evolution:

- Creator Camp can supply canon, scene, rights, and release context
- story Reels become traceable artifacts in an IP lifecycle

### 6. Source repositories were floating dependencies

Original state:

- no cross-repository source manifest

Evolution:

- `config/ecosystem/sources.json` pins audited source commits and declares authority/capability boundaries

## New architectural rules

1. Do not duplicate another repository's authoritative domain model.
2. Integrate through small versioned interchange contracts.
3. Pin source commits for reproducible audits and adapter development.
4. Keep content planning deterministic before invoking paid or stochastic providers.
5. Register produced assets and lineage back into Content Universe.
6. Compile local generated visuals through `my-creators` shot boundaries.
7. Route agents and approval policies through SuperAgents when agentic execution is introduced.
8. Reference curated SuperSkills IDs instead of importing arbitrary skill text.
9. Treat `agent-skills` as authored source material, not trusted production code by default.
10. Carry canon and rights context for story-derived content.
11. Keep publishing approval-first until platform-specific safety and idempotency checks are proven.
12. Preserve prompts, seeds, references, provider versions, costs, hashes, and parent assets for every generated output.

## Target evolved pipeline

```text
Creator idea / archive item / gameplay / canon scene
              |
              v
      icho-reel content contract
              |
              +--> SuperAgents capability route (optional)
              +--> SuperSkills capability IDs
              |
              v
      deterministic scene compiler
              |
       +------+-------------------+
       |                          |
       v                          v
Content Universe             my-creators
asset/provenance query       shot manifests
       |                          |
       +------------+-------------+
                    v
            resolved scene pack
                    |
                    v
        narration + captions + audio
                    |
                    v
              FFmpeg render
                    |
                    v
              ffprobe / QC
                    |
                    v
             approval package
                    |
                    v
         platform publish adapters
                    |
                    v
          Content Universe register
                    |
                    v
       Creator Camp release evidence
       when content belongs to an IP
```

## Implementation added by this audit

- pinned cross-repository source catalog
- deterministic ecosystem capability selector
- authority-aware integration-plan builder
- `my-creators` storyboard shot-manifest bridge
- Content Universe artifact/provenance handoff envelope
- regression tests that enforce repository ownership boundaries

## Next implementation tranche

Priority order:

1. Add an `AssetResolver` interface with a Content Universe adapter and filesystem fallback.
2. Validate emitted storyboard records against a vendored/pinned interchange schema snapshot or fetched package dependency.
3. Add subtitle/cue contracts to mirror Content Universe audiovisual lineage.
4. Add ffprobe QC and deterministic render execution.
5. Add approval-package schema with preview, costs, sources, and change requests.
6. Add n8n workflows for asset resolution, render callback, QC, and approval.
7. Add a SuperAgents-compatible reel request envelope.
8. Add SuperSkills proposals for reel-specific production capabilities.
9. Add Creator Camp linkage fields for narrative/IP content.
10. Register final Reel and derivative assets into Content Universe.

## Non-goal

The goal is not to merge six mature repositories into one directory. The goal is to make `icho-reel-eng` a highly interoperable short-form production engine that can compose the best parts of the ecosystem while keeping each repository's authority clear.
