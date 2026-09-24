from dataclasses import dataclass
import random


@dataclass
class Dinosaur:
    species: str
    rarity: str
    danger: int
    discovered: bool = False


class DinosaurExpeditionGame:
    GAME_ID = "AJVYRA-075"
    TITLE = "Jurassic Frontier"
    GENRE = "Dinosaur Expedition"

    def __init__(self):
        self.explorer = "Rai Kellan"
        self.health = 100
        self.supplies = 15
        self.discovery = 0

        self.dinosaurs = [
            Dinosaur("Velociraptor", "Common", 35),
            Dinosaur("Triceratops", "Rare", 45),
            Dinosaur("Stegosaurus", "Rare", 40),
            Dinosaur("Tyrannosaurus", "Legendary", 90),
            Dinosaur("Spinosaurus", "Legendary", 95),
        ]

    def explore(self, index: int):
        if index < 0 or index >= len(self.dinosaurs):
            return False

        if self.supplies <= 0:
            return False

        dinosaur = self.dinosaurs[index]
        self.supplies -= 1

        risk = random.randint(1, 100)

        if risk > dinosaur.danger:
            dinosaur.discovered = True
            self.discovery += 20
            return {
                "success": True,
                "species": dinosaur.species,
            }

        self.health = max(0, self.health - random.randint(5, 20))

        return {
            "success": False,
            "species": dinosaur.species,
        }

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "explorer": self.explorer,
            "health": self.health,
            "supplies": self.supplies,
            "discovery": self.discovery,
            "dinosaurs": [d.__dict__.copy() for d in self.dinosaurs],
        }
