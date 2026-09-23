from __future__ import annotations

import subprocess
import sys
from pathlib import Path


class AJVYRA60RealProductionMaster:

    def __init__(
        self,
        python: str | None = None,
    ):
        self.python = (
            python
            or sys.executable
        )

    def run(
        self,
        script: str,
    ):

        path = Path(script)

        if not path.exists():
            raise FileNotFoundError(
                path
            )

        print(
            f"\n[AJVYRA] RUNNING {path.name}\n"
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
                f"Production step failed: "
                f"{path.name}"
            )

    def produce_anime(self):

        self.run(
            "ajvyra_30_real_anime_batch_factory_v1.py"
        )

    def produce_games(self):

        self.run(
            "ajvyra_30_real_game_batch_factory_v1.py"
        )

    def export_games(self):

        self.run(
            "ajvyra_30_real_game_export_batch_v1.py"
        )

    def build_release_index(self):

        self.run(
            "ajvyra_60_real_asset_release_index_v1.py"
        )

    def execute(self):

        print(
            "\n"
            "========================================\n"
            "       AJVYRA 60 REAL ASSET FACTORY\n"
            "========================================\n"
        )

        print(
            "\n[1/4] REAL ANIME PRODUCTION"
        )

        self.produce_anime()

        print(
            "\n[2/4] REAL GAME PRODUCTION"
        )

        self.produce_games()

        print(
            "\n[3/4] REAL GAME EXPORT"
        )

        self.export_games()

        print(
            "\n[4/4] REAL RELEASE INDEX"
        )

        self.build_release_index()

        print(
            "\n"
            "========================================\n"
            "        AJVYRA 60/60 RELEASE READY\n"
            "        30 REAL ANIME\n"
            "        30 REAL GAMES\n"
            "========================================\n"
        )


if __name__ == "__main__":

    master = AJVYRA60RealProductionMaster()

    master.execute()
