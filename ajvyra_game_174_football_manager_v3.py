"""
AJVYRA 174 — Football Manager
Genre: Football / Management
"""

from dataclasses import dataclass


@dataclass
class Footballer:
    name: str
    attack: int
    defense: int
    stamina: int


class FootballManager:
    title = "Football Manager"
    manager_name = "Leo Hart"

    def __init__(self):
        self.money = 5000
        self.fans = 1000
        self.reputation = 40
        self.matches = 0
        self.wins = 0

        self.team = [
            Footballer("Arin", 82, 60, 85),
            Footballer("Milo", 75, 72, 90),
            Footballer("Sena", 68, 88, 80),
            Footballer("Rex", 90, 55, 78),
        ]

    def train(self, player_name, skill):
        player = self._find(player_name)

        if player is None or self.money < 150:
            return False

        if skill not in {
            "attack",
            "defense",
            "stamina",
        }:
            return False

        self.money -= 150

        setattr(
            player,
            skill,
            min(
                100,
                getattr(player, skill) + 4,
            ),
        )

        return True

    def play_match(self, opponent):
        attack = sum(
            p.attack for p in self.team
        ) / len(self.team)

        defense = sum(
            p.defense for p in self.team
        ) / len(self.team)

        stamina = sum(
            p.stamina for p in self.team
        ) / len(self.team)

        team_power = (
            attack * 0.45
            + defense * 0.30
            + stamina * 0.25
        )

        self.matches += 1

        if team_power >= opponent:
            self.wins += 1
            self.money += 600
            self.fans += 250
            self.reputation += 5
            return True

        self.fans = max(
            0,
            self.fans - 80,
        )
        return False

    def sign_player(self, player):
        if self.money < 700:
            return False

        self.money -= 700
        self.team.append(player)
        return True

    def _find(self, name):
        return next(
            (
                p for p in self.team
                if p.name.lower() == name.lower()
            ),
            None,
        )

    def status(self):
        return {
            "manager": self.manager_name,
            "money": self.money,
            "fans": self.fans,
            "reputation": self.reputation,
            "matches": self.matches,
            "wins": self.wins,
            "players": len(self.team),
        }


def create_game():
    return FootballManager()


if __name__ == "__main__":
    game = create_game()
    game.train("Arin", "attack")
    game.play_match(72)
    print(game.status())
