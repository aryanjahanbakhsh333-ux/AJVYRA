from __future__ import annotations

from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
import os


class AJVYRAWebHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript",
        ".json": "application/json",
        ".css": "text/css",
        ".html": "text/html",
    }


def run_server(
    host: str = "127.0.0.1",
    port: int = 8000,
) -> None:
    directory = os.path.dirname(
        os.path.abspath(__file__)
    )

    os.chdir(directory)

    server = ThreadingTCPServer(
        (host, port),
        AJVYRAWebHandler,
    )

    print(f"AJVYRA browser server: http://{host}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()
