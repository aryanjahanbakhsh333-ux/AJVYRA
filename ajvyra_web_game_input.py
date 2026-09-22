from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List
import json
from pathlib import Path


@dataclass
class InputAction:
    action_id: str
    keys: List[str] = field(default_factory=list)
    gamepad_buttons: List[int] = field(default_factory=list)
    touch_action: str = ""


@dataclass
class GameInputProfile:
    game_id: str
    actions: Dict[str, InputAction] = field(default_factory=dict)

    def add_action(
        self,
        action_id: str,
        keys: List[str] | None = None,
        gamepad_buttons: List[int] | None = None,
        touch_action: str = "",
    ) -> None:
        if not action_id.strip():
            raise ValueError("action_id cannot be empty")

        self.actions[action_id] = InputAction(
            action_id=action_id,
            keys=list(keys or []),
            gamepad_buttons=list(gamepad_buttons or []),
            touch_action=touch_action,
        )

    def validate(self) -> None:
        if not self.game_id.strip():
            raise ValueError("game_id cannot be empty")

        for action_id, action in self.actions.items():
            if action_id != action.action_id:
                raise ValueError(
                    f"Action key mismatch: {action_id}"
                )

            if not action.keys and not action.gamepad_buttons:
                if not action.touch_action:
                    raise ValueError(
                        f"Action '{action_id}' has no input mapping"
                    )

    def to_dict(self):
        self.validate()

        return {
            "game_id": self.game_id,
            "actions": {
                key: asdict(value)
                for key, value in self.actions.items()
            },
        }

    def save(self, path: str | Path) -> Path:
        self.validate()

        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            json.dumps(
                self.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


class AJVYRAInputProfileFactory:
    @staticmethod
    def standard_action_profile(game_id: str) -> GameInputProfile:
        profile = GameInputProfile(game_id=game_id)

        profile.add_action(
            "move_up",
            keys=["ArrowUp", "w", "W"],
            gamepad_buttons=[12],
            touch_action="up",
        )

        profile.add_action(
            "move_down",
            keys=["ArrowDown", "s", "S"],
            gamepad_buttons=[13],
            touch_action="down",
        )

        profile.add_action(
            "move_left",
            keys=["ArrowLeft", "a", "A"],
            gamepad_buttons=[14],
            touch_action="left",
        )

        profile.add_action(
            "move_right",
            keys=["ArrowRight", "d", "D"],
            gamepad_buttons=[15],
            touch_action="right",
        )

        profile.add_action(
            "primary",
            keys=[" ", "Enter"],
            gamepad_buttons=[0],
            touch_action="primary",
        )

        profile.add_action(
            "secondary",
            keys=["Shift"],
            gamepad_buttons=[1],
            touch_action="secondary",
        )

        profile.add_action(
            "pause",
            keys=["Escape", "p", "P"],
            gamepad_buttons=[9],
            touch_action="pause",
        )

        return profile


if __name__ == "__main__":
    profile = AJVYRAInputProfileFactory.standard_action_profile(
        "ajv_demo_001"
    )

    print(json.dumps(profile.to_dict(), indent=2))
