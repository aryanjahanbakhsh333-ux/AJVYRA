"""
AJVYRA AI VIDEO GENERATION ENGINE

Turns generated scene frames + audio into actual video.

Architecture:

AI story
   ↓
scene plan
   ↓
images / animation frames
   ↓
voice + music
   ↓
FFmpeg
   ↓
MP4

FFmpeg is used as the media compositor because it supports multiple
inputs, encoding, filtering and muxing of audio/video/subtitle streams.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class VideoRequest:

    project_id: str

    output_name: str = "episode.mp4"

    width: int = 1280
    height: int = 720

    fps: int = 24

    duration_seconds: int = 1800

    frames_dir: Optional[str] = None

    audio_files: Optional[List[str]] = None

    subtitle_files: Optional[List[str]] = None


class AJVYRAAIVideoGenerationEngine:

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self.root = Path(root).resolve()

        self.output_root = (
            self.root
            / "generated"
            / "videos"
        )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =========================================================
    # MAIN
    # =========================================================

    def render(
        self,
        request: VideoRequest,
    ) -> Dict[str, Any]:

        self._require_ffmpeg()

        project_dir = (
            self.output_root
            / request.project_id
        )

        project_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            project_dir
            / request.output_name
        )

        frames = self._collect_frames(
            request
        )

        audio = self._collect_audio(
            request
        )

        if not frames:
            raise RuntimeError(
                "No generated video frames were found."
            )

        command = self._build_ffmpeg_command(
            request,
            frames,
            audio,
            output_path,
        )

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        log_path = (
            project_dir
            / "ffmpeg.log"
        )

        log_path.write_text(
            process.stdout
            + "\n"
            + process.stderr,
            encoding="utf-8",
        )

        if process.returncode != 0:
            raise RuntimeError(
                "FFmpeg video render failed. "
                f"See {log_path}"
            )

        if not output_path.exists():
            raise RuntimeError(
                "FFmpeg finished without creating "
                "the expected video."
            )

        metadata = {
            "request": asdict(request),
            "output": str(output_path),
            "frames": len(frames),
            "audio_tracks": len(audio),
            "backend": "ffmpeg",
        }

        metadata_path = (
            output_path.with_suffix(
                ".json"
            )
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "status": "rendered",
            "video": str(output_path),
            "metadata": str(metadata_path),
        }

    # =========================================================
    # SCENE VIDEO
    # =========================================================

    def render_scene_sequence(
        self,
        project_id: str,
        frames_dir: Path | str,
        audio_files: List[str] | None = None,
        duration_seconds: int = 30,
    ) -> Dict[str, Any]:

        request = VideoRequest(
            project_id=project_id,
            output_name="scene.mp4",
            duration_seconds=duration_seconds,
            frames_dir=str(frames_dir),
            audio_files=audio_files or [],
        )

        return self.render(
            request
        )

    # =========================================================
    # FFmpeg
    # =========================================================

    def _build_ffmpeg_command(
        self,
        request: VideoRequest,
        frames: List[Path],
        audio: List[Path],
        output_path: Path,
    ) -> List[str]:

        frame_pattern = (
            str(
                frames[0].parent
                / "frame_%06d.png"
            )
        )

        command = [
            "ffmpeg",
            "-y",
            "-framerate",
            str(request.fps),
            "-i",
            frame_pattern,
        ]

        # -----------------------------------------------------
        # AUDIO
        # -----------------------------------------------------

        for audio_file in audio:
            command.extend(
                [
                    "-i",
                    str(audio_file),
                ]
            )

        # -----------------------------------------------------
        # VIDEO
        # -----------------------------------------------------

        command.extend(
            [
                "-vf",
                (
                    f"scale={request.width}:"
                    f"{request.height}:"
                    "force_original_aspect_ratio=decrease,"
                    f"pad={request.width}:"
                    f"{request.height}:(ow-iw)/2:"
                    "(oh-ih)/2"
                ),
                "-r",
                str(request.fps),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
            ]
        )

        # -----------------------------------------------------
        # AUDIO MIX
        # -----------------------------------------------------

        if audio:

            if len(audio) == 1:

                command.extend(
                    [
                        "-map",
                        "0:v:0",
                        "-map",
                        "1:a:0",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                    ]
                )

            else:

                inputs = "".join(
                    f"[{i}:a:0]"
                    for i in range(
                        1,
                        len(audio) + 1,
                    )
                )

                command.extend(
                    [
                        "-filter_complex",
                        (
                            inputs
                            + f"amix=inputs={len(audio)}:"
                            "duration=longest[aout]"
                        ),
                        "-map",
                        "0:v:0",
                        "-map",
                        "[aout]",
                        "-c:a",
                        "aac",
                        "-b:a",
                        "192k",
                    ]
                )

        else:

            command.extend(
                [
                    "-an",
                ]
            )

        command.extend(
            [
                "-movflags",
                "+faststart",
                str(output_path),
            ]
        )

        return command

    # =========================================================
    # DISCOVERY
    # =========================================================

    def _collect_frames(
        self,
        request: VideoRequest,
    ) -> List[Path]:

        if not request.frames_dir:
            return []

        directory = Path(
            request.frames_dir
        )

        if not directory.exists():
            return []

        frames = sorted(
            [
                p
                for p in directory.iterdir()
                if p.is_file()
                and p.suffix.lower()
                in {
                    ".png",
                    ".jpg",
                    ".jpeg",
                }
            ]
        )

        return frames

    def _collect_audio(
        self,
        request: VideoRequest,
    ) -> List[Path]:

        if not request.audio_files:
            return []

        return [
            Path(path)
            for path in request.audio_files
            if Path(path).exists()
        ]

    # =========================================================
    # REQUIREMENTS
    # =========================================================

    @staticmethod
    def _require_ffmpeg() -> None:

        if (
            shutil.which("ffmpeg")
            is None
        ):
            raise RuntimeError(
                "FFmpeg was not found in PATH."
            )
