from __future__ import annotations

import json
import subprocess
from pathlib import Path


class AJVYRAWan30FilmReleaseQCV2:

    def __init__(
        self,
        ffprobe_executable: str = "ffprobe",
    ):
        self.ffprobe = ffprobe_executable

    def inspect(
        self,
        video_path: Path,
    ) -> dict:

        if not video_path.exists():
            return {
                "passed": False,
                "reason": "missing_file",
            }

        if video_path.stat().st_size <= 0:
            return {
                "passed": False,
                "reason": "empty_file",
            }

        command = [
            self.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
            "-show_entries",
            "stream=codec_type,codec_name,width,height",
            "-of",
            "json",
            str(video_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return {
                "passed": False,
                "reason": "ffprobe_failed",
                "stderr": result.stderr,
            }

        try:
            data = json.loads(
                result.stdout
            )
        except json.JSONDecodeError:
            return {
                "passed": False,
                "reason": "invalid_probe_json",
            }

        streams = data.get(
            "streams",
            [],
        )

        video_streams = [
            stream
            for stream in streams
            if stream.get("codec_type") == "video"
        ]

        if not video_streams:
            return {
                "passed": False,
                "reason": "no_video_stream",
            }

        format_data = data.get(
            "format",
            {},
        )

        duration = float(
            format_data.get(
                "duration",
                0,
            ) or 0
        )

        if duration <= 0:
            return {
                "passed": False,
                "reason": "zero_duration",
            }

        return {
            "passed": True,
            "duration": duration,
            "size": int(
                format_data.get(
                    "size",
                    video_path.stat().st_size,
                )
            ),
            "streams": streams,
        }

    def require_pass(
        self,
        video_path: Path,
    ) -> dict:

        result = self.inspect(
            video_path
        )

        if not result["passed"]:
            raise RuntimeError(
                f"Release QC failed for "
                f"{video_path}: {result}"
            )

        return result
