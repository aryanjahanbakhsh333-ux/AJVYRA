from dataclasses import dataclass


@dataclass
class ArcadeMachine:
    name: str
    popularity: int
    condition: int = 100
    revenue: int = 0


class NeonArcadeOwner:
    def __init__(self):
        self.owner = "Kai Nova"
        self.money = 800
        self.reputation = 20
        self.energy = 100
        self.score = 0
        self.day = 1

        self.machines = [
            ArcadeMachine("Cyber Racer", 80),
            ArcadeMachine("Pixel Fighter", 90),
            ArcadeMachine("Galaxy Shooter", 75),
            ArcadeMachine("Mystery Cabinet", 65),
        ]

    def repair_machine(self, index: int):
        if not 0 <= index < len(self.machines):
            return False

        if self.money < 50:
            return False

        self.money -= 50
        self.machines[index].condition = min(
            100,
            self.machines[index].condition + 30
        )
        self.score += 25
        return True

    def promote_machine(self, index: int):
        if not 0 <= index < len(self.machines):
            return False

        if self.money < 70:
            return False

        self.money -= 70
        self.machines[index].popularity = min(
            100,
            self.machines[index].popularity + 10
        )
        self.score += 30
        return True

    def open_arcade(self):
        total_income = 0

        for machine in self.machines:
            if machine.condition <= 0:
                continue

            income = (
                machine.popularity
                * machine.condition
                // 100
            )

            machine.revenue += income
            total_income += income
            machine.condition = max(
                0,
                machine.condition - 3
            )

        self.money += total_income
        self.score += total_income
        self.reputation += total_income // 100
        return total_income

    def hire_technician(self):
        if self.money < 150:
            return False

        self.money -= 150

        for machine in self.machines:
            machine.condition = min(
                100,
                machine.condition + 10
            )

        self.score += 50
        return True

    def next_day(self):
        self.day += 1
        self.energy = min(100, self.energy + 40)

    def status(self):
        return {
            "owner": self.owner,
            "day": self.day,
            "money": self.money,
            "reputation": self.reputation,
            "score": self.score,
            "machines": len(self.machines),
            "average_condition": (
                sum(m.condition for m in self.machines)
                // len(self.machines)
            ),
        }


def create_game():
    return NeonArcadeOwner()


if __name__ == "__main__":
    game = create_game()
    game.open_arcade()
    game.repair_machine(1)
    game.promote_machine(0)
    print(game.status())
