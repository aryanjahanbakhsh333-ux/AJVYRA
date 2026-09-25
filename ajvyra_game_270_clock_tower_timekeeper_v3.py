from dataclasses import dataclass


@dataclass
class ClockMechanism:
    name: str
    condition: int = 100
    precision: int = 60
    power: int = 70


class ClockTowerTimekeeper:
    def __init__(self):
        self.timekeeper = "Orion Bell"
        self.hour = 12
        self.energy = 100
        self.score = 0
        self.coins = 150
        self.time_stability = 80
        self.mechanisms = [
            ClockMechanism("Main Gear"),
            ClockMechanism("Pendulum"),
            ClockMechanism("Moon Dial"),
            ClockMechanism("Bell Engine"),
        ]

    def wind_mechanism(self, index: int):
        if not 0 <= index < len(self.mechanisms):
            return False

        if self.energy < 10:
            return False

        mechanism = self.mechanisms[index]
        self.energy -= 10
        mechanism.power = min(100, mechanism.power + 15)
        mechanism.condition = min(100, mechanism.condition + 5)
        self.score += 25
        return True

    def calibrate(self, index: int):
        if not 0 <= index < len(self.mechanisms):
            return False

        mechanism = self.mechanisms[index]

        if self.energy < 15:
            return False

        self.energy -= 15
        mechanism.precision = min(
            100,
            mechanism.precision + 10
        )
        self.time_stability = min(
            100,
            self.time_stability + 5
        )
        self.score += 40
        return True

    def ring_bell(self):
        if self.mechanisms[3].power < 50:
            return False

        self.hour = (self.hour + 1) % 24
        self.time_stability = min(
            100,
            self.time_stability + 8
        )
        self.coins += 20
        self.score += 60
        return True

    def repair_tower(self):
        if self.coins < 50:
            return False

        self.coins -= 50

        for mechanism in self.mechanisms:
            mechanism.condition = min(
                100,
                mechanism.condition + 15
            )

        self.score += 50
        return True

    def restore_time(self):
        if self.time_stability < 100:
            self.time_stability = min(
                100,
                self.time_stability + 20
            )
            self.score += 80
            return True

        return False

    def status(self):
        return {
            "timekeeper": self.timekeeper,
            "hour": self.hour,
            "energy": self.energy,
            "coins": self.coins,
            "time_stability": self.time_stability,
            "score": self.score,
            "mechanisms": len(self.mechanisms),
        }


def create_game():
    return ClockTowerTimekeeper()


if __name__ == "__main__":
    game = create_game()
    game.wind_mechanism(0)
    game.calibrate(1)
    game.ring_bell()
    print(game.status())
