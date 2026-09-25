"""
AJVYRA 143 — Underground Fighter
Genre: Fighting / Career
"""

from dataclasses import dataclass


@dataclass
class Fighter:
    name: str
    power: int
    speed: int
    guard: int
    stamina: int = 100


class UndergroundFighter:
    title = "Underground Fighter"
    fighter_name = "Jax Vero"

    def __init__(self):
        self.cash = 500
        self.reputation = 0
        self.fight_number = 1

        self.fighter = Fighter(
            self.fighter_name,
            80,
            85,
            70,
        )

    def train(self, attribute):
        if self.cash < 100:
            return False

        allowed = {
            "power",
            "speed",
            "guard",
        }

        if attribute not in allowed:
            return False

        self.cash -= 100

        value = getattr(
            self.fighter,
            attribute,
        )

        setattr(
            self.fighter,
            attribute,
            value + 5,
        )

        return True

    def fight(self, opponent_power):
        own_power = (
            self.fighter.power * 0.4
            + self.fighter.speed * 0.35
            + self.fighter.guard * 0.25
        )

        own_power *= self.fighter.stamina / 100

        self.fighter.stamina = max(
            20,
            self.fighter.stamina - 25,
        )

        if own_power >= opponent_power:
            reward = 250 + self.fight_number * 50
            self.cash += reward
            self.reputation += 15
            self.fight_number += 1
            return True

        self.reputation = max(
            0,
            self.reputation - 5,
        )
        return False

    def recover(self):
        self.fighter.stamina = min(
            100,
            self.fighter.stamina + 40,
        )

    def status(self):
        return {
            "fighter": self.fighter.name,
            "cash": self.cash,
            "reputation": self.reputation,
            "fight_number": self.fight_number,
            "power": self.fighter.power,
            "speed": self.fighter.speed,
            "guard": self.fighter.guard,
            "stamina": self.fighter.stamina,
        }


def create_game():
    return UndergroundFighter()


if __name__ == "__main__":
    game = create_game()
    game.train("speed")
    game.fight(70)
    print(game.status())
