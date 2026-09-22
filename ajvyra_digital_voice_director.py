from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DirectedVoice:
    text: str
    emotion: str

    speed: float
    pitch: float
    energy: float

    delivery_instruction: str


class AJVYRADigitalVoiceDirector:

    EMOTIONS = {
        "calm": {
            "speed": 0.95,
            "pitch": -0.5,
            "energy": 0.80,
            "delivery": (
                "quiet, controlled, intimate cinematic delivery"
            ),
        },
        "sad": {
            "speed": 0.88,
            "pitch": -1.0,
            "energy": 0.60,
            "delivery": (
                "fragile, restrained sadness"
            ),
        },
        "angry": {
            "speed": 1.08,
            "pitch": 0.5,
            "energy": 1.45,
            "delivery": (
                "controlled anger with strong intensity"
            ),
        },
        "fear": {
            "speed": 1.12,
            "pitch": 1.0,
            "energy": 1.15,
            "delivery": (
                "tense and frightened delivery"
            ),
        },
        "cold": {
            "speed": 0.86,
            "pitch": -1.5,
            "energy": 0.65,
            "delivery": (
                "emotionally distant and cold"
            ),
        },
        "excited": {
            "speed": 1.12,
            "pitch": 1.0,
            "energy": 1.35,
            "delivery": (
                "energetic cinematic performance"
            ),
        },
        "whisper": {
            "speed": 0.82,
            "pitch": -1.0,
            "energy": 0.35,
            "delivery": (
                "very quiet intimate delivery"
            ),
        },
    }

    def direct(
        self,
        text: str,
        emotion: str,
        base_speed: float = 1.0,
        base_pitch: float = 0.0,
        base_energy: float = 1.0,
    ) -> DirectedVoice:

        emotion = emotion.lower().strip()

        profile = self.EMOTIONS.get(
            emotion,
            self.EMOTIONS["calm"],
        )

        return DirectedVoice(
            text=text,
            emotion=emotion,
            speed=(
                profile["speed"]
                * base_speed
            ),
            pitch=(
                profile["pitch"]
                + base_pitch
            ),
            energy=(
                profile["energy"]
                * base_energy
            ),
            delivery_instruction=(
                profile["delivery"]
            ),
        )
