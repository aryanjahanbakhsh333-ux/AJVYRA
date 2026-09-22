from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable


@dataclass
class FilmRuntimeStatus:
    film_id: str
    title: str
    status: str
    movie_path: str | None = None
    duration_seconds: float = 0.0
    error: str | None = None
    started_at: float | None = None
    finished_at: float | None = None


class AJVYRACinematicReal30Runtime:

    def __init__(
        self,
        workspace: str | Path,
    ) -> None:

        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.state_path = (
            self.workspace
            / "real_30_runtime_state.json"
        )

        self.statuses: dict[
            str,
            FilmRuntimeStatus
        ] = {}

        self._load()

    def run(
        self,
        films: list[Any],
        producer: Callable[[Any], Any],
        *,
        resume: bool = True,
    ) -> list[FilmRuntimeStatus]:

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

            previous = self.statuses.get(
                film_id
            )

            if (
                resume
                and previous
                and previous.status == "COMPLETE"
                and previous.movie_path
                and Path(
                    previous.movie_path
                ).exists()
            ):
                continue

            status = FilmRuntimeStatus(
                film_id=film_id,
                title=title,
                status="RUNNING",
                started_at=time.time(),
            )

            self.statuses[film_id] = status
            self._save()

            try:
                result = producer(film)

                output = (
                    getattr(
                        result,
                        "movie_path",
                        None,
                    )
                    or (
                        result.get("movie_path")
                        if isinstance(result, dict)
                        else None
                    )
                )

                duration = (
                    getattr(
                        result,
                        "duration_seconds",
                        0.0,
                    )
                    or (
                        result.get(
                            "duration_seconds",
                            0.0,
                        )
                        if isinstance(result, dict)
                        else 0.0
                    )
                )

                result_status = (
                    getattr(
                        result,
                        "status",
                        "",
                    )
                    or (
                        result.get(
                            "status",
                            "",
                        )
                        if isinstance(result, dict)
                        else ""
                    )
                )

                if (
                    str(result_status).upper()
                    not in {
                        "COMPLETE",
                        "COMPLETED",
                    }
                ):
                    raise RuntimeError(
                        f"Film producer returned status "
                        f"'{result_status}'."
                    )

                if not output:
                    raise RuntimeError(
                        "Film producer returned no movie path."
                    )

                output_path = Path(output)

                if not output_path.exists():
                    raise RuntimeError(
                        f"Final movie does not exist: "
                        f"{output_path}"
                    )

                if output_path.stat().st_size <= 0:
                    raise RuntimeError(
                        f"Final movie is empty: "
                        f"{output_path}"
                    )

                status.status = "COMPLETE"
                status.movie_path = str(
                    output_path
                )
                status.duration_seconds = float(
                    duration
                )

            except Exception as exc:
                status.status = "FAILED"
                status.error = str(exc)

            finally:
                status.finished_at = time.time()
                self._save()

        return list(
            self.statuses.values()
        )

    def summary(self) -> dict:
        values = list(
            self.statuses.values()
        )

        return {
            "total": len(values),
            "complete": sum(
                x.status == "COMPLETE"
                for x in values
            ),
            "running": sum(
                x.status == "RUNNING"
                for x in values
            ),
            "failed": sum(
                x.status == "FAILED"
                for x in values
            ),
            "pending": sum(
                x.status == "PENDING"
                for x in values
            ),
        }

    def _value(
        self,
        item: Any,
        *names: str,
    ) -> str | None:

        for name in names:
            if isinstance(item, dict):
                value = item.get(name)
            else:
                value = getattr(
                    item,
                    name,
                    None,
                )

            if value is not None:
                value = str(value).strip()

                if value:
                    return value

        return None

    def _save(self) -> None:

        payload = {
            film_id: asdict(status)
            for film_id, status
            in self.statuses.items()
        }

        self.state_path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _load(self) -> None:

        if not self.state_path.exists():
            return

        try:
            payload = json.loads(
                self.state_path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return

        for film_id, raw in payload.items():
            try:
                self.statuses[film_id] = (
                    FilmRuntimeStatus(**raw)
                )
            except TypeError:
                continue
