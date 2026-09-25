from dataclasses import dataclass


@dataclass
class Survivor:
    name: str
    health: int = 100
    stamina: int = 100
    survival: int = 60


class LostIslandSurvivalBuilder:
    def __init__(self):
        self.survivor = Survivor("Eli Storm")
        self.wood = 80
        self.food = 60
        self.water = 60
        self.shelter = 20
        self.day = 1
        self.score = 0
        self.rescue_signal = 0

    def gather_wood(self):
        if self.survivor.stamina < 10:
            return False

        self.survivor.stamina -= 10
        self.wood += 35
        self.score += 20
        return True

    def gather_food(self):
        if self.survivor.stamina < 12:
            return False

        self.survivor.stamina -= 12
        self.food += 25
        self.score += 20
        return True

    def build_shelter(self):
        if self.wood < 40:
            return False

        self.wood -= 40
        self.shelter = min(100, self.shelter + 25)
        self.score += 50
        return True

    def build_rescue_signal(self):
        if self.wood < 60:
            return False

        self.wood -= 60
        self.rescue_signal += 25
        self.score += 80
        return True

    def survive_day(self):
        self.day += 1
        self.food = max(0, self.food - 10)
        self.water = max(0, self.water - 12)
        self.survivor.stamina = max(
            0,
            self.survivor.stamina - 8
        )

        if self.food == 0 or self.water == 0:
            self.survivor.health = max(
                0,
                self.survivor.health - 15
            )

    def signal_rescue(self):
        if self.rescue_signal < 100:
            return False

        self.score += 400
        return True

    def status(self):
        return {
            "survivor": self.survivor.name,
            "day": self.day,
            "health": self.survivor.health,
            "stamina": self.survivor.stamina,
            "wood": self.wood,
            "food": self.food,
            "water": self.water,
            "shelter": self.shelter,
            "rescue_signal": self.rescue_signal,
            "score": self.score,
        }


def create_game():
    return LostIslandSurvivalBuilder()


if __name__ == "__main__":
    game = create_game()
    game.gather_wood()
    game.build_shelter()
    game.gather_food()
    game.survive_day()
    print(game.status())
