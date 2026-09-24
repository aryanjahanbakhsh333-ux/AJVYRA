import time
from typing import Optional

from ajvyra_game_catalog_v2 import GAME_DEFINITIONS
from ajvyra_game_registry_v2 import AJVYRA_GAMES


class GameRuntime:
    def __init__(self):
        self.current_game = None
        self.current_game_id: Optional[str] = None
        self.last_tick = time.monotonic()

    def launch(self, game_id, **kwargs):
        if game_id not in GAME_DEFINITIONS:
            raise KeyError(
                f"Unknown AJVYRA game: {game_id}"
            )

        self.current_game = AJVYRA_GAMES.create(
            game_id,
            **kwargs
        )

        self.current_game_id = game_id
        self.last_tick = time.monotonic()
        self.current_game.start()

        return self.current_game

    def tick(self):
        if not self.current_game:
            return

        now = time.monotonic()
        dt = now - self.last_tick
        self.last_tick = now

        self.current_game.update(dt)

    def stop(self):
        if self.current_game:
            self.current_game.stop()

    def pause(self):
        if self.current_game:
            self.current_game.paused = True

    def resume(self):
        if self.current_game:
            self.current_game.paused = False

    def snapshot(self):
        if not self.current_game:
            return None

        return self.current_game.snapshot()
