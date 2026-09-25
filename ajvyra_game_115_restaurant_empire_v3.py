"""
AJVYRA 115 — Restaurant Empire
Genre: Business Simulation
"""

from dataclasses import dataclass


@dataclass
class Restaurant:
    name: str
    reputation: int = 20
    money: int = 500
    staff: int = 2
    capacity: int = 12
    day: int = 1


class RestaurantEmpire:
    title = "Restaurant Empire"
    owner = "Lena March"

    def __init__(self):
        self.restaurant = Restaurant("Midnight Spoon")
        self.ingredients = 60
        self.menu = {
            "noodles": {"price": 18, "cost": 6},
            "burger": {"price": 20, "cost": 8},
            "soup": {"price": 14, "cost": 4},
        }
        self.log = []

    def hire_staff(self):
        cost = 120

        if self.restaurant.money < cost:
            return False

        self.restaurant.money -= cost
        self.restaurant.staff += 1
        self.restaurant.capacity += 5
        return True

    def buy_ingredients(self, amount):
        cost = amount * 2

        if self.restaurant.money < cost:
            return False

        self.restaurant.money -= cost
        self.ingredients += amount
        return True

    def serve_customers(self, dish, customers):
        if dish not in self.menu:
            return False

        if customers <= 0:
            return False

        customers = min(customers, self.restaurant.capacity)

        if self.ingredients < customers:
            self.log.append("Not enough ingredients.")
            return False

        data = self.menu[dish]
        revenue = customers * data["price"]
        cost = customers * data["cost"]

        self.ingredients -= customers
        self.restaurant.money += revenue - cost
        self.restaurant.reputation += min(
            10,
            customers // 2 + self.restaurant.staff,
        )

        return True

    def close_day(self):
        self.restaurant.day += 1

        operating_cost = self.restaurant.staff * 12
        self.restaurant.money = max(
            0,
            self.restaurant.money - operating_cost,
        )

        self.restaurant.reputation = min(
            100,
            self.restaurant.reputation + 1,
        )

    def status(self):
        return {
            "owner": self.owner,
            "restaurant": self.restaurant.name,
            "day": self.restaurant.day,
            "money": self.restaurant.money,
            "reputation": self.restaurant.reputation,
            "staff": self.restaurant.staff,
            "capacity": self.restaurant.capacity,
            "ingredients": self.ingredients,
        }


def create_game():
    return RestaurantEmpire()


if __name__ == "__main__":
    game = create_game()
    game.buy_ingredients(40)
    game.serve_customers("noodles", 10)
    game.close_day()
    print(game.status())
