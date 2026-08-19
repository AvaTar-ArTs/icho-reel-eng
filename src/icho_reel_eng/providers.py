from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass(slots=True)
class ProviderResult:
    provider: str
    operation: str
    output_path: Path | None
    external_id: str | None
    estimated_cost_usd: float
    metadata: dict[str, Any]


class VoiceProvider(Protocol):
    name: str

    def synthesize(self, *, text: str, voice_id: str | None, output_path: Path) -> ProviderResult:
        """Create narration audio and return provider metadata."""
        ...


class ImageProvider(Protocol):
    name: str

    def generate(self, *, prompt: str, output_path: Path, options: dict[str, Any]) -> ProviderResult:
        """Generate a still image for a scene."""
        ...


class VideoProvider(Protocol):
    name: str

    def generate(self, *, prompt: str, output_path: Path, options: dict[str, Any]) -> ProviderResult:
        """Generate a motion clip for a scene."""
        ...


class PublishProvider(Protocol):
    name: str

    def publish(self, *, media_path: Path, metadata: dict[str, Any]) -> ProviderResult:
        """Publish an approved media artifact."""
        ...


class ProviderRegistry:
    """Small dependency-injection registry for replaceable capabilities."""

    def __init__(self) -> None:
        self._providers: dict[tuple[str, str], Any] = {}

    def register(self, capability: str, provider_name: str, provider: Any) -> None:
        self._providers[(capability, provider_name)] = provider

    def get(self, capability: str, provider_name: str) -> Any:
        key = (capability, provider_name)
        if key not in self._providers:
            raise KeyError(f"No provider registered for {capability}:{provider_name}")
        return self._providers[key]

    def available(self, capability: str) -> list[str]:
        return sorted(name for cap, name in self._providers if cap == capability)
