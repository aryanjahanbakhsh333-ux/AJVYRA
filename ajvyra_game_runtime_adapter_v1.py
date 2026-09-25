"""
AJVYRA Game Runtime Adapter v1

Normalizes the different Python game modules into one runtime API.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, Optional


class GameRuntimeAdapter:
    def __init__(self, discovered_game: Any) -> None:
        self.game = discovered_game
        self.module = discovered_game.module
        self.instance = self._create_instance()

    def _create_instance(self) -> Any:
        module = self.module

        factories = (
            "create_game",
            "build_game",
            "create",
        )

        for factory_name in factories:
            factory = getattr(module, factory_name, None)

            if callable(factory):
                try:
                    return factory()
                except TypeError:
                    continue

        classes = []

        for name, value in vars(module).items():
            if inspect.isclass(value):
                if value.__module__ == module.__name__:
                    classes.append(value)

        for cls in classes:
            try:
                return cls()
            except TypeError:
                continue

        return module

    def start(self) -> Dict[str, Any]:
        return self._call_optional(
            ("start_game", "start", "begin"),
            default=self.state(),
        )

    def action(
        self,
        action_name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        target = getattr(self.instance, action_name, None)

        if not callable(target):
            target = getattr(self.module, action_name, None)

        if not callable(target):
            return {
                "ok": False,
                "error": f"Action '{action_name}' is not available.",
                "state": self.state(),
            }

        try:
            result = target(**kwargs)
        except TypeError:
            result = target()

        return {
            "ok": True,
            "action": action_name,
            "result": self._serialize(result),
            "state": self.state(),
        }

    def state(self) -> Dict[str, Any]:
        target = getattr(self.instance, "status", None)

        if callable(target):
            try:
                result = target()
                return self._serialize(result)
            except Exception:
                pass

        return self._extract_public_state(self.instance)

    def _call_optional(
        self,
        names: tuple[str, ...],
        default: Dict[str, Any],
    ) -> Dict[str, Any]:
        for name in names:
            target = getattr(self.instance, name, None)

            if callable(target):
                try:
                    result = target()
                    return self._serialize(result)
                except TypeError:
                    continue

        return default

    @classmethod
    def _serialize(cls, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, dict):
            return {
                str(k): cls._serialize(v)
                for k, v in value.items()
            }

        if isinstance(value, (list, tuple, set)):
            return [cls._serialize(v) for v in value]

        if hasattr(value, "__dict__"):
            return {
                str(k): cls._serialize(v)
                for k, v in vars(value).items()
                if not str(k).startswith("_")
            }

        return str(value)

    @classmethod
    def _extract_public_state(cls, instance: Any) -> Dict[str, Any]:
        if not hasattr(instance, "__dict__"):
            return {}

        return {
            str(k): cls._serialize(v)
            for k, v in vars(instance).items()
            if not str(k).startswith("_")
        }
