from __future__ import annotations

from pathlib import Path
import json


class AJVYRAStaticPlayerManifest:
    def __init__(
        self,
        public_root: str | Path = "public",
    ) -> None:
        self.public_root = Path(public_root)

    def build(
        self,
        registry_path: str | Path,
        output_path: str | Path | None = None,
    ) -> Path:

        registry_file = Path(registry_path)

        data = json.loads(
            registry_file.read_text(encoding="utf-8")
        )

        players = []

        for movie in data.get("movies", []):
            film_id = movie["film_id"]

            players.append(
                {
                    "film_id": film_id,
                    "title": movie["title"],
                    "duration_seconds": movie["duration_seconds"],
                    "watchable": True,
                    "video": f"/cinematic_anime/{film_id}/movie.mp4",
                    "poster": f"/cinematic_anime/{film_id}/poster.jpg",
                    "subtitles": {
                        "fa": f"/cinematic_anime/{film_id}/subtitles/fa.srt",
                        "en": f"/cinematic_anime/{film_id}/subtitles/en.srt",
                        "ja": f"/cinematic_anime/{film_id}/subtitles/ja.srt",
                    },
                }
            )

        destination = (
            Path(output_path)
            if output_path
            else self.public_root / "cinematic_player_manifest.json"
        )

        destination.parent.mkdir(parents=True, exist_ok=True)

        destination.write_text(
            json.dumps(
                {
                    "version": "1",
                    "players": players,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return destination
