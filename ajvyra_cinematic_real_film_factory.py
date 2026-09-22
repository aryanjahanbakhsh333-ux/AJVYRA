from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable
import hashlib
import json
import subprocess
import time


@dataclass
class FilmFactoryResult:
    film_id: str
    title: str
    status: str

    segment_count: int
    completed_segments: int

    final_movie: str | None
    error: str | None = None


class AJVYRACinematicRealFilmFactory:

    def __init__(
        self,
        provider: Any,
        planner: Any,
        root: str | Path = "public/cinematic_anime",
        retries: int = 3,
    ):
        self.provider = provider
        self.planner = planner
        self.root = Path(root)
        self.retries = max(1, retries)

    def produce(
        self,
        film_id: str,
        title: str,
        genre: str,
        story: str,
        characters: list[dict[str, Any]] | None = None,
        world: dict[str, Any] | None = None,
    ) -> FilmFactoryResult:

        film_root = self.root / film_id
        segment_root = film_root / "segments"
        film_root.mkdir(parents=True, exist_ok=True)
        segment_root.mkdir(parents=True, exist_ok=True)

        state_path = film_root / "factory_state.json"

        segments = self.planner.plan_film(
            film_id=film_id,
            title=title,
            genre=genre,
            story=story,
            characters=characters,
            world=world,
        )

        self.planner.save(
            segments,
            film_root / "segment_plan.json",
        )

        state = self._load_state(state_path)

        completed = 0

        for segment in segments:
            output_path = (
                segment_root
                / f"{segment.segment_id}.mp4"
            )

            if self._valid_media(output_path):
                completed += 1

                self._update_state(
                    state_path,
                    state,
                    segment.segment_id,
                    "completed",
                )

                continue

            request = {
                "film_id": film_id,
                "segment_id": segment.segment_id,
                "prompt": segment.prompt,
                "output_path": str(output_path),
                "duration_seconds": segment.duration_seconds,
                "resolution": "720p",
                "aspect_ratio": "16:9",
                "metadata": {
                    "title": title,
                    "genre": genre,
                    "chapter": segment.chapter,
                    "scene": segment.scene,
                    "emotion": segment.emotional_direction,
                },
            }

            success = False
            last_error = None

            for attempt in range(1, self.retries + 1):

                self._update_state(
                    state_path,
                    state,
                    segment.segment_id,
                    "running",
                    attempt=attempt,
                )

                try:
                    result = self.provider.generate(request)

                    if not self._valid_media(result):
                        raise RuntimeError(
                            "Provider returned invalid media."
                        )

                    completed += 1
                    success = True

                    self._update_state(
                        state_path,
                        state,
                        segment.segment_id,
                        "completed",
                        attempt=attempt,
                    )

                    break

                except Exception as exc:
                    last_error = str(exc)

                    self._update_state(
                        state_path,
                        state,
                        segment.segment_id,
                        "failed",
                        attempt=attempt,
                        error=last_error,
                    )

                    if attempt < self.retries:
                        time.sleep(min(30, attempt * 5))

            if not success:
                return FilmFactoryResult(
                    film_id=film_id,
                    title=title,
                    status="FAILED",
                    segment_count=len(segments),
                    completed_segments=completed,
                    final_movie=None,
                    error=(
                        f"{segment.segment_id}: "
                        f"{last_error}"
                    ),
                )

        final_movie = film_root / "movie.mp4"

        self._assemble(
            segments,
            segment_root,
            final_movie,
        )

        if not self._valid_media(final_movie):
            return FilmFactoryResult(
                film_id=film_id,
                title=title,
                status="FAILED",
                segment_count=len(segments),
                completed_segments=completed,
                final_movie=None,
                error="Final movie failed validation.",
            )

        checksum = self._sha256(final_movie)

        metadata = {
            "film_id": film_id,
            "title": title,
            "genre": genre,
            "status": "READY",
            "segment_count": len(segments),
            "completed_segments": completed,
            "movie": str(final_movie),
            "sha256": checksum,
        }

        (film_root / "movie_metadata.json").write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return FilmFactoryResult(
            film_id=film_id,
            title=title,
            status="READY",
            segment_count=len(segments),
            completed_segments=completed,
            final_movie=str(final_movie),
        )

    def _assemble(
        self,
        segments: list[Any],
        segment_root: Path,
        output: Path,
    ) -> None:

        concat_file = segment_root / "concat.txt"

        lines = []

        for segment in segments:
            path = (
                segment_root
                / f"{segment.segment_id}.mp4"
            )

            if not path.exists():
                raise RuntimeError(
                    f"Missing segment: {path}"
                )

            safe_path = path.resolve().as_posix().replace("'", "'\\''")

            lines.append(
                f"file '{safe_path}'"
            )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]

        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if process.returncode != 0:
            raise RuntimeError(
                "FFmpeg assembly failed:\n"
                + process.stderr[-4000:]
            )

    @staticmethod
    def _valid_media(path: str | Path) -> bool:
        path = Path(path)

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 10_000
        )

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(
                lambda: handle.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _load_state(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {
                "segments": {},
            }

        try:
            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return {
                "segments": {},
            }

    @staticmethod
    def _update_state(
        path: Path,
        state: dict[str, Any],
        segment_id: str,
        status: str,
        **extra: Any,
    ) -> None:

        state.setdefault("segments", {})

        state["segments"][segment_id] = {
            "status": status,
            **extra,
        }

        path.write_text(
            json.dumps(
                state,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
