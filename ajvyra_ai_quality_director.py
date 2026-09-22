from dataclasses import dataclass


@dataclass
class QualityReport:
    passed: bool
    errors: list[str]
    warnings: list[str]


class AIQualityDirector:

    def inspect_anime(
        self,
        blueprint,
    ) -> QualityReport:

        errors = []
        warnings = []

        if not blueprint.world:
            errors.append("Anime has no world.")

        if len(blueprint.characters) < 2:
            errors.append(
                "Anime needs at least two characters."
            )

        if not blueprint.scenes:
            errors.append(
                "Anime contains no scenes."
            )

        if not blueprint.dialogue:
            warnings.append(
                "Anime contains no dialogue yet."
            )

        return QualityReport(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def inspect_game(
        self,
        blueprint,
    ) -> QualityReport:

        errors = []
        warnings = []

        if not blueprint.world:
            errors.append("Game has no world.")

        if not blueprint.maps:
            errors.append("Game has no map.")

        if not blueprint.characters:
            errors.append(
                "Game has no characters."
            )

        if not blueprint.systems:
            errors.append(
                "Game has no gameplay systems."
            )

        if not blueprint.quests:
            warnings.append(
                "Game has no quests yet."
            )

        return QualityReport(
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )
