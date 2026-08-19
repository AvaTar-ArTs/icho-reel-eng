from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "schemas" / "content.schema.json"


@dataclass(slots=True)
class Scene:
    index: int
    role: str
    text: str
    duration_sec: float
    visual_strategy: str
    asset_query: list[str]


@dataclass(slots=True)
class Plan:
    content_id: str
    title: str
    content_type: str
    structure_mode: str
    target_duration_sec: int
    brand_profile: str
    publishing_mode: str
    scenes: list[Scene]
    estimated_total_sec: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_content(data: dict[str, Any], schema_path: str | Path = DEFAULT_SCHEMA) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    return [f"{'/'.join(map(str, err.absolute_path)) or '<root>'}: {err.message}" for err in errors]


def assert_valid_content(data: dict[str, Any], schema_path: str | Path = DEFAULT_SCHEMA) -> None:
    errors = validate_content(data, schema_path)
    if errors:
        raise ValueError("Invalid content package:\n- " + "\n- ".join(errors))


def flatten_script(script: str | dict[str, Any]) -> list[tuple[str, str]]:
    if isinstance(script, str):
        return [("body", script.strip())]

    parts: list[tuple[str, str]] = []
    hook = str(script.get("hook", "")).strip()
    if hook:
        parts.append(("hook", hook))

    body = script.get("body", [])
    if isinstance(body, str):
        body = [body]
    for item in body:
        text = str(item).strip()
        if text:
            parts.append(("body", text))

    cta = str(script.get("cta", "")).strip()
    if cta:
        parts.append(("cta", cta))
    return parts


def _word_weight(text: str) -> int:
    return max(1, len(text.split()))


def _visual_strategy(content_type: str, role: str) -> str:
    if content_type == "gameplay_insight":
        return "gameplay_primary"
    if content_type == "anthology_lore":
        return "panel_motion"
    if content_type == "builder_commentary":
        return "screen_or_brand_broll" if role == "body" else "kinetic_type"
    if content_type == "music_visual":
        return "music_visualizer"
    return "archive_first_broll"


def plan_content(data: dict[str, Any]) -> Plan:
    assert_valid_content(data)
    parts = flatten_script(data["script"])
    target = int(data["format"]["target_duration_sec"])
    weights = [_word_weight(text) for _, text in parts]
    total_weight = sum(weights)

    scenes: list[Scene] = []
    tags = list(data.get("assets", {}).get("asset_tags", []))
    for index, ((role, text), weight) in enumerate(zip(parts, weights), start=1):
        raw_duration = target * (weight / total_weight)
        duration = round(max(1.5, raw_duration), 2)
        scenes.append(
            Scene(
                index=index,
                role=role,
                text=text,
                duration_sec=duration,
                visual_strategy=_visual_strategy(data["content_type"], role),
                asset_query=[role, data["content_type"], *tags],
            )
        )

    total = round(sum(scene.duration_sec for scene in scenes), 2)
    if scenes and not math.isclose(total, target, abs_tol=0.05):
        scenes[-1].duration_sec = round(max(1.5, scenes[-1].duration_sec + (target - total)), 2)
        total = round(sum(scene.duration_sec for scene in scenes), 2)

    return Plan(
        content_id=data["content_id"],
        title=data["title"],
        content_type=data["content_type"],
        structure_mode=data["format"]["structure_mode"],
        target_duration_sec=target,
        brand_profile=data["branding"]["brand_profile"],
        publishing_mode=data["publishing"]["mode"],
        scenes=scenes,
        estimated_total_sec=total,
    )


def build_render_manifest(plan: Plan, output_path: str = "exports/final.mp4") -> dict[str, Any]:
    cursor = 0.0
    timeline = []
    for scene in plan.scenes:
        timeline.append(
            {
                "scene": scene.index,
                "start_sec": round(cursor, 2),
                "duration_sec": scene.duration_sec,
                "role": scene.role,
                "text": scene.text,
                "visual_strategy": scene.visual_strategy,
                "asset_query": scene.asset_query,
            }
        )
        cursor += scene.duration_sec
    return {
        "version": 1,
        "content_id": plan.content_id,
        "canvas": {"width": 1080, "height": 1920, "fps": 30},
        "brand_profile": plan.brand_profile,
        "timeline": timeline,
        "output": {"path": output_path, "video_codec": "libx264", "audio_codec": "aac"},
    }


def ffmpeg_available() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True, text=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def write_json(data: Any, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return destination
