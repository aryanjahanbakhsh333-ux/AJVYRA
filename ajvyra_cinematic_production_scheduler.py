from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class ProductionTask:
    task_id: str
    film_id: str
    task_type: str
    priority: int

    duration_seconds: float = 0.0
    dependencies: List[str] = field(
        default_factory=list
    )

    status: str = "pending"

    prompt: str = ""
    output_path: str = ""

    metadata: Dict = field(
        default_factory=dict
    )


class AJVYRACinematicProductionScheduler:

    def __init__(
        self,
        project_root: str | Path,
    ):
        self.root = Path(project_root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.tasks: Dict[
            str,
            ProductionTask
        ] = {}

    def add_task(
        self,
        task: ProductionTask,
    ) -> ProductionTask:

        if task.task_id in self.tasks:
            raise ValueError(
                f"Duplicate task: {task.task_id}"
            )

        self.tasks[task.task_id] = task
        return task

    def add_media_task(
        self,
        *,
        task_id: str,
        film_id: str,
        prompt: str,
        output_path: str,
        duration_seconds: float,
        dependencies: List[str] | None = None,
        priority: int = 50,
        metadata: Dict | None = None,
    ) -> ProductionTask:

        task = ProductionTask(
            task_id=task_id,
            film_id=film_id,
            task_type="video",
            priority=priority,
            duration_seconds=duration_seconds,
            dependencies=dependencies or [],
            prompt=prompt,
            output_path=output_path,
            metadata=metadata or {},
        )

        return self.add_task(task)

    def get_ready_tasks(self) -> List[ProductionTask]:

        ready = []

        for task in self.tasks.values():

            if task.status != "pending":
                continue

            dependencies_ready = all(
                self.tasks[
                    dependency
                ].status == "completed"
                for dependency in task.dependencies
                if dependency in self.tasks
            )

            dependencies_known = all(
                dependency in self.tasks
                for dependency in task.dependencies
            )

            if dependencies_known and dependencies_ready:
                ready.append(task)

        return sorted(
            ready,
            key=lambda item: (
                -item.priority,
                item.task_id,
            ),
        )

    def mark_running(
        self,
        task_id: str,
    ) -> None:
        self.tasks[
            task_id
        ].status = "running"

    def mark_completed(
        self,
        task_id: str,
    ) -> None:
        self.tasks[
            task_id
        ].status = "completed"

    def mark_failed(
        self,
        task_id: str,
    ) -> None:
        self.tasks[
            task_id
        ].status = "failed"

    def completion_ratio(self) -> float:

        if not self.tasks:
            return 0.0

        completed = sum(
            task.status == "completed"
            for task in self.tasks.values()
        )

        return completed / len(self.tasks)

    def save(self) -> Path:

        path = self.root / "production_queue.json"

        path.write_text(
            json.dumps(
                {
                    "tasks": [
                        asdict(task)
                        for task in self.tasks.values()
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
