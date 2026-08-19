from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol


@dataclass(slots=True)
class PublishRequest:
    content_id: str
    platform: str
    video_path: str
    caption: str
    hashtags: list[str]
    scheduled_at: str | None = None
    approval_token: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PublishResult:
    platform: str
    status: str
    external_id: str | None = None
    external_url: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Publisher(Protocol):
    def publish(self, request: PublishRequest) -> PublishResult: ...


class DryRunPublisher:
    """Non-destructive publisher used by tests, previews, and approval flows."""

    def publish(self, request: PublishRequest) -> PublishResult:
        return PublishResult(
            platform=request.platform,
            status="dry_run",
            external_id=f"dry:{request.platform}:{request.content_id}",
        )


def build_platform_requests(
    *,
    content_id: str,
    video_path: str,
    caption: str,
    hashtags: list[str],
    platforms: list[str],
    scheduled_at: str | None = None,
) -> list[PublishRequest]:
    allowed = {"instagram", "youtube_shorts", "tiktok"}
    unknown = sorted(set(platforms) - allowed)
    if unknown:
        raise ValueError(f"Unsupported publish platforms: {', '.join(unknown)}")
    return [
        PublishRequest(
            content_id=content_id,
            platform=platform,
            video_path=video_path,
            caption=caption,
            hashtags=hashtags,
            scheduled_at=scheduled_at,
        )
        for platform in platforms
    ]
