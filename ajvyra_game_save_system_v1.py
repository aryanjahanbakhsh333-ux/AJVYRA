from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class GameSaveSystem:
    def __init__(
        self,
        directory: str = "ajvyra_saves",
    ):
        self.directory = Path(directory)
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _file(self, game_id: int) -> Path:
        return self.directory / (
            f"game_{int(game_id):03d}.json"
        )

    def save(
        self,
        game_id: int,
        state: Dict[str, Any],
    ) -> str:
        path = self._file(game_id)

        temporary = path.with_suffix(
            ".tmp"
        )

        with temporary.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=2,
                default=str,
            )

        temporary.replace(path)

        return str(path)

    def load(
        self,
        game_id: int,
    ) -> Dict[str, Any] | None:
        path = self._file(game_id)

        if not path.exists():
            return None

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def delete(self, game_id: int) -> bool:
        path = self._file(game_id)

        if not path.exists():
            return False

        path.unlink()
        return True
