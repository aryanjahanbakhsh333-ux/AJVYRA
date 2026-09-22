from __future__ import annotations

import json
import time
import traceback
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, Optional


@dataclass
class FilmFactoryStatus:
    film_id: str
    title: str
    status: str

    total_segments: int = 0
    generated_segments: int = 0

    movie_path: Optional[str] = None
    duration_seconds: float = 0.0

    qc_passed: bool = False
    site_ready: bool = False

    error: Optional[str] = None


class AJVYRACompleteCinematicFilmFactory:
    """
    Complete build-time production factory.

    Pipeline:

        Story
          ↓
        Director
          ↓
        Segment Planner
          ↓
        Continuity
          ↓
        Local Wan
          ↓
        Real MP4 Segments
          ↓
        Assembly
          ↓
        QC
          ↓
        Site-ready movie

    No fake media is generated.
    """

    def __init__(
        self,
        production_root: str | Path = "production/ajvyra_cinematic",
        public_root: str | Path = "public",
        external_media_base_url: str | None = None,
    ) -> None:

        self.production_root = Path(
            production_root
        )

        self.public_root = Path(
            public_root
        )

        self.external_media_base_url = (
            external_media_base_url
        )

        self.production_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._load_components()

    # ---------------------------------------------------------
    # Component loading
    # ---------------------------------------------------------

    def _load_components(self) -> None:

        from ajvyra_cinematic_30_film_story_bible import (
            AJVYRA30FilmStoryBible,
        )

        from ajvyra_cinematic_real_film_director import (
            AJVYRACinematicRealFilmDirector,
        )

        from ajvyra_cinematic_segment_planner import (
            AJVYRACinematicSegmentPlanner,
        )

        from ajvyra_cinematic_local_production_runner import (
            AJVYRACinematicLocalProductionRunner,
        )

        from ajvyra_cinematic_local_batch_runner import (
            AJVYRACinematicLocalBatchRunner,
        )

        from ajvyra_cinematic_local_film_assembler import (
            AJVYRACinematicLocalFilmAssembler,
        )

        from ajvyra_cinematic_local_production_qc import (
            AJVYRACinematicLocalProductionQC,
        )

        self.story_bible = AJVYRA30FilmStoryBible()

        self.director = (
            AJVYRACinematicRealFilmDirector()
        )

        self.segment_planner = (
            AJVYRACinematicSegmentPlanner()
        )

        self.local_runner = (
            AJVYRACinematicLocalProductionRunner(
                output_root=self.production_root
            )
        )

        self.batch_runner = (
            AJVYRACinematicLocalBatchRunner(
                runner=self.local_runner,
                output_root=self.production_root,
            )
        )

        self.assembler = (
            AJVYRACinematicLocalFilmAssembler(
                output_root=self.production_root
            )
        )

        self.qc = (
            AJVYRACinematicLocalProductionQC(
                minimum_duration_seconds=1.0,
                maximum_duration_seconds=7200.0,
            )
        )

    # ---------------------------------------------------------
    # One film
    # ---------------------------------------------------------

    def build_film(
        self,
        film_id: str,
        *,
        resume: bool = True,
        stop_on_error: bool = True,
    ) -> FilmFactoryStatus:

        started = time.time()

        film = self._get_story(
            film_id
        )

        title = self._read(
            film,
            "title",
            film_id,
        )

        status = FilmFactoryStatus(
            film_id=film_id,
            title=title,
            status="STARTING",
        )

        state_path = (
            self.production_root
            / film_id
            / "factory_state.json"
        )

        try:

            self._save_state(
                status,
                state_path,
            )

            # -------------------------------------------------
            # Director
            # -------------------------------------------------

            directed = self._direct_film(
                film
            )

            # -------------------------------------------------
            # Segment planning
            # -------------------------------------------------

            segments = self._plan_segments(
                film,
                directed,
            )

            segments = list(
                segments
            )

            status.total_segments = len(
                segments
            )

            status.status = (
                "GENERATING_SEGMENTS"
            )

            self._save_state(
                status,
                state_path,
            )

            if not segments:
                raise RuntimeError(
                    "No cinematic segments were produced."
                )

            # -------------------------------------------------
            # Convert segments to local generation format
            # -------------------------------------------------

            generation_segments = []

            for index, segment in enumerate(
                segments,
                start=1,
            ):

                segment_id = self._read(
                    segment,
                    "segment_id",
                    f"segment_{index:04d}",
                )

                prompt = self._build_prompt(
                    film,
                    segment,
                )

                reference_image = (
                    self._read(
                        segment,
                        "reference_image",
                        None,
                    )
                )

                generation_segments.append(
                    {
                        "segment_id": segment_id,
                        "prompt": prompt,
                        "reference_image": (
                            reference_image
                        ),
                        "chapter": self._read(
                            segment,
                            "chapter",
                            "",
                        ),
                        "scene": self._read(
                            segment,
                            "scene",
                            "",
                        ),
                        "emotion": self._read(
                            segment,
                            "emotion",
                            "",
                        ),
                        "camera": self._read(
                            segment,
                            "camera",
                            "",
                        ),
                        "lighting": self._read(
                            segment,
                            "lighting",
                            "",
                        ),
                        "action": self._read(
                            segment,
                            "action",
                            "",
                        ),
                    }
                )

            # -------------------------------------------------
            # Real Wan generation
            # -------------------------------------------------

            generation_results = (
                self.batch_runner.run(
                    film_id=film_id,
                    film_title=title,
                    segments=generation_segments,
                    stop_on_error=stop_on_error,
                    resume=resume,
                    generation_options={
                        "width": 832,
                        "height": 480,
                        "fps": 16,
                        "num_frames": 81,
                        "seed": None,
                    },
                )
            )

            successful = [
                result
                for result in generation_results
                if result.success
            ]

            status.generated_segments = len(
                successful
            )

            if (
                len(successful)
                != len(generation_segments)
            ):

                status.status = (
                    "SEGMENT_GENERATION_FAILED"
                )

                failed = [
                    result
                    for result in generation_results
                    if not result.success
                ]

                if failed:
                    status.error = (
                        failed[0].error
                    )

                self._save_state(
                    status,
                    state_path,
                )

                return status

            # -------------------------------------------------
            # Assembly
            # -------------------------------------------------

            status.status = "ASSEMBLING"

            self._save_state(
                status,
                state_path,
            )

            segment_paths = [
                result.output_path
                for result in successful
                if result.output_path
            ]

            assembly = (
                self.assembler.assemble(
                    film_id,
                    segment_paths,
                )
            )

            if not assembly.success:
                raise RuntimeError(
                    assembly.error
                    or "Film assembly failed."
                )

            status.movie_path = (
                assembly.output_path
            )

            status.duration_seconds = (
                assembly.duration_seconds
            )

            # -------------------------------------------------
            # QC
            # -------------------------------------------------

            status.status = "QC"

            self._save_state(
                status,
                state_path,
            )

            qc = self.qc.check(
                film_id,
                assembly.output_path,
            )

            qc_path = (
                self.production_root
                / film_id
                / "qc.json"
            )

            self.qc.save_report(
                qc,
                qc_path,
            )

            status.qc_passed = qc.passed

            if not qc.passed:
                status.status = "QC_FAILED"
                status.error = "; ".join(
                    qc.errors
                )

                self._save_state(
                    status,
                    state_path,
                )

                return status

            # -------------------------------------------------
            # Site preparation
            # -------------------------------------------------

            status.status = (
                "PREPARING_SITE"
            )

            self._save_state(
                status,
                state_path,
            )

            self._prepare_site_entry(
                film,
                status,
            )

            status.site_ready = True
            status.status = "READY"

            self._save_state(
                status,
                state_path,
            )

            return status

        except Exception as exc:

            status.status = "FAILED"
            status.error = (
                f"{type(exc).__name__}: {exc}"
            )

            self._save_state(
                status,
                state_path,
            )

            return status

    # ---------------------------------------------------------
    # Story access
    # ---------------------------------------------------------

    def _get_story(
        self,
        film_id: str,
    ) -> Any:

        candidates = [
            "get",
            "get_film",
            "find",
        ]

        for method_name in candidates:

            method = getattr(
                self.story_bible,
                method_name,
                None,
            )

            if method is None:
                continue

            try:

                result = method(
                    film_id
                )

                if result is not None:
                    return result

            except TypeError:
                continue

        films = getattr(
            self.story_bible,
            "films",
            None,
        )

        if isinstance(
            films,
            dict,
        ):

            if film_id in films:
                return films[film_id]

        if isinstance(
            films,
            list,
        ):

            for film in films:

                if self._read(
                    film,
                    "film_id",
                    None,
                ) == film_id:

                    return film

        raise KeyError(
            f"Film not found in story bible: {film_id}"
        )

    # ---------------------------------------------------------
    # Director
    # ---------------------------------------------------------

    def _direct_film(
        self,
        film: Any,
    ) -> Any:

        for name in (
            "direct",
            "create_moments",
            "build",
        ):

            method = getattr(
                self.director,
                name,
                None,
            )

            if method is None:
                continue

            try:
                return method(
                    film
                )
            except TypeError:
                continue

        return None

    # ---------------------------------------------------------
    # Segment planner
    # ---------------------------------------------------------

    def _plan_segments(
        self,
        film: Any,
        directed: Any,
    ) -> Iterable[Any]:

        candidates = [
            (
                "plan",
                (film, directed),
            ),
            (
                "plan_film",
                (film,),
            ),
            (
                "build",
                (film,),
            ),
            (
                "create_segments",
                (film,),
            ),
        ]

        for name, args in candidates:

            method = getattr(
                self.segment_planner,
                name,
                None,
            )

            if method is None:
                continue

            try:

                result = method(
                    *args
                )

                if result is not None:
                    return result

            except TypeError:
                continue

        raise RuntimeError(
            "Could not find a compatible "
            "segment planner method."
        )

    # ---------------------------------------------------------
    # Prompt
    # ---------------------------------------------------------

    def _build_prompt(
        self,
        film: Any,
        segment: Any,
    ) -> str:

        story = self._read(
            film,
            "logline",
            "",
        )

        world = self._read(
            film,
            "world",
            "",
        )

        visual_style = self._read(
            film,
            "visual_style",
            "",
        )

        emotional_core = self._read(
            film,
            "emotional_core",
            "",
        )

        values = [
            "cinematic anime film",
            story,
            world,
            visual_style,
            emotional_core,
            self._read(
                segment,
                "prompt",
                "",
            ),
            f"emotion: {self._read(segment, 'emotion', '')}",
            f"camera: {self._read(segment, 'camera', '')}",
            f"lighting: {self._read(segment, 'lighting', '')}",
            f"action: {self._read(segment, 'action', '')}",
            (
                "Maintain exact character identity, "
                "hair, face, clothing, body proportions, "
                "location and lighting continuity."
            ),
        ]

        return " ".join(
            str(value).strip()
            for value in values
            if value
        )

    # ---------------------------------------------------------
    # Site entry
    # ---------------------------------------------------------

    def _prepare_site_entry(
        self,
        film: Any,
        status: FilmFactoryStatus,
    ) -> None:

        if not status.movie_path:
            raise RuntimeError(
                "Cannot prepare site entry "
                "without a movie."
            )

        movie = Path(
            status.movie_path
        )

        if not movie.exists():
            raise RuntimeError(
                "Final movie does not exist."
            )

        film_dir = (
            self.public_root
            / "cinematic_anime"
            / status.film_id
        )

        film_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata = {
            "film_id": status.film_id,
            "title": status.title,
            "watchable": True,
            "duration_seconds": (
                status.duration_seconds
            ),
            "movie_local_path": str(
                movie
            ),
            "external_url": self._external_url(
                status.film_id
            ),
        }

        path = (
            film_dir
            / "metadata.json"
        )

        path.write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def _external_url(
        self,
        film_id: str,
    ) -> Optional[str]:

        if not self.external_media_base_url:
            return None

        return (
            self.external_media_base_url.rstrip("/")
            + "/"
            + film_id
            + "/movie.mp4"
        )

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @staticmethod
    def _save_state(
        status: FilmFactoryStatus,
        path: Path,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                asdict(status),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _read(
        obj: Any,
        name: str,
        default: Any = None,
    ) -> Any:

        if obj is None:
            return default

        if isinstance(
            obj,
            dict,
        ):
            return obj.get(
                name,
                default,
            )

        return getattr(
            obj,
            name,
            default,
        )
