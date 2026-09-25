from dataclasses import dataclass


@dataclass
class RescueBoat:
    name: str
    fuel: int = 100
    speed: int = 70
    capacity: int = 8
    condition: int = 100


class OceanRescueCoordinator:
    def __init__(self):
        self.coordinator = "Mira Tide"
        self.boat = RescueBoat("Sea Guardian")
        self.location = 0
        self.rescue_target = 1500
        self.survivors = 0
        self.score = 0
        self.radio_signal = 70
        self.mission_complete = False

    def navigate(self, distance: int = 200):
        fuel_cost = max(5, distance // 40)

        if self.boat.fuel < fuel_cost:
            return False

        self.boat.fuel -= fuel_cost
        self.location += distance
        self.score += distance // 5
        return True

    def scan_ocean(self):
        self.radio_signal = min(
            100,
            self.radio_signal + 12
        )
        self.score += 35
        return True

    def rescue(self, amount: int = 1):
        if self.location < self.rescue_target:
            return False

        if self.survivors + amount > self.boat.capacity:
            return False

        self.survivors += amount
        self.score += amount * 100
        return True

    def return_to_base(self):
        if self.survivors <= 0:
            return False

        self.location = 0
        self.boat.fuel = max(
            0,
            self.boat.fuel - 20
        )
        self.score += self.survivors * 50
        return True

    def repair(self):
        self.boat.condition = min(
            100,
            self.boat.condition + 20
        )

    def complete_mission(self):
        if self.survivors <= 0 or self.location != 0:
            return False

        self.mission_complete = True
        self.score += 500
        return True

    def status(self):
        return {
            "coordinator": self.coordinator,
            "boat": self.boat.name,
            "location": self.location,
            "fuel": self.boat.fuel,
            "condition": self.boat.condition,
            "survivors": self.survivors,
            "radio_signal": self.radio_signal,
            "score": self.score,
            "complete": self.mission_complete,
        }


def create_game():
    return OceanRescueCoordinator()


if __name__ == "__main__":
    game = create_game()
    game.navigate(400)
    game.scan_ocean()
    print(game.status())
