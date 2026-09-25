"""
AJVYRA Game 108 - Weather Station
Genre: Forecasting / Management
"""

from dataclasses import dataclass
from random import randint


@dataclass
class Sensor:
    name: str
    value: int
    reliability: int


class WeatherStation:
    title = "Weather Station"
    character = "Noa Meridian"

    def __init__(self):
        self.day = 1
        self.reputation = 50
        self.energy = 100
        self.sensors = [
            Sensor("Temperature", 22, 90),
            Sensor("Humidity", 55, 85),
            Sensor("Wind", 20, 80),
            Sensor("Pressure", 1013, 95),
        ]

        self.real_weather = {
            "temperature": 24,
            "humidity": 58,
            "wind": 23,
            "pressure": 1010,
        }

    def calibrate(self, sensor_name):
        for sensor in self.sensors:
            if sensor.name.lower() == sensor_name.lower():
                if self.energy < 10:
                    return False

                self.energy -= 10
                sensor.reliability = min(
                    100, sensor.reliability + 5
                )
                return True

        return False

    def collect_data(self):
        if self.energy < 5:
            return False

        self.energy -= 5

        for sensor in self.sensors:
            sensor.value += randint(-2, 2)

        return True

    def forecast(self):
        predicted = {
            "temperature": self.sensors[0].value,
            "humidity": self.sensors[1].value,
            "wind": self.sensors[2].value,
            "pressure": self.sensors[3].value,
        }

        accuracy = self.forecast_accuracy(predicted)

        if accuracy >= 75:
            self.reputation += 8
        elif accuracy < 50:
            self.reputation = max(0, self.reputation - 6)

        return {
            "prediction": predicted,
            "accuracy": accuracy,
        }

    def forecast_accuracy(self, predicted):
        errors = [
            abs(predicted["temperature"] - self.real_weather["temperature"]),
            abs(predicted["humidity"] - self.real_weather["humidity"]),
            abs(predicted["wind"] - self.real_weather["wind"]),
            abs(predicted["pressure"] - self.real_weather["pressure"]),
        ]

        score = 100 - sum(errors) * 2
        return max(0, min(100, score))

    def next_day(self):
        self.day += 1
        self.energy = min(100, self.energy + 30)

    def snapshot(self):
        return {
            "scientist": self.character,
            "day": self.day,
            "reputation": self.reputation,
            "energy": self.energy,
            "sensors": [
                {
                    "name": s.name,
                    "value": s.value,
                    "reliability": s.reliability,
                }
                for s in self.sensors
            ],
        }


def create_game():
    return WeatherStation()


if __name__ == "__main__":
    game = create_game()
    game.collect_data()
    print(game.forecast())
    print(game.snapshot())
