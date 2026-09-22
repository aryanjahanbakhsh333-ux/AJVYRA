from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

from ajvyra_wan_cinematic_story_adapter import (
    AJVYRAWanCinematicStoryAdapter,
)

from ajvyra_wan_reference_frame_pipeline import (
    AJVYRAWanReferenceFramePipeline,
)

from ajvyra_wan_audio_postproduction_pipeline import (
    AJVYRAWanAudioPostProductionPipeline,
    AudioAsset,
)

from ajvyra_wan_auto_engine import (
    AJVYRAWanAutoEngine,
    WanAutoRequest,
)


@dataclass
class FilmPipelineResult:
    film_id: str
    title: str
    segments_generated: int
    expected_segments: int
    assembled_video: str | None
    final_video: str | None
    audio_ready: bool
    ready: bool
    error: str | None = None


class AJVYRAWanFullCinematicFilmPipeline:

    def __init__(
        self,
        production_root: str | Path = "ajvyra_wan_production",
        model_id: str = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    ) -> None:

        self.root = Path(production_root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.story_adapter = AJVYRAWanCinematicStoryAdapter()
        self.references = AJVYRAWanReferenceFramePipeline(
            self.root / "references"
        )
        self.audio = AJVYRAWanAudioPostProductionPipeline(
            self.root / "audio"
        )

        self.video_engine = AJVYRAWanAutoEngine(
            model_id=model_id,
        )

    def _ffmpeg(self, args: list[str]) -> None:
        completed = subprocess.run(
            ["ffmpeg", "-y", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                completed.stderr[-4000:]
            )

    def _assemble(
        self,
        segment_paths: list[Path],
        output_path: Path,
    ) -> None:

        concat_file = output_path.parent / "concat.txt"

        lines = []

        for path in segment_paths:
            escaped = str(path.resolve()).replace("'", "'\\''")
            lines.append(f"file '{escaped}'")

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        self._ffmpeg([
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_path),
        ])

    def _validate_video(
        self,
        path: Path,
        minimum_duration: float,
    ) -> None:

        if not path.exists():
            raise RuntimeError(
                f"Final video does not exist: {path}"
            )

        if path.stat().st_size < 1_000_000:
            raise RuntimeError(
                f"Final video is suspiciously small: {path}"
            )

        completed = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                completed.stderr[-2000:]
            )

        duration = float(completed.stdout.strip())

        if duration < minimum_duration:
            raise RuntimeError(
                f"Movie duration {duration:.2f}s is below "
                f"required {minimum_duration:.2f}s."
            )

    def produce(
        self,
        film_id: str,
        duration_seconds: int = 1800,
        segment_seconds: float = 5.0625,
        require_audio: bool = True,
    ) -> FilmPipelineResult:

        story = self.story_adapter.get(film_id)

        film_root = self.root / film_id
        segment_root = film_root / "segments"
        segment_root.mkdir(parents=True, exist_ok=True)

        expected_segments = int(
            (duration_seconds / segment_seconds) + 0.999999
        )

        generated = []

        try:
            previous_segment = None

            for index in range(expected_segments):

                output_path = (
                    segment_root /
                    f"segment_{index:04d}.mp4"
                )

                if output_path.exists() and output_path.stat().st_size > 100_000:
                    generated.append(output_path)
                    previous_segment = str(output_path)
                    continue

                continuity = (
                    self.references.build_reference_prompt(
                        film_id=film_id,
                        segment_index=index,
                        previous_segment=previous_segment,
                    )
                    if self.references.load_characters(film_id)
                    else (
                        "Maintain exact visual continuity with previous "
                        "shots, including character appearance, clothing, "
                        "environment and lighting."
                    )
                )

                action = (
                    "continue the emotional story naturally, "
                    "with subtle character acting and cinematic movement"
                )

                camera = (
                    "cinematic anime camera movement, "
                    "controlled depth of field"
                )

                emotion = story.emotional_core

                prompt = self.story_adapter.build_segment_prompt(
                    film_id=film_id,
                    segment_index=index,
                    action=action,
                    camera=camera,
                    emotion=emotion,
                    continuity=continuity,
                )

                request = WanAutoRequest(
                    prompt=prompt,
                    output_path=str(output_path),
                    seed=story.stable_seed(index),
                )

                result = self.video_engine.generate(request)

                if not result.success:
                    raise RuntimeError(
                        f"Wan failed at segment {index}: "
                        f"{result.error}"
                    )

                generated.append(output_path)
                previous_segment = str(output_path)

            if len(generated) != expected_segments:
                raise RuntimeError(
                    "Not all required segments were generated."
                )

            assembled = film_root / "assembled_video.mp4"

            self._assemble(
                generated,
                assembled,
            )

            self._validate_video(
                assembled,
                duration_seconds * 0.90,
            )

            audio_assets = self.audio.discover_assets(film_id)

            final_video = film_root / "final_movie.mp4"

            audio_result = self.audio.mux(
                assembled,
                final_video,
                assets=audio_assets,
                require_audio=require_audio,
            )

            if not audio_result.success:
                raise RuntimeError(
                    audio_result.error or "Audio post-production failed."
                )

            self._validate_video(
                final_video,
                duration_seconds * 0.90,
            )

            result = FilmPipelineResult(
                film_id=film_id,
                title=story.title,
                segments_generated=len(generated),
                expected_segments=expected_segments,
                assembled_video=str(assembled),
                final_video=str(final_video),
                audio_ready=True,
                ready=True,
            )

        except Exception as exc:
            result = FilmPipelineResult(
                film_id=film_id,
                title=story.title,
                segments_generated=len(generated),
                expected_segments=expected_segments,
                assembled_video=None,
                final_video=None,
                audio_ready=False,
                ready=False,
                error=str(exc),
            )

        (film_root / "film_pipeline_result.json").write_text(
            json.dumps(
                asdict(result),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return result
