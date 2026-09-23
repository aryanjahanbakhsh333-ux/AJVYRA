from __future__ import annotations

from pathlib import Path
import json

from flask import Flask, jsonify, send_file

from ajvyra_ai_shot_engine_v6 import AJVYRAShotEngine


app = Flask(__name__)
engine = AJVYRAShotEngine()


@app.get("/api/shots")
def all_shots():

    return jsonify({
        "project": "AJVYRA",
        "total": len(engine.shots),
        "shots": engine.shots,
    })


@app.get("/api/shots/ready")
def ready_shots():

    ready = [
        shot
        for shot in engine.shots
        if shot.get("status") == "ready"
    ]

    return jsonify({
        "total": len(ready),
        "shots": ready,
    })


@app.get("/api/shots/<int:number>")
def shot(number):

    matches = [
        s for s in engine.shots
        if s.get("number") == number
    ]

    if not matches:
        return jsonify({
            "error": "shot_not_found"
        }), 404

    return jsonify(matches[-1])


@app.get("/api/shots/<int:number>/video")
def shot_video(number):

    matches = [
        s for s in engine.shots
        if s.get("number") == number
    ]

    if not matches:
        return jsonify({
            "error": "shot_not_found"
        }), 404

    video = matches[-1].get("video")

    if not video:
        return jsonify({
            "error": "video_not_ready"
        }), 404

    path = Path(video)

    if not path.exists():
        return jsonify({
            "error": "video_file_missing"
        }), 404

    return send_file(
        path,
        mimetype="video/mp4"
    )


@app.get("/api/status")
def status():

    total = len(engine.shots)

    ready = sum(
        s.get("status") == "ready"
        for s in engine.shots
    )

    queued = sum(
        s.get("status") == "queued"
        for s in engine.shots
    )

    return jsonify({
        "project": "AJVYRA",
        "total": total,
        "ready": ready,
        "queued": queued,
        "running": total - ready - queued,
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8090,
        debug=False
    )
