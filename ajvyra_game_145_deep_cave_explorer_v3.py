"""
AJVYRA 145 — Deep Cave Explorer
Genre: Exploration / Resource Management
"""

from dataclasses import dataclass


@dataclass
class CaveZone:
    name: str
    depth: int
    treasure: int
    danger: int
    explored: bool = False


class DeepCaveExplorer:
    title = "Deep Cave Explorer"
    explorer = "Tarin Moss"

    def __init__(self):
        self.energy = 100
        self.rope = 100
        self.lamps = 5
        self.gold = 0
        self.score = 0

        self.zones = [
            CaveZone("Echo Entrance", 50, 40, 10),
            CaveZone("Crystal Hall", 180, 120, 25),
            CaveZone("Black Tunnel", 350, 250, 45),
            CaveZone("Dragon Vault", 600, 600, 80),
        ]

    def explore(self, index):
        if not 0 <= index < len(self.zones):
            return False

        zone = self.zones[index]

        if zone.explored:
            return False

        cost = zone.depth // 10

        if self.energy < cost or self.rope < cost // 2:
            return False

        self.energy -= cost
        self.rope -= cost // 2
        self.lamps -= 1

        zone.explored = True

        reward = max(
            0,
            zone.treasure - zone.danger,
        )

        self.gold += reward
        self.score += reward * 2
        return True

    def repair_rope(self):
        if self.gold < 100:
            return False

        self.gold -= 100
        self.rope = min(
            100,
            self.rope + 35,
        )
        return True

    def rest(self):
        self.energy = min(
            100,
            self.energy + 35,
        )

    def status(self):
        return {
            "explorer": self.explorer,
            "energy": self.energy,
            "rope": self.rope,
            "lamps": self.lamps,
            "gold": self.gold,
            "score": self.score,
            "explored": [
                z.name
                for z in self.zones
                if z.explored
            ],
        }


def create_game():
    return DeepCaveExplorer()


if __name__ == "__main__":
    game = create_game()
    game.explore(0)
    game.explore(1)
    print(game.status())
