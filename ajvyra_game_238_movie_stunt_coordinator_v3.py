from dataclasses import dataclass


@dataclass
class StuntPerformer:
    name: str
    agility: int
    courage: int
    stamina: int = 100
    reputation: int = 20


class MovieStuntCoordinator:
    def __init__(self):
        self.coordinator = "Rex Vale"
        self.budget = 1000
        self.fame = 0
        self.score = 0
        self.scene = 1
        self.performer = StuntPerformer(
            "Jax Orion",
            agility=75,
            courage=70,
        )
        self.completed_scenes = 0

    def rehearse(self):
        if self.performer.stamina < 15:
            return False

        self.performer.stamina -= 15
        self.performer.agility += 2
        self.score += 15
        return True

    def shoot_scene(self, difficulty: int):
        cost = difficulty * 10

        if self.budget < cost or self.performer.stamina < difficulty:
            return False

        self.budget -= cost
        self.performer.stamina -= difficulty

        skill = self.performer.agility + self.performer.courage

        if skill >= difficulty * 2:
            self.fame += difficulty
            self.score += difficulty * 20
            self.completed_scenes += 1
            self.scene += 1
            return True

        self.score += 5
        return False

    def rest_performer(self):
        self.performer.stamina = min(
            100,
            self.performer.stamina + 35
        )

    def upgrade_equipment(self):
        if self.budget < 150:
            return False

        self.budget -= 150
        self.performer.agility += 10
        self.performer.reputation += 5
        self.score += 30
        return True

    def status(self):
        return {
            "coordinator": self.coordinator,
            "performer": self.performer.name,
            "scene": self.scene,
            "budget": self.budget,
            "fame": self.fame,
            "score": self.score,
            "stamina": self.performer.stamina,
            "completed_scenes": self.completed_scenes,
        }


def create_game():
    return MovieStuntCoordinator()


if __name__ == "__main__":
    game = create_game()
    game.rehearse()
    game.shoot_scene(25)
    game.rest_performer()
    print(game.status())
