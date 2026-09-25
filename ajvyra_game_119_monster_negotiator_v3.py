"""
AJVYRA 119 — Monster Negotiator
Genre: Dialogue / Diplomacy
"""

from dataclasses import dataclass


@dataclass
class Monster:
    name: str
    fear: int
    trust: int
    anger: int
    need: str


class MonsterNegotiator:
    title = "Monster Negotiator"
    negotiator = "Cael Rowan"

    def __init__(self):
        self.monsters = [
            Monster(
                "Gorren",
                fear=60,
                trust=20,
                anger=30,
                need="food",
            ),
            Monster(
                "Veyla",
                fear=30,
                trust=35,
                anger=50,
                need="territory",
            ),
            Monster(
                "Moro",
                fear=70,
                trust=10,
                anger=60,
                need="safety",
            ),
        ]

        self.current = 0
        self.score = 0
        self.peace_deals = 0
        self.log = []

    @property
    def monster(self):
        return self.monsters[self.current]

    def speak(self, approach):
        m = self.monster

        if approach == "listen":
            m.trust += 15
            m.anger = max(0, m.anger - 10)

        elif approach == "offer":
            m.trust += 10
            m.fear = max(0, m.fear - 10)

        elif approach == "threaten":
            m.anger += 25
            m.trust = max(0, m.trust - 15)

        elif approach == "joke":
            if m.anger < 45:
                m.trust += 8
            else:
                m.anger += 10

        else:
            return False

        self.log.append(
            f"{self.negotiator} used {approach} with {m.name}."
        )
        return True

    def propose_deal(self):
        m = self.monster

        if m.trust >= 50 and m.anger <= 30:
            self.score += 150
            self.peace_deals += 1
            self.log.append(
                f"Peace agreement reached with {m.name}."
            )
            return True

        self.log.append("The monster rejected the proposal.")
        return False

    def next_monster(self):
        if self.current < len(self.monsters) - 1:
            self.current += 1
            return True
        return False

    def status(self):
        return {
            "negotiator": self.negotiator,
            "current_monster": self.monster.name,
            "fear": self.monster.fear,
            "trust": self.monster.trust,
            "anger": self.monster.anger,
            "score": self.score,
            "peace_deals": self.peace_deals,
        }


def create_game():
    return MonsterNegotiator()


if __name__ == "__main__":
    game = create_game()
    game.speak("listen")
    game.speak("offer")
    game.propose_deal()
    print(game.status())
