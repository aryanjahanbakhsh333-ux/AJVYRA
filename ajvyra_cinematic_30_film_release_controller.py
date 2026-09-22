from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from ajvyra_cinematic_complete_film_factory import (
    AJVYRACompleteCinematicFilmFactory,
    FilmFactoryStatus,
)


AJVYRA_30_FILMS = [
    ("anime_01", "Veylora"),
    ("anime_02", "Aelvryn"),
    ("anime_03", "Nyxara"),
    ("anime_04", "Kaelith"),
    ("anime_05", "Orivane"),
    ("anime_06", "Zeravia"),
    ("anime_07", "Vaelune"),
    ("anime_08", "Ravelyth"),
    ("anime_09", "Solvarya"),
    ("anime_10", "Xaveren"),
    ("anime_11", "Elyvara"),
    ("anime_12", "Neravelle"),
    ("anime_13", "Vaerith"),
    ("anime_14", "Lunavyr"),
    ("anime_15", "Averlyn"),
    ("anime_16", "Neyvara"),
    ("anime_17", "Elvaria"),
    ("anime_18", "Virelya"),
    ("anime_19", "Caelora"),
    ("anime_20", "Seravyn"),
    ("anime_21", "Mouravia"),
    ("anime_22", "Noxelya"),
    ("anime_23", "Vaelora"),
    ("anime_24", "Eryndra"),
    ("anime_25", "Neylith"),
    ("anime_26", "Auralyne"),
    ("anime_27", "Velmora"),
    ("anime_28", "Seyravia"),
    ("anime_29", "Oryvane"),
    ("anime_30", "Luminarae"),
]


class AJVYRA30FilmReleaseController:

    def __init__(
        self,
        production_root: str | Path = (
            "production/ajvyra_cinematic"
        ),
        public_root: str | Path = "public",
        external_media_base_url: str | None = None,
    ) -> None:

        self.production_root = Path(
            production_root
        )

        self.factory = (
            AJVYRACompleteCinematicFilmFactory(
                production_root=production_root,
                public_root=public_root,
                external_media_base_url=(
                    external_media_base_url
                ),
            )
        )

        self.external_media_base_url = (
            external_media_base_url
        )

    def run(
        self,
        *,
        start: int = 1,
        end: int = 30,
        resume: bool = True,
    ) -> list[FilmFactoryStatus]:

        if start < 1:
            start = 1

        if end > 30:
            end = 30

        if start > end:
            raise ValueError(
                "start cannot be greater than end."
            )

        results = []

        for index in range(
            start - 1,
            end,
        ):

            film_id, title = (
                AJVYRA_30_FILMS[index]
            )

            print(
                f"\n[{index + 1}/30] "
                f"BUILDING {title}"
            )

            result = (
                self.factory.build_film(
                    film_id,
                    resume=resume,
                    stop_on_error=True,
                )
            )

            results.append(
                result
            )

            print(
                f"STATUS: {result.status}"
            )

            if result.error:
                print(
                    f"ERROR: {result.error}"
                )

            self._save_controller_state(
                results
            )

        return results

    def _save_controller_state(
        self,
        results: list[FilmFactoryStatus],
    ) -> None:

        path = (
            self.production_root
            / "30_film_controller_state.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "total_films": 30,
            "processed": len(results),
            "ready": sum(
                1
                for result in results
                if result.site_ready
            ),
            "qc_passed": sum(
                1
                for result in results
                if result.qc_passed
            ),
            "failed": sum(
                1
                for result in results
                if result.status == "FAILED"
            ),
            "films": [
                result.__dict__
                for result in results
            ],
        }

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def status(self) -> dict[str, Any]:

        ready = 0
        qc = 0
        failed = 0

        states = []

        for film_id, title in AJVYRA_30_FILMS:

            path = (
                self.production_root
                / film_id
                / "factory_state.json"
            )

            if not path.exists():

                states.append(
                    {
                        "film_id": film_id,
                        "title": title,
                        "status": "NOT_STARTED",
                    }
                )

                continue

            try:

                state = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

            except Exception:

                state = {
                    "film_id": film_id,
                    "title": title,
                    "status": "INVALID_STATE",
                }

            states.append(state)

            if state.get(
                "site_ready"
            ):
                ready += 1

            if state.get(
                "qc_passed"
            ):
                qc += 1

            if state.get(
                "status"
            ) in {
                "FAILED",
                "QC_FAILED",
                "SEGMENT_GENERATION_FAILED",
            }:
                failed += 1

        return {
            "total": 30,
            "ready": ready,
            "qc_passed": qc,
            "failed": failed,
            "release_ready": ready == 30,
            "films": states,
        }
