from dataclasses import dataclass


@dataclass
class RobotPet:
    name: str
    battery: int = 100
    happiness: int = 60
    intelligence: int = 40
    trust: int = 50


class RobotPetAdventure:
    def __init__(self):
        self.owner = "Niko Ray"
        self.pet = RobotPet("Milo-8")
        self.location = "Home"
        self.distance = 0
        self.score = 0
        self.coins = 100
        self.memory_chips = 0
        self.adventure_complete = False

    def explore(self):
        if self.pet.battery < 15:
            return False

        self.pet.battery -= 15
        self.distance += 30
        self.pet.happiness = min(
            100,
            self.pet.happiness + 5
        )
        self.score += 20
        return True

    def play(self):
        if self.pet.battery < 10:
            return False

        self.pet.battery -= 10
        self.pet.happiness = min(
            100,
            self.pet.happiness + 15
        )
        self.pet.trust = min(100, self.pet.trust + 5)
        self.score += 25
        return True

    def teach(self):
        if self.pet.battery < 12:
            return False

        self.pet.battery -= 12
        self.pet.intelligence += 8
        self.pet.trust += 3
        self.score += 30
        return True

    def find_memory_chip(self):
        if self.distance < 50:
            return False

        self.memory_chips += 1
        self.pet.intelligence += 5
        self.score += 60
        return True

    def recharge(self):
        self.pet.battery = min(100, self.pet.battery + 40)

    def complete_adventure(self):
        if self.memory_chips >= 5 and self.pet.trust >= 80:
            self.adventure_complete = True
            self.score += 300
            return True

        return False

    def status(self):
        return {
            "owner": self.owner,
            "pet": self.pet.name,
            "location": self.location,
            "battery": self.pet.battery,
            "happiness": self.pet.happiness,
            "intelligence": self.pet.intelligence,
            "trust": self.pet.trust,
            "distance": self.distance,
            "memory_chips": self.memory_chips,
            "score": self.score,
            "complete": self.adventure_complete,
        }


def create_game():
    return RobotPetAdventure()


if __name__ == "__main__":
    game = create_game()
    game.play()
    game.explore()
    game.find_memory_chip()
    game.recharge()
    print(game.status())
