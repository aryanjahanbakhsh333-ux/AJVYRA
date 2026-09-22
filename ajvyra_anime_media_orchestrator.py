from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ProductionJob:
    anime_id: str
    episode_id: str
    genre: str
    target_duration_seconds: int = 1800
    status: str = "created"
    completed_shots: int = 0
    total_shots: int = 0
    failed_shots: int = 0
    output_video: Optional[str] = None


class AJVYRAMediaOrchestrator:
    """
    Master coordinator for real AJVYRA anime media production.

    Responsibilities:
    - create production workspace
    - generate/load shot plan
    - generate keyframes
    - generate videos
    - generate audio
    - render subtitles
    - assemble final episode
    - run validation
    """

    def __init__(
        self,
        root: str = "generated/anime_production",
        shot_engine=None,
        keyframe_engine=None,
        audio_engine=None,
        render_engine=None,
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.shot_engine = shot_engine
        self.keyframe_engine = keyframe_engine
        self.audio_engine = audio_engine
        self.render_engine = render_engine

    def workspace(self, anime_id: str, episode_id: str) -> Path:
        path = self.root / anime_id / "season_01" / episode_id
        path.mkdir(parents=True, exist_ok=True)

        for folder in (
            "media",
            "keyframes",
            "audio",
            "subtitles",
            "renders",
            "logs",
        ):
            (path / folder).mkdir(exist_ok=True)

        return path

    def create_job(
        self,
        anime_id: str,
        episode_id: str,
        genre: str,
        total_shots: int,
    ) -> ProductionJob:
        job = ProductionJob(
            anime_id=anime_id,
            episode_id=episode_id,
            genre=genre,
            total_shots=total_shots,
        )

        ws = self.workspace(anime_id, episode_id)
        self._write_json(ws / "production_job.json", asdict(job))

        return job

    def update_job(self, job: ProductionJob):
        ws = self.workspace(job.anime_id, job.episode_id)
        self._write_json(ws / "production_job.json", asdict(job))

    def run(
        self,
        anime_id: str,
        episode_id: str,
        genre: str,
        shot_plan: Dict[str, Any],
        *,
        generate_video: bool = True,
        generate_audio: bool = True,
        render: bool = True,
    ) -> Dict[str, Any]:

        shots = shot_plan.get("shots", [])

        job = self.create_job(
            anime_id=anime_id,
            episode_id=episode_id,
            genre=genre,
            total_shots=len(shots),
        )

        ws = self.workspace(anime_id, episode_id)

        self._write_json(ws / "shot_plan.json", shot_plan)

        job.status = "keyframe_generation"
        self.update_job(job)

        if self.keyframe_engine:
            self.keyframe_engine.generate_episode_keyframes(
                anime_id=anime_id,
                episode_id=episode_id,
                shot_plan=shot_plan,
            )

        if generate_video and self.shot_engine:
            job.status = "video_generation"
            self.update_job(job)

            for index, shot in enumerate(shots, start=1):
                try:
                    self.shot_engine.generate_shot(
                        anime_id=anime_id,
                        episode_id=episode_id,
                        shot=shot,
                    )

                    job.completed_shots = index
                    self.update_job(job)

                except Exception as exc:
                    job.failed_shots += 1

                    self._write_json(
                        ws / "logs" / f"shot_{index:04d}_error.json",
                        {
                            "shot": shot,
                            "error": str(exc),
                        },
                    )

                    self.update_job(job)

        if generate_audio and self.audio_engine:
            job.status = "audio_generation"
            self.update_job(job)

            self.audio_engine.generate_episode_audio(
                anime_id=anime_id,
                episode_id=episode_id,
                shot_plan=shot_plan,
            )

        if render and self.render_engine:
            job.status = "rendering"
            self.update_job(job)

            output = self.render_engine.render_episode(
                anime_id=anime_id,
                episode_id=episode_id,
                shot_plan=shot_plan,
            )

            job.output_video = str(output)

        job.status = "completed" if job.failed_shots == 0 else "completed_with_errors"
        self.update_job(job)

        return asdict(job)

    @staticmethod
    def _write_json(path: Path, data: Dict[str, Any]):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
