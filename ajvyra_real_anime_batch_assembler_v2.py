"""
AJVYRA — REAL 30 ANIME BATCH ASSEMBLER v2

تمام 30 anime را از segmentهای واقعی می‌سازد.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_local_real_generation_config_v1 import (
    LocalGenerationConfig,
)
from ajvyra_real_anime_assembly_v2 import (
    RealAnimeAssembler,
)
from ajvyra_real_anime_duration_lock_v2 import (
    AnimeDurationLock,
)


class RealThirtyAnimeAssembler:

    def __init__(
        self,
        config: LocalGenerationConfig,
    ):
        self.config = config

        self.assembler = RealAnimeAssembler(
            config
        )

        self.duration_lock = AnimeDurationLock(
            config.ffprobe_binary
        )

    def run(self) -> dict:

        results = []

        for anime_number in range(1, 31):

            print(
                f"[{anime_number}/30] "
                f"ASSEMBLING REAL ANIME"
            )

            output = self.assembler.assemble(
                anime_number
            )

            duration = (
                self.duration_lock.require_30_minutes(
                    output
                )
            )

            results.append(
                {
                    "anime_number": anime_number,
                    "video": str(output),
                    "duration_seconds": duration[
                        "duration_seconds"
                    ],
                    "ready": True,
                }
            )

        report = {
            "project": "AJVYRA",
            "anime_count": 30,
            "completed": len(results),
            "all_ready": len(results) == 30,
            "anime": results,
        }

        report_path = (
            self.config.production_root
            / "state"
            / "30_anime_assembly_report.json"
        )

        report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return report


def main():

    config = (
        LocalGenerationConfig
        .from_environment()
    )

    config.validate()

    builder = RealThirtyAnimeAssembler(
        config
    )

    report = builder.run()

    if not report["all_ready"]:
        raise SystemExit(2)

    print(
        "REAL 30 ANIME ASSEMBLY COMPLETE"
    )


if __name__ == "__main__":
    main()
