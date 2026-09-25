from dataclasses import dataclass


@dataclass
class HockeyPlayer:
    name: str
    speed: int = 65
    control: int = 70
    defense: int = 55
    stamina: int = 100


class UnderwaterHockey:
    def __init__(self):
        self.player = HockeyPlayer("Nero Wave")
        self.team_score = 0
        self.enemy_score = 0
        self.oxygen = 100
        self.puck_position = 0
        self.round = 1
        self.score = 0
        self.match_finished = False

    def swim_forward(self):
        if self.player.stamina < 8 or self.oxygen < 8:
            return False

        self.player.stamina -= 8
        self.oxygen -= 8
        self.puck_position += self.player.speed
        self.score += 20
        return True

    def control_puck(self):
        if self.player.stamina < 10:
            return False

        self.player.stamina -= 10

        if self.player.control >= 65:
            self.puck_position += 80
            self.score += 35
            return True

        self.puck_position -= 30
        return False

    def strike(self):
        if self.player.stamina < 15:
            return False

        self.player.stamina -= 15

        if self.puck_position >= 250:
            self.team_score += 1
            self.puck_position = 0
            self.score += 150
            return True

        self.score += 10
        return False

    def recover_oxygen(self):
        self.oxygen = min(100, self.oxygen + 30)
        self.player.stamina = min(
            100,
            self.player.stamina + 20
        )

    def enemy_attack(self):
        if self.puck_position <= 0:
            return

        if self.player.defense < 60:
            self.puck_position = max(
                0,
                self.puck_position - 60
            )

    def check_match(self):
        if self.team_score >= 5:
            self.score += 300
            self.match_finished = True
            return "victory"

        if self.enemy_score >= 5:
            self.match_finished = True
            return "defeat"

        return "ongoing"

    def status(self):
        return {
            "player": self.player.name,
            "team_score": self.team_score,
            "enemy_score": self.enemy_score,
            "oxygen": self.oxygen,
            "stamina": self.player.stamina,
            "puck_position": self.puck_position,
            "score": self.score,
            "finished": self.match_finished,
        }


def create_game():
    return UnderwaterHockey()


if __name__ == "__main__":
    game = create_game()
    game.swim_forward()
    game.control_puck()
    game.strike()
    print(game.status())
