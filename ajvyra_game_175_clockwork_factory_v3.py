"""
AJVYRA 175 — Clockwork Factory
Genre: Automation / Puzzle / Management
"""

from dataclasses import dataclass


@dataclass
class Machine:
    name: str
    efficiency: int
    maintenance: int
    active: bool = True


class ClockworkFactory:
    title = "Clockwork Factory"
    inventor = "Oren Gear"

    def __init__(self):
        self.money = 2500
        self.materials = 100
        self.products = 0
        self.energy = 100
        self.score = 0

        self.machines = [
            Machine("Press", 80, 10),
            Machine("Assembler", 75, 15),
            Machine("Polisher", 65, 20),
        ]

    def produce(self):
        active = [
            m for m in self.machines
            if m.active
        ]

        if not active:
            return False

        material_cost = len(active) * 8

        if (
            self.materials < material_cost
            or self.energy < 15
        ):
            return False

        efficiency = sum(
            m.efficiency for m in active
        ) // len(active)

        output = max(
            1,
            efficiency // 20,
        )

        self.materials -= material_cost
        self.energy -= 15
        self.products += output
        self.score += output * 60
        return output

    def maintain(self, machine_name):
        machine = self._find(machine_name)

        if machine is None or self.money < 100:
            return False

        self.money -= 100
        machine.maintenance = max(
            0,
            machine.maintenance - 5,
        )
        machine.efficiency = min(
            100,
            machine.efficiency + 3,
        )
        return True

    def buy_materials(self, amount):
        if amount <= 0:
            return False

        cost = amount * 5

        if self.money < cost:
            return False

        self.money -= cost
        self.materials += amount
        return True

    def sell_products(self):
        if self.products <= 0:
            return 0

        revenue = self.products * 80
        self.money += revenue
        self.score += revenue
        self.products = 0
        return revenue

    def recharge(self):
        self.energy = min(
            100,
            self.energy + 40,
        )

    def _find(self, name):
        return next(
            (
                m for m in self.machines
                if m.name == name
            ),
            None,
        )

    def status(self):
        return {
            "inventor": self.inventor,
            "money": self.money,
            "materials": self.materials,
            "products": self.products,
            "energy": self.energy,
            "score": self.score,
        }


def create_game():
    return ClockworkFactory()


if __name__ == "__main__":
    game = create_game()
    game.produce()
    game.maintain("Press")
    game.sell_products()
    print(game.status())
