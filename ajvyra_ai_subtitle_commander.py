from dataclasses import dataclass


@dataclass
class SubtitleInstruction:
    language: str
    text: str
    start: float
    end: float


class SubtitleCommander:

    SUPPORTED = {"en", "fa", "ja"}

    def validate_language(self, language: str) -> str:
        language = language.lower()

        if language not in self.SUPPORTED:
            raise ValueError(
                f"Unsupported subtitle language: {language}"
            )

        return language

    def create(
        self,
        language: str,
        text: str,
        start: float,
        end: float,
    ) -> SubtitleInstruction:

        self.validate_language(language)

        if end <= start:
            raise ValueError(
                "Subtitle end time must be greater than start time."
            )

        return SubtitleInstruction(
            language=language,
            text=text.strip(),
            start=float(start),
            end=float(end),
        )

    def build_tracks(
        self,
        dialogue: list[dict],
    ) -> dict[str, list[SubtitleInstruction]]:

        tracks = {
            "en": [],
            "fa": [],
            "ja": [],
        }

        for item in dialogue:
            start = float(item["start"])
            end = float(item["end"])

            for language in tracks:
                text = item.get(language)

                if text:
                    tracks[language].append(
                        self.create(
                            language,
                            text,
                            start,
                            end,
                        )
                    )

        return tracks
