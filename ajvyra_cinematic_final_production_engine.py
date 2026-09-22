from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from ajvyra_cinematic_final_contract import (
    CinematicFilmContract,
    CinematicMoment,
)

from ajvyra_cinematic_prompt_compiler import (
    AJVYRACinematicPromptCompiler,
)

from ajvyra_cinematic_media_normalizer import (
    AJVYRACinematicMediaNormalizer,
)


@dataclass
class FinalProductionResult:
    film_id: str
    status: str
    movie_path: str | None
    duration_seconds: float
    generated_segments: int
    failed_segments: int
    error: str | None = None


class AJVYRACinematicFinalProductionEngine:

    def __init__(
        self,
        workspace: str | Path,
        media_provider: Any,
        *,
        ffmpeg: str = "ffmpeg",
        ffprobe: str = "ffprobe",
    ) -> None:

        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.provider = media_provider

        self.compiler = (
            AJVYRACinematicPromptCompiler()
        )

        self.normalizer = (
            AJVYRACinematicMediaNormalizer(
                self.workspace / "normalized",
                ffmpeg=ffmpeg,
                ffprobe=ffprobe,
            )
        )

    def produce(
        self,
        film: CinematicFilmContract,
    ) -> FinalProductionResult:

        started = time.time()

        try:
            errors = film.validate()

            if errors:
                raise RuntimeError(
                    "Film contract validation failed:\n"
                    + "\n".join(errors)
                )

            if not self.normalizer.verify_ffmpeg():
                raise RuntimeError(
                    "FFmpeg is not available."
                )

            if not self.normalizer.verify_ffprobe():
                raise RuntimeError(
                    "FFprobe is not available."
                )

            film.status = "RUNNING"

            self._save_contract(film)

            normalized_segments: list[str] = []

            failed_segments = 0

            for moment in film.moments:

                source = self._generate_moment(
                    film,
                    moment,
                )

                if source is None:
                    failed_segments += 1

                    raise RuntimeError(
                        f"Moment generation failed: "
                        f"{moment.moment_id}"
                    )

                normalized = (
                    self._normalize_moment(
                        film,
                        moment,
                        source,
                    )
                )

                normalized_segments.append(
                    normalized
                )

            movie_path = self._assemble(
                film,
                normalized_segments,
            )

            duration = (
                self.normalizer.probe_duration(
                    movie_path
                )
            )

            if duration <= 0:
                raise RuntimeError(
                    "Final movie has invalid duration."
                )

            film.status = "COMPLETED"
            self._save_contract(film)

            result = FinalProductionResult(
                film_id=film.film_id,
                status="COMPLETED",
                movie_path=str(movie_path),
                duration_seconds=duration,
                generated_segments=len(
                    normalized_segments
                ),
                failed_segments=failed_segments,
            )

            self._save_result(
                film,
                result,
                started,
            )

            return result

        except Exception as exc:

            film.status = "FAILED"

            self._save_contract(film)

            result = FinalProductionResult(
                film_id=film.film_id,
                status="FAILED",
                movie_path=None,
                duration_seconds=0.0,
                generated_segments=0,
                failed_segments=1,
                error=str(exc),
            )

            self._save_result(
                film,
                result,
                started,
            )

            return result

    def _generate_moment(
        self,
        film: CinematicFilmContract,
        moment: CinematicMoment,
    ) -> str | None:

        character_data = []

        for character_id in moment.characters:

            character = film.characters.get(
                character_id
            )

            if character is None:
                continue

            character_data.append(
                {
                    "name": character.name,
                    "appearance": character.appearance,
                    "clothing": character.clothing,
                    "personality": character.personality,
                }
            )

        world_data = {}

        if film.worlds:
            world_data = asdict(
                next(
                    iter(film.worlds.values())
                )
            )

        prompt = self.compiler.compile(
            scene_description=moment.description,
            characters=character_data,
            world=world_data,
            emotion=moment.emotion,
            camera=moment.camera,
            lighting=moment.lighting,
            sound=moment.sound,
            continuity_token=film.metadata.get(
                "continuity_token",
                "",
            ),
        )

        output_dir = (
            self.workspace
            / "films"
            / film.film_id
            / "generated"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            output_dir
            / f"{moment.order:06d}_{moment.moment_id}.mp4"
        )

        request = {
            "film_id": film.film_id,
            "moment_id": moment.moment_id,
            "prompt": prompt,
            "output_path": str(
                output_path
            ),
            "duration_target": (
                moment.duration_target
            ),
            "first_frame": (
                moment.first_frame
            ),
            "last_frame": (
                moment.last_frame
            ),
        }

        result = self._provider_generate(
            request
        )

        actual_path = self._extract_path(
            result
        )

        if not actual_path:
            return None

        path = Path(actual_path)

        if not path.exists():
            return None

        if path.stat().st_size <= 0:
            return None

        moment.generated_media.append(
            str(path)
        )

        return str(path)

    def _provider_generate(
        self,
        request: dict[str, Any],
    ) -> Any:

        if hasattr(
            self.provider,
            "generate",
        ):
            return self.provider.generate(
                request
            )

        if hasattr(
            self.provider,
            "generate_media",
        ):
            return self.provider.generate_media(
                request
            )

        if callable(self.provider):
            return self.provider(
                request
            )

        raise TypeError(
            "Media provider has no supported "
            "generation interface."
        )

    def _normalize_moment(
        self,
        film: CinematicFilmContract,
        moment: CinematicMoment,
        source: str,
    ) -> str:

        output = (
            self.workspace
            / "films"
            / film.film_id
            / "normalized"
            / (
                f"{moment.order:06d}_"
                f"{moment.moment_id}.mp4"
            )
        )

        result = (
            self.normalizer.normalize_video(
                source,
                output,
            )
        )

        return result.output

    def _assemble(
        self,
        film: CinematicFilmContract,
        segments: list[str],
    ) -> Path:

        if not segments:
            raise RuntimeError(
                "No normalized segments."
            )

        film_dir = (
            self.workspace
            / "films"
            / film.film_id
            / "master"
        )

        film_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        concat_file = (
            film_dir
            / "segments.txt"
        )

        with concat_file.open(
            "w",
            encoding="utf-8",
        ) as handle:

            for segment in segments:

                escaped = (
                    str(
                        Path(segment).resolve()
                    )
                    .replace(
                        "\\",
                        "/",
                    )
                    .replace(
                        "'",
                        "'\\''",
                    )
                )

                handle.write(
                    f"file '{escaped}'\n"
                )

        movie = (
            film_dir
            / "movie.mp4"
        )

        import subprocess

        command = [
            self.normalizer.ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(movie),
        ]

        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                "Final FFmpeg assembly failed:\n"
                + completed.stderr.strip()
            )

        if not movie.exists():
            raise RuntimeError(
                "Final movie was not created."
            )

        if movie.stat().st_size <= 0:
            raise RuntimeError(
                "Final movie is empty."
            )

        return movie

    def _extract_path(
        self,
        result: Any,
    ) -> str | None:

        if isinstance(
            result,
            (str, Path),
        ):
            return str(result)

        if isinstance(
            result,
            dict,
        ):
            for key in (
                "output_path",
                "movie_path",
                "video_path",
                "file_path",
                "path",
            ):
                value = result.get(key)

                if value:
                    return str(value)

        for key in (
            "output_path",
            "movie_path",
            "video_path",
            "file_path",
            "path",
        ):
            value = getattr(
                result,
                key,
                None,
            )

            if value:
                return str(value)

        return None

    def _save_contract(
        self,
        film: CinematicFilmContract,
    ) -> None:

        path = (
            self.workspace
            / "films"
            / film.film_id
            / "film_contract.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        film.save(
            str(path)
        )

    def _save_result(
        self,
        film: CinematicFilmContract,
        result: FinalProductionResult,
        started: float,
    ) -> None:

        path = (
            self.workspace
            / "films"
            / film.film_id
            / "production_result.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = asdict(result)

        payload["started_at"] = started
        payload["finished_at"] = time.time()

        path.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
