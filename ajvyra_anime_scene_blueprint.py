from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class SceneBlueprint:
    scene_id: str
    anime_id: int
    scene_number: int

    title: str
    location: str
    time_of_day: str

    characters: List[str] = field(default_factory=list)

    action: str = ""
    camera: str = ""
    atmosphere: str = ""

    dialogue_required: bool = True
    music_required: bool = True
    effects_required: bool = True

    duration_seconds: int = 0

    def to_dict(self):
        return asdict(self)


class SceneBlueprintBuilder:

    def create(
        self,
        anime_id: int,
        scene_number: int,
        title: str,
        location: str,
        duration_seconds: int = 120,
        time_of_day: str = "day"
    ) -> SceneBlueprint:

        scene_id = (
            f"ANIME-{anime_id:02d}-"
            f"SCENE-{scene_number:03d}"
        )

        return SceneBlueprint(
            scene_id=scene_id,
            anime_id=anime_id,
            scene_number=scene_number,
            title=title,
            location=location,
            duration_seconds=duration_seconds,
            time_of_day=time_of_day
        )

    def total_duration(
        self,
        scenes: List[SceneBlueprint]
    ) -> int:

        return sum(
            scene.duration_seconds
            for scene in scenes
        )

    def validate_30_minutes(
        self,
        scenes: List[SceneBlueprint]
    ) -> bool:

        return self.total_duration(scenes) == 1800


if __name__ == "__main__":
    builder = SceneBlueprintBuilder()

    scene = builder.create(
        1,
        1,
        "The Signal",
        "Abandoned District",
        120,
        "night"
    )

    print(scene.to_dict())
