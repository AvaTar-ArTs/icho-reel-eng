from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True, frozen=True)
class EcosystemSource:
    repo: str
    commit: str
    mode: str
    authority: tuple[str, ...]
    capabilities: tuple[str, ...]
    notes: str = ""


@dataclass(slots=True, frozen=True)
class EcosystemCatalog:
    version: int
    generated_at: str
    sources: tuple[EcosystemSource, ...]


def load_ecosystem_catalog(path: str | Path) -> EcosystemCatalog:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    sources = tuple(
        EcosystemSource(
            repo=item["repo"],
            commit=item["commit"],
            mode=item["mode"],
            authority=tuple(item.get("authority", [])),
            capabilities=tuple(item.get("capabilities", [])),
            notes=item.get("notes", ""),
        )
        for item in payload["sources"]
    )
    return EcosystemCatalog(
        version=int(payload["version"]),
        generated_at=str(payload["generated_at"]),
        sources=sources,
    )


def select_sources(
    catalog: EcosystemCatalog,
    *,
    required_capabilities: set[str] | None = None,
) -> list[EcosystemSource]:
    required = required_capabilities or set()
    if not required:
        return list(catalog.sources)

    return [
        source
        for source in catalog.sources
        if required.intersection(source.capabilities)
    ]


def capability_coverage(catalog: EcosystemCatalog) -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = {}
    for source in catalog.sources:
        for capability in source.capabilities:
            coverage.setdefault(capability, []).append(source.repo)
    return {key: sorted(value) for key, value in sorted(coverage.items())}


def _source_for_authority(catalog: EcosystemCatalog, authority: str) -> str | None:
    for source in catalog.sources:
        if authority in source.authority:
            return source.repo
    return None


def build_integration_plan(
    catalog: EcosystemCatalog,
    *,
    content_type: str,
    requested_capabilities: set[str],
) -> dict[str, Any]:
    selected = select_sources(catalog, required_capabilities=requested_capabilities)
    available = set().union(*(set(source.capabilities) for source in selected)) if selected else set()
    missing = sorted(requested_capabilities - available)

    ownership = {
        "asset_system": _source_for_authority(catalog, "asset-system"),
        "visual_generation": _source_for_authority(catalog, "local-visual-generation"),
        "agent_routing": _source_for_authority(catalog, "agent-routing"),
        "skill_catalog": _source_for_authority(catalog, "curated-skill-catalog"),
        "creator_workflow": _source_for_authority(catalog, "creator-workflow"),
        "broad_skill_source": _source_for_authority(catalog, "broad-skill-source"),
    }

    return {
        "version": 1,
        "content_type": content_type,
        "requested_capabilities": sorted(requested_capabilities),
        "selected_sources": [
            {
                "repo": source.repo,
                "commit": source.commit,
                "mode": source.mode,
                "capabilities": sorted(
                    requested_capabilities.intersection(source.capabilities)
                ),
            }
            for source in selected
        ],
        "missing_capabilities": missing,
        "ownership": ownership,
        "invariants": [
            "icho-reel-eng orchestrates short-form production; it does not replace source repositories.",
            "Content Universe owns durable asset identity, provenance, and lineage.",
            "my-creators owns local storyboard and visual-generation contracts.",
            "SuperAgents owns agent routing and approval semantics.",
            "SuperSkills owns curated skill IDs and metadata.",
            "Creator Camp owns canon-to-release workflow for story/IP content.",
            "agent-skills remains a broad authored source, not an unrestricted runtime dependency.",
        ],
    }
