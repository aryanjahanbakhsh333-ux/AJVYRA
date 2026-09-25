"""
AJVYRA Game Catalog v1
Provides a unified catalog for discovered games.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ajvyra_game_discovery_loader_v1 import (
    GameDiscoveryLoader,
)


class AJVYRAGameCatalog:
    TOTAL_TARGET = 300

    def __init__(self) -> None:
        self.loader = GameDiscoveryLoader()

    def all_games(self) -> List[Dict[str, Any]]:
        games = self.loader.discover()

        return [
            {
                "id": game.game_id,
                "title": game.title,
                "module": game.module_name,
            }
            for game in games
        ]

    def get(self, game_id: int) -> Dict[str, Any]:
        game = self.loader.find_game(game_id)

        if game is None:
            raise KeyError(f"Game {game_id} was not found.")

        return {
            "id": game.game_id,
            "title": game.title,
            "module": game.module_name,
        }

    def count(self) -> int:
        return len(self.loader.discover())

    def launchable_ids(self) -> List[int]:
        return [
            game.game_id
            for game in self.loader.discover()
        ]

    def summary(self) -> Dict[str, Any]:
        games = self.loader.discover()
        ids = [game.game_id for game in games]

        return {
            "target": self.TOTAL_TARGET,
            "discovered": len(games),
            "missing_ids": [
                game_id
                for game_id in range(1, self.TOTAL_TARGET + 1)
                if game_id not in ids
            ],
            "ready_for_runtime": len(games),
        }
