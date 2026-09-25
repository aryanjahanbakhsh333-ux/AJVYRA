"""
AJVYRA Game Discovery Loader v1

Discovers numbered AJVYRA game modules without hardcoding
every filename.
"""

from __future__ import annotations

import importlib
import pkgutil
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


GAME_PATTERN = re.compile(
    r"^ajvyra_game_(\d{3})_.*_(?:v2|v3)$"
)


@dataclass
class DiscoveredGame:
    game_id: int
    module_name: str
    module: Any
    title: str


class GameDiscoveryLoader:
    def __init__(self, package_name: str = "") -> None:
        self.package_name = package_name

    def discover(self) -> List[DiscoveredGame]:
        results: List[DiscoveredGame] = []

        modules = self._find_modules()

        for module_name in modules:
            match = GAME_PATTERN.match(module_name)

            if not match:
                continue

            game_id = int(match.group(1))

            try:
                module = importlib.import_module(module_name)
            except Exception:
                # One broken module must not prevent the rest
                # of the catalog from loading.
                continue

            title = self._extract_title(module, game_id)

            results.append(
                DiscoveredGame(
                    game_id=game_id,
                    module_name=module_name,
                    module=module,
                    title=title,
                )
            )

        results.sort(key=lambda item: item.game_id)
        return results

    def _find_modules(self) -> List[str]:
        found: List[str] = []

        for item in pkgutil.iter_modules():
            name = item.name

            if name.startswith("ajvyra_game_"):
                found.append(name)

        return found

    @staticmethod
    def _extract_title(module: Any, game_id: int) -> str:
        for attribute in (
            "GAME_TITLE",
            "TITLE",
            "GAME_NAME",
            "NAME",
        ):
            value = getattr(module, attribute, None)

            if isinstance(value, str) and value.strip():
                return value.strip()

        return f"AJVYRA Game {game_id:03d}"

    def find_game(self, game_id: int) -> Optional[DiscoveredGame]:
        for game in self.discover():
            if game.game_id == int(game_id):
                return game

        return None
