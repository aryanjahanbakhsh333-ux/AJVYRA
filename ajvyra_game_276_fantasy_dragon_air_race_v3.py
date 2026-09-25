from dataclasses import dataclass


@dataclass
class Dragon:
    name: str
    speed: int = 75
    agility: int = 70
    stamina: int = 100
    flame_power: int = 60


class FantasyDragonAirRace:
    def __init__(self):
        self.rider = "Aren Sky"
        self.dragon = Dragon("Veyron")
        self.distance = 0
        self.goal = 2200
        self.altitude = 500
        self.score = 0
        self.combo = 0
        self.finished = False

    def fly(self):
        if self.dragon.stamina < 10:
            return False

        self.dragon.stamina -= 10
        self.distance += self.dragon.speed
        self.altitude += 20
        self.score += 20
        return True

    def aerial_turn(self):
        if self.dragon.stamina < 12:
            return False

        self.dragon.stamina -= 12

        if self.dragon.agility >= 65:
            self.combo += 1
            self.distance += 100
            self.score += 45 * self.combo
            return True

        self.combo = 0
        return False

    def flame_burst(self):
        if self.dragon.stamina < 18:
            return False

        self.dragon.stamina -= 18
        self.score += self.dragon.flame_power
        self.combo += 1
        return True

    def glide(self):
        self.dragon.stamina = min(
            100,
            self.dragon.stamina + 20
        )
        self.altitude = max(
            200,
            self.altitude - 40
        )

    def finish_race(self):
        if self.distance < self.goal:
            return False

        self.finished = True
        self.score += 450
        return True

    def status(self):
        return {
            "rider": self.rider,
            "dragon": self.dragon.name,
            "distance": self.distance,
            "goal": self.goal,
            "altitude": self.altitude,
            "stamina": self.dragon.stamina,
            "combo": self.combo,
            "score": self.score,
            "finished": self.finished,
        }


def create_game():
    return FantasyDragonAirRace()


if __name__ == "__main__":
    game = create_game()
    game.fly()
    game.aerial_turn()
    game.flame_burst()
    print(game.status())
