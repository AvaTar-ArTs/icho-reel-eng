from pathlib import Path

from icho_reel_eng.ecosystem import (
    build_integration_plan,
    load_ecosystem_catalog,
    select_sources,
)


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "ecosystem" / "sources.json"


def test_catalog_has_expected_sources():
    catalog = load_ecosystem_catalog(CATALOG)
    names = {source.repo for source in catalog.sources}
    assert names == {
        "AvaTar-ArTs/content-universe",
        "AvaTar-ArTs/agent-skills",
        "AvaTar-ArTs/superAgents",
        "AvaTar-ArTs/superSkills",
        "AvaTar-ArTs/creator-camp",
        "AvaTar-ArTs/my-creators",
    }


def test_catalog_sources_are_pinned_and_bounded():
    catalog = load_ecosystem_catalog(CATALOG)
    for source in catalog.sources:
        assert len(source.commit) == 40
        assert source.mode in {"reference", "contract", "runtime-adapter"}
        assert source.capabilities


def test_visual_generation_selects_my_creators_and_content_universe():
    catalog = load_ecosystem_catalog(CATALOG)
    selected = select_sources(
        catalog,
        required_capabilities={"asset-provenance", "storyboard-generation"},
    )
    repos = {source.repo for source in selected}
    assert "AvaTar-ArTs/content-universe" in repos
    assert "AvaTar-ArTs/my-creators" in repos


def test_integration_plan_keeps_repo_boundaries():
    catalog = load_ecosystem_catalog(CATALOG)
    plan = build_integration_plan(
        catalog,
        content_type="anthology_lore",
        requested_capabilities={
            "asset-provenance",
            "storyboard-generation",
            "canon-workflow",
            "capability-routing",
        },
    )
    assert plan["content_type"] == "anthology_lore"
    assert plan["ownership"]["asset_system"] == "AvaTar-ArTs/content-universe"
    assert plan["ownership"]["visual_generation"] == "AvaTar-ArTs/my-creators"
    assert plan["ownership"]["agent_routing"] == "AvaTar-ArTs/superAgents"
    assert plan["ownership"]["creator_workflow"] == "AvaTar-ArTs/creator-camp"
