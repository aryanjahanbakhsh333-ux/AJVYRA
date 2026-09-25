from dataclasses import dataclass


@dataclass
class Wizard:
    name: str
    mana: int = 100
    health: int = 100
    spell_power: int = 60
    defense: int = 50
    level: int = 1


class FantasyWizardDuelAcademy:
    def __init__(self):
        self.wizard = Wizard("Eryx Moon")
        self.enemy_health = 140
        self.enemy_defense = 45
        self.round = 1
        self.score = 0
        self.wins = 0
        self.gold = 100
        self.duel_finished = False

    def fire_spell(self):
        if self.wizard.mana < 15 or self.duel_finished:
            return False

        self.wizard.mana -= 15
        damage = max(
            5,
            self.wizard.spell_power - self.enemy_defense // 3
        )
        self.enemy_health -= damage
        self.score += damage
        return True

    def shield_spell(self):
        if self.wizard.mana < 20:
            return False

        self.wizard.mana -= 20
        self.wizard.defense += 8
        self.score += 15
        return True

    def lightning_spell(self):
        if self.wizard.mana < 30:
            return False

        self.wizard.mana -= 30
        damage = self.wizard.spell_power + 25
        self.enemy_health -= damage
        self.score += damage * 2
        return True

    def meditate(self):
        self.wizard.mana = min(100, self.wizard.mana + 30)
        self.score += 10

    def enemy_turn(self):
        if self.enemy_health <= 0:
            return

        damage = max(5, 25 - self.wizard.defense // 4)
        self.wizard.health -= damage

    def check_duel(self):
        if self.enemy_health <= 0:
            self.wins += 1
            self.gold += 75
            self.score += 200
            self.wizard.level += 1
            self.duel_finished = True
            return "victory"

        if self.wizard.health <= 0:
            self.duel_finished = True
            return "defeat"

        return "ongoing"

    def status(self):
        return {
            "wizard": self.wizard.name,
            "level": self.wizard.level,
            "health": self.wizard.health,
            "mana": self.wizard.mana,
            "enemy_health": self.enemy_health,
            "round": self.round,
            "wins": self.wins,
            "gold": self.gold,
            "score": self.score,
            "finished": self.duel_finished,
        }


def create_game():
    return FantasyWizardDuelAcademy()


if __name__ == "__main__":
    game = create_game()
    game.fire_spell()
    game.enemy_turn()
    game.shield_spell()
    print(game.status())
