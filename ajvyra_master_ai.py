"""
AJVYRA MASTER AI
Central command brain for anime + game production.

New file.
Does not replace existing AJVYRA engines.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ajvyra_ai_command_router import AICommandRouter, RoutedCommand
from ajvyra_ai_content_director import AJVYRAContentDirector
from ajvyra_ai_poster_creator import AJVYRAPosterCreator
from ajvyra_ai_universal_builder import AJVYRAUniversalBuilder


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | AJVYRA-MASTER | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger("ajvyra.master")


@dataclass
class MasterState:
    started_at: float = field(default_factory=time.time)
    last_command: str = ""
    last_operation: str = ""
    completed_operations: int = 0
    failed_operations: int = 0
    running: bool = False
    anime_total: int = 30
    game_total: int = 70

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AJVYRAMasterAI:
    """
    Single entry point for the whole AJVYRA production system.

    Supported operations:

        build_all
        build_anime
        build_games
        posters
        publish
        sync_site
        status
        search
        inspect
    """

    def __init__(
        self,
        root: Optional[Path | str] = None,
        public_base_url: Optional[str] = None,
    ) -> None:

        self.root = Path(root or os.getenv("AJVYRA_ROOT", ".")).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

        self.public_base_url = (
            public_base_url
            or os.getenv("AJVYRA_PUBLIC_BASE_URL", "")
        ).rstrip("/")

        self.state_file = self.root / "runtime" / "master_ai_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()

        self.router = AICommandRouter()
        self.director = AJVYRAContentDirector(self.root)
        self.poster_creator = AJVYRAPosterCreator(
            root=self.root,
            director=self.director,
        )
        self.builder = AJVYRAUniversalBuilder(
            root=self.root,
            director=self.director,
            poster_creator=self.poster_creator,
            public_base_url=self.public_base_url,
        )

    # ---------------------------------------------------------
    # STATE
    # ---------------------------------------------------------

    def _load_state(self) -> MasterState:
        if not self.state_file.exists():
            return MasterState()

        try:
            data = json.loads(self.state_file.read_text(encoding="utf-8"))
            state = MasterState()

            for key, value in data.items():
                if hasattr(state, key):
                    setattr(state, key, value)

            return state

        except Exception:
            LOGGER.exception("Could not load master state.")
            return MasterState()

    def _save_state(self) -> None:
        self.state_file.write_text(
            json.dumps(
                self.state.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # COMMAND EXECUTION
    # ---------------------------------------------------------

    def execute(self, command: str, **kwargs: Any) -> Dict[str, Any]:
        self.state.last_command = command
        self.state.running = True
        self._save_state()

        try:
            routed = self.router.route(command, **kwargs)

            LOGGER.info(
                "Command: %s -> operation=%s",
                command,
                routed.operation,
            )

            result = self._execute_routed(routed)

            self.state.last_operation = routed.operation
            self.state.completed_operations += 1

            return {
                "ok": True,
                "command": command,
                "operation": routed.operation,
                "result": result,
            }

        except Exception as exc:
            self.state.failed_operations += 1

            LOGGER.exception("Master AI command failed.")

            return {
                "ok": False,
                "command": command,
                "error": str(exc),
                "type": type(exc).__name__,
            }

        finally:
            self.state.running = False
            self._save_state()

    def _execute_routed(
        self,
        command: RoutedCommand,
    ) -> Dict[str, Any]:

        operation = command.operation
        args = command.arguments

        if operation == "build_all":
            return self.builder.build_all(
                resume=args.get("resume", True),
            )

        if operation == "build_anime":
            return self.builder.build_all_anime(
                resume=args.get("resume", True),
            )

        if operation == "build_games":
            return self.builder.build_all_games(
                resume=args.get("resume", True),
            )

        if operation == "posters":
            return self.builder.generate_all_posters(
                resume=args.get("resume", True),
            )

        if operation == "publish":
            return self.builder.publish_everything()

        if operation == "sync_site":
            return self.builder.sync_site()

        if operation == "status":
            return self.builder.status()

        if operation == "search":
            return self.builder.search(
                args.get("query", ""),
            )

        if operation == "inspect":
            return self.builder.inspect_project()

        raise ValueError(f"Unsupported operation: {operation}")

    # ---------------------------------------------------------
    # DIRECT API
    # ---------------------------------------------------------

    def build_all(self) -> Dict[str, Any]:
        return self.execute("build_all")

    def build_anime(self) -> Dict[str, Any]:
        return self.execute("build_anime")

    def build_games(self) -> Dict[str, Any]:
        return self.execute("build_games")

    def generate_posters(self) -> Dict[str, Any]:
        return self.execute("posters")

    def publish(self) -> Dict[str, Any]:
        return self.execute("publish")

    def sync_site(self) -> Dict[str, Any]:
        return self.execute("sync_site")

    def status(self) -> Dict[str, Any]:
        return self.execute("status")

    def search(self, query: str) -> Dict[str, Any]:
        return self.execute(
            "search",
            query=query,
        )


def main() -> int:
    master = AJVYRAMasterAI()

    if len(sys.argv) <= 1:
        print(
            json.dumps(
                master.status(),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    command = " ".join(sys.argv[1:]).strip()

    result = master.execute(command)

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )

    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
