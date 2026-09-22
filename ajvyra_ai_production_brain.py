from dataclasses import dataclass, field


@dataclass
class ProductionDecision:
    scene_id: str
    voice_jobs: list[dict] = field(default_factory=list)
    subtitle_jobs: list[dict] = field(default_factory=list)
    status: str = "planned"


class ProductionBrain:

    def __init__(
        self,
        language_commander,
        voice_commander,
        subtitle_commander,
    ):
        self.languages = language_commander
        self.voices = voice_commander
        self.subtitles = subtitle_commander

    def analyze_scene(
        self,
        anime_id: int,
        scene: dict,
    ) -> ProductionDecision:

        audio_languages = (
            self.languages.choose_audio_languages()
        )

        subtitle_languages = (
            self.languages.choose_subtitle_languages()
        )

        scene_id = scene["scene_id"]

        voice_jobs = []

        for language in audio_languages:
            voice_jobs.append({
                "anime_id": anime_id,
                "scene_id": scene_id,
                "character_id": scene["character_id"],
                "language": language,
                "text": scene["dialogue"],
                "emotion": scene.get(
                    "emotion",
                    "neutral",
                ),
            })

        subtitle_jobs = []

        for language in subtitle_languages:
            text = scene.get(language)

            if text:
                subtitle_jobs.append({
                    "scene_id": scene_id,
                    "language": language,
                    "text": text,
                })

        return ProductionDecision(
            scene_id=scene_id,
            voice_jobs=voice_jobs,
            subtitle_jobs=subtitle_jobs,
            status="ready",
        )
