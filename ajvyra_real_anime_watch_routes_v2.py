"""
AJVYRA — REAL ANIME WATCH ROUTES v2

لایه route مستقل از framework.

می‌تواند توسط Flask/FastAPI/Starlette یا backend فعلی
پروژه استفاده شود.
"""

from __future__ import annotations

from pathlib import Path

from ajvyra_real_anime_player_v2 import (
    AnimePlayerFactory,
)
from ajvyra_real_anime_web_library_v2 import (
    RealAnimeWebLibrary,
)


class AnimeWatchRoutes:

    def __init__(
        self,
        manifest: Path,
    ):
        self.library = RealAnimeWebLibrary(
            manifest
        )

        self.library.require_all_available()

        self.player_factory = (
            AnimePlayerFactory()
        )

    def list_anime(self) -> list[dict]:
        return self.library.all()

    def watch_data(
        self,
        anime_number: int,
    ) -> dict:

        anime = self.library.get(
            anime_number
        )

        player = self.player_factory.create(
            anime
        )

        return {
            "id": player.anime_id,
            "title": player.title,
            "video_url": player.video_url,
            "poster_url": player.poster_url,
            "duration_seconds": (
                player.duration_seconds
            ),
            "player_html": (
                self.player_factory.html(
                    player
                )
            ),
        }
