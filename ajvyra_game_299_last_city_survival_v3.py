from dataclasses import dataclass


@dataclass
class Survivor:
    name: str
    health: int = 100
    stamina: int = 100
    food: int = 60
    water: int = 60


class LastCitySurvival:
    def __init__(self):
        self.survivor = Survivor("Evan Cross")
        self.city_zone = 0
        self.supplies = 20
        self.days = 0
        self.score = 0
        self.shelter = 40
        self.signal_strength = 0
        self.rescued = False

    def explore(self):
        if self.survivor.stamina < 15:
            return False

        self.survivor.stamina -= 15
        self.survivor.food -= 5
        self.survivor.water -= 6
        self.city_zone += 1
        self.supplies += 4
        self.score += 40
        return True

    def search_supplies(self):
        if self.survivor.stamina < 10:
            return False

        self.survivor.stamina -= 10
        self.supplies += 8
        self.score += 60
        return True

    def reinforce_shelter(self):
        if self.supplies < 5:
            return False

        self.supplies -= 5
        self.shelter = min(
            100,
            self.shelter + 15
        )
        self.score += 45
        return True

    def build_signal(self):
        if self.supplies < 10:
            return False

        self.supplies -= 10
        self.signal_strength = min(
            100,
            self.signal_strength + 30
        )
        self.score += 100
        return True

    def rest(self):
        self.survivor.stamina = min(
            100,
            self.survivor.stamina + 30
        )
        self.survivor.health = min(
            100,
            self.survivor.health + 10
        )

    def survive_day(self):
        self.days += 1
        self.survivor.food = max(
            0,
            self.survivor.food - 5
        )
        self.survivor.water = max(
            0,
            self.survivor.water - 6
        )

        if self.survivor.food == 0:
            self.survivor.health -= 5

        if self.survivor.water == 0:
            self.survivor.health -= 8

        self.score += 25

    def call_rescue(self):
        if self.signal_strength < 90:
            return False

        self.rescued = True
        self.score += 700
        return True

    def status(self):
        return {
            "survivor": self.survivor.name,
            "days": self.days,
            "zone": self.city_zone,
            "health": self.survivor.health,
            "stamina": self.survivor.stamina,
            "food": self.survivor.food,
            "water": self.survivor.water,
            "supplies": self.supplies,
            "shelter": self.shelter,
            "signal": self.signal_strength,
            "score": self.score,
            "rescued": self.rescued,
        }


def create_game():
    return LastCitySurvival()


if __name__ == "__main__":
    game = create_game()
    game.explore()
    game.search_supplies()
    game.reinforce_shelter()
    game.build_signal()
    print(game.status())
