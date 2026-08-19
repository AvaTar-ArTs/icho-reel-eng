from pathlib import Path

import pytest

from icho_reel_eng.asset_resolver import (
    CompositeAssetResolver,
    ContentUniverseResolver,
    FilesystemAssetResolver,
)
from icho_reel_eng.compiler import build_subtitle_cues, compile_media_package
from icho_reel_eng.contracts import build_creator_camp_link, build_superagents_request
from icho_reel_eng.core import Plan, Scene
from icho_reel_eng.publishing import DryRunPublisher, build_platform_requests
from icho_reel_eng.qc import technical_qc


def make_plan() -> Plan:
    return Plan(
        content_id="icho-test-001",
        title="Archive first",
        content_type="anthology_lore",
        structure_mode="anthology_visual",
        target_duration_sec=10,
        brand_profile="heartbreak_alley",
        publishing_mode="approval",
        scenes=[
            Scene(
                index=1,
                role="hook",
                text="We keep the signal alive.",
                duration_sec=4.0,
                visual_strategy="panel_motion",
                asset_query=["hook", "anthology_lore", "trashcat"],
            ),
            Scene(
                index=2,
                role="body",
                text="Old work becomes new fuel.",
                duration_sec=6.0,
                visual_strategy="panel_motion",
                asset_query=["body", "anthology_lore", "archive"],
            ),
        ],
        estimated_total_sec=10.0,
    )


def test_content_universe_resolver_ranks_overlap():
    resolver = ContentUniverseResolver(
        [
            {
                "asset_id": "a1",
                "entity_key": "asset:a1",
                "path": "archive/a1.png",
                "tags": ["hook", "trashcat", "anthology_lore"],
            },
            {"asset_id": "a2", "path": "archive/a2.png", "tags": ["trashcat"]},
        ]
    )
    candidates = resolver.resolve(make_plan().scenes[0])
    assert [item.asset_id for item in candidates] == ["a1", "a2"]
    assert candidates[0].score > candidates[1].score


def test_composite_resolver_prefers_content_universe(tmp_path: Path):
    local = tmp_path / "trashcat-hook.png"
    local.write_bytes(b"fake")
    resolver = CompositeAssetResolver(
        [
            ContentUniverseResolver(
                [{"asset_id": "cu", "path": "cu.png", "tags": ["hook", "trashcat"]}]
            ),
            FilesystemAssetResolver([tmp_path]),
        ]
    )
    candidates = resolver.resolve(make_plan().scenes[0], limit=2)
    assert candidates[0].source == "content-universe"


def test_compile_package_generates_missing_visual_requests():
    plan = make_plan()
    package = compile_media_package(plan, ContentUniverseResolver([]))
    assert package["version"] == 2
    assert len(package["resolved_scenes"]) == 2
    assert all(item["generation_request"] for item in package["resolved_scenes"])
    assert "storyboard-generation" in package["agent_request"]["required_capabilities"]


def test_subtitle_cues_preserve_scene_timing():
    cues = build_subtitle_cues(make_plan())
    assert cues[0].start_sec == 0.0
    assert cues[0].end_sec == 4.0
    assert cues[1].start_sec == 4.0
    assert cues[1].end_sec == 10.0


def test_superagents_and_creator_camp_contracts():
    request = build_superagents_request(
        content_id="icho-test-001",
        stage="approve",
        capabilities=["verification", "verification"],
        payload={"ready": True},
        approval_required=True,
    )
    assert request["required_capabilities"] == ["verification"]
    assert request["approval_required"] is True

    link = build_creator_camp_link(
        content_id="icho-test-001",
        ip_id="love-is-rubbish",
        story_id="lir-001",
        scene_id="scene-01",
        canon_version="1.0.0",
    )
    assert link["adaptation_of"]["canon_version"] == "1.0.0"
    assert link["rights_state"] == "owned"


def test_publish_contract_is_approval_safe():
    requests = build_platform_requests(
        content_id="icho-test-001",
        video_path="exports/final.mp4",
        caption="Signal alive.",
        hashtags=["#ichoTaKu"],
        platforms=["instagram", "youtube_shorts"],
    )
    publisher = DryRunPublisher()
    assert [publisher.publish(item).status for item in requests] == ["dry_run", "dry_run"]

    with pytest.raises(ValueError):
        build_platform_requests(
            content_id="x",
            video_path="x.mp4",
            caption="x",
            hashtags=[],
            platforms=["unknown"],
        )


def test_qc_fails_closed_when_output_missing(tmp_path: Path):
    result = technical_qc(tmp_path / "missing.mp4", target_duration_sec=30)
    assert result.passed is False
    assert "output file is missing" in result.issues
