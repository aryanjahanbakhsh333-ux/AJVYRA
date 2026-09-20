from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class AnimeScene:
    scene_id: str
    project_id: str

    order: int
    duration_seconds: int = 0

    location_id: str = ""
    time_of_day: str = ""

    character_ids: List[str] = field(default_factory=list)

    action: str = ""
    camera_direction: str = ""
    atmosphere: str = ""

    dialogue_ids: List[str] = field(default_factory=list)

    music: str = ""
    sound_effects: List[str] = field(default_factory=list)

    visual_prompt: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class SceneBuilder:

    def __init__(self):
        self.scenes: Dict[str, AnimeScene] = {}

    def create(
        self,
        scene_id: str,
        project_id: str,
        order: int,
        duration_seconds: int,
        location_id: str = ""
    ) -> AnimeScene:

        if scene_id in self.scenes:
            raise ValueError("Scene already exists.")

        scene = AnimeScene(
            scene_id=scene_id,
            project_id=project_id,
            order=order,
            duration_seconds=duration_seconds,
            location_id=location_id
        )

        self.scenes[scene_id] = scene
        return scene

    def add_character(
        self,
        scene_id: str,
        character_id: str
    ):
        scene = self.scenes[scene_id]

        if character_id not in scene.character_ids:
            scene.character_ids.append(character_id)

    def add_dialogue(
        self,
        scene_id: str,
        dialogue_id: str
    ):
        self.scenes[scene_id].dialogue_ids.append(dialogue_id)

    def for_project(
        self,
        project_id: str
    ) -> List[AnimeScene]:

        scenes = [
            scene
            for scene in self.scenes.values()
            if scene.project_id == project_id
        ]

        return sorted(
            scenes,
            key=lambda scene: scene.order
        )


if __name__ == "__main__":
    builder = SceneBuilder()

    scene = builder.create(
        "SCENE-001",
        "PROJECT-001",
        1,
        120,
        "LOC-001"
    )

    builder.add_character(
        "SCENE-001",
        "CHAR-001"
    )

    print(scene.to_dict())
