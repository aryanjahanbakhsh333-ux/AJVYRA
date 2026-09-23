"""
AJVYRA — REAL ANIME JOB STORE v1

Persistent queue state.

اگر سیستم خاموش شود، Jobهای کامل‌شده دوباره تولید نمی‌شوند.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class AnimeJobStore:

    def __init__(self, path: Path):
        self.path = path

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.path.exists():
            self.save(
                {
                    "version": 1,
                    "jobs": {},
                }
            )

    def load(self) -> dict:
        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    def save(self, data: dict) -> None:
        temporary = self.path.with_suffix(
            self.path.suffix + ".tmp"
        )

        temporary.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        temporary.replace(self.path)

    def key(
        self,
        anime_number: int,
        segment_number: int,
    ) -> str:
        return (
            f"anime_{anime_number:02d}"
            f"_segment_{segment_number:02d}"
        )

    def get(
        self,
        anime_number: int,
        segment_number: int,
    ) -> dict | None:

        data = self.load()

        return data["jobs"].get(
            self.key(
                anime_number,
                segment_number,
            )
        )

    def set(
        self,
        anime_number: int,
        segment_number: int,
        **values: Any,
    ) -> None:

        data = self.load()

        key = self.key(
            anime_number,
            segment_number,
        )

        current = data["jobs"].get(
            key,
            {},
        )

        current.update(values)

        data["jobs"][key] = current

        self.save(data)

    def completed(
        self,
        anime_number: int,
        segment_number: int,
        output_path: Path,
    ) -> bool:

        record = self.get(
            anime_number,
            segment_number,
        )

        if not record:
            return False

        if record.get("status") != "complete":
            return False

        if not output_path.exists():
            return False

        if output_path.stat().st_size < 100_000:
            return False

        return True
