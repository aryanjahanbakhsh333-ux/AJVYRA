from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from typing import Any, Dict

from ajvyra_anime_site_runtime import RUNTIME
from ajvyra_anime_watch_runtime import WATCH_RUNTIME
from ajvyra_anime_episode_runtime import EPISODES


HOST = "127.0.0.1"
PORT = 8790


class AnimeSiteGateway(BaseHTTPRequestHandler):
    """
    HTTP gateway dedicated to the AJVYRA Anime section.

    Endpoints:

        /api/anime
        /api/anime/<id>
        /api/anime/<id>/player
        /api/anime/<id>/watch
        /api/anime/<id>/assets
        /api/search?q=...
    """

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._headers()
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        query = parse_qs(parsed.query)

        if path == "/api/anime":
            self._json(
                RUNTIME.payload()
            )
            return

        if path == "/api/search":
            value = query.get(
                "q",
                [""],
            )[0]

            results = [
                item.__dict__
                for item in RUNTIME.search(value)
            ]

            self._json(
                {
                    "query": value,
                    "count": len(results),
                    "items": results,
                }
            )
            return

        parts = [
            part
            for part in path.split("/")
            if part
        ]

        if (
            len(parts) >= 3
            and parts[0] == "api"
            and parts[1] == "anime"
        ):
            try:
                anime_id = int(parts[2])
            except ValueError:
                self._error(
                    400,
                    "Invalid anime id.",
                )
                return

            item = RUNTIME.get(anime_id)

            if item is None:
                self._error(
                    404,
                    "Anime not found.",
                )
                return

            if len(parts) == 3:
                self._json(
                    {
                        "anime": item.__dict__,
                    }
                )
                return

            action = parts[3]

            if action == "player":
                self._json(
                    EPISODES.player_payload(
                        anime_id,
                        item.title,
                    )
                )
                return

            if action == "watch":
                self._json(
                    WATCH_RUNTIME.payload(
                        anime_id
                    )
                )
                return

            if action == "assets":
                episode = EPISODES.build(
                    anime_id,
                    item.title,
                )

                self._json(
                    {
                        "anime_id": anime_id,
                        "ready": EPISODES.ready(
                            episode
                        ),
                        "assets": (
                            EPISODES.asset_status(
                                episode
                            )
                        ),
                    }
                )
                return

        self._error(
            404,
            "Anime API route not found.",
        )

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        parts = [
            part
            for part in path.split("/")
            if part
        ]

        if (
            len(parts) == 4
            and parts[0] == "api"
            and parts[1] == "anime"
            and parts[3] == "watch"
        ):
            try:
                anime_id = int(parts[2])
            except ValueError:
                self._error(
                    400,
                    "Invalid anime id.",
                )
                return

            try:
                body = self._read_json()

                state = WATCH_RUNTIME.save(
                    anime_id=anime_id,
                    position_seconds=float(
                        body.get(
                            "position_seconds",
                            0,
                        )
                    ),
                    selected_audio=str(
                        body.get(
                            "audio",
                            "fa",
                        )
                    ),
                    selected_subtitle=str(
                        body.get(
                            "subtitle",
                            "fa",
                        )
                    ),
                    duration_seconds=float(
                        body.get(
                            "duration_seconds",
                            1800,
                        )
                    ),
                )

                self._json(
                    {
                        "success": True,
                        "state": state.__dict__,
                    }
                )

            except Exception as exc:
                self._error(
                    400,
                    str(exc),
                )

            return

        self._error(
            404,
            "Anime POST route not found.",
        )

    def _read_json(self) -> Dict[str, Any]:
        length = int(
            self.headers.get(
                "Content-Length",
                "0",
            )
        )

        if length <= 0:
            return {}

        raw = self.rfile.read(length)

        return json.loads(
            raw.decode("utf-8")
        )

    def _json(
        self,
        payload: Dict[str, Any],
        status: int = 200,
    ) -> None:

        raw = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(status)
        self._headers()
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(raw)),
        )
        self.end_headers()

        self.wfile.write(raw)

    def _error(
        self,
        status: int,
        message: str,
    ) -> None:

        self._json(
            {
                "success": False,
                "error": message,
            },
            status=status,
        )

    def _headers(self) -> None:
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS",
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )

    def log_message(
        self,
        format: str,
        *args: Any,
    ) -> None:
        return


def start(
    host: str = HOST,
    port: int = PORT,
) -> None:

    server = ThreadingHTTPServer(
        (host, port),
        AnimeSiteGateway,
    )

    print(
        f"AJVYRA Anime Gateway: "
        f"http://{host}:{port}"
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    start()
