"""
AJVYRA CINEMATIC AUDIO TIMELINE
-------------------------------
Film-level audio timeline.

Supports:
- dialogue
- voice identity
- music
- ambience
- SFX
- silence
- language tracks
- overlap
- fades
- ducking
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List


@dataclass
class AudioClip:
    clip_id: str
    track_type: str

    start: float
    duration: float

    source: str

    language: str = ""
    character_id: str = ""

    volume: float = 1.0

    fade_in: float = 0.0
    fade_out: float = 0.0

    emotion: str = ""

    metadata: Dict = field(
        default_factory=dict
    )


@dataclass
class AudioTimeline:
    duration: float

    clips: List[
        AudioClip
    ] = field(default_factory=list)

    language_tracks: Dict[
        str,
        List[str]
    ] = field(default_factory=dict)


class AJVYRACinematicAudioTimeline:
    VERSION = "1.0.0"

    TRACK_TYPES = {
        "dialogue",
        "music",
        "ambience",
        "sfx",
        "silence",
    }

    def __init__(
        self,
        duration: float,
    ) -> None:
        if duration <= 0:
            raise ValueError(
                "Audio duration must be positive."
            )

        self.timeline = AudioTimeline(
            duration=float(duration)
        )

    def add(
        self,
        track_type: str,
        start: float,
        duration: float,
        source: str,
        language: str = "",
        character_id: str = "",
        volume: float = 1.0,
        fade_in: float = 0.0,
        fade_out: float = 0.0,
        emotion: str = "",
        metadata: Dict | None = None,
    ) -> AudioClip:

        if track_type not in self.TRACK_TYPES:
            raise ValueError(
                f"Unsupported audio track: "
                f"{track_type}"
            )

        if start < 0:
            raise ValueError(
                "Audio start cannot be negative."
            )

        if duration <= 0:
            raise ValueError(
                "Audio duration must be positive."
            )

        end = start + duration

        if end > self.timeline.duration + 0.001:
            raise ValueError(
                f"Audio clip exceeds film duration: "
                f"{end:.2f}s > "
                f"{self.timeline.duration:.2f}s"
            )

        clip = AudioClip(
            clip_id=uuid.uuid4().hex,
            track_type=track_type,
            start=float(start),
            duration=float(duration),
            source=source,
            language=language,
            character_id=character_id,
            volume=max(
                0.0,
                min(2.0, volume),
            ),
            fade_in=max(
                0.0,
                min(duration / 2, fade_in),
            ),
            fade_out=max(
                0.0,
                min(duration / 2, fade_out),
            ),
            emotion=emotion,
            metadata=metadata or {},
        )

        self.timeline.clips.append(
            clip
        )

        if language:
            self.timeline.language_tracks.setdefault(
                language,
                [],
            ).append(
                clip.clip_id
            )

        return clip

    def add_dialogue(
        self,
        start: float,
        duration: float,
        audio_path: str,
        language: str,
        character_id: str,
        emotion: str,
        volume: float = 1.0,
    ) -> AudioClip:
        return self.add(
            track_type="dialogue",
            start=start,
            duration=duration,
            source=audio_path,
            language=language,
            character_id=character_id,
            emotion=emotion,
            volume=volume,
        )

    def add_music(
        self,
        start: float,
        duration: float,
        audio_path: str,
        energy: float = 0.5,
    ) -> AudioClip:
        return self.add(
            track_type="music",
            start=start,
            duration=duration,
            source=audio_path,
            volume=0.30 + (
                max(
                    0.0,
                    min(1.0, energy)
                ) * 0.40
            ),
            fade_in=1.5,
            fade_out=2.0,
        )

    def add_ambience(
        self,
        start: float,
        duration: float,
        audio_path: str,
        volume: float = 0.25,
    ) -> AudioClip:
        return self.add(
            track_type="ambience",
            start=start,
            duration=duration,
            source=audio_path,
            volume=volume,
            fade_in=1.0,
            fade_out=1.0,
        )

    def add_sfx(
        self,
        start: float,
        duration: float,
        audio_path: str,
        volume: float = 0.7,
    ) -> AudioClip:
        return self.add(
            track_type="sfx",
            start=start,
            duration=duration,
            source=audio_path,
            volume=volume,
        )

    def validate(
        self,
    ) -> List[str]:
        errors: List[str] = []

        for clip in self.timeline.clips:
            if clip.start < 0:
                errors.append(
                    f"{clip.clip_id}: negative start"
                )

            if clip.duration <= 0:
                errors.append(
                    f"{clip.clip_id}: invalid duration"
                )

            if (
                clip.start + clip.duration
                > self.timeline.duration + 0.001
            ):
                errors.append(
                    f"{clip.clip_id}: exceeds timeline"
                )

            if not clip.source.strip():
                errors.append(
                    f"{clip.clip_id}: missing source"
                )

        return errors

    def language_timeline(
        self,
        language: str,
    ) -> List[AudioClip]:
        ids = set(
            self.timeline.language_tracks.get(
                language,
                [],
            )
        )

        return [
            clip
            for clip in self.timeline.clips
            if clip.clip_id in ids
        ]

    def export(
        self,
        path: str | Path,
    ) -> Path:
        target = Path(path)

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                {
                    "version": self.VERSION,
                    "timeline": asdict(
                        self.timeline
                    ),
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


if __name__ == "__main__":
    timeline = (
        AJVYRACinematicAudioTimeline(
            duration=1800
        )
    )

    timeline.add_dialogue(
        start=14.2,
        duration=3.4,
        audio_path=(
            "audio/fa/vey_01_001.wav"
        ),
        language="fa",
        character_id="vey_01",
        emotion="sadness",
    )

    timeline.add_dialogue(
        start=14.2,
        duration=3.4,
        audio_path=(
            "audio/ja/vey_01_001.wav"
        ),
        language="ja",
        character_id="vey_01",
        emotion="sadness",
    )

    timeline.add_ambience(
        start=0,
        duration=1800,
        audio_path="audio/rain_harbor.wav",
    )

    timeline.add_music(
        start=8,
        duration=45,
        audio_path="music/scene_01.wav",
        energy=0.25,
    )

    errors = timeline.validate()

    if errors:
        raise RuntimeError(
            "\n".join(errors)
        )

    timeline.export(
        "generated/cinematic/veyllora/"
        "audio_timeline.json"
    )

    print("Audio timeline ready.")
