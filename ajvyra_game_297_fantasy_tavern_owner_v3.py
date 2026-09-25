from dataclasses import dataclass


@dataclass
class Tavern:
    name: str
    reputation: int = 30
    capacity: int = 20
    comfort: int = 60
    supplies: int = 100


class FantasyTavernOwner:
    def __init__(self):
        self.owner = "Mira Ember"
        self.tavern = Tavern("The Silver Lantern")
        self.gold = 400
        self.guests = 0
        self.fame = 10
        self.score = 0
        self.day = 1

    def cook_meal(self):
        if self.tavern.supplies < 10:
            return False

        self.tavern.supplies -= 10
        self.tavern.comfort += 3
        self.score += 30
        return True

    def serve_guests(self, amount: int):
        if amount <= 0:
            return False

        if self.guests + amount > self.tavern.capacity:
            return False

        if self.tavern.supplies < amount * 3:
            return False

        self.tavern.supplies -= amount * 3
        self.guests += amount
        self.gold += amount * 25
        self.fame += amount
        self.score += amount * 20
        return True

    def hire_bard(self):
        if self.gold < 150:
            return False

        self.gold -= 150
        self.fame += 10
        self.tavern.reputation += 8
        self.score += 70
        return True

    def decorate(self):
        if self.gold < 100:
            return False

        self.gold -= 100
        self.tavern.comfort = min(
            100,
            self.tavern.comfort + 15
        )
        self.score += 50
        return True

    def buy_supplies(self):
        if self.gold < 80:
            return False

        self.gold -= 80
        self.tavern.supplies += 60
        return True

    def next_day(self):
        self.day += 1
        self.guests = 0

    def status(self):
        return {
            "owner": self.owner,
            "tavern": self.tavern.name,
            "day": self.day,
            "gold": self.gold,
            "reputation": self.tavern.reputation,
            "comfort": self.tavern.comfort,
            "supplies": self.tavern.supplies,
            "fame": self.fame,
            "score": self.score,
        }


def create_game():
    return FantasyTavernOwner()


if __name__ == "__main__":
    game = create_game()
    game.cook_meal()
    game.serve_guests(5)
    game.hire_bard()
    print(game.status())
