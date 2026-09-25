"""
AJVYRA 161 — Samurai Ronin
Genre: Action / Duel / Story
"""

from dataclasses import dataclass


@dataclass
class Ronin:
    name: str
    health: int = 100
    stamina: int = 100
    attack: int = 72
    defense: int = 68
    focus: int = 60


class SamuraiRonin:
    title = "Samurai Ronin"
    hero_name = "Kaizen Rho"

    def __init__(self):
        self.hero = Ronin(self.hero_name)
        self.chapter = 1
        self.honor = 0
        self.coins = 300
        self.score = 0

        self.enemies = [
            ("Ash Guard", 55),
            ("Red Wolf", 70),
            ("Iron Monk", 85),
            ("Silent Lord", 105),
        ]

    def slash(self, enemy):
        if self.hero.stamina < 15:
            return False

        self.hero.stamina -= 15

        damage = (
            self.hero.attack
            + self.hero.focus // 4
        )

        return damage >= enemy

    def focused_strike(self, enemy):
        if self.hero.stamina < 30 or self.hero.focus < 20:
            return False

        self.hero.stamina -= 30
        self.hero.focus -= 20

        damage = (
            self.hero.attack * 2
            + self.hero.focus
        )

        if damage >= enemy:
            self.score += 250
            self.honor += 10
            return True

        self.hero.health = max(
            0,
            self.hero.health - 15,
        )
        return False

    def meditate(self):
        self.hero.stamina = min(
            100,
            self.hero.stamina + 30,
        )
        self.hero.focus = min(
            100,
            self.hero.focus + 20,
        )

    def defend(self):
        self.hero.health = min(
            100,
            self.hero.health + 5,
        )
        self.hero.stamina = min(
            100,
            self.hero.stamina + 10,
        )

    def complete_chapter(self):
        if self.chapter > len(self.enemies):
            return False

        enemy_name, enemy_power = self.enemies[
            self.chapter - 1
        ]

        if self.slash(enemy_power):
            self.chapter += 1
            self.honor += 20
            self.coins += 150
            self.score += 400
            return enemy_name

        return False

    def status(self):
        return {
            "hero": self.hero.name,
            "chapter": self.chapter,
            "health": self.hero.health,
            "stamina": self.hero.stamina,
            "focus": self.hero.focus,
            "honor": self.honor,
            "coins": self.coins,
            "score": self.score,
        }


def create_game():
    return SamuraiRonin()


if __name__ == "__main__":
    game = create_game()
    game.meditate()
    game.complete_chapter()
    print(game.status())
