"""
AJVYRA Anime - Digital Voice Router

Routes each fictional character to an independent digital voice profile.
The actual synthesis engine can be local or provider-based.
"""

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass(frozen=True)
class VoiceProfile:
    voice_id: str
    character_id: str
    gender_style: str
    age_style: str
    tone: str
    speaking_rate: float
    pitch: float
    languages: tuple


VOICE_PROFILES: Dict[str, VoiceProfile] = {}


def register_character_voice(
    character_id: str,
    voice_number: int,
    gender_style: str,
    age_style: str,
    tone: str,
):
    voice_id = "AJVYRA-VOICE-{:03d}".format(voice_number)

    VOICE_PROFILES[character_id] = VoiceProfile(
        voice_id=voice_id,
        character_id=character_id,
        gender_style=gender_style,
        age_style=age_style,
        tone=tone,
        speaking_rate=1.0,
        pitch=0.0,
        languages=("fa", "ja"),
    )


voice_number = 1

for anime_id in range(1, 31):
    character_count = 3 if anime_id in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30) else 2

    for character_number in range(1, character_count + 1):
        character_id = "A{:02d}-C{:02d}".format(
            anime_id,
            character_number,
        )

        register_character_voice(
            character_id,
            voice_number,
            "female" if character_number == 2 else "male",
            "young_adult",
            "cinematic-neutral",
        )

        voice_number += 1


def get_voice(character_id: str) -> Dict:
    profile = VOICE_PROFILES.get(character_id)

    if profile is None:
        raise KeyError(
            "No digital voice registered for {}".format(character_id)
        )

    return asdict(profile)


def get_voice_id(character_id: str, language: str = "fa") -> str:
    profile = VOICE_PROFILES.get(character_id)

    if profile is None:
        raise KeyError(character_id)

    if language not in profile.languages:
        raise ValueError(
            "Language {} is not supported for {}".format(
                language,
                character_id,
            )
        )

    return profile.voice_id


def route_dialogue(character_id: str, language: str, text: str) -> Dict:
    return {
        "character_id": character_id,
        "language": language,
        "voice_id": get_voice_id(character_id, language),
        "text": text,
        "ready_for_tts": bool(text.strip()),
    }


def all_voice_profiles() -> Dict[str, Dict]:
    return {
        key: asdict(value)
        for key, value in VOICE_PROFILES.items()
    }


if __name__ == "__main__":
    print("Digital voice profiles:", len(VOICE_PROFILES))
