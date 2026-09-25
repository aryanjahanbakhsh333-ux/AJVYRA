"""
AJVYRA Game State Manager v1
JSON-compatible state persistence.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional


class GameStateManager:
    def __init__(self, directory: str = "ajvyra_game_states") -> None:
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def _path(self, session_id: str) -> str:
        safe_id = "".join(
            char for char in session_id
            if char.isalnum() or char in "-_"
        )

        return os.path.join(
            self.directory,
            f"{safe_id}.json",
        )

    def save(
        self,
        session_id: str,
        state: Dict[str, Any],
    ) -> str:
        path = self._path(session_id)

        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=2,
                default=str,
            )

        return path

    def load(
        self,
        session_id: str,
    ) -> Optional[Dict[str, Any]]:
        path = self._path(session_id)

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def delete(self, session_id: str) -> bool:
        path = self._path(session_id)

        if not os.path.exists(path):
            return False

        os.remove(path)
        return True
