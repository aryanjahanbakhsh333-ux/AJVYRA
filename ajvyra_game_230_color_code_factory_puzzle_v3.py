from dataclasses import dataclass


@dataclass
class FactoryNode:
    name: str
    code: str
    output: int
    solved: bool = False


class ColorCodeFactoryPuzzle:
    def __init__(self):
        self.engineer = "Riven Cole"
        self.energy = 100
        self.level = 1
        self.score = 0
        self.products = 0
        self.coins = 100
        self.nodes = [
            FactoryNode("Node A", "RED-BLUE", 20),
            FactoryNode("Node B", "BLUE-GREEN", 30),
            FactoryNode("Node C", "GREEN-YELLOW", 40),
            FactoryNode("Node D", "YELLOW-PURPLE", 55),
        ]

    def inspect_node(self, index: int):
        if index < 0 or index >= len(self.nodes):
            return None

        return {
            "name": self.nodes[index].name,
            "required_code": self.nodes[index].code,
            "output": self.nodes[index].output,
        }

    def solve_node(self, index: int, code: str):
        if index < 0 or index >= len(self.nodes):
            return False

        node = self.nodes[index]

        if node.solved or self.energy < 10:
            return False

        self.energy -= 10

        if code.upper() != node.code:
            self.score = max(0, self.score - 10)
            return False

        node.solved = True
        self.products += node.output
        self.score += node.output
        self.coins += node.output // 2

        if self.score >= self.level * 150:
            self.level += 1

        return True

    def optimize_factory(self):
        solved = sum(node.solved for node in self.nodes)

        if solved < 2 or self.energy < 15:
            return False

        self.energy -= 15
        self.products += solved * 10
        self.score += solved * 25
        return True

    def sell_products(self):
        if self.products <= 0:
            return False

        self.coins += self.products * 2
        self.score += self.products
        self.products = 0
        return True

    def recharge(self):
        self.energy = min(100, self.energy + 35)

    def status(self):
        return {
            "engineer": self.engineer,
            "level": self.level,
            "energy": self.energy,
            "score": self.score,
            "coins": self.coins,
            "products": self.products,
            "solved_nodes": sum(n.solved for n in self.nodes),
            "total_nodes": len(self.nodes),
        }


def create_game():
    return ColorCodeFactoryPuzzle()


if __name__ == "__main__":
    game = create_game()
    game.solve_node(0, "RED-BLUE")
    game.solve_node(1, "BLUE-GREEN")
    game.optimize_factory()
    game.sell_products()
    print(game.status())
