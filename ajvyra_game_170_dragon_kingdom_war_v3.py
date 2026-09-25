"""
AJVYRA 170 — Dragon Kingdom War
Genre: Fantasy Strategy / RPG
"""

from dataclasses import dataclass


@dataclass
class Kingdom:
    name: str
    troops: int
    defense: int
    morale: int
    controlled: bool = False


class DragonKingdomWar:
    title = "Dragon Kingdom War"
    commander = "Aeron Dray"

    def __init__(self):
        self.gold = 4000
        self.mana = 100
        self.score = 0
        self.turn = 1

        self.kingdoms = [
            Kingdom("Emberfall", 500, 70, 80),
            Kingdom("Frosthelm", 420, 85, 65),
            Kingdom("Stormreach", 600, 60, 75),
            Kingdom("Mooncrest", 350, 90, 90),
        ]

    def reinforce(self, kingdom_name):
        kingdom = self._find(kingdom_name)

        if kingdom is None or self.gold < 300:
            return False

        self.gold -= 300
        kingdom.troops += 100
        kingdom.morale = min(
            100,
            kingdom.morale + 8,
        )
        self.score += 100
        return True

    def inspire(self, kingdom_name):
        kingdom = self._find(kingdom_name)

        if kingdom is None or self.mana < 20:
            return False

        self.mana -= 20
        kingdom.morale = min(
            100,
            kingdom.morale + 15,
        )
        kingdom.defense += 5
        self.score += 150
        return True

    def campaign(self, kingdom_name, enemy_strength):
        kingdom = self._find(kingdom_name)

        if kingdom is None:
            return False

        combat_power = (
            kingdom.troops
            * (kingdom.morale / 100)
            + kingdom.defense * 4
        )

        if combat_power >= enemy_strength:
            kingdom.controlled = True
            self.gold += 600
            self.score += enemy_strength
            return True

        kingdom.troops = max(
            0,
            kingdom.troops - enemy_strength // 5,
        )
        kingdom.morale = max(
            0,
            kingdom.morale - 15,
        )
        return False

    def next_turn(self):
        self.turn += 1
        self.gold += 250
        self.mana = min(
            100,
            self.mana + 15,
        )

    def _find(self, name):
        return next(
            (
                k for k in self.kingdoms
                if k.name == name
            ),
            None,
        )

    def status(self):
        return {
            "commander": self.commander,
            "turn": self.turn,
            "gold": self.gold,
            "mana": self.mana,
            "score": self.score,
            "controlled_kingdoms": [
                k.name
                for k in self.kingdoms
                if k.controlled
            ],
        }


def create_game():
    return DragonKingdomWar()


if __name__ == "__main__":
    game = create_game()
    game.reinforce("Emberfall")
    game.inspire("Emberfall")
    game.campaign("Emberfall", 400)
    print(game.status())
