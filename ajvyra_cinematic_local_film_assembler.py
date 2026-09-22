from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class FilmAssemblyResult:
    film_id: str
    output_path: str | None
    success: bool
    segment_count: int
    duration_seconds: float
    sha256: str | None
    error: str | None


class AJVYRACinematicLocalFilmAssembler:

    def __init__(
        self,
        output_root: str | Path = "production/cinematic_local",
    ) -> None:

        self.output_root = Path(output_root)

    def assemble(
        self,
        film_id: str,
        segment_paths: Iterable[str | Path],
        *,
        output_name: str = "movie.mp4",
    ) -> FilmAssemblyResult:

        paths = [
            Path(path)
            for path in segment_paths
        ]

        try:

            if not paths:
                raise ValueError(
                    "No segments were supplied."
                )

            for path in paths:

                if not path.exists():
                    raise FileNotFoundError(
                        f"Missing segment: {path}"
                    )

                if path.stat().st_size <= 1024:
                    raise RuntimeError(
                        f"Invalid segment: {path}"
                    )

            ffmpeg = shutil.which("ffmpeg")
            ffprobe = shutil.which("ffprobe")

            if not ffmpeg:
                raise RuntimeError(
                    "ffmpeg was not found in PATH."
                )

            if not ffprobe:
                raise RuntimeError(
                    "ffprobe was not found in PATH."
                )

            film_dir = (
                self.output_root
                / film_id
            )

            film_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            concat_file = (
                film_dir
                / "segments_concat.txt"
            )

            output_path = (
                film_dir
                / output_name
            )

            lines = []

            for path in paths:

                escaped = (
                    str(path.resolve())
                    .replace("'", "'\\''")
                )

                lines.append(
                    f"file '{escaped}'"
                )

            concat_file.write_text(
                "\n".join(lines),
                encoding="utf-8",
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
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(output_path),
            ]

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            if process.returncode != 0:

                raise RuntimeError(
                    "FFmpeg assembly failed:\n"
                    + process.stderr[-4000:]
                )

            if not output_path.exists():
                raise RuntimeError(
                    "FFmpeg completed but the "
                    "final movie does not exist."
                )

            duration = self._probe_duration(
                output_path
            )

            checksum = self._sha256(
                output_path
            )

            report = {
                "film_id": film_id,
                "output_path": str(output_path),
                "segment_count": len(paths),
                "duration_seconds": duration,
                "sha256": checksum,
                "success": True,
            }

            report_path = (
                film_dir
                / "assembly_report.json"
            )

            report_path.write_text(
                json.dumps(
                    report,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            return FilmAssemblyResult(
                film_id=film_id,
                output_path=str(output_path),
                success=True,
                segment_count=len(paths),
                duration_seconds=duration,
                sha256=checksum,
                error=None,
            )

        except Exception as exc:

            return FilmAssemblyResult(
                film_id=film_id,
                output_path=None,
                success=False,
                segment_count=len(paths),
                duration_seconds=0.0,
                sha256=None,
                error=str(exc),
            )

    @staticmethod
    def _probe_duration(
        path: Path,
    ) -> float:

        ffprobe = shutil.which("ffprobe")

        if not ffprobe:
            raise RuntimeError(
                "ffprobe was not found."
            )

        command = [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
            )

        value = float(
            result.stdout.strip()
        )

        if value <= 0:
            raise RuntimeError(
                "Invalid video duration."
            )

        return value

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as handle:

            while True:

                chunk = handle.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()
