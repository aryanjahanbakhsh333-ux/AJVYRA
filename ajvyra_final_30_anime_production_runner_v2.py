from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

FILMS = [
    "Veylora",
    "Aelvryn",
    "Nyxara",
    "Kaelith",
    "Orivane",
    "Zeravia",
    "Vaelune",
    "Ravelyth",
    "Solvarya",
    "Xaveren",
    "Elyvara",
    "Neravelle",
    "Vaerith",
    "Lunavyr",
    "Averlyn",
    "Neyvara",
    "Elvaria",
    "Virelya",
    "Caelora",
    "Seravyn",
    "Mouravia",
    "Noxelya",
    "Vaelora",
    "Eryndra",
    "Neylith",
    "Auralyne",
    "Velmora",
    "Seyravia",
    "Oryvane",
    "Luminarae",
]


class AJVYRAFinal30AnimeRunner:

    def __init__(
        self,
        output_root: str = "assets/anime-final",
        producer_script: str = (
            "ajvyra_30_real_anime_batch_factory_v1.py"
        ),
    ):
        self.output_root = Path(output_root)
        self.producer_script = Path(producer_script)

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def slug(value: str) -> str:
        return "".join(
            char.lower() if char.isalnum() else "_"
            for char in value
        ).strip("_")

    def verify_movie(self, title: str) -> Path:
        movie = (
            self.output_root /
            f"{self.slug(title)}.mp4"
        )

        if not movie.exists():
            raise RuntimeError(
                f"REAL ANIME MISSING: {title}"
            )

        if movie.stat().st_size < 10_000:
            raise RuntimeError(
                f"REAL ANIME FILE INVALID: {title}"
            )

        return movie

    def run_generation(self):

        if not self.producer_script.exists():
            raise FileNotFoundError(
                self.producer_script
            )

        subprocess.run(
            [
                sys.executable,
                str(self.producer_script),
            ],
            check=True,
        )

    def build_index(self):

        records = []

        for number, title in enumerate(
            FILMS,
            start=1,
        ):
            movie = self.verify_movie(title)

            records.append(
                {
                    "id": f"ajvyra-anime-{number:02d}",
                    "title": title,
                    "number": number,
                    "video": str(movie),
                    "real_asset": True,
                    "ready": True,
                    "published": True,
                }
            )

        if len(records) != 30:
            raise RuntimeError(
                "FINAL ANIME COUNT IS NOT 30"
            )

        index = {
            "type": "ajvyra-final-anime",
            "count": 30,
            "items": records,
        }

        output = (
            self.output_root /
            "ajvyra-final-30-anime.json"
        )

        output.write_text(
            json.dumps(
                index,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return output

    def execute(self):

        self.run_generation()

        index = self.build_index()

        print(
            "\nAJVYRA ANIME COMPLETE: 30/30"
        )

        print(index)


if __name__ == "__main__":
    AJVYRAFinal30AnimeRunner().execute()ج
