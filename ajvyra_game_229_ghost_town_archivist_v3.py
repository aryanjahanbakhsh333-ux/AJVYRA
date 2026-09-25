from dataclasses import dataclass


@dataclass
class ArchiveFragment:
    title: str
    year: int
    rarity: int
    discovered: bool = False


class GhostTownArchivist:
    def __init__(self):
        self.archivist = "Elias Wren"
        self.location = "Grey Hollow"
        self.energy = 100
        self.reputation = 10
        self.score = 0
        self.fragments_found = 0
        self.final_story = False

        self.archive = [
            ArchiveFragment("The First Settlement", 1872, 20),
            ArchiveFragment("The Train Record", 1891, 35),
            ArchiveFragment("The Empty School", 1910, 50),
            ArchiveFragment("The Last Letter", 1934, 70),
            ArchiveFragment("The Town's Secret", 1940, 100),
        ]

    def search_building(self, index: int):
        if index < 0 or index >= len(self.archive):
            return False

        if self.energy < 12:
            return False

        fragment = self.archive[index]

        if fragment.discovered:
            return False

        self.energy -= 12
        fragment.discovered = True
        self.fragments_found += 1
        self.score += fragment.rarity
        return True

    def compare_records(self):
        if self.fragments_found < 2:
            return False

        self.reputation += 10
        self.score += 30
        return True

    def reconstruct_history(self):
        if self.fragments_found < 4:
            return False

        self.score += 100
        self.reputation += 25
        return True

    def uncover_final_story(self):
        if self.fragments_found < 5:
            return False

        self.final_story = True
        self.score += 250
        self.reputation += 50
        return True

    def rest(self):
        self.energy = min(100, self.energy + 30)

    def status(self):
        return {
            "archivist": self.archivist,
            "location": self.location,
            "energy": self.energy,
            "reputation": self.reputation,
            "score": self.score,
            "fragments_found": self.fragments_found,
            "final_story": self.final_story,
        }


def create_game():
    return GhostTownArchivist()


if __name__ == "__main__":
    game = create_game()
    game.search_building(0)
    game.search_building(1)
    game.compare_records()
    print(game.status())
