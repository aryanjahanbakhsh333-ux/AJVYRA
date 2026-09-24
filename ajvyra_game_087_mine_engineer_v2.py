from dataclasses import dataclass
import random


@dataclass
class MineNode:
    name: str
    resources: int
    stability: int


class MineEngineerGame:
    GAME_ID = "AJVYRA-087"
    TITLE = "Deep Core"
    GENRE = "Mining Engineering"

    def __init__(self):
        self.engineer = "Rex Orin"
        self.energy = 100
        self.money = 500
        self.risk = 0

        self.nodes = [
            MineNode("Copper Shaft", 100, 90),
            MineNode("Crystal Tunnel", 180, 75),
            MineNode("Titanium Core", 300, 60),
            MineNode("Dark Chamber", 500, 40),
        ]

    def mine(self, index: int):
        if index < 0 or index >= len(self.nodes):
            return False

        node = self.nodes[index]

        if self.energy < 15 or node.resources <= 0:
            return False

        self.energy -= 15

        extracted = min(node.resources, random.randint(10, 35))
        node.resources -= extracted

        node.stability -= random.randint(1, 8)

        if node.stability < 30:
            self.risk += 10

        self.money += extracted * 2

        return extracted

    def reinforce(self, index: int):
        if index < 0 or index >= len(self.nodes):
            return False

        if self.money < 100:
            return False

        self.money -= 100
        self.nodes[index].stability = min(
            100,
            self.nodes[index].stability + 20,
        )

        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "engineer": self.engineer,
            "energy": self.energy,
            "money": self.money,
            "risk": self.risk,
            "nodes": [n.__dict__.copy() for n in self.nodes],
        }
