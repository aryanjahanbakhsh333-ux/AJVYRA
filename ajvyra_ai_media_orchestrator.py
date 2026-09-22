from dataclasses import dataclass, field
from typing import Any


@dataclass
class MediaJob:
    job_id: str
    anime_id: int
    scene_id: str
    tasks: list[str] = field(default_factory=list)
    results: dict[str, Any] = field(default_factory=dict)


class MediaOrchestrator:

    def __init__(
        self,
        production_brain,
    ):
        self.brain = production_brain

    def create_job(
        self,
        job_id: str,
        anime_id: int,
        scene: dict,
    ) -> MediaJob:

        decision = self.brain.analyze_scene(
            anime_id=anime_id,
            scene=scene,
        )

        tasks = [
            "prepare_voice",
            "generate_persian_audio",
            "generate_japanese_audio",
            "prepare_english_subtitle",
            "prepare_persian_subtitle",
            "prepare_japanese_subtitle",
            "validate_output",
        ]

        return MediaJob(
            job_id=job_id,
            anime_id=anime_id,
            scene_id=decision.scene_id,
            tasks=tasks,
        )

    def execute_plan(
        self,
        job: MediaJob,
        handlers: dict[str, Any],
    ) -> MediaJob:

        for task in job.tasks:

            handler = handlers.get(task)

            if handler is None:
                job.results[task] = {
                    "status": "waiting",
                    "reason": "handler_not_ready",
                }
                continue

            try:
                result = handler(job)
                job.results[task] = {
                    "status": "completed",
                    "result": result,
                }

            except Exception as exc:
                job.results[task] = {
                    "status": "failed",
                    "error": str(exc),
                }

        return job
