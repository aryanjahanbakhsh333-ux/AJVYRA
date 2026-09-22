from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

from ajvyra_wan_final_cinematic_release_factory import (
    AJVYRAWanFinalCinematicReleaseFactory,
)


@dataclass
class SiteMovie:
    film_id: str
    title: str
    url: str
    duration_seconds: float
    sha256: str
    watchable: bool


@dataclass
class FinalSiteRelease:
    expected: int
    ready: int
    blocked: int
    release_ready: bool
    movies: list[SiteMovie]


class AJVYRAWanFinal30ReleaseGate:

    def __init__(
        self,
        production_root: str | Path = "ajvyra_final_release",
        public_root: str | Path = "public",
    ):

        self.production_root = Path(
            production_root
        )

        self.public_root = Path(
            public_root
        )

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def checksum(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as handle:

            while True:

                block = handle.read(
                    1024 * 1024
                )

                if not block:
                    break

                digest.update(block)

        return digest.hexdigest()

    @staticmethod
    def duration(
        path: Path,
    ) -> float:

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr
            )

        return float(
            result.stdout.strip()
        )

    def build(
        self,
        expected: int = 30,
    ) -> FinalSiteRelease:

        movies = []

        for result_file in sorted(
            self.production_root.glob(
                "*/FINAL_RELEASE.json"
            )
        ):

            data = json.loads(
                result_file.read_text(
                    encoding="utf-8"
                )
            )

            if not data.get(
                "final_movie_ready"
            ):
                continue

            source = Path(
                data["final_movie"]
            )

            if not source.exists():
                continue

            duration = self.duration(
                source
            )

            if duration < 1500:
                continue

            film_id = data[
                "film_id"
            ]

            title = data[
                "title"
            ]

            destination = (
                self.public_root
                / "cinematic_anime"
                / film_id
                / "movie.mp4"
            )

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source,
                destination,
            )

            checksum = self.checksum(
                destination
            )

            movies.append(
                SiteMovie(
                    film_id=film_id,
                    title=title,
                    url=(
                        f"/cinematic_anime/"
                        f"{film_id}/movie.mp4"
                    ),
                    duration_seconds=duration,
                    sha256=checksum,
                    watchable=True,
                )
            )

        release_ready = (
            len(movies) == expected
        )

        catalog = {
            "version": 1,
            "expected_movies": expected,
            "watchable_movies": len(
                movies
            ),
            "release_ready": release_ready,
            "movies": [
                asdict(movie)
                for movie in movies
            ],
        }

        catalog_path = (
            self.public_root
            / "cinematic_player_manifest.json"
        )

        catalog_path.write_text(
            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        release = FinalSiteRelease(
            expected=expected,
            ready=len(movies),
            blocked=max(
                0,
                expected - len(movies),
            ),
            release_ready=release_ready,
            movies=movies,
        )

        (
            self.public_root
            / "FINAL_SITE_RELEASE.json"
        ).write_text(
            json.dumps(
                asdict(release),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return release


def main() -> int:

    gate = AJVYRAWanFinal30ReleaseGate()

    release = gate.build(
        expected=30
    )

    print()
    print(
        "======================================"
    )
    print(
        "      AJVYRA FINAL RELEASE GATE"
    )
    print(
        "======================================"
    )

    print(
        f"Ready: {release.ready}/30"
    )

    print(
        f"Blocked: {release.blocked}"
    )

    if release.release_ready:

        print(
            "RELEASE READY — 30/30"
        )

        return 0

    print(
        "RELEASE BLOCKED — 30 real movies required."
    )

    return 2


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
