from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List
import time


@dataclass
class GameQualityState:
    started: bool = False
    paused: bool = False
    completed: bool = False
    failed: bool = False
    score: int = 0
    level: int = 1
    elapsed: float = 0.0
    actions: int = 0
    history: List[str] = field(default_factory=list)


class GameQualityCore:
    def __init__(self, game_id: int, title: str):
        self.game_id = int(game_id)
        self.title = title
        self.state = GameQualityState()
        self.started_at = 0.0

    def start(self) -> Dict[str, Any]:
        if not self.state.started:
            self.state.started = True
            self.started_at = time.time()
            self.state.history.append("game_started")

        return self.snapshot()

    def pause(self) -> Dict[str, Any]:
        if self.state.started and not self.state.completed:
            self.state.paused = True
            self.state.history.append("paused")

        return self.snapshot()

    def resume(self) -> Dict[str, Any]:
        if self.state.started and not self.state.completed:
            self.state.paused = False
            self.state.history.append("resumed")

        return self.snapshot()

    def add_score(self, amount: int) -> None:
        if not self.state.completed and not self.state.failed:
            self.state.score = max(
                0,
                self.state.score + int(amount),
            )

    def register_action(self, name: str) -> None:
        self.state.actions += 1
        self.state.history.append(str(name))

    def complete(self) -> Dict[str, Any]:
        self.state.completed = True
        self.state.paused = False
        self.state.history.append("completed")
        self._update_elapsed()
        return self.snapshot()

    def fail(self) -> Dict[str, Any]:
        self.state.failed = True
        self.state.paused = False
        self.state.history.append("failed")
        self._update_elapsed()
        return self.snapshot()

    def tick(self) -> Dict[str, Any]:
        if self.state.started and not self.state.paused:
            self._update_elapsed()

        return self.snapshot()

    def _update_elapsed(self) -> None:
        if self.started_at:
            self.state.elapsed = max(
                0.0,
                time.time() - self.started_at,
            )

    def snapshot(self) -> Dict[str, Any]:
        self._update_elapsed()

        return {
            "game_id": self.game_id,
            "title": self.title,
            "started": self.state.started,
            "paused": self.state.paused,
            "completed": self.state.completed,
            "failed": self.state.failed,
            "score": self.state.score,
            "level": self.state.level,
            "elapsed": round(
                self.state.elapsed,
                2,
            ),
            "actions": self.state.actions,
            "history": list(
                self.state.history[-30:]
            ),
        }
