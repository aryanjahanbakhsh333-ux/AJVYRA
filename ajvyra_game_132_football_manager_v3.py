"""
AJVYRA 132 — Football Manager
Genre: Football Strategy / Management
"""

from dataclasses import dataclass


@dataclass
class Player:
    name: str
    attack: int
    defense: int
    stamina: int
    morale: int = 70


class FootballManager:
    title = "Football Manager"
    manager = "Rayan Cole"

    def __init__(self):
        self.money = 5000
        self.fame = 0
        self.wins = 0
        self.losses = 0

        self.players = [
            Player("Nico", 86, 50, 82),
            Player("Aris", 72, 75, 90),
            Player("Kian", 65, 88, 85),
            Player("Milo", 91, 45, 76),
            Player("Zane", 78, 70, 80),
        ]

        self.formation = "balanced"

    def set_formation(self, formation):
        formations = {
            "attack": 1.15,
            "balanced": 1.0,
            "defense": 0.88,
        }

        if formation not in formations:
            return False

        self.formation = formation
        return True

    def team_power(self):
        attack = sum(p.attack for p in self.players) / len(self.players)
        defense = sum(p.defense for p in self.players) / len(self.players)

        multiplier = {
            "attack": 1.15,
            "balanced": 1.0,
            "defense": 0.88,
        }[self.formation]

        return (
            attack * multiplier
            + defense
            + sum(p.stamina for p in self.players) / len(self.players)
        ) / 3 * 100 / 100

    def play_match(self, opponent_power):
        power = self.team_power()

        for player in self.players:
            player.stamina = max(
                20,
                player.stamina - 15,
            )

        if power >= opponent_power:
            self.wins += 1
            self.money += 700
            self.fame += 20
            for player in self.players:
                player.morale = min(
                    100,
                    player.morale + 8,
                )
            return "win"

        self.losses += 1
        self.money += 200

        for player in self.players:
            player.morale = max(
                0,
                player.morale - 10,
            )

        return "loss"

    def train(self, player_name):
        player = next(
            (
                p for p in self.players
                if p.name.lower() == player_name.lower()
            ),
            None,
        )

        if player is None or self.money < 150:
            return False

        self.money -= 150
        player.attack += 3
        player.defense += 2
        player.stamina = min(
            100,
            player.stamina + 10,
        )
        return True

    def rest_team(self):
        for player in self.players:
            player.stamina = min(
                100,
                player.stamina + 25,
            )

    def status(self):
        return {
            "manager": self.manager,
            "formation": self.formation,
            "money": self.money,
            "wins": self.wins,
            "losses": self.losses,
            "fame": self.fame,
            "team_power": round(self.team_power(), 2),
        }


def create_game():
    return FootballManager()


if __name__ == "__main__":
    game = create_game()
    game.set_formation("attack")
    game.train("Nico")
    print(game.play_match(0.72))
    print(game.status())
