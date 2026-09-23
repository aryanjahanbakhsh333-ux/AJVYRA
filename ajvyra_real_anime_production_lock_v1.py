"""
AJVYRA — REAL ANIME PRODUCTION LOCK v1

این فایل اجازه نمی‌دهد پروژه ادعا کند که ۳۰ انیمه آماده‌اند
مگر اینکه واقعاً ۳۶۰ Segment خروجی معتبر وجود داشته باشد.

30 × 12 = 360
360 Segment × 150 seconds = 54,000 seconds
54,000 / 60 = 900 minutes
900 / 30 anime = 30 minutes per anime
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_local_real_generation_config_v1 import (
    LocalGenerationConfig,
)
from ajvyra_real_anime_job_builder_v1 import (
    build_anime_jobs,
)
from ajvyra_real_ffprobe_validator_v1 import (
    RealVideoValidator,
)


class RealAnimeProductionLock:

    def __init__(
        self,
        config: LocalGenerationConfig,
    ):
        self.config = config

        self.validator = RealVideoValidator(
            config.ffprobe_binary
        )

    def inspect(self) -> dict:

        jobs = build_anime_jobs(
            self.config.production_root
        )

        anime_results = {}

        for anime_number in range(1, 31):

            anime_jobs = [
                job
                for job in jobs
                if job.anime_number == anime_number
            ]

            valid_segments = 0
            missing_segments = []

            durations = []

            for job in anime_jobs:

                try:

                    probe = self.validator.require_valid(
                        job.output_path
                    )

                    valid_segments += 1
                    durations.append(
                        probe.duration
                    )

                except Exception:

                    missing_segments.append(
                        job.segment_number
                    )

            anime_results[
                str(anime_number)
            ] = {
                "valid_segments": valid_segments,
                "required_segments": 12,
                "missing_segments": missing_segments,
                "segment_durations": durations,
                "ready_for_assembly": (
                    valid_segments == 12
                ),
            }

        ready_anime = sum(
            1
            for item in anime_results.values()
            if item["ready_for_assembly"]
        )

        return {
            "project": "AJVYRA",
            "real_segment_jobs": 360,
            "required_anime": 30,
            "anime_ready_for_assembly": ready_anime,
            "release_ready": False,
            "anime": anime_results,
        }

    def require_all_segments(self) -> dict:

        report = self.inspect()

        if report["anime_ready_for_assembly"] != 30:

            failed = [
                number
                for number, data
                in report["anime"].items()
                if not data["ready_for_assembly"]
            ]

            raise RuntimeError(
                "REAL ANIME PRODUCTION LOCK FAILED.\n"
                f"Ready: "
                f"{report['anime_ready_for_assembly']}/30\n"
                f"Failed anime: {failed}"
            )

        return report

    def save_report(
        self,
        path: Path,
    ) -> Path:

        report = self.inspect()

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path


def main() -> int:

    config = LocalGenerationConfig.from_environment()
    config.validate()

    lock = RealAnimeProductionLock(
        config
    )

    report = lock.inspect()

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
    )

    return (
        0
        if report["anime_ready_for_assembly"] == 30
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
