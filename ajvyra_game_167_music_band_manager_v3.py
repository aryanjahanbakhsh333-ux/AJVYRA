"""
AJVYRA 167 — Music Band Manager
Genre: Music / Career / Management
"""

from dataclasses import dataclass


@dataclass
class BandMember:
    name: str
    skill: int
    energy: int = 100


class MusicBandManager:
    title = "Music Band Manager"
    band_name = "Neon Echo"

    def __init__(self):
        self.money = 1000
        self.fans = 200
        self.fame = 0
        self.score = 0

        self.members = [
            BandMember("Ari", 78),
            BandMember("Juno", 84),
            BandMember("Vale", 72),
        ]

    def rehearse(self):
        for member in self.members:
            if member.energy < 20:
                return False

        for member in self.members:
            member.skill = min(
                100,
                member.skill + 3,
            )
            member.energy -= 15

        self.score += 100
        return True

    def concert(self, venue_capacity):
        average_skill = (
            sum(m.skill for m in self.members)
            / len(self.members)
        )

        energy = (
            sum(m.energy for m in self.members)
            / len(self.members)
        )

        audience = int(
            venue_capacity
            * (average_skill / 100)
            * (energy / 100)
        )

        self.fans += audience
        self.fame += audience // 20
        self.money += audience * 2
        self.score += audience * 5

        for member in self.members:
            member.energy = max(
                0,
                member.energy - 30,
            )

        return audience

    def record_song(self):
        cost = 250

        if self.money < cost:
            return False

        self.money -= cost
        self.fans += 100
        self.fame += 10
        self.score += 500
        return True

    def rest(self):
        for member in self.members:
            member.energy = min(
                100,
                member.energy + 35,
            )

    def status(self):
        return {
            "band": self.band_name,
            "money": self.money,
            "fans": self.fans,
            "fame": self.fame,
            "score": self.score,
            "members": {
                m.name: {
                    "skill": m.skill,
                    "energy": m.energy,
                }
                for m in self.members
            },
        }


def create_game():
    return MusicBandManager()


if __name__ == "__main__":
    game = create_game()
    game.rehearse()
    game.record_song()
    game.rest()
    game.concert(1000)
    print(game.status())
