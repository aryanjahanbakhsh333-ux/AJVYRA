from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json

from ajvyra_browser_runtime_v1 import (
    AJVYRABrowserRuntime,
)


RUNTIME = AJVYRABrowserRuntime()


class AJVYRAAPIHandler(BaseHTTPRequestHandler):

    def _json(self, payload: dict, status: int = 200):
        data = json.dumps(
            payload,
            ensure_ascii=False,
            default=str,
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(data)),
        )
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, GET, OPTIONS",
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )
        self.end_headers()

    def do_POST(self):
        length = int(
            self.headers.get(
                "Content-Length",
                "0",
            )
        )

        raw = self.rfile.read(length)

        try:
            body = json.loads(
                raw.decode("utf-8")
            )
        except Exception:
            self._json(
                {
                    "ok": False,
                    "error": "Invalid JSON.",
                },
                400,
            )
            return

        try:
            if self.path == "/api/game/launch":
                result = RUNTIME.launch(
                    int(body["game_id"])
                )

            elif self.path == "/api/game/action":
                result = RUNTIME.action(
                    body["session_id"],
                    body["action"],
                    body.get("params", {}),
                )

            elif self.path == "/api/game/state":
                result = RUNTIME.state(
                    body["session_id"]
                )

            elif self.path == "/api/game/stop":
                result = RUNTIME.stop(
                    body["session_id"]
                )

            else:
                self._json(
                    {
                        "ok": False,
                        "error": "Not found.",
                    },
                    404,
                )
                return

            self._json(result)

        except Exception as exc:
            self._json(
                {
                    "ok": False,
                    "error": str(exc),
                },
                500,
            )

    def log_message(self, format, *args):
        return
