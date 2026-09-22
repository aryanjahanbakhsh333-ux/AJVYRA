from __future__ import annotations

import math
import struct
import wave
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("ajvyra_projects")
TTS_ROOT = ROOT / "tts"
AUDIO_ROOT = TTS_ROOT / "native_audio"

SAMPLE_RATE = 44100


@dataclass
class VoiceStyle:
    voice_id: str
    language: str
    base_frequency: float
    brightness: float = 0.5
    breath: float = 0.04
    roughness: float = 0.02
    speed: float = 1.0


@dataclass
class SpeechRequest:
    text: str
    language: str
    voice_id: str
    output_name: str
    emotion: str = "neutral"
    speed: float = 1.0


class NativeSpeechSynthesizer:
    """
    AJVYRA's independent algorithmic speech synthesizer.

    This engine does NOT require:
        - an external TTS API
        - a commercial voice provider
        - a pretrained TTS model

    It generates actual WAV audio directly with DSP algorithms.

    The result is synthetic/stylized speech rather than
    human-realistic speech. It is designed for anime/game
    characters and can be improved independently over time.
    """

    LANGUAGE_DEFAULTS = {
        "fa": 145.0,
        "ja": 165.0,
        "en": 150.0,
    }

    EMOTION_MAP = {
        "neutral": {
            "pitch": 1.00,
            "energy": 1.00,
            "roughness": 1.00,
        },
        "sad": {
            "pitch": 0.88,
            "energy": 0.72,
            "roughness": 0.85,
        },
        "angry": {
            "pitch": 1.15,
            "energy": 1.25,
            "roughness": 1.70,
        },
        "happy": {
            "pitch": 1.12,
            "energy": 1.12,
            "roughness": 0.90,
        },
        "fear": {
            "pitch": 1.25,
            "energy": 0.78,
            "roughness": 1.35,
        },
        "whisper": {
            "pitch": 0.96,
            "energy": 0.42,
            "roughness": 0.65,
        },
        "cold": {
            "pitch": 0.90,
            "energy": 0.78,
            "roughness": 0.72,
        },
        "excited": {
            "pitch": 1.28,
            "energy": 1.30,
            "roughness": 1.10,
        },
    }

    def __init__(self) -> None:
        AUDIO_ROOT.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.voices: dict[str, VoiceStyle] = {}

    # ---------------------------------------------------------
    # Voice creation
    # ---------------------------------------------------------

    def create_voice(
        self,
        voice_id: str,
        language: str,
        base_frequency: float | None = None,
        brightness: float = 0.5,
        breath: float = 0.04,
        roughness: float = 0.02,
        speed: float = 1.0,
    ) -> VoiceStyle:

        language = language.lower()

        if language not in self.LANGUAGE_DEFAULTS:
            raise ValueError(
                f"Unsupported language: {language}"
            )

        voice = VoiceStyle(
            voice_id=voice_id,
            language=language,
            base_frequency=(
                base_frequency
                if base_frequency is not None
                else self.LANGUAGE_DEFAULTS[language]
            ),
            brightness=max(
                0.0,
                min(1.0, brightness),
            ),
            breath=max(
                0.0,
                min(1.0, breath),
            ),
            roughness=max(
                0.0,
                min(1.0, roughness),
            ),
            speed=max(
                0.25,
                min(3.0, speed),
            ),
        )

        self.voices[voice_id] = voice

        return voice

    def get_voice(
        self,
        voice_id: str,
    ) -> VoiceStyle:

        if voice_id not in self.voices:
            raise KeyError(
                f"Voice '{voice_id}' does not exist."
            )

        return self.voices[voice_id]

    # ---------------------------------------------------------
    # Language phonetic approximation
    # ---------------------------------------------------------

    @staticmethod
    def _clean_text(text: str) -> str:
        return " ".join(
            text.replace("\n", " ").split()
        )

    @staticmethod
    def _character_weight(
        character: str,
    ) -> float:

        vowels = (
            "aeiou"
            "آاوی"
            "アイウエオ"
            "あいうえお"
        )

        if character.lower() in vowels:
            return 1.25

        if character.isspace():
            return 0.35

        if character in ".,!?؛،":
            return 0.15

        return 1.0

    def _phonetic_units(
        self,
        text: str,
        language: str,
    ) -> list[tuple[str, float]]:

        text = self._clean_text(text)

        units: list[tuple[str, float]] = []

        for character in text:

            weight = self._character_weight(
                character
            )

            if language == "ja":
                weight *= 1.05

            elif language == "fa":
                weight *= 1.08

            elif language == "en":
                weight *= 0.96

            units.append(
                (character, weight)
            )

        return units

    # ---------------------------------------------------------
    # DSP primitives
    # ---------------------------------------------------------

    @staticmethod
    def _clamp(
        value: float,
        minimum: float = -1.0,
        maximum: float = 1.0,
    ) -> float:

        return max(
            minimum,
            min(maximum, value),
        )

    @staticmethod
    def _soft_clip(
        value: float,
    ) -> float:

        return math.tanh(value)

    @staticmethod
    def _envelope(
        position: float,
    ) -> float:

        position = max(
            0.0,
            min(1.0, position),
        )

        attack = min(
            0.16,
            position * 2.5,
        )

        release = min(
            0.20,
            (1.0 - position) * 3.0,
        )

        return min(
            1.0,
            attack,
            release,
        )

    def _voice_wave(
        self,
        frequency: float,
        duration: float,
        style: VoiceStyle,
        emotion: dict,
    ) -> list[float]:

        count = max(
            1,
            int(duration * SAMPLE_RATE),
        )

        samples: list[float] = []

        phase = 0.0

        for index in range(count):

            t = index / SAMPLE_RATE

            phase += (
                2.0
                * math.pi
                * frequency
                / SAMPLE_RATE
            )

            harmonic_1 = math.sin(phase)

            harmonic_2 = (
                math.sin(phase * 2.0)
                * (0.42 + style.brightness * 0.30)
            )

            harmonic_3 = (
                math.sin(phase * 3.0)
                * (0.18 + style.brightness * 0.20)
            )

            harmonic_4 = (
                math.sin(phase * 4.0)
                * style.brightness
                * 0.10
            )

            rough = (
                math.sin(
                    phase * 7.0
                    + math.sin(t * 4.0) * 0.7
                )
                * style.roughness
                * emotion["roughness"]
            )

            signal = (
                harmonic_1
                + harmonic_2
                + harmonic_3
                + harmonic_4
                + rough
            )

            breath = (
                math.sin(
                    t * 1371.0
                    + math.sin(t * 7.0)
                )
                * style.breath
            )

            signal += breath

            signal *= emotion["energy"]

            samples.append(
                self._soft_clip(signal)
            )

        return samples

    # ---------------------------------------------------------
    # Prosody
    # ---------------------------------------------------------

    def _frequency_curve(
        self,
        base: float,
        emotion: dict,
        index: int,
        total: int,
    ) -> float:

        progress = (
            index / max(1, total - 1)
        )

        natural_variation = (
            math.sin(progress * math.pi * 2.4)
            * 0.035
        )

        sentence_shape = (
            math.sin(progress * math.pi)
            * 0.055
        )

        return (
            base
            * emotion["pitch"]
            * (
                1.0
                + natural_variation
                + sentence_shape
            )
        )

    # ---------------------------------------------------------
    # Silence
    # ---------------------------------------------------------

    @staticmethod
    def _silence(
        duration: float,
    ) -> list[float]:

        return [
            0.0
            for _ in range(
                max(
                    1,
                    int(
                        duration
                        * SAMPLE_RATE
                    ),
                )
            )
        ]

    # ---------------------------------------------------------
    # Generate speech
    # ---------------------------------------------------------

    def synthesize(
        self,
        request: SpeechRequest,
    ) -> Path:

        voice = self.get_voice(
            request.voice_id
        )

        if voice.language != request.language:
            raise ValueError(
                "Voice language and request language "
                "must match."
            )

        emotion = self.EMOTION_MAP.get(
            request.emotion.lower(),
            self.EMOTION_MAP["neutral"],
        )

        units = self._phonetic_units(
            request.text,
            request.language,
        )

        speed = max(
            0.25,
            min(
                3.0,
                request.speed * voice.speed,
            ),
        )

        samples: list[float] = []

        non_space_count = max(
            1,
            sum(
                not character.isspace()
                for character, _ in units
            ),
        )

        character_index = 0

        for character, weight in units:

            if character.isspace():
                samples.extend(
                    self._silence(
                        0.045 / speed
                    )
                )
                continue

            if character in ".,!?؛،":
                samples.extend(
                    self._silence(
                        0.12 / speed
                    )
                )
                continue

            base_duration = (
                0.075
                * weight
                / speed
            )

            frequency = self._frequency_curve(
                voice.base_frequency,
                emotion,
                character_index,
                non_space_count,
            )

            character_index += 1

            tone = self._voice_wave(
                frequency=frequency,
                duration=base_duration,
                style=voice,
                emotion=emotion,
            )

            envelope_length = len(tone)

            for i in range(
                envelope_length
            ):

                position = (
                    i
                    / max(
                        1,
                        envelope_length - 1,
                    )
                )

                tone[i] *= self._envelope(
                    position
                )

            samples.extend(tone)

        if not samples:
            raise ValueError(
                "Text produced no speech samples."
            )

        samples = self._normalize(
            samples
        )

        output = (
            AUDIO_ROOT
            / f"{request.output_name}.wav"
        )

        self._write_wav(
            output,
            samples,
        )

        return output

    # ---------------------------------------------------------
    # Audio processing
    # ---------------------------------------------------------

    @staticmethod
    def _normalize(
        samples: list[float],
    ) -> list[float]:

        peak = max(
            abs(sample)
            for sample in samples
        )

        if peak <= 0.000001:
            return samples

        gain = 0.88 / peak

        return [
            NativeSpeechSynthesizer._clamp(
                sample * gain
            )
            for sample in samples
        ]

    @staticmethod
    def _write_wav(
        path: Path,
        samples: list[float],
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        pcm = bytearray()

        for sample in samples:

            value = int(
                NativeSpeechSynthesizer._clamp(
                    sample
                )
                * 32767
            )

            pcm.extend(
                struct.pack(
                    "<h",
                    value,
                )
            )

        with wave.open(
            str(path),
            "wb",
        ) as wav:

            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(
                SAMPLE_RATE
            )
            wav.writeframes(pcm)

    # ---------------------------------------------------------
    # Anime / game integration
    # ---------------------------------------------------------

    def generate_character_line(
        self,
        character_id: str,
        text: str,
        language: str,
        emotion: str,
        output_name: str,
    ) -> Path:

        voice_id = (
            f"{character_id}_{language}"
        )

        if voice_id not in self.voices:

            self.create_voice(
                voice_id=voice_id,
                language=language,
            )

        return self.synthesize(
            SpeechRequest(
                text=text,
                language=language,
                voice_id=voice_id,
                output_name=output_name,
                emotion=emotion,
            )
        )

    def generate_multilingual_line(
        self,
        character_id: str,
        texts: dict[str, str],
        emotion: str,
        output_prefix: str,
    ) -> dict[str, str]:

        result: dict[str, str] = {}

        for language, text in texts.items():

            path = self.generate_character_line(
                character_id=character_id,
                text=text,
                language=language,
                emotion=emotion,
                output_name=(
                    f"{output_prefix}_{language}"
                ),
            )

            result[language] = str(path)

        return result

    # ---------------------------------------------------------
    # Batch generation
    # ---------------------------------------------------------

    def generate_batch(
        self,
        lines: list[SpeechRequest],
    ) -> list[dict]:

        results: list[dict] = []

        for request in lines:

            try:
                path = self.synthesize(
                    request
                )

                results.append(
                    {
                        "success": True,
                        "voice_id": request.voice_id,
                        "language": request.language,
                        "emotion": request.emotion,
                        "audio": str(path),
                    }
                )

            except Exception as exc:

                results.append(
                    {
                        "success": False,
                        "voice_id": request.voice_id,
                        "language": request.language,
                        "emotion": request.emotion,
                        "audio": "",
                        "error": str(exc),
                    }
                )

        return results


# -------------------------------------------------------------
# Global AJVYRA native voice engine
# -------------------------------------------------------------

AJVYRA_NATIVE_TTS = NativeSpeechSynthesizer()


def create_voice(
    voice_id: str,
    language: str,
    base_frequency: float | None = None,
    brightness: float = 0.5,
    breath: float = 0.04,
    roughness: float = 0.02,
) -> VoiceStyle:

    return AJVYRA_NATIVE_TTS.create_voice(
        voice_id=voice_id,
        language=language,
        base_frequency=base_frequency,
        brightness=brightness,
        breath=breath,
        roughness=roughness,
    )


def speak(
    text: str,
    language: str,
    voice_id: str,
    output_name: str,
    emotion: str = "neutral",
) -> str:

    path = AJVYRA_NATIVE_TTS.synthesize(
        SpeechRequest(
            text=text,
            language=language,
            voice_id=voice_id,
            output_name=output_name,
            emotion=emotion,
        )
    )

    return str(path)


if __name__ == "__main__":

    print("=" * 60)
    print("AJVYRA NATIVE TTS")
    print("=" * 60)

    engine = AJVYRA_NATIVE_TTS

    engine.create_voice(
        voice_id="demo_fa",
        language="fa",
        base_frequency=145.0,
        brightness=0.58,
        breath=0.035,
        roughness=0.025,
    )

    output = engine.synthesize(
        SpeechRequest(
            text="این صدای ساخته شده توسط موتور صوتی AJVYRA است.",
            language="fa",
            voice_id="demo_fa",
            output_name="ajvyra_demo_fa",
            emotion="cold",
        )
    )

    print("Audio created:")
    print(output)
    print("Sample rate:", SAMPLE_RATE)
