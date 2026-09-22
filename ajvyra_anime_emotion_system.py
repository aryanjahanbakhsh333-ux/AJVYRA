"""
AJVYRA Anime - Emotion System
Controls emotional direction for acting, dialogue, music and visuals.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


EMOTIONS = (
    "neutral",
    "curiosity",
    "joy",
    "warmth",
    "love",
    "tension",
    "fear",
    "anger",
    "shock",
    "sadness",
    "grief",
    "loneliness",
    "hope",
    "relief",
    "determination",
)


@dataclass(frozen=True)
class EmotionState:
    emotion: str
    intensity: int
    voice_speed: float
    pause_ratio: float
    music_energy: float
    facial_expression: str


EMOTION_PROFILES: Dict[str, EmotionState] = {
    "neutral": EmotionState("neutral", 2, 1.00, 0.10, 0.20, "neutral"),
    "curiosity": EmotionState("curiosity", 4, 0.95, 0.15, 0.35, "focused"),
    "joy": EmotionState("joy", 7, 1.08, 0.06, 0.75, "smiling"),
    "warmth": EmotionState("warmth", 5, 0.96, 0.12, 0.45, "soft"),
    "love": EmotionState("love", 7, 0.90, 0.18, 0.65, "gentle"),
    "tension": EmotionState("tension", 7, 1.02, 0.20, 0.80, "alert"),
    "fear": EmotionState("fear", 8, 1.05, 0.24, 0.85, "anxious"),
    "anger": EmotionState("anger", 8, 1.08, 0.08, 0.95, "angry"),
    "shock": EmotionState("shock", 9, 0.82, 0.30, 0.90, "stunned"),
    "sadness": EmotionState("sadness", 6, 0.88, 0.24, 0.30, "sad"),
    "grief": EmotionState("grief", 9, 0.72, 0.35, 0.20, "crying"),
    "loneliness": EmotionState("loneliness", 7, 0.80, 0.30, 0.18, "distant"),
    "hope": EmotionState("hope", 7, 0.94, 0.16, 0.70, "soft smile"),
    "relief": EmotionState("relief", 5, 0.98, 0.10, 0.45, "relaxed"),
    "determination": EmotionState("determination", 8, 0.98, 0.12, 0.90, "focused"),
}


def get_emotion(name: str) -> Dict:
    key = name.lower().strip()

    if key not in EMOTION_PROFILES:
        raise KeyError("Unknown emotion: {}".format(name))

    return asdict(EMOTION_PROFILES[key])


def emotion_sequence(anime_id: int) -> List[str]:
    sequences = {
        1: ["curiosity", "tension", "shock", "grief", "determination", "relief"],
        2: ["wonder", "curiosity", "fear", "sadness", "determination", "hope"],
        3: ["curiosity", "fear", "shock", "tension", "determination", "relief"],
        4: ["anger", "fear", "determination", "tension", "hope"],
        5: ["mystery", "fear", "sadness", "grief", "determination", "relief"],
        6: ["curiosity", "tension", "fear", "determination", "hope"],
        7: ["loneliness", "warmth", "love", "sadness", "hope"],
        8: ["tension", "fear", "anger", "determination", "relief"],
        9: ["curiosity", "wonder", "fear", "grief", "hope"],
        10: ["shock", "anger", "sadness", "determination", "hope"],
    }

    return sequences.get(
        anime_id,
        ["curiosity", "warmth", "tension", "sadness", "determination", "hope"],
    )


def scene_emotion(anime_id: int, scene_number: int) -> Dict:
    sequence = emotion_sequence(anime_id)
    emotion = sequence[(scene_number - 1) % len(sequence)]

    # Unknown names such as "wonder" are normalized to curiosity.
    if emotion not in EMOTION_PROFILES:
        emotion = "curiosity"

    return get_emotion(emotion)


if __name__ == "__main__":
    print(get_emotion("grief"))
