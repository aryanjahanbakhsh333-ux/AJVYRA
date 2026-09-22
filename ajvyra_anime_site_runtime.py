from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path("anime_assets")
RUNTIME_ROOT = Path("ajvyra_projects/anime/runtime")
STATE_FILE = RUNTIME_ROOT / "anime_runtime.json"


@dataclass
class AnimeRuntimeItem:
    anime_id: int
    title: str
    genre: str
    mood: str
    duration_seconds: int
    video: Optional[str]
    audio_fa: Optional[str]
    audio_ja: Optional[str]
    subtitle_en: Optional[str]
    subtitle_fa: Optional[str]
    subtitle_ja: Optional[str]
    poster: Optional[str]
    playable: bool
    watchable: bool


class AnimeSiteRuntime:
    """
    Runtime registry for the complete AJVYRA Anime section.

    This module does not duplicate anime titles.
    It reads the existing AJVYRA anime catalog and exposes
    normalized runtime information for the website.
    """

    def __init__(
        self,
        root: Path = ROOT,
        runtime_root: Path = RUNTIME_ROOT,
    ):
        self.root = Path(root)
        self.runtime_root = Path(runtime_root)

        self.runtime_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.items: List[AnimeRuntimeItem] = []

        self.refresh()

    def refresh(self) -> List[AnimeRuntimeItem]:
        catalog = self._load_catalog()

        self.items = []

        for anime in catalog:
            number = int(
                getattr(
                    anime,
                    "number",
                    anime.get("number", 0)
                    if isinstance(anime, dict)
                    else 0,
                )
            )

            title = str(
                getattr(
                    anime,
                    "title",
                    anime.get("title", "")
                    if isinstance(anime, dict)
                    else "",
                )
            )

            genre = str(
                getattr(
                    anime,
                    "genre",
                    anime.get("genre", "")
                    if isinstance(anime, dict)
                    else "",
                )
            )

            mood = str(
                getattr(
                    anime,
                    "mood",
                    anime.get("mood", "")
                    if isinstance(anime, dict)
                    else "",
                )
            )

            self.items.append(
                AnimeRuntimeItem(
                    anime_id=number,
                    title=title,
                    genre=genre,
                    mood=mood,
                    duration_seconds=1800,
                    video=self._asset(
                        anime,
                        "video_path",
                        f"anime_{number:02d}/video/main.mp4",
                    ),
                    audio_fa=self._asset(
                        anime,
                        "voice_fa_path",
                        f"anime_{number:02d}/voice/fa_full.mp3",
                    ),
                    audio_ja=self._asset(
                        anime,
                        "voice_ja_path",
                        f"anime_{number:02d}/voice/ja_full.mp3",
                    ),
                    subtitle_en=self._asset(
                        anime,
                        "subtitle_en_path",
                        f"anime_{number:02d}/subtitles/en.srt",
                    ),
                    subtitle_fa=self._asset(
                        anime,
                        "subtitle_fa_path",
                        f"anime_{number:02d}/subtitles/fa.srt",
                    ),
                    subtitle_ja=self._asset(
                        anime,
                        "subtitle_ja_path",
                        f"anime_{number:02d}/subtitles/ja.srt",
                    ),
                    poster=self._asset(
                        anime,
                        "poster_path",
                        f"anime_{number:02d}/poster.jpg",
                    ),
                    playable=False,
                    watchable=False,
                )
            )

        self._update_availability()
        self.save()

        return self.items

    def _load_catalog(self) -> List[Any]:
        try:
            from ajvyra_anime_studio import ANIME

            return list(ANIME)
        except Exception:
            try:
                from ajvyra_anime_content_core import all_anime

                return list(all_anime())
            except Exception:
                return []

    def _asset(
        self,
        anime: Any,
        attribute: str,
        fallback: str,
    ) -> Optional[str]:

        value = getattr(anime, attribute, None)

        if value is None and isinstance(anime, dict):
            value = anime.get(attribute)

        if value:
            return str(value)

        return fallback

    def _exists(self, relative_path: Optional[str]) -> bool:
        if not relative_path:
            return False

        candidate = self.root / relative_path

        return candidate.is_file()

    def _update_availability(self) -> None:
        for item in self.items:
            item.watchable = self._exists(item.video)
            item.playable = item.watchable

    def get(self, anime_id: int) -> Optional[AnimeRuntimeItem]:
        for item in self.items:
            if item.anime_id == int(anime_id):
                return item

        return None

    def all(self) -> List[AnimeRuntimeItem]:
        return list(self.items)

    def search(self, query: str) -> List[AnimeRuntimeItem]:
        query = query.strip().lower()

        if not query:
            return self.all()

        return [
            item
            for item in self.items
            if query in item.title.lower()
            or query in item.genre.lower()
            or query in item.mood.lower()
        ]

    def payload(self) -> Dict[str, Any]:
        return {
            "section": "anime",
            "count": len(self.items),
            "duration_seconds": 1800,
            "languages": {
                "audio": ["fa", "ja"],
                "subtitles": ["en", "fa", "ja"],
                "subtitle_off": True,
            },
            "items": [
                asdict(item)
                for item in self.items
            ],
        }

    def save(self) -> None:
        STATE_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        STATE_FILE.write_text(
            json.dumps(
                self.payload(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


RUNTIME = AnimeSiteRuntime()


if __name__ == "__main__":
    print(
        json.dumps(
            RUNTIME.payload(),
            ensure_ascii=False,
            indent=2,
        )
    )
