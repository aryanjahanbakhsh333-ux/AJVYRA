"""
AJVYRA — REAL FFPROBE VIDEO VALIDATOR v1

این فایل فقط فایل‌هایی را قبول می‌کند که FFprobe بتواند
به عنوان ویدیوی واقعی بخواند.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoProbe:
    path: Path
    duration: float
    width: int
    height: int
    fps: float
    codec: str
    size_bytes: int


class RealVideoValidator:

    def __init__(
        self,
        ffprobe_binary: str = "ffprobe",
    ):
        self.ffprobe_binary = ffprobe_binary

    def probe(self, path: Path) -> VideoProbe:

        if not path.exists():
            raise RuntimeError(
                f"Video does not exist: {path}"
            )

        if path.stat().st_size < 100_000:
            raise RuntimeError(
                f"Video is too small: {path}"
            )

        command = [
            self.ffprobe_binary,
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,codec_name,r_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
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
                f"FFprobe failed for {path}:\n"
                f"{result.stderr}"
            )

        try:
            data = json.loads(
                result.stdout
            )

            stream = data["streams"][0]
            duration = float(
                data["format"]["duration"]
            )

            width = int(
                stream["width"]
            )

            height = int(
                stream["height"]
            )

            codec = str(
                stream["codec_name"]
            )

            rate = stream["r_frame_rate"]

            numerator, denominator = (
                rate.split("/")
            )

            fps = (
                float(numerator)
                / float(denominator)
            )

        except Exception as exc:
            raise RuntimeError(
                f"Invalid video metadata: {path}"
            ) from exc

        return VideoProbe(
            path=path,
            duration=duration,
            width=width,
            height=height,
            fps=fps,
            codec=codec,
            size_bytes=path.stat().st_size,
        )

    def require_valid(
        self,
        path: Path,
        minimum_duration: float = 1.0,
    ) -> VideoProbe:

        probe = self.probe(path)

        if probe.duration < minimum_duration:
            raise RuntimeError(
                f"Video duration is invalid: "
                f"{probe.duration:.2f}s"
            )

        if probe.width < 320:
            raise RuntimeError(
                "Video width is too small."
            )

        if probe.height < 240:
            raise RuntimeError(
                "Video height is too small."
            )

        if not probe.codec:
            raise RuntimeError(
                "Video codec is missing."
            )

        return probe
