from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class QCResult:
    film_id: str
    passed: bool

    duration_seconds: float = 0.0
    has_video: bool = False
    has_audio: bool = False
    file_size_bytes: int = 0

    issues: List[str] = field(
        default_factory=list
    )


class AJVYRACinematicProductionQC:

    def __init__(
        self,
        minimum_duration_seconds: float = 1700.0,
        maximum_duration_seconds: float = 1900.0,
    ):
        self.minimum_duration = (
            minimum_duration_seconds
        )

        self.maximum_duration = (
            maximum_duration_seconds
        )

    def inspect(
        self,
        film_id: str,
        movie_path: str | Path,
    ) -> QCResult:

        path = Path(movie_path)

        result = QCResult(
            film_id=film_id,
            passed=False,
        )

        if not path.exists():
            result.issues.append(
                "Final movie file does not exist."
            )
            return result

        result.file_size_bytes = (
            path.stat().st_size
        )

        if result.file_size_bytes < 1024:
            result.issues.append(
                "Movie file is unexpectedly small."
            )
            return result

        ffprobe = shutil.which("ffprobe")

        if not ffprobe:
            result.issues.append(
                "ffprobe is not installed."
            )
            return result

        probe = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-show_entries",
                "stream=codec_type",
                "-of",
                "json",
                str(path),
            ],
            capture_output=True,
            text=True,
        )

        if probe.returncode != 0:
            result.issues.append(
                "ffprobe could not inspect the movie."
            )
            return result

        try:
            data = json.loads(
                probe.stdout
            )

            result.duration_seconds = float(
                data.get(
                    "format",
                    {},
                ).get(
                    "duration",
                    0,
                )
            )

            stream_types = {
                stream.get("codec_type")
                for stream in data.get(
                    "streams",
                    [],
                )
            }

            result.has_video = (
                "video" in stream_types
            )

            result.has_audio = (
                "audio" in stream_types
            )

        except Exception as exc:
            result.issues.append(
                f"Invalid ffprobe response: {exc}"
            )
            return result

        if not result.has_video:
            result.issues.append(
                "No video stream found."
            )

        if not result.has_audio:
            result.issues.append(
                "No audio stream found."
            )

        if (
            result.duration_seconds
            < self.minimum_duration
        ):
            result.issues.append(
                "Movie is shorter than the production gate."
            )

        if (
            result.duration_seconds
            > self.maximum_duration
        ):
            result.issues.append(
                "Movie exceeds the production duration gate."
            )

        result.passed = not result.issues

        return result

    def save_report(
        self,
        result: QCResult,
        output_path: str | Path,
    ) -> Path:

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                asdict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
