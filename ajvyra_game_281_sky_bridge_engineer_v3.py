from dataclasses import dataclass


@dataclass
class SkyBridge:
    name: str
    length: int
    integrity: int = 100
    traffic: int = 0


class SkyBridgeEngineer:
    def __init__(self):
        self.engineer = "Arin Cloud"
        self.bridge = SkyBridge("Aether Bridge", 1000)
        self.materials = 300
        self.energy = 100
        self.credits = 500
        self.score = 0
        self.day = 1
        self.completed = False

    def build_segment(self, length: int = 100):
        cost = max(10, length // 5)

        if self.materials < cost or self.energy < 8:
            return False

        self.materials -= cost
        self.energy -= 8
        self.bridge.length += length
        self.bridge.integrity = min(
            100,
            self.bridge.integrity + 4
        )
        self.score += length // 2
        return True

    def reinforce(self):
        if self.materials < 40:
            return False

        self.materials -= 40
        self.bridge.integrity = min(
            100,
            self.bridge.integrity + 20
        )
        self.score += 50
        return True

    def open_traffic(self, vehicles: int):
        if vehicles <= 0:
            return False

        if self.bridge.integrity < 50:
            return False

        self.bridge.traffic += vehicles
        self.credits += vehicles * 8
        self.score += vehicles * 5
        return True

    def inspect(self):
        self.energy = max(0, self.energy - 5)

        if self.bridge.traffic > 20:
            self.bridge.integrity -= 5

        self.score += 25
        return self.bridge.integrity

    def recharge(self):
        self.energy = min(100, self.energy + 35)

    def complete_bridge(self):
        if self.bridge.length >= 2000 and self.bridge.integrity >= 70:
            self.completed = True
            self.score += 500
            self.credits += 700
            return True

        return False

    def next_day(self):
        self.day += 1
        self.bridge.integrity = max(
            0,
            self.bridge.integrity - 2
        )
        self.recharge()

    def status(self):
        return {
            "engineer": self.engineer,
            "bridge": self.bridge.name,
            "length": self.bridge.length,
            "integrity": self.bridge.integrity,
            "traffic": self.bridge.traffic,
            "materials": self.materials,
            "energy": self.energy,
            "credits": self.credits,
            "day": self.day,
            "score": self.score,
            "completed": self.completed,
        }


def create_game():
    return SkyBridgeEngineer()


if __name__ == "__main__":
    game = create_game()
    game.build_segment(300)
    game.reinforce()
    game.open_traffic(8)
    print(game.status())
