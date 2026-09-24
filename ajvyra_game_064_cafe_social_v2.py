from dataclasses import dataclass
import random


@dataclass
class Customer:
    name: str
    favorite: str
    patience: int
    happiness: int = 50


class CafeSocialGame:
    GAME_ID = "AJVYRA-064"
    TITLE = "Midnight Café"
    GENRE = "Social Café Simulation"

    def __init__(self):
        self.money = 1000
        self.reputation = 20
        self.day = 1

        self.customers = [
            Customer("Mira", "latte", 70),
            Customer("Kael", "tea", 60),
            Customer("Nora", "cake", 80),
            Customer("Zane", "espresso", 55),
        ]

        self.menu = {
            "latte": 12,
            "tea": 8,
            "cake": 15,
            "espresso": 10,
        }

    def serve(self, customer_index: int, item: str):
        if customer_index >= len(self.customers):
            return False

        customer = self.customers[customer_index]

        if item not in self.menu:
            return False

        if item == customer.favorite:
            customer.happiness = min(100, customer.happiness + 25)
            self.reputation += 3
        else:
            customer.happiness = max(0, customer.happiness - 10)
            self.reputation -= 1

        self.money += self.menu[item]
        customer.patience = max(0, customer.patience - random.randint(5, 15))

        return True

    def end_day(self):
        bonus = max(0, self.reputation * 5)
        self.money += bonus
        self.day += 1

        for customer in self.customers:
            customer.patience = min(100, customer.patience + 20)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "day": self.day,
            "money": self.money,
            "reputation": self.reputation,
            "customers": [
                {
                    "name": c.name,
                    "favorite": c.favorite,
                    "patience": c.patience,
                    "happiness": c.happiness,
                }
                for c in self.customers
            ],
        }
