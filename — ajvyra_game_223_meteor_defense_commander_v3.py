from dataclasses import dataclass
import random


@dataclass
class Meteor:
    name: str
    size: int
    speed: int
    distance: int
    reward: int
    destroyed: bool = False


class MeteorDefenseCommander:
    def __init__(self):
        self.commander = "Aron Vey"
        self.energy = 100
        self.shield = 100
        self.credits = 250
        self.score = 0
        self.wave = 1
        self.threat_level = 0
        self.meteors = self._spawn_wave()

    def _spawn_wave(self):
        return [
            Meteor(
                f"Meteor-{i}",
                random.randint(20, 70),
                random.randint(5, 15),
                random.randint(60, 120),
                random.randint(30, 90),
            )
            for i in range(1, 5)
        ]

    def scan_sky(self):
        self.threat_level = sum(m.size for m in self.meteors if not m.destroyed)
        return self.threat_level

    def fire_interceptor(self, meteor_index: int):
        if self.energy < 15:
            return False

        if meteor_index < 0 or meteor_index >= len(self.meteors):
            return False

        meteor = self.meteors[meteor_index]
        if meteor.destroyed:
            return False

        self.energy -= 15

        accuracy = 75 - meteor.speed
        if random.randint(1, 100) <= accuracy:
            meteor.destroyed = True
            self.score += meteor.reward
            self.credits += meteor.reward // 2
            return True

        return False

    def strengthen_shield(self):
        if self.credits < 40:
            return False

        self.credits -= 40
        self.shield = min(100, self.shield + 20)
        return True

    def recharge(self):
        self.energy = min(100, self.energy + 30)

    def meteor_impact(self):
        incoming = [m for m in self.meteors if not m.destroyed]

        if not incoming:
            return 0

        damage = sum(max(5, m.size // 6) for m in incoming)
        self.shield = max(0, self.shield - damage)

        return damage

    def next_wave(self):
        if any(not m.destroyed for m in self.meteors):
            return False

        self.wave += 1
        self.meteors = self._spawn_wave()
        self.energy = min(100, self.energy + 20)
        return True

    def status(self):
        return {
            "commander": self.commander,
            "wave": self.wave,
            "energy": self.energy,
            "shield": self.shield,
            "credits": self.credits,
            "score": self.score,
            "threat": self.threat_level,
            "destroyed": sum(m.destroyed for m in self.meteors),
            "total_meteors": len(self.meteors),
        }


def create_game():
    return MeteorDefenseCommander()


if __name__ == "__main__":
    game = create_game()
    game.scan_sky()
    game.fire_interceptor(0)
    game.recharge()
    print(game.status())
