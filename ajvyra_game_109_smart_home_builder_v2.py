"""
AJVYRA Game 109 - Smart Home Builder
Genre: Logic / Automation
"""

from dataclasses import dataclass


@dataclass
class Device:
    name: str
    state: bool = False


class SmartHomeBuilder:
    title = "Smart Home Builder"
    character = "Ivo Ray"

    def __init__(self):
        self.devices = {
            "lamp": Device("lamp"),
            "door": Device("door"),
            "alarm": Device("alarm"),
            "fan": Device("fan"),
            "heater": Device("heater"),
        }

        self.energy = 100
        self.security = 0
        self.rules = []

    def toggle(self, device):
        if device not in self.devices:
            return False

        self.devices[device].state = not self.devices[device].state
        return True

    def add_rule(self, trigger, action):
        self.rules.append(
            {
                "trigger": trigger,
                "action": action,
            }
        )

    def run_rule(self, trigger):
        executed = []

        for rule in self.rules:
            if rule["trigger"] != trigger:
                continue

            action = rule["action"]

            if action in self.devices:
                self.devices[action].state = True
                executed.append(action)

        self.update_security()
        return executed

    def update_security(self):
        door = self.devices["door"].state
        alarm = self.devices["alarm"].state

        if not door and alarm:
            self.security = 100
        elif not door:
            self.security = 50
        else:
            self.security = 10

    def consume_energy(self):
        active = sum(
            1 for device in self.devices.values()
            if device.state
        )

        self.energy = max(0, self.energy - active * 3)

    def snapshot(self):
        return {
            "builder": self.character,
            "energy": self.energy,
            "security": self.security,
            "devices": {
                name: device.state
                for name, device in self.devices.items()
            },
            "rules": list(self.rules),
        }


def create_game():
    return SmartHomeBuilder()


if __name__ == "__main__":
    game = create_game()
    game.add_rule("night", "lamp")
    game.add_rule("security", "alarm")
    game.run_rule("night")
    game.run_rule("security")
    game.consume_energy()
    print(game.snapshot())
