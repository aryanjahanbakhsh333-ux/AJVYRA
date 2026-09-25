from dataclasses import dataclass


@dataclass
class Dancer:
    name: str
    rhythm: int = 65
    balance: int = 60
    style: int = 55
    stamina: int = 100


class NeonHologramDancer:
    def __init__(self):
        self.dancer = Dancer("Veya Pulse")
        self.stage = "Neon Dome"
        self.score = 0
        self.combo = 0
        self.fans = 0
        self.level = 1
        self.performance_complete = False

    def rhythm_step(self):
        if self.dancer.stamina < 8:
            return False

        self.dancer.stamina -= 8

        if self.dancer.rhythm >= 60:
            self.combo += 1
            self.score += 25 * self.combo
            return True

        self.combo = 0
        return False

    def hologram_spin(self):
        if self.dancer.stamina < 12:
            return False

        self.dancer.stamina -= 12

        if self.dancer.balance >= 60:
            self.combo += 1
            self.score += 35 * self.combo
            return True

        self.combo = 0
        return False

    def style_burst(self):
        if self.dancer.stamina < 20:
            return False

        self.dancer.stamina -= 20
        self.combo += 2
        self.score += 70 + self.dancer.style
        return True

    def recover(self):
        self.dancer.stamina = min(
            100,
            self.dancer.stamina + 30
        )
        self.combo = max(0, self.combo - 1)

    def finish_performance(self):
        if self.score < 300:
            return False

        self.fans += self.score // 10
        self.level += 1
        self.score += 200
        self.performance_complete = True
        return True

    def status(self):
        return {
            "dancer": self.dancer.name,
            "stage": self.stage,
            "stamina": self.dancer.stamina,
            "combo": self.combo,
            "fans": self.fans,
            "level": self.level,
            "score": self.score,
            "complete": self.performance_complete,
        }


def create_game():
    return NeonHologramDancer()


if __name__ == "__main__":
    game = create_game()
    game.rhythm_step()
    game.hologram_spin()
    game.style_burst()
    game.finish_performance()
    print(game.status())
