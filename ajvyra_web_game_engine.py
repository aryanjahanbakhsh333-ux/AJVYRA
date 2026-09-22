from __future__ import annotations

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import time


@dataclass
class GameDefinition:
    game_id: str
    title: str
    genre: str
    version: str = "1.0.0"
    entry_script: str = ""
    canvas_width: int = 1280
    canvas_height: int = 720
    mobile_supported: bool = True
    keyboard_supported: bool = True
    gamepad_supported: bool = True
    touch_supported: bool = True
    save_supported: bool = True
    assets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not self.game_id.strip():
            raise ValueError("game_id cannot be empty")

        if not self.title.strip():
            raise ValueError("title cannot be empty")

        if not self.genre.strip():
            raise ValueError("genre cannot be empty")

        if self.canvas_width < 320:
            raise ValueError("canvas_width is too small")

        if self.canvas_height < 240:
            raise ValueError("canvas_height is too small")

        if not self.entry_script.strip():
            raise ValueError(
                f"{self.game_id}: entry_script is required"
            )

    def to_dict(self) -> Dict[str, Any]:
        self.validate()
        return asdict(self)


@dataclass
class GameRuntimeState:
    status: str = "booting"
    elapsed_seconds: float = 0.0
    frame_count: int = 0
    score: int = 0
    level: int = 1
    paused: bool = False
    game_over: bool = False
    victory: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AJVYRAWebGameEngine:
    """
    Build/runtime contract for browser games.

    Python owns:
    - game definitions
    - validation
    - runtime state schema
    - browser runtime generation

    The actual gameplay loop runs in the generated JavaScript.
    """

    def __init__(
        self,
        definition: GameDefinition,
        output_root: str | Path = "public/games",
    ):
        definition.validate()

        self.definition = definition
        self.output_root = Path(output_root)
        self.state = GameRuntimeState()

        self.created_at = time.time()

    @property
    def game_root(self) -> Path:
        return self.output_root / self.definition.game_id

    def prepare_directory(self) -> Path:
        self.game_root.mkdir(parents=True, exist_ok=True)
        return self.game_root

    def build_manifest(self) -> Dict[str, Any]:
        return {
            "engine": "AJVYRA_WEB_GAME_ENGINE",
            "engine_version": "1.0.0",
            "game": self.definition.to_dict(),
            "runtime": self.state.to_dict(),
            "created_at": self.created_at,
        }

    def save_manifest(self) -> Path:
        root = self.prepare_directory()

        target = root / "game.manifest.json"

        target.write_text(
            json.dumps(
                self.build_manifest(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target

    def reset_runtime(self) -> None:
        self.state = GameRuntimeState()

    def mark_running(self) -> None:
        self.state.status = "running"
        self.state.paused = False

    def mark_paused(self) -> None:
        self.state.status = "paused"
        self.state.paused = True

    def mark_victory(self) -> None:
        self.state.status = "victory"
        self.state.victory = True
        self.state.game_over = False
        self.state.paused = False

    def mark_game_over(self) -> None:
        self.state.status = "game_over"
        self.state.game_over = True
        self.state.victory = False
        self.state.paused = False

    def increment_score(self, amount: int) -> None:
        self.state.score += int(amount)

    def set_level(self, level: int) -> None:
        self.state.level = max(1, int(level))

    def export_state(self) -> Dict[str, Any]:
        return self.state.to_dict()


if __name__ == "__main__":
    demo = GameDefinition(
        game_id="ajv_demo_001",
        title="AJVYRA Demo",
        genre="action",
        entry_script="game.js",
    )

    engine = AJVYRAWebGameEngine(demo)
    print(json.dumps(engine.build_manifest(), indent=2))
