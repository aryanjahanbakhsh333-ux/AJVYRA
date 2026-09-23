57 — ajvyra_wan_shot_production_bridge_v7.py

from __future__ import annotations

import json
import time
import uuid
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
SHOTS = ROOT / "ajvyra_shots"
VIDEOS = SHOTS / "videos"
WORKFLOWS = ROOT / "ajvyra_workflows"

SHOTS.mkdir(exist_ok=True)
VIDEOS.mkdir(exist_ok=True)
WORKFLOWS.mkdir(exist_ok=True)

COMFY_URL = "http://127.0.0.1:8188"


class WanShotProductionBridge:

    def __init__(self, comfy_url: str = COMFY_URL):
        self.comfy_url = comfy_url.rstrip("/")

    def _request(
        self,
        path: str,
        method: str = "GET",
        payload: dict | None = None,
        timeout: int = 60,
    ) -> dict:

        data = None

        headers = {
            "Content-Type": "application/json"
        }

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            self.comfy_url + path,
            data=data,
            headers=headers,
            method=method,
        )

        with urllib.request.urlopen(
            request,
            timeout=timeout
        ) as response:

            raw = response.read()

            if not raw:
                return {}

            return json.loads(
                raw.decode("utf-8")
            )

    def available(self) -> bool:

        try:
            self._request(
                "/system_stats",
                timeout=10
            )
            return True
        except Exception:
            return False

    def queue(
        self,
        workflow: dict,
        client_id: str | None = None
    ) -> str:

        payload = {
            "prompt": workflow,
            "client_id": client_id or uuid.uuid4().hex,
        }

        result = self._request(
            "/prompt",
            method="POST",
            payload=payload,
        )

        prompt_id = result.get("prompt_id")

        if not prompt_id:
            raise RuntimeError(
                f"ComfyUI did not return prompt_id: {result}"
            )

        return prompt_id

    def history(self, prompt_id: str) -> dict:

        return self._request(
            f"/history/{prompt_id}",
            timeout=30
        )

    def wait_for_completion(
        self,
        prompt_id: str,
        timeout_seconds: int = 3600,
        poll_seconds: int = 5,
    ) -> dict:

        started = time.time()

        while True:

            if time.time() - started > timeout_seconds:
                raise TimeoutError(
                    f"Shot generation timed out: {prompt_id}"
                )

            history = self.history(prompt_id)

            if prompt_id in history:
                return history[prompt_id]

            time.sleep(poll_seconds)

    def find_video_output(
        self,
        history: dict
    ) -> dict | None:

        outputs = history.get("outputs", {})

        for node in outputs.values():

            for key in (
                "gifs",
                "videos",
                "video",
                "images",
            ):

                items = node.get(key)

                if not isinstance(items, list):
                    continue

                for item in items:

                    if not isinstance(item, dict):
                        continue

                    filename = item.get("filename")

                    if filename:
                        return {
                            "filename": filename,
                            "subfolder": item.get(
                                "subfolder",
                                ""
                            ),
                            "type": item.get(
                                "type",
                                "output"
                            ),
                        }

        return None

    def download_output(
        self,
        output: dict,
        destination: Path,
    ) -> Path:

        params = urllib.parse.urlencode({
            "filename": output["filename"],
            "subfolder": output.get(
                "subfolder",
                ""
            ),
            "type": output.get(
                "type",
                "output"
            ),
        })

        url = (
            f"{self.comfy_url}/view?"
            f"{params}"
        )

        request = urllib.request.Request(
            url,
            method="GET"
        )

        with urllib.request.urlopen(
            request,
            timeout=300
        ) as response:

            data = response.read()

        if len(data) < 100_000:
            raise RuntimeError(
                "Downloaded media is suspiciously small."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        destination.write_bytes(data)

        return destination
