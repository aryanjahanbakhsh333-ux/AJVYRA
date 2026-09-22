from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


@dataclass
class SubtitleCue:
    start: float
    end: float
    text: str

    def validate(self) -> None:
        if self.start < 0:
            raise ValueError(
                "Subtitle start cannot be negative."
            )

        if self.end <= self.start:
            raise ValueError(
                "Subtitle end must be after start."
            )

        if not self.text.strip():
            raise ValueError(
                "Subtitle text cannot be empty."
            )


class AJVYRACinematicSubtitleEngine:

    def __init__(self):
        self.tracks: Dict[
            str,
            List[SubtitleCue]
        ] = {}

    def add_track(
        self,
        language: str,
        cues: List[SubtitleCue],
    ) -> None:

        normalized = language.lower().strip()

        if not normalized:
            raise ValueError(
                "Language cannot be empty."
            )

        for cue in cues:
            cue.validate()

        ordered = sorted(
            cues,
            key=lambda cue: cue.start,
        )

        for previous, current in zip(
            ordered,
            ordered[1:],
        ):
            if current.start < previous.end:
                raise ValueError(
                    f"Overlapping subtitles in {normalized}."
                )

        self.tracks[
            normalized
        ] = ordered

    def export_srt(
        self,
        language: str,
        output_path: str | Path,
    ) -> Path:

        language = language.lower()

        cues = self.tracks.get(
            language,
            [],
        )

        target = Path(output_path)

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        lines = []

        for index, cue in enumerate(
            cues,
            start=1,
        ):
            lines.extend(
                [
                    str(index),
                    (
                        f"{self._format_srt_time(cue.start)}"
                        " --> "
                        f"{self._format_srt_time(cue.end)}"
                    ),
                    cue.text.strip(),
                    "",
                ]
            )

        target.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return target

    def export_vtt(
        self,
        language: str,
        output_path: str | Path,
    ) -> Path:

        language = language.lower()

        cues = self.tracks.get(
            language,
            [],
        )

        target = Path(output_path)

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        lines = ["WEBVTT", ""]

        for cue in cues:
            lines.extend(
                [
                    (
                        f"{self._format_vtt_time(cue.start)}"
                        " --> "
                        f"{self._format_vtt_time(cue.end)}"
                    ),
                    html.escape(
                        cue.text.strip()
                    ),
                    "",
                ]
            )

        target.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        return target

    def export_all(
        self,
        output_directory: str | Path,
        format: str = "srt",
    ) -> List[Path]:

        output = Path(output_directory)
        output.mkdir(
            parents=True,
            exist_ok=True,
        )

        created = []

        for language in self.tracks:

            if format.lower() == "vtt":
                created.append(
                    self.export_vtt(
                        language,
                        output
                        / f"{language}.vtt",
                    )
                )
            else:
                created.append(
                    self.export_srt(
                        language,
                        output
                        / f"{language}.srt",
                    )
                )

        return created

    @staticmethod
    def _format_srt_time(
        seconds: float,
    ) -> str:

        milliseconds = int(
            round(seconds * 1000)
        )

        hours = milliseconds // 3_600_000
        milliseconds %= 3_600_000

        minutes = milliseconds // 60_000
        milliseconds %= 60_000

        secs = milliseconds // 1000
        milliseconds %= 1000

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d},"
            f"{milliseconds:03d}"
        )

    @staticmethod
    def _format_vtt_time(
        seconds: float,
    ) -> str:

        value = (
            AJVYRACinematicSubtitleEngine
            ._format_srt_time(seconds)
        )

        return value.replace(",", ".")
