"""
AJVYRA Game Session API v1

Framework-neutral service layer.
A web framework can call this service without knowing
the internals of individual games.
"""

from __future__ import annotations

from typing import Any, Dict

from ajvyra_game_catalog_v1 import AJVYRAGameCatalog
from ajvyra_game_runtime_adapter_v1 import GameRuntimeAdapter
from ajvyra_game_state_manager_v1 import GameStateManager
from ajvyra_universal_game_engine_v1 import UniversalGameEngine


class GameSessionAPI:
    def __init__(self) -> None:
        self.engine = UniversalGameEngine()
        self.catalog = AJVYRAGameCatalog()
        self.states = GameStateManager()
        self.adapters: Dict[str, GameRuntimeAdapter] = {}

    def create(self, game_id: int) -> Dict[str, Any]:
        discovered = self.catalog.loader.find_game(game_id)

        if discovered is None:
            return {
                "ok": False,
                "error": f"Game {game_id} was not found.",
            }

        adapter = GameRuntimeAdapter(discovered)
        session = self.engine.create_session(game_id)

        self.adapters[session.session_id] = adapter

        initial = adapter.start()
        session.state = initial

        return {
            "ok": True,
            "session": self.engine.snapshot(
                session.session_id
            ),
            "game": self.catalog.get(game_id),
        }

    def action(
        self,
        session_id: str,
        action: str,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        adapter = self.adapters.get(session_id)

        if adapter is None:
            return {
                "ok": False,
                "error": "Unknown session.",
            }

        result = adapter.action(
            action,
            **(params or {}),
        )

        self.engine.update_state(
            session_id,
            result.get("state", {}),
        )

        self.states.save(
            session_id,
            self.engine.snapshot(session_id),
        )

        return result

    def state(self, session_id: str) -> Dict[str, Any]:
        return self.engine.snapshot(session_id)

    def stop(self, session_id: str) -> Dict[str, Any]:
        self.engine.stop_session(session_id)

        self.states.save(
            session_id,
            self.engine.snapshot(session_id),
        )

        return {
            "ok": True,
            "session": self.engine.snapshot(session_id),
        }
