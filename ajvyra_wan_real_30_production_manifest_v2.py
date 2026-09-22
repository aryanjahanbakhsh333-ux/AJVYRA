from __future__ import annotations

import json
from pathlib import Path


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


class AJVYRAReal30ProductionManifestV2:

    def __init__(self, path: str):
        self.path = Path(path)

    def create_from_story_database(
        self,
        story_database: dict,
    ) -> dict:

        manifest = {}

        for film_id, title in FILMS:

            source = story_database.get(film_id)

            if not source:
                raise ValueError(
                    f"Story database has no entry for {film_id}"
                )

            scenes = source.get("scenes", [])

            if not scenes:
                raise ValueError(
                    f"{film_id} has no scenes."
                )

            shots = []

            shot_number = 1

            for scene in scenes:

                scene_prompt = scene.get(
                    "visual_prompt"
                )

                if scene_prompt:

                    shots.append(
                        {
                            "shot_id": f"shot_{shot_number:04d}",
                            "scene_id": scene.get(
                                "scene_id",
                                f"scene_{shot_number:04d}",
                            ),
                            "prompt": scene_prompt,
                            "seed": shot_number,
                        }
                    )

                    shot_number += 1

            if not shots:
                raise ValueError(
                    f"{film_id} has scenes but no "
                    f"visual prompts."
                )

            manifest[film_id] = {
                "title": title,
                "shots": shots,
            }

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.path.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return manifest
