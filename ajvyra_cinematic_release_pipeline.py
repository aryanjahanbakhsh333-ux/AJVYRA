from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json

from ajvyra_cinematic_site_movie_registry import (
    AJVYRACinematicSiteMovieRegistry,
)
from ajvyra_cinematic_static_player_manifest import (
    AJVYRAStaticPlayerManifest,
)
from ajvyra_cinematic_release_verifier import (
    AJVYRACinematicReleaseVerifier,
)


class AJVYRACinematicReleasePipeline:
    """
    Final bridge between the cinematic production output
    and the website's playable movie catalog.

    It never creates fake movies.
    It only publishes movies that already exist as valid MP4 files.
    """

    def __init__(
        self,
        production_root: str | Path = "public/cinematic_anime",
        public_root: str | Path = "public",
        expected_movies: int = 30,
    ) -> None:

        self.production_root = Path(production_root)
        self.public_root = Path(public_root)
        self.expected_movies = expected_movies

        self.registry = AJVYRACinematicSiteMovieRegistry(
            production_root=self.production_root
        )

        self.player_manifest = AJVYRAStaticPlayerManifest(
            public_root=self.public_root
        )

        self.verifier = AJVYRACinematicReleaseVerifier(
            expected_count=expected_movies
        )

    def load_master_catalog(
        self,
        catalog_path: str | Path,
    ) -> list[dict]:

        path = Path(catalog_path)

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        if isinstance(data, list):
            return data

        if "films" in data:
            return data["films"]

        if "movies" in data:
            return data["movies"]

        raise ValueError(
            "Cinematic master catalog has no films/movies list."
        )

    def run(
        self,
        master_catalog_path: str | Path,
    ) -> dict:

        catalog = self.load_master_catalog(
            master_catalog_path
        )

        registered = self.registry.build_registry(
            catalog
        )

        registry_path = self.public_root / (
            "cinematic_site_movie_registry.json"
        )

        self.registry.save_registry(
            registered,
            registry_path,
        )

        player_manifest_path = (
            self.player_manifest.build(
                registry_path=registry_path
            )
        )

        verification = self.verifier.verify(
            registry_path
        )

        verification_path = (
            self.public_root /
            "cinematic_release_verification.json"
        )

        self.verifier.save_report(
            verification,
            verification_path,
        )

        release = {
            "version": "1",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "ready": verification.ready,
            "required_movies": verification.required_movies,
            "watchable_movies": verification.watchable_movies,
            "missing_movies": verification.missing_movies,
            "registry": str(registry_path),
            "player_manifest": str(player_manifest_path),
            "verification": str(verification_path),
        }

        release_path = (
            self.public_root /
            "cinematic_release.json"
        )

        release_path.write_text(
            json.dumps(
                release,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return release


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build AJVYRA cinematic release."
    )

    parser.add_argument(
        "--catalog",
        required=True,
        help="Path to the cinematic master catalog JSON.",
    )

    parser.add_argument(
        "--production-root",
        default="public/cinematic_anime",
    )

    parser.add_argument(
        "--public-root",
        default="public",
    )

    parser.add_argument(
        "--expected-movies",
        type=int,
        default=30,
    )

    args = parser.parse_args()

    pipeline = AJVYRACinematicReleasePipeline(
        production_root=args.production_root,
        public_root=args.public_root,
        expected_movies=args.expected_movies,
    )

    result = pipeline.run(
        master_catalog_path=args.catalog
    )

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    ))

    if not result["ready"]:
        raise SystemExit(
            "RELEASE BLOCKED: real cinematic movies are missing."
        )

    print(
        "AJVYRA CINEMATIC RELEASE READY: "
        "all required movies are watchable."
    )
