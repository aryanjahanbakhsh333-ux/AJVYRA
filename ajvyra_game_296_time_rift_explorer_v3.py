from dataclasses import dataclass


@dataclass
class TimeExplorer:
    name: str
    stability: int = 100
    energy: int = 100
    knowledge: int = 0


class TimeRiftExplorer:
    def __init__(self):
        self.explorer = TimeExplorer("Orin Vale")
        self.year = 2026
        self.target_year = 3026
        self.score = 0
        self.artifacts = 0
        self.rifts_closed = 0
        self.returned = False

    def jump(self, years: int):
        cost = max(10, abs(years) // 20)

        if self.explorer.energy < cost:
            return False

        self.explorer.energy -= cost
        self.year += years
        self.explorer.stability -= max(
            1,
            abs(years) // 100
        )
        self.score += abs(years) // 5
        return True

    def study_rift(self):
        if self.explorer.energy < 15:
            return False

        self.explorer.energy -= 15
        self.explorer.knowledge += 20
        self.score += 50
        return True

    def collect_artifact(self):
        if self.explorer.knowledge < 20:
            return False

        self.explorer.knowledge -= 20
        self.artifacts += 1
        self.score += 100
        return True

    def close_rift(self):
        if self.explorer.stability < 20:
            return False

        self.explorer.stability -= 10
        self.rifts_closed += 1
        self.score += 150
        return True

    def stabilize(self):
        self.explorer.stability = min(
            100,
            self.explorer.stability + 20
        )
        self.explorer.energy = min(
            100,
            self.explorer.energy + 20
        )

    def return_home(self):
        if self.year != 2026:
            return False

        self.returned = True
        self.score += 500
        return True

    def status(self):
        return {
            "explorer": self.explorer.name,
            "year": self.year,
            "energy": self.explorer.energy,
            "stability": self.explorer.stability,
            "knowledge": self.explorer.knowledge,
            "artifacts": self.artifacts,
            "rifts_closed": self.rifts_closed,
            "score": self.score,
            "returned": self.returned,
        }


def create_game():
    return TimeRiftExplorer()


if __name__ == "__main__":
    game = create_game()
    game.jump(1000)
    game.study_rift()
    game.collect_artifact()
    print(game.status())
