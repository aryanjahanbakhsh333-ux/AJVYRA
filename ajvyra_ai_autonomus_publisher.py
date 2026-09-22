"""
AJVYRA AI AUTONOMOUS PUBLISHER

Publishes only projects that pass the completion gate.

It also creates:
    sitemap.xml
    robots.txt
    search-index.json
    site-manifest.json

No per-anime manual upload step is required by this publisher.

For real deployment, the hosting/repository must already be configured.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List

from ajvyra_ai_completion_gate import (
    AJVYRACompletionGate,
)


class AJVYRAAutonomousPublisher:

    def __init__(
        self,
        root: Path | str,
        public_base_url: str = "",
    ) -> None:

        self.root = Path(root).resolve()

        self.public_base_url = (
            public_base_url
            or os.getenv(
                "AJVYRA_PUBLIC_BASE_URL",
                "",
            )
        ).rstrip("/")

        self.site_root = (
            self.root
            / "generated"
            / "site"
        )

        self.site_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.gate = (
            AJVYRACompletionGate(
                self.root
            )
        )

    # =========================================================
    # PUBLISH
    # =========================================================

    def publish_ready_content(
        self,
    ) -> Dict[str, Any]:

        validation = (
            self.gate.validate_everything()
        )

        published_anime = [
            item
            for item in validation["anime"]
            if item["complete"]
        ]

        published_games = [
            item
            for item in validation["games"]
            if item["complete"]
        ]

        self._build_search_index(
            published_anime,
            published_games,
        )

        self._build_sitemap(
            published_anime,
            published_games,
        )

        self._build_manifest(
            published_anime,
            published_games,
        )

        deployment = self._deploy()

        return {
            "anime_ready": len(
                published_anime
            ),
            "games_ready": len(
                published_games
            ),
            "deployment": deployment,
            "validation": validation,
        }

    # =========================================================
    # SEARCH
    # =========================================================

    def _build_search_index(
        self,
        anime: List[Dict[str, Any]],
        games: List[Dict[str, Any]],
    ) -> None:

        entries = []

        for item in anime:

            anime_id = item["project_id"].split(
                "-"
            )[-1]

            entries.append(
                {
                    "type": "anime",
                    "id": int(anime_id),
                    "title": (
                        f"AJVYRA Anime {anime_id}"
                    ),
                    "url": self._url(
                        f"/anime/{anime_id}/"
                    ),
                    "status": "ready",
                }
            )

        for item in games:

            game_id = item["project_id"].split(
                "-"
            )[-1]

            entries.append(
                {
                    "type": "game",
                    "id": int(game_id),
                    "title": (
                        f"AJVYRA Game {game_id}"
                    ),
                    "url": self._url(
                        f"/games/{game_id}/"
                    ),
                    "status": "ready",
                }
            )

        self._write_json(
            self.site_root
            / "search-index.json",
            {
                "generated_at": time.time(),
                "items": entries,
            },
        )

    # =========================================================
    # SITEMAP
    # =========================================================

    def _build_sitemap(
        self,
        anime: List[Dict[str, Any]],
        games: List[Dict[str, Any]],
    ) -> None:

        urls = []

        for item in anime:
            anime_id = item[
                "project_id"
            ].split("-")[-1]

            urls.append(
                self._url(
                    f"/anime/{anime_id}/"
                )
            )

        for item in games:
            game_id = item[
                "project_id"
            ].split("-")[-1]

            urls.append(
                self._url(
                    f"/games/{game_id}/"
                )
            )

        xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            (
                '<urlset xmlns='
                '"http://www.sitemaps.org/schemas/'
                'sitemap/0.9">'
            ),
        ]

        for url in urls:

            if not url:
                continue

            xml.append(
                "<url>"
                f"<loc>{self._escape(url)}</loc>"
                "<changefreq>weekly</changefreq>"
                "<priority>0.8</priority>"
                "</url>"
            )

        xml.append(
            "</urlset>"
        )

        (
            self.site_root
            / "sitemap.xml"
        ).write_text(
            "\n".join(xml),
            encoding="utf-8",
        )

        robots = (
            "User-agent: *\n"
            "Allow: /\n\n"
        )

        sitemap_url = self._url(
            "/sitemap.xml"
        )

        if sitemap_url:
            robots += (
                f"Sitemap: {sitemap_url}\n"
            )

        (
            self.site_root
            / "robots.txt"
        ).write_text(
            robots,
            encoding="utf-8",
        )

    # =========================================================
    # MANIFEST
    # =========================================================

    def _build_manifest(
        self,
        anime: List[Dict[str, Any]],
        games: List[Dict[str, Any]],
    ) -> None:

        manifest = {
            "site": "AJVYRA",
            "generated_at": time.time(),
            "ready_anime": len(anime),
            "ready_games": len(games),
            "search_index": "/search-index.json",
            "sitemap": "/sitemap.xml",
            "robots": "/robots.txt",
        }

        self._write_json(
            self.site_root
            / "site-manifest.json",
            manifest,
        )

    # =========================================================
    # DEPLOY
    # =========================================================

    def _deploy(self) -> Dict[str, Any]:

        enabled = (
            os.getenv(
                "AJVYRA_AUTO_DEPLOY",
                "0",
            ).lower()
            in {
                "1",
                "true",
                "yes",
                "on",
            }
        )

        if not enabled:
            return {
                "status": "prepared",
                "reason": (
                    "AJVYRA_AUTO_DEPLOY is disabled."
                ),
                "site_root": str(
                    self.site_root
                ),
            }

        repository = Path(
            os.getenv(
                "AJVYRA_DEPLOY_REPO",
                str(self.root),
            )
        ).resolve()

        if not (
            repository / ".git"
        ).exists():

            return {
                "status": "blocked",
                "reason": (
                    "Deployment repository was not found."
                ),
            }

        commands = [
            [
                "git",
                "-C",
                str(repository),
                "add",
                ".",
            ],
            [
                "git",
                "-C",
                str(repository),
                "commit",
                "-m",
                "AJVYRA autonomous AI production",
            ],
            [
                "git",
                "-C",
                str(repository),
                "push",
            ],
        ]

        results = []

        for command in commands:

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            results.append(
                {
                    "command": command,
                    "returncode": process.returncode,
                    "stdout": process.stdout[-2000:],
                    "stderr": process.stderr[-2000:],
                }
            )

            combined = (
                process.stdout
                + process.stderr
            ).lower()

            if (
                process.returncode != 0
                and "nothing to commit" not in combined
            ):

                return {
                    "status": "failed",
                    "steps": results,
                }

        return {
            "status": "deployed",
            "steps": results,
        }

    # =========================================================
    # HELPERS
    # =========================================================

    def _url(
        self,
        path: str,
    ) -> str:

        if not self.public_base_url:
            return path

        if not path.startswith("/"):
            path = "/" + path

        return (
            self.public_base_url
            + path
        )

    @staticmethod
    def _escape(
        value: str,
    ) -> str:

        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )

    @staticmethod
    def _write_json(
        path: Path,
        data: Any,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
