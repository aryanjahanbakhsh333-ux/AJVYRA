import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from ajvyra_game_input_system import (
    AJVYRAInputSystem,
)

from ajvyra_game_collision_system import (
    AJVYRACollisionSystem,
)

from ajvyra_game_entity_system import (
    AJVYRAEntitySystem,
)

from ajvyra_game_genre_runtime import (
    AJVYRAGenreRuntime,
)


@dataclass
class RuntimeConfig:
    game_id: int
    title: str
    genre: str
    seed: int
    width: int = 1280
    height: int = 720
    target_fps: int = 60


class AJVYRAFinalGameRuntime:
    """
    Final shared runtime for AJVYRA playable games.

    This is the Python-side authoritative runtime model.
    Browser games use the same concepts when rendered in JS.
    """

    def __init__(
        self,
        config: RuntimeConfig,
        save_directory: str = "generated/game_saves",
    ):
        self.config = config

        self.input = AJVYRAInputSystem()
        self.collision = AJVYRACollisionSystem()
        self.entities = AJVYRAEntitySystem()

        self.genre = AJVYRAGenreRuntime(
            genre=config.genre,
            seed=config.seed,
        )

        self.save_directory = Path(
            save_directory
        )

        self.running = False
        self.last_time: Optional[float] = None

        self.player = self.entities.create_entity(
            x=config.width / 2,
            y=config.height / 2,
            width=32,
            height=32,
            health=100,
            max_health=100,
            tags=["player"],
        )

    def start(self):
        self.running = True
        self.last_time = time.perf_counter()

    def stop(self):
        self.running = False

    def pause(self):
        self.genre.pause()

    def resume(self):
        self.genre.resume()

    def update(self, dt: float):
        if not self.running:
            return

        if dt <= 0:
            return

        dt = min(dt, 0.05)

        movement = self.input.movement()

        speed = 220.0

        self.player.vx = 0.0
        self.player.vy = 0.0

        if movement["left"]:
            self.player.vx -= speed

        if movement["right"]:
            self.player.vx += speed

        if movement["up"]:
            self.player.vy -= speed

        if movement["down"]:
            self.player.vy += speed

        self.entities.update(dt)

        self.player.x = max(
            0,
            min(
                self.config.width -
                self.player.width,
                self.player.x,
            ),
        )

        self.player.y = max(
            0,
            min(
                self.config.height -
                self.player.height,
                self.player.y,
            ),
        )

        actions = {}

        if self.input.state.action_pressed:
            actions["action"] = True

        self.genre.update(
            dt,
            actions,
        )

        self.input.consume_frame()

    def tick(self):
        """
        Runs one time-based simulation step.

        A browser implementation should use
        requestAnimationFrame and pass its timestamp.
        """

        if not self.running:
            return

        now = time.perf_counter()

        if self.last_time is None:
            self.last_time = now

        dt = now - self.last_time
        self.last_time = now

        self.update(dt)

    def save(self):
        self.save_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        save_file = (
            self.save_directory /
            f"game_{self.config.game_id:02d}.json"
        )

        payload = {
            "game_id": self.config.game_id,
            "title": self.config.title,
            "genre": self.config.genre,
            "seed": self.config.seed,
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "health": self.player.health,
            },
            "genre_state": (
                self.genre.snapshot()
            ),
        }

        save_file.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return save_file

    def load(self) -> bool:
        save_file = (
            self.save_directory /
            f"game_{self.config.game_id:02d}.json"
        )

        if not save_file.exists():
            return False

        payload = json.loads(
            save_file.read_text(
                encoding="utf-8"
            )
        )

        player_data = payload.get(
            "player",
            {},
        )

        self.player.x = player_data.get(
            "x",
            self.player.x,
        )

        self.player.y = player_data.get(
            "y",
            self.player.y,
        )

        self.player.health = player_data.get(
            "health",
            self.player.health,
        )

        return True

    def reset(self):
        self.entities.clear()

        self.player = self.entities.create_entity(
            x=self.config.width / 2,
            y=self.config.height / 2,
            width=32,
            height=32,
            health=100,
            max_health=100,
            tags=["player"],
        )

        self.genre.reset()

    def status(self) -> Dict:
        return {
            "game_id": self.config.game_id,
            "title": self.config.title,
            "genre": self.config.genre,
            "running": self.running,
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "health": self.player.health,
            },
            "genre_runtime": (
                self.genre.snapshot()
            ),
            "entities": len(
                self.entities.entities
            ),
            "projectiles": len(
                self.entities.projectiles
            ),
        }


if __name__ == "__main__":
    config = RuntimeConfig(
        game_id=1,
        title="AJVYRA Prototype",
        genre="rpg",
        seed=10001,
    )

    runtime = AJVYRAFinalGameRuntime(
        config
    )

    runtime.start()

    for _ in range(5):
        runtime.tick()

    print(
        json.dumps(
            runtime.status(),
            ensure_ascii=False,
            indent=2,
        )
    )
