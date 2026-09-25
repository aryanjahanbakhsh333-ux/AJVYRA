"""
AJVYRA Render Bridge v1

Converts Python game state into renderer-neutral data.

The browser renderer can consume this contract later through
Canvas/WebGL/HTML5.
"""

from __future__ import annotations

from typing import Any, Dict


class GameRenderBridge:
    VERSION = "1.0"

    def frame(
        self,
        game_id: int,
        title: str,
        state: Dict[str, Any],
        device_config: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return {
            "engine": "AJVYRA",
            "engine_version": self.VERSION,
            "game": {
                "id": int(game_id),
                "title": title,
            },
            "viewport": self._viewport(
                device_config or {}
            ),
            "state": self._clean_state(state),
        }

    def _viewport(
        self,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        width = int(config.get("width", 1280))
        height = int(config.get("height", 720))

        return {
            "width": width,
            "height": height,
            "orientation": config.get(
                "orientation",
                "landscape",
            ),
            "touch": bool(
                config.get("touch_controls", False)
            ),
        }

    def _clean_state(
        self,
        state: Dict[str, Any],
    ) -> Dict[str, Any]:
        return self._serialize(state)

    def _serialize(self, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, dict):
            return {
                str(key): self._serialize(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple, set)):
            return [
                self._serialize(item)
                for item in value
            ]

        if hasattr(value, "__dict__"):
            return {
                str(key): self._serialize(item)
                for key, item in vars(value).items()
                if not str(key).startswith("_")
            }

        return str(value)
