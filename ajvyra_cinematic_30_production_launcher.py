from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Optional


@dataclass
class FilmLaunchStatus:
    film_id: str
    title: str
    status: str
    started_at: Optional[float] = None
    finished_at: Optional[float] = None
    error: Optional[str] = None


class AJVYRACinematic30ProductionLauncher:
    """
    Resumable production launcher for the complete 30-film catalog.

    The launcher does not fake completion. A film becomes COMPLETE only
    when the supplied production callback reports a real completed output.
    """

    def __init__(
        self,
        workspace: str | Path,
        *,
        state_filename: str = "cinematic_30_launcher_state.json",
    ) -> None:
        self.workspace = Path(workspace)
        self.workspace.mkdir(parents=True, exist_ok=True)

        self.state_path = self.workspace / state_filename

        self.statuses: dict[str, FilmLaunchStatus] = {}
        self._load()

    def register_films(
        self,
        films: list[Any],
    ) -> None:

        for film in films:
            film_id = self._value(
                film,
                "film_id",
                "id",
            )

            title = self._value(
                film,
                "title",
                "name",
            ) or film_id

            if not film_id:
                continue

            if film_id not in self.statuses:
                self.statuses[film_id] = FilmLaunchStatus(
                    film_id=film_id,
                    title=title,
                    status="PENDING",
                )

        self._save()

    def launch(
        self,
        films: list[Any],
        producer: Callable[[Any], Any],
        *,
        resume: bool = True,
        stop_on_failure: bool = False,
    ) -> list[FilmLaunchStatus]:

        self.register_films(films)

        for film in films:
            film_id = self._value(
                film,
                "film_id",
                "id",
            )

            if not film_id:
                continue

            current = self.statuses[film_id]

            if resume and current.status == "COMPLETE":
                continue

            current.status = "RUNNING"
            current.started_at = time.time()
            current.error = None
            self._save()

            try:
                result = producer(film)

                if not self._production_result_is_complete(result):
                    raise RuntimeError(
                        f"Producer returned an incomplete result for '{film_id}'."
                    )

                current.status = "COMPLETE"
                current.finished_at = time.time()

            except Exception as exc:
                current.status = "FAILED"
                current.finished_at = time.time()
                current.error = str(exc)

                self._save()

                if stop_on_failure:
                    break

            self._save()

        return list(self.statuses.values())

    def get_status(
        self,
        film_id: str,
    ) -> Optional[FilmLaunchStatus]:
        return self.statuses.get(film_id)

    def completion_ratio(self) -> float:
        total = len(self.statuses)

        if total == 0:
            return 0.0

        completed = sum(
            1
            for item in self.statuses.values()
            if item.status == "COMPLETE"
        )

        return completed / total

    def summary(self) -> dict:
        total = len(self.statuses)

        complete = sum(
            1
            for item in self.statuses.values()
            if item.status == "COMPLETE"
        )

        running = sum(
            1
            for item in self.statuses.values()
            if item.status == "RUNNING"
        )

        failed = sum(
            1
            for item in self.statuses.values()
            if item.status == "FAILED"
        )

        pending = sum(
            1
            for item in self.statuses.values()
            if item.status == "PENDING"
        )

        return {
            "total": total,
            "complete": complete,
            "running": running,
            "failed": failed,
            "pending": pending,
            "completion_ratio": self.completion_ratio(),
        }

    def _production_result_is_complete(
        self,
        result: Any,
    ) -> bool:

        if result is True:
            return True

        if result is False or result is None:
            return False

        if isinstance(result, dict):
            status = str(
                result.get("status", "")
            ).upper()

            output = (
                result.get("output_path")
                or result.get("movie_path")
            )

            return (
                status in {
                    "COMPLETE",
                    "COMPLETED",
                    "READY",
                    "PUBLISHED",
                    "ASSEMBLED",
                }
                and bool(output)
                and Path(output).exists()
                and Path(output).stat().st_size > 0
            )

        status = str(
            getattr(result, "status", "")
        ).upper()

        output = (
            getattr(result, "output_path", None)
            or getattr(result, "movie_path", None)
        )

        return (
            status in {
                "COMPLETE",
                "COMPLETED",
                "READY",
                "PUBLISHED",
                "ASSEMBLED",
            }
            and bool(output)
            and Path(output).exists()
            and Path(output).stat().st_size > 0
        )

    def _value(
        self,
        item: Any,
        *names: str,
    ) -> Optional[str]:

        for name in names:
            if isinstance(item, dict):
                value = item.get(name)
            else:
                value = getattr(item, name, None)

            if value is not None:
                value = str(value).strip()

                if value:
                    return value

        return None

    def _save(self) -> None:
        data = {
            film_id: asdict(status)
            for film_id, status in self.statuses.items()
        }

        self.state_path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _load(self) -> None:
        if not self.state_path.exists():
            return

        try:
            data = json.loads(
                self.state_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return

        for film_id, raw in data.items():
            try:
                self.statuses[film_id] = FilmLaunchStatus(
                    **raw
                )
            except TypeError:
                continue
