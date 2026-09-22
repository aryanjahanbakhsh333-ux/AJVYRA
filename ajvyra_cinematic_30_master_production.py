from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

from ajvyra_cinematic_30_production_manifest import (
    CinematicFilmManifest,
)
from ajvyra_cinematic_30_queue_builder import (
    AJVYRACinematic30QueueBuilder,
    QueueBuildReport,
)
from ajvyra_cinematic_master_catalog import (
    AJVYRA_CINEMATIC_30_CATALOG,
)


@dataclass
class MasterProductionReport:
    total_films: int
    queue_tasks: int
    manifest_path: str
    films: List[Dict]


class AJVYRACinematic30MasterProduction:

    def __init__(
        self,
        root: str | Path = "cinematic_production",
    ):
        self.root = Path(root)

        self.builder = (
            AJVYRACinematic30QueueBuilder(
                self.root
            )
        )

    def build_all(
        self,
    ) -> MasterProductionReport:

        manifests = []

        for item in AJVYRA_CINEMATIC_30_CATALOG:

            film = CinematicFilmManifest(
                film_id=item.film_id,
                title=item.title,
                genre=item.genre,
                duration_seconds=1800,
                metadata={
                    "catalog_source": (
                        "AJVYRA_CINEMATIC_30_CATALOG"
                    ),
                },
            )

            manifests.append(film)

        report: QueueBuildReport = (
            self.builder.build(
                manifests
            )
        )

        result = MasterProductionReport(
            total_films=report.films_added,
            queue_tasks=report.tasks_created,
            manifest_path=report.manifest_path,
            films=[
                asdict(film)
                for film in manifests
            ],
        )

        output = (
            self.root
            / "master_production_report.json"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                asdict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return result


if __name__ == "__main__":

    production = (
        AJVYRACinematic30MasterProduction()
    )

    report = production.build_all()

    print(
        json.dumps(
            asdict(report),
            ensure_ascii=False,
            indent=2,
        )
    )
