from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict


class AJVYRAAuto30AnimeProducer:

    def __init__(
        self,
        root: str = "generated/anime_production",
    ):
        self.root = Path(root)

    def run(self):

        from ajvyra_anime_30_master_catalog import (
            AJVYRA30AnimeMasterCatalog,
        )

        from ajvyra_anime_auto_episode_director import (
            AJVYRAAutoEpisodeDirector,
        )

        from ajvyra_anime_auto_production_queue import (
            AJVYRAAnimeAutoProductionQueue,
        )

        catalog_builder = (
            AJVYRA30AnimeMasterCatalog(
                root=str(self.root)
            )
        )

        catalog_path = catalog_builder.save()

        catalog = json.loads(
            catalog_path.read_text(
                encoding="utf-8"
            )
        )

        entries = catalog["entries"]

        queue_engine = (
            AJVYRAAnimeAutoProductionQueue(
                root=str(self.root)
            )
        )

        queue = queue_engine.create_queue(
            entries
        )

        director = AJVYRAAutoEpisodeDirector(
            root=str(self.root)
        )

        from ajvyra_anime_real_production_master import (
            AJVYRAAnimeRealProductionMaster,
        )

        master = AJVYRAAnimeRealProductionMaster(
            root=str(self.root)
        )

        results = []

        for anime in entries:

            queue_engine.mark_running(
                anime["anime_id"]
            )

            try:

                story = director.create_episode(
                    anime
                )

                result = master.produce(
                    anime=anime,
                    story=story,
                )

                if result.get("success"):
                    queue_engine.mark_completed(
                        anime["anime_id"],
                        result.get(
                            "output_video",
                            "",
                        ),
                    )
                else:
                    queue_engine.mark_failed(
                        anime["anime_id"]
                    )

                results.append(result)

            except Exception as exc:

                queue_engine.mark_failed(
                    anime["anime_id"]
                )

                results.append(
                    {
                        "success": False,
                        "anime_id": anime[
                            "anime_id"
                        ],
                        "error": str(exc),
                    }
                )

        report = {
            "total_anime": 30,
            "completed": sum(
                1
                for item in results
                if item.get("success")
            ),
            "failed": sum(
                1
                for item in results
                if not item.get("success")
            ),
            "results": results,
        }

        report_path = (
            self.root
            / "30_anime_production_report.json"
        )

        report_path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":

    producer = AJVYRAAuto30AnimeProducer()

    result = producer.run()

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )
