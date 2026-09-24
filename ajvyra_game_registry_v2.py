from typing import Dict, Type

from ajvyra_mobile_engine_v2 import MobileGame


class GameRegistry:
    def __init__(self):
        self._games: Dict[str, Type[MobileGame]] = {}

    def register(self, game_id: str, game_class: Type[MobileGame]):
        if game_id in self._games:
            raise ValueError(
                f"Game already registered: {game_id}"
            )

        self._games[game_id] = game_class

    def create(self, game_id: str, **kwargs):
        game_class = self._games.get(game_id)

        if game_class is None:
            raise KeyError(
                f"Game implementation not found: {game_id}"
            )

        game = game_class(**kwargs)
        game.state["game_id"] = game_id
        return game

    def contains(self, game_id):
        return game_id in self._games

    def ids(self):
        return list(self._games.keys())

    def count(self):
        return len(self._games)


AJVYRA_GAMES = GameRegistry()
