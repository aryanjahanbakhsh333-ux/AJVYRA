from dataclasses import dataclass


@dataclass
class GravityExplorer:
    name: str
    energy: int = 100
    suit_integrity: int = 100
    position: int = 0
    keys: int = 0


class GravityLabEscape:
    def __init__(self):
        self.player = GravityExplorer("Eli Varen")
        self.gravity = 1.0
        self.score = 0
        self.turn = 1
        self.exit_unlocked = False

    def change_gravity(self, value: float):
        if value not in (0.5, 1.0, 1.5, 2.0):
            return False

        self.gravity = value
        self.player.energy -= 4
        self.score += 12
        return True

    def move(self, direction: int):
        if direction not in (-1, 1):
            return False

        cost = int(5 * self.gravity)

        if self.player.energy < cost:
            return False

        self.player.energy -= cost
        self.player.position += direction
        self.score += 10
        self.turn += 1

        if self.player.position == 3:
            self.player.keys += 1
            self.score += 50

        return True

    def solve_gravity_puzzle(self):
        if self.player.keys <= 0:
            return False

        if self.gravity != 0.5:
            return False

        self.player.keys -= 1
        self.exit_unlocked = True
        self.score += 150
        return True

    def escape(self):
        if not self.exit_unlocked:
            return False

        self.score += 300
        return True

    def rest(self):
        self.player.energy = min(100, self.player.energy + 20)
        self.player.suit_integrity = min(
            100,
            self.player.suit_integrity + 10
        )

    def status(self):
        return {
            "explorer": self.player.name,
            "energy": self.player.energy,
            "suit_integrity": self.player.suit_integrity,
            "position": self.player.position,
            "gravity": self.gravity,
            "keys": self.player.keys,
            "turn": self.turn,
            "score": self.score,
            "exit_unlocked": self.exit_unlocked,
        }


def create_game():
    return GravityLabEscape()


def demo():
    game = create_game()
    game.change_gravity(0.5)
    game.move(1)
    game.move(1)
    game.move(1)
    game.solve_gravity_puzzle()
    game.escape()
    return game.status()


if __name__ == "__main__":
    print(demo())
