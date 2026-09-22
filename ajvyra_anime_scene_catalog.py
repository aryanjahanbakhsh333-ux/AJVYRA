"""
AJVYRA Anime - Scene Catalog
12 cinematic scenes per anime.
12 x 150 seconds = 1800 seconds = 30 minutes.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


SCENE_LENGTH = 150
SCENE_COUNT = 12


@dataclass(frozen=True)
class Scene:
    anime_id: int
    scene_number: int
    scene_id: str
    title: str
    location: str
    characters: List[str]
    action: str
    camera: str
    atmosphere: str
    music: str
    sound_effects: List[str]


SCENES: List[Scene] = []


SCENE_PATTERNS = [
    ("Opening", "establishing environment and protagonist", "wide cinematic shot", "quiet", "ambient"),
    ("Inciting Incident", "the central unusual event begins", "slow push-in", "curious", "soft tension"),
    ("Investigation", "characters follow the first clue", "tracking shot", "mysterious", "low pulse"),
    ("Discovery", "a hidden truth is revealed", "close-up", "uneasy", "rising strings"),
    ("Connection", "characters share an important moment", "two-shot", "intimate", "piano"),
    ("Reversal", "the meaning of the situation changes", "rapid cuts", "shocking", "deep bass"),
    ("Consequences", "the characters face the result", "handheld movement", "unstable", "dark ambience"),
    ("Crisis", "the protagonist reaches the emotional low point", "close handheld", "heavy", "minimal piano"),
    ("Decision", "the protagonist chooses a path", "slow orbit", "determined", "building strings"),
    ("Climax", "the central conflict reaches its peak", "dynamic cinematic camera", "intense", "full score"),
    ("Resolution", "the main conflict settles", "slow wide shot", "relieved", "soft piano"),
    ("Final Image", "a final visual closes the story", "static wide shot", "reflective", "piano and ambience"),
]


for anime_id in range(1, 31):
    for number, pattern in enumerate(SCENE_PATTERNS, 1):
        title, action, camera, atmosphere, music = pattern

        location = "anime_{}_location_{}".format(
            anime_id,
            min(((number - 1) // 4) + 1, 3),
        )

        characters = [
            "A{:02d}-C01".format(anime_id),
            "A{:02d}-C02".format(anime_id),
        ]

        if anime_id in (1, 2, 6, 30) and number in (4, 10):
            characters.append("A{:02d}-C03".format(anime_id))

        SCENES.append(
            Scene(
                anime_id,
                number,
                "A{:02d}-S{:02d}".format(anime_id, number),
                title,
                location,
                characters,
                action,
                camera,
                atmosphere,
                music,
                ["room tone", "environment ambience"],
            )
        )


def get_scenes(anime_id: int) -> List[Dict]:
    return [
        asdict(scene)
        for scene in SCENES
        if scene.anime_id == anime_id
    ]


def all_scenes() -> List[Dict]:
    return [asdict(scene) for scene in SCENES]


def validate_scene_lengths() -> Dict[str, object]:
    durations = {}

    for anime_id in range(1, 31):
        scenes = get_scenes(anime_id)
        durations[anime_id] = len(scenes) * SCENE_LENGTH

    return {
        "scene_count_per_anime": SCENE_COUNT,
        "scene_length_seconds": SCENE_LENGTH,
        "episode_length_seconds": SCENE_COUNT * SCENE_LENGTH,
        "all_are_30_minutes": all(
            value == 1800 for value in durations.values()
        ),
    }


if __name__ == "__main__":
    print(validate_scene_lengths())
