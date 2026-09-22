import random
from dataclasses import dataclass
from typing import Dict, List

from ajvyra_game_genre_registry import AJVYGameGenreRegistry
from ajvyra_game_mechanics_engine import AJVYGameMechanicsEngine


@dataclass
class GameVariation:
    game_id: int
    title: str
    genre: str
    objective: str
    mechanics: List[str]
    difficulty_factor: float
    seed: int


class AJVYRAIGameVariationEngine:
    """
    Makes the 70 games different from one another.

    Genre is not the only variable:
    objective, mechanics, difficulty and seed also vary.
    """

    def __init__(self):
        self.registry = AJVYGameGenreRegistry()
        self.mechanics = AJVYGameMechanicsEngine()

        self.title_parts = {
            "rpg": [
                "Echoes of",
                "Kingdom of",
                "Chronicles of",
                "Legacy of",
            ],
            "platformer": [
                "Skybound",
                "Neon Leap",
                "Moon Jump",
                "Last Platform",
            ],
            "horror": [
                "The Silent",
                "Nocturne",
                "Whispers in",
                "The Forgotten",
            ],
            "racing": [
                "Velocity",
                "Night Circuit",
                "Zero Mile",
                "Final Lap",
            ],
            "puzzle": [
                "Mindlock",
                "Fractured Pattern",
                "The Last Cipher",
                "Echo Grid",
            ],
            "survival": [
                "Afterfall",
                "Last Shelter",
                "Ash Survival",
                "Seven Nights",
            ],
            "adventure": [
                "Beyond",
                "Lost Horizon",
                "The Hidden Path",
                "Wanderer",
            ],
            "shooter": [
                "Dark Sector",
                "Void Strike",
                "Red Orbit",
                "Final Defense",
            ],
            "stealth": [
                "Silent Step",
                "Shadow Protocol",
                "No Witness",
                "Black Corridor",
            ],
            "runner": [
                "Never Stop",
                "Night Runner",
                "Endless Road",
                "Last Run",
            ],
        }

        self.second_words = [
            "Veyra",
            "Nox",
            "Aelith",
            "Raven",
            "Sol",
            "Kael",
            "Mora",
            "Nyx",
            "Lun",
            "Orin",
            "Elyra",
            "Vael",
        ]

    def choose_genre(self, game_id: int) -> str:
        names = self.registry.names()

        return names[(game_id - 1) % len(names)]

    def create_variation(self, game_id: int) -> GameVariation:
        genre = self.choose_genre(game_id)
        definition = self.registry.get(genre)

        seed = 10000 + game_id * 7919
        rng = random.Random(seed)

        prefix = rng.choice(self.title_parts[genre])
        suffix = rng.choice(self.second_words)

        title = f"{prefix} {suffix}"

        objective = rng.choice(
            definition.objective_types
        )

        mechanics = list(definition.mechanics)

        rng.shuffle(mechanics)

        selected_mechanics = mechanics[
            :min(4, len(mechanics))
        ]

        difficulty = round(
            0.75 + rng.random() * 1.1,
            2
        )

        return GameVariation(
            game_id=game_id,
            title=title,
            genre=genre,
            objective=objective,
            mechanics=selected_mechanics,
            difficulty_factor=difficulty,
            seed=seed,
        )

    def build_runtime_profile(
        self,
        variation: GameVariation,
    ) -> Dict:

        profile = self.mechanics.build_profile(
            genre=variation.genre,
            mechanics=variation.mechanics,
            difficulty_factor=variation.difficulty_factor,
        )

        return {
            "genre": profile.genre,
            "mechanics": profile.mechanics,
            "player_speed": profile.player_speed,
            "enemy_speed": profile.enemy_speed,
            "spawn_rate": profile.spawn_rate,
            "health": profile.health,
            "score_multiplier": profile.score_multiplier,
            "special_rules": profile.special_rules,
        }
