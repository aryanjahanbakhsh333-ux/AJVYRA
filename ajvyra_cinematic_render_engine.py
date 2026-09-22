"""
AJVYRA CINEMATIC RENDER ENGINE
------------------------------
Final media assembly layer.

Responsibilities:
- discover generated visual media
- validate media
- concatenate visual segments
- build audio mix
- mux final audio/video
- write render manifest
- resume failed renders

Requires FFmpeg installed and available on PATH.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RenderInput:
    path: str
    start: float
    duration: float
    order: int


@dataclass
class RenderReport:
    film_id: str
    status: str

    output: str = ""

    video_segments: int = 0
    audio_tracks: int = 0

    duration_seconds: float = 0.0

    errors: List[str] = field(
        default_factory=list
    )

    created_at: float = field(
        default_factory=time.time
    )


class AJVYRACinematicRenderEngine:
    VERSION = "1.0.0"

    def __init__(
        self,
        film_id: str,
        workspace: str | Path,
        ffmpeg: str = "ffmpeg",
        ffprobe: str = "ffprobe",
    ) -> None:
        self.film_id = film_id

        self.workspace = Path(
            workspace
        )

        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.ffmpeg = ffmpeg
        self.ffprobe = ffprobe

        self.report = RenderReport(
            film_id=film_id,
            status="created",
        )

    # ---------------------------------------------------------
    # Tool validation
    # ---------------------------------------------------------

    def check_tools(self) -> None:
        if shutil.which(
            self.ffmpeg
        ) is None:
            raise RuntimeError(
                "FFmpeg was not found on PATH."
            )

        if shutil.which(
            self.ffprobe
        ) is None:
            raise RuntimeError(
                "FFprobe was not found on PATH."
            )

    # ---------------------------------------------------------
    # Media inspection
    # ---------------------------------------------------------

    def probe(
        self,
        media_path: str | Path,
    ) -> Dict:
        self.check_tools()

        path = Path(media_path)

        if not path.exists():
            raise FileNotFoundError(
                path
            )

        command = [
            self.ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration,size",
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
                result.stderr.strip()
            )

        data = json.loads(
            result.stdout
        )

        format_data = data.get(
            "format",
            {},
        )

        return {
            "duration": float(
                format_data.get(
                    "duration",
                    0,
                )
            ),
            "size": int(
                format_data.get(
                    "size",
                    0,
                )
            ),
        }

    # ---------------------------------------------------------
    # Video assembly
    # ---------------------------------------------------------

    def concatenate_video(
        self,
        segments: List[
            RenderInput
        ],
        output: str | Path,
    ) -> Path:
        self.check_tools()

        if not segments:
            raise ValueError(
                "No video segments supplied."
            )

        ordered = sorted(
            segments,
            key=lambda item: item.order,
        )

        files = []

        for item in ordered:
            path = Path(item.path)

            if not path.exists():
                raise FileNotFoundError(
                    path
                )

            files.append(
                path
            )

        concat_file = (
            self.workspace
            / "video_concat.txt"
        )

        lines = []

        for path in files:
            escaped = str(
                path.resolve()
            ).replace(
                "'",
                "'\\''",
            )

            lines.append(
                f"file '{escaped}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        output = Path(output)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            self.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        self.report.video_segments = len(
            files
        )

        return output

    # ---------------------------------------------------------
    # Audio mix
    # ---------------------------------------------------------

    def mix_audio(
        self,
        audio_files: List[
            str | Path
        ],
        output: str | Path,
    ) -> Path:
        self.check_tools()

        if not audio_files:
            raise ValueError(
                "No audio files supplied."
            )

        output = Path(output)

        input_args = []

        for path in audio_files:
            path = Path(path)

            if not path.exists():
                raise FileNotFoundError(
                    path
                )

            input_args.extend(
                [
                    "-i",
                    str(path),
                ]
            )

        count = len(audio_files)

        if count == 1:
            filter_complex = (
                "[0:a]"
                "aresample=48000"
                "[mix]"
            )
        else:
            inputs = "".join(
                f"[{index}:a]"
                for index in range(count)
            )

            filter_complex = (
                f"{inputs}"
                f"amix=inputs={count}:"
                "duration=longest:"
                "dropout_transition=2,"
                "aresample=48000"
                "[mix]"
            )

        command = [
            self.ffmpeg,
            "-y",
            *input_args,
            "-filter_complex",
            filter_complex,
            "-map",
            "[mix]",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            str(output),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        self.report.audio_tracks = count

        return output

    # ---------------------------------------------------------
    # Final mux
    # ---------------------------------------------------------

    def mux(
        self,
        video: str | Path,
        audio: str | Path,
        output: str | Path,
    ) -> Path:
        self.check_tools()

        video = Path(video)
        audio = Path(audio)
        output = Path(output)

        if not video.exists():
            raise FileNotFoundError(
                video
            )

        if not audio.exists():
            raise FileNotFoundError(
                audio
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            self.ffmpeg,
            "-y",
            "-i",
            str(video),
            "-i",
            str(audio),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(output),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        self.report.output = str(
            output
        )

        self.report.status = "rendered"

        try:
            info = self.probe(
                output
            )
            self.report.duration_seconds = (
                info["duration"]
            )
        except Exception as exc:
            self.report.errors.append(
                f"Final probe failed: {exc}"
            )

        return output

    # ---------------------------------------------------------
    # Complete render
    # ---------------------------------------------------------

    def render(
        self,
        video_segments: List[
            RenderInput
        ],
        audio_files: List[
            str | Path
        ],
        output: str | Path,
    ) -> RenderReport:

        self.report.status = "rendering"

        try:
            video_path = (
                self.workspace
                / "assembled_video.mp4"
            )

            audio_path = (
                self.workspace
                / "assembled_audio.m4a"
            )

            self.concatenate_video(
                video_segments,
                video_path,
            )

            self.mix_audio(
                audio_files,
                audio_path,
            )

            self.mux(
                video_path,
                audio_path,
                output,
            )

            self.report.status = (
                "completed"
            )

        except Exception as exc:
            self.report.status = "failed"

            self.report.errors.append(
                str(exc)
            )

        self._save_report()

        return self.report

    def _save_report(self) -> None:
        path = (
            self.workspace
            / "render_report.json"
        )

        path.write_text(
            json.dumps(
                {
                    "version": self.VERSION,
                    "report": self.report.__dict__,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    engine = AJVYRACinematicRenderEngine(
        film_id="veyllora_01",
        workspace=(
            "generated/cinematic/"
            "veyllora/render"
        ),
    )

    engine.check_tools()

    print(
        "AJVYRA cinematic renderer is ready."
    )
