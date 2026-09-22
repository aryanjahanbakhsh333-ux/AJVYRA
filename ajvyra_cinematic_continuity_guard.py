from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ContinuityIssue:
    severity: str
    category: str
    message: str
    entity_id: Optional[str] = None


@dataclass
class ContinuityReport:
    passed: bool
    issues: List[ContinuityIssue] = field(
        default_factory=list
    )

    def errors(self) -> List[ContinuityIssue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == "error"
        ]


class AJVYRACinematicContinuityGuard:

    def __init__(self):
        self.character_signatures: Dict[
            str,
            str
        ] = {}

        self.character_clothing: Dict[
            str,
            str
        ] = {}

        self.location_signatures: Dict[
            str,
            str
        ] = {}

        self.timeline_states: Dict[
            str,
            Dict
        ] = {}

    def register_character(
        self,
        character_id: str,
        continuity_hash: str,
        clothing: str,
    ) -> None:

        self.character_signatures[
            character_id
        ] = continuity_hash

        self.character_clothing[
            character_id
        ] = clothing

    def register_location(
        self,
        location_id: str,
        signature: str,
    ) -> None:

        self.location_signatures[
            location_id
        ] = signature

    def validate_character(
        self,
        character_id: str,
        continuity_hash: str,
        clothing: str,
    ) -> ContinuityReport:

        issues: List[ContinuityIssue] = []

        expected_hash = (
            self.character_signatures.get(
                character_id
            )
        )

        expected_clothing = (
            self.character_clothing.get(
                character_id
            )
        )

        if expected_hash is None:
            issues.append(
                ContinuityIssue(
                    "error",
                    "character",
                    "Character is not registered.",
                    character_id,
                )
            )
        elif expected_hash != continuity_hash:
            issues.append(
                ContinuityIssue(
                    "error",
                    "identity",
                    "Character continuity signature changed.",
                    character_id,
                )
            )

        if (
            expected_clothing is not None
            and expected_clothing != clothing
        ):
            issues.append(
                ContinuityIssue(
                    "warning",
                    "costume",
                    (
                        "Character clothing differs from "
                        "the registered state."
                    ),
                    character_id,
                )
            )

        return ContinuityReport(
            passed=not any(
                issue.severity == "error"
                for issue in issues
            ),
            issues=issues,
        )

    def validate_timeline_state(
        self,
        timeline_id: str,
        state: Dict,
    ) -> ContinuityReport:

        issues: List[ContinuityIssue] = []

        previous = self.timeline_states.get(
            timeline_id
        )

        if previous:

            for key in (
                "time_of_day",
                "weather",
                "season",
                "location_id",
            ):

                if (
                    key in previous
                    and key in state
                    and previous[key] != state[key]
                ):
                    issues.append(
                        ContinuityIssue(
                            "warning",
                            "world",
                            (
                                f"World state changed for "
                                f"{key}: "
                                f"{previous[key]} -> {state[key]}"
                            ),
                        )
                    )

        self.timeline_states[
            timeline_id
        ] = dict(state)

        return ContinuityReport(
            passed=True,
            issues=issues,
        )

    def validate(
        self,
        *,
        character_id: Optional[str] = None,
        continuity_hash: Optional[str] = None,
        clothing: Optional[str] = None,
        timeline_id: Optional[str] = None,
        world_state: Optional[Dict] = None,
    ) -> ContinuityReport:

        reports = []

        if character_id:
            reports.append(
                self.validate_character(
                    character_id,
                    continuity_hash or "",
                    clothing or "",
                )
            )

        if timeline_id and world_state is not None:
            reports.append(
                self.validate_timeline_state(
                    timeline_id,
                    world_state,
                )
            )

        issues = [
            issue
            for report in reports
            for issue in report.issues
        ]

        return ContinuityReport(
            passed=not any(
                issue.severity == "error"
                for issue in issues
            ),
            issues=issues,
        )
