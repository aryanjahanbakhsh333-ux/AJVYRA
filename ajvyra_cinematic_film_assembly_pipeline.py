from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class FilmSegment:
    segment_id: str
    file_path: str
    order: int
    expected_duration: Optional[float] = None
    actual_duration: Optional[float] = None


@dataclass
class FilmAssemblyResult:
    film_id: str
    output_path: str
    segment_count: int
    duration_seconds: float
    status: str


class AJVYRACinematicFilmAssemblyPipeline:
    """
    Converts real generated media segments into one film master.

    Every segment must physically exist.
    """

    def __init__(
        self,
        workspace: str | Path,
        *,
        ffmpeg_binary: str = "ffmpeg",
        ffprobe_binary: str = "ffprobe",
    ) -> None:
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.ffmpeg = ffmpeg_binary
        self.ffprobe = ffprobe_binary

    def probe_duration(self, file_path: str | Path) -> float:
        command = [
            self.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(file_path),
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                f"ffprobe failed for '{file_path}': "
                f"{completed.stderr.strip()}"
            )

        try:
            duration = float(completed.stdout.strip())
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid duration returned by ffprobe for '{file_path}'."
            ) from exc

        if duration <= 0:
            raise RuntimeError(
                f"Non-positive media duration for '{file_path}'."
            )

        return duration

    def collect_segments(
        self,
        segments: list[FilmSegment],
    ) -> list[FilmSegment]:

        ordered = sorted(
            segments,
            key=lambda item: item.order,
        )

        for segment in ordered:
            path = Path(segment.file_path)

            if not path.exists():
                raise FileNotFoundError(
                    f"Film segment does not exist: {path}"
                )

            if path.stat().st_size <= 0:
                raise RuntimeError(
                    f"Film segment is empty: {path}"
                )

            segment.actual_duration = self.probe_duration(path)

        return ordered

    def assemble(
        self,
        film_id: str,
        segments: list[FilmSegment],
        output_path: str | Path,
    ) -> FilmAssemblyResult:

        if not segments:
            raise ValueError("Cannot assemble a film without segments.")

        ordered = self.collect_segments(segments)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        concat_file = self.workspace / f"{film_id}_concat.txt"

        with concat_file.open("w", encoding="utf-8") as handle:
            for segment in ordered:
                absolute = Path(segment.file_path).resolve()

                escaped = (
                    str(absolute)
                    .replace("\\", "/")
                    .replace("'", "'\\''")
                )

                handle.write(f"file '{escaped}'\n")

        command = [
            self.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                "FFmpeg film assembly failed:\n"
                + completed.stderr.strip()
            )

        if not output.exists() or output.stat().st_size <= 0:
            raise RuntimeError(
                f"FFmpeg reported success but output is invalid: {output}"
            )

        duration = self.probe_duration(output)

        result = FilmAssemblyResult(
            film_id=film_id,
            output_path=str(output),
            segment_count=len(ordered),
            duration_seconds=duration,
            status="ASSEMBLED",
        )

        report_path = self.workspace / f"{film_id}_assembly.json"

        with report_path.open("w", encoding="utf-8") as handle:
            json.dump(
                asdict(result),
                handle,
                ensure_ascii=False,
                indent=2,
            )

        return result
