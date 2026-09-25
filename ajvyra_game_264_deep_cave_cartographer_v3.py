from dataclasses import dataclass


@dataclass
class CaveMap:
    name: str
    discovered: int = 0
    danger: int = 30
    accuracy: int = 50


class DeepCaveCartographer:
    def __init__(self):
        self.cartographer = "Tarin Moss"
        self.energy = 100
        self.rope = 500
        self.depth = 0
        self.score = 0
        self.maps_completed = 0
        self.caves = [
            CaveMap("Echo Cavern"),
            CaveMap("Crystal Depths"),
            CaveMap("Blackwater Tunnel"),
            CaveMap("Titan Hollow"),
        ]

    def descend(self, distance: int):
        if distance <= 0 or self.energy < distance // 10:
            return False

        self.energy -= max(5, distance // 10)
        self.rope -= distance
        self.depth += distance
        self.score += distance // 2
        return self.rope > 0

    def map_area(self, index: int):
        if not 0 <= index < len(self.caves):
            return False

        if self.energy < 15:
            return False

        cave = self.caves[index]
        self.energy -= 15
        cave.discovered += 25
        cave.accuracy += 8
        self.score += 40
        return True

    def mark_danger(self, index: int):
        if not 0 <= index < len(self.caves):
            return False

        cave = self.caves[index]
        cave.danger = max(0, cave.danger - 10)
        self.score += 20
        return True

    def surface(self):
        self.depth = 0
        self.energy = min(100, self.energy + 35)
        self.rope = min(500, self.rope + 100)

    def complete_map(self, index: int):
        if not 0 <= index < len(self.caves):
            return False

        cave = self.caves[index]

        if cave.discovered < 100:
            return False

        self.maps_completed += 1
        self.score += 250
        return True

    def status(self):
        return {
            "cartographer": self.cartographer,
            "depth": self.depth,
            "energy": self.energy,
            "rope": self.rope,
            "maps_completed": self.maps_completed,
            "score": self.score,
            "caves": len(self.caves),
        }


def create_game():
    return DeepCaveCartographer()


if __name__ == "__main__":
    game = create_game()
    game.descend(100)
    game.map_area(0)
    game.mark_danger(0)
    print(game.status())
