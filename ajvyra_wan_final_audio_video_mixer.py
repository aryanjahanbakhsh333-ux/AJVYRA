from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class AJVYRAFinalAudioVideoMixer:

    def __init__(self):
        self._require("ffmpeg")
        self._require("ffprobe")

    @staticmethod
    def _require(name: str) -> None:

        if shutil.which(name) is None:
            raise RuntimeError(
                f"{name} is required but was not found in PATH."
            )

    @staticmethod
    def _run(
        args: list[str],
    ) -> subprocess.CompletedProcess:

        return subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def mux(
        self,
        video: str | Path,
        audio_tracks: list[str | Path],
        output: str | Path,
    ) -> Path:

        video = Path(video)
        output = Path(output)

        if not video.exists():
            raise FileNotFoundError(video)

        if not audio_tracks:
            raise RuntimeError(
                "No real audio tracks supplied."
            )

        for audio in audio_tracks:

            if not Path(audio).exists():
                raise FileNotFoundError(audio)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
        ]

        for audio in audio_tracks:
            command += [
                "-i",
                str(audio),
            ]

        filters = []

        for index in range(
            1,
            len(audio_tracks) + 1,
        ):
            filters.append(
                f"[{index}:a]"
                f"aresample=48000,"
                f"aformat=sample_fmts=fltp:"
                f"sample_rates=48000:"
                f"channel_layouts=stereo"
                f"[a{index}]"
            )

        if len(audio_tracks) == 1:

            audio_map = "[a1]"

        else:

            inputs = "".join(
                f"[a{i}]"
                for i in range(
                    1,
                    len(audio_tracks) + 1,
                )
            )

            filters.append(
                f"{inputs}"
                f"amix=inputs={len(audio_tracks)}:"
                f"duration=longest:"
                f"dropout_transition=2"
                f"[mixed]"
            )

            audio_map = "[mixed]"

        result = self._run(
            command
            + [
                "-filter_complex",
                ";".join(filters),
                "-map",
                "0:v:0",
                "-map",
                audio_map,
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "256k",
                "-ar",
                "48000",
                "-ac",
                "2",
                "-shortest",
                str(output),
            ]
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        return output

    def add_subtitle_track(
        self,
        video: str | Path,
        subtitle: str | Path,
        output: str | Path,
        language: str,
    ) -> Path:

        video = Path(video)
        subtitle = Path(subtitle)
        output = Path(output)

        if not video.exists():
            raise FileNotFoundError(video)

        if not subtitle.exists():
            raise FileNotFoundError(subtitle)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        result = self._run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video),
                "-i",
                str(subtitle),
                "-map",
                "0:v:0",
                "-map",
                "0:a?",
                "-map",
                "1:0",
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                "-c:s",
                "webvtt",
                "-metadata:s:s:0",
                f"language={language}",
                str(output),
            ]
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        return output
