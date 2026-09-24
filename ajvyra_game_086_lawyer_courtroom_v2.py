from dataclasses import dataclass


@dataclass
class Evidence:
    name: str
    strength: int
    discovered: bool = False


class CourtroomGame:
    GAME_ID = "AJVYRA-086"
    TITLE = "The Final Argument"
    GENRE = "Courtroom Strategy"

    def __init__(self):
        self.lawyer = "Aren Cross"
        self.case_score = 0
        self.time = 100
        self.evidence = [
            Evidence("Security Footage", 30),
            Evidence("Witness Statement", 20),
            Evidence("Digital Record", 35),
            Evidence("Timeline", 25),
        ]

    def investigate(self, index: int):
        if index < 0 or index >= len(self.evidence):
            return False

        evidence = self.evidence[index]

        if evidence.discovered or self.time < 10:
            return False

        evidence.discovered = True
        self.case_score += evidence.strength
        self.time -= 10

        return True

    def present_argument(self):
        discovered = sum(
            1 for evidence in self.evidence if evidence.discovered
        )

        if discovered >= 3:
            self.case_score += 50
            return "STRONG_ARGUMENT"

        return "WEAK_ARGUMENT"

    def verdict(self):
        if self.case_score >= 100:
            return "CASE_SUPPORTED"

        return "CASE_UNCERTAIN"

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "lawyer": self.lawyer,
            "case_score": self.case_score,
            "time": self.time,
            "evidence": [e.__dict__.copy() for e in self.evidence],
            "verdict": self.verdict(),
        }
