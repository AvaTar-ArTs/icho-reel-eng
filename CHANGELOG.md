# Changelog

All notable changes to `icho-reel-eng` are recorded here.

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
