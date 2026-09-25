from dataclasses import dataclass


@dataclass
class Pilot:
    name: str
    reflex: int = 70
    shield: int = 100
    energy: int = 100
    fuel: int = 100


class MeteorShowerSurvival:
    def __init__(self):
        self.pilot = Pilot("Kael Orion")
        self.distance = 0
        self.goal = 3000
        self.score = 0
        self.wave = 1
        self.destroyed_meteors = 0
        self.survived = False

    def accelerate(self):
        if self.pilot.fuel < 10 or self.pilot.energy < 5:
            return False

        self.pilot.fuel -= 10
        self.pilot.energy -= 5
        self.distance += 180
        self.score += 30
        return True

    def dodge(self):
        if self.pilot.energy < 12:
            return False

        self.pilot.energy -= 12

        if self.pilot.reflex >= 65:
            self.score += 60
            return True

        self.pilot.shield -= 15
        return False

    def activate_shield(self):
        if self.pilot.energy < 20:
            return False

        self.pilot.energy -= 20
        self.pilot.shield = min(100, self.pilot.shield + 30)
        self.score += 35
        return True

    def destroy_meteor(self):
        if self.pilot.energy < 15:
            return False

        self.pilot.energy -= 15
        self.destroyed_meteors += 1
        self.score += 90
        return True

    def next_wave(self):
        self.wave += 1
        self.pilot.fuel = max(0, self.pilot.fuel - 5)

    def reach_destination(self):
        if self.distance < self.goal or self.pilot.shield <= 0:
            return False

        self.survived = True
        self.score += 600
        return True

    def status(self):
        return {
            "pilot": self.pilot.name,
            "distance": self.distance,
            "goal": self.goal,
            "shield": self.pilot.shield,
            "energy": self.pilot.energy,
            "fuel": self.pilot.fuel,
            "wave": self.wave,
            "meteors": self.destroyed_meteors,
            "score": self.score,
            "survived": self.survived,
        }


def create_game():
    return MeteorShowerSurvival()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.dodge()
    game.destroy_meteor()
    print(game.status())
