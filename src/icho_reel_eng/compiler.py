from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .asset_resolver import AssetResolver
from .bridges import build_storyboard_shot_manifest
from .contracts import SubtitleCue, build_superagents_request
from .core import Plan, Scene, build_render_manifest


@dataclass(slots=True)
class ResolvedScene:
    scene: Scene
    assets: list[dict[str, Any]]
    generation_request: dict[str, Any] | None
    cues: list[SubtitleCue]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scene": asdict(self.scene),
            "assets": self.assets,
            "generation_request": self.generation_request,
            "cues": [cue.to_dict() for cue in self.cues],
        }


def build_subtitle_cues(plan: Plan) -> list[SubtitleCue]:
    cursor = 0.0
    cues: list[SubtitleCue] = []
    for scene in plan.scenes:
        cue = SubtitleCue(
            start_sec=round(cursor, 2),
            end_sec=round(cursor + scene.duration_sec, 2),
            text=scene.text,
            provenance=[f"content:{plan.content_id}", f"scene:{scene.index:03d}"],
        )
        cues.append(cue)
        cursor += scene.duration_sec
    return cues


def compile_scene(
    plan: Plan,
    scene: Scene,
    resolver: AssetResolver,
    *,
    minimum_asset_score: float = 0.25,
) -> ResolvedScene:
    candidates = resolver.resolve(scene)
    accepted = [item for item in candidates if item.score >= minimum_asset_score]
    generation_request: dict[str, Any] | None = None
    if not accepted:
        generation_request = build_storyboard_shot_manifest(plan, scene)

    cue = SubtitleCue(
        start_sec=0.0,
        end_sec=scene.duration_sec,
        text=scene.text,
        provenance=[f"content:{plan.content_id}", f"scene:{scene.index:03d}"],
    )
    return ResolvedScene(
        scene=scene,
        assets=[item.to_dict() for item in accepted],
        generation_request=generation_request,
        cues=[cue],
    )


def compile_media_package(plan: Plan, resolver: AssetResolver) -> dict[str, Any]:
    """Compile a plan into a production package without executing providers.

    The package is deterministic and can be handed to n8n, SuperAgents,
    my-creators, or a local runner. Missing assets become explicit generation
    requests instead of silent provider calls.
    """
    resolved = [compile_scene(plan, scene, resolver) for scene in plan.scenes]
    capabilities: set[str] = {"creative.vertical-video-composition"}
    if any(item.generation_request for item in resolved):
        capabilities.add("storyboard-generation")
    if any(item.assets for item in resolved):
        capabilities.add("asset-provenance")

    render_manifest = build_render_manifest(plan)
    request = build_superagents_request(
        content_id=plan.content_id,
        stage="compile",
        capabilities=sorted(capabilities),
        payload={
            "content_id": plan.content_id,
            "brand_profile": plan.brand_profile,
            "resolved_scene_count": len(resolved),
        },
    )
    return {
        "version": 2,
        "content_id": plan.content_id,
        "plan": plan.to_dict(),
        "resolved_scenes": [item.to_dict() for item in resolved],
        "subtitles": [cue.to_dict() for cue in build_subtitle_cues(plan)],
        "render_manifest": render_manifest,
        "agent_request": request,
        "status": "compiled",
    }
