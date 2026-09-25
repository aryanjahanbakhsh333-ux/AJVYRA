from dataclasses import dataclass


@dataclass
class BeachPlayer:
    name: str
    serve: int = 72
    defense: int = 68
    attack: int = 75
    stamina: int = 100


class BeachVolleyballChampionship:
    def __init__(self):
        self.player = BeachPlayer("Nia Sol")
        self.partner = BeachPlayer("Kiro Vale", 68, 75, 70)
        self.opponent_score = 0
        self.team_score = 0
        self.rally = 0
        self.set_number = 1
        self.won = False

    def serve_ball(self):
        if self.player.stamina < 5:
            return False

        self.player.stamina -= 5
        self.rally += 1

        if self.player.serve >= 65:
            self.team_score += 1
            return True

        self.opponent_score += 1
        return False

    def dig(self):
        if self.partner.stamina < 4:
            return False

        self.partner.stamina -= 4
        self.rally += 1

        success = self.partner.defense >= 65

        if success:
            self.team_score += 1
        else:
            self.opponent_score += 1

        return success

    def spike(self):
        if self.player.stamina < 8:
            return False

        self.player.stamina -= 8
        self.rally += 1

        success = self.player.attack + self.rally >= 75

        if success:
            self.team_score += 2
        else:
            self.opponent_score += 1

        return success

    def recover(self):
        self.player.stamina = min(
            100,
            self.player.stamina + 20
        )
        self.partner.stamina = min(
            100,
            self.partner.stamina + 20
        )

    def check_match(self):
        if self.team_score >= 21:
            self.won = True
            return "team_victory"

        if self.opponent_score >= 21:
            return "opponent_victory"

        return "in_progress"

    def status(self):
        return {
            "player": self.player.name,
            "partner": self.partner.name,
            "team_score": self.team_score,
            "opponent_score": self.opponent_score,
            "rally": self.rally,
            "set": self.set_number,
            "player_stamina": self.player.stamina,
            "partner_stamina": self.partner.stamina,
            "won": self.won,
        }


def create_game():
    return BeachVolleyballChampionship()


def demo():
    game = create_game()

    game.serve_ball()
    game.dig()
    game.spike()
    game.recover()

    return game.status()


if __name__ == "__main__":
    print(demo())
