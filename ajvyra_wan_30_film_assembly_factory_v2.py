from __future__ import annotations

import subprocess
from pathlib import Path


class AJVYRAWan30FilmAssemblyFactoryV2:
    """
    Joins generated Wan shots into one film master.

    Requires FFmpeg on the production machine.
    """

    def __init__(
        self,
        ffmpeg_executable: str = "ffmpeg",
    ):
        self.ffmpeg = ffmpeg_executable

    def validate_shots(
        self,
        shots: list[Path],
    ) -> None:

        if not shots:
            raise ValueError(
                "Cannot assemble a film without shots."
            )

        for shot in shots:
            if not shot.exists():
                raise FileNotFoundError(
                    f"Missing shot: {shot}"
                )

            if shot.stat().st_size <= 0:
                raise RuntimeError(
                    f"Empty shot: {shot}"
                )

    def create_concat_file(
        self,
        shots: list[Path],
        concat_path: Path,
    ) -> Path:

        self.validate_shots(shots)

        concat_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        lines = []

        for shot in shots:
            escaped = str(
                shot.resolve()
            ).replace("'", "'\\''")

            lines.append(
                f"file '{escaped}'"
            )

        concat_path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

        return concat_path

    def assemble(
        self,
        shots: list[Path],
        output_path: Path,
    ) -> Path:

        self.validate_shots(shots)

        concat_file = (
            output_path.parent
            / "concat.txt"
        )

        self.create_concat_file(
            shots,
            concat_file,
        )

        output_path.parent.mkdir(
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
            "-c",
            "copy",
            str(output_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "FFmpeg assembly failed:\n"
                + result.stderr
            )

        if not output_path.exists():
            raise RuntimeError(
                "Assembly reported success but "
                "the final MP4 was not created."
            )

        if output_path.stat().st_size <= 0:
            raise RuntimeError(
                "Final assembled MP4 is empty."
            )

        return output_path
