from dataclasses import dataclass


@dataclass
class Wizard:
    name: str
    health: int = 100
    mana: int = 100
    shield: int = 0
    focus: int = 0


class WizardDuelTactics:
    def __init__(self):
        self.player = Wizard("Aeris Vonn")
        self.opponent = Wizard("Drax Elion", 110, 90)
        self.turn = 1
        self.score = 0

    def spell(self, spell_name: str):
        spells = {
            "ember": (15, 12),
            "frost": (12, 18),
            "storm": (22, 25),
        }

        if spell_name not in spells:
            return False

        damage, mana_cost = spells[spell_name]

        if self.player.mana < mana_cost:
            return False

        self.player.mana -= mana_cost
        damage += self.player.focus

        absorbed = min(self.opponent.shield, damage)
        self.opponent.shield -= absorbed
        damage -= absorbed

        self.opponent.health -= damage
        self.score += damage * 2
        self.player.focus = 0

        return damage

    def shield(self):
        if self.player.mana < 10:
            return False

        self.player.mana -= 10
        self.player.shield += 25
        self.score += 5
        return True

    def focus(self):
        self.player.focus += 8
        self.player.mana = min(100, self.player.mana + 5)
        self.score += 8

    def enemy_turn(self):
        damage = 10 + self.turn * 2

        absorbed = min(self.player.shield, damage)
        self.player.shield -= absorbed
        damage -= absorbed

        self.player.health -= damage

    def next_turn(self):
        self.enemy_turn()
        self.turn += 1
        self.player.mana = min(100, self.player.mana + 8)

    def duel_finished(self):
        return self.player.health <= 0 or self.opponent.health <= 0

    def status(self):
        return {
            "player": self.player,
            "opponent": self.opponent,
            "turn": self.turn,
            "score": self.score,
            "finished": self.duel_finished(),
        }


def create_game():
    return WizardDuelTactics()


def demo():
    game = create_game()

    game.focus()
    game.spell("storm")
    game.next_turn()
    game.shield()
    game.spell("frost")

    return game.status()


if __name__ == "__main__":
    print(demo())
