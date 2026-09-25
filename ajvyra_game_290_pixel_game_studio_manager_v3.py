from dataclasses import dataclass


@dataclass
class GameProject:
    name: str
    budget: int
    quality: int = 20
    hype: int = 10
    completed: bool = False


class PixelGameStudioManager:
    def __init__(self):
        self.manager = "Alex Byte"
        self.money = 1500
        self.fans = 100
        self.reputation = 20
        self.energy = 100
        self.score = 0
        self.day = 1
        self.projects = [
            GameProject("Neon Runner", 500),
            GameProject("Moon Quest", 700),
            GameProject("Clockwork City", 900),
        ]

    def design(self, index: int):
        if not 0 <= index < len(self.projects):
            return False

        project = self.projects[index]

        if self.energy < 10 or self.money < 40:
            return False

        self.energy -= 10
        self.money -= 40
        project.quality = min(
            100,
            project.quality + 12
        )
        self.score += 35
        return True

    def advertise(self, index: int):
        if not 0 <= index < len(self.projects):
            return False

        if self.money < 100:
            return False

        self.money -= 100
        self.projects[index].hype = min(
            100,
            self.projects[index].hype + 20
        )
        self.fans += 30
        self.score += 50
        return True

    def hire_developer(self):
        if self.money < 250:
            return False

        self.money -= 250
        self.reputation += 5
        self.score += 80
        return True

    def release_game(self, index: int):
        if not 0 <= index < len(self.projects):
            return False

        project = self.projects[index]

        if project.completed:
            return False

        if project.quality < 70:
            return False

        project.completed = True

        success = (
            project.quality
            + project.hype
        )

        self.fans += success
        self.money += success * 4
        self.reputation += 10
        self.score += success * 3
        return True

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def next_day(self):
        self.day += 1
        self.energy = min(100, self.energy + 15)
        self.money += self.reputation * 2

    def status(self):
        return {
            "manager": self.manager,
            "day": self.day,
            "money": self.money,
            "fans": self.fans,
            "reputation": self.reputation,
            "energy": self.energy,
            "score": self.score,
            "released_games": sum(
                p.completed for p in self.projects
            ),
            "projects": len(self.projects),
        }


def create_game():
    return PixelGameStudioManager()


if __name__ == "__main__":
    game = create_game()
    game.design(0)
    game.advertise(0)
    game.hire_developer()
    print(game.status())
