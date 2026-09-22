from pathlib import Path


class AIProjectBuilder:

    def __init__(
        self,
        factory,
    ):
        self.factory = factory

    def build_anime(
        self,
        project_id: str,
        blueprint,
    ) -> Path:

        root = self.factory.project_root(
            project_id
        )

        folders = [
            "story",
            "characters",
            "locations",
            "scenes",
            "dialogue",
            "audio/fa",
            "audio/ja",
            "subtitles/en",
            "subtitles/fa",
            "subtitles/ja",
            "video",
            "posters",
        ]

        for folder in folders:
            self.factory.create_folder(
                project_id,
                folder,
            )

        self.factory.write_json(
            project_id,
            "story/blueprint.json",
            {
                "title": blueprint.title,
                "genres": blueprint.genre,
                "premise": blueprint.premise,
                "world": blueprint.world,
            },
        )

        return root

    def build_game(
        self,
        project_id: str,
        blueprint,
    ) -> Path:

        root = self.factory.project_root(
            project_id
        )

        folders = [
            "world",
            "characters",
            "maps",
            "quests",
            "items",
            "systems",
            "audio",
            "code",
            "data",
            "builds",
        ]

        for folder in folders:
            self.factory.create_folder(
                project_id,
                folder,
            )

        self.factory.write_json(
            project_id,
            "world/game.json",
            {
                "title": blueprint.title,
                "genre": blueprint.genre,
                "premise": blueprint.premise,
                "world": blueprint.world,
            },
        )

        return root
