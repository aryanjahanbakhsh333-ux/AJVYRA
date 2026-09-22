from dataclasses import dataclass, field


@dataclass
class GameBlueprint:
    title: str
    genre: str
    premise: str

    world: dict = field(default_factory=dict)
    characters: list[dict] = field(default_factory=list)
    maps: list[dict] = field(default_factory=list)
    quests: list[dict] = field(default_factory=list)
    items: list[dict] = field(default_factory=list)
    systems: list[dict] = field(default_factory=list)


class GameCreatorAI:

    def create_blueprint(
        self,
        title: str,
        genre: str,
        description: str,
    ) -> GameBlueprint:

        return GameBlueprint(
            title=title,
            genre=genre,
            premise=description,
        )

    def add_world(
        self,
        game: GameBlueprint,
        world: dict,
    ):

        game.world = world
        return game

    def add_character(
        self,
        game: GameBlueprint,
        character: dict,
    ):

        game.characters.append(character)
        return game

    def add_map(
        self,
        game: GameBlueprint,
        game_map: dict,
    ):

        game.maps.append(game_map)
        return game

    def add_quest(
        self,
        game: GameBlueprint,
        quest: dict,
    ):

        game.quests.append(quest)
        return game

    def add_item(
        self,
        game: GameBlueprint,
        item: dict,
    ):

        game.items.append(item)
        return game

    def add_system(
        self,
        game: GameBlueprint,
        system: dict,
    ):

        game.systems.append(system)
        return game

    def validate(
        self,
        game: GameBlueprint,
    ) -> list[str]:

        problems = []

        if not game.world:
            problems.append("world_missing")

        if not game.characters:
            problems.append("characters_missing")

        if not game.maps:
            problems.append("maps_missing")

        if not game.systems:
            problems.append("game_systems_missing")

        return problems
