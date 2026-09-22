from dataclasses import dataclass


EMOTIONS = (
    "neutral",
    "happy",
    "sad",
    "angry",
    "fear",
    "surprised",
    "calm",
    "lonely",
    "romantic",
    "broken",
    "whisper",
    "crying",
)


@dataclass(frozen=True)
class EmotionVector:
    name: str
    intensity: float
    values: tuple[float, ...]


class EmotionEncoder:

    def __init__(self):
        self.emotions = {
            name: index
            for index, name in enumerate(EMOTIONS)
        }

    def encode(
        self,
        emotion: str,
        intensity: float = 1.0,
    ) -> EmotionVector:

        emotion = emotion.lower()

        if emotion not in self.emotions:
            emotion = "neutral"

        intensity = max(
            0.0,
            min(1.0, float(intensity)),
        )

        values = [0.0] * len(EMOTIONS)

        values[self.emotions[emotion]] = intensity

        return EmotionVector(
            name=emotion,
            intensity=intensity,
            values=tuple(values),
        )

    @property
    def dimension(self) -> int:
        return len(EMOTIONS)
