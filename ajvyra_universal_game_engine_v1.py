"""
AJVYRA Universal Game Engine v1
Core lifecycle for all AJVYRA games.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import time
import uuid


@dataclass
class GameSession:
    session_id: str
    game_id: int
    created_at: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    running: bool = True
    state: Dict[str, Any] = field(default_factory=dict)


class UniversalGameEngine:
    VERSION = "1.0"

    def __init__(self) -> None:
        self.sessions: Dict[str, GameSession] = {}

    def create_session(
        self,
        game_id: int,
        initial_state: Optional[Dict[str, Any]] = None,
    ) -> GameSession:
        session = GameSession(
            session_id=uuid.uuid4().hex,
            game_id=int(game_id),
            state=dict(initial_state or {}),
        )
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[GameSession]:
        return self.sessions.get(session_id)

    def update_state(
        self,
        session_id: str,
        changes: Dict[str, Any],
    ) -> GameSession:
        session = self._require_session(session_id)

        if not session.running:
            raise RuntimeError("Game session is no longer running.")

        session.state.update(changes)
        session.last_update = time.time()
        return session

    def stop_session(self, session_id: str) -> None:
        session = self._require_session(session_id)
        session.running = False
        session.last_update = time.time()

    def remove_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)

    def snapshot(self, session_id: str) -> Dict[str, Any]:
        session = self._require_session(session_id)

        return {
            "session_id": session.session_id,
            "game_id": session.game_id,
            "created_at": session.created_at,
            "last_update": session.last_update,
            "running": session.running,
            "state": dict(session.state),
        }

    def _require_session(self, session_id: str) -> GameSession:
        session = self.get_session(session_id)

        if session is None:
            raise KeyError(f"Unknown game session: {session_id}")

        return session
