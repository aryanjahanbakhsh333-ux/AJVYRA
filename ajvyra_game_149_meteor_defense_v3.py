"""
AJVYRA 149 — Meteor Defense
Genre: Space Defense / Strategy
"""

from dataclasses import dataclass


@dataclass
class Meteor:
    name: str
    size: int
    speed: int
    health: int


class MeteorDefense:
    title = "Meteor Defense"
    commander = "Sol Vega"

    def __init__(self):
        self.energy = 100
        self.ammo = 50
        self.credits = 1000
        self.score = 0
        self.wave = 1

        self.meteors = [
            Meteor("Alpha", 20, 4, 40),
            Meteor("Beta", 35, 5, 65),
            Meteor("Gamma", 50, 7, 90),
        ]

    def fire(self, index, power):
        if not 0 <= index < len(self.meteors):
            return False

        if self.ammo <= 0 or power <= 0:
            return False

        meteor = self.meteors[index]

        self.ammo -= 1
        self.energy = max(
            0,
            self.energy - power // 10,
        )

        meteor.health -= power

        if meteor.health <= 0:
            self.score += meteor.size * 10
            self.credits += meteor.size * 5
            return True

        return False

    def repair_system(self):
        if self.credits < 150:
            return False

        self.credits -= 150
        self.energy = min(
            100,
            self.energy + 30,
        )
        return True

    def reload(self):
        if self.credits < 100:
            return False

        self.credits -= 100
        self.ammo += 20
        return True

    def clear_destroyed(self):
        self.meteors = [
            m for m in self.meteors
            if m.health > 0
        ]

    def next_wave(self):
        self.clear_destroyed()

        if self.meteors:
            return False

        self.wave += 1
        self.ammo += 10
        self.energy = min(
            100,
            self.energy + 20,
        )
        return True

    def status(self):
        return {
            "commander": self.commander,
            "wave": self.wave,
            "energy": self.energy,
            "ammo": self.ammo,
            "credits": self.credits,
            "score": self.score,
            "remaining_meteors": len(self.meteors),
        }


def create_game():
    return MeteorDefense()


if __name__ == "__main__":
    game = create_game()
    game.fire(0, 50)
    game.clear_destroyed()
    print(game.status())
