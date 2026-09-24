from dataclasses import dataclass


@dataclass
class Robot:
    name: str
    speed: int
    armor: int
    intelligence: int


class RobotFactoryGame:
    GAME_ID = "AJVYRA-097"
    TITLE = "Mech Foundry"
    GENRE = "Robot Factory Simulation"

    def __init__(self):
        self.engineer = "Axel Nox"
        self.money = 2500
        self.factory_level = 1
        self.robots = []

    def build_robot(
        self,
        name: str,
        speed: int,
        armor: int,
        intelligence: int,
    ):
        cost = 300 + (speed + armor + intelligence) * 3

        if self.money < cost:
            return False

        robot = Robot(
            name,
            max(1, min(100, speed)),
            max(1, min(100, armor)),
            max(1, min(100, intelligence)),
        )

        self.money -= cost
        self.robots.append(robot)

        return True

    def test_robot(self, index: int):
        if index < 0 or index >= len(self.robots):
            return False

        robot = self.robots[index]

        performance = (
            robot.speed * 0.35
            + robot.armor * 0.25
            + robot.intelligence * 0.40
        )

        reward = int(performance * 8)
        self.money += reward

        return reward

    def upgrade_factory(self):
        cost = self.factory_level * 1200

        if self.money < cost:
            return False

        self.money -= cost
        self.factory_level += 1

        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "engineer": self.engineer,
            "money": self.money,
            "factory_level": self.factory_level,
            "robots": [r.__dict__.copy() for r in self.robots],
        }
