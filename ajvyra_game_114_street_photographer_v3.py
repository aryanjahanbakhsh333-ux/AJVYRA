"""
AJVYRA 114 — Street Photographer
Genre: Photography / Exploration
"""

from dataclasses import dataclass


@dataclass
class Photo:
    subject: str
    composition: int
    timing: int
    rarity: int
    score: int = 0


class StreetPhotographer:
    title = "Street Photographer"
    photographer = "Ren Solis"

    SUBJECTS = {
        "rain": 25,
        "musician": 30,
        "runner": 20,
        "sunset": 35,
        "market": 15,
        "stranger_smile": 40,
    }

    def __init__(self):
        self.photos: list[Photo] = []
        self.reputation = 0
        self.camera_battery = 100
        self.money = 0

    def take_photo(
        self,
        subject: str,
        composition: int,
        timing: int,
    ):
        subject = subject.lower()

        if self.camera_battery <= 0:
            return None

        if subject not in self.SUBJECTS:
            return None

        composition = max(0, min(100, composition))
        timing = max(0, min(100, timing))
        rarity = self.SUBJECTS[subject]

        score = int(
            composition * 0.4
            + timing * 0.4
            + rarity * 0.2
        )

        photo = Photo(
            subject,
            composition,
            timing,
            rarity,
            score,
        )

        self.photos.append(photo)
        self.camera_battery -= 5
        self.reputation += score // 20
        self.money += score // 10

        return photo

    def recharge(self):
        self.camera_battery = 100

    def gallery(self):
        return [
            {
                "subject": p.subject,
                "score": p.score,
            }
            for p in self.photos
        ]

    def status(self):
        return {
            "photographer": self.photographer,
            "battery": self.camera_battery,
            "reputation": self.reputation,
            "money": self.money,
            "photos": self.gallery(),
        }


def create_game():
    return StreetPhotographer()


if __name__ == "__main__":
    game = create_game()
    game.take_photo("rain", 92, 88)
    print(game.status())
