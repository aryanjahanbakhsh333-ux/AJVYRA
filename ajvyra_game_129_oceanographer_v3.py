"""
AJVYRA 129 — Oceanographer
Genre: Scientific Exploration
"""

from dataclasses import dataclass


@dataclass
class OceanSample:
    depth: int
    temperature: float
    salinity: float
    oxygen: float


class Oceanographer:
    title = "Oceanographer"
    scientist = "Mira Tide"

    def __init__(self):
        self.depth = 0
        self.battery = 100
        self.pressure = 1.0
        self.samples: list[OceanSample] = []
        self.score = 0

    def descend(self, meters):
        if meters <= 0:
            return False

        energy = meters * 0.2

        if energy > self.battery:
            return False

        self.depth += meters
        self.battery -= energy
        self.pressure = 1 + self.depth / 10
        return True

    def collect_sample(self):
        if self.depth < 100:
            return False

        sample = OceanSample(
            depth=self.depth,
            temperature=max(
                2,
                25 - self.depth * 0.02,
            ),
            salinity=34 + self.depth * 0.005,
            oxygen=max(
                2,
                8 - self.depth * 0.01,
            ),
        )

        self.samples.append(sample)
        self.score += 100
        self.battery -= 5
        return True

    def analyze(self, index):
        if not 0 <= index < len(self.samples):
            return None

        sample = self.samples[index]

        return {
            "depth": sample.depth,
            "temperature": round(sample.temperature, 2),
            "salinity": round(sample.salinity, 2),
            "oxygen": round(sample.oxygen, 2),
            "deep_water": sample.depth >= 500,
        }

    def surface(self):
        self.depth = 0
        self.pressure = 1
        self.battery = min(100, self.battery + 20)

    def status(self):
        return {
            "scientist": self.scientist,
            "depth": self.depth,
            "pressure": round(self.pressure, 2),
            "battery": round(self.battery, 1),
            "samples": len(self.samples),
            "score": self.score,
        }


def create_game():
    return Oceanographer()


if __name__ == "__main__":
    game = create_game()
    game.descend(500)
    game.collect_sample()
    print(game.analyze(0))
    print(game.status())
