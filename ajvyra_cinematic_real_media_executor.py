from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass
class ExecutionResult:
    task_id: str
    status: str
    output_path: Optional[str]
    provider: Optional[str]
    attempts: int
    error: Optional[str] = None
    started_at: Optional[float] = None
    finished_at: Optional[float] = None


class AJVYRACinematicRealMediaExecutor:
    """
    Executes real cinematic media tasks.

    It never creates fake media files. A successful task must produce
    an actual output file on disk.
    """

    def __init__(
        self,
        workspace: str | Path,
        provider_registry: Any,
        *,
        max_attempts: int = 3,
        retry_delay_seconds: float = 2.0,
    ) -> None:
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.registry = provider_registry
        self.max_attempts = max(1, int(max_attempts))
        self.retry_delay_seconds = max(0.0, float(retry_delay_seconds))

        self.results: dict[str, ExecutionResult] = {}

    def execute_task(
        self,
        task: Any,
        *,
        provider_name: Optional[str] = None,
        payload_builder: Optional[Callable[[Any], dict]] = None,
    ) -> ExecutionResult:

        task_id = str(getattr(task, "task_id", "")).strip()

        if not task_id:
            raise ValueError("Task must contain task_id.")

        media_type = str(
            getattr(task, "media_type", "video")
        ).strip() or "video"

        provider_record = None

        if provider_name:
            provider_record = next(
                (
                    item
                    for item in self.registry.list(media_type)
                    if item.name == provider_name
                ),
                None,
            )

            if provider_record is None:
                raise RuntimeError(
                    f"Provider '{provider_name}' is unavailable "
                    f"for media type '{media_type}'."
                )
        else:
            provider_record = self.registry.select(media_type)

        if provider_record is None:
            result = ExecutionResult(
                task_id=task_id,
                status="FAILED",
                output_path=None,
                provider=None,
                attempts=0,
                error=f"No provider available for media type '{media_type}'.",
            )

            self.results[task_id] = result
            self._save_result(result)
            return result

        provider = provider_record.provider
        payload = (
            payload_builder(task)
            if payload_builder
            else self._default_payload(task)
        )

        started_at = time.time()
        last_error: Optional[str] = None

        for attempt in range(1, self.max_attempts + 1):
            try:
                output = self._call_provider(
                    provider,
                    payload,
                    task,
                )

                output_path = self._extract_output_path(output)

                if not output_path:
                    raise RuntimeError(
                        "Provider completed without returning an output path."
                    )

                output_file = Path(output_path)

                if not output_file.exists():
                    raise RuntimeError(
                        f"Provider reported output that does not exist: "
                        f"{output_file}"
                    )

                if output_file.stat().st_size <= 0:
                    raise RuntimeError(
                        f"Provider produced an empty media file: {output_file}"
                    )

                result = ExecutionResult(
                    task_id=task_id,
                    status="COMPLETED",
                    output_path=str(output_file),
                    provider=provider_record.name,
                    attempts=attempt,
                    started_at=started_at,
                    finished_at=time.time(),
                )

                self.results[task_id] = result
                self._save_result(result)
                return result

            except Exception as exc:
                last_error = str(exc)

                if attempt < self.max_attempts:
                    time.sleep(self.retry_delay_seconds)

        result = ExecutionResult(
            task_id=task_id,
            status="FAILED",
            output_path=None,
            provider=provider_record.name,
            attempts=self.max_attempts,
            error=last_error,
            started_at=started_at,
            finished_at=time.time(),
        )

        self.results[task_id] = result
        self._save_result(result)

        return result

    def execute_tasks(
        self,
        tasks: list[Any],
        *,
        stop_on_failure: bool = False,
    ) -> list[ExecutionResult]:

        results: list[ExecutionResult] = []

        for task in tasks:
            result = self.execute_task(task)
            results.append(result)

            if stop_on_failure and result.status != "COMPLETED":
                break

        return results

    def get_result(self, task_id: str) -> Optional[ExecutionResult]:
        return self.results.get(task_id)

    def _call_provider(
        self,
        provider: Any,
        payload: dict,
        task: Any,
    ) -> Any:

        if hasattr(provider, "generate"):
            return provider.generate(payload)

        if hasattr(provider, "generate_media"):
            return provider.generate_media(payload)

        if callable(provider):
            return provider(payload)

        raise TypeError(
            f"Provider for task '{getattr(task, 'task_id', '?')}' "
            "does not expose generate(), generate_media(), or __call__()."
        )

    def _extract_output_path(self, output: Any) -> Optional[str]:

        if isinstance(output, (str, Path)):
            return str(output)

        if isinstance(output, dict):
            for key in (
                "output_path",
                "file_path",
                "path",
                "video_path",
                "audio_path",
            ):
                value = output.get(key)

                if value:
                    return str(value)

        for attribute in (
            "output_path",
            "file_path",
            "path",
            "video_path",
            "audio_path",
        ):
            value = getattr(output, attribute, None)

            if value:
                return str(value)

        return None

    def _default_payload(self, task: Any) -> dict:
        if hasattr(task, "to_dict"):
            return task.to_dict()

        try:
            return asdict(task)
        except TypeError:
            return dict(vars(task))

    def _save_result(self, result: ExecutionResult) -> None:
        path = self.workspace / "execution_results"
        path.mkdir(parents=True, exist_ok=True)

        output = path / f"{result.task_id}.json"

        with output.open("w", encoding="utf-8") as handle:
            json.dump(
                asdict(result),
                handle,
                ensure_ascii=False,
                indent=2,
            )
