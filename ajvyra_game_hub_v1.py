"""
AJVYRA Game Hub v1

Main entry point for the 300-game catalog/runtime layer.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ajvyra_game_catalog_v1 import AJVYRAGameCatalog
from ajvyra_game_session_api_v1 import GameSessionAPI


class AJVYRAGameHub:
    NAME = "AJVYRA Game Hub"
    TARGET_GAMES = 300

    def __init__(self) -> None:
        self.catalog = AJVYRAGameCatalog()
        self.api = GameSessionAPI()

    def catalog_data(self) -> Dict[str, Any]:
        games = self.catalog.all_games()

        return {
            "hub": self.NAME,
            "target_games": self.TARGET_GAMES,
            "available_games": len(games),
            "games": games,
        }

    def launch(self, game_id: int) -> Dict[str, Any]:
        return self.api.create(game_id)

    def send_action(
        self,
        session_id: str,
        action: str,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return self.api.action(
            session_id=session_id,
            action=action,
            params=params,
        )

    def status(self) -> Dict[str, Any]:
        return {
            "target": self.TARGET_GAMES,
            "catalog": self.catalog.summary(),
        }


def create_hub() -> AJVYRAGameHub:
    return AJVYRAGameHub()


if __name__ == "__main__":
    hub = create_hub()

    print("AJVYRA GAME HUB")
    print("=" * 40)
    print(hub.status())
