# Changelog

All notable changes to `icho-reel-eng` are recorded here.

## [0.2.0] - 2026-08-19

### Added

- Cross-repository ecosystem audit covering Content Universe, agent-skills, SuperAgents, SuperSkills, Creator Camp, and my-creators.
- Pinned ecosystem source catalog with explicit authority, mode, and capability declarations.
- Reel-stage capability mapping for ingestion, planning, asset resolution, generation, rendering, approval, publishing, archiving, and story release.
- Deterministic ecosystem capability selector and integration-plan builder.
- my-creators storyboard bridge that compiles reel scenes into shot-manifest shaped records.
- Content Universe artifact bridge for typed asset identity, SHA-256 provenance, and parent lineage.
- Regression tests enforcing repository boundaries, source pinning, visual-generation routing, and provenance handoff behavior.

### Changed

- Reframed `icho-reel-eng` as the short-form production compiler within the wider AvaTar-ArTs creator ecosystem rather than a self-contained media monolith.
- Asset identity and long-term provenance are now delegated conceptually to Content Universe.
- Local generated-visual planning now targets the my-creators storyboard contract boundary.
- Agent routing and approval semantics are reserved for SuperAgents integration.
- Curated reusable capability IDs are sourced from SuperSkills while agent-skills remains the broader authored source ecosystem.
- Narrative and anthology content can evolve toward Creator Camp canon, rights, release, and adaptation lineage.

### Architecture decisions

- Specialized repositories retain implementation ownership.
- Cross-repository integration uses narrow interchange records instead of copied internal schemas.
- External source commits are pinned for reproducible audits and adapter work.
- Agent selection never implies authorization for external writes.
- Broad agent-skills content is not treated as an unrestricted runtime dependency.

## [0.1.0] - 2026-08-19

### Added

- Initial ichoTaKu-focused reel-engine repository foundation.
- Creator-facing content JSON Schema.
- Run-state JSON Schema.
- Deterministic content planner and render-manifest builder.
- CLI commands for validation, planning, and local runtime checks.
- Provider adapter protocols and registry.
- Brand profiles for ichoTaKu Default, DigitalDive, Heartbreak Alley, and ESO Gaming.
- Example builder-commentary, gameplay-insight, and anthology-lore packages.
- n8n intake workflow starter and orchestration contract documentation.
- Architecture, operations, roadmap, and brand execution documentation.
- Regression tests for schemas, scene planning, gameplay strategy, and vertical output.
- GitHub Actions CI with linting, tests, and example validation.

### Design decisions

- Approval-first publishing is the default.
- Existing creator assets are preferred before paid generation.
- The system uses adaptive composition instead of a hard-coded avatar/B-roll ratio.
- Provider-specific APIs remain behind capability boundaries.
- FFmpeg remains the preferred local render foundation.
