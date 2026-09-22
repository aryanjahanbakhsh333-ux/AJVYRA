from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class GameGenre:
    name: str
    description: str
    mechanics: List[str]
    camera: str
    objective_types: List[str]
    difficulty: str


class AJVYGameGenreRegistry:
    """
    Central registry for AJVYRA's playable game genres.

    Each genre describes a different gameplay family.
    """

    def __init__(self):
        self.genres: Dict[str, GameGenre] = {
            "rpg": GameGenre(
                name="RPG",
                description="Exploration, combat, quests and progression.",
                mechanics=[
                    "exploration",
                    "combat",
                    "experience",
                    "inventory",
                    "quests",
                    "boss"
                ],
                camera="top_down",
                objective_types=[
                    "defeat_boss",
                    "complete_quest",
                    "collect_artifacts"
                ],
                difficulty="adaptive"
            ),

            "platformer": GameGenre(
                name="Platformer",
                description="Jump across platforms while avoiding hazards.",
                mechanics=[
                    "jumping",
                    "gravity",
                    "platforms",
                    "collectibles",
                    "hazards"
                ],
                camera="side_scroll",
                objective_types=[
                    "reach_exit",
                    "collect_items",
                    "survive"
                ],
                difficulty="adaptive"
            ),

            "horror": GameGenre(
                name="Horror",
                description="Dark survival gameplay with limited resources.",
                mechanics=[
                    "fear",
                    "darkness",
                    "enemy_chase",
                    "battery",
                    "escape"
                ],
                camera="top_down",
                objective_types=[
                    "escape",
                    "survive",
                    "find_key"
                ],
                difficulty="adaptive"
            ),

            "racing": GameGenre(
                name="Racing",
                description="Fast arcade racing with obstacles and checkpoints.",
                mechanics=[
                    "acceleration",
                    "steering",
                    "boost",
                    "checkpoints",
                    "laps"
                ],
                camera="top_down",
                objective_types=[
                    "finish_race",
                    "beat_time",
                    "complete_laps"
                ],
                difficulty="adaptive"
            ),

            "puzzle": GameGenre(
                name="Puzzle",
                description="Logic challenges based on patterns and decisions.",
                mechanics=[
                    "matching",
                    "memory",
                    "patterns",
                    "timers",
                    "progression"
                ],
                camera="board",
                objective_types=[
                    "solve_puzzle",
                    "clear_board",
                    "reach_score"
                ],
                difficulty="adaptive"
            ),

            "survival": GameGenre(
                name="Survival",
                description="Stay alive while resources become increasingly scarce.",
                mechanics=[
                    "resources",
                    "waves",
                    "health",
                    "crafting",
                    "enemy_spawn"
                ],
                camera="top_down",
                objective_types=[
                    "survive_time",
                    "defeat_waves",
                    "collect_resources"
                ],
                difficulty="adaptive"
            ),

            "adventure": GameGenre(
                name="Adventure",
                description="Explore locations and complete objectives.",
                mechanics=[
                    "exploration",
                    "interaction",
                    "collectibles",
                    "secrets",
                    "story_events"
                ],
                camera="top_down",
                objective_types=[
                    "discover",
                    "collect",
                    "reach_destination"
                ],
                difficulty="story"
            ),

            "shooter": GameGenre(
                name="Shooter",
                description="Real-time combat with enemies and projectiles.",
                mechanics=[
                    "shooting",
                    "enemy_ai",
                    "projectiles",
                    "health",
                    "waves"
                ],
                camera="top_down",
                objective_types=[
                    "defeat_enemies",
                    "survive_waves",
                    "defeat_boss"
                ],
                difficulty="adaptive"
            ),

            "stealth": GameGenre(
                name="Stealth",
                description="Avoid detection and reach the objective.",
                mechanics=[
                    "visibility",
                    "enemy_patrol",
                    "hiding",
                    "noise",
                    "escape"
                ],
                camera="top_down",
                objective_types=[
                    "avoid_detection",
                    "steal_object",
                    "escape"
                ],
                difficulty="adaptive"
            ),

            "runner": GameGenre(
                name="Endless Runner",
                description="Run continuously while avoiding increasingly difficult obstacles.",
                mechanics=[
                    "automatic_running",
                    "jumping",
                    "sliding",
                    "obstacles",
                    "score"
                ],
                camera="side_scroll",
                objective_types=[
                    "survive",
                    "reach_score",
                    "beat_distance"
                ],
                difficulty="progressive"
            ),
        }

    def get(self, genre: str) -> GameGenre:
        key = genre.lower().strip()

        if key not in self.genres:
            raise ValueError(f"Unknown game genre: {genre}")

        return self.genres[key]

    def names(self) -> List[str]:
        return list(self.genres.keys())

    def all(self) -> Dict[str, GameGenre]:
        return dict(self.genres)

    def genre_for_index(self, index: int) -> GameGenre:
        names = self.names()

        if not names:
            raise RuntimeError("No genres registered.")

        return self.genres[names[index % len(names)]]
