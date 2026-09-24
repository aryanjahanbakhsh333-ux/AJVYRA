"""
AJVYRA Game 101 - Siege Commander
Genre: Tactical Siege Strategy
"""

from dataclasses import dataclass, field
from random import randint


@dataclass
class Commander:
    name: str
    morale: int = 100
    supplies: int = 100
    troops: int = 120
    reputation: int = 0


@dataclass
class SiegeState:
    wall_integrity: int = 100
    enemy_morale: int = 100
    day: int = 1
    victory: bool = False
    defeat: bool = False
    log: list[str] = field(default_factory=list)


class SiegeCommander:
    title = "Siege Commander"
    character = "Kael Veyron"

    def __init__(self):
        self.commander = Commander(self.character)
        self.state = SiegeState()

    def prepare(self):
        self.commander.supplies += 15
        self.commander.morale += 5
        self.state.log.append("The army prepares before sunrise.")

    def bombard(self):
        if self.commander.supplies < 12:
            self.state.log.append("Not enough supplies.")
            return

        self.commander.supplies -= 12
        damage = randint(10, 20)
        self.state.wall_integrity = max(0, self.state.wall_integrity - damage)
        self.state.enemy_morale = max(
            0, self.state.enemy_morale - randint(5, 12)
        )
        self.state.log.append(f"Heavy bombardment dealt {damage} damage.")

    def negotiate(self):
        chance = randint(1, 100)

        if chance <= 35:
            self.state.enemy_morale = max(
                0, self.state.enemy_morale - 20
            )
            self.commander.reputation += 10
            self.state.log.append("The enemy commander begins negotiating.")
        else:
            self.state.log.append("Negotiations failed.")

    def assault(self):
        if self.commander.troops < 15:
            self.state.log.append("Too few troops for an assault.")
            return

        self.commander.troops -= randint(8, 18)

        if self.state.wall_integrity <= 35:
            self.state.enemy_morale = max(
                0, self.state.enemy_morale - randint(20, 35)
            )
            self.state.log.append("The assault breaks through the defenses.")
        else:
            self.commander.morale -= 10
            self.state.log.append("The assault was repelled.")

    def next_day(self):
        self.state.day += 1
        self.commander.supplies = max(0, self.commander.supplies - 5)

        if self.commander.supplies == 0:
            self.commander.morale -= 15

        self.check_end()

    def check_end(self):
        if self.state.enemy_morale <= 0 or self.state.wall_integrity <= 0:
            self.state.victory = True

        if self.commander.morale <= 0 or self.commander.troops <= 0:
            self.state.defeat = True

    def command(self, action):
        actions = {
            "prepare": self.prepare,
            "bombard": self.bombard,
            "negotiate": self.negotiate,
            "assault": self.assault,
            "next_day": self.next_day,
        }

        action = action.lower().strip()

        if action in actions and not self.state.victory and not self.state.defeat:
            actions[action]()
            self.check_end()

    def snapshot(self):
        return {
            "day": self.state.day,
            "wall": self.state.wall_integrity,
            "enemy_morale": self.state.enemy_morale,
            "troops": self.commander.troops,
            "supplies": self.commander.supplies,
            "morale": self.commander.morale,
            "victory": self.state.victory,
            "defeat": self.state.defeat,
        }


def create_game():
    return SiegeCommander()


if __name__ == "__main__":
    game = create_game()
    game.command("prepare")
    game.command("bombard")
    print(game.snapshot())
