from dataclasses import dataclass
import random


@dataclass
class HockeyPlayer:
    name: str
    shooting: int
    skating: int
    defense: int
    stamina: int = 100


class IceHockeyGame:
    GAME_ID = "AJVYRA-081"
    TITLE = "Frozen Legends"
    GENRE = "Ice Hockey"

    def __init__(self):
        self.team = "North Wolves"
        self.score = 0
        self.opponent_score = 0
        self.energy = 100

        self.players = [
            HockeyPlayer("Rian Frost", 88, 91, 70),
            HockeyPlayer("Vexa Snow", 82, 94, 75),
            HockeyPlayer("Kalen Ice", 75, 86, 92),
        ]

        self.puck_position = [0, 0]

    def skate(self, direction: str):
        directions = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0),
        }

        if direction not in directions or self.energy <= 0:
            return False

        dx, dy = directions[direction]
        self.puck_position[0] += dx
        self.puck_position[1] += dy
        self.energy -= 4

        return True

    def shoot(self, player_index: int):
        if player_index < 0 or player_index >= len(self.players):
            return False

        player = self.players[player_index]

        chance = (player.shooting + player.skating) / 200

        if random.random() < chance:
            self.score += 1
            return "GOAL"

        return "MISS"

    def defend(self):
        defense = sum(p.defense for p in self.players) / len(self.players)

        if random.random() < defense / 120:
            return "BLOCKED"

        self.opponent_score += 1
        return "CONCEDED"

    def recover(self):
        self.energy = min(100, self.energy + 20)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "team": self.team,
            "score": self.score,
            "opponent_score": self.opponent_score,
            "energy": self.energy,
            "puck_position": self.puck_position[:],
            "players": [p.__dict__.copy() for p in self.players],
        }
