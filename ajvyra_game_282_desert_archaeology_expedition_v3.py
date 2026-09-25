from dataclasses import dataclass


@dataclass
class ArtifactSite:
    name: str
    difficulty: int
    value: int
    discovered: bool = False
    documented: bool = False


class DesertArchaeologyExpedition:
    def __init__(self):
        self.archaeologist = "Sera Venn"
        self.water = 100
        self.food = 100
        self.tools = 80
        self.distance = 0
        self.score = 0
        self.artifacts = 0
        self.credits = 300
        self.day = 1
        self.expedition_complete = False

        self.sites = [
            ArtifactSite("Sunken Observatory", 25, 80),
            ArtifactSite("Glass Temple", 45, 130),
            ArtifactSite("Buried Palace", 65, 200),
            ArtifactSite("Crown Archive", 85, 300),
        ]

    def travel(self, distance: int = 100):
        if self.water < 8 or self.food < 5:
            return False

        self.water -= 8
        self.food -= 5
        self.distance += distance
        self.score += distance // 5
        return True

    def excavate(self, index: int):
        if not 0 <= index < len(self.sites):
            return False

        site = self.sites[index]

        if self.tools < site.difficulty:
            return False

        self.tools -= site.difficulty // 2
        site.discovered = True
        self.artifacts += 1
        self.score += site.value
        return True

    def document(self, index: int):
        if not 0 <= index < len(self.sites):
            return False

        site = self.sites[index]

        if not site.discovered or site.documented:
            return False

        site.documented = True
        self.score += 75
        self.credits += site.value // 2
        return True

    def rest(self):
        self.water = min(100, self.water + 20)
        self.food = min(100, self.food + 15)
        self.tools = min(100, self.tools + 10)

    def next_day(self):
        self.day += 1
        self.water = max(0, self.water - 4)
        self.food = max(0, self.food - 3)

    def finish_expedition(self):
        if self.artifacts >= 4:
            self.expedition_complete = True
            self.score += 500
            return True

        return False

    def status(self):
        return {
            "archaeologist": self.archaeologist,
            "day": self.day,
            "distance": self.distance,
            "water": self.water,
            "food": self.food,
            "tools": self.tools,
            "artifacts": self.artifacts,
            "credits": self.credits,
            "score": self.score,
            "complete": self.expedition_complete,
        }


def create_game():
    return DesertArchaeologyExpedition()


if __name__ == "__main__":
    game = create_game()
    game.travel()
    game.excavate(0)
    game.document(0)
    print(game.status())
