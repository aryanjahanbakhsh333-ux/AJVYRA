from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path

from ajvyra_wan_cinematic_story_adapter import (
    AJVYRAWanCinematicStoryAdapter,
)

from ajvyra_wan_final_reference_chain import (
    AJVYRAWanFinalReferenceChain,
)

from ajvyra_wan_final_voice_bridge import (
    AJVYRAFinalVoiceBridge,
    VoiceRequest,
)

from ajvyra_wan_final_subtitle_bridge import (
    AJVYRAFinalSubtitleBridge,
    FinalSubtitleCue,
)

from ajvyra_wan_final_audio_video_mixer import (
    AJVYRAFinalAudioVideoMixer,
)

from ajvyra_wan_auto_engine import (
    AJVYRAWanAutoEngine,
    WanAutoRequest,
)


@dataclass
class FinalFilmRelease:
    film_id: str
    title: str

    segments_expected: int
    segments_ready: int

    video_ready: bool
    voice_ready: bool
    subtitle_ready: bool
    final_movie_ready: bool

    final_movie: str | None
    checksum: str | None

    error: str | None = None


class AJVYRAWanFinalCinematicReleaseFactory:

    FILMS = [
        "vey­lora",
        "aelvryn",
        "nyxara",
        "kaelith",
        "orivane",
        "zeravia",
        "vaelune",
        "ravelyth",
        "solvarya",
        "xaveren",
        "elyvara",
        "neravelle",
        "vaerith",
        "lunavyr",
        "averlyn",
        "neyvara",
        "elvaria",
        "virelya",
        "caelora",
        "seravyn",
        "mouravia",
        "noxelya",
        "vaelora",
        "eryndra",
        "neylith",
        "auralyne",
        "velmora",
        "seyravia",
        "oryvane",
        "luminarae",
    ]

    def __init__(
        self,
        root: str | Path = "ajvyra_final_release",
        model_id: str = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    ):

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.story = (
            AJVYRAWanCinematicStoryAdapter()
        )

        self.reference = (
            AJVYRAWanFinalReferenceChain(
                self.root / "references"
            )
        )

        self.voice = (
            AJVYRAFinalVoiceBridge(
                self.root / "voice"
            )
        )

        self.subtitles = (
            AJVYRAFinalSubtitleBridge(
                self.root / "subtitles"
            )
        )

        self.mixer = (
            AJVYRAFinalAudioVideoMixer()
        )

        self.wan = (
            AJVYRAWanAutoEngine(
                model_id=model_id
            )
        )

    @staticmethod
    def checksum(
        path: str | Path,
    ) -> str:

        digest = hashlib.sha256()

        with Path(path).open("rb") as handle:

            while True:

                chunk = handle.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def ffprobe_duration(
        path: str | Path,
    ) -> float:

        result = subprocess.run(
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

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr
            )

        return float(
            result.stdout.strip()
        )

    def produce_segment(
        self,
        film_id: str,
        index: int,
        prompt: str,
        output: Path,
    ) -> Path:

        story = self.story.get(
            film_id
        )

        request = WanAutoRequest(
            prompt=prompt,
            output_path=str(output),
            seed=story.stable_seed(index),
        )

        result = self.wan.generate(
            request
        )

        if not result.success:
            raise RuntimeError(
                f"Wan generation failed: "
                f"{result.error}"
            )

        if not output.exists():
            raise RuntimeError(
                "Wan reported success but "
                "no MP4 was produced."
            )

        return output

    def assemble(
        self,
        segments: list[Path],
        output: Path,
    ) -> Path:

        concat = (
            output.parent
            / "segments.txt"
        )

        lines = []

        for segment in segments:

            if not segment.exists():
                raise FileNotFoundError(
                    segment
                )

            path = (
                str(segment.resolve())
                .replace("'", "'\\''")
            )

            lines.append(
                f"file '{path}'"
            )

        concat.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat),
                "-c",
                "copy",
                str(output),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr[-5000:]
            )

        return output

    def create_release(
        self,
        film_id: str,
        duration_seconds: int = 1800,
        segment_seconds: float = 5.0625,
    ) -> FinalFilmRelease:

        story = self.story.get(
            film_id
        )

        film_root = (
            self.root / film_id
        )

        segments_root = (
            film_root / "segments"
        )

        segments_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        expected = int(
            duration_seconds
            / segment_seconds
            + 0.999999
        )

        ready_segments = []

        try:

            for index in range(
                expected
            ):

                output = (
                    segments_root
                    / f"{index:04d}.mp4"
                )

                if (
                    output.exists()
                    and output.stat().st_size
                    > 100_000
                ):

                    ready_segments.append(
                        output
                    )
                    continue

                snapshot = (
                    self.reference
                    .create_snapshot(
                        film_id=film_id,
                        segment_index=index,
                        characters=[
                            {
                                "name":
                                    story.protagonist,
                                "role":
                                    "protagonist",
                            },
                            {
                                "name":
                                    story.antagonist,
                                "role":
                                    "antagonistic_force",
                            },
                        ],
                        locations=[
                            {
                                "world":
                                    story.world
                            }
                        ],
                        costume_state={},
                        lighting_state={
                            "style":
                                story.visual_style
                        },
                    )
                )

                prompt = (
                    story.base_prompt()
                    + "\n"
                    + self.reference.build_prompt(
                        story.base_prompt(),
                        snapshot,
                    )
                    + "\n"
                    "Current action: continue the story "
                    "naturally from the previous shot. "
                    "Preserve cinematic continuity."
                )

                self.produce_segment(
                    film_id,
                    index,
                    prompt,
                    output,
                )

                ready_segments.append(
                    output
                )

            if len(ready_segments) != expected:
                raise RuntimeError(
                    "Not every required video segment exists."
                )

            assembled = (
                film_root
                / "assembled.mp4"
            )

            self.assemble(
                ready_segments,
                assembled,
            )

            duration = (
                self.ffprobe_duration(
                    assembled
                )
            )

            if duration < (
                duration_seconds * 0.90
            ):
                raise RuntimeError(
                    f"Assembled film is too short: "
                    f"{duration:.2f}s"
                )

            voice_requests = []

            voice_script = (
                film_root
                / "dialogue.json"
            )

            if voice_script.exists():

                data = json.loads(
                    voice_script.read_text(
                        encoding="utf-8"
                    )
                )

                for index, item in enumerate(
                    data
                ):

                    output = (
                        film_root
                        / "voice"
                        / f"{index:05d}.wav"
                    )

                    request = VoiceRequest(
                        film_id=film_id,
                        segment_index=int(
                            item.get(
                                "segment_index",
                                0,
                            )
                        ),
                        character_id=str(
                            item.get(
                                "character_id",
                                "unknown",
                            )
                        ),
                        text=str(
                            item["text"]
                        ),
                        language=str(
                            item.get(
                                "language",
                                "fa",
                            )
                        ),
                        emotion=str(
                            item.get(
                                "emotion",
                                story.emotional_core,
                            )
                        ),
                        output_path=str(
                            output
                        ),
                    )

                    result = (
                        self.voice.synthesize(
                            request
                        )
                    )

                    if not result.success:
                        raise RuntimeError(
                            result.error
                        )

                    voice_requests.append(
                        request
                    )

            else:

                raise RuntimeError(
                    "No dialogue.json exists. "
                    "A real cinematic release cannot "
                    "be published without a dialogue plan."
                )

            self.voice.save_manifest(
                film_id,
                voice_requests,
            )

            subtitle_cues = []

            for item in json.loads(
                voice_script.read_text(
                    encoding="utf-8"
                )
            ):

                subtitle_cues.append(
                    FinalSubtitleCue(
                        start=float(
                            item["start"]
                        ),
                        end=float(
                            item["end"]
                        ),
                        text=str(
                            item["text"]
                        ),
                        speaker=str(
                            item.get(
                                "speaker",
                                "",
                            )
                        ),
                    )
                )

            subtitle_file = (
                self.subtitles.write_srt(
                    film_id,
                    subtitle_cues,
                    "fa",
                )
            )

            if not self.subtitles.validate(
                subtitle_file
            ):
                raise RuntimeError(
                    "Subtitle generation failed."
                )

            audio_files = [
                request.output_path
                for request in voice_requests
            ]

            if not audio_files:
                raise RuntimeError(
                    "No real voice files generated."
                )

            audio_video = (
                film_root
                / "audio_master.mp4"
            )

            self.mixer.mux(
                assembled,
                audio_files,
                audio_video,
            )

            final_movie = (
                film_root
                / "movie.mp4"
            )

            self.mixer.add_subtitle_track(
                audio_video,
                subtitle_file,
                final_movie,
                "fa",
            )

            final_duration = (
                self.ffprobe_duration(
                    final_movie
                )
            )

            if final_duration < (
                duration_seconds * 0.90
            ):
                raise RuntimeError(
                    "Final movie duration failed QC."
                )

            checksum = (
                self.checksum(
                    final_movie
                )
            )

            release = FinalFilmRelease(
                film_id=film_id,
                title=story.title,
                segments_expected=expected,
                segments_ready=len(
                    ready_segments
                ),
                video_ready=True,
                voice_ready=True,
                subtitle_ready=True,
                final_movie_ready=True,
                final_movie=str(
                    final_movie
                ),
                checksum=checksum,
            )

        except Exception as exc:

            release = FinalFilmRelease(
                film_id=film_id,
                title=story.title,
                segments_expected=expected,
                segments_ready=len(
                    ready_segments
                ),
                video_ready=False,
                voice_ready=False,
                subtitle_ready=False,
                final_movie_ready=False,
                final_movie=None,
                checksum=None,
                error=str(exc),
            )

        report = (
            film_root
            / "FINAL_RELEASE.json"
        )

        report.write_text(
            json.dumps(
                asdict(release),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return release
