59 — ajvyra_real_shot_worker_v7.py

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

from ajvyra_ai_shot_engine_v6 import (
    AJVYRAShotEngine
)

from ajvyra_wan_shot_production_bridge_v7 import (
    WanShotProductionBridge
)

from ajvyra_shot_continuity_system_v7 import (
    ContinuitySystem
)


ROOT = Path(__file__).resolve().parent
SHOTS_DIR = ROOT / "ajvyra_shots"
VIDEO_DIR = SHOTS_DIR / "videos"

ENGINE = AJVYRAShotEngine()
WAN = WanShotProductionBridge()
CONTINUITY = ContinuitySystem()


class RealShotWorker:

    def __init__(self):
        self.max_retries = 3

    def build_prompt(self, shot: dict) -> str:

        return f"""
Create one continuous 10-second cinematic
original anime video shot.

GENRE:
{shot["genre"]}

SCENE:
{shot["prompt"]}

{CONTINUITY.context()}

Animation requirements:
- continuous motion
- cinematic camera movement
- stable character identity
- stable clothing
- stable environment
- coherent lighting
- coherent anatomy
- expressive emotion
- no text
- no watermark
- no logo

The result must be a real video,
not a still image.
"""

    def build_workflow(
        self,
        shot: dict
    ) -> dict:

        prompt = self.build_prompt(shot)

        workflow_file = (
            ROOT /
            "ajvyra_workflows" /
            "wan_shot_workflow.json"
        )

        if not workflow_file.exists():
            raise FileNotFoundError(
                "Missing Wan workflow template: "
                f"{workflow_file}"
            )

        workflow = json.loads(
            workflow_file.read_text(
                encoding="utf-8"
            )
        )

        text_blob = json.dumps(
            workflow,
            ensure_ascii=False
        )

        text_blob = text_blob.replace(
            "{{POSITIVE_PROMPT}}",
            prompt
        )

        text_blob = text_blob.replace(
            "{{NEGATIVE_PROMPT}}",
            shot["negative_prompt"]
        )

        text_blob = text_blob.replace(
            "{{SEED}}",
            str(shot["number"] * 7919)
        )

        return json.loads(text_blob)

    def mark_ready(
        self,
        shot: dict,
        video: Path
    ):

        shot["status"] = "ready"
        shot["video"] = str(video)

        for item in ENGINE.shots:

            if item.get("id") == shot.get("id"):
                item.update(shot)
                break

        ENGINE._save()

    def process(self, shot: dict):

        if not WAN.available():
            raise RuntimeError(
                "ComfyUI/Wan engine is not available."
            )

        workflow = self.build_workflow(
            shot
        )

        prompt_id = WAN.queue(
            workflow,
            client_id=shot["id"]
        )

        shot["status"] = "running"
        ENGINE._save()

        history = WAN.wait_for_completion(
            prompt_id,
            timeout_seconds=3600
        )

        output = WAN.find_video_output(
            history
        )

        if not output:
            raise RuntimeError(
                "Wan finished without a video output."
            )

        destination = (
            VIDEO_DIR /
            f"episode_{shot['episode']:02d}_"
            f"shot_{shot['number']:03d}.mp4"
        )

        WAN.download_output(
            output,
            destination
        )

        self.validate_video(
            destination
        )

        self.mark_ready(
            shot,
            destination
        )

        return destination

    def validate_video(
        self,
        video: Path
    ):

        if not video.exists():
            raise RuntimeError(
                "Video does not exist."
            )

        if video.stat().st_size < 100_000:
            raise RuntimeError(
                "Video is too small."
            )

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:"
                "nokey=1",
                str(video),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "ffprobe could not validate video."
            )

        duration = float(
            result.stdout.strip()
        )

        if not 8.0 <= duration <= 12.0:
            raise RuntimeError(
                f"Invalid shot duration: {duration}"
            )

    def process_next(self):

        queued = [
            s for s in ENGINE.shots
            if s.get("status") == "queued"
        ]

        if not queued:
            shot = ENGINE.next_shot()

        else:
            shot = queued[0]

        return self.process(shot)


if __name__ == "__main__":

    worker = RealShotWorker()

    while True:

        try:
            worker.process_next()

        except Exception as error:

            print(
                "[AJVYRA SHOT WORKER ERROR]",
                error
            )

            time.sleep(60)
