from __future__ import annotations

from typing import Any

from .core import Plan, Scene


def build_storyboard_shot_manifest(
    plan: Plan,
    scene: Scene,
    *,
    backend: str = "comfyui",
    style_profile: str | None = None,
    references: list[str] | None = None,
    seed: int | str = "derived",
) -> dict[str, Any]:
    """Compile a reel scene into the my-creators shot-manifest boundary."""
    index = f"{scene.index:03d}"
    return {
        "project_id": plan.content_id,
        "scene_id": f"{plan.content_id}:scene:{index}",
        "shot_id": f"{plan.content_id}:shot:{index}",
        "duration_seconds": scene.duration_sec,
        "framing": "vertical-short",
        "camera": "derived-from-scene-plan",
        "action": scene.visual_strategy,
        "emotion": "inherit-from-content",
        "characters": [],
        "style": {
            "profile": style_profile or plan.brand_profile,
            "palette": [],
        },
        "references": references or [],
        "prompt": scene.text,
        "negative_prompt": "",
        "backend": backend,
        "workflow": scene.visual_strategy,
        "seed": seed,
        "aspect_ratio": "9:16",
        "output_directory": f"runs/{plan.content_id}/visuals",
        "status": "planned",
        "metadata": {
            "source_engine": "icho-reel-eng",
            "content_type": plan.content_type,
            "scene_role": scene.role,
            "asset_query": scene.asset_query,
        },
    }


def build_content_universe_artifact(
    plan: Plan,
    *,
    asset_id: str,
    path: str,
    sha256: str,
    parents: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an interchange record for registration in Content Universe.

    This intentionally emits a narrow handoff envelope rather than copying the
    Content Universe internal persistence model.
    """
    relationships = [
        {"kind": "derived_from", "target": parent}
        for parent in (parents or [])
    ]
    return {
        "entity_key": f"asset:{asset_id}",
        "asset_id": asset_id,
        "kind": "video",
        "content_id": plan.content_id,
        "title": plan.title,
        "path": path,
        "relationships": relationships,
        "provenance": {
            "source": "icho-reel-eng",
            "sha256": sha256,
            "brand_profile": plan.brand_profile,
            "structure_mode": plan.structure_mode,
            "target_duration_sec": plan.target_duration_sec,
        },
        "metadata": metadata or {},
    }
