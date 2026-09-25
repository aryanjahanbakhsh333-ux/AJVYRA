from dataclasses import dataclass


@dataclass
class Lighthouse:
    name: str
    light_power: int = 60
    lens_condition: int = 100
    fuel: int = 100
    visibility: int = 70


class FantasyLighthouseKeeper:
    def __init__(self):
        self.keeper = "Elian Moon"
        self.lighthouse = Lighthouse("Moonfire Beacon")
        self.mana = 100
        self.ships_saved = 0
        self.score = 0
        self.day = 1
        self.money = 250

    def ignite_beacon(self):
        if self.lighthouse.fuel < 10:
            return False

        self.lighthouse.fuel -= 10
        self.lighthouse.light_power = min(
            100,
            self.lighthouse.light_power + 8
        )
        self.score += 30
        return True

    def magical_beam(self):
        if self.mana < 20:
            return False

        self.mana -= 20
        self.lighthouse.visibility = min(
            100,
            self.lighthouse.visibility + 20
        )
        self.score += 80
        return True

    def repair_lens(self):
        if self.money < 70:
            return False

        self.money -= 70
        self.lighthouse.lens_condition = min(
            100,
            self.lighthouse.lens_condition + 25
        )
        self.score += 40
        return True

    def guide_ship(self):
        if (
            self.lighthouse.light_power < 50
            or self.lighthouse.visibility < 50
        ):
            return False

        self.ships_saved += 1
        self.score += 150
        self.money += 60
        return True

    def restore_mana(self):
        self.mana = min(100, self.mana + 30)

    def next_night(self):
        self.day += 1
        self.lighthouse.fuel = max(
            0,
            self.lighthouse.fuel - 5
        )
        self.lighthouse.lens_condition = max(
            0,
            self.lighthouse.lens_condition - 3
        )
        self.restore_mana()

    def status(self):
        return {
            "keeper": self.keeper,
            "lighthouse": self.lighthouse.name,
            "light_power": self.lighthouse.light_power,
            "lens": self.lighthouse.lens_condition,
            "fuel": self.lighthouse.fuel,
            "visibility": self.lighthouse.visibility,
            "mana": self.mana,
            "ships_saved": self.ships_saved,
            "money": self.money,
            "score": self.score,
            "day": self.day,
        }


def create_game():
    return FantasyLighthouseKeeper()


if __name__ == "__main__":
    game = create_game()
    game.ignite_beacon()
    game.magical_beam()
    game.guide_ship()
    print(game.status())
