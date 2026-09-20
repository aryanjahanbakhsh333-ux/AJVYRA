import random


class ScreenShake:

    def __init__(self):

        self.amount = 0

    def trigger(self, amount=8):

        self.amount = max(
            self.amount,
            amount
        )

    def update(self):

        if self.amount > 0:

            self.amount -= 1

    def offset(self):

        if self.amount <= 0:

            return 0, 0

        return (
            random.randint(
                -self.amount,
                self.amount
            ),
            random.randint(
                -self.amount,
                self.amount
            )
        )
