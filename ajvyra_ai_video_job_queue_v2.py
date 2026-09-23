from __future__ import annotations

import secrets
import threading
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass
class AJVYRAAIJob:
    job_id: str
    prompt: str
    status: str
    created_at: str
    updated_at: str
    video_url: str | None = None
    local_video: str | None = None
    error: str | None = None
    source: str = "AJVYRA AI Video Studio"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AJVYRAAIVideoJobQueue:
    """
    Small in-process queue for a ZeroGPU Gradio Space.

    Jobs are intentionally serialized because GPU quota is limited.
    """

    def __init__(
        self,
        max_pending_jobs: int = 16,
        max_jobs_per_session: int = 3,
    ):
        self.max_pending_jobs = max_pending_jobs
        self.max_jobs_per_session = max_jobs_per_session

        self._jobs: dict[str, AJVYRAAIJob] = {}
        self._session_jobs: dict[str, list[str]] = {}

        self._lock = threading.RLock()

    @staticmethod
    def _now() -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    def create(
        self,
        prompt: str,
        session_id: str,
    ) -> AJVYRAAIJob:

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt is empty.")

        with self._lock:

            pending = sum(
                1
                for job in self._jobs.values()
                if job.status in {
                    "queued",
                    "generating",
                    "uploading",
                }
            )

            if pending >= self.max_pending_jobs:
                raise RuntimeError(
                    "AJVYRA AI queue is currently full."
                )

            previous = self._session_jobs.get(
                session_id,
                [],
            )

            recent_pending = sum(
                1
                for job_id in previous
                if self._jobs.get(job_id)
                and self._jobs[job_id].status
                in {
                    "queued",
                    "generating",
                    "uploading",
                }
            )

            if recent_pending >= self.max_jobs_per_session:
                raise RuntimeError(
                    "Too many pending jobs for this session."
                )

            job_id = (
                "ajv-job-"
                + secrets.token_hex(8)
            )

            now = self._now()

            job = AJVYRAAIJob(
                job_id=job_id,
                prompt=prompt,
                status="queued",
                created_at=now,
                updated_at=now,
            )

            self._jobs[job_id] = job

            self._session_jobs.setdefault(
                session_id,
                [],
            ).append(job_id)

            return job

    def update(
        self,
        job_id: str,
        status: str,
        **fields: Any,
    ) -> AJVYRAAIJob:

        with self._lock:

            if job_id not in self._jobs:
                raise KeyError(
                    f"Unknown job: {job_id}"
                )

            job = self._jobs[job_id]

            allowed = {
                "queued",
                "generating",
                "uploading",
                "ready",
                "failed",
            }

            if status not in allowed:
                raise ValueError(
                    f"Invalid job status: {status}"
                )

            job.status = status
            job.updated_at = self._now()

            for key, value in fields.items():
                if hasattr(job, key):
                    setattr(job, key, value)

            return job

    def get(
        self,
        job_id: str,
    ) -> AJVYRAAIJob | None:

        with self._lock:
            return self._jobs.get(job_id)

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [
                job.to_dict()
                for job in self._jobs.values()
            ]

    def run_job(
        self,
        job_id: str,
        generator: Callable[[str], str],
        publisher: Callable[[str, str], dict[str, Any]],
    ) -> AJVYRAAIJob:

        job = self.get(job_id)

        if job is None:
            raise KeyError(job_id)

        try:

            self.update(
                job_id,
                "generating",
            )

            local_video = generator(
                job.prompt
            )

            self.update(
                job_id,
                "uploading",
                local_video=local_video,
            )

            published = publisher(
                local_video,
                job_id,
            )

            return self.update(
                job_id,
                "ready",
                video_url=published[
                    "video_url"
                ],
            )

        except Exception as exc:

            return self.update(
                job_id,
                "failed",
                error=str(exc),
            )

    def wait(
        self,
        job_id: str,
        timeout: float = 240.0,
        interval: float = 1.0,
    ) -> AJVYRAAIJob:

        started = time.monotonic()

        while True:

            job = self.get(job_id)

            if job is None:
                raise KeyError(job_id)

            if job.status in {
                "ready",
                "failed",
            }:
                return job

            if (
                time.monotonic()
                - started
                >= timeout
            ):
                raise TimeoutError(
                    "AI video job timed out."
                )

            time.sleep(interval)
