from dataclasses import dataclass
import random


@dataclass
class Road:
    name: str
    traffic: int
    green: bool = False


class TrafficControllerGame:
    GAME_ID = "AJVYRA-069"
    TITLE = "City Flow"
    GENRE = "Traffic Management"

    def __init__(self):
        self.score = 0
        self.penalties = 0
        self.time = 0

        self.roads = [
            Road("North Avenue", 45),
            Road("East Boulevard", 70),
            Road("South Street", 30),
            Road("West Highway", 85),
        ]

    def change_light(self, road_index: int):
        if road_index < 0 or road_index >= len(self.roads):
            return False

        for i, road in enumerate(self.roads):
            road.green = i == road_index

        return True

    def tick(self):
        self.time += 1

        for road in self.roads:
            if road.green:
                road.traffic = max(0, road.traffic - random.randint(8, 18))
                self.score += 10
            else:
                road.traffic += random.randint(2, 8)

                if road.traffic > 100:
                    self.penalties += 1
                    road.traffic = 100

        return self.state()

    def emergency_clear(self, road_index: int):
        if road_index < 0 or road_index >= len(self.roads):
            return False

        road = self.roads[road_index]
        road.traffic = max(0, road.traffic - 35)
        self.score += 25
        return True

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "score": self.score,
            "penalties": self.penalties,
            "time": self.time,
            "roads": [road.__dict__.copy() for road in self.roads],
        }
