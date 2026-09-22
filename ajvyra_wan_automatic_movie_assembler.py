from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class AJVYRAWanAutomaticMovieAssembler:

    def __init__(
        self,
        production_root: str | Path = (
            "production/wan_films"
        ),
    ) -> None:

        self.production_root = Path(
            production_root
        )

    def assemble(
        self,
        film_id: str,
    ) -> Path:

        film_root = (
            self.production_root
            / film_id
        )

        segments_root = (
            film_root
            / "segments"
        )

        final_movie = (
            film_root
            / "movie.mp4"
        )

        if not segments_root.exists():
            raise RuntimeError(
                "Segments directory does not exist."
            )

        segments = sorted(
            segments_root.glob(
                "segment_*.mp4"
            )
        )

        if not segments:
            raise RuntimeError(
                "No generated video segments found."
            )

        for segment in segments:

            if segment.stat().st_size <= 1024:

                raise RuntimeError(
                    f"Invalid segment: {segment}"
                )

        ffmpeg = shutil.which(
            "ffmpeg"
        )

        if not ffmpeg:

            raise RuntimeError(
                "FFmpeg is not installed."
            )

        concat_file = (
            film_root
            / "concat.txt"
        )

        lines = []

        for segment in segments:

            path = (
                str(
                    segment.resolve()
                )
                .replace(
                    "'",
                    "'\\''",
                )
            )

            lines.append(
                f"file '{path}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        print(
            f"[ASSEMBLE] "
            f"{film_id}: "
            f"{len(segments)} segments"
        )

        command = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(final_movie),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                "FFmpeg failed:\n"
                + result.stderr[-5000:]
            )

        if not final_movie.exists():

            raise RuntimeError(
                "Final movie was not created."
            )

        if final_movie.stat().st_size <= 1024:

            raise RuntimeError(
                "Final movie is invalid."
            )

        duration = (
            self._duration(
                final_movie
            )
        )

        report = {
            "film_id": film_id,
            "segments": len(segments),
            "duration_seconds": duration,
            "movie": str(final_movie),
            "real_media": True,
        }

        (
            film_root
            / "assembly_report.json"
        ).write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return final_movie

    @staticmethod
    def _duration(
        path: Path,
    ) -> float:

        ffprobe = shutil.which(
            "ffprobe"
        )

        if not ffprobe:
            raise RuntimeError(
                "ffprobe is not installed."
            )

        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                result.stderr
            )

        return float(
            result.stdout.strip()
        )
