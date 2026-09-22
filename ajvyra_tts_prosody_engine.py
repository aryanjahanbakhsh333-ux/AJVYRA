from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Prosody:
    speaking_rate: float
    pitch_shift: float
    energy: float
    pause_scale: float


class ProsodyEngine:

    def analyze(
        self,
        text: str,
        emotion: str = "neutral",
    ) -> Prosody:

        punctuation_count = len(
            re.findall(r"[.!?,،؛:؟。！？、]", text)
        )

        length = max(len(text), 1)

        pause_scale = min(
            2.0,
            0.8 + punctuation_count / length * 8,
        )

        emotion_settings = {
            "neutral": (1.0, 0.0, 1.0),
            "happy": (1.08, 0.08, 1.10),
            "sad": (0.88, -0.08, 0.80),
            "angry": (1.08, 0.12, 1.25),
            "fear": (1.12, 0.10, 0.90),
            "calm": (0.86, -0.04, 0.75),
            "lonely": (0.82, -0.10, 0.65),
            "romantic": (0.92, -0.03, 0.82),
            "broken": (0.76, -0.14, 0.60),
            "whisper": (0.82, -0.05, 0.35),
            "crying": (0.78, -0.12, 0.70),
        }

        rate, pitch, energy = emotion_settings.get(
            emotion,
            emotion_settings["neutral"],
        )

        return Prosody(
            speaking_rate=rate,
            pitch_shift=pitch,
            energy=energy,
            pause_scale=pause_scale,
        )
