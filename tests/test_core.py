from pathlib import Path

from icho_reel_eng.core import (
    build_render_manifest,
    load_json,
    plan_content,
    validate_content,
)

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "content" / "examples"


def test_examples_validate():
    for path in sorted(EXAMPLES.glob("*.json")):
        assert validate_content(load_json(path)) == [], path.name


def test_planner_targets_requested_duration():
    data = load_json(EXAMPLES / "builder-commentary.json")
    plan = plan_content(data)
    assert plan.estimated_total_sec == data["format"]["target_duration_sec"]
    assert plan.scenes[0].role == "hook"
    assert plan.scenes[-1].role == "cta"


def test_gameplay_uses_gameplay_visual_strategy():
    data = load_json(EXAMPLES / "gameplay-insight.json")
    plan = plan_content(data)
    assert all(scene.visual_strategy == "gameplay_primary" for scene in plan.scenes)


def test_render_manifest_is_vertical():
    data = load_json(EXAMPLES / "anthology-lore.json")
    manifest = build_render_manifest(plan_content(data))
    assert manifest["canvas"] == {"width": 1080, "height": 1920, "fps": 30}
    assert manifest["brand_profile"] == "heartbreak_alley"
