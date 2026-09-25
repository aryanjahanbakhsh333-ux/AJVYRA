from dataclasses import dataclass


@dataclass
class MetroLine:
    name: str
    trains: int
    passengers: int
    delay: int = 0
    efficiency: int = 70


class UndergroundMetroController:
    def __init__(self):
        self.controller = "Nora Kade"
        self.hour = 6
        self.money = 300
        self.score = 0
        self.incidents = 0
        self.lines = [
            MetroLine("Blue Line", 4, 500),
            MetroLine("Silver Line", 3, 350),
            MetroLine("Gold Line", 5, 650),
            MetroLine("Green Line", 2, 240),
        ]

    def dispatch_train(self, line_name: str):
        line = self._line(line_name)

        if line is None or line.trains <= 0:
            return False

        line.delay = max(0, line.delay - 5)
        line.efficiency = min(100, line.efficiency + 3)
        self.score += line.passengers // 10
        self.money += 20
        return True

    def reroute_passengers(self, source: str, target: str):
        source_line = self._line(source)
        target_line = self._line(target)

        if source_line is None or target_line is None:
            return False

        if target_line.efficiency < 50:
            return False

        moved = min(100, source_line.passengers // 5)
        source_line.passengers -= moved
        target_line.passengers += moved

        self.score += moved
        return True

    def repair_line(self, line_name: str):
        line = self._line(line_name)

        if line is None or self.money < 60:
            return False

        self.money -= 60
        line.delay = max(0, line.delay - 15)
        line.efficiency = min(100, line.efficiency + 12)
        self.score += 40
        return True

    def trigger_incident(self, line_name: str):
        line = self._line(line_name)

        if line is None:
            return False

        line.delay += 20
        line.efficiency = max(0, line.efficiency - 15)
        self.incidents += 1
        return True

    def next_hour(self):
        self.hour += 1

        for line in self.lines:
            line.passengers += 50
            line.delay = max(0, line.delay - 2)

        self.money += 30

    def _line(self, name):
        return next(
            (line for line in self.lines if line.name == name),
            None
        )

    def status(self):
        return {
            "controller": self.controller,
            "hour": self.hour,
            "money": self.money,
            "score": self.score,
            "incidents": self.incidents,
            "lines": {
                line.name: {
                    "trains": line.trains,
                    "passengers": line.passengers,
                    "delay": line.delay,
                    "efficiency": line.efficiency,
                }
                for line in self.lines
            },
        }


def create_game():
    return UndergroundMetroController()


if __name__ == "__main__":
    game = create_game()
    game.dispatch_train("Blue Line")
    game.reroute_passengers("Gold Line", "Silver Line")
    game.repair_line("Green Line")
    print(game.status())
