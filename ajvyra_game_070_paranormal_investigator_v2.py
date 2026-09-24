from dataclasses import dataclass
import random


@dataclass
class Evidence:
    name: str
    strength: int
    found: bool = False


class ParanormalInvestigatorGame:
    GAME_ID = "AJVYRA-070"
    TITLE = "Whispers at 3:17"
    GENRE = "Paranormal Investigation"

    def __init__(self):
        self.investigator = "Veyra"
        self.sanity = 100
        self.battery = 100
        self.evidence_score = 0
        self.night = 1

        self.evidence = [
            Evidence("Cold Footprint", 20),
            Evidence("Broken Radio", 25),
            Evidence("Shadow Photograph", 35),
            Evidence("Unknown Voice", 30),
        ]

    def investigate(self, index: int):
        if index < 0 or index >= len(self.evidence):
            return False

        if self.battery < 10:
            return False

        self.battery -= 10

        evidence = self.evidence[index]

        if evidence.found:
            return False

        chance = random.random()

        if chance < 0.75:
            evidence.found = True
            self.evidence_score += evidence.strength
            self.sanity = max(0, self.sanity - random.randint(2, 8))
            return True

        self.sanity = max(0, self.sanity - random.randint(5, 15))
        return False

    def rest(self):
        self.battery = min(100, self.battery + 30)
        self.sanity = min(100, self.sanity + 15)
        self.night += 1

    def case_complete(self):
        return all(e.found for e in self.evidence)

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "investigator": self.investigator,
            "night": self.night,
            "sanity": self.sanity,
            "battery": self.battery,
            "evidence_score": self.evidence_score,
            "case_complete": self.case_complete(),
            "evidence": [e.__dict__.copy() for e in self.evidence],
        }
