from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

from ajvyra_wan_auto_engine import (
    AJVYRAWanAutoEngine,
    WanGenerationRequest,
)


@dataclass
class FilmSegment:
    index: int
    segment_id: str

    prompt: str

    start_seconds: float
    end_seconds: float

    seed: int


@dataclass
class FilmProductionState:
    film_id: str
    title: str

    target_duration_seconds: int
    segment_duration_seconds: float
    total_segments: int

    generated_segments: int = 0

    status: str = "NOT_STARTED"

    final_movie: Optional[str] = None

    error: Optional[str] = None


class AJVYRAWAutomaticFilmProducer:

    def __init__(
        self,
        engine: AJVYRAWanAutoEngine,
        production_root: str | Path = (
            "production/wan_films"
        ),
    ) -> None:

        self.engine = engine

        self.production_root = Path(
            production_root
        )

    # ---------------------------------------------------------
    # Produce
    # ---------------------------------------------------------

    def produce(
        self,
        film_id: str,
        title: str,
        story: str,
        character_description: str,
        world_description: str,
        *,
        duration_seconds: int = 1800,
        resume: bool = True,
    ) -> FilmProductionState:

        segment_duration = (
            81 / 16
        )

        total_segments = int(
            duration_seconds
            / segment_duration
        )

        if (
            total_segments
            * segment_duration
        ) < duration_seconds:

            total_segments += 1

        state = FilmProductionState(
            film_id=film_id,
            title=title,
            target_duration_seconds=(
                duration_seconds
            ),
            segment_duration_seconds=(
                segment_duration
            ),
            total_segments=total_segments,
            status="GENERATING",
        )

        film_root = (
            self.production_root
            / film_id
        )

        segments_root = (
            film_root
            / "segments"
        )

        segments_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        state_path = (
            film_root
            / "production_state.json"
        )

        try:

            self._save_state(
                state,
                state_path,
            )

            for index in range(
                total_segments
            ):

                segment_id = (
                    f"segment_{index + 1:04d}"
                )

                output_path = (
                    segments_root
                    / f"{segment_id}.mp4"
                )

                # Resume.
                if (
                    resume
                    and output_path.exists()
                    and output_path.stat().st_size
                    > 1024
                ):

                    state.generated_segments += 1

                    self._save_state(
                        state,
                        state_path,
                    )

                    print(
                        f"[RESUME] "
                        f"{title} "
                        f"{index + 1}/"
                        f"{total_segments}"
                    )

                    continue

                start = (
                    index
                    * segment_duration
                )

                end = min(
                    start
                    + segment_duration,
                    duration_seconds,
                )

                prompt = (
                    self._build_prompt(
                        title=title,
                        story=story,
                        character_description=(
                            character_description
                        ),
                        world_description=(
                            world_description
                        ),
                        segment_index=index,
                        total_segments=(
                            total_segments
                        ),
                        start_seconds=start,
                        end_seconds=end,
                    )
                )

                seed = (
                    100000
                    + (
                        abs(
                            hash(
                                film_id
                            )
                        )
                        % 10000
                    )
                    + index
                )

                request = (
                    WanGenerationRequest(
                        prompt=prompt,
                        output_path=output_path,
                        width=832,
                        height=480,
                        num_frames=81,
                        fps=16,
                        guidance_scale=5.0,
                        flow_shift=3.0,
                        seed=seed,
                    )
                )

                result = (
                    self.engine.generate(
                        request
                    )
                )

                if not result.success:

                    state.status = (
                        "FAILED"
                    )

                    state.error = (
                        result.error
                    )

                    self._save_state(
                        state,
                        state_path,
                    )

                    return state

                state.generated_segments += 1

                self._save_state(
                    state,
                    state_path,
                )

                print(
                    f"[DONE] "
                    f"{title} "
                    f"{state.generated_segments}/"
                    f"{total_segments}"
                )

            state.status = (
                "SEGMENTS_COMPLETE"
            )

            self._save_state(
                state,
                state_path,
            )

            return state

        except Exception as exc:

            state.status = "FAILED"

            state.error = (
                f"{type(exc).__name__}: {exc}"
            )

            self._save_state(
                state,
                state_path,
            )

            return state

    # ---------------------------------------------------------
    # Prompt
    # ---------------------------------------------------------

    @staticmethod
    def _build_prompt(
        *,
        title: str,
        story: str,
        character_description: str,
        world_description: str,
        segment_index: int,
        total_segments: int,
        start_seconds: float,
        end_seconds: float,
    ) -> str:

        progress = (
            segment_index
            / max(
                total_segments - 1,
                1,
            )
        )

        if progress < 0.25:
            phase = "opening"
        elif progress < 0.60:
            phase = "rising conflict"
        elif progress < 0.85:
            phase = "climax"
        else:
            phase = "resolution"

        return f"""
Cinematic original anime feature film.

Film title: {title}.

Story:
{story}

Main character:
{character_description}

World:
{world_description}

Current film phase:
{phase}.

This is cinematic segment
{segment_index + 1} of {total_segments}.

Time range:
{start_seconds:.2f} to {end_seconds:.2f} seconds.

Create a continuous animated cinematic shot.

Maintain exactly the same character identity,
face structure, hair, eye color, clothing,
body proportions and visual design.

Maintain the same world geography,
architecture, weather, time of day and
lighting language.

Use deliberate cinematic camera movement.

Show meaningful character action rather than
a static image.

Strong anime cinematography,
detailed environment,
cinematic composition,
depth,
natural movement,
consistent anatomy,
dramatic lighting,
emotionally coherent storytelling.

Do not add text.
Do not add subtitles.
Do not add logos.
Do not change character identity.
""".strip()

    # ---------------------------------------------------------
    # State
    # ---------------------------------------------------------

    @staticmethod
    def _save_state(
        state: FilmProductionState,
        path: Path,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                asdict(state),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
