from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import quote


@dataclass(frozen=True)
class CinematicStorageObject:
    film_id: str
    local_path: Path
    public_url: str


class AJVYRACinematicStorageAdapter:
    """
    Resolves locally generated cinematic MP4 files into public URLs.

    The actual storage provider is intentionally abstracted away.
    For GitHub Pages, the recommended approach is to keep large MP4 files
    outside the Pages artifact and expose them through a CDN/object store.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        local_root: str | Path = "public/cinematic_anime",
    ) -> None:
        self.base_url = (
            base_url
            or os.getenv("AJVYRA_CINEMATIC_MEDIA_BASE_URL")
            or ""
        ).rstrip("/")

        self.local_root = Path(local_root)

    def resolve(
        self,
        film_id: str,
        filename: str = "movie.mp4",
    ) -> CinematicStorageObject:
        film_id = self._safe_segment(film_id)
        filename = self._safe_filename(filename)

        local_path = self.local_root / film_id / filename

        if self.base_url:
            public_url = (
                f"{self.base_url}/"
                f"{quote(film_id)}/"
                f"{quote(filename)}"
            )
        else:
            public_url = (
                f"/cinematic_anime/"
                f"{quote(film_id)}/"
                f"{quote(filename)}"
            )

        return CinematicStorageObject(
            film_id=film_id,
            local_path=local_path,
            public_url=public_url,
        )

    def exists_locally(
        self,
        film_id: str,
        filename: str = "movie.mp4",
    ) -> bool:
        return self.resolve(film_id, filename).local_path.is_file()

    @staticmethod
    def _safe_segment(value: str) -> str:
        value = str(value).strip()

        if not value:
            raise ValueError("film_id cannot be empty")

        if value in {".", ".."}:
            raise ValueError("Invalid film_id")

        if "/" in value or "\\" in value:
            raise ValueError("film_id cannot contain path separators")

        return value

    @staticmethod
    def _safe_filename(value: str) -> str:
        value = str(value).strip()

        if not value:
            raise ValueError("filename cannot be empty")

        if "/" in value or "\\" in value:
            raise ValueError("filename cannot contain path separators")

        if value in {".", ".."}:
            raise ValueError("Invalid filename")

        return value
