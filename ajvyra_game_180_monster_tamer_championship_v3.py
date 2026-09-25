"""
AJVYRA 180 — Monster Tamer Championship
Genre: Creature Battle / Strategy / RPG
"""

from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    element: str
    power: int
    defense: int
    speed: int
    health: int = 100


class MonsterTamerChampionship:
    title = "Monster Tamer Championship"
    tamer = "Riko Vale"

    def __init__(self):
        self.gold = 1000
        self.trophies = 0
        self.score = 0
        self.round = 1

        self.team = [
            Monster(
                "Flareonix",
                "fire",
                82,
                65,
                75,
            ),
            Monster(
                "Aquaryn",
                "water",
                70,
                82,
                68,
            ),
            Monster(
                "Voltaris",
                "electric",
                78,
                62,
                90,
            ),
        ]

    def battle(self, monster_index, enemy_power):
        if not 0 <= monster_index < len(
            self.team
        ):
            return False

        monster = self.team[monster_index]

        if monster.health <= 0:
            return False

        attack_power = (
            monster.power
            + monster.speed // 2
            + monster.defense // 4
        )

        if attack_power >= enemy_power:
            reward = enemy_power * 4
            self.gold += reward
            self.score += reward
            return True

        monster.health = max(
            0,
            monster.health - 20,
        )
        return False

    def train(self, monster_index):
        if not 0 <= monster_index < len(
            self.team
        ):
            return False

        monster = self.team[monster_index]

        if self.gold < 150:
            return False

        self.gold -= 150

        monster.power = min(
            100,
            monster.power + 4,
        )

        monster.speed = min(
            100,
            monster.speed + 3,
        )

        return True

    def heal_team(self):
        if self.gold < 200:
            return False

        self.gold -= 200

        for monster in self.team:
            monster.health = min(
                100,
                monster.health + 30,
            )

        return True

    def win_championship(self):
        if self.round < 5:
            return False

        self.trophies += 1
        self.score += 2000
        return True

    def status(self):
        return {
            "tamer": self.tamer,
            "gold": self.gold,
            "round": self.round,
            "trophies": self.trophies,
            "score": self.score,
            "team": {
                m.name: {
                    "element": m.element,
                    "power": m.power,
                    "health": m.health,
                }
                for m in self.team
            },
        }


def create_game():
    return MonsterTamerChampionship()


if __name__ == "__main__":
    game = create_game()
    game.train(0)
    game.battle(0, 70)
    game.heal_team()
    print(game.status())
