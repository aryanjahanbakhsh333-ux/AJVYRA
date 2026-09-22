from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ProsodySettings:
    base_pitch: float = 180.0
    pitch_variation: float = 0.08
    speaking_rate: float = 1.0
    energy: float = 1.0
    breath: float = 0.03
    pause_scale: float = 1.0


class NativeProsodyRenderer:
    """
    Generates deterministic pitch, energy and timing curves
    for algorithmic speech.

    Punctuation affects pauses and intonation.
    """

    PUNCTUATION = {
        ".": 0.24,
        ",": 0.12,
        "!": 0.22,
        "?": 0.28,
        "؛": 0.16,
        ";": 0.16,
        ":": 0.12,
        "…": 0.36,
    }

    EMOTION = {
        "neutral": (1.00, 1.00, 0.00),
        "sad": (0.86, 0.78, -0.05),
        "angry": (1.12, 1.18, 0.08),
        "happy": (1.08, 1.10, 0.12),
        "fear": (1.18, 0.82, 0.18),
        "whisper": (0.92, 0.48, -0.02),
        "cold": (0.90, 0.76, -0.10),
        "excited": (1.18, 1.24, 0.16),
    }

    def __init__(self, settings: ProsodySettings | None = None):
        self.settings = settings or ProsodySettings()

    def emotion_settings(
        self,
        emotion: str,
    ) -> ProsodySettings:

        emotion = emotion.lower().strip()

        pitch_mul, energy_mul, pitch_offset = self.EMOTION.get(
            emotion,
            self.EMOTION["neutral"],
        )

        return ProsodySettings(
            base_pitch=max(
                50.0,
                self.settings.base_pitch
                * pitch_mul
                + pitch_offset * 100.0,
            ),
            pitch_variation=self.settings.pitch_variation,
            speaking_rate=self.settings.speaking_rate,
            energy=self.settings.energy * energy_mul,
            breath=self.settings.breath,
            pause_scale=self.settings.pause_scale,
        )

    def pitch_curve(
        self,
        count: int,
        settings: ProsodySettings | None = None,
        question: bool = False,
        excited: bool = False,
    ) -> List[float]:

        settings = settings or self.settings

        if count <= 0:
            return []

        curve: List[float] = []

        for index in range(count):
            p = index / max(1, count - 1)

            natural = math.sin(
                2.0 * math.pi * 1.35 * p
            )

            rise = p * 0.08

            if question:
                ending = p * 0.20
            else:
                ending = -p * 0.13

            if excited:
                ending += p * 0.12

            value = settings.base_pitch * (
                1.0
                + settings.pitch_variation * natural
                + rise
                + ending
            )

            curve.append(max(55.0, value))

        return curve

    def energy_curve(
        self,
        count: int,
        settings: ProsodySettings | None = None,
    ) -> List[float]:

        settings = settings or self.settings

        if count <= 0:
            return []

        curve: List[float] = []

        for index in range(count):
            p = index / max(1, count - 1)

            rise = min(1.0, p / 0.10)
            fall = min(1.0, (1.0 - p) / 0.18)

            envelope = rise * fall

            curve.append(
                max(
                    0.03,
                    envelope * settings.energy,
                )
            )

        return curve

    def punctuation_pause(self, symbol: str) -> float:
        return (
            self.PUNCTUATION.get(
                symbol,
                0.0,
            )
            * self.settings.pause_scale
        )

    def text_pause_plan(self, text: str) -> List[float]:
        return [
            self.punctuation_pause(char)
            for char in text
        ]

    def detect_question(self, text: str) -> bool:
        return text.rstrip().endswith("?") or text.rstrip().endswith("؟")

    def detect_excited(self, text: str) -> bool:
        return text.rstrip().endswith("!")

    def syllable_timing(
        self,
        syllable_count: int,
        settings: ProsodySettings | None = None,
    ) -> List[float]:

        settings = settings or self.settings

        if syllable_count <= 0:
            return []

        base = 0.15 / max(
            0.35,
            settings.speaking_rate,
        )

        result = []

        for index in range(syllable_count):
            variation = 1.0 + (
                0.08
                * math.sin(index * 1.73)
            )

            result.append(
                max(
                    0.035,
                    base * variation,
                )
            )

        return result
