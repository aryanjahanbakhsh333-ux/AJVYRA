"""
AJVYRA CINEMATIC EMOTION ENGINE
-------------------------------
Unified emotional intelligence for cinematic anime.

Emotion is represented as a continuous state rather than a
single label. Other engines consume this state to control:

- facial acting
- body language
- camera
- lighting
- pacing
- voice
- music
- silence
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class EmotionVector:
    joy: float = 0.0
    sadness: float = 0.0
    fear: float = 0.0
    anger: float = 0.0
    love: float = 0.0
    hope: float = 0.0
    tension: float = 0.0
    loneliness: float = 0.0
    surprise: float = 0.0
    trust: float = 0.0

    def clamp(self) -> "EmotionVector":
        for name in self.__dataclass_fields__:
            value = getattr(self, name)
            setattr(
                self,
                name,
                max(0.0, min(1.0, float(value))),
            )
        return self

    def blend(
        self,
        other: "EmotionVector",
        amount: float,
    ) -> "EmotionVector":
        amount = max(0.0, min(1.0, amount))

        values = {}

        for name in self.__dataclass_fields__:
            a = getattr(self, name)
            b = getattr(other, name)

            values[name] = (
                a + (b - a) * amount
            )

        return EmotionVector(**values).clamp()

    def dominant(self) -> str:
        values = asdict(self)

        return max(
            values,
            key=values.get,
        )


@dataclass
class EmotionDirection:
    primary: str
    secondary: str

    intensity: float
    volatility: float

    facial_expression: str
    body_language: str
    eye_behavior: str

    vocal_energy: float
    vocal_speed: float

    camera_energy: float
    music_energy: float

    silence_weight: float

    color_temperature: str
    lighting_contrast: float


class AJVYRAEmotionEngine:
    VERSION = "1.0.0"

    PROFILES: Dict[str, EmotionVector] = {
        "joy": EmotionVector(
            joy=0.90,
            hope=0.55,
            trust=0.65,
        ),
        "sadness": EmotionVector(
            sadness=0.92,
            loneliness=0.72,
            hope=0.12,
        ),
        "fear": EmotionVector(
            fear=0.94,
            tension=0.90,
            surprise=0.55,
            trust=0.10,
        ),
        "anger": EmotionVector(
            anger=0.94,
            tension=0.88,
            trust=0.10,
        ),
        "love": EmotionVector(
            love=0.94,
            joy=0.42,
            trust=0.86,
            hope=0.68,
        ),
        "hope": EmotionVector(
            hope=0.94,
            joy=0.42,
            trust=0.58,
        ),
        "loneliness": EmotionVector(
            loneliness=0.96,
            sadness=0.78,
            trust=0.12,
        ),
        "shock": EmotionVector(
            surprise=0.98,
            fear=0.45,
            tension=0.72,
        ),
        "despair": EmotionVector(
            sadness=0.98,
            loneliness=0.94,
            hope=0.02,
            tension=0.60,
        ),
    }

    def __init__(self) -> None:
        self.history: List[Dict] = []

    def profile(
        self,
        emotion: str,
        intensity: float = 1.0,
    ) -> EmotionVector:
        base = self.PROFILES.get(
            emotion.lower(),
            EmotionVector(),
        )

        intensity = max(
            0.0,
            min(1.0, intensity),
        )

        return EmotionVector(
            **{
                name: getattr(base, name) * intensity
                for name in base.__dataclass_fields__
            }
        ).clamp()

    def direction(
        self,
        vector: EmotionVector,
    ) -> EmotionDirection:
        vector.clamp()

        values = asdict(vector)
        ordered = sorted(
            values.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        primary = ordered[0][0]
        secondary = (
            ordered[1][0]
            if len(ordered) > 1
            else "neutral"
        )

        intensity = max(
            values.values()
        )

        volatility = min(
            1.0,
            vector.tension * 0.65
            + vector.surprise * 0.35,
        )

        return EmotionDirection(
            primary=primary,
            secondary=secondary,
            intensity=round(
                intensity,
                4,
            ),
            volatility=round(
                volatility,
                4,
            ),
            facial_expression=(
                self._face(primary)
            ),
            body_language=(
                self._body(primary)
            ),
            eye_behavior=(
                self._eyes(primary)
            ),
            vocal_energy=round(
                self._voice_energy(vector),
                4,
            ),
            vocal_speed=round(
                self._voice_speed(vector),
                4,
            ),
            camera_energy=round(
                self._camera_energy(vector),
                4,
            ),
            music_energy=round(
                self._music_energy(vector),
                4,
            ),
            silence_weight=round(
                self._silence(vector),
                4,
            ),
            color_temperature=(
                self._temperature(vector)
            ),
            lighting_contrast=round(
                self._contrast(vector),
                4,
            ),
        )

    def transition(
        self,
        start: EmotionVector,
        end: EmotionVector,
        progress: float,
    ) -> EmotionVector:
        return start.blend(
            end,
            max(
                0.0,
                min(1.0, progress),
            ),
        )

    def record(
        self,
        timestamp: float,
        character_id: str,
        vector: EmotionVector,
    ) -> EmotionDirection:
        direction = self.direction(vector)

        self.history.append(
            {
                "time": timestamp,
                "character_id": character_id,
                "vector": asdict(vector),
                "direction": asdict(direction),
            }
        )

        return direction

    @staticmethod
    def _face(emotion: str) -> str:
        return {
            "joy": "natural open smile",
            "sadness": "restrained sadness",
            "fear": "controlled fear",
            "anger": "contained anger",
            "love": "soft unguarded expression",
            "hope": "quiet hopeful expression",
            "loneliness": "emotionally distant expression",
            "surprise": "brief stunned expression",
            "despair": "emotionally exhausted expression",
        }.get(
            emotion,
            "neutral expression",
        )

    @staticmethod
    def _body(emotion: str) -> str:
        return {
            "joy": "light relaxed movement",
            "sadness": "minimal restrained movement",
            "fear": "defensive tension",
            "anger": "rigid controlled posture",
            "love": "subtle openness",
            "hope": "gradually opening posture",
            "loneliness": "isolated stillness",
            "surprise": "brief involuntary reaction",
            "despair": "heavy withdrawn posture",
        }.get(
            emotion,
            "natural posture",
        )

    @staticmethod
    def _eyes(emotion: str) -> str:
        return {
            "joy": "natural eye contact",
            "sadness": "look downward or away",
            "fear": "searching uncertain gaze",
            "anger": "direct focused stare",
            "love": "sustained gentle eye contact",
            "hope": "look toward distant light",
            "loneliness": "avoidance of eye contact",
            "surprise": "rapid focus shift",
            "despair": "unfocused downward gaze",
        }.get(
            emotion,
            "contextual gaze",
        )

    @staticmethod
    def _voice_energy(
        vector: EmotionVector,
    ) -> float:
        return min(
            1.0,
            0.18
            + vector.anger * 0.55
            + vector.fear * 0.35
            + vector.joy * 0.25
            + vector.tension * 0.25,
        )

    @staticmethod
    def _voice_speed(
        vector: EmotionVector,
    ) -> float:
        return max(
            0.45,
            min(
                1.35,
                0.90
                + vector.anger * 0.28
                + vector.fear * 0.18
                - vector.sadness * 0.25
                - vector.loneliness * 0.18,
            ),
        )

    @staticmethod
    def _camera_energy(
        vector: EmotionVector,
    ) -> float:
        return min(
            1.0,
            vector.tension * 0.55
            + vector.surprise * 0.35
            + vector.anger * 0.25,
        )

    @staticmethod
    def _music_energy(
        vector: EmotionVector,
    ) -> float:
        return min(
            1.0,
            0.18
            + vector.tension * 0.40
            + vector.love * 0.25
            + vector.sadness * 0.22
            + vector.hope * 0.20,
        )

    @staticmethod
    def _silence(
        vector: EmotionVector,
    ) -> float:
        return min(
            1.0,
            vector.sadness * 0.60
            + vector.loneliness * 0.55
            + vector.despair
            if hasattr(vector, "despair")
            else vector.sadness * 0.60
            + vector.loneliness * 0.55,
        )

    @staticmethod
    def _temperature(
        vector: EmotionVector,
    ) -> str:
        warm = (
            vector.joy
            + vector.love
            + vector.hope
        )

        cold = (
            vector.sadness
            + vector.fear
            + vector.loneliness
        )

        if cold > warm + 0.20:
            return "cold"

        if warm > cold + 0.20:
            return "warm"

        return "neutral"

    @staticmethod
    def _contrast(
        vector: EmotionVector,
    ) -> float:
        return max(
            0.25,
            min(
                0.95,
                0.35
                + vector.fear * 0.30
                + vector.anger * 0.25
                + vector.tension * 0.20,
            ),
        )

    def save(
        self,
        path: str | Path,
    ) -> Path:
        target = Path(path)
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                {
                    "version": self.VERSION,
                    "history": self.history,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


if __name__ == "__main__":
    engine = AJVYRAEmotionEngine()

    vector = engine.profile(
        "sadness",
        0.92,
    )

    direction = engine.record(
        timestamp=420.0,
        character_id="vey_01",
        vector=vector,
    )

    print(
        json.dumps(
            asdict(direction),
            ensure_ascii=False,
            indent=2,
        )
    )
