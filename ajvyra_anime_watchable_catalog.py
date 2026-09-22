from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class AJVYRAWatchableAnimeCatalog:

    def __init__(
        self,
        public_root: str = "public/anime",
        output: str = (
            "generated/anime_site/watchable_catalog.json"
        ),
    ):
        self.public_root = Path(public_root)
        self.output = Path(output)

    def build(self) -> Dict[str, Any]:

        entries: List[Dict[str, Any]] = []

        for anime_dir in sorted(
            self.public_root.glob("anime_*")
        ):
            metadata = (
                anime_dir
                / "anime.json"
            )

            video = (
                anime_dir
                / "season_01"
                / "episode_01.mp4"
            )

            if not metadata.exists():
                continue

            if not video.exists():
                continue

            try:
                data = json.loads(
                    metadata.read_text(
                        encoding="utf-8"
                    )
                )
            except json.JSONDecodeError:
                continue

            if data.get("status") != "WATCHABLE":
                continue

            data["watch_url"] = (
                f"/anime/{data['anime_id']}/"
                f"season_01/episode_01.mp4"
            )

            entries.append(data)

        catalog = {
            "status": "READY",
            "total_watchable": len(entries),
            "anime": entries,
        }

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output.write_text(
            json.dumps(
                catalog,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return catalog


if __name__ == "__main__":
    catalog = (
        AJVYRAWatchableAnimeCatalog()
        .build()
    )

    print(
        json.dumps(
            catalog,
            ensure_ascii=False,
            indent=2,
        )
    )
