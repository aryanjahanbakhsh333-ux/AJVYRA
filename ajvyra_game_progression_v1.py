from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class GameProgress:
    level: int = 1
    xp: int = 0
    score: int = 0
    wins: int = 0
    losses: int = 0
    checkpoints: int = 0
    completed: bool = False


class GameProgression:
    XP_PER_LEVEL = 100

    def __init__(self):
        self.progress = GameProgress()

    def reward(
        self,
        xp: int = 0,
        score: int = 0,
    ) -> Dict[str, Any]:
        self.progress.xp += max(0, int(xp))
        self.progress.score += max(
            0,
            int(score),
        )

        while (
            self.progress.xp
            >= self.progress.level
            * self.XP_PER_LEVEL
        ):
            self.progress.level += 1

        return self.snapshot()

    def win(self) -> Dict[str, Any]:
        self.progress.wins += 1
        return self.reward(
            xp=50,
            score=100,
        )

    def lose(self) -> Dict[str, Any]:
        self.progress.losses += 1
        return self.snapshot()

    def checkpoint(self) -> Dict[str, Any]:
        self.progress.checkpoints += 1
        return self.snapshot()

    def complete(self) -> Dict[str, Any]:
        self.progress.completed = True
        return self.snapshot()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "level": self.progress.level,
            "xp": self.progress.xp,
            "score": self.progress.score,
            "wins": self.progress.wins,
            "losses": self.progress.losses,
            "checkpoints": self.progress.checkpoints,
            "completed": self.progress.completed,
        }
