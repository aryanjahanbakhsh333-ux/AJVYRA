from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class InputState:
    keys_down: Set[str] = field(default_factory=set)
    keys_pressed: Set[str] = field(default_factory=set)
    pointer_down: bool = False
    pointer_x: float = 0.0
    pointer_y: float = 0.0
    action_pressed: bool = False

    def clear_frame(self):
        self.keys_pressed.clear()
        self.action_pressed = False


class AJVYRAInputSystem:
    """
    Platform-independent input state.

    The browser runtime maps keyboard, touch and gamepad
    events into this structure.
    """

    MOVEMENT_KEYS = {
        "up": {"ArrowUp", "w", "W"},
        "down": {"ArrowDown", "s", "S"},
        "left": {"ArrowLeft", "a", "A"},
        "right": {"ArrowRight", "d", "D"},
    }

    def __init__(self):
        self.state = InputState()

    def key_down(self, key: str):
        if key not in self.state.keys_down:
            self.state.keys_pressed.add(key)

        self.state.keys_down.add(key)

    def key_up(self, key: str):
        self.state.keys_down.discard(key)

    def action(self):
        self.state.action_pressed = True

    def set_pointer(
        self,
        x: float,
        y: float,
        pressed: bool,
    ):
        self.state.pointer_x = x
        self.state.pointer_y = y
        self.state.pointer_down = pressed

    def is_down(self, key: str) -> bool:
        return key in self.state.keys_down

    def movement(self) -> Dict[str, bool]:
        result = {}

        for direction, keys in self.MOVEMENT_KEYS.items():
            result[direction] = any(
                key in self.state.keys_down
                for key in keys
            )

        return result

    def consume_frame(self):
        self.state.clear_frame()
