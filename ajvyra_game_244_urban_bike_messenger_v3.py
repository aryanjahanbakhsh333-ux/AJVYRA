from dataclasses import dataclass


@dataclass
class MessengerBike:
    name: str
    speed: int = 60
    handling: int = 65
    stamina: int = 100
    condition: int = 100


class UrbanBikeMessenger:
    def __init__(self):
        self.messenger = "Jace Rowan"
        self.bike = MessengerBike("Night Runner")
        self.city_zone = "Central"
        self.money = 80
        self.reputation = 10
        self.score = 0
        self.deliveries = 0
        self.combo = 0

    def ride(self, distance: int):
        if distance <= 0:
            return False

        stamina_cost = max(5, distance // 8)

        if self.bike.stamina < stamina_cost:
            return False

        self.bike.stamina -= stamina_cost
        self.bike.condition = max(
            0,
            self.bike.condition - distance // 100
        )
        self.score += distance // 2
        return True

    def shortcut(self):
        if self.bike.stamina < 15:
            return False

        self.bike.stamina -= 15

        if self.bike.handling >= 60:
            self.score += 50
            self.combo += 1
            return True

        self.bike.condition = max(0, self.bike.condition - 15)
        self.combo = 0
        return False

    def deliver_package(self):
        if self.bike.stamina < 10:
            return False

        self.bike.stamina -= 10
        self.deliveries += 1
        self.combo += 1

        reward = 35 + self.combo * 10
        self.money += reward
        self.reputation += 3
        self.score += reward
        return True

    def repair_bike(self):
        if self.money < 40:
            return False

        self.money -= 40
        self.bike.condition = min(100, self.bike.condition + 30)
        return True

    def rest(self):
        self.bike.stamina = min(100, self.bike.stamina + 35)

    def status(self):
        return {
            "messenger": self.messenger,
            "bike": self.bike.name,
            "stamina": self.bike.stamina,
            "condition": self.bike.condition,
            "money": self.money,
            "reputation": self.reputation,
            "deliveries": self.deliveries,
            "combo": self.combo,
            "score": self.score,
        }


def create_game():
    return UrbanBikeMessenger()


if __name__ == "__main__":
    game = create_game()
    game.ride(120)
    game.shortcut()
    game.deliver_package()
    print(game.status())
