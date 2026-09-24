import random


class SamuraiDuelGame:
    GAME_ID = "AJVYRA-089"
    TITLE = "Moonblade"
    GENRE = "Samurai Duel"

    def __init__(self):
        self.samurai = "Rai Kuro"
        self.health = 100
        self.enemy_health = 100
        self.stamina = 100
        self.combo = 0

    def attack(self, style: str):
        if self.stamina < 10:
            return False

        self.stamina -= 10

        attacks = {
            "quick": 12,
            "heavy": 25,
            "counter": 18,
        }

        damage = attacks.get(style)

        if damage is None:
            return False

        if random.random() < 0.15:
            damage *= 2
            self.combo += 1
        else:
            self.combo = 0

        self.enemy_health = max(0, self.enemy_health - damage)

        return damage

    def enemy_turn(self):
        if self.enemy_health <= 0:
            return "DEFEATED"

        damage = random.randint(8, 18)
        self.health = max(0, self.health - damage)

        return damage

    def recover(self):
        self.stamina = min(100, self.stamina + 25)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "samurai": self.samurai,
            "health": self.health,
            "enemy_health": self.enemy_health,
            "stamina": self.stamina,
            "combo": self.combo,
        }
