from dataclasses import dataclass


@dataclass
class RadioSignal:
    name: str
    frequency: int
    clarity: int
    importance: int
    decoded: bool = False


class SpaceRadioStation:
    def __init__(self):
        self.operator = "Nova Ray"
        self.energy = 100
        self.signal_strength = 60
        self.credits = 200
        self.score = 0
        self.reputation = 15
        self.messages = 0

        self.signals = [
            RadioSignal("Lunar Beacon", 104, 70, 30),
            RadioSignal("Orion Distress", 221, 55, 60),
            RadioSignal("Unknown Pulse", 309, 40, 90),
            RadioSignal("Deep Space Archive", 417, 30, 120),
        ]

    def scan_frequency(self, index: int):
        if not 0 <= index < len(self.signals):
            return False

        if self.energy < 10:
            return False

        self.energy -= 10
        signal = self.signals[index]
        signal.clarity += self.signal_strength // 10
        self.score += 20
        return True

    def decode_signal(self, index: int):
        if not 0 <= index < len(self.signals):
            return False

        signal = self.signals[index]

        if signal.decoded or self.energy < 15:
            return False

        self.energy -= 15

        if signal.clarity >= 60:
            signal.decoded = True
            self.messages += 1
            self.credits += signal.importance
            self.reputation += 4
            self.score += signal.importance
            return True

        return False

    def amplify_station(self):
        if self.credits < 80:
            return False

        self.credits -= 80
        self.signal_strength += 15
        self.score += 35
        return True

    def recharge(self):
        self.energy = min(100, self.energy + 40)

    def archive_messages(self):
        if self.messages < 2:
            return False

        self.score += self.messages * 40
        return True

    def status(self):
        return {
            "operator": self.operator,
            "energy": self.energy,
            "signal_strength": self.signal_strength,
            "credits": self.credits,
            "reputation": self.reputation,
            "messages": self.messages,
            "score": self.score,
        }


def create_game():
    return SpaceRadioStation()


if __name__ == "__main__":
    game = create_game()
    game.scan_frequency(0)
    game.decode_signal(0)
    game.amplify_station()
    print(game.status())
