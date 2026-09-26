from __future__ import annotations

from typing import Any, Callable, Dict


class GameActionRouter:
    """
    Converts browser input into game-specific actions.
    """

    def __init__(self):
        self.bindings: Dict[str, str] = {}
        self.handlers: Dict[str, Callable[..., Any]] = {}

    def bind(
        self,
        input_name: str,
        action_name: str,
    ) -> None:
        self.bindings[
            input_name.lower()
        ] = action_name

    def register(
        self,
        action_name: str,
        handler: Callable[..., Any],
    ) -> None:
        self.handlers[action_name] = handler

    def dispatch(
        self,
        input_name: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        key = input_name.lower()
        action = self.bindings.get(key)

        if action is None:
            return {
                "ok": False,
                "error": "unbound_input",
                "input": input_name,
            }

        handler = self.handlers.get(action)

        if handler is None:
            return {
                "ok": False,
                "error": "unregistered_action",
                "action": action,
            }

        try:
            result = handler(**kwargs)

            return {
                "ok": True,
                "action": action,
                "result": result,
            }

        except Exception as exc:
            return {
                "ok": False,
                "error": str(exc),
                "action": action,
            }

    def export(self) -> Dict[str, str]:
        return dict(self.bindings)
