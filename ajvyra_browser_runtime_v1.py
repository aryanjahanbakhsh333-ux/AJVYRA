from __future__ import annotations

from typing import Any, Dict
from ajvyra_game_session_api_v1 import GameSessionAPI


class AJVYRABrowserRuntime:
    def __init__(self) -> None:
        self.api = GameSessionAPI()

    def launch(self, game_id: int) -> Dict[str, Any]:
        return self.api.create(int(game_id))

    def action(
        self,
        session_id: str,
        action: str,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return self.api.action(
            session_id,
            action,
            params or {},
        )

    def state(self, session_id: str) -> Dict[str, Any]:
        return self.api.state(session_id)

    def stop(self, session_id: str) -> Dict[str, Any]:
        return self.api.stop(session_id)
