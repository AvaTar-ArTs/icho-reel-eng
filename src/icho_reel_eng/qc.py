from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TechnicalQCResult:
    passed: bool
    duration_sec: float | None
    width: int | None
    height: int | None
    has_audio: bool
    issues: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def probe_media(path: str | Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_streams",
        "-show_format",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def technical_qc(
    path: str | Path,
    *,
    target_duration_sec: float,
    duration_tolerance_sec: float = 1.5,
    expected_width: int = 1080,
    expected_height: int = 1920,
) -> TechnicalQCResult:
    media = Path(path)
    if not media.exists():
        return TechnicalQCResult(False, None, None, None, False, ["output file is missing"])

    try:
        probe = probe_media(media)
    except (FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return TechnicalQCResult(False, None, None, None, False, [f"ffprobe failed: {exc}"])

    streams = probe.get("streams", [])
    video = next((item for item in streams if item.get("codec_type") == "video"), None)
    has_audio = any(item.get("codec_type") == "audio" for item in streams)
    duration_raw = probe.get("format", {}).get("duration")
    duration = float(duration_raw) if duration_raw is not None else None
    width = int(video.get("width")) if video and video.get("width") else None
    height = int(video.get("height")) if video and video.get("height") else None

    issues: list[str] = []
    if video is None:
        issues.append("video stream missing")
    if width != expected_width or height != expected_height:
        issues.append(f"expected {expected_width}x{expected_height}, got {width}x{height}")
    if not has_audio:
        issues.append("audio stream missing")
    if duration is None:
        issues.append("duration unavailable")
    elif abs(duration - target_duration_sec) > duration_tolerance_sec:
        issues.append(
            f"duration {duration:.2f}s outside target {target_duration_sec:.2f}s ± "
            f"{duration_tolerance_sec:.2f}s"
        )

    return TechnicalQCResult(
        passed=not issues,
        duration_sec=duration,
        width=width,
        height=height,
        has_audio=has_audio,
        issues=issues,
    )
