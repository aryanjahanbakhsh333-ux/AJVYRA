from dataclasses import dataclass
from typing import List


@dataclass
class DefenseTower:
    name: str
    power: int
    accuracy: int
    health: int = 100


@dataclass
class Meteor:
    size: int
    distance: int
    destroyed: bool = False


class MeteorShowerDefense:
    def __init__(self):
        self.commander = "Vera Sol"
        self.energy = 150
        self.score = 0
        self.wave = 1
        self.towers: List[DefenseTower] = [
            DefenseTower("North Cannon", 25, 70),
            DefenseTower("East Cannon", 30, 65),
            DefenseTower("Orbital Laser", 45, 80),
        ]

        self.meteors = [
            Meteor(20, 100),
            Meteor(35, 140),
            Meteor(50, 180),
            Meteor(25, 120),
        ]

    def fire(self, tower_index: int, meteor_index: int):
        if not (0 <= tower_index < len(self.towers)):
            return False

        if not (0 <= meteor_index < len(self.meteors)):
            return False

        tower = self.towers[tower_index]
        meteor = self.meteors[meteor_index]

        if meteor.destroyed or self.energy < tower.power:
            return False

        self.energy -= tower.power

        hit = tower.accuracy >= 60

        if hit:
            meteor.destroyed = True
            self.score += meteor.size * 5
            return True

        self.score = max(0, self.score - 5)
        return False

    def emergency_power(self):
        self.energy = min(200, self.energy + 40)
        self.score += 10

    def repair_tower(self, index: int):
        if not (0 <= index < len(self.towers)):
            return False

        tower = self.towers[index]

        if self.energy < 20:
            return False

        self.energy -= 20
        tower.health = min(100, tower.health + 25)
        return True

    def next_wave(self):
        if all(m.destroyed for m in self.meteors):
            self.wave += 1
            self.energy = min(200, self.energy + 30)
            return True

        return False

    def victory(self):
        return all(m.destroyed for m in self.meteors)

    def status(self):
        return {
            "commander": self.commander,
            "wave": self.wave,
            "energy": self.energy,
            "score": self.score,
            "meteors_destroyed": sum(
                m.destroyed for m in self.meteors
            ),
            "total_meteors": len(self.meteors),
            "victory": self.victory(),
        }


def create_game():
    return MeteorShowerDefense()


def demo():
    game = create_game()

    for i in range(len(game.meteors)):
        game.fire(2, i)

    game.next_wave()
    return game.status()


if __name__ == "__main__":
    print(demo())
