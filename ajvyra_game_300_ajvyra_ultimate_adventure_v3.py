from dataclasses import dataclass


@dataclass
class Hero:
    name: str
    health: int = 100
    stamina: int = 100
    energy: int = 100
    strength: int = 60
    intelligence: int = 60


class AJVYRAUltimateAdventure:
    def __init__(self):
        self.hero = Hero("AJ")
        self.chapter = 1
        self.location = "Black Horizon"
        self.score = 0
        self.gold = 100
        self.keys = 0
        self.artifacts = 0
        self.enemies_defeated = 0
        self.puzzles_solved = 0
        self.path = []
        self.final_gate_open = False
        self.completed = False

    def explore(self, location: str):
        locations = {
            "Black Horizon": 20,
            "Crystal Valley": 40,
            "Silent Forest": 60,
            "Neon Ruins": 80,
            "Sky Citadel": 120,
        }

        if location not in locations:
            return False

        self.location = location
        self.path.append(location)
        self.score += locations[location]
        return True

    def attack(self):
        if self.hero.stamina < 15:
            return False

        self.hero.stamina -= 15
        self.enemies_defeated += 1
        self.gold += 35
        self.score += 90
        return True

    def powerful_strike(self):
        if self.hero.energy < 25:
            return False

        self.hero.energy -= 25
        self.enemies_defeated += 1
        self.score += 180
        self.gold += 60
        return True

    def solve_puzzle(self):
        if self.hero.energy < 10:
            return False

        self.hero.energy -= 10
        self.puzzles_solved += 1
        self.keys += 1
        self.score += 140
        return True

    def collect_artifact(self):
        self.artifacts += 1
        self.score += 200
        self.gold += 100
        return True

    def recover(self):
        self.hero.health = min(
            100,
            self.hero.health + 25
        )
        self.hero.stamina = min(
            100,
            self.hero.stamina + 30
        )
        self.hero.energy = min(
            100,
            self.hero.energy + 25
        )

    def open_final_gate(self):
        if (
            self.keys >= 3
            and self.artifacts >= 3
            and self.enemies_defeated >= 3
        ):
            self.final_gate_open = True
            self.score += 500
            return True

        return False

    def enter_final_chamber(self):
        if not self.final_gate_open:
            return False

        self.location = "AJVYRA Core"
        self.chapter = 5
        self.score += 300
        return True

    def complete_adventure(self):
        if self.location != "AJVYRA Core":
            return False

        self.completed = True
        self.score += 1000
        return True

    def status(self):
        return {
            "hero": self.hero.name,
            "chapter": self.chapter,
            "location": self.location,
            "health": self.hero.health,
            "stamina": self.hero.stamina,
            "energy": self.hero.energy,
            "gold": self.gold,
            "keys": self.keys,
            "artifacts": self.artifacts,
            "enemies_defeated": self.enemies_defeated,
            "puzzles_solved": self.puzzles_solved,
            "score": self.score,
            "final_gate_open": self.final_gate_open,
            "completed": self.completed,
            "path": self.path,
        }


def create_game():
    return AJVYRAUltimateAdventure()


if __name__ == "__main__":
    game = create_game()

    game.explore("Crystal Valley")
    game.solve_puzzle()
    game.explore("Silent Forest")
    game.attack()
    game.collect_artifact()

    print(game.status())
