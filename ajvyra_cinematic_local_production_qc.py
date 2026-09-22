from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LocalFilmQCResult:
    film_id: str
    passed: bool
    file_exists: bool
    file_size_bytes: int
    duration_seconds: float
    has_video: bool
    has_audio: bool
    checks: dict[str, bool]
    errors: list[str]


class AJVYRACinematicLocalProductionQC:

    def __init__(
        self,
        minimum_duration_seconds: float = 1.0,
        maximum_duration_seconds: float = 7200.0,
    ) -> None:

        self.minimum_duration_seconds = (
            minimum_duration_seconds
        )

        self.maximum_duration_seconds = (
            maximum_duration_seconds
        )

    def check(
        self,
        film_id: str,
        movie_path: str | Path,
    ) -> LocalFilmQCResult:

        path = Path(movie_path)

        errors: list[str] = []

        file_exists = (
            path.exists()
            and path.is_file()
        )

        file_size = (
            path.stat().st_size
            if file_exists
            else 0
        )

        duration = 0.0
        has_video = False
        has_audio = False

        checks = {
            "file_exists": file_exists,
            "file_not_empty": False,
            "ffprobe_available": False,
            "video_stream": False,
            "audio_stream": False,
            "duration_valid": False,
        }

        if not file_exists:

            errors.append(
                "Movie file does not exist."
            )

            return self._result(
                film_id,
                file_exists,
                file_size,
                duration,
                has_video,
                has_audio,
                checks,
                errors,
            )

        if file_size <= 1024:

            errors.append(
                "Movie file is too small."
            )

        else:

            checks["file_not_empty"] = True

        ffprobe = shutil.which("ffprobe")

        if ffprobe is None:

            errors.append(
                "ffprobe is not available."
            )

            return self._result(
                film_id,
                file_exists,
                file_size,
                duration,
                has_video,
                has_audio,
                checks,
                errors,
            )

        checks["ffprobe_available"] = True

        probe = self._probe(
            ffprobe,
            path,
        )

        if probe is None:

            errors.append(
                "ffprobe could not read the movie."
            )

            return self._result(
                film_id,
                file_exists,
                file_size,
                duration,
                has_video,
                has_audio,
                checks,
                errors,
            )

        streams = probe.get(
            "streams",
            [],
        )

        for stream in streams:

            codec_type = stream.get(
                "codec_type"
            )

            if codec_type == "video":
                has_video = True

            elif codec_type == "audio":
                has_audio = True

        checks["video_stream"] = has_video
        checks["audio_stream"] = has_audio

        if not has_video:
            errors.append(
                "No video stream found."
            )

        if not has_audio:
            errors.append(
                "No audio stream found."
            )

        try:

            duration = float(
                probe.get(
                    "format",
                    {},
                ).get(
                    "duration",
                    0,
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            duration = 0.0

        if (
            self.minimum_duration_seconds
            <= duration
            <= self.maximum_duration_seconds
        ):

            checks["duration_valid"] = True

        else:

            errors.append(
                "Movie duration is outside "
                f"the allowed range "
                f"{self.minimum_duration_seconds}–"
                f"{self.maximum_duration_seconds} seconds."
            )

        return self._result(
            film_id,
            file_exists,
            file_size,
            duration,
            has_video,
            has_audio,
            checks,
            errors,
        )

    def save_report(
        self,
        result: LocalFilmQCResult,
        path: str | Path,
    ) -> None:

        output = Path(path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                {
                    "film_id": result.film_id,
                    "passed": result.passed,
                    "file_exists": result.file_exists,
                    "file_size_bytes": result.file_size_bytes,
                    "duration_seconds": (
                        result.duration_seconds
                    ),
                    "has_video": result.has_video,
                    "has_audio": result.has_audio,
                    "checks": result.checks,
                    "errors": result.errors,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _probe(
        ffprobe: str,
        path: Path,
    ) -> dict | None:

        command = [
            ffprobe,
            "-v",
            "error",
            "-show_streams",
            "-show_format",
            "-of",
            "json",
            str(path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return None

        try:
            return json.loads(
                result.stdout
            )
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _result(
        film_id: str,
        file_exists: bool,
        file_size: int,
        duration: float,
        has_video: bool,
        has_audio: bool,
        checks: dict[str, bool],
        errors: list[str],
    ) -> LocalFilmQCResult:

        passed = (
            not errors
            and all(checks.values())
        )

        return LocalFilmQCResult(
            film_id=film_id,
            passed=passed,
            file_exists=file_exists,
            file_size_bytes=file_size,
            duration_seconds=duration,
            has_video=has_video,
            has_audio=has_audio,
            checks=checks,
            errors=errors,
        )
