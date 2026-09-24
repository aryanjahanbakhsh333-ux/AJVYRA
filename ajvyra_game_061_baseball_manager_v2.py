from dataclasses import dataclass, field
from typing import List, Dict
import random


@dataclass
class BaseballPlayer:
    name: str
    position: str
    batting: int
    pitching: int
    stamina: int
    morale: int = 70


@dataclass
class BaseballTeam:
    name: str
    city: str
    players: List[BaseballPlayer]
    wins: int = 0
    losses: int = 0
    money: int = 5000


class BaseballManagerGame:
    GAME_ID = "AJVYRA-061"
    TITLE = "Diamond Dynasty"
    GENRE = "Baseball Management"
    STORY = (
        "You inherit a struggling baseball club and have one season "
        "to rebuild it into a championship contender."
    )

    def __init__(self):
        self.day = 1
        self.team = BaseballTeam(
            name="Night Owls",
            city="Nova City",
            players=[
                BaseballPlayer("Kairo Venn", "Pitcher", 55, 88, 90),
                BaseballPlayer("Mira Solen", "Catcher", 82, 60, 84),
                BaseballPlayer("Riven Holt", "Shortstop", 86, 45, 91),
                BaseballPlayer("Teya Moon", "Outfielder", 78, 52, 87),
                BaseballPlayer("Orin Vale", "First Base", 91, 20, 80),
            ],
        )

    def train_player(self, player_name: str, skill: str) -> bool:
        for player in self.team.players:
            if player.name == player_name:
                if self.team.money < 250:
                    return False

                self.team.money -= 250

                if skill == "batting":
                    player.batting = min(100, player.batting + 3)
                elif skill == "pitching":
                    player.pitching = min(100, player.pitching + 3)
                elif skill == "stamina":
                    player.stamina = min(100, player.stamina + 3)
                else:
                    return False

                player.morale = min(100, player.morale + 2)
                return True

        return False

    def play_match(self, opponent_strength: int = 70) -> Dict:
        batting_power = sum(p.batting for p in self.team.players) / len(
            self.team.players
        )

        pitching_power = sum(p.pitching for p in self.team.players) / len(
            self.team.players
        )

        team_power = (batting_power * 0.6) + (pitching_power * 0.4)
        chance = max(0.15, min(0.85, 0.5 + (team_power - opponent_strength) / 200))

        won = random.random() < chance

        if won:
            self.team.wins += 1
            self.team.money += 750
            result = "WIN"
        else:
            self.team.losses += 1
            self.team.money += 250
            result = "LOSS"

        self.day += 1

        for player in self.team.players:
            player.stamina = max(20, player.stamina - random.randint(2, 7))

        return {
            "result": result,
            "day": self.day,
            "wins": self.team.wins,
            "losses": self.team.losses,
            "money": self.team.money,
        }

    def rest_team(self):
        for player in self.team.players:
            player.stamina = min(100, player.stamina + 15)
            player.morale = min(100, player.morale + 5)

        self.day += 1

    def get_state(self) -> Dict:
        return {
            "game_id": self.GAME_ID,
            "title": self.TITLE,
            "day": self.day,
            "team": self.team.name,
            "wins": self.team.wins,
            "losses": self.team.losses,
            "money": self.team.money,
            "players": [
                {
                    "name": p.name,
                    "position": p.position,
                    "batting": p.batting,
                    "pitching": p.pitching,
                    "stamina": p.stamina,
                    "morale": p.morale,
                }
                for p in self.team.players
            ],
        }
