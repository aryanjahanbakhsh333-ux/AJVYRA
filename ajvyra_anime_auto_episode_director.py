from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


class AJVYRAAutoEpisodeDirector:

    def __init__(
        self,
        root: str = "generated/anime_production",
    ):
        self.root = Path(root)

    def create_episode(
        self,
        anime: Dict,
    ) -> Dict:

        anime_id = anime["anime_id"]
        title = anime["title"]
        genre = anime["genre"]

        episode_root = (
            self.root
            / anime_id
            / "season_01"
            / "episode_01"
        )

        episode_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        characters = self._characters(
            title,
            genre,
        )

        scenes = self._scenes(
            title,
            genre,
            characters,
        )

        story = {
            "anime_id": anime_id,
            "title": title,
            "genre": genre,
            "episode": 1,
            "duration_seconds": 1800,
            "language_tracks": [
                "fa",
                "ja",
            ],
            "subtitle_tracks": [
                "fa",
                "ja",
                "en",
            ],
            "characters": characters,
            "scenes": scenes,
        }

        output = episode_root / "story.json"

        output.write_text(
            json.dumps(
                story,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return story

    def _characters(
        self,
        title: str,
        genre: str,
    ) -> List[Dict]:

        return [
            {
                "id": f"{title.lower()}_protagonist",
                "name": f"{title} Protagonist",
                "role": "protagonist",
                "gender": "unspecified",
                "personality": (
                    "calm, emotionally complex, "
                    "determined"
                ),
                "visual_identity": {
                    "hair": "original anime hairstyle",
                    "eyes": "distinctive anime eyes",
                    "clothing": "genre-appropriate outfit",
                    "palette": "consistent character palette",
                },
                "voice_identity": {
                    "fa": "ajvyra_voice_fa_01",
                    "ja": "ajvyra_voice_ja_01",
                },
            },
            {
                "id": f"{title.lower()}_companion",
                "name": f"{title} Companion",
                "role": "supporting",
                "gender": "unspecified",
                "personality": (
                    "expressive, loyal, "
                    "emotionally contrasting"
                ),
                "visual_identity": {
                    "hair": "distinct original hairstyle",
                    "eyes": "unique anime eyes",
                    "clothing": "consistent supporting outfit",
                    "palette": "secondary character palette",
                },
                "voice_identity": {
                    "fa": "ajvyra_voice_fa_02",
                    "ja": "ajvyra_voice_ja_02",
                },
            },
        ]

    def _scenes(
        self,
        title: str,
        genre: str,
        characters: List[Dict],
    ) -> List[Dict]:

        protagonist = characters[0]["name"]
        companion = characters[1]["name"]

        scene_count = 30
        duration = 60

        scenes = []

        moods = [
            "mysterious",
            "quiet",
            "emotional",
            "tense",
            "hopeful",
            "dangerous",
        ]

        locations = [
            "original city street",
            "old train station",
            "quiet rooftop",
            "forest path",
            "abandoned building",
            "night city",
        ]

        for index in range(scene_count):

            mood = moods[index % len(moods)]
            location = locations[index % len(locations)]

            scenes.append(
                {
                    "scene_id": f"scene_{index + 1:03d}",
                    "duration": duration,
                    "characters": [
                        protagonist,
                        companion,
                    ],
                    "location": location,
                    "emotion": mood,
                    "action": (
                        f"{protagonist} and "
                        f"{companion} continue the "
                        f"{genre.lower()} story of {title}."
                    ),
                    "camera": (
                        "cinematic anime camera, "
                        "controlled movement"
                    ),
                    "lighting": (
                        "dramatic cinematic lighting"
                    ),
                    "style": (
                        "original cinematic anime"
                    ),
                    "dialogue": [],
                }
            )

        return scenes
