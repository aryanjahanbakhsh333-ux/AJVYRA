from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from ajvyra_cinematic_public_url_resolver import (
    AJVYRACinematicPublicURLResolver,
)


@dataclass(frozen=True)
class DeployMovie:
    film_id: str
    title: str
    genre: str
    duration_seconds: float
    movie_url: str
    poster_url: str | None
    subtitle_urls: dict[str, str]
    watchable: bool


class AJVYRACinematicDeployManifestBuilder:
    """
    Builds the browser-facing manifest used by the cinematic site.

    Only records explicitly marked watchable are emitted.
    """

    def __init__(
        self,
        resolver: AJVYRACinematicPublicURLResolver | None = None,
    ) -> None:
        self.resolver = (
            resolver
            or AJVYRACinematicPublicURLResolver()
        )

    def build(
        self,
        records: Sequence[Mapping[str, Any]],
    ) -> dict[str, Any]:
        movies: list[dict[str, Any]] = []

        for record in records:
            if not self._is_watchable(record):
                continue

            film_id = str(record.get("film_id", "")).strip()

            if not film_id:
                continue

            resolved = self.resolver.resolve(
                film_id=film_id,
                record=record,
            )

            movie = DeployMovie(
                film_id=film_id,
                title=str(
                    record.get("title")
                    or film_id
                ),
                genre=str(
                    record.get("genre")
                    or "Cinematic Anime"
                ),
                duration_seconds=float(
                    record.get("duration_seconds", 0)
                ),
                movie_url=resolved.url,
                poster_url=self._optional_string(
                    record.get("poster_url")
                ),
                subtitle_urls=self._subtitle_urls(record),
                watchable=True,
            )

            movies.append(asdict(movie))

        return {
            "schema": "ajvyra.cinematic.deploy.v1",
            "watchable_count": len(movies),
            "movies": movies,
        }

    def save(
        self,
        records: Sequence[Mapping[str, Any]],
        output_path: str | Path,
    ) -> Path:
        payload = self.build(records)

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path

    @staticmethod
    def _is_watchable(record: Mapping[str, Any]) -> bool:
        return bool(
            record.get("watchable")
            or record.get("status") == "READY"
            or record.get("status") == "WATCHABLE"
        )

    @staticmethod
    def _optional_string(value: Any) -> str | None:
        if value is None:
            return None

        value = str(value).strip()

        return value or None

    @staticmethod
    def _subtitle_urls(
        record: Mapping[str, Any],
    ) -> dict[str, str]:
        raw = record.get("subtitle_urls")

        if isinstance(raw, Mapping):
            return {
                str(language): str(url)
                for language, url in raw.items()
                if str(url).strip()
            }

        subtitles: dict[str, str] = {}

        for language in ("fa", "en", "ja"):
            key = f"{language}_subtitle_url"
            value = record.get(key)

            if value:
                subtitles[language] = str(value)

        return subtitles
