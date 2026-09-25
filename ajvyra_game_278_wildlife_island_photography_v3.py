from dataclasses import dataclass


@dataclass
class WildlifeSubject:
    name: str
    rarity: int
    patience: int
    photographed: bool = False


class WildlifeIslandPhotography:
    def __init__(self):
        self.photographer = "Mira Lens"
        self.battery = 100
        self.film = 20
        self.stealth = 65
        self.score = 0
        self.photos = 0
        self.money = 100

        self.subjects = [
            WildlifeSubject("Silver Fox", 30, 60),
            WildlifeSubject("Storm Eagle", 60, 50),
            WildlifeSubject("Blue Panther", 90, 40),
            WildlifeSubject("Golden Crane", 120, 30),
        ]

    def scout(self):
        if self.battery < 8:
            return False

        self.battery -= 8
        self.score += 25
        return True

    def approach(self, index: int):
        if not 0 <= index < len(self.subjects):
            return False

        subject = self.subjects[index]

        if self.battery < 10:
            return False

        self.battery -= 10

        if self.stealth >= subject.patience:
            self.score += subject.rarity
            return True

        self.stealth = max(20, self.stealth - 10)
        return False

    def photograph(self, index: int):
        if not 0 <= index < len(self.subjects):
            return False

        subject = self.subjects[index]

        if subject.photographed or self.film <= 0:
            return False

        self.film -= 1
        subject.photographed = True
        self.photos += 1
        self.score += subject.rarity * 2
        self.money += subject.rarity
        return True

    def change_lens(self):
        self.stealth += 10
        self.battery = max(0, self.battery - 5)

    def recharge(self):
        self.battery = min(100, self.battery + 40)

    def status(self):
        return {
            "photographer": self.photographer,
            "battery": self.battery,
            "film": self.film,
            "photos": self.photos,
            "money": self.money,
            "score": self.score,
            "subjects": len(self.subjects),
        }


def create_game():
    return WildlifeIslandPhotography()


if __name__ == "__main__":
    game = create_game()
    game.scout()
    game.approach(0)
    game.photograph(0)
    print(game.status())
