from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MechanicsProfile:
    genre: str
    mechanics: List[str]
    player_speed: float
    enemy_speed: float
    spawn_rate: float
    health: int
    score_multiplier: float
    special_rules: Dict[str, object] = field(default_factory=dict)


class AJVYGameMechanicsEngine:
    """
    Converts a genre into concrete gameplay parameters.
    """

    def __init__(self):
        self.profiles = {
            "rpg": {
                "player_speed": 3.2,
                "enemy_speed": 1.4,
                "spawn_rate": 1.8,
                "health": 100,
                "score_multiplier": 1.0,
                "special_rules": {
                    "experience": True,
                    "inventory": True,
                    "boss": True,
                },
            },

            "platformer": {
                "player_speed": 4.0,
                "enemy_speed": 2.0,
                "spawn_rate": 2.5,
                "health": 3,
                "score_multiplier": 1.2,
                "special_rules": {
                    "gravity": True,
                    "jump": True,
                    "platforms": True,
                },
            },

            "horror": {
                "player_speed": 2.4,
                "enemy_speed": 2.0,
                "spawn_rate": 3.0,
                "health": 60,
                "score_multiplier": 1.5,
                "special_rules": {
                    "darkness": True,
                    "battery": True,
                    "fear": True,
                },
            },

            "racing": {
                "player_speed": 5.5,
                "enemy_speed": 4.5,
                "spawn_rate": 1.2,
                "health": 1,
                "score_multiplier": 1.8,
                "special_rules": {
                    "boost": True,
                    "checkpoints": True,
                    "laps": True,
                },
            },

            "puzzle": {
                "player_speed": 0,
                "enemy_speed": 0,
                "spawn_rate": 0,
                "health": 1,
                "score_multiplier": 2.0,
                "special_rules": {
                    "grid": True,
                    "matching": True,
                    "timer": True,
                },
            },

            "survival": {
                "player_speed": 3.0,
                "enemy_speed": 1.8,
                "spawn_rate": 0.8,
                "health": 100,
                "score_multiplier": 1.4,
                "special_rules": {
                    "waves": True,
                    "resources": True,
                    "crafting": True,
                },
            },

            "adventure": {
                "player_speed": 2.8,
                "enemy_speed": 1.2,
                "spawn_rate": 4.0,
                "health": 100,
                "score_multiplier": 1.1,
                "special_rules": {
                    "exploration": True,
                    "secrets": True,
                    "story_events": True,
                },
            },

            "shooter": {
                "player_speed": 3.8,
                "enemy_speed": 1.8,
                "spawn_rate": 1.0,
                "health": 100,
                "score_multiplier": 1.7,
                "special_rules": {
                    "projectiles": True,
                    "waves": True,
                    "boss": True,
                },
            },

            "stealth": {
                "player_speed": 2.7,
                "enemy_speed": 2.2,
                "spawn_rate": 2.0,
                "health": 1,
                "score_multiplier": 2.2,
                "special_rules": {
                    "visibility": True,
                    "patrols": True,
                    "noise": True,
                },
            },

            "runner": {
                "player_speed": 5.0,
                "enemy_speed": 0,
                "spawn_rate": 0.7,
                "health": 3,
                "score_multiplier": 1.6,
                "special_rules": {
                    "automatic_running": True,
                    "obstacles": True,
                    "distance": True,
                },
            },
        }

    def build_profile(
        self,
        genre: str,
        mechanics: List[str] | None = None,
        difficulty_factor: float = 1.0,
    ) -> MechanicsProfile:

        genre = genre.lower().strip()

        if genre not in self.profiles:
            raise ValueError(f"Unsupported genre: {genre}")

        data = self.profiles[genre]

        factor = max(0.5, min(2.0, difficulty_factor))

        return MechanicsProfile(
            genre=genre,
            mechanics=list(mechanics or []),
            player_speed=data["player_speed"],
            enemy_speed=data["enemy_speed"] * factor,
            spawn_rate=max(
                0.2,
                data["spawn_rate"] / factor
            ),
            health=data["health"],
            score_multiplier=data["score_multiplier"] * factor,
            special_rules=dict(data["special_rules"]),
        )
