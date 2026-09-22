from dataclasses import dataclass, field
from typing import Dict, List
import random


@dataclass
class GenreRuntimeState:
    genre: str
    level: int = 1
    score: float = 0.0
    elapsed: float = 0.0
    objective_progress: float = 0.0
    objective_target: float = 100.0
    lives: int = 3
    completed: bool = False
    failed: bool = False
    paused: bool = False
    data: Dict[str, object] = field(
        default_factory=dict
    )


class AJVYRAGenreRuntime:
    """
    Defines genre-specific gameplay rules.

    Rendering is handled by the browser runtime.
    This layer decides what the game actually does.
    """

    SUPPORTED = {
        "rpg",
        "platformer",
        "horror",
        "racing",
        "puzzle",
        "survival",
        "adventure",
        "shooter",
        "stealth",
        "runner",
    }

    def __init__(
        self,
        genre: str,
        seed: int = 0,
    ):
        genre = genre.lower().strip()

        if genre not in self.SUPPORTED:
            raise ValueError(
                f"Unsupported genre: {genre}"
            )

        self.genre = genre
        self.random = random.Random(seed)

        self.state = GenreRuntimeState(
            genre=genre
        )

        self.config = self._build_config()

    def _build_config(self) -> Dict:
        configs = {
            "rpg": {
                "objective": "defeat_boss",
                "levels": 8,
                "enemy_scaling": 1.15,
                "xp": True,
                "inventory": True,
                "boss": True,
            },

            "platformer": {
                "objective": "reach_exit",
                "levels": 10,
                "gravity": 1500,
                "jump_power": 560,
                "platforms": True,
            },

            "horror": {
                "objective": "escape",
                "levels": 6,
                "darkness": True,
                "battery": 100,
                "fear": 0,
                "enemy_tracking": True,
            },

            "racing": {
                "objective": "finish_race",
                "levels": 7,
                "laps": 3,
                "boost": 100,
                "checkpoints": True,
            },

            "puzzle": {
                "objective": "solve_puzzle",
                "levels": 12,
                "grid_size": 6,
                "moves": 40,
                "combo": 0,
            },

            "survival": {
                "objective": "survive_time",
                "levels": 10,
                "wave": 1,
                "resources": 100,
                "enemy_scaling": 1.12,
            },

            "adventure": {
                "objective": "discover",
                "levels": 9,
                "secrets": 12,
                "locations": 15,
                "story_flags": [],
            },

            "shooter": {
                "objective": "defeat_enemies",
                "levels": 10,
                "ammo": 60,
                "enemy_waves": 8,
                "boss": True,
            },

            "stealth": {
                "objective": "avoid_detection",
                "levels": 8,
                "visibility": 0,
                "noise": 0,
                "guards": True,
            },

            "runner": {
                "objective": "beat_distance",
                "levels": 5,
                "distance": 0,
                "target_distance": 5000,
                "obstacle_rate": 1.0,
            },
        }

        return configs[self.genre].copy()

    def update(
        self,
        dt: float,
        actions: Dict[str, object] | None = None,
    ):

        if self.state.completed:
            return

        if self.state.failed:
            return

        if self.state.paused:
            return

        actions = actions or {}

        self.state.elapsed += dt

        handler = getattr(
            self,
            f"_update_{self.genre}",
            None,
        )

        if handler:
            handler(dt, actions)

        self._check_completion()

    def _update_rpg(self, dt, actions):
        if actions.get("enemy_defeated"):
            self.state.score += 100
            self.state.objective_progress += 10

        if actions.get("xp"):
            self.state.data["xp"] = (
                self.state.data.get("xp", 0)
                + actions["xp"]
            )

    def _update_platformer(self, dt, actions):
        if actions.get("checkpoint"):
            self.state.objective_progress += 10

        if actions.get("fall"):
            self.state.lives -= 1

            if self.state.lives <= 0:
                self.state.failed = True

    def _update_horror(self, dt, actions):
        self.config["battery"] = max(
            0,
            self.config["battery"] - dt * 1.5,
        )

        if actions.get("enemy_near"):
            self.config["fear"] = min(
                100,
                self.config["fear"] + dt * 12,
            )
        else:
            self.config["fear"] = max(
                0,
                self.config["fear"] - dt * 4,
            )

        if actions.get("key_found"):
            self.state.objective_progress += 25

    def _update_racing(self, dt, actions):
        if actions.get("checkpoint"):
            self.state.objective_progress += 10

        if actions.get("boost"):
            self.config["boost"] = max(
                0,
                self.config["boost"] - dt * 20,
            )

    def _update_puzzle(self, dt, actions):
        if actions.get("move"):
            self.config["moves"] -= 1

            if self.config["moves"] <= 0:
                self.state.failed = True

        if actions.get("combo"):
            self.config["combo"] += 1
            self.state.score += (
                25 * self.config["combo"]
            )

        if actions.get("solved"):
            self.state.objective_progress = 100

    def _update_survival(self, dt, actions):
        self.state.objective_progress += (
            dt * 2
        )

        if actions.get("resource"):
            self.config["resources"] = min(
                100,
                self.config["resources"] + 5,
            )

        if actions.get("wave_complete"):
            self.config["wave"] += 1
            self.state.score += 250

    def _update_adventure(self, dt, actions):
        if actions.get("secret_found"):
            self.config["secrets"] -= 1
            self.state.score += 200

        if actions.get("location_discovered"):
            self.state.objective_progress += 7

    def _update_shooter(self, dt, actions):
        if actions.get("enemy_defeated"):
            self.state.score += 50
            self.state.objective_progress += 5

        if actions.get("wave_complete"):
            self.config["enemy_waves"] -= 1

    def _update_stealth(self, dt, actions):
        if actions.get("noise"):
            self.config["noise"] += actions["noise"]

        self.config["noise"] = max(
            0,
            self.config["noise"] - dt * 5,
        )

        if actions.get("detected"):
            self.state.lives -= 1

            if self.state.lives <= 0:
                self.state.failed = True

        if actions.get("objective_complete"):
            self.state.objective_progress = 100

    def _update_runner(self, dt, actions):
        speed = actions.get(
            "speed",
            250,
        )

        self.config["distance"] += (
            speed * dt
        )

        self.state.objective_progress = (
            self.config["distance"] /
            self.config["target_distance"] *
            100
        )

        if actions.get("obstacle_hit"):
            self.state.lives -= 1

            if self.state.lives <= 0:
                self.state.failed = True

    def _check_completion(self):
        if (
            self.state.objective_progress >=
            self.state.objective_target
        ):
            self.state.completed = True

    def next_level(self):
        maximum = self.config.get(
            "levels",
            1,
        )

        if self.state.level >= maximum:
            self.state.completed = True
            return

        self.state.level += 1
        self.state.objective_progress = 0

    def pause(self):
        self.state.paused = True

    def resume(self):
        self.state.paused = False

    def reset(self):
        self.state = GenreRuntimeState(
            genre=self.genre
        )
        self.config = self._build_config()

    def snapshot(self) -> Dict:
        return {
            "genre": self.state.genre,
            "level": self.state.level,
            "score": self.state.score,
            "elapsed": self.state.elapsed,
            "objective_progress": (
                self.state.objective_progress
            ),
            "lives": self.state.lives,
            "completed": self.state.completed,
            "failed": self.state.failed,
            "paused": self.state.paused,
            "config": self.config.copy(),
        }
