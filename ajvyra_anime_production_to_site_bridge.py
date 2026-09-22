from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class AJVYRAAnimeProductionToSiteBridge:

    def __init__(
        self,
        production_root: str = (
            "generated/anime_production"
        ),
        public_root: str = "public/anime",
    ):
        self.production_root = Path(
            production_root
        )
        self.public_root = Path(
            public_root
        )

    def sync(self) -> Dict[str, Any]:

        from ajvyra_anime_real_30_publisher import (
            AJVYRAAnimeReal30Publisher,
        )

        publisher = AJVYRAAnimeReal30Publisher(
            production_root=str(
                self.production_root
            ),
            public_root=str(
                self.public_root
            ),
        )

        result = publisher.publish_all()

        from ajvyra_anime_watchable_catalog import (
            AJVYRAWatchableAnimeCatalog,
        )

        catalog = (
            AJVYRAWatchableAnimeCatalog(
                public_root=str(
                    self.public_root
                )
            ).build()
        )

        final = {
            "publisher": result,
            "watchable_catalog": catalog,
            "watchable_count": catalog[
                "total_watchable"
            ],
        }

        output = (
            self.production_root
            / "site_sync_report.json"
        )

        output.write_text(
            json.dumps(
                final,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return final
