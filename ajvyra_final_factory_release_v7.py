62 — ajvyra_final_factory_release_v7.py

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHOT_DIR = ROOT / "ajvyra_shots"
VIDEO_DIR = SHOT_DIR / "videos"
RELEASE = ROOT / "ajvyra_release"


def run(command):

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr or
            result.stdout
        )

    return result.stdout


def collect_ready_shots():

    database = (
        SHOT_DIR /
        "shot_database.json"
    )

    if not database.exists():
        raise RuntimeError(
            "Shot database does not exist."
        )

    data = json.loads(
        database.read_text(
            encoding="utf-8"
        )
    )

    ready = []

    for shot in data:

        if shot.get("status") != "ready":
            continue

        video = Path(
            shot.get("video", "")
        )

        if not video.exists():
            continue

        ready.append(
            (shot, video)
        )

    return sorted(
        ready,
        key=lambda item: item[0]["number"]
    )


def build_episode():

    ready = collect_ready_shots()

    if len(ready) < 1:
        raise RuntimeError(
            "No real shots are ready."
        )

    RELEASE.mkdir(
        parents=True,
        exist_ok=True
    )

    concat_file = (
        RELEASE /
        "episode_01_concat.txt"
    )

    lines = []

    for _, video in ready:

        safe = str(
            video.resolve()
        ).replace(
            "'",
            "'\\''"
        )

        lines.append(
            f"file '{safe}'"
        )

    concat_file.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    output = (
        RELEASE /
        "AJVYRA_EPISODE_01.mp4"
    )

    run([
        "ffmpeg",
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
    ])

    return output, len(ready)


def write_manifest(
    episode: Path,
    count: int
):

    manifest = {
        "project": "AJVYRA",
        "episode": 1,
        "real_video": True,
        "shots": count,
        "duration_per_shot": 10,
        "video": str(episode),
        "status": "ready"
    }

    path = (
        RELEASE /
        "episode_01_manifest.json"
    )

    path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


if __name__ == "__main__":

    episode, count = build_episode()

    write_manifest(
        episode,
        count
    )

    print(
        f"AJVYRA EPISODE READY: "
        f"{count} real shots"
    )
