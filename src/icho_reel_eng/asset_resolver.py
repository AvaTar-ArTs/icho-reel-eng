from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol

from .core import Scene


@dataclass(slots=True)
class AssetCandidate:
    asset_id: str
    path: str
    source: str
    tags: list[str]
    score: float
    provenance_key: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AssetResolver(Protocol):
    def resolve(self, scene: Scene, *, limit: int = 5) -> list[AssetCandidate]: ...


def _score_tags(query: Iterable[str], tags: Iterable[str]) -> float:
    wanted = {str(item).casefold() for item in query}
    available = {str(item).casefold() for item in tags}
    if not wanted:
        return 0.0
    return round(len(wanted & available) / len(wanted), 4)


class ContentUniverseResolver:
    """Resolve scene assets from Content Universe export/search records.

    The resolver deliberately accepts normalized records instead of importing
    Content Universe internals. A future adapter can populate these records
    through CLI, HTTP, MCP, database, or export files without changing the
    compiler contract.
    """

    def __init__(self, records: Iterable[dict[str, Any]]) -> None:
        self.records = list(records)

    def resolve(self, scene: Scene, *, limit: int = 5) -> list[AssetCandidate]:
        ranked: list[AssetCandidate] = []
        for record in self.records:
            tags = list(record.get("tags", []))
            score = _score_tags(scene.asset_query, tags)
            if score <= 0:
                continue
            ranked.append(
                AssetCandidate(
                    asset_id=str(record.get("asset_id") or record.get("entity_key")),
                    path=str(record.get("path", "")),
                    source="content-universe",
                    tags=tags,
                    score=score,
                    provenance_key=record.get("entity_key"),
                    metadata=dict(record.get("metadata", {})),
                )
            )
        ranked.sort(key=lambda item: (-item.score, item.asset_id))
        return ranked[:limit]


class FilesystemAssetResolver:
    """Portable fallback resolver for local personal archives."""

    MEDIA_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".png", ".jpg", ".jpeg", ".webp"}

    def __init__(self, roots: Iterable[str | Path]) -> None:
        self.roots = [Path(root) for root in roots]

    def resolve(self, scene: Scene, *, limit: int = 5) -> list[AssetCandidate]:
        terms = [term.casefold().replace("_", "-") for term in scene.asset_query]
        ranked: list[AssetCandidate] = []
        for root in self.roots:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix.casefold() not in self.MEDIA_SUFFIXES:
                    continue
                haystack = path.stem.casefold().replace("_", "-")
                matched = [term for term in terms if term and term in haystack]
                if not matched:
                    continue
                ranked.append(
                    AssetCandidate(
                        asset_id=f"file:{path.name}",
                        path=str(path),
                        source="filesystem",
                        tags=matched,
                        score=round(len(matched) / max(1, len(terms)), 4),
                    )
                )
        ranked.sort(key=lambda item: (-item.score, item.path))
        return ranked[:limit]


class CompositeAssetResolver:
    """Archive-first resolver with deterministic fallback ordering."""

    def __init__(self, resolvers: Iterable[AssetResolver]) -> None:
        self.resolvers = list(resolvers)

    def resolve(self, scene: Scene, *, limit: int = 5) -> list[AssetCandidate]:
        output: list[AssetCandidate] = []
        seen: set[str] = set()
        for resolver in self.resolvers:
            for candidate in resolver.resolve(scene, limit=limit):
                key = candidate.provenance_key or candidate.path
                if key in seen:
                    continue
                seen.add(key)
                output.append(candidate)
                if len(output) >= limit:
                    return output
        return output
