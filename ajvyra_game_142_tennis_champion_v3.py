"""
AJVYRA 142 — Tennis Champion
Genre: Sports / Tournament
"""

from dataclasses import dataclass


@dataclass
class TennisPlayer:
    name: str
    serve: int
    return_game: int
    movement: int
    confidence: int = 70


class TennisChampion:
    title = "Tennis Champion"
    player_name = "Kaia Ren"

    def __init__(self):
        self.round = 1
        self.coins = 800
        self.trophies = 0
        self.score = 0

        self.player = TennisPlayer(
            self.player_name,
            84,
            76,
            81,
        )

    def practice(self, style):
        bonuses = {
            "serve": ("serve", 4),
            "return": ("return_game", 4),
            "movement": ("movement", 4),
            "mental": ("confidence", 6),
        }

        if style not in bonuses or self.coins < 75:
            return False

        attribute, bonus = bonuses[style]
        self.coins -= 75

        setattr(
            self.player,
            attribute,
            getattr(self.player, attribute) + bonus,
        )
        return True

    def match(self, opponent):
        attack = (
            self.player.serve * 0.35
            + self.player.return_game * 0.35
            + self.player.movement * 0.30
        )

        attack += self.player.confidence * 0.2

        if attack >= opponent:
            self.score += 250 * self.round
            self.coins += 200
            self.player.confidence = min(
                100,
                self.player.confidence + 5,
            )

            if self.round >= 5:
                self.trophies += 1

            self.round += 1
            return True

        self.player.confidence = max(
            20,
            self.player.confidence - 8,
        )
        return False

    def status(self):
        return {
            "player": self.player.name,
            "round": self.round,
            "coins": self.coins,
            "trophies": self.trophies,
            "score": self.score,
            "confidence": self.player.confidence,
        }


def create_game():
    return TennisChampion()


if __name__ == "__main__":
    game = create_game()
    game.practice("serve")
    game.match(78)
    print(game.status())
