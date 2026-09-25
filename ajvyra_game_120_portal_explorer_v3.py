"""
AJVYRA 120 — Portal Explorer
Genre: Multiverse Exploration / Physics Puzzle
"""

from dataclasses import dataclass


@dataclass
class World:
    name: str
    gravity: float
    time_scale: float
    portal_cost: int
    discovered: bool = False


class PortalExplorer:
    title = "Portal Explorer"
    explorer = "Nyx Arden"

    def __init__(self):
        self.energy = 100
        self.health = 100
        self.score = 0
        self.current_world = 0

        self.worlds = [
            World(
                "Gravity Garden",
                gravity=0.5,
                time_scale=1.0,
                portal_cost=10,
            ),
            World(
                "Frozen Hour",
                gravity=1.0,
                time_scale=0.25,
                portal_cost=20,
            ),
            World(
                "Heavy Sky",
                gravity=2.0,
                time_scale=1.0,
                portal_cost=25,
            ),
            World(
                "Reverse Rain",
                gravity=-0.5,
                time_scale=1.5,
                portal_cost=30,
            ),
            World(
                "Silent Dimension",
                gravity=0.0,
                time_scale=0.5,
                portal_cost=35,
            ),
        ]

        self.worlds[0].discovered = True
        self.inventory = []
        self.log = []

    @property
    def world(self):
        return self.worlds[self.current_world]

    def enter_portal(self, world_index):
        if not 0 <= world_index < len(self.worlds):
            return False

        destination = self.worlds[world_index]

        if self.energy < destination.portal_cost:
            self.log.append("Insufficient portal energy.")
            return False

        self.energy -= destination.portal_cost
        self.current_world = world_index
        destination.discovered = True

        self.score += 50
        self.log.append(
            f"Entered {destination.name}."
        )
        return True

    def interact(self, action):
        world = self.world

        if action == "jump":
            difficulty = abs(world.gravity)

            if difficulty <= 1:
                self.score += 15
            else:
                self.health -= int(difficulty * 5)

        elif action == "observe":
            self.score += int(
                20 * world.time_scale
            )

        elif action == "collect":
            item = f"artifact_{self.current_world}"
            if item not in self.inventory:
                self.inventory.append(item)
                self.score += 40
            else:
                return False

        else:
            return False

        return True

    def recharge(self):
        self.energy = min(100, self.energy + 25)

    def all_worlds_discovered(self):
        return all(
            world.discovered
            for world in self.worlds
        )

    def status(self):
        return {
            "explorer": self.explorer,
            "world": self.world.name,
            "gravity": self.world.gravity,
            "time_scale": self.world.time_scale,
            "energy": self.energy,
            "health": self.health,
            "score": self.score,
            "inventory": list(self.inventory),
            "worlds_discovered": sum(
                world.discovered
                for world in self.worlds
            ),
            "complete": self.all_worlds_discovered(),
        }


def create_game():
    return PortalExplorer()


if __name__ == "__main__":
    game = create_game()

    for index in range(1, 5):
        game.enter_portal(index)
        game.interact("observe")

    print(game.status())
