from __future__ import annotations

import json
import time
import urllib.request
import uuid


class ComfyUIClient:

    def __init__(
        self,
        base_url: str,
    ):
        self.base_url = base_url.rstrip("/")

    def _request(
        self,
        method: str,
        path: str,
        body=None,
    ):
        data = None

        headers = {
            "Content-Type": "application/json"
        }

        if body is not None:
            data = json.dumps(
                body
            ).encode("utf-8")

        request = urllib.request.Request(
            self.base_url + path,
            data=data,
            headers=headers,
            method=method,
        )

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            raw = response.read()

        if not raw:
            return {}

        return json.loads(
            raw.decode("utf-8")
        )

    def queue_prompt(
        self,
        workflow,
    ) -> str:

        client_id = str(
            uuid.uuid4()
        )

        result = self._request(
            "POST",
            "/prompt",
            {
                "client_id": client_id,
                "prompt": workflow,
            },
        )

        prompt_id = result.get(
            "prompt_id"
        )

        if not prompt_id:
            raise RuntimeError(
                "ComfyUI did not return prompt_id."
            )

        return prompt_id

    def history(
        self,
        prompt_id: str,
    ):

        return self._request(
            "GET",
            f"/history/{prompt_id}"
        )

    def wait(
        self,
        prompt_id: str,
        timeout: int = 3600,
        interval: int = 5,
    ):

        started = time.time()

        while True:

            if time.time() - started > timeout:
                raise TimeoutError(
                    "ComfyUI generation timed out."
                )

            history = self.history(
                prompt_id
            )

            if prompt_id in history:
                record = history[
                    prompt_id
                ]

                status = record.get(
                    "status",
                    {}
                )

                completed = status.get(
                    "completed",
                    False
                )

                messages = status.get(
                    "messages",
                    []
                )

                if completed:
                    return record

                for message in messages:
                    if (
                        isinstance(message, list)
                        and message
                        and message[0] == "execution_error"
                    ):
                        raise RuntimeError(
                            str(message)
                        )

            time.sleep(interval)

    def find_outputs(
        self,
        history_record,
    ):
        outputs = []

        nodes = history_record.get(
            "outputs",
            {}
        )

        for node in nodes.values():

            files = node.get(
                "gifs",
                []
            )

            files += node.get(
                "videos",
                []
            )

            files += node.get(
                "images",
                []
            )

            outputs.extend(files)

        return outputs
