import json
import os
import tempfile
from typing import Dict, Any


class SaveSystem:
    VERSION = 2

    def __init__(self, directory="ajvyra_saves"):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def _path(self, game_id):
        safe = "".join(
            c for c in game_id
            if c.isalnum() or c in "-_"
        )
        return os.path.join(
            self.directory,
            f"{safe}.json"
        )

    def save(self, game_id, state: Dict[str, Any]):
        payload = {
            "version": self.VERSION,
            "game_id": game_id,
            "state": state
        }

        path = self._path(game_id)

        fd, temporary = tempfile.mkstemp(
            prefix="ajvyra_",
            suffix=".tmp",
            dir=self.directory
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                json.dump(
                    payload,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            os.replace(temporary, path)

        except Exception:
            try:
                os.remove(temporary)
            except OSError:
                pass
            raise

    def load(self, game_id):
        path = self._path(game_id)

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as file:
            payload = json.load(file)

        if payload.get("game_id") != game_id:
            raise ValueError("Save belongs to another game.")

        return payload.get("state")

    def exists(self, game_id):
        return os.path.exists(self._path(game_id))

    def delete(self, game_id):
        path = self._path(game_id)

        if os.path.exists(path):
            os.remove(path)
