from __future__ import annotations

import argparse
import json
import sys
import traceback
from pathlib import Path
from typing import Any

from ajvyra_anime_30_catalog_runner import (
    Anime30CatalogRunner,
)
from ajvyra_anime_generation_orchestrator import (
    AnimeGenerationOrchestrator,
)
from ajvyra_anime_full_production_engine import (
    FullAnimeProductionEngine,
)


class AJVYRAAnimeWarMachine:
    """
    Autonomous anime production commander.

    Mission:

        30 anime
            ↓
        production queue
            ↓
        story
            ↓
        characters
            ↓
        locations
            ↓
        scenes
            ↓
        dialogue
            ↓
        native voices
            ↓
        native visuals
            ↓
        animation
            ↓
        video
            ↓
        subtitles
            ↓
        publishing
            ↓
        website-ready catalog
    """

    def __init__(self):
        self.catalog = Anime30CatalogRunner()

        self.orchestrator = (
            AnimeGenerationOrchestrator()
        )

        self.engine = FullAnimeProductionEngine()

    def prepare(self) -> dict:
        return self.catalog.build_queue()

    def produce_one(
        self,
        anime_id: int,
    ) -> dict[str, Any]:
        manifest = (
            self.orchestrator.registry.load(
                anime_id
            )
        )

        state = (
            self.orchestrator.load_state(
                anime_id
            )
        )

        results = []

        for step in state["steps"]:
            name = step["name"]

            if step["status"] == "completed":
                continue

            result = self.orchestrator.run_step(
                anime_id=anime_id,
                step_name=name,
                worker=lambda current_manifest,
                current_step=name:
                    self.engine.execute(
                        current_manifest,
                        current_step,
                    ),
            )

            results.append(result)

            if not result["ok"]:
                return {
                    "ok": False,
                    "anime_id": anime_id,
                    "failed_step": name,
                    "results": results,
                }

        return {
            "ok": True,
            "anime_id": anime_id,
            "title": manifest.title,
            "results": results,
            "status": (
                self.orchestrator.status(
                    anime_id
                )
            ),
        }

    def produce_all(
        self,
        stop_on_error: bool = False,
    ) -> dict:
        self.prepare()

        summary = {
            "total": 30,
            "completed": 0,
            "failed": 0,
            "results": [],
        }

        while True:
            job = self.catalog.next_job()

            if job is None:
                break

            anime_id = int(
                job["anime_id"]
            )

            self.catalog.mark_job(
                anime_id,
                "running",
            )

            try:
                result = self.produce_one(
                    anime_id
                )

                summary["results"].append(
                    result
                )

                if result["ok"]:
                    summary["completed"] += 1

                    self.catalog.mark_job(
                        anime_id,
                        "completed",
                    )
                else:
                    summary["failed"] += 1

                    self.catalog.mark_job(
                        anime_id,
                        "failed",
                        error=result.get(
                            "failed_step"
                        ),
                    )

                    if stop_on_error:
                        break

            except Exception as error:
                summary["failed"] += 1

                self.catalog.mark_job(
                    anime_id,
                    "failed",
                    error=str(error),
                )

                summary["results"].append(
                    {
                        "ok": False,
                        "anime_id": anime_id,
                        "error": str(error),
                        "traceback": (
                            traceback.format_exc()
                        ),
                    }
                )

                if stop_on_error:
                    break

        return summary

    def inspect(
        self,
        anime_id: int,
    ) -> dict:
        return (
            self.orchestrator.status(
                anime_id
            )
        )

    def site_status(self) -> dict:
        return self.catalog.status()

    def command(
        self,
        command: str,
        anime_id: int | None = None,
    ):
        if command == "prepare":
            return self.prepare()

        if command == "produce-one":
            if anime_id is None:
                raise ValueError(
                    "anime_id is required."
                )

            return self.produce_one(
                anime_id
            )

        if command == "produce-all":
            return self.produce_all()

        if command == "inspect":
            if anime_id is None:
                raise ValueError(
                    "anime_id is required."
                )

            return self.inspect(
                anime_id
            )

        if command == "site-status":
            return self.site_status()

        raise ValueError(
            f"Unknown command: {command}"
        )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA Anime AI War Machine"
        )
    )

    parser.add_argument(
        "command",
        choices=[
            "prepare",
            "produce-one",
            "produce-all",
            "inspect",
            "site-status",
        ],
    )

    parser.add_argument(
        "--anime",
        type=int,
        default=None,
        help="Anime number: 1-30",
    )

    args = parser.parse_args()

    machine = AJVYRAAnimeWarMachine()

    try:
        result = machine.command(
            args.command,
            args.anime,
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

    except Exception as error:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(error),
                    "traceback": traceback.format_exc(),
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )

        raise SystemExit(1)


if __name__ == "__main__":
    main()
