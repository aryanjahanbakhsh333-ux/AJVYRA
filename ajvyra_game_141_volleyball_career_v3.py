"""
AJVYRA 141 — Volleyball Career
Genre: Sports / Career
"""

from dataclasses import dataclass


@dataclass
class Athlete:
    name: str
    serve: int
    spike: int
    defense: int
    stamina: int = 100


class VolleyballCareer:
    title = "Volleyball Career"
    coach = "Mara Venn"

    def __init__(self):
        self.week = 1
        self.money = 1200
        self.fans = 100
        self.wins = 0
        self.losses = 0

        self.player = Athlete(
            "Riven Sol",
            serve=72,
            spike=78,
            defense=68,
        )

    def train(self, skill):
        if self.money < 100:
            return False

        values = {
            "serve": "serve",
            "spike": "spike",
            "defense": "defense",
        }

        if skill not in values:
            return False

        self.money -= 100
        attribute = values[skill]

        setattr(
            self.player,
            attribute,
            getattr(self.player, attribute) + 4,
        )

        self.player.stamina = min(
            100,
            self.player.stamina + 5,
        )
        return True

    def play_match(self, opponent):
        power = (
            self.player.serve * 0.3
            + self.player.spike * 0.4
            + self.player.defense * 0.3
        )

        power *= self.player.stamina / 100

        self.player.stamina = max(
            20,
            self.player.stamina - 20,
        )

        if power >= opponent:
            self.wins += 1
            self.money += 350
            self.fans += 75
            return True

        self.losses += 1
        self.fans = max(0, self.fans - 20)
        return False

    def rest(self):
        self.player.stamina = min(
            100,
            self.player.stamina + 35,
        )

    def next_week(self):
        self.week += 1
        self.rest()

    def status(self):
        return {
            "coach": self.coach,
            "week": self.week,
            "money": self.money,
            "fans": self.fans,
            "wins": self.wins,
            "losses": self.losses,
            "player": self.player.name,
            "serve": self.player.serve,
            "spike": self.player.spike,
            "defense": self.player.defense,
            "stamina": self.player.stamina,
        }


def create_game():
    return VolleyballCareer()


if __name__ == "__main__":
    game = create_game()
    game.train("spike")
    game.play_match(65)
    print(game.status())
