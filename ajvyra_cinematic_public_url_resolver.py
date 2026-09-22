from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class ResolvedPublicURL:
    film_id: str
    url: str
    source: str
    is_external: bool


class AJVYRACinematicPublicURLResolver:
    """
    Converts catalog movie records into URLs usable by the web player.

    Priority:
        1. Explicit movie_url
        2. Explicit public_url
        3. Configured external media base URL
        4. Local Pages-style path
    """

    def __init__(self, media_base_url: Optional[str] = None) -> None:
        self.media_base_url = (
            media_base_url
            or os.getenv("AJVYRA_CINEMATIC_MEDIA_BASE_URL")
            or ""
        ).rstrip("/")

    def resolve(
        self,
        film_id: str,
        record: Optional[Mapping[str, Any]] = None,
    ) -> ResolvedPublicURL:
        record = record or {}

        explicit = (
            record.get("movie_url")
            or record.get("public_url")
            or record.get("video_url")
        )

        if explicit:
            url = str(explicit).strip()
            return ResolvedPublicURL(
                film_id=film_id,
                url=url,
                source="catalog",
                is_external=self._is_external(url),
            )

        if self.media_base_url:
            url = f"{self.media_base_url}/{film_id}/movie.mp4"

            return ResolvedPublicURL(
                film_id=film_id,
                url=url,
                source="external-storage",
                is_external=True,
            )

        url = f"/cinematic_anime/{film_id}/movie.mp4"

        return ResolvedPublicURL(
            film_id=film_id,
            url=url,
            source="local-site",
            is_external=False,
        )

    @staticmethod
    def _is_external(url: str) -> bool:
        parsed = urlparse(url)

        return parsed.scheme in {
            "http",
            "https",
        }
