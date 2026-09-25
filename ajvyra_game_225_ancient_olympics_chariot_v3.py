from dataclasses import dataclass


@dataclass
class Charioteer:
    name: str
    speed: int = 60
    control: int = 60
    stamina: int = 100
    fame: int = 0


class AncientOlympicsChariot:
    def __init__(self):
        self.racer = Charioteer("Dorian Vale")
        self.lap = 1
        self.position = 4
        self.distance = 0
        self.score = 0
        self.coins = 100
        self.damage = 0
        self.finished = False

    def accelerate(self):
        if self.racer.stamina < 12:
            return False

        self.racer.stamina -= 12
        self.distance += self.racer.speed // 8
        self.score += 10
        return True

    def drift_turn(self):
        if self.racer.stamina < 10:
            return False

        self.racer.stamina -= 10

        success = self.racer.control >= 50
        if success:
            self.distance += 10
            self.position = max(1, self.position - 1)
            self.score += 25
        else:
            self.damage += 10

        return success

    def use_whip(self):
        if self.racer.stamina < 18:
            return False

        self.racer.stamina -= 18
        self.distance += 15
        self.score += 20
        return True

    def repair_chariot(self):
        if self.coins < 25:
            return False

        self.coins -= 25
        self.damage = max(0, self.damage - 20)
        return True

    def next_lap(self):
        if self.distance < 50:
            return False

        self.distance = 0
        self.lap += 1
        self.racer.stamina = min(100, self.racer.stamina + 10)

        if self.lap > 5:
            self.finished = True
            if self.position == 1:
                self.racer.fame += 100
                self.score += 200

        return True

    def status(self):
        return {
            "racer": self.racer.name,
            "lap": self.lap,
            "position": self.position,
            "distance": self.distance,
            "stamina": self.racer.stamina,
            "damage": self.damage,
            "score": self.score,
            "fame": self.racer.fame,
            "finished": self.finished,
        }


def create_game():
    return AncientOlympicsChariot()


if __name__ == "__main__":
    game = create_game()
    game.accelerate()
    game.drift_turn()
    print(game.status())
