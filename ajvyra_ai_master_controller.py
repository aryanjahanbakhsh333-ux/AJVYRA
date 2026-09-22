from ajvyra_ai_commander import AJVYRAAICommander
from ajvyra_ai_language_commander import LanguageCommander
from ajvyra_ai_voice_commander import VoiceCommander
from ajvyra_ai_subtitle_commander import SubtitleCommander
from ajvyra_ai_scene_commander import SceneCommander
from ajvyra_ai_episode_commander import EpisodeCommander
from ajvyra_ai_translation_memory import TranslationMemory
from ajvyra_ai_production_brain import ProductionBrain
from ajvyra_ai_media_orchestrator import MediaOrchestrator


class AJVYRAMasterAI:

    def __init__(self):

        self.commander = AJVYRAAICommander()

        self.languages = LanguageCommander()
        self.voices = VoiceCommander()
        self.subtitles = SubtitleCommander()
        self.scenes = SceneCommander()
        self.episodes = EpisodeCommander()

        self.translation_memory = (
            TranslationMemory()
        )

        self.brain = ProductionBrain(
            language_commander=self.languages,
            voice_commander=self.voices,
            subtitle_commander=self.subtitles,
        )

        self.media = MediaOrchestrator(
            production_brain=self.brain
        )

        self._register_modules()

    def _register_modules(self):

        self.commander.register(
            "language",
            self.languages,
        )

        self.commander.register(
            "voice",
            self.voices,
        )

        self.commander.register(
            "subtitle",
            self.subtitles,
        )

        self.commander.register(
            "scene",
            self.scenes,
        )

        self.commander.register(
            "episode",
            self.episodes,
        )

        self.commander.register(
            "production",
            self.brain,
        )

        self.commander.register(
            "media",
            self.media,
        )

    def attach_tts(self, tts_core):
        """
        موتور TTS داخلی AJVYRA را به مغز مرکزی معرفی می‌کند.
        """
        self.voices.attach_core(tts_core)

    def plan_anime(
        self,
        anime_id: int,
        scenes: list[dict],
    ) -> dict:

        audio = (
            self.languages.choose_audio_languages()
        )

        subtitles = (
            self.languages.choose_subtitle_languages()
        )

        decisions = []

        for scene in scenes:

            decision = self.brain.analyze_scene(
                anime_id=anime_id,
                scene=scene,
            )

            decisions.append(decision)

        return {
            "anime_id": anime_id,
            "audio_languages": audio,
            "subtitle_languages": subtitles,
            "subtitle_off": True,
            "scenes": decisions,
        }

    def status(self) -> dict:

        return {
            "ai_commander": self.commander.status(),
            "language_plan": self.languages.language_plan(),
            "tts_attached": self.voices.tts_core is not None,
            "systems": {
                "voice": "controlled",
                "languages": "controlled",
                "subtitles": "controlled",
                "scenes": "controlled",
                "episodes": "controlled",
                "media": "controlled",
            },
        }


MASTER_AI = AJVYRAMasterAI()


if __name__ == "__main__":

    print(
        "AJVYRA MASTER AI ONLINE"
    )

    print(
        MASTER_AI.status()
    )
