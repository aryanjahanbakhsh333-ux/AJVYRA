from __future__ import annotations

import json
from ajvyra_browser_runtime_v1 import AJVYRABrowserRuntime


class BrowserBridge:
    def __init__(self) -> None:
        self.runtime = AJVYRABrowserRuntime()

    def handle(self, payload: str) -> str:
        try:
            request = json.loads(payload)
            command = request.get("command")

            if command == "launch":
                result = self.runtime.launch(
                    int(request["game_id"])
                )

            elif command == "action":
                result = self.runtime.action(
                    request["session_id"],
                    request["action"],
                    request.get("params", {}),
                )

            elif command == "state":
                result = self.runtime.state(
                    request["session_id"]
                )

            elif command == "stop":
                result = self.runtime.stop(
                    request["session_id"]
                )

            else:
                result = {
                    "ok": False,
                    "error": "Unknown browser command.",
                }

        except Exception as exc:
            result = {
                "ok": False,
                "error": str(exc),
            }

        return json.dumps(
            result,
            ensure_ascii=False,
            default=str,
        )
