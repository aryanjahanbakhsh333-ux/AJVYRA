"""
AJVYRA Anime - Automatic TTS Engine
====================================

Central text-to-speech engine for the entire AJVYRA Anime system.

Responsibilities:
- Connect characters to their digital voice profiles.
- Support Persian and Japanese.
- Convert dialogue text into audio requests.
- Create per-character/per-language audio paths.
- Cache generated audio.
- Batch-generate dialogue.
- Automatically connect to the existing voice router.
- Provide a local-engine adapter.
- Keep the rest of AJVYRA independent from the actual TTS provider.

IMPORTANT:
This module is the orchestration layer.
A real TTS backend/model must exist for actual speech synthesis.
"""


from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib
import json
import shutil
import subprocess
import tempfile


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

ROOT = Path("anime_assets")
TTS_ROOT = ROOT / "tts"
CACHE_ROOT = TTS_ROOT / "cache"
OUTPUT_ROOT = TTS_ROOT / "generated"

SUPPORTED_LANGUAGES = ("fa", "ja")


# ---------------------------------------------------------------------------
# Language configuration
# ---------------------------------------------------------------------------

LANGUAGE_CONFIG = {
    "fa": {
        "name": "Persian",
        "locale": "fa-IR",
        "file_suffix": "fa",
    },
    "ja": {
        "name": "Japanese",
        "locale": "ja-JP",
        "file_suffix": "ja",
    },
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TTSRequest:
    anime_id: int
    character_id: str
    language: str
    text: str
    scene_number: int = 0
    dialogue_id: str = ""
    emotion: str = "neutral"


@dataclass(frozen=True)
class TTSResult:
    success: bool
    anime_id: int
    character_id: str
    language: str
    audio_path: str
    voice_id: str
    cached: bool
    engine: str
    error: str = ""


# ---------------------------------------------------------------------------
# Backend interface
# ---------------------------------------------------------------------------

class TTSBackend:
    """
    Base class for any real TTS provider or local model.
    """

    name = "base"

    def available(self) -> bool:
        return False

    def synthesize(
        self,
        text: str,
        language: str,
        voice_id: str,
        output_path: Path,
        emotion: str = "neutral",
    ) -> bool:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Local eSpeak backend
# ---------------------------------------------------------------------------

class ESpeakBackend(TTSBackend):
    """
    Lightweight local fallback.

    This is useful for testing the complete pipeline.
    It is NOT intended to be the final cinematic anime voice.
    """

    name = "espeak"

    def __init__(self):
        self.executable = self._find_executable()

    @staticmethod
    def _find_executable() -> Optional[str]:
        for command in ("espeak-ng", "espeak"):
            if shutil.which(command):
                return command

        return None

    def available(self) -> bool:
        return self.executable is not None

    def _voice_for_language(self, language: str) -> str:
        if language == "fa":
            # Availability depends on the installed eSpeak voices.
            return "fa"

        if language == "ja":
            return "ja"

        return language

    def synthesize(
        self,
        text: str,
        language: str,
        voice_id: str,
        output_path: Path,
        emotion: str = "neutral",
    ) -> bool:

        if not self.available():
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)

        voice = self._voice_for_language(language)

        command = [
            self.executable,
            "-v",
            voice,
            "-w",
            str(output_path),
            text,
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120,
            )

            return result.returncode == 0 and output_path.exists()

        except (
            subprocess.SubprocessError,
            OSError,
        ):
            return False


# ---------------------------------------------------------------------------
# Generic command backend
# ---------------------------------------------------------------------------

class CommandTTSBackend(TTSBackend):
    """
    Allows AJVYRA to use another installed/local TTS engine.

    The command template can contain:

        {text}
        {language}
        {voice_id}
        {output}
        {emotion}

    Example concept:

        some_tts_command --voice {voice_id} --text {text} --output {output}
    """

    name = "command"

    def __init__(
        self,
        command_template: List[str],
        executable: str,
    ):
        self.command_template = command_template
        self.executable = executable

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def synthesize(
        self,
        text: str,
        language: str,
        voice_id: str,
        output_path: Path,
        emotion: str = "neutral",
    ) -> bool:

        if not self.available():
            return False

        output_path.parent.mkdir(parents=True, exist_ok=True)

        values = {
            "text": text,
            "language": language,
            "voice_id": voice_id,
            "output": str(output_path),
            "emotion": emotion,
        }

        command = [
            part.format(**values)
            for part in self.command_template
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300,
            )

            return result.returncode == 0 and output_path.exists()

        except (
            subprocess.SubprocessError,
            OSError,
        ):
            return False


# ---------------------------------------------------------------------------
# Main AJVYRA TTS Engine
# ---------------------------------------------------------------------------

class AJVYRA_TTS:
    """
    Central TTS controller.

    Other AJVYRA modules should communicate with this class instead
    of communicating directly with an individual TTS engine.
    """

    def __init__(
        self,
        backend: Optional[TTSBackend] = None,
    ):
        self.backend = backend or ESpeakBackend()

        CACHE_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

        OUTPUT_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    @staticmethod
    def validate_language(language: str) -> str:
        language = language.lower().strip()

        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                "Unsupported language '{}'. "
                "Supported languages: {}".format(
                    language,
                    ", ".join(SUPPORTED_LANGUAGES),
                )
            )

        return language

    @staticmethod
    def validate_text(text: str) -> str:
        text = text.strip()

        if not text:
            raise ValueError("TTS text cannot be empty.")

        return text

    # -----------------------------------------------------------------------
    # Voice router integration
    # -----------------------------------------------------------------------

    @staticmethod
    def get_voice_profile(character_id: str) -> Dict[str, Any]:
        """
        Automatically reads the central AJVYRA voice router.
        """

        try:
            from ajvyra_anime_voice_router import get_voice

            return get_voice(character_id)

        except ImportError as exc:
            raise RuntimeError(
                "ajvyra_anime_voice_router.py is required."
            ) from exc

    # -----------------------------------------------------------------------
    # Cache
    # -----------------------------------------------------------------------

    @staticmethod
    def _cache_key(
        text: str,
        language: str,
        voice_id: str,
        emotion: str,
    ) -> str:

        raw = "|".join(
            [
                text,
                language,
                voice_id,
                emotion,
            ]
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

    def _cache_path(
        self,
        text: str,
        language: str,
        voice_id: str,
        emotion: str,
    ) -> Path:

        key = self._cache_key(
            text,
            language,
            voice_id,
            emotion,
        )

        return CACHE_ROOT / "{}.wav".format(key)

    # -----------------------------------------------------------------------
    # Output path
    # -----------------------------------------------------------------------

    def build_output_path(
        self,
        anime_id: int,
        character_id: str,
        language: str,
        dialogue_id: str,
    ) -> Path:

        language = self.validate_language(language)

        anime_folder = (
            OUTPUT_ROOT
            / "anime_{:02d}".format(anime_id)
            / language
        )

        anime_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        safe_dialogue_id = (
            dialogue_id.strip()
            if dialogue_id.strip()
            else "dialogue"
        )

        return (
            anime_folder
            / "{}_{}.wav".format(
                character_id,
                safe_dialogue_id,
            )
        )

    # -----------------------------------------------------------------------
    # Single synthesis
    # -----------------------------------------------------------------------

    def synthesize(
        self,
        request: TTSRequest,
    ) -> TTSResult:

        try:
            language = self.validate_language(
                request.language
            )

            text = self.validate_text(
                request.text
            )

            voice = self.get_voice_profile(
                request.character_id
            )

            voice_id = voice["voice_id"]

            output_path = self.build_output_path(
                anime_id=request.anime_id,
                character_id=request.character_id,
                language=language,
                dialogue_id=request.dialogue_id,
            )

            cache_path = self._cache_path(
                text=text,
                language=language,
                voice_id=voice_id,
                emotion=request.emotion,
            )

            # ---------------------------------------------------------------
            # Reuse cached audio
            # ---------------------------------------------------------------

            if cache_path.exists():

                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.copy2(
                    cache_path,
                    output_path,
                )

                return TTSResult(
                    success=True,
                    anime_id=request.anime_id,
                    character_id=request.character_id,
                    language=language,
                    audio_path=str(output_path),
                    voice_id=voice_id,
                    cached=True,
                    engine=self.backend.name,
                )

            # ---------------------------------------------------------------
            # Generate audio
            # ---------------------------------------------------------------

            success = self.backend.synthesize(
                text=text,
                language=language,
                voice_id=voice_id,
                output_path=output_path,
                emotion=request.emotion,
            )

            if not success:
                return TTSResult(
                    success=False,
                    anime_id=request.anime_id,
                    character_id=request.character_id,
                    language=language,
                    audio_path="",
                    voice_id=voice_id,
                    cached=False,
                    engine=self.backend.name,
                    error=(
                        "TTS backend could not synthesize audio. "
                        "Install/configure a supported TTS backend."
                    ),
                )

            # ---------------------------------------------------------------
            # Cache generated result
            # ---------------------------------------------------------------

            cache_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                output_path,
                cache_path,
            )

            return TTSResult(
                success=True,
                anime_id=request.anime_id,
                character_id=request.character_id,
                language=language,
                audio_path=str(output_path),
                voice_id=voice_id,
                cached=False,
                engine=self.backend.name,
            )

        except Exception as exc:

            return TTSResult(
                success=False,
                anime_id=request.anime_id,
                character_id=request.character_id,
                language=request.language,
                audio_path="",
                voice_id="",
                cached=False,
                engine=self.backend.name,
                error=str(exc),
            )

    # -----------------------------------------------------------------------
    # Batch synthesis
    # -----------------------------------------------------------------------

    def synthesize_batch(
        self,
        requests: List[TTSRequest],
    ) -> List[TTSResult]:

        results = []

        for request in requests:
            results.append(
                self.synthesize(request)
            )

        return results

    # -----------------------------------------------------------------------
    # Generate both languages automatically
    # -----------------------------------------------------------------------

    def synthesize_bilingual(
        self,
        anime_id: int,
        character_id: str,
        text_fa: str,
        text_ja: str,
        scene_number: int = 0,
        dialogue_id: str = "",
        emotion: str = "neutral",
    ) -> Dict[str, TTSResult]:

        requests = [
            TTSRequest(
                anime_id=anime_id,
                character_id=character_id,
                language="fa",
                text=text_fa,
                scene_number=scene_number,
                dialogue_id=dialogue_id,
                emotion=emotion,
            ),
            TTSRequest(
                anime_id=anime_id,
                character_id=character_id,
                language="ja",
                text=text_ja,
                scene_number=scene_number,
                dialogue_id=dialogue_id,
                emotion=emotion,
            ),
        ]

        results = self.synthesize_batch(requests)

        return {
            "fa": results[0],
            "ja": results[1],
        }

    # -----------------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------------

    def status(self) -> Dict[str, Any]:
        return {
            "engine": self.backend.name,
            "backend_available": self.backend.available(),
            "supported_languages": list(
                SUPPORTED_LANGUAGES
            ),
            "cache_directory": str(CACHE_ROOT),
            "output_directory": str(OUTPUT_ROOT),
        }


# ---------------------------------------------------------------------------
# Global engine
# ---------------------------------------------------------------------------

TTS_ENGINE = AJVYRA_TTS()


# ---------------------------------------------------------------------------
# Simple public API
# ---------------------------------------------------------------------------

def speak(
    anime_id: int,
    character_id: str,
    language: str,
    text: str,
    scene_number: int = 0,
    dialogue_id: str = "",
    emotion: str = "neutral",
) -> TTSResult:

    request = TTSRequest(
        anime_id=anime_id,
        character_id=character_id,
        language=language,
        text=text,
        scene_number=scene_number,
        dialogue_id=dialogue_id,
        emotion=emotion,
    )

    return TTS_ENGINE.synthesize(request)


def speak_both_languages(
    anime_id: int,
    character_id: str,
    text_fa: str,
    text_ja: str,
    scene_number: int = 0,
    dialogue_id: str = "",
    emotion: str = "neutral",
) -> Dict[str, TTSResult]:

    return TTS_ENGINE.synthesize_bilingual(
        anime_id=anime_id,
        character_id=character_id,
        text_fa=text_fa,
        text_ja=text_ja,
        scene_number=scene_number,
        dialogue_id=dialogue_id,
        emotion=emotion,
    )


def engine_status() -> Dict[str, Any]:
    return TTS_ENGINE.status()


# ---------------------------------------------------------------------------
# Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("AJVYRA AUTOMATIC TTS ENGINE")
    print("=" * 60)

    print(
        json.dumps(
            engine_status(),
            indent=2,
            ensure_ascii=False,
        )
    )

    example = TTSRequest(
        anime_id=1,
        character_id="A01-C01",
        language="fa",
        text="من این صدا رو قبلاً شنیدم...",
        scene_number=1,
        dialogue_id="A01-S01-D01",
        emotion="fear",
    )

    result = TTS_ENGINE.synthesize(example)

    print("\nResult:")
    print(
        json.dumps(
            asdict(result),
            indent=2,
            ensure_ascii=False,
        )
    )
