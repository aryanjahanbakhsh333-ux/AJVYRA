from __future__ import annotations

import json
from pathlib import Path


class AJVYRAWan30FinalReleaseManifestV2:

    FILMS = [
        ("veylora", "Veylora"),
        ("aelvryn", "Aelvryn"),
        ("nyxara", "Nyxara"),
        ("kaelith", "Kaelith"),
        ("orivane", "Orivane"),
        ("zeravia", "Zeravia"),
        ("vaelune", "Vaelune"),
        ("ravelyth", "Ravelyth"),
        ("solvarya", "Solvarya"),
        ("xaveren", "Xaveren"),
        ("elyvara", "Elyvara"),
        ("neravelle", "Neravelle"),
        ("vaerith", "Vaerith"),
        ("lunavyr", "Lunavyr"),
        ("averlyn", "Averlyn"),
        ("neyvara", "Neyvara"),
        ("elvaria", "Elvaria"),
        ("virelya", "Virelya"),
        ("caelora", "Caelora"),
        ("seravyn", "Seravyn"),
        ("mouravia", "Mouravia"),
        ("noxelya", "Noxelya"),
        ("vaelora", "Vaelora"),
        ("eryndra", "Eryndra"),
        ("neylith", "Neylith"),
        ("auralyne", "Auralyne"),
        ("velmora", "Velmora"),
        ("seyravia", "Seyravia"),
        ("oryvane", "Oryvane"),
        ("luminarae", "Luminarae"),
    ]

    def __init__(
        self,
        output_path: str,
    ):
        self.output_path = Path(
            output_path
        )

    def build(
        self,
        qc_results: dict,
    ) -> dict:

        if len(qc_results) != 30:
            raise RuntimeError(
                "Release manifest requires "
                "exactly 30 films."
            )

        manifest = {
            "project": "AJVYRA",
            "status": "READY",
            "films": [],
        }

        for film_id, title in self.FILMS:

            result = qc_results.get(
                film_id
            )

            if not result:
                raise RuntimeError(
                    f"Missing QC result: {film_id}"
                )

            if not result.get("passed"):
                raise RuntimeError(
                    f"Film failed QC: {film_id}"
                )

            manifest["films"].append(
                {
                    "id": film_id,
                    "title": title,
                    "status": "READY",
                    "video": result["video"],
                    "duration": result["duration"],
                    "size": result["size"],
                }
            )

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.output_path.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return manifest
