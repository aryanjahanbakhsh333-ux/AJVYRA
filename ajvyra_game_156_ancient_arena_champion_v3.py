"""
AJVYRA 156 — Ancient Arena Champion
Genre: Arena / Action
"""

from dataclasses import dataclass


@dataclass
class Champion:
    name: str
    attack: int
    defense: int
    agility: int
    health: int = 100


class AncientArenaChampion:
    title = "Ancient Arena Champion"
    champion_name = "Darian Sol"

    def __init__(self):
        self.champion = Champion(
            self.champion_name,
            80,
            75,
            82,
        )

        self.round = 1
        self.gold = 500
        self.honor = 0
        self.score = 0

    def heavy_attack(self, enemy_defense):
        damage = (
            self.champion.attack
            + self.champion.agility // 2
            - enemy_defense // 3
        )

        damage = max(5, damage)

        self.score += damage
        return damage

    def quick_attack(self, enemy_defense):
        damage = (
            self.champion.agility
            + self.champion.attack // 3
            - enemy_defense // 4
        )

        damage = max(5, damage)

        self.score += damage
        return damage

    def block(self):
        self.champion.health = min(
            100,
            self.champion.health + 5,
        )

    def win_round(self):
        reward = 150 + self.round * 50
        self.gold += reward
        self.honor += 10
        self.round += 1
        self.champion.health = 100

    def status(self):
        return {
            "champion": self.champion.name,
            "round": self.round,
            "gold": self.gold,
            "honor": self.honor,
            "score": self.score,
            "health": self.champion.health,
        }


def create_game():
    return AncientArenaChampion()


if __name__ == "__main__":
    game = create_game()
    game.heavy_attack(60)
    game.quick_attack(55)
    game.win_round()
    print(game.status())
