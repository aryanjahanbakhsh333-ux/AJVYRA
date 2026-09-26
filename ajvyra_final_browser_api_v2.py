from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from ajvyra_final_browser_game_runtime_v2 import runtime


ROOT = Path(__file__).resolve().parent


class APIHandler(BaseHTTPRequestHandler):

    def _send(self, status, data, content_type="application/json"):
        if isinstance(data, str):
            payload = data.encode("utf-8")
        else:
            payload = json.dumps(
                data,
                ensure_ascii=False,
                default=str,
            ).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/games":
            self._send(200, {
                "target": 300,
                "games": runtime.discover(),
            })
            return

        if path.startswith("/api/game/"):
            try:
                game_id = int(path.split("/")[-1])
                session = runtime.create(game_id)

                frame = runtime.frame(session)

                self.server.sessions[
                    str(game_id)
                ] = session

                self._send(200, {
                    "session": str(game_id),
                    "frame": frame.__dict__,
                })
                return
            except Exception as exc:
                self._send(500, {"error": str(exc)})
                return

        if path in ("/", "/index.html"):
            html = (ROOT / "ajvyra_final_game_shell_v1.html").read_text(
                encoding="utf-8"
            )
            self._send(200, html, "text/html; charset=utf-8")
            return

        self._send(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path

        if path.startswith("/api/action/"):
            try:
                parts = path.strip("/").split("/")
                game_id = parts[2]
                action = parts[3]

                session = self.server.sessions[game_id]
                result = runtime.execute(session, action)
                frame = runtime.frame(session)

                self._send(200, {
                    "result": result,
                    "frame": frame.__dict__,
                })
                return

            except Exception as exc:
                self._send(400, {"error": str(exc)})
                return

        self._send(404, {"error": "not found"})


def serve(host="0.0.0.0", port=8080):
    server = ThreadingHTTPServer((host, port), APIHandler)
    server.sessions = {}

    print(f"AJVYRA Final Runtime: http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    serve()
