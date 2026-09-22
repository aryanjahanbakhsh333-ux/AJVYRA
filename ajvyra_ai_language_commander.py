from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageProfile:
    code: str
    name: str
    enabled: bool = True


class LanguageCommander:

    SUPPORTED = {
        "fa": LanguageProfile("fa", "Persian"),
        "ja": LanguageProfile("ja", "Japanese"),
        "en": LanguageProfile("en", "English"),
    }

    def validate(self, language: str) -> LanguageProfile:
        language = language.lower().strip()

        if language not in self.SUPPORTED:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        return self.SUPPORTED[language]

    def choose_audio_languages(
        self,
        requested: list[str] | None = None,
    ) -> list[str]:

        if requested is None:
            requested = ["fa", "ja"]

        return [
            self.validate(language).code
            for language in requested
        ]

    def choose_subtitle_languages(
        self,
        requested: list[str] | None = None,
    ) -> list[str]:

        if requested is None:
            requested = ["en", "fa", "ja"]

        return [
            self.validate(language).code
            for language in requested
        ]

    def language_plan(self) -> dict:
        return {
            "audio": ["fa", "ja"],
            "subtitles": ["en", "fa", "ja"],
            "subtitle_off": True,
        }
