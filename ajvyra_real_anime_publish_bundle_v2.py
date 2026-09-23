"""
AJVYRA — REAL ANIME PUBLISH BUNDLE v2

آخرین مرحله بسته دوم.

این فایل تا وقتی هر 30 anime واقعاً آماده نباشند
manifest قابل انتشار نمی‌سازد.

هیچ fake-success وجود ندارد.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_local_real_generation_config_v1 import (
    LocalGenerationConfig,
)
from ajvyra_real_anime_poster_extractor_v2 import (
    RealPosterExtractor,
)
from ajvyra_real_anime_manifest_v2 import (
    RealAnimeManifestBuilder,
)
from ajvyra_real_anime_release_validator_v2 import (
    AnimeReleaseValidator,
)


class RealAnimePublishBundle:

    def __init__(
        self,
        config: LocalGenerationConfig,
    ):
        self.config = config

        self.root = config.production_root

        self.poster_extractor = (
            RealPosterExtractor(
                config.ffmpeg_binary
            )
        )

        self.validator = (
            AnimeReleaseValidator(
                self.root,
                config.ffprobe_binary,
            )
        )

        self.manifest_builder = (
            RealAnimeManifestBuilder(
                self.root,
                config.ffprobe_binary,
            )
        )

    def create_posters(self):

        for number in range(1, 31):

            anime_dir = (
                self.root
                / f"anime_{number:02d}"
            )

            video = (
                anime_dir
                / "video"
                / "main.mp4"
            )

            poster = (
                anime_dir
                / "poster.jpg"
            )

            if not video.exists():
                raise RuntimeError(
                    f"Missing video for anime "
                    f"{number}"
                )

            if not poster.exists():
                self.poster_extractor.extract(
                    video,
                    poster,
                    timestamp=30.0,
                )

    def publish(self) -> Path:

        # مرحله 1:
        # Posterها از ویدیوی واقعی ساخته می‌شوند.
        self.create_posters()

        # مرحله 2:
        # Release Gate
        report = (
            self.validator
            .require_release_ready()
        )

        if report["ready"] != 30:
            raise RuntimeError(
                "Refusing to publish fewer than 30 anime."
            )

        # مرحله 3:
        # ساخت manifest واقعی
        manifest = (
            self.manifest_builder.build()
        )

        if manifest["count"] != 30:
            raise RuntimeError(
                "Manifest count is not 30."
            )

        # مرحله 4:
        # ذخیره manifest
        output = (
            self.root
            / "ajvyra_real_anime_manifest.json"
        )

        output.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        # مرحله 5:
        # Final verification
        verification = json.loads(
            output.read_text(
                encoding="utf-8"
            )
        )

        if len(
            verification["items"]
        ) != 30:
            raise RuntimeError(
                "Final manifest verification failed."
            )

        for item in verification["items"]:

            if not item["available"]:
                raise RuntimeError(
                    f"Unavailable anime: "
                    f"{item['number']}"
                )

            if item["duration_seconds"] < 1799:
                raise RuntimeError(
                    f"Anime is not 30 minutes: "
                    f"{item['number']}"
                )

        print(
            "===================================="
        )
        print(
            "AJVYRA REAL ANIME PUBLISH READY"
        )
        print(
            "30 / 30 REAL ANIME"
        )
        print(
            "30 MINUTES EACH"
        )
        print(
            "REAL MP4 + REAL POSTER"
        )
        print(
            "===================================="
        )

        return output


def main():

    config = (
        LocalGenerationConfig
        .from_environment()
    )

    config.validate()

    publisher = RealAnimePublishBundle(
        config
    )

    publisher.publish()


if __name__ == "__main__":
    main()
