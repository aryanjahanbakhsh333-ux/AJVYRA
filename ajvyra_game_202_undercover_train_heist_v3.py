from dataclasses import dataclass
from typing import List


@dataclass
class Agent:
    name: str
    disguise: int = 80
    stealth: int = 75
    nerve: int = 70


@dataclass
class SecurityNode:
    name: str
    difficulty: int
    disabled: bool = False


class UndercoverTrainHeist:
    def __init__(self):
        self.agent = Agent("Rex Calder")
        self.carriage = 1
        self.time_left = 25
        self.alert = 0
        self.intel = 0
        self.score = 0
        self.escaped = False

        self.security: List[SecurityNode] = [
            SecurityNode("Front Scanner", 55),
            SecurityNode("Vault Sensor", 70),
            SecurityNode("Rear Lock", 60),
        ]

    def move(self, carriage: int):
        if not 1 <= carriage <= 8:
            return False

        distance = abs(carriage - self.carriage)
        self.time_left -= distance
        self.carriage = carriage

        return self.time_left > 0

    def gather_intel(self):
        if self.time_left <= 0:
            return False

        self.time_left -= 2
        self.intel += 20
        self.score += 25
        return True

    def disable_security(self, index: int):
        if not 0 <= index < len(self.security):
            return False

        node = self.security[index]

        if node.disabled:
            return True

        if self.agent.stealth + self.intel < node.difficulty:
            self.alert += 15
            self.agent.nerve -= 5
            return False

        node.disabled = True
        self.intel = max(0, self.intel - 10)
        self.score += 60
        return True

    def access_vault(self):
        if not all(node.disabled for node in self.security):
            return False

        self.time_left -= 3
        self.score += 150
        return True

    def escape_train(self):
        if self.score < 300 or self.alert >= 80:
            return False

        self.escaped = True
        self.score += 250
        return True

    def status(self):
        return {
            "agent": self.agent.name,
            "carriage": self.carriage,
            "time_left": self.time_left,
            "alert": self.alert,
            "intel": self.intel,
            "score": self.score,
            "security_disabled": sum(
                node.disabled for node in self.security
            ),
            "escaped": self.escaped,
        }


def create_game():
    return UndercoverTrainHeist()


def demo():
    game = create_game()
    game.gather_intel()

    for i in range(3):
        game.disable_security(i)

    game.access_vault()
    game.escape_train()

    return game.status()


if __name__ == "__main__":
    print(demo())
