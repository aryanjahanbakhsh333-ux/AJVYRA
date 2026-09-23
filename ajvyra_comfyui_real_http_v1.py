"""
AJVYRA — REAL COMFYUI HTTP CLIENT v1

این فایل واقعاً با ComfyUI محلی ارتباط می‌گیرد.

هیچ خروجی‌ای را خودش تولیدشده فرض نمی‌کند.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class ComfyUIError(RuntimeError):
    pass


class RealComfyUIClient:

    def __init__(
        self,
        base_url: str,
        timeout: int = 7200,
        poll_seconds: float = 3.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.poll_seconds = poll_seconds

        self.client_id = str(uuid.uuid4())

    def _request(
        self,
        method: str,
        path: str,
        payload: dict | None = None,
    ):
        url = self.base_url + path

        body = None
        headers = {}

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(
            url,
            data=body,
            headers=headers,
            method=method,
        )

        try:
            with urlopen(request, timeout=60) as response:
                raw = response.read()

                content_type = response.headers.get(
                    "Content-Type",
                    "",
                )

                if "application/json" in content_type:
                    return json.loads(raw.decode("utf-8"))

                return raw

        except HTTPError as exc:
            detail = exc.read().decode(
                "utf-8",
                errors="replace",
            )

            raise ComfyUIError(
                f"ComfyUI HTTP {exc.code}: {detail}"
            ) from exc

        except URLError as exc:
            raise ComfyUIError(
                f"Cannot connect to ComfyUI: {exc}"
            ) from exc

    def health_check(self) -> bool:
        try:
            self._request("GET", "/system_stats")
            return True
        except Exception:
            return False

    def submit_workflow(self, workflow: dict) -> str:

        payload = {
            "prompt": workflow,
            "client_id": self.client_id,
        }

        result = self._request(
            "POST",
            "/prompt",
            payload,
        )

        prompt_id = result.get("prompt_id")

        if not prompt_id:
            raise ComfyUIError(
                f"ComfyUI did not return prompt_id: {result}"
            )

        return str(prompt_id)

    def get_history(self, prompt_id: str) -> dict:
        result = self._request(
            "GET",
            f"/history/{prompt_id}",
        )

        if not isinstance(result, dict):
            raise ComfyUIError(
                "Invalid history response."
            )

        return result

    def wait_for_completion(
        self,
        prompt_id: str,
    ) -> dict:

        started = time.time()

        while True:

            if time.time() - started > self.timeout:
                raise TimeoutError(
                    f"ComfyUI generation timed out: {prompt_id}"
                )

            history = self.get_history(prompt_id)

            entry = history.get(prompt_id)

            if entry:

                status = entry.get("status", {})

                if status.get("status_str") == "error":
                    raise ComfyUIError(
                        f"ComfyUI generation failed: {entry}"
                    )

                if entry.get("outputs"):
                    return entry

            time.sleep(self.poll_seconds)

    def list_output_files(
        self,
        history_entry: dict,
    ) -> list[dict]:

        outputs = history_entry.get("outputs", {})
        found = []

        for node_id, node_output in outputs.items():

            for key in (
                "gifs",
                "videos",
                "images",
            ):
                items = node_output.get(key, [])

                for item in items:
                    if "filename" in item:
                        found.append(
                            {
                                "node_id": node_id,
                                "filename": item["filename"],
                                "subfolder": item.get(
                                    "subfolder",
                                    "",
                                ),
                                "type": item.get(
                                    "type",
                                    "output",
                                ),
                            }
                        )

        return found

    def download_output(
        self,
        output_info: dict,
        destination: Path,
    ) -> Path:

        query = urlencode(
            {
                "filename": output_info["filename"],
                "subfolder": output_info.get(
                    "subfolder",
                    "",
                ),
                "type": output_info.get(
                    "type",
                    "output",
                ),
            }
        )

        data = self._request(
            "GET",
            f"/view?{query}",
        )

        if not isinstance(data, bytes):
            raise ComfyUIError(
                "ComfyUI output download did not return bytes."
            )

        if len(data) < 100_000:
            raise ComfyUIError(
                "Downloaded media is suspiciously small."
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(data)

        if destination.stat().st_size < 100_000:
            raise ComfyUIError(
                "Downloaded output failed size validation."
            )

        return destination
