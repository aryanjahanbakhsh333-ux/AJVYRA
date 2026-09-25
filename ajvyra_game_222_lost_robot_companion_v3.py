from dataclasses import dataclass


@dataclass
class CompanionRobot:
    name: str
    battery: int = 100
    trust: int = 20
    courage: int = 50
    memories: int = 0


class LostRobotCompanion:
    def __init__(self):
        self.hero = "Mira Vale"
        self.robot = CompanionRobot("Lumo")
        self.location = "Abandoned Station"
        self.distance = 100
        self.supplies = 5
        self.score = 0
        self.fragments = 0
        self.finished = False

    def explore(self):
        if self.robot.battery < 10:
            return False

        self.robot.battery -= 10
        self.distance = max(0, self.distance - 15)
        self.score += 10
        return True

    def repair_robot(self):
        if self.supplies <= 0:
            return False

        self.supplies -= 1
        self.robot.battery = min(100, self.robot.battery + 25)
        self.robot.trust = min(100, self.robot.trust + 8)
        self.score += 15
        return True

    def share_memory(self):
        if self.robot.battery < 5:
            return False

        self.robot.battery -= 5
        self.robot.memories += 1
        self.robot.trust = min(100, self.robot.trust + 15)
        self.score += 20
        return True

    def cross_danger(self):
        if self.robot.trust < 40:
            self.robot.courage = max(0, self.robot.courage - 10)
            return False

        self.robot.battery -= 15
        self.robot.courage = min(100, self.robot.courage + 10)
        self.distance = max(0, self.distance - 30)
        self.score += 35
        return True

    def recover_memory_fragment(self):
        if self.distance > 30:
            return False

        self.fragments += 1
        self.robot.memories += 1
        self.score += 50
        return True

    def reach_home(self):
        if self.distance > 0 or self.fragments < 1:
            return False

        self.finished = True
        self.score += self.robot.trust
        return True

    def status(self):
        return {
            "hero": self.hero,
            "robot": self.robot.name,
            "location": self.location,
            "distance": self.distance,
            "battery": self.robot.battery,
            "trust": self.robot.trust,
            "memories": self.robot.memories,
            "fragments": self.fragments,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return LostRobotCompanion()


if __name__ == "__main__":
    game = create_game()
    game.explore()
    game.share_memory()
    game.repair_robot()
    print(game.status())
