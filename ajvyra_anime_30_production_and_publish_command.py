from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


class AJVYRAAnime30ProductionAndPublishCommand:

    def __init__(
        self,
        root: str = "generated/anime_production",
    ):
        self.root = Path(root)

    def sync_only(self):

        from ajvyra_anime_production_to_site_bridge import (
            AJVYRAAnimeProductionToSiteBridge,
        )

        result = (
            AJVYRAAnimeProductionToSiteBridge(
                production_root=str(
                    self.root
                )
            ).sync()
        )

        self._print(result)

    def status(self):

        from ajvyra_anime_watchable_catalog import (
            AJVYRAWatchableAnimeCatalog,
        )

        result = (
            AJVYRAWatchableAnimeCatalog()
            .build()
        )

        self._print(result)

    def _print(
        self,
        data: Dict[str, Any],
    ):

        print(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            )
        )


def main():

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA 30 Anime "
            "Production/Publishing Controller"
        )
    )

    parser.add_argument(
        "command",
        choices=[
            "sync",
            "status",
        ],
    )

    args = parser.parse_args()

    command = (
        AJVYRAAnime30ProductionAndPublishCommand()
    )

    if args.command == "sync":
        command.sync_only()

    elif args.command == "status":
        command.status()


if __name__ == "__main__":
    main()
