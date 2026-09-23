"""
AJVYRA — REAL ANIME ASSEMBLY v2

360 segment واقعی
    ↓
30 anime
    ↓
هر anime = 12 segment
    ↓
هر segment = 150 ثانیه
    ↓
final main.mp4 = دقیقاً 1800 ثانیه

هیچ فایل placeholder پذیرفته نیست.
"""

from __future__ import annotations

import subprocess
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


class RealAnimeAssembler:

    def __init__(
        self,
        config: LocalGenerationConfig,
    ):
        self.config = config
        self.validator = RealVideoValidator(
            config.ffprobe_binary
        )

    def _concat_file(
        self,
        anime_number: int,
        segment_paths: list[Path],
    ) -> Path:

        concat_path = (
            self.config.production_root
            / f"anime_{anime_number:02d}"
            / "concat.txt"
        )

        concat_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        lines = []

        for path in segment_paths:
            escaped = str(
                path.resolve()
            ).replace("'", "'\\''")

            lines.append(
                f"file '{escaped}'"
            )

        concat_path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

        return concat_path

    def assemble(
        self,
        anime_number: int,
    ) -> Path:

        jobs = build_anime_jobs(
            self.config.production_root
        )

        selected = [
            job
            for job in jobs
            if job.anime_number == anime_number
        ]

        if len(selected) != 12:
            raise RuntimeError(
                f"Anime {anime_number} "
                f"does not have 12 segments."
            )

        selected.sort(
            key=lambda item: item.segment_number
        )

        segment_paths = []

        for job in selected:

            if not job.output_path.exists():
                raise RuntimeError(
                    f"Missing REAL segment: "
                    f"{job.output_path}"
                )

            probe = self.validator.require_valid(
                job.output_path
            )

            if probe.duration < 145:
                raise RuntimeError(
                    f"Segment {job.segment_number} "
                    f"is too short: "
                    f"{probe.duration:.2f}s"
                )

            segment_paths.append(
                job.output_path
            )

        concat_file = self._concat_file(
            anime_number,
            segment_paths,
        )

        output = (
            self.config.production_root
            / f"anime_{anime_number:02d}"
            / "video"
            / "main.mp4"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        temporary = output.with_name(
            "main_assembly_temp.mp4"
        )

        command = [
            self.config.ffmpeg_binary,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-map",
            "0:v:0",
            "-map",
            "0:a?",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-t",
            "1800",
            "-movflags",
            "+faststart",
            str(temporary),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg assembly failed:\n"
                + result.stderr[-5000:]
            )

        if not temporary.exists():
            raise RuntimeError(
                "FFmpeg reported success but "
                "final video was not created."
            )

        final_probe = self.validator.require_valid(
            temporary,
            minimum_duration=1799.0,
        )

        if final_probe.duration < 1799.0:
            raise RuntimeError(
                f"Final anime is shorter than 30 minutes: "
                f"{final_probe.duration:.3f}s"
            )

        temporary.replace(output)

        return output
