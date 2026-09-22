from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List


SOURCE_ROOT = Path("anime_assets")
PUBLISH_ROOT = Path(
    "ajvyra_projects/published/anime"
)

MANIFEST = PUBLISH_ROOT / "manifest.json"


@dataclass
class PublishedAnime:
    anime_id: int
    title: str
    directory: str
    video: str | None
    audio_fa: str | None
    audio_ja: str | None
    subtitle_en: str | None
    subtitle_fa: str | None
    subtitle_ja: str | None
    poster: str | None
    ready: bool


class AnimePublisher:
    """
    Converts generated anime assets into a clean,
    site-facing publication structure.
    """

    def __init__(
        self,
        source_root: Path = SOURCE_ROOT,
        publish_root: Path = PUBLISH_ROOT,
    ):
        self.source_root = Path(source_root)
        self.publish_root = Path(publish_root)

        self.publish_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def publish(
        self,
        anime_id: int,
        title: str,
    ) -> PublishedAnime:

        source = self.source_root / (
            f"anime_{anime_id:02d}"
        )

        target = self.publish_root / (
            f"anime_{anime_id:02d}"
        )

        target.mkdir(
            parents=True,
            exist_ok=True,
        )

        mappings = {
            "video": (
                source / "video" / "main.mp4"
            ),
            "audio_fa": (
                source / "voice" / "fa_full.mp3"
            ),
            "audio_ja": (
                source / "voice" / "ja_full.mp3"
            ),
            "subtitle_en": (
                source / "subtitles" / "en.srt"
            ),
            "subtitle_fa": (
                source / "subtitles" / "fa.srt"
            ),
            "subtitle_ja": (
                source / "subtitles" / "ja.srt"
            ),
            "poster": (
                source / "poster.jpg"
            ),
        }

        result: Dict[str, str | None] = {}

        for key, source_file in mappings.items():
            result[key] = self._copy_if_exists(
                source_file,
                target / source_file.name,
            )

        ready = bool(
            result["video"]
            and (
                result["audio_fa"]
                or result["audio_ja"]
            )
        )

        published = PublishedAnime(
            anime_id=int(anime_id),
            title=title,
            directory=str(target),
            video=result["video"],
            audio_fa=result["audio_fa"],
            audio_ja=result["audio_ja"],
            subtitle_en=result["subtitle_en"],
            subtitle_fa=result["subtitle_fa"],
            subtitle_ja=result["subtitle_ja"],
            poster=result["poster"],
            ready=ready,
        )

        self._update_manifest(
            published
        )

        return published

    def publish_all(
        self,
        catalog: List[Any],
    ) -> Dict[str, Any]:

        published = []

        for anime in catalog:
            anime_id = int(
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

            if anime_id <= 0 or not title:
                continue

            published.append(
                self.publish(
                    anime_id,
                    title,
                )
            )

        ready_count = sum(
            item.ready
            for item in published
        )

        return {
            "total": len(published),
            "ready": ready_count,
            "not_ready": (
                len(published)
                - ready_count
            ),
            "items": [
                asdict(item)
                for item in published
            ],
        }

    def _copy_if_exists(
        self,
        source: Path,
        target: Path,
    ) -> str | None:

        if not source.is_file():
            return None

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.copy2(
            source,
            target,
        )

        return str(target)

    def _update_manifest(
        self,
        item: PublishedAnime,
    ) -> None:

        existing = []

        if MANIFEST.exists():
            try:
                existing = json.loads(
                    MANIFEST.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                existing = []

        existing = [
            value
            for value in existing
            if int(
                value.get("anime_id", -1)
            ) != item.anime_id
        ]

        existing.append(
            asdict(item)
        )

        existing.sort(
            key=lambda value: value[
                "anime_id"
            ]
        )

        MANIFEST.write_text(
            json.dumps(
                existing,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


PUBLISHER = AnimePublisher()


if __name__ == "__main__":
    try:
        from ajvyra_anime_studio import ANIME

        result = PUBLISHER.publish_all(
            list(ANIME)
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

    except Exception as exc:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
