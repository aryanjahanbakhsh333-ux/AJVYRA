from __future__ import annotations

import json
from pathlib import Path


class AJVYRAAnimeFinalAssetIndexV3:

    def __init__(
        self,
        output_path: str,
    ):
        self.output_path = Path(
            output_path
        )

    def build(
        self,
        release_manifest: dict,
    ) -> dict:

        films = release_manifest.get(
            "films",
            []
        )

        if len(films) != 30:
            raise RuntimeError(
                "Cannot create final asset index "
                "without all 30 films."
            )

        assets = []

        for film in films:

            if film.get("status") != "READY":
                raise RuntimeError(
                    f"Film is not READY: "
                    f"{film.get('id')}"
                )

            video = film.get("video")

            if not video:
                raise RuntimeError(
                    f"Missing video: "
                    f"{film.get('id')}"
                )

            path = Path(video)

            if not path.exists():
                raise RuntimeError(
                    f"Missing physical MP4: "
                    f"{path}"
                )

            assets.append(
                {
                    "id": film["id"],
                    "title": film["title"],
                    "type": "anime",
                    "status": "READY",
                    "video": str(path),
                    "duration": film.get(
                        "duration",
                        0
                    ),
                    "size": path.stat().st_size,
                }
            )

        index = {
            "project": "AJVYRA",
            "version": 3,
            "anime_count": 30,
            "assets": assets,
        }

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_path.write_text(
            json.dumps(
                index,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return index
