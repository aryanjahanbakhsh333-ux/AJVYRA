from __future__ import annotations

import json
from pathlib import Path

from flask import (
    Flask,
    jsonify,
    send_from_directory,
    abort,
)


BASE = Path(
    "ajvyra_public_media"
).resolve()

ANIME = (
    BASE / "anime"
)

app = Flask(
    __name__,
    static_folder=None
)


# ============================================================
# REAL VIDEO DELIVERY
# ============================================================

@app.route(
    "/media/anime/<episode>/shots/<shot>/main.mp4"
)
def video(
    episode,
    shot
):

    folder = (
        ANIME
        / episode
        / "shots"
        / shot
    )

    file = (
        folder / "main.mp4"
    )

    if not file.exists():
        abort(404)

    return send_from_directory(
        folder,
        "main.mp4",
        mimetype="video/mp4",
        conditional=True,
        max_age=3600,
    )


# ============================================================
# MANIFEST API
# ============================================================

@app.route(
    "/api/anime/<episode>/manifest"
)
def manifest(
    episode
):

    file = (
        ANIME
        / episode
        / "manifest.json"
    )

    if not file.exists():
        return jsonify({
            "project": "AJVYRA",
            "episode": episode,
            "real_media_only": True,
            "shot_count": 0,
            "shots": [],
        })

    data = json.loads(
        file.read_text(
            encoding="utf-8"
        )
    )

    return jsonify(data)


# ============================================================
# ANIME PLAYER
# ============================================================

@app.route(
    "/anime/<episode>"
)
def player(
    episode
):

    file = (
        ANIME
        / episode
        / "index.html"
    )

    if not file.exists():
        abort(404)

    return send_from_directory(
        file.parent,
        "index.html"
    )


# ============================================================
# HEALTH
# ============================================================

@app.route(
    "/api/status"
)
def status():

    episodes = []

    if ANIME.exists():

        for folder in sorted(
            ANIME.iterdir()
        ):

            if not folder.is_dir():
                continue

            manifest = (
                folder
                / "manifest.json"
            )

            if not manifest.exists():
                continue

            try:

                data = json.loads(
                    manifest.read_text(
                        encoding="utf-8"
                    )
                )

                episodes.append({
                    "episode":
                        data.get(
                            "episode"
                        ),
                    "shot_count":
                        data.get(
                            "shot_count",
                            0
                        ),
                })

            except Exception:
                continue

    return jsonify({
        "project": "AJVYRA",
        "real_media_only": True,
        "episodes": episodes,
    })


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
    )
