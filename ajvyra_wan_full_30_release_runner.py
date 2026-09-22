from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from ajvyra_wan_cinematic_story_adapter import (
    AJVYRAWanCinematicStoryAdapter,
)

from ajvyra_wan_full_cinematic_film_pipeline import (
    AJVYRAWanFullCinematicFilmPipeline,
)


@dataclass
class FilmReleaseStatus:
    film_id: str
    title: str
    ready: bool
    final_video: str | None
    error: str | None = None


@dataclass
class ReleaseReport:
    expected_films: int
    ready_films: int
    failed_films: int
    release_ready: bool
    films: list[FilmReleaseStatus]


class AJVYRAWanFull30ReleaseRunner:

    def __init__(
        self,
        production_root: str | Path = "ajvyra_wan_production",
        model_id: str = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    ) -> None:

        self.root = Path(production_root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.story_adapter = AJVYRAWanCinematicStoryAdapter()

        self.pipeline = AJVYRAWanFullCinematicFilmPipeline(
            production_root=self.root,
            model_id=model_id,
        )

    def status(self) -> ReleaseReport:

        films = []

        for story in self.story_adapter.all():

            result_file = (
                self.root
                / story.film_id
                / "film_pipeline_result.json"
            )

            if not result_file.exists():

                films.append(
                    FilmReleaseStatus(
                        film_id=story.film_id,
                        title=story.title,
                        ready=False,
                        final_video=None,
                        error="Film has not been produced yet.",
                    )
                )

                continue

            data = json.loads(
                result_file.read_text(
                    encoding="utf-8"
                )
            )

            films.append(
                FilmReleaseStatus(
                    film_id=story.film_id,
                    title=story.title,
                    ready=bool(data.get("ready")),
                    final_video=data.get("final_video"),
                    error=data.get("error"),
                )
            )

        ready_count = sum(
            1 for film in films if film.ready
        )

        failed_count = len(films) - ready_count

        return ReleaseReport(
            expected_films=len(films),
            ready_films=ready_count,
            failed_films=failed_count,
            release_ready=(
                len(films) == 30
                and ready_count == 30
            ),
            films=films,
        )

    def save_report(
        self,
        report: ReleaseReport,
    ) -> Path:

        path = self.root / "release_report.json"

        path.write_text(
            json.dumps(
                asdict(report),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return path

    def run(
        self,
        start: int = 1,
        end: int = 30,
        duration_seconds: int = 1800,
        require_audio: bool = True,
    ) -> ReleaseReport:

        stories = self.story_adapter.all()

        selected = stories[
            max(0, start - 1):min(end, len(stories))
        ]

        for index, story in enumerate(selected, start=start):

            print(
                f"\n[{index}/{len(stories)}] "
                f"Producing {story.title}..."
            )

            result = self.pipeline.produce(
                film_id=story.film_id,
                duration_seconds=duration_seconds,
                require_audio=require_audio,
            )

            if result.ready:
                print(
                    f"READY: {story.title}"
                )
            else:
                print(
                    f"FAILED: {story.title}"
                )
                print(
                    f"Reason: {result.error}"
                )

        report = self.status()
        self.save_report(report)

        print("\n==============================")
        print("AJVYRA CINEMATIC RELEASE GATE")
        print("==============================")
        print(
            f"Films ready: "
            f"{report.ready_films}/{report.expected_films}"
        )

        if report.release_ready:
            print("RELEASE READY: 30/30 films are ready.")
        else:
            print(
                "RELEASE BLOCKED: "
                "30 real finished films are required."
            )

        return report


def main() -> int:

    parser = argparse.ArgumentParser(
        description="AJVYRA Wan 30-film release runner"
    )

    parser.add_argument(
        "--start",
        type=int,
        default=1,
    )

    parser.add_argument(
        "--end",
        type=int,
        default=30,
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=1800,
    )

    parser.add_argument(
        "--model",
        default="Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    )

    parser.add_argument(
        "--no-audio",
        action="store_true",
    )

    args = parser.parse_args()

    runner = AJVYRAWanFull30ReleaseRunner(
        model_id=args.model,
    )

    report = runner.run(
        start=args.start,
        end=args.end,
        duration_seconds=args.duration,
        require_audio=not args.no_audio,
    )

    return 0 if report.release_ready else 2


if __name__ == "__main__":
    raise SystemExit(main())
