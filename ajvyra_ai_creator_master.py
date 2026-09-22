from ajvyra_creator_spec import (
    CreatorRequest,
    CreatorResult,
    validate_request,
)

from ajvyra_creator_memory import (
    CreatorMemory,
)

from ajvyra_creator_planner import (
    CreatorPlanner,
)

from ajvyra_anime_creator_ai import (
    AnimeCreatorAI,
)

from ajvyra_game_creator_ai import (
    GameCreatorAI,
)

from ajvyra_ai_asset_factory import (
    AIAssetFactory,
)

from ajvyra_ai_project_builder import (
    AIProjectBuilder,
)

from ajvyra_ai_quality_director import (
    AIQualityDirector,
)


class AJVYRAAICreatorMaster:

    def __init__(self):

        self.memory = CreatorMemory()

        self.planner = CreatorPlanner()

        self.anime_ai = AnimeCreatorAI()

        self.game_ai = GameCreatorAI()

        self.factory = AIAssetFactory()

        self.builder = AIProjectBuilder(
            self.factory
        )

        self.quality = AIQualityDirector()

    def create(
        self,
        request: CreatorRequest,
    ) -> CreatorResult:

        validate_request(request)

        project_id = (
            request.project_type
            + "_"
            + request.request_id
        )

        if request.project_type == "anime":

            blueprint = (
                self.anime_ai.create_blueprint(
                    title=request.title,
                    description=request.description,
                    genres=request.features,
                )
            )

            self.builder.build_anime(
                project_id,
                blueprint,
            )

            report = (
                self.quality.inspect_anime(
                    blueprint
                )
            )

        else:

            genre = (
                request.features[0]
                if request.features
                else "adventure"
            )

            blueprint = (
                self.game_ai.create_blueprint(
                    title=request.title,
                    genre=genre,
                    description=request.description,
                )
            )

            self.builder.build_game(
                project_id,
                blueprint,
            )

            report = (
                self.quality.inspect_game(
                    blueprint
                )
            )

        self.memory.remember(
            "projects",
            {
                "request_id": request.request_id,
                "project_id": project_id,
                "type": request.project_type,
                "title": request.title,
                "status": (
                    "ready"
                    if report.passed
                    else "needs_work"
                ),
            },
        )

        return CreatorResult(
            request_id=request.request_id,
            project_type=request.project_type,
            project_path=str(
                self.factory.project_root(
                    project_id
                )
            ),
            warnings=report.warnings
            + report.errors,
            status=(
                "ready"
                if report.passed
                else "needs_work"
            ),
        )


CREATOR_AI = AJVYRAAICreatorMaster()


if __name__ == "__main__":

    anime_request = CreatorRequest(
        request_id="demo_anime_001",
        project_type="anime",
        title="Demo Anime",
        description=(
            "A mysterious story about memory, "
            "friendship and an unknown city."
        ),
        target_language="fa",
        features=[
            "mystery",
            "psychological",
            "drama",
        ],
    )

    result = CREATOR_AI.create(
        anime_request
    )

    print(result)
