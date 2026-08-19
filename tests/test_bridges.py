from pathlib import Path

from icho_reel_eng.bridges import (
    build_content_universe_artifact,
    build_storyboard_shot_manifest,
)
from icho_reel_eng.core import load_json, plan_content


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "content" / "examples"


def test_storyboard_bridge_emits_my_creators_shape():
    plan = plan_content(load_json(EXAMPLES / "anthology-lore.json"))
    shot = build_storyboard_shot_manifest(
        plan,
        plan.scenes[0],
        backend="comfyui",
        style_profile="heartbreak_alley",
    )
    assert shot["project_id"] == plan.content_id
    assert shot["scene_id"] == f"{plan.content_id}:scene:001"
    assert shot["shot_id"] == f"{plan.content_id}:shot:001"
    assert shot["backend"] == "comfyui"
    assert shot["style"]["profile"] == "heartbreak_alley"
    assert shot["status"] == "planned"


def test_content_universe_bridge_preserves_typed_identity_and_lineage():
    plan = plan_content(load_json(EXAMPLES / "builder-commentary.json"))
    record = build_content_universe_artifact(
        plan,
        asset_id="local:render:001",
        path="exports/final.mp4",
        sha256="a" * 64,
        parents=["generation:source-001"],
    )
    assert record["entity_key"] == "asset:local:render:001"
    assert record["kind"] == "video"
    assert record["content_id"] == plan.content_id
    assert record["relationships"] == [
        {"kind": "derived_from", "target": "generation:source-001"}
    ]
    assert record["provenance"]["sha256"] == "a" * 64
