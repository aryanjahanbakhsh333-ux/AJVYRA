from dataclasses import dataclass


@dataclass
class Skater:
    name: str
    speed: int = 70
    balance: int = 70
    style: int = 60
    stamina: int = 100


class UrbanSkateRival:
    def __init__(self):
        self.skater = Skater("Vex Rowan")
        self.distance = 0
        self.score = 0
        self.combo = 0
        self.rival_score = 0
        self.round = 1
        self.won = False

    def sprint(self):
        if self.skater.stamina < 10:
            return False

        self.skater.stamina -= 10
        self.distance += self.skater.speed
        self.score += 20
        return True

    def grind(self):
        if self.skater.stamina < 12:
            return False

        self.skater.stamina -= 12

        if self.skater.balance >= 65:
            self.combo += 1
            self.score += 50 * self.combo
            return True

        self.combo = 0
        return False

    def trick(self):
        if self.skater.stamina < 15:
            return False

        self.skater.stamina -= 15
        self.combo += 1
        self.score += self.skater.style * self.combo
        return True

    def recover(self):
        self.skater.stamina = min(
            100,
            self.skater.stamina + 30
        )

    def rival_move(self):
        self.rival_score += 40 + self.round * 10

    def finish_round(self):
        self.rival_move()

        if self.score > self.rival_score:
            self.won = True
            self.score += 250
            return True

        self.round += 1
        return False

    def status(self):
        return {
            "skater": self.skater.name,
            "distance": self.distance,
            "score": self.score,
            "rival_score": self.rival_score,
            "combo": self.combo,
            "stamina": self.skater.stamina,
            "round": self.round,
            "won": self.won,
        }


def create_game():
    return UrbanSkateRival()


if __name__ == "__main__":
    game = create_game()
    game.sprint()
    game.grind()
    game.trick()
    game.finish_round()
    print(game.status())
