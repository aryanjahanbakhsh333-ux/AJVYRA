from dataclasses import dataclass
import random


@dataclass
class WordQuest:
    word: str
    clue: str
    reward: int


class WordAdventureGame:
    GAME_ID = "AJVYRA-067"
    TITLE = "The Library of Lost Words"
    GENRE = "Educational Word Adventure"

    def __init__(self):
        self.hero = "Lio"
        self.points = 0
        self.level = 1

        self.quests = [
            WordQuest("planet", "A world orbiting a star.", 20),
            WordQuest("forest", "A large area filled with trees.", 25),
            WordQuest("gravity", "The force that pulls objects downward.", 30),
            WordQuest("ocean", "A huge body of salt water.", 20),
        ]

        random.shuffle(self.quests)

    def answer(self, answer: str):
        if not self.quests:
            return {"complete": True}

        quest = self.quests[0]

        if answer.strip().lower() == quest.word:
            self.points += quest.reward
            self.level = 1 + self.points // 100
            self.quests.pop(0)
            return {
                "correct": True,
                "reward": quest.reward,
                "points": self.points,
            }

        self.points = max(0, self.points - 5)

        return {
            "correct": False,
            "points": self.points,
        }

    def current_question(self):
        if not self.quests:
            return None

        quest = self.quests[0]

        return {
            "clue": quest.clue,
            "reward": quest.reward,
        }

    def state(self):
        return {
            "game_id": self.GAME_ID,
            "hero": self.hero,
            "level": self.level,
            "points": self.points,
            "remaining_questions": len(self.quests),
        }
