from __future__ import annotations

import importlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path("ajvyra_projects")
STATE_FILE = ROOT / "site_catalog.json"

ANIME_COUNT = 30
GAME_COUNT = 70


@dataclass
class SiteItem:
    item_id: int
    title: str
    item_type: str
    genre: str = ""
    description: str = ""
    status: str = "ready"
    source: str = ""


class AJVYRASiteCatalog:
    """
    Central catalog used by the AJVYRA website.

    It does not duplicate anime/game data into every page.
    The website reads one normalized catalog from here.
    """

    def __init__(self) -> None:
        self.root = ROOT
        self.state_file = STATE_FILE
        self.anime: list[SiteItem] = []
        self.games: list[SiteItem] = []

        self.root.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Generic helpers
    # ---------------------------------------------------------

    @staticmethod
    def _read_value(obj: Any, *names: str, default: Any = "") -> Any:
        for name in names:
            if isinstance(obj, dict) and name in obj:
                return obj[name]

            if hasattr(obj, name):
                return getattr(obj, name)

        return default

    @staticmethod
    def _as_list(value: Any) -> list[Any]:
        if value is None:
            return []

        if isinstance(value, (list, tuple, set)):
            return list(value)

        if isinstance(value, dict):
            return list(value.values())

        return []

    @staticmethod
    def _unique(items: Iterable[SiteItem]) -> list[SiteItem]:
        result: list[SiteItem] = []
        seen: set[tuple[str, int]] = set()

        for item in items:
            key = (item.item_type, item.item_id)

            if key in seen:
                continue

            seen.add(key)
            result.append(item)

        return result

    # ---------------------------------------------------------
    # Anime
    # ---------------------------------------------------------

    def load_anime(self) -> list[SiteItem]:
        """
        Loads the existing 30-anime catalog.

        It intentionally does not create another copy of the
        anime titles.
        """

        modules = (
            "ajvyra_anime_studio",
            "ajvyra_anime_content_core",
        )

        loaded: list[SiteItem] = []

        for module_name in modules:
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                continue

            catalog = getattr(module, "ANIME", None)

            if catalog is None:
                catalog = getattr(module, "ANIME_CONTENT", None)

            if catalog is None:
                continue

            for raw in self._as_list(catalog):
                number = self._read_value(
                    raw,
                    "number",
                    "id",
                    "anime_id",
                    default=len(loaded) + 1,
                )

                title = self._read_value(
                    raw,
                    "title",
                    "name",
                    default=f"Anime {number}",
                )

                genre = self._read_value(
                    raw,
                    "genre",
                    "genres",
                    default="",
                )

                if isinstance(genre, (list, tuple)):
                    genre = ", ".join(map(str, genre))

                description = self._read_value(
                    raw,
                    "logline",
                    "description",
                    "premise",
                    default="",
                )

                loaded.append(
                    SiteItem(
                        item_id=int(number),
                        title=str(title),
                        item_type="anime",
                        genre=str(genre),
                        description=str(description),
                        status="ready",
                        source=module_name,
                    )
                )

        loaded = self._unique(
            sorted(loaded, key=lambda item: item.item_id)
        )

        self.anime = loaded[:ANIME_COUNT]
        return self.anime

    # ---------------------------------------------------------
    # Games
    # ---------------------------------------------------------

    def load_games(self) -> list[SiteItem]:
        """
        Discovers an existing game catalog without assuming
        a particular implementation.

        This allows the AI creator to plug into the site later
        without rewriting the website catalog.
        """

        possible_modules = (
            "ajvyra_game_catalog",
            "ajvyra_games",
            "ajvyra_game_registry",
            "ajvyra_game_library",
            "ajvyra_games_catalog",
            "ajvyra_game_creator_ai",
        )

        variable_names = (
            "GAMES",
            "GAME_CATALOG",
            "GAME_LIBRARY",
            "GAME_REGISTRY",
        )

        loaded: list[SiteItem] = []

        for module_name in possible_modules:
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                continue

            catalog = None

            for variable_name in variable_names:
                candidate = getattr(module, variable_name, None)

                if candidate is not None:
                    catalog = candidate
                    break

            if catalog is None:
                continue

            for raw in self._as_list(catalog):
                number = self._read_value(
                    raw,
                    "number",
                    "id",
                    "game_id",
                    default=len(loaded) + 1,
                )

                title = self._read_value(
                    raw,
                    "title",
                    "name",
                    default=f"Game {number}",
                )

                genre = self._read_value(
                    raw,
                    "genre",
                    "genres",
                    default="",
                )

                if isinstance(genre, (list, tuple)):
                    genre = ", ".join(map(str, genre))

                description = self._read_value(
                    raw,
                    "description",
                    "logline",
                    "summary",
                    default="",
                )

                loaded.append(
                    SiteItem(
                        item_id=int(number),
                        title=str(title),
                        item_type="game",
                        genre=str(genre),
                        description=str(description),
                        status="ready",
                        source=module_name,
                    )
                )

        loaded = self._unique(
            sorted(loaded, key=lambda item: item.item_id)
        )

        self.games = loaded[:GAME_COUNT]
        return self.games

    # ---------------------------------------------------------
    # AI-created placeholders
    # ---------------------------------------------------------

    def fill_missing_games(self) -> list[SiteItem]:
        """
        Creates project entries for games that do not yet have
        a concrete catalog entry.

        These are project records, not fake finished games.
        The AI creator can later replace their status with
        generated/build-ready assets.
        """

        existing_ids = {game.item_id for game in self.games}

        for game_id in range(1, GAME_COUNT + 1):
            if game_id in existing_ids:
                continue

            self.games.append(
                SiteItem(
                    item_id=game_id,
                    title=f"AJVYRA Game {game_id:02d}",
                    item_type="game",
                    genre="AI Generated",
                    description=(
                        "AI game project awaiting its generated "
                        "world, mechanics, characters and assets."
                    ),
                    status="ai_project",
                    source="ajvyra_ai_creator",
                )
            )

        self.games.sort(key=lambda item: item.item_id)
        return self.games

    # ---------------------------------------------------------
    # Site initialization
    # ---------------------------------------------------------

    def initialize(self) -> dict[str, Any]:
        self.load_anime()
        self.load_games()
        self.fill_missing_games()

        state = {
            "project": "AJVYRA",
            "initialized": True,
            "anime_count": len(self.anime),
            "game_count": len(self.games),
            "anime": [asdict(item) for item in self.anime],
            "games": [asdict(item) for item in self.games],
        }

        self.state_file.write_text(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return state

    # ---------------------------------------------------------
    # Website API data
    # ---------------------------------------------------------

    def api_payload(self) -> dict[str, Any]:
        if not self.anime and not self.games:
            self.initialize()

        return {
            "project": "AJVYRA",
            "anime": [asdict(item) for item in self.anime],
            "games": [asdict(item) for item in self.games],
            "counts": {
                "anime": len(self.anime),
                "games": len(self.games),
                "total": len(self.anime) + len(self.games),
            },
        }

    def find(
        self,
        item_type: str | None = None,
        item_id: int | None = None,
        query: str | None = None,
    ) -> list[SiteItem]:

        items = self.anime + self.games

        if item_type:
            items = [
                item
                for item in items
                if item.item_type == item_type
            ]

        if item_id is not None:
            items = [
                item
                for item in items
                if item.item_id == item_id
            ]

        if query:
            q = query.strip().lower()

            items = [
                item
                for item in items
                if (
                    q in item.title.lower()
                    or q in item.genre.lower()
                    or q in item.description.lower()
                )
            ]

        return items


# -------------------------------------------------------------
# Global runtime
# -------------------------------------------------------------

SITE_CATALOG = AJVYRASiteCatalog()


def initialize_site() -> dict[str, Any]:
    return SITE_CATALOG.initialize()


def site_api_payload() -> dict[str, Any]:
    return SITE_CATALOG.api_payload()


def search_site(
    query: str,
    item_type: str | None = None,
) -> list[dict[str, Any]]:

    return [
        asdict(item)
        for item in SITE_CATALOG.find(
            item_type=item_type,
            query=query,
        )
    ]


if __name__ == "__main__":
    state = initialize_site()

    print("AJVYRA SITE INITIALIZED")
    print(f"Anime : {state['anime_count']}")
    print(f"Games : {state['game_count']}")
    print(f"Total : {state['anime_count'] + state['game_count']}")
    print(f"State : {STATE_FILE}")
