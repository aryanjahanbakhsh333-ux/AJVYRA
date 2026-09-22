from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


class AJVYRAAnimeVoiceToFinalMovie:

    def __init__(
        self,
        root: str | Path = "ajvyra_anime_voice_output",
    ):
        self.root = Path(root)

        if shutil.which("ffmpeg") is None:
            raise RuntimeError(
                "FFmpeg is required for anime audio assembly."
            )

    def collect_voice_files(
        self,
        film_id: str,
    ) -> list[Path]:

        film_root = (
            self.root / film_id
        )

        if not film_root.exists():
            return []

        files = sorted(
            film_root.glob(
                "**/*.wav"
            )
        )

        return [
            path
            for path in files
            if path.stat().st_size > 1024
        ]

    def build_audio(
        self,
        film_id: str,
        output: str | Path,
    ) -> Path:

        files = self.collect_voice_files(
            film_id
        )

        if not files:
            raise RuntimeError(
                f"No digital voice files exist for {film_id}."
            )

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            "ffmpeg",
            "-y",
        ]

        for path in files:
            command.extend(
                [
                    "-i",
                    str(path),
                ]
            )

        inputs = "".join(
            f"[{index}:a]"
            for index in range(
                len(files)
            )
        )

        filter_complex = (
            f"{inputs}"
            f"amix="
            f"inputs={len(files)}:"
            f"duration=longest:"
            f"dropout_transition=2"
            f"[voice]"
        )

        command.extend(
            [
                "-filter_complex",
                filter_complex,
                "-map",
                "[voice]",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "48000",
                str(output),
            ]
        )

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        if (
            not output.exists()
            or output.stat().st_size < 1024
        ):
            raise RuntimeError(
                "Digital voice mix was not created."
            )

        return output

    def attach_to_movie(
        self,
        movie: str | Path,
        voice_audio: str | Path,
        output: str | Path,
    ) -> Path:

        movie = Path(movie)
        voice_audio = Path(voice_audio)
        output = Path(output)

        if not movie.exists():
            raise FileNotFoundError(movie)

        if not voice_audio.exists():
            raise FileNotFoundError(
                voice_audio
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(movie),
                "-i",
                str(voice_audio),
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
                str(output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        return output
