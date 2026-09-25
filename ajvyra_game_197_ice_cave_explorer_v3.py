from dataclasses import dataclass
from typing import Dict


@dataclass
class IceExplorer:
    name: str
    warmth: int = 100
    oxygen: int = 100
    rope: int = 100
    discoveries: int = 0


class IceCaveExplorer:
    def __init__(self):
        self.explorer = IceExplorer("Kael Nor")
        self.position = "Entrance"
        self.score = 0
        self.depth = 0

        self.rooms: Dict[str, int] = {
            "Entrance": 0,
            "Frozen Hall": 20,
            "Crystal Chamber": 40,
            "Blue Abyss": 60,
            "Hidden Sanctuary": 80,
        }

    def descend(self, room: str):
        if room not in self.rooms:
            return False

        depth = self.rooms[room]
        cost = max(5, depth // 5)

        if self.explorer.rope < cost:
            return False

        self.explorer.rope -= cost
        self.explorer.oxygen -= 5
        self.explorer.warmth -= 7
        self.position = room
        self.depth = depth
        self.score += depth
        return True

    def inspect_crystal(self):
        if self.position != "Crystal Chamber":
            return False

        self.explorer.discoveries += 1
        self.score += 70
        return True

    def discover_sanctuary(self):
        if self.position != "Hidden Sanctuary":
            return False

        self.explorer.discoveries += 2
        self.score += 150
        return True

    def warm_up(self):
        self.explorer.warmth = min(
            100,
            self.explorer.warmth + 25
        )

    def surface(self):
        self.position = "Entrance"
        self.depth = 0
        self.explorer.oxygen = min(100, self.explorer.oxygen + 30)
        self.explorer.rope = min(100, self.explorer.rope + 20)

    def status(self):
        return {
            "explorer": self.explorer.name,
            "position": self.position,
            "depth": self.depth,
            "warmth": self.explorer.warmth,
            "oxygen": self.explorer.oxygen,
            "rope": self.explorer.rope,
            "discoveries": self.explorer.discoveries,
            "score": self.score,
        }


def create_game():
    return IceCaveExplorer()


def demo():
    game = create_game()
    game.descend("Frozen Hall")
    game.descend("Crystal Chamber")
    game.inspect_crystal()
    game.descend("Hidden Sanctuary")
    game.discover_sanctuary()
    game.surface()
    return game.status()


if __name__ == "__main__":
    print(demo())
