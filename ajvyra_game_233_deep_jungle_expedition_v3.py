from dataclasses import dataclass


@dataclass
class Explorer:
    name: str
    health: int = 100
    stamina: int = 100
    survival: int = 60
    knowledge: int = 40


class DeepJungleExpedition:
    def __init__(self):
        self.explorer = Explorer("Tarin Moss")
        self.location = 0
        self.goal = 12
        self.supplies = 10
        self.artifacts = 0
        self.score = 0
        self.weather = "humid"
        self.completed = False

    def advance(self):
        if self.explorer.stamina < 15 or self.supplies <= 0:
            return False

        self.explorer.stamina -= 15
        self.supplies -= 1
        self.location += 1
        self.score += 20
        return True

    def study_ruins(self):
        if self.location < 3 or self.explorer.stamina < 10:
            return False

        self.explorer.stamina -= 10
        self.explorer.knowledge += 10
        self.score += 45
        self.artifacts += 1
        return True

    def forage(self):
        if self.explorer.stamina < 8:
            return False

        self.explorer.stamina -= 8
        self.supplies += 3
        self.score += 10
        return True

    def cross_river(self):
        if self.location < 5:
            return False

        if self.explorer.survival < 50:
            self.explorer.health -= 15
            return False

        self.location += 2
        self.score += 60
        return True

    def rest(self):
        self.explorer.stamina = min(100, self.explorer.stamina + 30)
        self.explorer.health = min(100, self.explorer.health + 10)

    def complete_expedition(self):
        if self.location >= self.goal:
            self.completed = True
            self.score += 300
            return True
        return False

    def status(self):
        return {
            "explorer": self.explorer.name,
            "location": self.location,
            "goal": self.goal,
            "health": self.explorer.health,
            "stamina": self.explorer.stamina,
            "supplies": self.supplies,
            "artifacts": self.artifacts,
            "score": self.score,
            "completed": self.completed,
        }


def create_game():
    return DeepJungleExpedition()


if __name__ == "__main__":
    game = create_game()
    game.advance()
    game.forage()
    game.rest()
    print(game.status())
