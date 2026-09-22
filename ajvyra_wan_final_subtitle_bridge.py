from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FinalSubtitleCue:
    start: float
    end: float
    text: str
    speaker: str = ""


class AJVYRAFinalSubtitleBridge:

    def __init__(
        self,
        root: str | Path = "ajvyra_final_subtitles",
    ):

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _timestamp(
        seconds: float,
    ) -> str:

        milliseconds = int(
            round(seconds * 1000)
        )

        hours = milliseconds // 3_600_000
        milliseconds %= 3_600_000

        minutes = milliseconds // 60_000
        milliseconds %= 60_000

        seconds_int = milliseconds // 1000
        milliseconds %= 1000

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{seconds_int:02d},"
            f"{milliseconds:03d}"
        )

    def write_srt(
        self,
        film_id: str,
        cues: list[FinalSubtitleCue],
        language: str,
    ) -> Path:

        output = (
            self.root
            / film_id
            / f"{language}.srt"
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        blocks = []

        for index, cue in enumerate(
            cues,
            start=1,
        ):

            speaker = (
                f"{cue.speaker}: "
                if cue.speaker
                else ""
            )

            blocks.append(
                f"{index}\n"
                f"{self._timestamp(cue.start)} --> "
                f"{self._timestamp(cue.end)}\n"
                f"{speaker}{cue.text}\n"
            )

        output.write_text(
            "\n".join(blocks),
            encoding="utf-8",
        )

        return output

    def load_dialogue_script(
        self,
        path: str | Path,
    ) -> list[FinalSubtitleCue]:

        data = json.loads(
            Path(path).read_text(
                encoding="utf-8"
            )
        )

        cues = []

        for item in data:

            cues.append(
                FinalSubtitleCue(
                    start=float(item["start"]),
                    end=float(item["end"]),
                    text=str(item["text"]),
                    speaker=str(
                        item.get(
                            "speaker",
                            "",
                        )
                    ),
                )
            )

        return cues

    def validate(
        self,
        path: str | Path,
    ) -> bool:

        path = Path(path)

        if not path.exists():
            return False

        text = path.read_text(
            encoding="utf-8"
        ).strip()

        return bool(text)
