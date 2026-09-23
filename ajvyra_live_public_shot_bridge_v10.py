from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any


# ============================================================
# AJVYRA LIVE PUBLIC SHOT BRIDGE v10
# ============================================================
#
# REAL PIPELINE
#
# Wan / ComfyUI
#      ↓
# main.mp4
#      ↓
# Public Media Library
#      ↓
# manifest.json
#      ↓
# AJVYRA website
#      ↓
# Browser Video Player
#
# No fake videos.
# No placeholder entries.
#
# A shot becomes PUBLIC only when a real MP4 exists
# and passes the basic integrity checks.
# ============================================================


class AJVYRAPublicConfig:

    MEDIA_ROOT = Path(
        "ajvyra_public_media"
    )

    ANIME_ROOT = (
        MEDIA_ROOT / "anime"
    )

    MANIFEST = (
        MEDIA_ROOT / "anime_manifest.json"
    )

    SITE_ROOT = Path(
        "ajvyra_site"
    )

    SITE_ANIME_ROOT = (
        SITE_ROOT / "anime"
    )

    MIN_VIDEO_SIZE = 100_000

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".webm",
        ".mov",
        ".mkv",
    }


# ============================================================
# PUBLIC SHOT BRIDGE
# ============================================================

class AJVYRALivePublicShotBridge:

    def __init__(
        self,
        config=AJVYRAPublicConfig,
    ):

        self.config = config

        self.config.ANIME_ROOT.mkdir(
            parents=True,
            exist_ok=True
        )

        self.config.SITE_ANIME_ROOT.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Locate real generated shots
    # --------------------------------------------------------

    def find_generated_shots(
        self,
        episode_id: str,
    ) -> list[Path]:

        episode_root = (
            self.config.ANIME_ROOT
            / episode_id
        )

        if not episode_root.exists():
            return []

        results = []

        for file in episode_root.rglob("*"):

            if not file.is_file():
                continue

            if (
                file.suffix.lower()
                not in self.config.VIDEO_EXTENSIONS
            ):
                continue

            if (
                file.stat().st_size
                < self.config.MIN_VIDEO_SIZE
            ):
                continue

            results.append(file)

        return sorted(results)

    # --------------------------------------------------------
    # Check MP4
    # --------------------------------------------------------

    def validate_video(
        self,
        video: Path,
    ) -> bool:

        if not video.exists():
            return False

        if not video.is_file():
            return False

        if (
            video.stat().st_size
            < self.config.MIN_VIDEO_SIZE
        ):
            return False

        return (
            video.suffix.lower()
            in self.config.VIDEO_EXTENSIONS
        )

    # --------------------------------------------------------
    # Extract shot number
    # --------------------------------------------------------

    @staticmethod
    def shot_number(
        path: Path,
    ) -> int | None:

        name = path.stem.lower()

        # shot_0001
        if "shot_" in name:

            try:

                value = (
                    name.split(
                        "shot_",
                        1
                    )[1]
                    .split("_", 1)[0]
                )

                return int(value)

            except Exception:
                pass

        # Fallback: search digits
        digits = ""

        for char in name:

            if char.isdigit():
                digits += char

        if digits:

            try:
                return int(digits)
            except Exception:
                return None

        return None

    # --------------------------------------------------------
    # Public URL
    # --------------------------------------------------------

    @staticmethod
    def public_url(
        episode_id: str,
        shot_number: int,
    ) -> str:

        return (
            "/media/anime/"
            f"{episode_id}/"
            f"shots/"
            f"shot_{shot_number:04d}/"
            "main.mp4"
        )

    # --------------------------------------------------------
    # Copy into public structure
    # --------------------------------------------------------

    def publish_shot(
        self,
        episode_id: str,
        video: Path,
    ) -> dict[str, Any]:

        if not self.validate_video(video):

            raise ValueError(
                f"Invalid real video: {video}"
            )

        number = self.shot_number(
            video
        )

        if number is None:

            raise ValueError(
                f"Cannot determine shot number: "
                f"{video}"
            )

        target_dir = (
            self.config.SITE_ANIME_ROOT
            / episode_id
            / "shots"
            / f"shot_{number:04d}"
        )

        target_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        target = (
            target_dir
            / "main.mp4"
        )

        # Do not expose a half-written file.
        temporary = (
            target_dir
            / "main.mp4.part"
        )

        shutil.copy2(
            video,
            temporary
        )

        if not self.validate_video(
            temporary
        ):

            temporary.unlink(
                missing_ok=True
            )

            raise RuntimeError(
                "Copied video failed integrity check."
            )

        temporary.replace(
            target
        )

        return {
            "episode": episode_id,
            "shot": number,
            "status": "READY",
            "file": str(target),
            "url": self.public_url(
                episode_id,
                number
            ),
            "size_bytes":
                target.stat().st_size,
            "published_at":
                time.time(),
        }

    # --------------------------------------------------------
    # Build episode manifest
    # --------------------------------------------------------

    def build_episode_manifest(
        self,
        episode_id: str,
    ) -> dict[str, Any]:

        source_files = (
            self.find_generated_shots(
                episode_id
            )
        )

        published = []

        for source in source_files:

            try:

                item = self.publish_shot(
                    episode_id,
                    source
                )

                published.append(
                    item
                )

            except Exception:
                continue

        published.sort(
            key=lambda item:
            item["shot"]
        )

        manifest = {

            "project":
                "AJVYRA",

            "episode":
                episode_id,

            "status":
                (
                    "READY"
                    if published
                    else "EMPTY"
                ),

            "shot_count":
                len(published),

            "shots":
                published,

            "updated_at":
                time.time(),
        }

        episode_manifest = (
            self.config.SITE_ANIME_ROOT
            / episode_id
            / "manifest.json"
        )

        episode_manifest.write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return manifest

    # --------------------------------------------------------
    # Build complete website manifest
    # --------------------------------------------------------

    def build_global_manifest(
        self,
    ) -> dict[str, Any]:

        episodes = []

        if self.config.SITE_ANIME_ROOT.exists():

            for directory in sorted(
                self.config.SITE_ANIME_ROOT.iterdir()
            ):

                if not directory.is_dir():
                    continue

                manifest_file = (
                    directory
                    / "manifest.json"
                )

                if not manifest_file.exists():
                    continue

                try:

                    data = json.loads(
                        manifest_file.read_text(
                            encoding="utf-8"
                        )
                    )

                    episodes.append(
                        data
                    )

                except Exception:
                    continue

        result = {

            "project":
                "AJVYRA",

            "library":
                "anime",

            "real_media_only":
                True,

            "episode_count":
                len(episodes),

            "episodes":
                episodes,

            "updated_at":
                time.time(),
        }

        self.config.MANIFEST.write_text(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return result

    # --------------------------------------------------------
    # Synchronize everything
    # --------------------------------------------------------

    def sync(
        self,
        episode_id: str,
    ) -> dict[str, Any]:

        episode = (
            self.build_episode_manifest(
                episode_id
            )
        )

        global_manifest = (
            self.build_global_manifest()
        )

        return {
            "episode":
                episode,

            "global":
                global_manifest,
        }

    # --------------------------------------------------------
    # Watch mode
    #
    # Whenever Wan creates a new MP4:
    #
    # MP4 → Public → Manifest → Website
    # --------------------------------------------------------

    def watch(
        self,
        episode_id: str,
        interval: int = 10,
    ):

        print(
            "AJVYRA LIVE PUBLIC SHOT BRIDGE"
        )

        print(
            f"Episode: {episode_id}"
        )

        print(
            "Watching for real generated videos..."
        )

        last_signature = ""

        while True:

            try:

                result = self.sync(
                    episode_id
                )

                shots = (
                    result[
                        "episode"
                    ][
                        "shots"
                    ]
                )

                signature = "|".join(
                    f"{x['shot']}:{x['size_bytes']}"
                    for x in shots
                )

                if signature != last_signature:

                    print(
                        f"[AJVYRA] "
                        f"{len(shots)} real shots "
                        f"available on site."
                    )

                    last_signature = signature

                time.sleep(
                    interval
                )

            except KeyboardInterrupt:

                print(
                    "\nAJVYRA bridge stopped."
                )

                break

            except Exception as exc:

                print(
                    "[AJVYRA ERROR]",
                    exc
                )

                time.sleep(
                    interval
                )


# ============================================================
# SITE PLAYER
#
# This generates a simple browser page that reads the
# manifest and automatically displays every READY shot.
# ============================================================

def create_site_player(
    episode_id: str,
):

    config = AJVYRAPublicConfig()

    player_dir = (
        config.SITE_ANIME_ROOT
        / episode_id
    )

    player_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    player = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>AJVYRA Anime</title>

<style>

html,
body {
    margin: 0;
    padding: 0;
    background: #000;
    color: #fff;
    font-family: Arial, sans-serif;
}

body {
    min-height: 100vh;
}

header {
    padding: 18px;
    border-bottom: 1px solid #222;
}

h1 {
    margin: 0;
    font-size: 20px;
}

#status {
    margin-top: 7px;
    color: #888;
    font-size: 13px;
}

#player {
    width: 100%;
    max-width: 1100px;
    margin: 25px auto 0;
    display: block;
    background: #050505;
}

#shots {
    max-width: 1100px;
    margin: 20px auto;
    padding: 0 15px 40px;
}

.shot {
    width: 100%;
    padding: 14px;
    margin-bottom: 8px;
    box-sizing: border-box;
    background: #101010;
    border: 1px solid #222;
    color: white;
    cursor: pointer;
    text-align: left;
}

.shot:hover {
    background: #181818;
}

.ready {
    color: #fff;
}

</style>
</head>

<body>

<header>

<h1>AJVYRA</h1>

<div id="status">
Loading real anime shots...
</div>

</header>

<video
    id="player"
    controls
    playsinline
></video>

<div id="shots"></div>

<script>

const episode =
    location.pathname
        .split("/")
        .filter(Boolean)
        .pop();

const manifestURL =
    "manifest.json";

const player =
    document.getElementById("player");

const shots =
    document.getElementById("shots");

const status =
    document.getElementById("status");


async function loadAnime() {

    try {

        const response =
            await fetch(
                manifestURL,
                {
                    cache: "no-store"
                }
            );

        if (!response.ok) {
            throw new Error(
                "Manifest unavailable"
            );
        }

        const data =
            await response.json();

        const list =
            data.shots || [];

        shots.innerHTML = "";

        status.textContent =
            list.length +
            " real shot(s) available";

        for (
            const shot of list
        ) {

            if (
                shot.status !== "READY"
            ) {
                continue;
            }

            const button =
                document.createElement(
                    "button"
                );

            button.className =
                "shot ready";

            button.textContent =
                "SHOT " +
                String(
                    shot.shot
                ).padStart(
                    4,
                    "0"
                );

            button.onclick =
                () => {

                    player.src =
                        shot.url;

                    player.play()
                        .catch(
                            () => {}
                        );
                };

            shots.appendChild(
                button
            );
        }

        if (list.length > 0) {

            player.src =
                list[0].url;

        }

    } catch (error) {

        status.textContent =
            "Waiting for real generated shots...";

        console.error(error);
    }
}


loadAnime();

setInterval(
    loadAnime,
    10000
);

</script>

</body>
</html>
"""

    (player_dir / "index.html").write_text(
        player,
        encoding="utf-8"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=[
            "sync",
            "watch",
            "player",
        ]
    )

    parser.add_argument(
        "--episode",
        default="episode_01"
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=10
    )

    args = parser.parse_args()

    bridge = (
        AJVYRALivePublicShotBridge()
    )

    if args.command == "sync":

        result = bridge.sync(
            args.episode
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )

    elif args.command == "watch":

        bridge.watch(
            args.episode,
            args.interval
        )

    elif args.command == "player":

        create_site_player(
            args.episode
        )

        print(
            "AJVYRA player created."
        )


if __name__ == "__main__":
    main()
