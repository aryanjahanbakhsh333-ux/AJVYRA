"""
AJVYRA CINEMATIC FILM ENGINE
----------------------------
Film-level orchestration for 30-minute cinematic anime.

The film is the primary production object.
Internal render segments may exist, but they are implementation
details rather than the creative model.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from ajvyra_cinematic_ai_brain import (
    AJVYRACinematicAIBrain,
)


@dataclass
class FilmAct:
    number: int
    name: str
    start_seconds: float
    end_seconds: float
    purpose: str
    emotional_direction: str


@dataclass
class CinematicFilm:
    film_id: str
    title: str
    genre: str
    duration_seconds: int = 1800

    language_tracks: List[str] = field(
        default_factory=lambda: [
            "ja",
            "fa",
        ]
    )

    subtitle_tracks: List[str] = field(
        default_factory=lambda: [
            "ja",
            "fa",
            "en",
        ]
    )

    acts: List[FilmAct] = field(
        default_factory=list
    )

    creative_rules: Dict[str, Any] = field(
        default_factory=dict
    )

    production_state: Dict[str, Any] = field(
        default_factory=dict
    )


class AJVYRACinematicFilmEngine:
    VERSION = "1.0.0"

    def __init__(
        self,
        film: CinematicFilm,
        project_root: str | Path = (
            "generated/cinematic_films"
        ),
    ) -> None:
        self.film = film

        self.project_root = Path(project_root)
        self.project_dir = (
            self.project_root
            / self._safe_name(film.film_id)
        )

        self.project_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.brain = AJVYRACinematicAIBrain(
            film_id=film.film_id,
            title=film.title,
            genre=film.genre,
            duration_seconds=film.duration_seconds,
            memory_path=(
                self.project_dir
                / "cinematic_memory.json"
            ),
        )

        self._ensure_default_structure()

    @staticmethod
    def _safe_name(value: str) -> str:
        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789-_"
        )

        result = "".join(
            char if char in allowed else "_"
            for char in value
        )

        return result.strip("_") or "film"

    def _ensure_default_structure(self) -> None:
        if not self.film.acts:
            self.film.acts = [
                FilmAct(
                    number=1,
                    name="Beginning",
                    start_seconds=0,
                    end_seconds=self.film.duration_seconds * 0.25,
                    purpose="Introduce world, characters and central conflict.",
                    emotional_direction="curiosity → connection",
                ),
                FilmAct(
                    number=2,
                    name="Descent",
                    start_seconds=self.film.duration_seconds * 0.25,
                    end_seconds=self.film.duration_seconds * 0.70,
                    purpose="Escalate conflict and transform relationships.",
                    emotional_direction="connection → loss → tension",
                ),
                FilmAct(
                    number=3,
                    name="Resolution",
                    start_seconds=self.film.duration_seconds * 0.70,
                    end_seconds=self.film.duration_seconds,
                    purpose="Deliver climax, consequence and emotional resolution.",
                    emotional_direction="tension → truth → resolution",
                ),
            ]

        self.film.production_state.setdefault(
            "created_at",
            time.time(),
        )

        self.film.production_state.setdefault(
            "status",
            "development",
        )

        self.film.production_state.setdefault(
            "render_progress",
            0.0,
        )

    # ---------------------------------------------------------
    # Film lifecycle
    # ---------------------------------------------------------

    def prepare(self) -> Dict[str, Any]:
        self.film.production_state[
            "status"
        ] = "prepared"

        self._write_json(
            "film_manifest.json",
            asdict(self.film),
        )

        self.brain.save()

        return self.manifest()

    def start_production(self) -> None:
        if self.film.production_state.get(
            "status"
        ) not in {
            "prepared",
            "paused",
            "development",
        }:
            raise RuntimeError(
                "Film cannot enter production from "
                f"state={self.film.production_state.get('status')}"
            )

        self.film.production_state[
            "status"
        ] = "production"

        self.brain.set_flag(
            "story_locked",
            True,
        )

        self._persist()

    def pause(self) -> None:
        self.film.production_state[
            "status"
        ] = "paused"

        self._persist()

    def complete(self) -> None:
        if not self.brain.ready_for(
            "publish"
        ):
            raise RuntimeError(
                "Film is not ready for completion."
            )

        self.film.production_state[
            "status"
        ] = "completed"

        self.film.production_state[
            "render_progress"
        ] = 1.0

        self._persist()

    # ---------------------------------------------------------
    # Film time
    # ---------------------------------------------------------

    def seek(
        self,
        seconds: float,
    ) -> Dict[str, Any]:
        self.brain.seek(seconds)

        return self.timeline_state()

    def advance(
        self,
        seconds: float,
    ) -> Dict[str, Any]:
        self.brain.advance_time(seconds)

        return self.timeline_state()

    def timeline_state(self) -> Dict[str, Any]:
        current = self.brain.memory.current_time

        act = next(
            (
                act
                for act in self.film.acts
                if act.start_seconds
                <= current
                <= act.end_seconds
            ),
            self.film.acts[-1],
        )

        progress = (
            current / self.film.duration_seconds
        )

        return {
            "film_id": self.film.film_id,
            "time": round(current, 3),
            "duration": self.film.duration_seconds,
            "progress": round(progress, 5),
            "act": asdict(act),
        }

    # ---------------------------------------------------------
    # Creative state
    # ---------------------------------------------------------

    def set_creative_rule(
        self,
        name: str,
        value: Any,
    ) -> None:
        self.film.creative_rules[name] = value
        self._persist()

    def lock_stage(
        self,
        stage: str,
    ) -> None:
        mapping = {
            "story": "story_locked",
            "characters": "characters_locked",
            "world": "world_locked",
            "director": "director_locked",
        }

        if stage not in mapping:
            raise ValueError(
                f"Unknown stage: {stage}"
            )

        self.brain.set_flag(
            mapping[stage],
            True,
        )

        self._persist()

    def update_render_progress(
        self,
        progress: float,
    ) -> None:
        self.film.production_state[
            "render_progress"
        ] = max(
            0.0,
            min(1.0, float(progress)),
        )

        self._persist()

    # ---------------------------------------------------------
    # Manifest
    # ---------------------------------------------------------

    def manifest(self) -> Dict[str, Any]:
        return {
            "engine": (
                "AJVYRA Cinematic Film Engine"
            ),
            "version": self.VERSION,
            "film": asdict(self.film),
            "brain": self.brain.snapshot(),
            "timeline": self.timeline_state(),
            "ready": {
                "visual": self.brain.ready_for(
                    "visual"
                ),
                "audio": self.brain.ready_for(
                    "audio"
                ),
                "render": self.brain.ready_for(
                    "render"
                ),
                "publish": self.brain.ready_for(
                    "publish"
                ),
            },
        }

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def _persist(self) -> None:
        self._write_json(
            "film_manifest.json",
            asdict(self.film),
        )
        self.brain.save()

    def _write_json(
        self,
        filename: str,
        data: Dict[str, Any],
    ) -> None:
        path = self.project_dir / filename

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    film = CinematicFilm(
        film_id="veyllora_cinematic_01",
        title="Veylora",
        genre="dark_fantasy",
        duration_seconds=1800,
    )

    engine = AJVYRACinematicFilmEngine(
        film
    )

    engine.prepare()
    engine.start_production()

    engine.set_creative_rule(
        "visual_style",
        "cinematic_dark_anime",
    )

    engine.set_creative_rule(
        "continuity_priority",
        "strict",
    )

    engine.lock_stage("characters")
    engine.lock_stage("world")
    engine.lock_stage("director")

    print(
        json.dumps(
            engine.manifest(),
            ensure_ascii=False,
            indent=2,
        )
    )
