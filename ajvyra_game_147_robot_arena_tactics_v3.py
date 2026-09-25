"""
AJVYRA 147 — Robot Arena Tactics
Genre: Tactical Combat
"""

from dataclasses import dataclass


@dataclass
class Robot:
    name: str
    armor: int
    energy: int
    attack: int
    speed: int


class RobotArenaTactics:
    title = "Robot Arena Tactics"
    pilot = "Vex Orion"

    def __init__(self):
        self.credits = 1000
        self.round = 1
        self.score = 0

        self.robot = Robot(
            "AX-9",
            armor=90,
            energy=100,
            attack=75,
            speed=70,
        )

    def strike(self, enemy_armor):
        if self.robot.energy < 15:
            return False

        self.robot.energy -= 15

        damage = (
            self.robot.attack
            + self.robot.speed // 3
        )

        if damage >= enemy_armor:
            self.score += enemy_armor * 3
            self.credits += 250
            return True

        return False

    def shield(self):
        if self.robot.energy < 20:
            return False

        self.robot.energy -= 20
        self.robot.armor = min(
            100,
            self.robot.armor + 15,
        )
        return True

    def overdrive(self):
        if self.robot.energy < 40:
            return False

        self.robot.energy -= 40
        self.robot.attack += 15
        self.robot.speed += 10
        self.score += 100
        return True

    def recharge(self):
        self.robot.energy = min(
            100,
            self.robot.energy + 35,
        )

    def next_round(self):
        self.round += 1
        self.recharge()

    def status(self):
        return {
            "pilot": self.pilot,
            "robot": self.robot.name,
            "round": self.round,
            "armor": self.robot.armor,
            "energy": self.robot.energy,
            "attack": self.robot.attack,
            "speed": self.robot.speed,
            "credits": self.credits,
            "score": self.score,
        }


def create_game():
    return RobotArenaTactics()


if __name__ == "__main__":
    game = create_game()
    game.overdrive()
    game.strike(80)
    print(game.status())
