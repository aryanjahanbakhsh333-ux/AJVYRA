from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class AJVYRAWanRealOutputControllerV2:
    """
    Controls real Wan output paths.

    The controller never treats a missing or empty MP4 as success.
    """

    def __init__(
        self,
        ffmpeg_executable: str = "ffmpeg",
    ):
        self.ffmpeg_executable = ffmpeg_executable

    def ensure_parent(self, path: Path) -> None:
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def validate_video(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(
                f"Video does not exist: {path}"
            )

        if path.stat().st_size <= 0:
            raise RuntimeError(
                f"Video is empty: {path}"
            )

        if path.suffix.lower() != ".mp4":
            raise RuntimeError(
                f"Expected MP4 output: {path}"
            )

    def copy_wan_output(
        self,
        source: Path,
        destination: Path,
    ) -> Path:

        self.validate_video(source)
        self.ensure_parent(destination)

        shutil.copy2(
            source,
            destination,
        )

        self.validate_video(destination)

        return destination

    def probe_video(
        self,
        path: Path,
    ) -> dict:

        self.validate_video(path)

        command = [
            self.ffmpeg_executable,
            "-v",
            "error",
            "-i",
            str(path),
            "-f",
            "null",
            "-",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "path": str(path),
            "valid": result.returncode == 0,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
