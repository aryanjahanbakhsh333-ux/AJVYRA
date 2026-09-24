from dataclasses import dataclass


@dataclass
class Aircraft:
    callsign: str
    altitude: int
    target_altitude: int
    speed: int
    landed: bool = False


class AirTrafficPilotGame:
    GAME_ID = "AJVYRA-080"
    TITLE = "Sky Control"
    GENRE = "Air Traffic Management"

    def __init__(self):
        self.controller = "Ari Venn"
        self.score = 0
        self.errors = 0

        self.aircraft = [
            Aircraft("AJ-101", 8000, 3000, 450),
            Aircraft("AJ-202", 6500, 2500, 420),
            Aircraft("AJ-303", 10000, 4000, 500),
        ]

    def change_altitude(self, index: int, altitude: int):
        if index < 0 or index >= len(self.aircraft):
            return False

        aircraft = self.aircraft[index]

        if not 1000 <= altitude <= 12000:
            self.errors += 1
            return False

        aircraft.target_altitude = altitude

        difference = abs(aircraft.altitude - altitude)
        aircraft.altitude = altitude

        if difference < 3000:
            self.score += 15
        else:
            self.score += 5

        return True

    def land(self, index: int):
        if index < 0 or index >= len(self.aircraft):
            return False

        aircraft = self.aircraft[index]

        if aircraft.altitude > 4000:
            self.errors += 1
            return False

        aircraft.landed = True
        self.score += 50
        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "controller": self.controller,
            "score": self.score,
            "errors": self.errors,
            "aircraft": [a.__dict__.copy() for a in self.aircraft],
        }
