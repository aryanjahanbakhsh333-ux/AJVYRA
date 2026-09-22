from dataclasses import dataclass, field


@dataclass
class AnimeBlueprint:
    title: str
    genre: list[str]
    premise: str

    world: dict = field(default_factory=dict)
    characters: list[dict] = field(default_factory=list)
    locations: list[dict] = field(default_factory=list)
    scenes: list[dict] = field(default_factory=list)
    dialogue: list[dict] = field(default_factory=list)


class AnimeCreatorAI:

    def create_blueprint(
        self,
        title: str,
        description: str,
        genres: list[str],
    ) -> AnimeBlueprint:

        return AnimeBlueprint(
            title=title,
            genre=genres,
            premise=description,
        )

    def add_world(
        self,
        blueprint: AnimeBlueprint,
        world: dict,
    ) -> AnimeBlueprint:

        blueprint.world = world

        return blueprint

    def add_character(
        self,
        blueprint: AnimeBlueprint,
        character: dict,
    ) -> AnimeBlueprint:

        blueprint.characters.append(character)

        return blueprint

    def add_location(
        self,
        blueprint: AnimeBlueprint,
        location: dict,
    ) -> AnimeBlueprint:

        blueprint.locations.append(location)

        return blueprint

    def add_scene(
        self,
        blueprint: AnimeBlueprint,
        scene: dict,
    ) -> AnimeBlueprint:

        blueprint.scenes.append(scene)

        return blueprint

    def add_dialogue(
        self,
        blueprint: AnimeBlueprint,
        dialogue: dict,
    ) -> AnimeBlueprint:

        blueprint.dialogue.append(dialogue)

        return blueprint

    def validate(
        self,
        blueprint: AnimeBlueprint,
    ) -> list[str]:

        problems = []

        if not blueprint.world:
            problems.append("world_missing")

        if not blueprint.characters:
            problems.append("characters_missing")

        if not blueprint.locations:
            problems.append("locations_missing")

        if not blueprint.scenes:
            problems.append("scenes_missing")

        return problems
