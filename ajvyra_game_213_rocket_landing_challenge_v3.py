from dataclasses import dataclass


@dataclass
class Pilot:
    name: str
    fuel: int = 100
    altitude: int = 5000
    velocity: int = 100
    heat: int = 20
    landing_score: int = 0


class RocketLandingChallenge:
    def __init__(self):
        self.pilot = Pilot("Orin Vale")
        self.score = 0
        self.landed = False

    def thrust(self, power: int):
        if power < 1 or power > 10:
            return False

        fuel_cost = power * 2

        if self.pilot.fuel < fuel_cost:
            return False

        self.pilot.fuel -= fuel_cost
        self.pilot.velocity = max(
            0,
            self.pilot.velocity - power * 4
        )
        self.pilot.altitude = max(
            0,
            self.pilot.altitude - power * 150
        )
        self.pilot.heat += power * 2
        self.score += power * 5
        return True

    def stabilize(self):
        self.pilot.velocity = max(
            0,
            self.pilot.velocity - 8
        )
        self.pilot.heat = max(
            0,
            self.pilot.heat - 5
        )
        self.score += 15

    def cool_engines(self):
        self.pilot.heat = max(
            0,
            self.pilot.heat - 20
        )
        self.pilot.fuel = max(
            0,
            self.pilot.fuel - 3
        )

    def landing_attempt(self):
        if self.pilot.altitude > 200:
            return False

        if self.pilot.velocity > 15:
            self.pilot.landing_score -= 30
            return False

        if self.pilot.heat > 70:
            return False

        self.landed = True
        self.pilot.landing_score += 100
        self.score += self.pilot.landing_score
        return True

    def status(self):
        return {
            "pilot": self.pilot.name,
            "fuel": self.pilot.fuel,
            "altitude": self.pilot.altitude,
            "velocity": self.pilot.velocity,
            "heat": self.pilot.heat,
            "score": self.score,
            "landed": self.landed,
        }


def create_game():
    return RocketLandingChallenge()


def demo():
    game = create_game()

    for _ in range(8):
        game.thrust(5)

    game.stabilize()
    game.cool_engines()
    game.landing_attempt()

    return game.status()


if __name__ == "__main__":
    print(demo())
