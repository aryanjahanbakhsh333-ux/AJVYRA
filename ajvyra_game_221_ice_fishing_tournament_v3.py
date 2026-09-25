from dataclasses import dataclass, field
import random


@dataclass
class Angler:
    name: str
    skill: int = 55
    patience: int = 60
    energy: int = 100
    trophies: int = 0


@dataclass
class Fish:
    name: str
    weight: float
    difficulty: int
    points: int


class IceFishingTournament:
    def __init__(self):
        self.player = Angler("Kai Frost")
        self.day = 1
        self.hole = 1
        self.time_left = 12
        self.score = 0
        self.coins = 100
        self.weather = "Clear"
        self.caught = []
        self.round_finished = False

        self.fish_pool = [
            Fish("Silver Pike", 4.2, 35, 80),
            Fish("Frozen Trout", 2.8, 45, 60),
            Fish("Blue Perch", 1.7, 25, 40),
            Fish("Winter Salmon", 6.1, 65, 120),
        ]

    def change_weather(self):
        self.weather = random.choice(
            ["Clear", "Snow", "Strong Wind", "Ice Fog"]
        )

    def move_hole(self, hole: int):
        if hole < 1 or hole > 6:
            return False
        if self.player.energy < 5:
            return False

        self.hole = hole
        self.player.energy -= 5
        return True

    def drill_hole(self):
        if self.player.energy < 10:
            return False

        self.player.energy -= 10
        self.time_left -= 1
        self.hole = min(6, self.hole + 1)
        return True

    def cast_line(self):
        if self.time_left <= 0 or self.player.energy < 8:
            return None

        self.time_left -= 1
        self.player.energy -= 8

        weather_penalty = {
            "Clear": 0,
            "Snow": 5,
            "Strong Wind": 12,
            "Ice Fog": 8,
        }[self.weather]

        chance = self.player.skill + self.player.patience - weather_penalty
        if random.randint(1, 150) > chance:
            return None

        fish = random.choice(self.fish_pool)
        catch_power = self.player.skill + random.randint(0, 35)

        if catch_power >= fish.difficulty:
            self.caught.append(fish)
            self.score += fish.points
            self.coins += fish.points // 3
            return fish.name

        self.player.energy = max(0, self.player.energy - 5)
        return "escaped"

    def warm_up(self):
        if self.coins < 15:
            return False

        self.coins -= 15
        self.player.energy = min(100, self.player.energy + 25)
        self.player.patience = min(100, self.player.patience + 10)
        return True

    def finish_tournament(self):
        if self.time_left > 0:
            self.time_left = 0

        if self.score >= 300:
            self.player.trophies += 1

        self.round_finished = True
        return self.score

    def status(self):
        return {
            "angler": self.player.name,
            "hole": self.hole,
            "weather": self.weather,
            "time_left": self.time_left,
            "energy": self.player.energy,
            "score": self.score,
            "coins": self.coins,
            "fish_caught": len(self.caught),
            "trophies": self.player.trophies,
            "finished": self.round_finished,
        }


def create_game():
    return IceFishingTournament()


if __name__ == "__main__":
    game = create_game()
    game.change_weather()
    game.drill_hole()
    game.cast_line()
    print(game.status())
