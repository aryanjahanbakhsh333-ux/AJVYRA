from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass
class ProductionQueueItem:
    anime_id: str
    title: str
    genre: str
    episode: int
    status: str = "queued"
    attempts: int = 0
    output: str = ""


class AJVYRAAnimeAutoProductionQueue:

    def __init__(
        self,
        root: str = "generated/anime_production",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.queue_file = (
            self.root / "production_queue.json"
        )

    def create_queue(
        self,
        catalog: List[Dict],
    ) -> List[ProductionQueueItem]:

        queue = [
            ProductionQueueItem(
                anime_id=item["anime_id"],
                title=item["title"],
                genre=item["genre"],
                episode=1,
            )
            for item in catalog
        ]

        self.save(queue)

        return queue

    def load(self) -> List[ProductionQueueItem]:

        if not self.queue_file.exists():
            return []

        data = json.loads(
            self.queue_file.read_text(
                encoding="utf-8"
            )
        )

        return [
            ProductionQueueItem(**item)
            for item in data
        ]

    def save(
        self,
        queue: List[ProductionQueueItem],
    ):

        self.queue_file.write_text(
            json.dumps(
                [
                    asdict(item)
                    for item in queue
                ],
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def next_item(
        self,
    ) -> ProductionQueueItem | None:

        queue = self.load()

        for item in queue:
            if item.status in (
                "queued",
                "failed",
            ):
                return item

        return None

    def mark_running(
        self,
        anime_id: str,
    ):

        queue = self.load()

        for item in queue:
            if item.anime_id == anime_id:
                item.status = "running"
                item.attempts += 1

        self.save(queue)

    def mark_completed(
        self,
        anime_id: str,
        output: str,
    ):

        queue = self.load()

        for item in queue:
            if item.anime_id == anime_id:
                item.status = "completed"
                item.output = output

        self.save(queue)

    def mark_failed(
        self,
        anime_id: str,
    ):

        queue = self.load()

        for item in queue:
            if item.anime_id == anime_id:
                item.status = "failed"

        self.save(queue)

    def status(self) -> Dict:

        queue = self.load()

        counts = {}

        for item in queue:
            counts[item.status] = (
                counts.get(item.status, 0) + 1
            )

        return {
            "total": len(queue),
            "counts": counts,
        }
