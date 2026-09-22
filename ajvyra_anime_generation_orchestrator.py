from __future__ import annotations

import importlib
import json
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Callable

from ajvyra_anime_production_manifest import (
    ManifestRegistry,
    ProductionManifest,
)


@dataclass
class GenerationStep:
    name: str
    order: int
    status: str = "pending"
    started_at: str | None = None
    finished_at: str | None = None
    error: str | None = None
    output: dict[str, Any] | None = None


class AnimeGenerationOrchestrator:
    """
    Central production commander.

    It does not replace the existing engines.
    It commands them in a deterministic production order.
    """

    STEP_NAMES = [
        "story",
        "characters",
        "locations",
        "scenes",
        "dialogue",
        "voices",
        "visuals",
        "animation",
        "video",
        "subtitles",
        "publish",
    ]

    MANIFEST_FIELDS = {
        "story": "story_ready",
        "characters": "characters_ready",
        "locations": "locations_ready",
        "scenes": "scenes_ready",
        "dialogue": "dialogue_ready",
        "voices": "voices_ready",
        "visuals": "visuals_ready",
        "animation": "animation_ready",
        "video": "video_ready",
        "subtitles": "subtitles_ready",
        "publish": "published",
    }

    def __init__(
        self,
        root: str | Path = "ajvyra_projects/orchestrator",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.registry = ManifestRegistry()

    def _now(self) -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    def _state_path(
        self,
        anime_id: int,
    ) -> Path:
        return (
            self.root
            / f"anime_{anime_id:02d}_state.json"
        )

    def create_state(
        self,
        anime_id: int,
        title: str,
    ) -> dict[str, Any]:
        steps = [
            GenerationStep(
                name=name,
                order=index + 1,
            )
            for index, name in enumerate(
                self.STEP_NAMES
            )
        ]

        state = {
            "anime_id": anime_id,
            "title": title,
            "status": "queued",
            "created_at": self._now(),
            "updated_at": self._now(),
            "steps": [
                asdict(step)
                for step in steps
            ],
        }

        with self._state_path(
            anime_id
        ).open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return state

    def load_state(
        self,
        anime_id: int,
    ) -> dict[str, Any]:
        path = self._state_path(anime_id)

        if not path.exists():
            raise FileNotFoundError(
                f"Production state not found: {anime_id}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)

    def _save_state(
        self,
        state: dict[str, Any],
    ):
        state["updated_at"] = self._now()

        with self._state_path(
            state["anime_id"]
        ).open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=2,
            )

    def _find_step(
        self,
        state: dict[str, Any],
        name: str,
    ) -> dict[str, Any]:
        for step in state["steps"]:
            if step["name"] == name:
                return step

        raise ValueError(
            f"Unknown generation step: {name}"
        )

    def register_anime(
        self,
        anime_id: int,
        title: str,
        duration_seconds: int = 1800,
        fps: int = 24,
    ):
        self.registry.create(
            anime_id=anime_id,
            title=title,
            duration_seconds=duration_seconds,
            fps=fps,
        )

        return self.create_state(
            anime_id,
            title,
        )

    def run_step(
        self,
        anime_id: int,
        step_name: str,
        worker: Callable[
            [ProductionManifest],
            dict[str, Any] | None
        ],
    ) -> dict[str, Any]:
        state = self.load_state(anime_id)

        manifest = self.registry.load(anime_id)

        step = self._find_step(
            state,
            step_name,
        )

        step["status"] = "running"
        step["started_at"] = self._now()
        step["error"] = None

        state["status"] = "running"

        self._save_state(state)

        try:
            result = worker(manifest)

            field = self.MANIFEST_FIELDS.get(
                step_name
            )

            if field:
                setattr(
                    manifest,
                    field,
                    True,
                )

            manifest.status = (
                "publishing"
                if step_name == "publish"
                else "generating"
            )

            self.registry.update(manifest)

            step["status"] = "completed"
            step["finished_at"] = self._now()
            step["output"] = result or {}

            state["status"] = "running"

            self._save_state(state)

            return {
                "ok": True,
                "step": step_name,
                "result": result or {},
            }

        except Exception as error:
            step["status"] = "failed"
            step["finished_at"] = self._now()
            step["error"] = (
                f"{type(error).__name__}: {error}"
            )

            state["status"] = "failed"

            self._save_state(state)

            return {
                "ok": False,
                "step": step_name,
                "error": str(error),
                "traceback": traceback.format_exc(),
            }

    def next_step(
        self,
        anime_id: int,
    ) -> str | None:
        state = self.load_state(anime_id)

        for step in sorted(
            state["steps"],
            key=lambda item: item["order"],
        ):
            if step["status"] in {
                "pending",
                "failed",
            }:
                return step["name"]

        return None

    def status(
        self,
        anime_id: int,
    ) -> dict[str, Any]:
        state = self.load_state(anime_id)
        manifest = self.registry.load(anime_id)

        completed = sum(
            1
            for step in state["steps"]
            if step["status"] == "completed"
        )

        total = len(state["steps"])

        return {
            "anime_id": anime_id,
            "title": state["title"],
            "status": state["status"],
            "progress": (
                completed / total
                if total
                else 0
            ),
            "completed_steps": completed,
            "total_steps": total,
            "ready_for_publish": (
                manifest.ready_for_publish()
            ),
            "steps": state["steps"],
        }

    def import_worker(
        self,
        module_name: str,
        function_name: str,
    ):
        module = importlib.import_module(
            module_name
        )

        worker = getattr(
            module,
            function_name,
        )

        if not callable(worker):
            raise TypeError(
                f"{module_name}.{function_name} "
                "is not callable"
            )

        return worker
