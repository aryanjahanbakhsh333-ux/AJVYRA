from __future__ import annotations

import subprocess
from pathlib import Path


class VideoAssembler:

    def assemble(
        self,
        clips,
        output: Path,
    ):

        clips = [
            Path(x)
            for x in clips
        ]

        clips = [
            x
            for x in clips
            if x.exists()
        ]

        if not clips:
            raise RuntimeError(
                "No real video clips available."
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        concat = output.parent / (
            "concat_list.txt"
        )

        lines = []

        for clip in clips:
            lines.append(
                "file "
                + repr(
                    str(
                        clip.resolve()
                    )
                )
            )

        concat.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat),
            "-c",
            "copy",
            str(output),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr
            )

        if not output.exists():
            raise RuntimeError(
                "FFmpeg did not create the final video."
            )

        return output
