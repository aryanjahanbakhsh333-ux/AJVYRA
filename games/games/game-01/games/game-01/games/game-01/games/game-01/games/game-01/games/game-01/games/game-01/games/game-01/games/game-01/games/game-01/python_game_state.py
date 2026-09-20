class GameState:

    def __init__(self):
        self.reset()

    def reset(self):
        self.score = 0
        self.health = 100
        self.collected_orbs = 0

        self.running = True
        self.paused = False
        self.completed = False
        self.game_over = False

    def add_score(self, amount):
        self.score += max(0, amount)

    def collect_orb(self):
        self.collected_orbs += 1
        self.add_score(250)

    def damage(self, amount):
        self.health = max(
            0,
            self.health - amount
        )

        if self.health <= 0:
            self.game_over = True

    def finish(self):
        self.completed = True
        self.running = False
