from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass
class TouchPoint:
    x: float
    y: float
    active: bool = True


class VirtualJoystick:
    def __init__(self, center_x, center_y, radius=75):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.active_pointer: Optional[int] = None
        self.x = 0.0
        self.y = 0.0

    def begin(self, pointer_id, x, y):
        distance = (
            (x - self.center_x) ** 2 +
            (y - self.center_y) ** 2
        ) ** 0.5

        if distance <= self.radius * 1.4:
            self.active_pointer = pointer_id
            self.update(x, y)
            return True

        return False

    def update(self, x, y):
        if self.active_pointer is None:
            return

        dx = x - self.center_x
        dy = y - self.center_y

        distance = max(
            1.0,
            (dx * dx + dy * dy) ** 0.5
        )

        if distance > self.radius:
            dx = dx / distance * self.radius
            dy = dy / distance * self.radius

        self.x = dx / self.radius
        self.y = dy / self.radius

    def end(self, pointer_id):
        if pointer_id == self.active_pointer:
            self.active_pointer = None
            self.x = 0.0
            self.y = 0.0


class TouchButton:
    def __init__(self, button_id, x, y, width, height):
        self.button_id = button_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressed = False

    def contains(self, x, y):
        return (
            self.x <= x <= self.x + self.width and
            self.y <= y <= self.y + self.height
        )


class TouchController:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        self.joystick = VirtualJoystick(
            110,
            screen_height - 110
        )

        self.buttons: Dict[str, TouchButton] = {
            "action": TouchButton(
                "action",
                screen_width - 180,
                screen_height - 150,
                90,
                90
            ),
            "action2": TouchButton(
                "action2",
                screen_width - 300,
                screen_height - 100,
                75,
                75
            ),
            "pause": TouchButton(
                "pause",
                screen_width - 80,
                20,
                55,
                55
            )
        }

    def touch_down(self, pointer_id, x, y):
        if self.joystick.begin(pointer_id, x, y):
            return "joystick"

        for button in self.buttons.values():
            if button.contains(x, y):
                button.pressed = True
                return button.button_id

        return None

    def touch_move(self, pointer_id, x, y):
        if pointer_id == self.joystick.active_pointer:
            self.joystick.update(x, y)

    def touch_up(self, pointer_id, x=None, y=None):
        self.joystick.end(pointer_id)

        for button in self.buttons.values():
            button.pressed = False

    def movement(self) -> Tuple[float, float]:
        return self.joystick.x, self.joystick.y

    def pressed(self, button_id):
        button = self.buttons.get(button_id)
        return bool(button and button.pressed)
