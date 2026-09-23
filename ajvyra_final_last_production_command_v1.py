from __future__ import annotations

import subprocess
import sys
from pathlib import Path


STEPS = [
    (
        "30 REAL ANIME",
        "ajvyra_final_30_anime_production_runner_v2.py",
    ),
    (
        "30 REAL GAME WEB BUILDS",
        "ajvyra_final_30_game_web_export_v2.py",
    ),
    (
        "60 REAL SITE ASSETS",
        "ajvyra_final_60_asset_site_materializer_v1.py",
    ),
    (
        "FINAL 60-ASSET RELEASE GATE",
        "ajvyra_final_60_release_gate_v1.py",
    ),
]


class AJVYRAFinalLastProductionCommand:

    def __init__(
        self,
        python: str | None = None,
    ):
        self.python = (
            python
            or sys.executable
        )

    def execute_step(
        self,
        title: str,
        script: str,
    ):

        print(
            "\n"
            "===================================="
        )

        print(
            f"AJVYRA: {title}"
        )

        print(
            "===================================="
        )

        path = Path(script)

        if not path.exists():
            raise RuntimeError(
                f"Required production file missing: "
                f"{script}"
            )

        result = subprocess.run(
            [
                self.python,
                str(path),
            ],
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"PRODUCTION STOPPED AT: {title}"
            )

    def execute(self):

        for title, script in STEPS:
            self.execute_step(
                title,
                script,
            )

        print(
            "\n"
            "################################################\n"
            "#                                              #\n"
            "#       AJVYRA FINAL 60/60 COMPLETE           #\n"
            "#                                              #\n"
            "#       30 REAL ANIME                          #\n"
            "#       30 REAL GAMES                          #\n"
            "#       60 REAL SITE ASSETS                    #\n"
            "#                                              #\n"
            "#       SITE RELEASE: APPROVED                 #\n"
            "#                                              #\n"
            "################################################\n"
        )


if __name__ == "__main__":
    AJVYRAFinalLastProductionCommand().execute()
