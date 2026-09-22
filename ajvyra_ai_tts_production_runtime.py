from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import wave
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


ROOT = Path("ajvyra_projects")
TTS_ROOT = ROOT / "tts"
OUTPUT_ROOT = TTS_ROOT / "generated"
VOICE_ROOT = TTS_ROOT / "voices"
CONFIG_FILE = TTS_ROOT / "runtime.json"

OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
VOICE_ROOT.mkdir(parents=True, exist_ok=True)


@dataclass
class VoiceProfile:
    voice_id: str
    character_id: str
    language: str
    name: str
    gender: str = "unknown"
    emotion: str = "neutral"
    speed: float = 1.0
    pitch: float = 0.0


@dataclass
class TTSRequest:
    text: str
    language: str
    voice_id: str
    emotion: str = "neutral"
    speed: float = 1.0
    pitch: float = 0.0
    output_name: str = ""


@dataclass
class TTSResult:
    success: bool
    audio_path: str
    engine: str
    language: str
    voice_id: str
    error: str = ""


class TTSBackend:
    name = "base"

    def available(self) -> bool:
        return False

    def synthesize(
        self,
        request: TTSRequest,
        output_path: Path,
    ) -> TTSResult:
        raise NotImplementedError


class ESpeakBackend(TTSBackend):
    name = "espeak"

    def __init__(self) -> None:
        self.command = (
            shutil.which("espeak-ng")
            or shutil.which("espeak")
        )

    def available(self) -> bool:
        return self.command is not None

    def _language(self, language: str) -> str:
        mapping = {
            "fa": "fa",
            "ja": "ja",
            "en": "en",
        }

        return mapping.get(language, "en")

    def synthesize(
        self,
        request: TTSRequest,
        output_path: Path,
    ) -> TTSResult:

        if not self.available():
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="eSpeak is not installed.",
            )

        language = self._language(request.language)

        speed = max(
            80,
            min(
                450,
                int(175 * request.speed),
            ),
        )

        command = [
            self.command,
            "-v",
            language,
            "-s",
            str(speed),
            "-w",
            str(output_path),
            request.text,
        ]

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120,
            )

        except subprocess.TimeoutExpired:
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="TTS process timed out.",
            )

        if completed.returncode != 0:
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error=(
                    completed.stderr.strip()
                    or "TTS process failed."
                ),
            )

        if not output_path.exists():
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="TTS produced no audio file.",
            )

        return TTSResult(
            success=True,
            audio_path=str(output_path),
            engine=self.name,
            language=request.language,
            voice_id=request.voice_id,
        )


class MacOSSayBackend(TTSBackend):
    name = "macos_say"

    def __init__(self) -> None:
        self.command = shutil.which("say")

    def available(self) -> bool:
        return self.command is not None

    def synthesize(
        self,
        request: TTSRequest,
        output_path: Path,
    ) -> TTSResult:

        if not self.available():
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="macOS say is not available.",
            )

        temp_aiff = output_path.with_suffix(".aiff")

        rate = max(
            80,
            min(
                400,
                int(180 * request.speed),
            ),
        )

        command = [
            self.command,
            "-r",
            str(rate),
            "-o",
            str(temp_aiff),
            request.text,
        ]

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120,
            )

        except subprocess.TimeoutExpired:
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="macOS TTS process timed out.",
            )

        if completed.returncode != 0:
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error=(
                    completed.stderr.strip()
                    or "macOS TTS failed."
                ),
            )

        if not temp_aiff.exists():
            return TTSResult(
                success=False,
                audio_path="",
                engine=self.name,
                language=request.language,
                voice_id=request.voice_id,
                error="No AIFF file was produced.",
            )

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(temp_aiff),
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )

        except (subprocess.TimeoutExpired, FileNotFoundError):
            output_path.write_bytes(
                temp_aiff.read_bytes()
            )

        if temp_aiff.exists():
            temp_aiff.unlink()

        return TTSResult(
            success=output_path.exists(),
            audio_path=(
                str(output_path)
                if output_path.exists()
                else ""
            ),
            engine=self.name,
            language=request.language,
            voice_id=request.voice_id,
            error=(
                ""
                if output_path.exists()
                else "Audio conversion failed."
            ),
        )


class AJVYRAAIRealTTS:
    """
    Production TTS controller.

    The controller keeps the voice identity of every character
    separate and automatically chooses an available local
    synthesis backend.

    The architecture also allows a future neural TTS backend
    to be plugged in without changing the anime/game systems.
    """

    SUPPORTED_LANGUAGES = {
        "fa": "Persian",
        "ja": "Japanese",
        "en": "English",
    }

    def __init__(self) -> None:
        self.backends: list[TTSBackend] = [
            ESpeakBackend(),
            MacOSSayBackend(),
        ]

        self.voices: dict[str, VoiceProfile] = {}
        self._load_config()

    # ---------------------------------------------------------
    # Configuration
    # ---------------------------------------------------------

    def _load_config(self) -> None:
        if not CONFIG_FILE.exists():
            return

        try:
            data = json.loads(
                CONFIG_FILE.read_text(
                    encoding="utf-8"
                )
            )
        except (OSError, json.JSONDecodeError):
            return

        for raw in data.get("voices", []):
            try:
                profile = VoiceProfile(**raw)
                self.voices[profile.voice_id] = profile
            except TypeError:
                continue

    def _save_config(self) -> None:
        payload = {
            "languages": self.SUPPORTED_LANGUAGES,
            "voices": [
                asdict(voice)
                for voice in self.voices.values()
            ],
        }

        CONFIG_FILE.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # Voice identities
    # ---------------------------------------------------------

    def register_voice(
        self,
        voice_id: str,
        character_id: str,
        language: str,
        name: str,
        gender: str = "unknown",
        emotion: str = "neutral",
        speed: float = 1.0,
        pitch: float = 0.0,
    ) -> VoiceProfile:

        language = language.lower().strip()

        if language not in self.SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        if not voice_id.strip():
            raise ValueError(
                "voice_id cannot be empty."
            )

        profile = VoiceProfile(
            voice_id=voice_id,
            character_id=character_id,
            language=language,
            name=name,
            gender=gender,
            emotion=emotion,
            speed=speed,
            pitch=pitch,
        )

        self.voices[voice_id] = profile
        self._save_config()

        return profile

    def get_voice(
        self,
        voice_id: str,
    ) -> VoiceProfile:

        voice = self.voices.get(voice_id)

        if voice is None:
            raise KeyError(
                f"Unknown voice: {voice_id}"
            )

        return voice

    # ---------------------------------------------------------
    # Backend discovery
    # ---------------------------------------------------------

    def available_backends(self) -> list[str]:
        return [
            backend.name
            for backend in self.backends
            if backend.available()
        ]

    def _select_backend(self) -> Optional[TTSBackend]:
        for backend in self.backends:
            if backend.available():
                return backend

        return None

    # ---------------------------------------------------------
    # File naming
    # ---------------------------------------------------------

    @staticmethod
    def _safe_name(value: str) -> str:
        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789_-"
        )

        return "".join(
            char if char in allowed else "_"
            for char in value
        )

    def _output_path(
        self,
        request: TTSRequest,
    ) -> Path:

        name = (
            request.output_name.strip()
            or f"{request.voice_id}_speech"
        )

        name = self._safe_name(name)

        language_dir = (
            OUTPUT_ROOT /
            request.language
        )

        language_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return language_dir / f"{name}.wav"

    # ---------------------------------------------------------
    # Synthesis
    # ---------------------------------------------------------

    def synthesize(
        self,
        request: TTSRequest,
        force: bool = False,
    ) -> TTSResult:

        if not request.text.strip():
            return TTSResult(
                success=False,
                audio_path="",
                engine="none",
                language=request.language,
                voice_id=request.voice_id,
                error="Text is empty.",
            )

        voice = self.get_voice(
            request.voice_id
        )

        if voice.language != request.language:
            return TTSResult(
                success=False,
                audio_path="",
                engine="none",
                language=request.language,
                voice_id=request.voice_id,
                error=(
                    "Voice language does not match "
                    "the requested language."
                ),
            )

        output_path = self._output_path(
            request
        )

        if output_path.exists() and not force:
            return TTSResult(
                success=True,
                audio_path=str(output_path),
                engine="cache",
                language=request.language,
                voice_id=request.voice_id,
            )

        backend = self._select_backend()

        if backend is None:
            return TTSResult(
                success=False,
                audio_path="",
                engine="none",
                language=request.language,
                voice_id=request.voice_id,
                error=(
                    "No local TTS backend is installed."
                ),
            )

        merged_request = TTSRequest(
            text=request.text,
            language=request.language,
            voice_id=request.voice_id,
            emotion=(
                request.emotion
                or voice.emotion
            ),
            speed=(
                request.speed
                if request.speed != 1.0
                else voice.speed
            ),
            pitch=(
                request.pitch
                if request.pitch != 0.0
                else voice.pitch
            ),
            output_name=request.output_name,
        )

        return backend.synthesize(
            merged_request,
            output_path,
        )

    # ---------------------------------------------------------
    # Multilingual generation
    # ---------------------------------------------------------

    def synthesize_multilingual(
        self,
        texts: dict[str, str],
        voices: dict[str, str],
        base_name: str,
    ) -> dict[str, TTSResult]:

        results: dict[str, TTSResult] = {}

        for language, text in texts.items():

            if not text.strip():
                continue

            voice_id = voices.get(language)

            if not voice_id:
                results[language] = TTSResult(
                    success=False,
                    audio_path="",
                    engine="none",
                    language=language,
                    voice_id="",
                    error=(
                        f"No voice configured for {language}."
                    ),
                )
                continue

            request = TTSRequest(
                text=text,
                language=language,
                voice_id=voice_id,
                output_name=(
                    f"{base_name}_{language}"
                ),
            )

            results[language] = self.synthesize(
                request
            )

        return results

    # ---------------------------------------------------------
    # Character voice pack
    # ---------------------------------------------------------

    def create_character_voice_pack(
        self,
        character_id: str,
        character_name: str,
        voice_prefix: str,
    ) -> dict[str, str]:

        result: dict[str, str] = {}

        for language in (
            "fa",
            "ja",
            "en",
        ):
            voice_id = (
                f"{voice_prefix}_{language}"
            )

            self.register_voice(
                voice_id=voice_id,
                character_id=character_id,
                language=language,
                name=(
                    f"{character_name} "
                    f"{language.upper()}"
                ),
            )

            result[language] = voice_id

        return result

    # ---------------------------------------------------------
    # Episode dialogue generation
    # ---------------------------------------------------------

    def synthesize_dialogue_lines(
        self,
        lines: list[dict],
        output_prefix: str,
    ) -> list[dict]:

        generated: list[dict] = []

        for index, line in enumerate(lines, start=1):

            text = str(
                line.get("text", "")
            ).strip()

            language = str(
                line.get("language", "fa")
            ).lower()

            voice_id = str(
                line.get("voice_id", "")
            ).strip()

            if not text or not voice_id:
                generated.append(
                    {
                        "line": index,
                        "success": False,
                        "error": (
                            "text and voice_id "
                            "are required."
                        ),
                    }
                )
                continue

            request = TTSRequest(
                text=text,
                language=language,
                voice_id=voice_id,
                emotion=str(
                    line.get(
                        "emotion",
                        "neutral",
                    )
                ),
                speed=float(
                    line.get(
                        "speed",
                        1.0,
                    )
                ),
                pitch=float(
                    line.get(
                        "pitch",
                        0.0,
                    )
                ),
                output_name=(
                    f"{output_prefix}_"
                    f"{index:04d}"
                ),
            )

            result = self.synthesize(request)

            generated.append(
                {
                    "line": index,
                    "text": text,
                    "language": language,
                    "voice_id": voice_id,
                    **asdict(result),
                }
            )

        return generated

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def status(self) -> dict:
        return {
            "supported_languages": (
                self.SUPPORTED_LANGUAGES
            ),
            "registered_voices": len(
                self.voices
            ),
            "available_backends": (
                self.available_backends()
            ),
            "output_directory": str(
                OUTPUT_ROOT
            ),
            "neural_model_ready": False,
            "note": (
                "The runtime is ready for a trained "
                "neural TTS backend. Local fallback "
                "backends may produce synthetic speech."
            ),
        }


# -------------------------------------------------------------
# Global runtime
# -------------------------------------------------------------

AJVYRA_TTS_RUNTIME = AJVYRAAIRealTTS()


def register_character_voice(
    character_id: str,
    character_name: str,
    voice_prefix: str,
) -> dict[str, str]:

    return AJVYRA_TTS_RUNTIME.create_character_voice_pack(
        character_id=character_id,
        character_name=character_name,
        voice_prefix=voice_prefix,
    )


def speak(
    text: str,
    language: str,
    voice_id: str,
    output_name: str = "",
) -> TTSResult:

    return AJVYRA_TTS_RUNTIME.synthesize(
        TTSRequest(
            text=text,
            language=language,
            voice_id=voice_id,
            output_name=output_name,
        )
    )


def tts_status() -> dict:
    return AJVYRA_TTS_RUNTIME.status()


if __name__ == "__main__":

    print("=" * 60)
    print("AJVYRA AI TTS PRODUCTION RUNTIME")
    print("=" * 60)

    status = tts_status()

    print(
        "Languages:",
        ", ".join(
            status["supported_languages"].keys()
        ),
    )

    print(
        "Backends:",
        ", ".join(
            status["available_backends"]
        )
        or "none",
    )

    print(
        "Registered voices:",
        status["registered_voices"],
    )

    print(
        "Neural model ready:",
        status["neural_model_ready"],
    )

    print(
        "Output:",
        status["output_directory"],
    )
