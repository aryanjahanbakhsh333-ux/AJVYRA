import json
from pathlib import Path
from typing import Any


class CreatorMemory:

    def __init__(
        self,
        path: str = "ajvyra_creator_data/memory.json",
    ):
        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.data = self._load()

    def _load(self) -> dict[str, Any]:

        if not self.path.exists():
            return {
                "projects": [],
                "characters": [],
                "worlds": [],
                "locations": [],
            }

        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    def save(self) -> None:

        self.path.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def remember(
        self,
        category: str,
        item: dict[str, Any],
    ) -> None:

        if category not in self.data:
            self.data[category] = []

        self.data[category].append(item)

        self.save()

    def all(self, category: str) -> list:
        return list(
            self.data.get(category, [])
        )

    def exists(
        self,
        category: str,
        key: str,
        value: Any,
    ) -> bool:

        return any(
            item.get(key) == value
            for item in self.data.get(
                category,
                [],
            )
        )
