from dataclasses import dataclass
from typing import List


@dataclass
class Performer:
    name: str
    skill: int
    stamina: int = 100
    morale: int = 70


class CircusShowManager:
    def __init__(self):
        self.manager = "Raya Moon"
        self.money = 500
        self.audience = 0
        self.reputation = 10
        self.score = 0

        self.performers: List[Performer] = [
            Performer("Lio", 75),
            Performer("Nara", 82),
            Performer("Vex", 68),
            Performer("Sena", 88),
        ]

    def rehearse(self, index: int):
        if not (0 <= index < len(self.performers)):
            return False

        performer = self.performers[index]

        if performer.stamina < 15:
            return False

        performer.stamina -= 15
        performer.skill = min(100, performer.skill + 3)
        performer.morale = min(100, performer.morale + 5)
        self.score += 12
        return True

    def perform_show(self):
        total_skill = sum(p.skill for p in self.performers)
        average = total_skill // len(self.performers)

        self.audience += average * 8
        self.money += average * 4
        self.reputation += average // 20
        self.score += average * 5

        for performer in self.performers:
            performer.stamina -= 20

        return average

    def improve_stage(self):
        if self.money < 150:
            return False

        self.money -= 150
        self.score += 75
        self.reputation += 3
        return True

    def rest_team(self):
        for performer in self.performers:
            performer.stamina = min(100, performer.stamina + 30)
            performer.morale = min(100, performer.morale + 10)

    def status(self):
        return {
            "manager": self.manager,
            "money": self.money,
            "audience": self.audience,
            "reputation": self.reputation,
            "score": self.score,
            "performers": [
                {
                    "name": p.name,
                    "skill": p.skill,
                    "stamina": p.stamina,
                    "morale": p.morale,
                }
                for p in self.performers
            ],
        }


def create_game():
    return CircusShowManager()


def demo():
    game = create_game()
    game.rehearse(0)
    game.rehearse(1)
    game.rehearse(2)
    game.rehearse(3)
    game.improve_stage()
    game.perform_show()
    return game.status()


if __name__ == "__main__":
    print(demo())
