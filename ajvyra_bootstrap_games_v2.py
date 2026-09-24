from ajvyra_game_registry_v2 import AJVYRA_GAMES
from ajvyra_game_001_football_v2 import AJVYRAFootballGame


def register_builtin_games():
    if not AJVYRA_GAMES.contains("game_001"):
        AJVYRA_GAMES.register(
            "game_001",
            AJVYRAFootballGame
        )


def initialize_ajvyra():
    register_builtin_games()

    return {
        "game_catalog_loaded": True,
        "registered_implementations": AJVYRA_GAMES.count(),
        "registered_game_ids": AJVYRA_GAMES.ids()
    }


AJVYRA_STARTUP = initialize_ajvyra()
