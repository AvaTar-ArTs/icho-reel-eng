from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class SubtitleCue:
    start_sec: float
    end_sec: float
    text: str
    speaker: str = "ichoTaKu"
    source: str = "script"
    provenance: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ApprovalPackage:
    content_id: str
    preview_path: str
    final_path: str
    caption: str
    hashtags: list[str]
    title_variants: list[str]
    estimated_cost_usd: float
    asset_sources: list[str]
    technical_qc: dict[str, Any]
    provenance: dict[str, Any]
    status: str = "ready_for_review"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_superagents_request(
    *,
    content_id: str,
    stage: str,
    capabilities: list[str],
    payload: dict[str, Any],
    approval_required: bool = False,
) -> dict[str, Any]:
    """Create the narrow request envelope consumed by SuperAgents routing."""
    return {
        "request_id": f"reel:{content_id}:{stage}",
        "source": "icho-reel-eng",
        "stage": stage,
        "required_capabilities": sorted(set(capabilities)),
        "approval_required": approval_required,
        "payload": payload,
    }


def build_creator_camp_link(
    *,
    content_id: str,
    ip_id: str,
    story_id: str,
    scene_id: str,
    canon_version: str,
    rights_state: str = "owned",
) -> dict[str, Any]:
    """Link a Reel adaptation to Creator Camp canon/release lineage."""
    return {
        "artifact_id": f"reel:{content_id}",
        "artifact_type": "short-form-video",
        "adaptation_of": {
            "ip_id": ip_id,
            "story_id": story_id,
            "scene_id": scene_id,
            "canon_version": canon_version,
        },
        "rights_state": rights_state,
        "release_state": "planned",
        "source_engine": "icho-reel-eng",
    }
