from __future__ import annotations

from typing import Any, Dict

from ajvyra_game_action_router_v1 import (
    GameActionRouter,
)
from ajvyra_game_audio_system_v1 import (
    GameAudioSystem,
)
from ajvyra_game_progression_v1 import (
    GameProgression,
)
from ajvyra_game_quality_core_v1 import (
    GameQualityCore,
)
from ajvyra_game_save_system_v1 import (
    GameSaveSystem,
)
from ajvyra_game_visual_scene_v1 import (
    VisualScene,
)


class AJVYRAFinalGameRuntime:
    """
    Final shared runtime layer.

    Individual games remain responsible for their own
    mechanics, characters, story and rules.
    """

    VERSION = "1.0-final-runtime"

    def __init__(
        self,
        game_id: int,
        title: str,
    ):
        self.game_id = int(game_id)
        self.title = title

        self.quality = GameQualityCore(
            game_id,
            title,
        )

        self.progression = GameProgression()
        self.audio = GameAudioSystem()
        self.scene = VisualScene()
        self.input = GameActionRouter()
        self.save_system = GameSaveSystem()

    def start(self) -> Dict[str, Any]:
        self.quality.start()

        return self.snapshot()

    def action(
        self,
        name: str,
        **params: Any,
    ) -> Dict[str, Any]:
        self.quality.register_action(name)

        result = self.input.dispatch(
            name,
            **params,
        )

        self.save()

        return {
            "runtime": self.snapshot(),
            "action": result,
        }

    def reward(
        self,
        xp: int,
        score: int,
    ) -> Dict[str, Any]:
        self.progression.reward(
            xp=xp,
            score=score,
        )

        self.quality.add_score(score)

        self.save()

        return self.snapshot()

    def complete(self) -> Dict[str, Any]:
        self.progression.complete()
        self.quality.complete()

        self.save()

        return self.snapshot()

    def save(self) -> str:
        return self.save_system.save(
            self.game_id,
            self.snapshot(),
        )

    def snapshot(self) -> Dict[str, Any]:
        return {
            "runtime_version": self.VERSION,
            "game_id": self.game_id,
            "title": self.title,
            "quality": self.quality.snapshot(),
            "progression": self.progression.snapshot(),
            "audio": self.audio.export(),
            "scene": self.scene.export(),
            "input": self.input.export(),
        }
