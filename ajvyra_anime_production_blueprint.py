from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class ProductionBlueprint:
    anime_id: int
    title: str

    target_duration_seconds: int = 1800

    characters: List[str] = field(default_factory=list)
    voice_cast: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)

    story_events: List[str] = field(default_factory=list)
    scenes: List[str] = field(default_factory=list)
    dialogues: List[str] = field(default_factory=list)

    audio_ready: bool = False
    subtitles_ready: bool = False
    visuals_ready: bool = False
    animation_ready: bool = False

    def to_dict(self):
        return asdict(self)


class ProductionBlueprintManager:

    def __init__(self):
        self.projects: Dict[int, ProductionBlueprint] = {}

    def create(
        self,
        anime_id: int,
        title: str
    ) -> ProductionBlueprint:

        if anime_id in self.projects:
            raise ValueError(
                "Blueprint already exists."
            )

        blueprint = ProductionBlueprint(
            anime_id=anime_id,
            title=title
        )

        self.projects[anime_id] = blueprint
        return blueprint

    def add_character(
        self,
        anime_id: int,
        character_id: str
    ):
        self.projects[anime_id].characters.append(
            character_id
        )

    def add_event(
        self,
        anime_id: int,
        event_id: str
    ):
        self.projects[anime_id].story_events.append(
            event_id
        )

    def add_scene(
        self,
        anime_id: int,
        scene_id: str
    ):
        self.projects[anime_id].scenes.append(
            scene_id
        )

    def get(self, anime_id: int):
        return self.projects.get(anime_id)


if __name__ == "__main__":
    manager = ProductionBlueprintManager()

    blueprint = manager.create(
        1,
        "Veylora"
    )

    manager.add_event(
        1,
        "A01-E001"
    )

    print(blueprint.to_dict())
