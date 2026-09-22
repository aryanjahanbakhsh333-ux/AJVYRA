from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import json


class AJVYRAWebGameBootstrap:
    """
    Creates the browser-side bootstrap contract for an AJVYRA game.

    It does not pretend to generate gameplay.
    It prepares the files that the real browser runtime loads.
    """

    def __init__(
        self,
        game_id: str,
        output_root: str | Path = "public/games",
    ):
        if not game_id.strip():
            raise ValueError("game_id cannot be empty")

        self.game_id = game_id
        self.output_root = Path(output_root)

    @property
    def root(self) -> Path:
        return self.output_root / self.game_id

    def prepare(self) -> Path:
        self.root.mkdir(parents=True, exist_ok=True)
        return self.root

    def create_runtime_manifest(
        self,
        entry_script: str,
        title: str,
        genre: str,
    ) -> Path:
        if not entry_script.strip():
            raise ValueError("entry_script cannot be empty")

        payload: Dict[str, Any] = {
            "game_id": self.game_id,
            "title": title,
            "genre": genre,
            "runtime": {
                "loop": "/engine/ajvyra_web_game_loop.js",
                "input": "/engine/ajvyra_web_game_runtime.js",
            },
            "entry": entry_script,
            "status": "development",
            "playable": False,
            "release_verified": False,
        }

        target = self.prepare() / "runtime.manifest.json"

        target.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target

    def create_boot_script(self) -> Path:
        script = f"""(() => {{
    "use strict";

    const GAME_ID = {json.dumps(self.game_id)};

    window.AJVYRA_GAME_BOOT = {{
        gameId: GAME_ID,

        start() {{
            window.dispatchEvent(
                new CustomEvent(
                    "ajvyra-game-ready",
                    {{
                        detail: {{
                            gameId: GAME_ID
                        }}
                    }}
                )
            );
        }}
    }};

    window.AJVYRA_GAME_BOOT.start();
}})();
"""

        target = self.prepare() / "boot.js"
        target.write_text(script, encoding="utf-8")

        return target


if __name__ == "__main__":
    bootstrap = AJVYRAWebGameBootstrap(
        game_id="ajv_demo_001"
    )

    bootstrap.create_runtime_manifest(
        entry_script="game.js",
        title="AJVYRA Demo",
        genre="action",
    )

    bootstrap.create_boot_script()

    print("AJVYRA browser game bootstrap created.")
