from dataclasses import dataclass


@dataclass
class Conductor:
    name: str
    energy: int = 100
    reputation: int = 20
    passengers: int = 40
    tickets: int = 0


class MagicTrainConductor:
    def __init__(self):
        self.conductor = Conductor("Elias Rune")
        self.station = "Moon Station"
        self.day = 1
        self.score = 0
        self.route_progress = 0

    def depart(self, destination: str):
        routes = {
            "Moon Station": 0,
            "Crystal Station": 20,
            "Storm Station": 40,
            "Dragon Station": 60,
        }

        if destination not in routes:
            return False

        cost = max(5, routes[destination] // 4)

        if self.conductor.energy < cost:
            return False

        self.conductor.energy -= cost
        self.station = destination
        self.route_progress += 1
        self.score += routes[destination]
        return True

    def check_tickets(self, amount: int):
        if amount <= 0 or amount > self.conductor.passengers:
            return False

        self.conductor.passengers -= amount
        self.conductor.tickets += amount
        self.conductor.reputation += amount // 5
        self.score += amount * 5
        return True

    def use_magic_signal(self):
        if self.conductor.energy < 15:
            return False

        self.conductor.energy -= 15
        self.route_progress += 1
        self.score += 40
        return True

    def rest(self):
        self.day += 1
        self.conductor.energy = min(
            100,
            self.conductor.energy + 30
        )

    def complete_route(self):
        return self.route_progress >= 5

    def status(self):
        return {
            "conductor": self.conductor.name,
            "station": self.station,
            "day": self.day,
            "energy": self.conductor.energy,
            "passengers": self.conductor.passengers,
            "tickets": self.conductor.tickets,
            "reputation": self.conductor.reputation,
            "route_progress": self.route_progress,
            "score": self.score,
            "route_complete": self.complete_route(),
        }


def create_game():
    return MagicTrainConductor()


def demo():
    game = create_game()

    game.depart("Crystal Station")
    game.check_tickets(10)
    game.use_magic_signal()
    game.depart("Storm Station")
    game.use_magic_signal()
    game.depart("Dragon Station")

    return game.status()


if __name__ == "__main__":
    print(demo())
