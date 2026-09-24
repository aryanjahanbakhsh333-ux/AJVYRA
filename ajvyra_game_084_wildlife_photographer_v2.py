from dataclasses import dataclass
import random


@dataclass
class Animal:
    name: str
    rarity: str
    value: int
    patience: int
    photographed: bool = False


class WildlifePhotographerGame:
    GAME_ID = "AJVYRA-084"
    TITLE = "Wild Lens"
    GENRE = "Wildlife Photography"

    def __init__(self):
        self.photographer = "Mira Sol"
        self.camera_battery = 100
        self.photos = 0
        self.reputation = 0

        self.animals = [
            Animal("Silver Wolf", "Rare", 80, 70),
            Animal("Golden Eagle", "Rare", 100, 55),
            Animal("Moon Lynx", "Epic", 180, 40),
            Animal("Black Panther", "Legendary", 300, 25),
        ]

    def observe(self, index: int):
        if index < 0 or index >= len(self.animals):
            return False

        animal = self.animals[index]

        if animal.photographed or self.camera_battery < 5:
            return False

        self.camera_battery -= 5

        if random.randint(1, 100) <= animal.patience:
            animal.photographed = True
            self.photos += 1
            self.reputation += animal.value
            return {
                "success": True,
                "animal": animal.name,
            }

        return {
            "success": False,
            "animal": animal.name,
        }

    def recharge(self):
        self.camera_battery = 100

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "photographer": self.photographer,
            "battery": self.camera_battery,
            "photos": self.photos,
            "reputation": self.reputation,
            "animals": [a.__dict__.copy() for a in self.animals],
        }
