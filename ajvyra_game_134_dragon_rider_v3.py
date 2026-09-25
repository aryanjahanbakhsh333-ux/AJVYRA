"""
AJVYRA 134 — Dragon Rider
Genre: Fantasy Flight / Adventure
"""

from dataclasses import dataclass


@dataclass
class Dragon:
    name: str
    power: int
    speed: int
    trust: int = 40
    stamina: int = 100


class DragonRider:
    title = "Dragon Rider"
    rider = "Aren Sky"

    def __init__(self):
        self.dragon = Dragon(
            "Vaelor",
            power=85,
            speed=90,
        )
        self.altitude = 0
        self.distance = 0
        self.score = 0
        self.gems = 5

    def fly(self, distance, altitude):
        cost = max(5, distance // 5 + altitude // 100)

        if self.dragon.stamina < cost:
            return False

        self.dragon.stamina -= cost
        self.distance += distance
        self.altitude = altitude
        self.score += distance + altitude // 10
        return True

    def train(self):
        if self.gems <= 0:
            return False

        self.gems -= 1
        self.dragon.trust = min(
            100,
            self.dragon.trust + 10,
        )
        self.dragon.power += 2
        self.dragon.speed += 2
        return True

    def rest(self):
        self.dragon.stamina = min(
            100,
            self.dragon.stamina + 35,
        )

    def challenge(self, difficulty):
        power = (
            self.dragon.power
            + self.dragon.speed
            + self.dragon.trust
        )

        if power >= difficulty:
            self.score += difficulty * 2
            return True

        self.dragon.stamina = max(
            0,
            self.dragon.stamina - 20,
        )
        return False

    def status(self):
        return {
            "rider": self.rider,
            "dragon": self.dragon.name,
            "power": self.dragon.power,
            "speed": self.dragon.speed,
            "trust": self.dragon.trust,
            "stamina": self.dragon.stamina,
            "distance": self.distance,
            "score": self.score,
        }


def create_game():
    return DragonRider()


if __name__ == "__main__":
    game = create_game()
    game.train()
    game.fly(40, 800)
    game.challenge(180)
    print(game.status())
