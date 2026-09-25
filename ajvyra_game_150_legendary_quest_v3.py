"""
AJVYRA 150 — Legendary Quest
Genre: Story RPG / Adventure
"""

from dataclasses import dataclass


@dataclass
class Hero:
    name: str
    level: int
    health: int
    mana: int
    power: int


class LegendaryQuest:
    title = "Legendary Quest"
    hero_name = "Aeron Vale"

    def __init__(self):
        self.hero = Hero(
            self.hero_name,
            level=1,
            health=100,
            mana=80,
            power=25,
        )

        self.gold = 300
        self.experience = 0
        self.chapter = 1
        self.score = 0

        self.quests = [
            "The Silent Forest",
            "The Broken Crown",
            "The Glass Mountain",
            "The Last Gate",
        ]

        self.completed = []

    def fight(self, enemy_power):
        if self.hero.mana < 10:
            return False

        attack = (
            self.hero.power
            + self.hero.level * 8
            + self.hero.mana // 10
        )

        self.hero.mana -= 10

        if attack >= enemy_power:
            self.experience += enemy_power
            self.gold += enemy_power * 2
            self.score += enemy_power * 5
            self._level_up()
            return True

        self.hero.health = max(
            0,
            self.hero.health - enemy_power // 4,
        )
        return False

    def complete_quest(self):
        if self.chapter > len(self.quests):
            return False

        quest = self.quests[self.chapter - 1]

        if quest in self.completed:
            return False

        self.completed.append(quest)
        self.chapter += 1
        self.gold += 250
        self.experience += 100
        self.score += 300

        self._level_up()
        return True

    def heal(self):
        if self.gold < 75:
            return False

        self.gold -= 75
        self.hero.health = min(
            100,
            self.hero.health + 40,
        )
        self.hero.mana = min(
            80,
            self.hero.mana + 30,
        )
        return True

    def _level_up(self):
        required = self.hero.level * 120

        while self.experience >= required:
            self.experience -= required
            self.hero.level += 1
            self.hero.power += 7
            self.hero.health = 100
            self.hero.mana = 80
            required = self.hero.level * 120

    def finished(self):
        return len(self.completed) == len(
            self.quests
        )

    def status(self):
        return {
            "hero": self.hero.name,
            "level": self.hero.level,
            "health": self.hero.health,
            "mana": self.hero.mana,
            "power": self.hero.power,
            "gold": self.gold,
            "chapter": self.chapter,
            "experience": self.experience,
            "score": self.score,
            "completed_quests": list(self.completed),
            "finished": self.finished(),
        }


def create_game():
    return LegendaryQuest()


if __name__ == "__main__":
    game = create_game()
    game.fight(30)
    game.complete_quest()
    print(game.status())
