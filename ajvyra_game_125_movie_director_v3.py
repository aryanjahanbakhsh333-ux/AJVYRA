"""
AJVYRA 125 — Movie Director
Genre: Creative Management
"""

from dataclasses import dataclass


@dataclass
class Scene:
    name: str
    mood: str
    difficulty: int
    completed: bool = False


class MovieDirector:
    title = "Movie Director"
    director = "Arden Lux"

    def __init__(self):
        self.budget = 1000
        self.fame = 0
        self.audience = 0
        self.energy = 100

        self.scenes = [
            Scene("Opening", "mystery", 20),
            Scene("Chase", "action", 35),
            Scene("Revelation", "emotional", 40),
            Scene("Finale", "epic", 50),
        ]

    def film_scene(self, index, performance):
        if not 0 <= index < len(self.scenes):
            return False

        scene = self.scenes[index]

        if scene.completed:
            return False

        cost = scene.difficulty * 2

        if self.budget < cost or self.energy < 10:
            return False

        self.budget -= cost
        self.energy -= 10

        quality = (
            performance * 0.7
            + (100 - scene.difficulty) * 0.3
        )

        if quality >= 65:
            scene.completed = True
            self.fame += int(quality / 10)
            self.audience += int(quality)
            return True

        return False

    def reshoot(self, index):
        if not 0 <= index < len(self.scenes):
            return False

        self.budget -= 50
        self.energy = max(0, self.energy - 5)
        return True

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def movie_finished(self):
        return all(scene.completed for scene in self.scenes)

    def status(self):
        return {
            "director": self.director,
            "budget": self.budget,
            "fame": self.fame,
            "audience": self.audience,
            "energy": self.energy,
            "scenes": [
                {
                    "name": s.name,
                    "mood": s.mood,
                    "completed": s.completed,
                }
                for s in self.scenes
            ],
            "finished": self.movie_finished(),
        }


def create_game():
    return MovieDirector()


if __name__ == "__main__":
    game = create_game()

    for i in range(4):
        game.film_scene(i, 90)

    print(game.status())
