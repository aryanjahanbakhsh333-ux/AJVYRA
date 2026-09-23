from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path


class AJVYRARealPublicPublisher:

    def __init__(
        self,
        source_root="ComfyUI/output",
        public_root="ajvyra_public_media/anime",
        episode_id="episode_01",
    ):
        self.source_root = Path(source_root)
        self.public_root = Path(public_root)
        self.episode_id = episode_id

        self.episode_root = (
            self.public_root / self.episode_id
        )

        self.shots_root = (
            self.episode_root / "shots"
        )

        self.shots_root.mkdir(
            parents=True,
            exist_ok=True
        )

    # ---------------------------------------------------------
    # VIDEO VALIDATION
    # ---------------------------------------------------------

    def validate_video(self, path: Path):

        if not path.exists():
            return False

        if not path.is_file():
            return False

        if path.stat().st_size < 100_000:
            return False

        if path.suffix.lower() != ".mp4":
            return False

        try:
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v:0",
                    "-show_entries",
                    "stream=codec_name,width,height",
                    "-of",
                    "json",
                    str(path),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                return False

            data = json.loads(
                result.stdout
            )

            streams = data.get(
                "streams",
                []
            )

            if not streams:
                return False

            stream = streams[0]

            if not stream.get(
                "codec_name"
            ):
                return False

            if not stream.get("width"):
                return False

            if not stream.get("height"):
                return False

            return True

        except Exception:
            return False

    # ---------------------------------------------------------
    # DURATION
    # ---------------------------------------------------------

    def duration(self, path: Path):

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            return 0.0

        try:
            return float(
                result.stdout.strip()
            )
        except Exception:
            return 0.0

    # ---------------------------------------------------------
    # SHOT NUMBER
    # ---------------------------------------------------------

    def shot_number(self, path: Path):

        name = path.stem.lower()

        if "shot_" not in name:
            return None

        try:
            value = name.split(
                "shot_",
                1
            )[1]

            digits = ""

            for char in value:
                if char.isdigit():
                    digits += char
                else:
                    break

            if not digits:
                return None

            return int(digits)

        except Exception:
            return None

    # ---------------------------------------------------------
    # FIND REAL MP4 FILES
    # ---------------------------------------------------------

    def find_new_videos(self):

        if not self.source_root.exists():
            return []

        videos = []

        for file in self.source_root.rglob(
            "*.mp4"
        ):

            if self.validate_video(file):
                videos.append(file)

        return sorted(
            videos,
            key=lambda x: x.stat().st_mtime
        )

    # ---------------------------------------------------------
    # PUBLISH ONE SHOT
    # ---------------------------------------------------------

    def publish(self, source: Path):

        number = self.shot_number(
            source
        )

        if number is None:
            return None

        target_dir = (
            self.shots_root
            / f"shot_{number:04d}"
        )

        target_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        temporary = (
            target_dir
            / "main.mp4.part"
        )

        target = (
            target_dir
            / "main.mp4"
        )

        shutil.copy2(
            source,
            temporary
        )

        if not self.validate_video(
            temporary
        ):
            temporary.unlink(
                missing_ok=True
            )
            raise RuntimeError(
                f"Invalid generated video: {source}"
            )

        temporary.replace(
            target
        )

        seconds = self.duration(
            target
        )

        return {
            "shot": number,
            "status": "READY",
            "file": str(target),
            "url": (
                f"/media/anime/"
                f"{self.episode_id}/"
                f"shots/"
                f"shot_{number:04d}/"
                f"main.mp4"
            ),
            "duration_seconds": round(
                seconds,
                3
            ),
            "size_bytes":
                target.stat().st_size,
            "published_at":
                time.time(),
        }

    # ---------------------------------------------------------
    # MANIFEST
    # ---------------------------------------------------------

    def build_manifest(self):

        shots = []

        for shot_dir in sorted(
            self.shots_root.glob(
                "shot_*"
            )
        ):

            video = (
                shot_dir / "main.mp4"
            )

            if not self.validate_video(
                video
            ):
                continue

            number = self.shot_number(
                video
            )

            if number is None:
                continue

            shots.append({
                "shot": number,
                "status": "READY",
                "url": (
                    f"/media/anime/"
                    f"{self.episode_id}/"
                    f"shots/"
                    f"shot_{number:04d}/"
                    f"main.mp4"
                ),
                "duration_seconds":
                    round(
                        self.duration(video),
                        3
                    ),
                "size_bytes":
                    video.stat().st_size,
            })

        shots.sort(
            key=lambda x: x["shot"]
        )

        manifest = {
            "project": "AJVYRA",
            "episode": self.episode_id,
            "real_media_only": True,
            "shot_count": len(shots),
            "shots": shots,
            "updated_at": time.time(),
        }

        output = (
            self.episode_root
            / "manifest.json"
        )

        output.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return manifest

    # ---------------------------------------------------------
    # SYNC EVERYTHING
    # ---------------------------------------------------------

    def sync(self):

        published = []

        for video in self.find_new_videos():

            number = self.shot_number(
                video
            )

            if number is None:
                continue

            destination = (
                self.shots_root
                / f"shot_{number:04d}"
                / "main.mp4"
            )

            if destination.exists():
                continue

            try:
                item = self.publish(
                    video
                )

                if item:
                    published.append(
                        item
                    )

            except Exception as error:
                print(
                    "[AJVYRA]",
                    "publish failed:",
                    error
                )

        manifest = self.build_manifest()

        return {
            "published_now":
                published,
            "manifest":
                manifest,
        }

    # ---------------------------------------------------------
    # CONTINUOUS MODE
    # ---------------------------------------------------------

    def watch(
        self,
        interval=10
    ):

        print(
            "AJVYRA REAL SHOT PUBLICATION"
        )

        print(
            f"Episode: {self.episode_id}"
        )

        while True:

            try:

                result = self.sync()

                count = (
                    result[
                        "manifest"
                    ][
                        "shot_count"
                    ]
                )

                if result[
                    "published_now"
                ]:
                    print(
                        f"[AJVYRA] "
                        f"{len(result['published_now'])} "
                        f"new real shot(s) published."
                    )

                print(
                    f"[AJVYRA] "
                    f"{count} real shot(s) "
                    f"available."
                )

                time.sleep(
                    interval
                )

            except KeyboardInterrupt:
                print(
                    "Stopped."
                )
                break

            except Exception as error:

                print(
                    "[AJVYRA ERROR]",
                    error
                )

                time.sleep(
                    interval
                )


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        default="ComfyUI/output"
    )

    parser.add_argument(
        "--public",
        default="ajvyra_public_media/anime"
    )

    parser.add_argument(
        "--episode",
        default="episode_01"
    )

    parser.add_argument(
        "--watch",
        action="store_true"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=10
    )

    args = parser.parse_args()

    publisher = (
        AJVYRARealPublicPublisher(
            source_root=args.source,
            public_root=args.public,
            episode_id=args.episode,
        )
    )

    if args.watch:

        publisher.watch(
            args.interval
        )

    else:

        result = publisher.sync()

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )


if __name__ == "__main__":
    main()
