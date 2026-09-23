"""
AJVYRA 30-Film FFmpeg Assembly V1
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run(command):
    result = subprocess.run(
        command,
        check=False
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg assembly failed."
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--queue",
        required=True
    )

    parser.add_argument(
        "--root",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    args = parser.parse_args()

    queue = load(
        Path(args.queue)
    )

    root = Path(
        args.root
    )

    output_root = Path(
        args.output
    )

    films = {}

    for job in queue["jobs"]:
        films.setdefault(
            job["film_id"],
            {
                "title": job["film_title"],
                "jobs": []
            }
        )["jobs"].append(job)

    for film_id, film in films.items():

        jobs = sorted(
            film["jobs"],
            key=lambda x: (
                x["scene_number"],
                x["shot_number"]
            )
        )

        concat_file = (
            output_root
            / "concat"
            / f"{film_id}.txt"
        )

        concat_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            concat_file,
            "w",
            encoding="utf-8"
        ) as f:

            for job in jobs:

                path = (
                    root /
                    Path(job["output_file"])
                )

                if not path.exists():
                    raise RuntimeError(
                        f"Missing video: {path}"
                    )

                escaped = (
                    str(path.resolve())
                    .replace("'", "'\\''")
                )

                f.write(
                    f"file '{escaped}'\n"
                )

        final_dir = (
            output_root /
            "films"
        )

        final_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        final_file = (
            final_dir /
            f"{film_id}.mp4"
        )

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(final_file)
        ]

        print(
            f"ASSEMBLING: {film['title']}"
        )

        run(command)

        if (
            not final_file.exists()
            or final_file.stat().st_size < 1024
        ):
            raise RuntimeError(
                f"Invalid final movie: {final_file}"
            )

        print(
            f"READY: {final_file}"
        )


if __name__ == "__main__":
    main()
