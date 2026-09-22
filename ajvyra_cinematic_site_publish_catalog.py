from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class CinematicWatchEntry:
    film_id: str
    title: str
    movie_path: str
    duration_seconds: float
    status: str
    checksum_sha256: str
    published_at: float


class AJVYRACinematicSitePublishCatalog:
    """
    Site-facing catalog for completed cinematic films.

    Only physically existing, QC-approved masters are exposed as READY.
    """

    def __init__(
        self,
        catalog_path: str | Path,
        public_root: str | Path,
    ) -> None:
        self.catalog_path = Path(catalog_path)
        self.public_root = Path(public_root)

        self.catalog_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.public_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.entries: dict[str, CinematicWatchEntry] = {}
        self._load()

    def publish(
        self,
        film_id: str,
        title: str,
        source_movie: str | Path,
        duration_seconds: float,
        *,
        qc_passed: bool,
    ) -> CinematicWatchEntry:

        if not qc_passed:
            raise RuntimeError(
                f"Film '{film_id}' cannot be published because QC failed."
            )

        source = Path(source_movie)

        if not source.exists():
            raise FileNotFoundError(
                f"Cannot publish missing movie: {source}"
            )

        if source.stat().st_size <= 0:
            raise RuntimeError(
                f"Cannot publish empty movie: {source}"
            )

        film_dir = self.public_root / film_id
        film_dir.mkdir(parents=True, exist_ok=True)

        destination = film_dir / "movie.mp4"

        self._copy_file(source, destination)

        checksum = self._sha256(destination)

        entry = CinematicWatchEntry(
            film_id=film_id,
            title=title,
            movie_path=str(destination),
            duration_seconds=float(duration_seconds),
            status="READY",
            checksum_sha256=checksum,
            published_at=time.time(),
        )

        self.entries[film_id] = entry
        self._save()

        return entry

    def unpublish(self, film_id: str) -> bool:
        entry = self.entries.pop(film_id, None)

        if entry is None:
            return False

        self._save()
        return True

    def get(self, film_id: str) -> Optional[CinematicWatchEntry]:
        return self.entries.get(film_id)

    def list_ready(self) -> list[CinematicWatchEntry]:
        return [
            entry
            for entry in self.entries.values()
            if entry.status == "READY"
            and Path(entry.movie_path).exists()
        ]

    def is_watchable(self, film_id: str) -> bool:
        entry = self.get(film_id)

        if entry is None:
            return False

        if entry.status != "READY":
            return False

        path = Path(entry.movie_path)

        return path.exists() and path.stat().st_size > 0

    def export(self) -> dict:
        return {
            "films": [
                asdict(entry)
                for entry in self.list_ready()
            ]
        }

    def _copy_file(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        import shutil

        shutil.copy2(source, destination)

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda: handle.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()

    def _save(self) -> None:
        with self.catalog_path.open(
            "w",
            encoding="utf-8",
        ) as handle:
            json.dump(
                self.export(),
                handle,
                ensure_ascii=False,
                indent=2,
            )

    def _load(self) -> None:
        if not self.catalog_path.exists():
            return

        try:
            data = json.loads(
                self.catalog_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return

        for raw in data.get("films", []):
            try:
                entry = CinematicWatchEntry(**raw)
                self.entries[entry.film_id] = entry
            except TypeError:
                continue
