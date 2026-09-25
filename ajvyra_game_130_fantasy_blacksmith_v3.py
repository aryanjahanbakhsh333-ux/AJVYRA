"""
AJVYRA 130 — Fantasy Blacksmith
Genre: Crafting / RPG
"""

from dataclasses import dataclass


@dataclass
class Material:
    name: str
    strength: int
    rarity: int


@dataclass
class Weapon:
    name: str
    power: int
    durability: int
    rarity: int


class FantasyBlacksmith:
    title = "Fantasy Blacksmith"
    blacksmith = "Eron Forge"

    def __init__(self):
        self.gold = 500
        self.level = 1
        self.experience = 0
        self.materials = {
            "iron": 20,
            "moonsteel": 5,
            "dragon_glass": 2,
        }
        self.material_data = {
            "iron": Material("Iron", 10, 1),
            "moonsteel": Material("Moonsteel", 30, 5),
            "dragon_glass": Material("Dragon Glass", 50, 10),
        }
        self.weapons: list[Weapon] = []

    def forge(self, material_name, weapon_name):
        if material_name not in self.materials:
            return None

        if self.materials[material_name] <= 0:
            return None

        material = self.material_data[material_name]
        self.materials[material_name] -= 1

        power = material.strength + self.level * 5
        durability = material.strength * 3

        weapon = Weapon(
            weapon_name,
            power,
            durability,
            material.rarity,
        )

        self.weapons.append(weapon)
        self.experience += material.rarity * 20

        self._level_up()
        return weapon

    def temper(self, weapon_index):
        if not 0 <= weapon_index < len(self.weapons):
            return False

        weapon = self.weapons[weapon_index]

        if self.gold < 50:
            return False

        self.gold -= 50
        weapon.power += 10
        weapon.durability += 20
        self.experience += 10

        self._level_up()
        return True

    def enchant(self, weapon_index):
        if not 0 <= weapon_index < len(self.weapons):
            return False

        weapon = self.weapons[weapon_index]

        if self.materials["dragon_glass"] <= 0:
            return False

        self.materials["dragon_glass"] -= 1
        weapon.power += 30
        weapon.rarity += 5
        self.experience += 50

        self._level_up()
        return True

    def sell(self, weapon_index):
        if not 0 <= weapon_index < len(self.weapons):
            return False

        weapon = self.weapons.pop(weapon_index)
        self.gold += (
            weapon.power
            + weapon.durability
            + weapon.rarity * 10
        )
        return True

    def _level_up(self):
        required = self.level * 100

        while self.experience >= required:
            self.experience -= required
            self.level += 1
            required = self.level * 100

    def status(self):
        return {
            "blacksmith": self.blacksmith,
            "level": self.level,
            "experience": self.experience,
            "gold": self.gold,
            "materials": dict(self.materials),
            "weapons": [
                {
                    "name": w.name,
                    "power": w.power,
                    "durability": w.durability,
                    "rarity": w.rarity,
                }
                for w in self.weapons
            ],
        }


def create_game():
    return FantasyBlacksmith()


if __name__ == "__main__":
    game = create_game()

    game.forge("iron", "Dawn Blade")
    game.forge("moonsteel", "Moon Fang")
    game.enchant(1)

    print(game.status())
