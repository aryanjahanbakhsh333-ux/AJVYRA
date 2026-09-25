from dataclasses import dataclass


@dataclass
class Balloon:
    pilot: str
    altitude: int = 100
    fuel: int = 100
    stability: int = 80
    discoveries: int = 0


class AirBalloonExpedition:
    def __init__(self):
        self.balloon = Balloon("Lena Vey")
        self.location = "Green Valley"
        self.score = 0
        self.wind = 20

    def ascend(self, amount: int):
        if amount <= 0 or self.fuel_cost(amount) > self.balloon.fuel:
            return False

        self.balloon.altitude += amount
        self.balloon.fuel -= self.fuel_cost(amount)
        self.balloon.stability -= amount // 100
        self.score += amount // 2
        return True

    def fuel_cost(self, amount):
        return max(2, amount // 50)

    def descend(self, amount: int):
        self.balloon.altitude = max(
            0,
            self.balloon.altitude - amount
        )
        self.balloon.stability = min(
            100,
            self.balloon.stability + 3
        )
        return True

    def scan_landscape(self):
        if self.balloon.stability < 30:
            return False

        self.balloon.discoveries += 1
        self.score += 50
        return True

    def navigate_wind(self, skill: int):
        if skill >= self.wind // 2:
            self.balloon.stability = min(
                100,
                self.balloon.stability + 10
            )
            self.score += 30
            return True

        self.balloon.stability -= 15
        return False

    def land(self):
        self.balloon.altitude = 0
        self.score += 25

    def status(self):
        return {
            "pilot": self.balloon.pilot,
            "location": self.location,
            "altitude": self.balloon.altitude,
            "fuel": self.balloon.fuel,
            "stability": self.balloon.stability,
            "discoveries": self.balloon.discoveries,
            "score": self.score,
        }


def create_game():
    return AirBalloonExpedition()


def demo():
    game = create_game()
    game.ascend(300)
    game.navigate_wind(15)
    game.scan_landscape()
    game.ascend(200)
    game.scan_landscape()
    game.land()
    return game.status()


if __name__ == "__main__":
    print(demo())
