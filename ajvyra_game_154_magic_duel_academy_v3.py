"""
AJVYRA 154 — Magic Duel Academy
Genre: Fantasy / Duel
"""

from dataclasses import dataclass


@dataclass
class Mage:
    name: str
    health: int
    mana: int
    spell_power: int
    shield: int = 0


class MagicDuelAcademy:
    title = "Magic Duel Academy"
    mage_name = "Elyon Ash"

    def __init__(self):
        self.mage = Mage(
            self.mage_name,
            100,
            100,
            35,
        )

        self.enemy_health = 120
        self.enemy_mana = 80
        self.round = 1
        self.score = 0

    def cast(self, spell):
        spells = {
            "fire": (20, 45),
            "ice": (25, 30),
            "arcane": (35, 55),
        }

        if spell not in spells:
            return False

        cost, base_damage = spells[spell]

        if self.mage.mana < cost:
            return False

        self.mage.mana -= cost

        damage = base_damage + self.mage.spell_power // 3
        self.enemy_health = max(
            0,
            self.enemy_health - damage,
        )

        self.score += damage * 3

        if self.enemy_health == 0:
            self.score += 500

        return True

    def shield_spell(self):
        if self.mage.mana < 20:
            return False

        self.mage.mana -= 20
        self.mage.shield += 35
        return True

    def enemy_turn(self):
        incoming = 15

        blocked = min(
            incoming,
            self.mage.shield,
        )

        self.mage.shield -= blocked

        remaining = incoming - blocked

        self.mage.health = max(
            0,
            self.mage.health - remaining,
        )

        self.enemy_mana = max(
            0,
            self.enemy_mana - 10,
        )

    def recover_mana(self):
        self.mage.mana = min(
            100,
            self.mage.mana + 25,
        )

    def next_round(self):
        self.round += 1
        self.recover_mana()

    def status(self):
        return {
            "mage": self.mage.name,
            "health": self.mage.health,
            "mana": self.mage.mana,
            "shield": self.mage.shield,
            "enemy_health": self.enemy_health,
            "round": self.round,
            "score": self.score,
        }


def create_game():
    return MagicDuelAcademy()


if __name__ == "__main__":
    game = create_game()
    game.cast("fire")
    game.enemy_turn()
    game.next_round()
    print(game.status())
