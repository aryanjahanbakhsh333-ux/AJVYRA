from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ajvyra_anime_production_manifest import (
    ManifestRegistry,
)
from ajvyra_anime_generation_orchestrator import (
    AnimeGenerationOrchestrator,
)


class Anime30CatalogRunner:
    """
    Reads the existing AJVYRA anime catalog and prepares
    all 30 anime for autonomous production.
    """

    def __init__(
        self,
        queue_path: str | Path = (
            "ajvyra_projects/anime_production_queue.json"
        ),
    ):
        self.queue_path = Path(queue_path)

        self.queue_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.orchestrator = (
            AnimeGenerationOrchestrator()
        )

    def _load_existing_catalog(self) -> list[dict]:
        possible_modules = [
            "ajvyra_anime_studio",
            "ajvyra_anime_content_core",
        ]

        for module_name in possible_modules:
            try:
                module = __import__(
                    module_name
                )

                if hasattr(module, "ANIME"):
                    catalog = getattr(
                        module,
                        "ANIME",
                    )

                    result = []

                    for item in catalog:
                        if hasattr(
                            item,
                            "number",
                        ):
                            result.append(
                                {
                                    "anime_id": int(
                                        item.number
                                    ),
                                    "title": str(
                                        item.title
                                    ),
                                }
                            )

                    if result:
                        return result

                if hasattr(
                    module,
                    "ANIME_CONTENT",
                ):
                    catalog = getattr(
                        module,
                        "ANIME_CONTENT",
                    )

                    result = []

                    for item in catalog:
                        if hasattr(
                            item,
                            "number",
                        ):
                            anime_id = int(
                                item.number
                            )
                        elif hasattr(
                            item,
                            "anime_id",
                        ):
                            anime_id = int(
                                item.anime_id
                            )
                        else:
                            continue

                        result.append(
                            {
                                "anime_id": anime_id,
                                "title": str(
                                    item.title
                                ),
                            }
                        )

                    if result:
                        return result

            except Exception:
                continue

        raise RuntimeError(
            "AJVYRA anime catalog could not be loaded."
        )

    def build_queue(self) -> dict[str, Any]:
        catalog = self._load_existing_catalog()

        catalog = sorted(
            catalog,
            key=lambda item: item["anime_id"],
        )

        if len(catalog) != 30:
            raise RuntimeError(
                f"AJVYRA requires 30 anime. "
                f"Found {len(catalog)}."
            )

        registry = ManifestRegistry()

        jobs = []

        for item in catalog:
            anime_id = item["anime_id"]
            title = item["title"]

            manifest_path = registry.path_for(
                anime_id
            )

            if manifest_path.exists():
                manifest = registry.load(
                    anime_id
                )
            else:
                manifest = registry.create(
                    anime_id=anime_id,
                    title=title,
                    duration_seconds=1800,
                    fps=24,
                )

            if not self.orchestrator._state_path(
                anime_id
            ).exists():
                self.orchestrator.create_state(
                    anime_id,
                    title,
                )

            jobs.append(
                {
                    "anime_id": anime_id,
                    "title": title,
                    "duration_seconds": 1800,
                    "fps": 24,
                    "status": "queued",
                    "languages": {
                        "audio": [
                            "fa",
                            "ja",
                        ],
                        "subtitles": [
                            "en",
                            "fa",
                            "ja",
                        ],
                    },
                }
            )

        payload = {
            "project": "AJVYRA",
            "type": "anime_production",
            "total_anime": 30,
            "episode_duration_seconds": 1800,
            "episode_duration_minutes": 30,
            "jobs": jobs,
        }

        with self.queue_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                payload,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return payload

    def next_job(self) -> dict | None:
        if not self.queue_path.exists():
            self.build_queue()

        with self.queue_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            queue = json.load(file)

        for job in queue["jobs"]:
            if job["status"] == "queued":
                return job

        return None

    def mark_job(
        self,
        anime_id: int,
        status: str,
        error: str | None = None,
    ):
        with self.queue_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            queue = json.load(file)

        for job in queue["jobs"]:
            if job["anime_id"] == anime_id:
                job["status"] = status

                if error:
                    job["error"] = error

                break

        with self.queue_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                queue,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def status(self) -> dict:
        if not self.queue_path.exists():
            self.build_queue()

        with self.queue_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            queue = json.load(file)

        counts = {
            "queued": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
        }

        for job in queue["jobs"]:
            status = job.get(
                "status",
                "queued",
            )

            counts.setdefault(status, 0)
            counts[status] += 1

        return {
            "total": len(queue["jobs"]),
            "counts": counts,
            "jobs": queue["jobs"],
        }


if __name__ == "__main__":
    runner = Anime30CatalogRunner()

    result = runner.build_queue()

    print(
        json.dumps(
            {
                "message": (
                    "30 AJVYRA anime are queued "
                    "for autonomous production."
                ),
                "total": result["total_anime"],
                "duration_minutes": (
                    result[
                        "episode_duration_minutes"
                    ]
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
