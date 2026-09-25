"""
AJVYRA 144 — Kingdom Diplomat
Genre: Strategy / Diplomacy
"""

from dataclasses import dataclass


@dataclass
class Kingdom:
    name: str
    trust: int
    trade: int
    military: int


class KingdomDiplomat:
    title = "Kingdom Diplomat"
    diplomat = "Elian Crest"

    def __init__(self):
        self.gold = 3000
        self.influence = 20
        self.turn = 1

        self.kingdoms = {
            "Valora": Kingdom(
                "Valora", 55, 70, 60
            ),
            "Draven": Kingdom(
                "Draven", 40, 85, 80
            ),
            "Elyria": Kingdom(
                "Elyria", 75, 55, 45
            ),
            "Noren": Kingdom(
                "Noren", 60, 90, 50
            ),
        }

    def negotiate(self, kingdom_name, proposal):
        kingdom = self.kingdoms.get(kingdom_name)

        if kingdom is None:
            return False

        effects = {
            "trade": (8, 15),
            "peace": (15, 5),
            "alliance": (20, -5),
        }

        if proposal not in effects:
            return False

        trust_gain, trade_gain = effects[proposal]

        kingdom.trust = min(
            100,
            kingdom.trust + trust_gain,
        )

        kingdom.trade = min(
            100,
            kingdom.trade + trade_gain,
        )

        self.influence += 5
        self.gold += kingdom.trade * 2
        return True

    def invest(self, kingdom_name):
        if self.gold < 500:
            return False

        kingdom = self.kingdoms.get(kingdom_name)

        if kingdom is None:
            return False

        self.gold -= 500
        kingdom.trade = min(
            100,
            kingdom.trade + 10,
        )
        kingdom.trust = min(
            100,
            kingdom.trust + 5,
        )
        return True

    def alliance_count(self):
        return sum(
            k.trust >= 85
            for k in self.kingdoms.values()
        )

    def next_turn(self):
        self.turn += 1
        self.gold += self.influence * 5

    def status(self):
        return {
            "diplomat": self.diplomat,
            "turn": self.turn,
            "gold": self.gold,
            "influence": self.influence,
            "alliances": self.alliance_count(),
            "kingdoms": {
                name: {
                    "trust": kingdom.trust,
                    "trade": kingdom.trade,
                    "military": kingdom.military,
                }
                for name, kingdom in self.kingdoms.items()
            },
        }


def create_game():
    return KingdomDiplomat()


if __name__ == "__main__":
    game = create_game()
    game.negotiate("Valora", "alliance")
    game.invest("Valora")
    print(game.status())
