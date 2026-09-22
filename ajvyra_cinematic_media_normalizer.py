from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class NormalizedMedia:
    source: str
    output: str
    duration: float
    status: str


class AJVYRACinematicMediaNormalizer:

    def __init__(
        self,
        workspace: str | Path,
        *,
        ffmpeg: str = "ffmpeg",
        ffprobe: str = "ffprobe",
    ) -> None:

        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.ffmpeg = ffmpeg
        self.ffprobe = ffprobe

    def normalize_video(
        self,
        source: str | Path,
        output: str | Path,
        *,
        width: int = 1280,
        height: int = 720,
        fps: int = 24,
        audio_sample_rate: int = 48000,
    ) -> NormalizedMedia:

        source = Path(source)
        output = Path(output)

        if not source.exists():
            raise FileNotFoundError(
                f"Source video does not exist: {source}"
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            self.ffmpeg,
            "-y",
            "-i",
            str(source),

            "-vf",
            (
                f"scale={width}:{height}:"
                "force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
            ),

            "-r",
            str(fps),

            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",

            "-c:a",
            "aac",
            "-ar",
            str(audio_sample_rate),
            "-ac",
            "2",

            "-movflags",
            "+faststart",

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
                "FFmpeg normalization failed:\n"
                + completed.stderr.strip()
            )

        if not output.exists():
            raise RuntimeError(
                f"Normalization produced no file: {output}"
            )

        if output.stat().st_size <= 0:
            raise RuntimeError(
                f"Normalized file is empty: {output}"
            )

        duration = self.probe_duration(
            output
        )

        return NormalizedMedia(
            source=str(source),
            output=str(output),
            duration=duration,
            status="NORMALIZED",
        )

    def probe_duration(
        self,
        path: str | Path,
    ) -> float:

        command = [
            self.ffprobe,
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
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip()
            )

        try:
            value = float(
                result.stdout.strip()
            )
        except ValueError as exc:
            raise RuntimeError(
                f"Invalid duration: {path}"
            ) from exc

        if value <= 0:
            raise RuntimeError(
                f"Invalid media duration: {path}"
            )

        return value

    def verify_ffmpeg(self) -> bool:
        return shutil.which(
            self.ffmpeg
        ) is not None

    def verify_ffprobe(self) -> bool:
        return shutil.which(
            self.ffprobe
        ) is not None
