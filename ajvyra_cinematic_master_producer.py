from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from ajvyra_cinematic_media_backend import (
    AJVYRACinematicMediaBackend,
    MediaGenerationRequest,
)
from ajvyra_cinematic_production_scheduler import (
    AJVYRACinematicProductionScheduler,
    ProductionTask,
)


@dataclass
class FilmProductionReport:
    film_id: str
    status: str
    completed_tasks: int
    failed_tasks: int
    total_tasks: int
    final_output: Optional[str] = None
    error: Optional[str] = None


class AJVYRACinematicMasterProducer:

    def __init__(
        self,
        film_id: str,
        project_root: str | Path,
        media_backend: AJVYRACinematicMediaBackend,
    ):

        self.film_id = film_id
        self.root = Path(project_root)

        self.media = media_backend

        self.scheduler = (
            AJVYRACinematicProductionScheduler(
                self.root
            )
        )

    # ---------------------------------------------------------
    # Task registration
    # ---------------------------------------------------------

    def register_video_task(
        self,
        *,
        task_id: str,
        prompt: str,
        output_path: str,
        duration_seconds: float,
        dependencies: List[str] | None = None,
        priority: int = 50,
        metadata: Dict | None = None,
    ) -> ProductionTask:

        return self.scheduler.add_media_task(
            task_id=task_id,
            film_id=self.film_id,
            prompt=prompt,
            output_path=output_path,
            duration_seconds=duration_seconds,
            dependencies=dependencies,
            priority=priority,
            metadata=metadata,
        )

    # ---------------------------------------------------------
    # Production
    # ---------------------------------------------------------

    def run(
        self,
        *,
        stop_on_failure: bool = True,
    ) -> FilmProductionReport:

        while True:

            ready = (
                self.scheduler.get_ready_tasks()
            )

            if not ready:
                break

            for task in ready:

                self.scheduler.mark_running(
                    task.task_id
                )

                result = self.media.generate(
                    MediaGenerationRequest(
                        media_id=task.task_id,
                        media_type=task.task_type,
                        prompt=task.prompt,
                        output_path=task.output_path,
                        duration_seconds=(
                            task.duration_seconds
                        ),
                        metadata=task.metadata,
                    )
                )

                if result.status != "completed":
                    self.scheduler.mark_failed(
                        task.task_id
                    )

                    if stop_on_failure:
                        return self._report(
                            status="failed",
                            error=result.error,
                        )

                    continue

                self.scheduler.mark_completed(
                    task.task_id
                )

                self.scheduler.save()

        failed = [
            task
            for task in self.scheduler.tasks.values()
            if task.status == "failed"
        ]

        pending = [
            task
            for task in self.scheduler.tasks.values()
            if task.status == "pending"
        ]

        if failed:
            return self._report(
                status="failed",
                error="One or more production tasks failed.",
            )

        if pending:
            return self._report(
                status="blocked",
                error=(
                    "Production queue contains unresolved "
                    "dependencies."
                ),
            )

        if not self.scheduler.tasks:
            return self._report(
                status="empty",
                error="No production tasks registered.",
            )

        return self._report(
            status="media_ready"
        )

    # ---------------------------------------------------------
    # Final assembly
    # ---------------------------------------------------------

    def assemble(
        self,
        output_path: str | Path,
    ) -> Path:

        completed = [
            task
            for task in self.scheduler.tasks.values()
            if (
                task.status == "completed"
                and task.task_type == "video"
            )
        ]

        if not completed:
            raise RuntimeError(
                "No completed video tasks available."
            )

        completed.sort(
            key=lambda task: (
                task.metadata.get(
                    "timeline_order",
                    0,
                )
            )
        )

        for task in completed:
            if not Path(
                task.output_path
            ).exists():
                raise FileNotFoundError(
                    task.output_path
                )

        ffmpeg = shutil.which("ffmpeg")

        if not ffmpeg:
            raise RuntimeError(
                "FFmpeg is required for final assembly."
            )

        output = Path(output_path)
        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat_file = (
            self.root / "cinematic_concat.txt"
        )

        lines = []

        for task in completed:

            source = (
                Path(task.output_path)
                .resolve()
                .as_posix()
                .replace("'", "'\\''")
            )

            lines.append(
                f"file '{source}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        command = [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-movflags",
            "+faststart",
            str(output),
        ]

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if process.returncode != 0:
            raise RuntimeError(
                "FFmpeg assembly failed:\n"
                + process.stderr[-4000:]
            )

        if not output.exists():
            raise RuntimeError(
                "FFmpeg reported success but final "
                "film does not exist."
            )

        return output

    # ---------------------------------------------------------
    # Publish gate
    # ---------------------------------------------------------

    def publish(
        self,
        final_output: str | Path,
        public_directory: str | Path,
        minimum_duration_seconds: float = 1700.0,
    ) -> Path:

        source = Path(final_output)

        if not source.exists():
            raise FileNotFoundError(
                f"Final film does not exist: {source}"
            )

        duration = self._probe_duration(
            source
        )

        if duration < minimum_duration_seconds:
            raise RuntimeError(
                f"Film is too short for publication: "
                f"{duration:.2f}s"
            )

        public_dir = (
            Path(public_directory)
            / self.film_id
        )

        public_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = (
            public_dir / "movie.mp4"
        )

        shutil.copy2(
            source,
            destination,
        )

        metadata = {
            "film_id": self.film_id,
            "status": "READY",
            "duration_seconds": duration,
            "file": str(destination),
        }

        (
            public_dir / "metadata.json"
        ).write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return destination

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _report(
        self,
        *,
        status: str,
        error: Optional[str] = None,
    ) -> FilmProductionReport:

        tasks = list(
            self.scheduler.tasks.values()
        )

        return FilmProductionReport(
            film_id=self.film_id,
            status=status,
            completed_tasks=sum(
                task.status == "completed"
                for task in tasks
            ),
            failed_tasks=sum(
                task.status == "failed"
                for task in tasks
            ),
            total_tasks=len(tasks),
            error=error,
        )

    @staticmethod
    def _probe_duration(
        path: Path,
    ) -> float:

        ffprobe = shutil.which("ffprobe")

        if not ffprobe:
            raise RuntimeError(
                "ffprobe is required for publication."
            )

        result = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "ffprobe failed:\n"
                + result.stderr
            )

        return float(
            result.stdout.strip()
        )
