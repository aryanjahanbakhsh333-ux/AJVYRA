from ajvyra_anime_content_core import (
    get_anime,
    all_anime
)

from ajvyra_anime_story_events import (
    get_events
)

from ajvyra_anime_scene_blueprint import (
    SceneBlueprintBuilder
)

from ajvyra_anime_production_blueprint import (
    ProductionBlueprintManager
)


class AJVYRAAnimeAutoProduction:

    def __init__(self):
        self.scene_builder = SceneBlueprintBuilder()
        self.blueprints = ProductionBlueprintManager()

    def initialize_anime(self, anime_id: int):

        anime = get_anime(anime_id)

        blueprint = self.blueprints.create(
            anime.anime_id,
            anime.title
        )

        events = get_events(anime_id)

        for event in events:
            blueprint.story_events.append(
                event.event_id
            )

        return blueprint

    def initialize_all(self):

        results = []

        for anime in all_anime():

            if anime.anime_id in self.blueprints.projects:
                continue

            results.append(
                self.initialize_anime(
                    anime.anime_id
                )
            )

        return results

    def status(self):

        return {
            "anime_count": len(
                self.blueprints.projects
            ),
            "initialized": [
                anime_id
                for anime_id in self.blueprints.projects
            ]
        }


if __name__ == "__main__":
    system = AJVYRAAnimeAutoProduction()

    projects = system.initialize_all()

    print(
        "AJVYRA Anime projects initialized:",
        len(projects)
    )

    print(system.status())
