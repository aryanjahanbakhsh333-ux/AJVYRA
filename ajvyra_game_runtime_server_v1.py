from __future__ import annotations

import json
import os
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse

from ajvyra_browser_api_v1 import (
    AJVYRAAPIHandler,
)


class AJVYRAHTTPHandler(AJVYRAAPIHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.path = "/ajvyra_game_browser.html"

        if parsed.path == "/ajvyra_game_browser.html":
            return self._serve_file(
                "ajvyra_game_browser.html",
                "text/html; charset=utf-8",
            )

        if parsed.path == "/ajvyra_game_browser_v1.js":
            return self._serve_file(
                "ajvyra_game_browser_v1.js",
                "application/javascript",
            )

        if parsed.path == "/ajvyra_game_browser_v1.css":
            return self._serve_file(
                "ajvyra_game_browser_v1.css",
                "text/css",
            )

        if parsed.path == "/ajvyra_game_manifest.json":
            return self._serve_file(
                "ajvyra_game_manifest.json",
                "application/json",
            )

        self.send_response(404)
        self.end_headers()

    def _serve_file(
        self,
        filename: str,
        content_type: str,
    ):
        base = os.path.dirname(
            os.path.abspath(__file__)
        )

        path = os.path.join(
            base,
            filename,
        )

        if not os.path.exists(path):
            self.send_response(404)
            self.end_headers()
            return

        with open(path, "rb") as file:
            data = file.read()

        self.send_response(200)
        self.send_header(
            "Content-Type",
            content_type,
        )
        self.send_header(
            "Content-Length",
            str(len(data)),
        )
        self.end_headers()

        self.wfile.write(data)


def start_server(
    host: str = "0.0.0.0",
    port: int = 8000,
):
    server = ThreadingHTTPServer(
        (host, port),
        AJVYRAHTTPHandler,
    )

    print(
        f"AJVYRA Runtime: "
        f"http://{host}:{port}"
    )

    server.serve_forever()


if __name__ == "__main__":
    start_server()
