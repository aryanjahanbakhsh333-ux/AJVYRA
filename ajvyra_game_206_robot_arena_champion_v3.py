from dataclasses import dataclass


@dataclass
class ArenaRobot:
    name: str
    armor: int = 100
    energy: int = 100
    attack: int = 30
    defense: int = 25
    victories: int = 0


class RobotArenaChampion:
    def __init__(self):
        self.pilot = "Zera Quinn"
        self.robot = ArenaRobot("Titan-7")
        self.enemy_armor = 120
        self.enemy_attack = 22
        self.round = 1
        self.score = 0

    def plasma_strike(self):
        if self.robot.energy < 15:
            return False

        self.robot.energy -= 15
        damage = self.robot.attack + 15
        self.enemy_armor -= damage
        self.score += damage * 2
        return True

    def heavy_guard(self):
        if self.robot.energy < 10:
            return False

        self.robot.energy -= 10
        self.robot.defense += 8
        self.score += 10
        return True

    def shockwave(self):
        if self.robot.energy < 25:
            return False

        self.robot.energy -= 25
        damage = self.robot.attack + self.robot.defense
        self.enemy_armor -= damage
        self.score += damage * 3
        return True

    def enemy_attack(self):
        damage = max(
            1,
            self.enemy_attack - self.robot.defense
        )

        self.robot.armor -= damage
        return damage

    def recharge(self):
        self.robot.energy = min(
            100,
            self.robot.energy + 30
        )

    def finish_round(self):
        if self.enemy_armor <= 0:
            self.robot.victories += 1
            self.score += 200
            self.round += 1
            self.enemy_armor = 120 + self.round * 10
            self.robot.armor = min(100, self.robot.armor + 20)
            return True

        return False

    def status(self):
        return {
            "pilot": self.pilot,
            "robot": self.robot.name,
            "armor": self.robot.armor,
            "energy": self.robot.energy,
            "enemy_armor": self.enemy_armor,
            "round": self.round,
            "victories": self.robot.victories,
            "score": self.score,
        }


def create_game():
    return RobotArenaChampion()


def demo():
    game = create_game()
    game.plasma_strike()
    game.heavy_guard()
    game.shockwave()
    game.enemy_attack()
    game.recharge()
    game.finish_round()

    return game.status()


if __name__ == "__main__":
    print(demo())
