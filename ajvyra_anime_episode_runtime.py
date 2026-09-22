from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


ANIME_ROOT = Path("anime_assets")


@dataclass(frozen=True)
class AnimeEpisode:
    anime_id: int
    episode_number: int
    title: str
    duration_seconds: int
    video: str
    audio_fa: str
    audio_ja: str
    subtitle_en: str
    subtitle_fa: str
    subtitle_ja: str


class AnimeEpisodeRuntime:
    """
    Creates the runtime episode representation.

    AJVYRA currently defines each anime as one 30-minute episode.
    Internally it may still contain production segments.
    """

    def __init__(
        self,
        root: Path = ANIME_ROOT,
    ):
        self.root = Path(root)

    def build(
        self,
        anime_id: int,
        title: str,
    ) -> AnimeEpisode:

        folder = (
            f"anime_{int(anime_id):02d}"
        )

        return AnimeEpisode(
            anime_id=int(anime_id),
            episode_number=1,
            title=title,
            duration_seconds=1800,
            video=(
                f"{folder}/video/main.mp4"
            ),
            audio_fa=(
                f"{folder}/voice/fa_full.mp3"
            ),
            audio_ja=(
                f"{folder}/voice/ja_full.mp3"
            ),
            subtitle_en=(
                f"{folder}/subtitles/en.srt"
            ),
            subtitle_fa=(
                f"{folder}/subtitles/fa.srt"
            ),
            subtitle_ja=(
                f"{folder}/subtitles/ja.srt"
            ),
        )

    def player_payload(
        self,
        anime_id: int,
        title: str,
    ) -> Dict[str, Any]:

        episode = self.build(
            anime_id,
            title,
        )

        return {
            "anime_id": episode.anime_id,
            "episodes": [
                {
                    **asdict(episode),
                    "episode_url": (
                        f"/anime/"
                        f"{episode.anime_id}/"
                        f"episode/"
                        f"{episode.episode_number}"
                    ),
                }
            ],
            "audio_options": [
                {
                    "id": "fa",
                    "label": "فارسی",
                },
                {
                    "id": "ja",
                    "label": "日本語",
                },
            ],
            "subtitle_options": [
                {
                    "id": "en",
                    "label": "English",
                },
                {
                    "id": "fa",
                    "label": "فارسی",
                },
                {
                    "id": "ja",
                    "label": "日本語",
                },
                {
                    "id": "off",
                    "label": "خاموش",
                },
            ],
        }

    def asset_status(
        self,
        episode: AnimeEpisode,
    ) -> Dict[str, bool]:

        paths = {
            "video": episode.video,
            "audio_fa": episode.audio_fa,
            "audio_ja": episode.audio_ja,
            "subtitle_en": episode.subtitle_en,
            "subtitle_fa": episode.subtitle_fa,
            "subtitle_ja": episode.subtitle_ja,
        }

        return {
            key: (
                self.root / path
            ).is_file()
            for key, path in paths.items()
        }

    def ready(
        self,
        episode: AnimeEpisode,
    ) -> bool:

        status = self.asset_status(
            episode
        )

        return (
            status["video"]
            and (
                status["audio_fa"]
                or status["audio_ja"]
            )
        )


EPISODES = AnimeEpisodeRuntime()
