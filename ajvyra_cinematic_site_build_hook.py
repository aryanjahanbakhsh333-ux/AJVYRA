from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from ajvyra_cinematic_deploy_manifest_builder import (
    AJVYRACinematicDeployManifestBuilder,
)


@dataclass(frozen=True)
class SiteBuildResult:
    success: bool
    movie_count: int
    manifest_path: str
    message: str


class AJVYRACinematicSiteBuildHook:
    """
    Final build hook for the static AJVYRA site.

    It never invents movies.
    It only publishes records that already passed the production pipeline.
    """

    def __init__(
        self,
        manifest_builder: AJVYRACinematicDeployManifestBuilder | None = None,
    ) -> None:
        self.builder = (
            manifest_builder
            or AJVYRACinematicDeployManifestBuilder()
        )

    def run(
        self,
        catalog_path: str | Path,
        output_manifest_path: str | Path,
        expected_movies: int = 30,
    ) -> SiteBuildResult:
        catalog_file = Path(catalog_path)

        if not catalog_file.is_file():
            return SiteBuildResult(
                success=False,
                movie_count=0,
                manifest_path=str(output_manifest_path),
                message=f"Catalog not found: {catalog_file}",
            )

        records = self._load_records(catalog_file)

        payload = self.builder.build(records)

        count = int(
            payload.get("watchable_count", 0)
        )

        output = Path(output_manifest_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        if count != expected_movies:
            return SiteBuildResult(
                success=False,
                movie_count=count,
                manifest_path=str(output),
                message=(
                    f"Build blocked: {count}/{expected_movies} "
                    "cinematic movies are watchable."
                ),
            )

        return SiteBuildResult(
            success=True,
            movie_count=count,
            manifest_path=str(output),
            message=(
                f"Build ready: {count} cinematic movies "
                "are available to the site."
            ),
        )

    @staticmethod
    def _load_records(
        path: Path,
    ) -> Sequence[Mapping[str, Any]]:
        payload = json.loads(
            path.read_text(encoding="utf-8")
        )

        if isinstance(payload, list):
            return payload

        if isinstance(payload, Mapping):
            movies = payload.get("movies")

            if isinstance(movies, list):
                return movies

        raise ValueError(
            "Unsupported cinematic catalog format."
        )
