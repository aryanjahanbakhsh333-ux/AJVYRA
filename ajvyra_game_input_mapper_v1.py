"""
AJVYRA Input Mapper v1

One action system for keyboard, mouse, touch and controller-like
inputs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class InputAction:
    action: str
    value: float = 1.0


class GameInputMapper:
    DEFAULTS = {
        "up": ["ArrowUp", "w", "W"],
        "down": ["ArrowDown", "s", "S"],
        "left": ["ArrowLeft", "a", "A"],
        "right": ["ArrowRight", "d", "D"],
        "primary": ["Space", "Enter"],
        "secondary": ["Shift"],
        "pause": ["Escape", "p", "P"],
    }

    def __init__(
        self,
        bindings: Optional[Dict[str, list[str]]] = None,
    ) -> None:
        self.bindings = dict(bindings or self.DEFAULTS)

    def keyboard(self, key: str) -> Optional[InputAction]:
        for action, keys in self.bindings.items():
            if key in keys:
                return InputAction(action=action)

        return None

    def touch(
        self,
        control: str,
        value: float = 1.0,
    ) -> Optional[InputAction]:
        control = control.lower().strip()

        if control in self.bindings:
            return InputAction(
                action=control,
                value=float(value),
            )

        aliases = {
            "up_button": "up",
            "down_button": "down",
            "left_button": "left",
            "right_button": "right",
            "a": "primary",
            "b": "secondary",
        }

        action = aliases.get(control)

        if action:
            return InputAction(
                action=action,
                value=float(value),
            )

        return None

    def bind(
        self,
        action: str,
        keys: list[str],
    ) -> None:
        self.bindings[action] = list(keys)

    def export(self) -> Dict[str, list[str]]:
        return {
            key: list(value)
            for key, value in self.bindings.items()
        }
