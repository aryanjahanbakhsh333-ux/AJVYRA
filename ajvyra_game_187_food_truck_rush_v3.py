from dataclasses import dataclass


@dataclass
class FoodTruck:
    name: str
    money: int = 100
    reputation: int = 10
    fuel: int = 100
    ingredients: int = 40
    meals_served: int = 0


class FoodTruckRush:
    def __init__(self):
        self.owner = "Maya Rell"
        self.truck = FoodTruck("Midnight Bites")
        self.location = "Central Street"
        self.time = 8
        self.score = 0
        self.routes = {
            "Central Street": 20,
            "Harbor": 35,
            "Night Market": 50,
            "Old Town": 30,
        }

    def drive_to(self, location: str):
        if location not in self.routes:
            return False

        fuel_cost = self.routes[location] // 5

        if self.truck.fuel < fuel_cost:
            return False

        self.truck.fuel -= fuel_cost
        self.location = location
        self.time += 1
        return True

    def serve_customer(self, meals: int = 1):
        if meals <= 0 or self.truck.ingredients < meals:
            return False

        self.truck.ingredients -= meals
        self.truck.money += meals * 12
        self.truck.reputation += meals
        self.truck.meals_served += meals
        self.score += meals * 15
        self.time += 1

        return True

    def buy_ingredients(self, amount: int):
        cost = amount * 2

        if self.truck.money < cost:
            return False

        self.truck.money -= cost
        self.truck.ingredients += amount
        return True

    def refuel(self):
        if self.truck.money < 20:
            return False

        self.truck.money -= 20
        self.truck.fuel = min(100, self.truck.fuel + 40)
        return True

    def close_shift(self):
        bonus = self.truck.reputation * 2
        self.score += bonus
        return self.status()

    def status(self):
        return {
            "owner": self.owner,
            "truck": self.truck.name,
            "location": self.location,
            "time": self.time,
            "money": self.truck.money,
            "reputation": self.truck.reputation,
            "fuel": self.truck.fuel,
            "ingredients": self.truck.ingredients,
            "meals_served": self.truck.meals_served,
            "score": self.score,
        }


def create_game():
    return FoodTruckRush()


def demo():
    game = create_game()
    game.drive_to("Night Market")
    game.serve_customer(5)
    game.buy_ingredients(20)
    game.serve_customer(3)
    return game.close_shift()


if __name__ == "__main__":
    print(demo())
