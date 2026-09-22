from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ProviderRecord:
    name: str
    provider: Any
    media_type: str
    enabled: bool = True
    priority: int = 100


class AJVYRACinematicProviderRegistry:
    """
    Central registry for cinematic media providers.

    The cinematic engine does not need to know which company/model
    actually performs generation.
    """

    def __init__(self) -> None:
        self._providers: Dict[str, ProviderRecord] = {}

    def register(
        self,
        name: str,
        provider: Any,
        media_type: str,
        *,
        priority: int = 100,
        enabled: bool = True,
    ) -> ProviderRecord:
        if not name.strip():
            raise ValueError("Provider name cannot be empty.")

        if not media_type.strip():
            raise ValueError("Media type cannot be empty.")

        record = ProviderRecord(
            name=name,
            provider=provider,
            media_type=media_type,
            enabled=enabled,
            priority=priority,
        )

        self._providers[name] = record
        return record

    def unregister(self, name: str) -> bool:
        return self._providers.pop(name, None) is not None

    def enable(self, name: str) -> None:
        self._require(name).enabled = True

    def disable(self, name: str) -> None:
        self._require(name).enabled = False

    def get(self, name: str) -> Any:
        return self._require(name).provider

    def select(self, media_type: str) -> Optional[ProviderRecord]:
        candidates = [
            record
            for record in self._providers.values()
            if record.enabled and record.media_type == media_type
        ]

        if not candidates:
            return None

        candidates.sort(key=lambda item: item.priority)
        return candidates[0]

    def list(self, media_type: Optional[str] = None) -> list[ProviderRecord]:
        records = list(self._providers.values())

        if media_type is not None:
            records = [
                record
                for record in records
                if record.media_type == media_type
            ]

        return sorted(records, key=lambda item: item.priority)

    def snapshot(self) -> list[dict]:
        return [
            {
                "name": record.name,
                "media_type": record.media_type,
                "enabled": record.enabled,
                "priority": record.priority,
            }
            for record in self.list()
        ]

    def _require(self, name: str) -> ProviderRecord:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(
                f"Cinematic provider '{name}' is not registered."
            ) from exc
