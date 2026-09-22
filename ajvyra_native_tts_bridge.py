from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from ajvyra_native_phoneme_speech import NativePhonemeSpeech
from ajvyra_native_formant_synthesizer import (
    NativeFormantSynthesizer,
    normalize,
)
from ajvyra_native_prosody_renderer import (
    NativeProsodyRenderer,
    ProsodySettings,
)


@dataclass
class NativeBridgeRequest:
    text: str
    language: str = "fa"
    emotion: str = "neutral"
    pitch: float = 180.0
    speed: float = 1.0
    energy: float = 1.0
    character_id: str = "default"
    output_name: str = "speech"


class NativeTTSBridge:
    """
    Connects the new phoneme/formant/prosody layers into
    the existing AJVYRA native audio engine.

    The bridge itself is independent and does not overwrite
    ajvyra_native_tts_engine.py.
    """

    def __init__(
        self,
        sample_rate: int = 22050,
        output_root: str = "ajvyra_projects/tts/bridge_audio",
    ):
        self.sample_rate = sample_rate
        self.output_root = Path(output_root)

        self.phonemes = NativePhonemeSpeech()
        self.formants = NativeFormantSynthesizer(sample_rate)
        self.prosody = NativeProsodyRenderer()

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def render(
        self,
        request: NativeBridgeRequest,
    ) -> Dict[str, Any]:

        if not request.text.strip():
            raise ValueError("Text cannot be empty.")

        language = request.language.lower().strip()

        phoneme_list = self.phonemes.analyze(
            request.text,
            language,
        )

        settings = ProsodySettings(
            base_pitch=max(60.0, request.pitch),
            speaking_rate=max(0.25, request.speed),
            energy=max(0.05, request.energy),
        )

        settings = self.prosody.emotion_settings(
            request.emotion,
        )

        pitch_curve = self.prosody.pitch_curve(
            len(phoneme_list),
            settings=settings,
            question=self.prosody.detect_question(
                request.text
            ),
            excited=self.prosody.detect_excited(
                request.text
            ),
        )

        samples: List[float] = []

        for index, phoneme in enumerate(phoneme_list):
            pitch = (
                pitch_curve[index]
                if index < len(pitch_curve)
                else settings.base_pitch
            )

            duration = (
                phoneme.duration
                / max(
                    0.25,
                    request.speed,
                )
            )

            rendered = self.formants.synthesize_phoneme(
                phoneme.symbol,
                duration,
                pitch,
                phoneme.energy * settings.energy,
            )

            samples.extend(rendered)

        samples = normalize(samples)

        output_path = (
            self.output_root
            / f"{request.output_name}.wav"
        )

        self._write_wav(
            output_path,
            samples,
        )

        return {
            "success": True,
            "path": str(output_path),
            "language": language,
            "emotion": request.emotion,
            "character_id": request.character_id,
            "phonemes": len(phoneme_list),
            "duration_seconds": round(
                len(samples) / self.sample_rate,
                3,
            ),
        }

    def _write_wav(
        self,
        path: Path,
        samples: List[float],
    ) -> None:

        import struct
        import wave

        pcm = b"".join(
            struct.pack(
                "<h",
                int(
                    max(-1.0, min(1.0, value))
                    * 32767
                ),
            )
            for value in samples
        )

        with wave.open(str(path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(pcm)


def create_native_voice(
    text: str,
    language: str = "fa",
    emotion: str = "neutral",
    output_name: str = "voice",
    character_id: str = "default",
) -> Dict[str, Any]:

    bridge = NativeTTSBridge()

    return bridge.render(
        NativeBridgeRequest(
            text=text,
            language=language,
            emotion=emotion,
            output_name=output_name,
            character_id=character_id,
        )
    )


if __name__ == "__main__":
    result = create_native_voice(
        text="صدای خاموش هنوز توی این شهر می‌مونه.",
        language="fa",
        emotion="sad",
        output_name="demo_bridge",
        character_id="character_01",
    )

    print(result)
