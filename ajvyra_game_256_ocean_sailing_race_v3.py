from dataclasses import dataclass


@dataclass
class Sailboat:
    name: str
    speed: int = 65
    handling: int = 60
    sail_condition: int = 100
    stamina: int = 100


class OceanSailingRace:
    def __init__(self):
        self.captain = "Mira Wave"
        self.boat = Sailboat("Blue Horizon")
        self.distance = 0
        self.goal = 2000
        self.wind = 60
        self.score = 0
        self.money = 150
        self.finished = False

    def sail(self):
        if self.boat.stamina < 10:
            return False

        self.boat.stamina -= 10
        progress = self.boat.speed + self.wind // 3
        self.distance += progress
        self.boat.sail_condition -= 2
        self.score += progress // 2
        return True

    def adjust_sails(self):
        if self.boat.stamina < 8:
            return False

        self.boat.stamina -= 8
        self.wind += 5
        self.boat.sail_condition = min(
            100,
            self.boat.sail_condition + 3
        )
        self.score += 25
        return True

    def turn_with_waves(self):
        if self.boat.handling < 50:
            self.boat.sail_condition -= 10
            return False

        self.distance += 100
        self.score += 45
        return True

    def repair(self):
        if self.money < 50:
            return False

        self.money -= 50
        self.boat.sail_condition = min(
            100,
            self.boat.sail_condition + 25
        )
        return True

    def finish_race(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 400
        self.money += 250
        return True

    def status(self):
        return {
            "captain": self.captain,
            "boat": self.boat.name,
            "distance": self.distance,
            "goal": self.goal,
            "wind": self.wind,
            "stamina": self.boat.stamina,
            "sail_condition": self.boat.sail_condition,
            "score": self.score,
            "money": self.money,
            "finished": self.finished,
        }


def create_game():
    return OceanSailingRace()


if __name__ == "__main__":
    game = create_game()
    game.sail()
    game.adjust_sails()
    game.turn_with_waves()
    print(game.status())
