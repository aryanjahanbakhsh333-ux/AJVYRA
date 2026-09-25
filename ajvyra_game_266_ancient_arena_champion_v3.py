from dataclasses import dataclass


@dataclass
class Gladiator:
    name: str
    health: int = 100
    stamina: int = 100
    attack: int = 65
    defense: int = 50
    victories: int = 0


class AncientArenaChampion:
    def __init__(self):
        self.gladiator = Gladiator("Cassian Vale")
        self.opponent_health = 130
        self.opponent_attack = 30
        self.round = 1
        self.gold = 100
        self.score = 0
        self.champion = False

    def strike(self):
        if self.gladiator.stamina < 12:
            return False

        self.gladiator.stamina -= 12
        damage = self.gladiator.attack
        self.opponent_health -= damage
        self.score += damage
        return True

    def defend(self):
        if self.gladiator.stamina < 8:
            return False

        self.gladiator.stamina -= 8
        self.gladiator.defense += 8
        self.score += 15
        return True

    def heavy_strike(self):
        if self.gladiator.stamina < 25:
            return False

        self.gladiator.stamina -= 25
        damage = self.gladiator.attack + 25
        self.opponent_health -= damage
        self.score += damage * 2
        return True

    def recover(self):
        self.gladiator.stamina = min(
            100,
            self.gladiator.stamina + 25
        )

    def opponent_turn(self):
        if self.opponent_health <= 0:
            return

        damage = max(
            5,
            self.opponent_attack - self.gladiator.defense // 5
        )
        self.gladiator.health -= damage

    def check_champion(self):
        if self.opponent_health <= 0:
            self.gladiator.victories += 1
            self.gold += 100
            self.score += 250

            if self.gladiator.victories >= 3:
                self.champion = True

            return "victory"

        if self.gladiator.health <= 0:
            return "defeat"

        return "ongoing"

    def status(self):
        return {
            "gladiator": self.gladiator.name,
            "health": self.gladiator.health,
            "stamina": self.gladiator.stamina,
            "opponent_health": self.opponent_health,
            "victories": self.gladiator.victories,
            "gold": self.gold,
            "score": self.score,
            "champion": self.champion,
        }


def create_game():
    return AncientArenaChampion()


if __name__ == "__main__":
    game = create_game()
    game.strike()
    game.opponent_turn()
    game.defend()
    print(game.status())
