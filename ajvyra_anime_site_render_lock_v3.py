from __future__ import annotations

import json
from pathlib import Path

from ajvyra_anime_pre_render_gate_v3 import (
    AJVYRAAnimePreRenderGateV3,
)


class AJVYRAAnimeSiteRenderLockV3:

    def __init__(
        self,
        release_manifest: str,
        lock_file: str = "release/anime-render-approved.json",
    ):
        self.release_manifest = Path(
            release_manifest
        )
        self.lock_file = Path(lock_file)

    def approve(self) -> dict:

        gate = AJVYRAAnimePreRenderGateV3(
            str(self.release_manifest)
        )

        result = gate.verify()

        self.lock_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = {
            "project": "AJVYRA",
            "anime_release": "APPROVED",
            "film_count": result["films"],
            "site_render": "ALLOWED",
        }

        self.lock_file.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return payload

    def is_approved(self) -> bool:
        if not self.lock_file.exists():
            return False

        try:
            data = json.loads(
                self.lock_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return False

        return (
            data.get("project") == "AJVYRA"
            and data.get("anime_release") == "APPROVED"
            and data.get("film_count") == 30
            and data.get("site_render") == "ALLOWED"
        )
