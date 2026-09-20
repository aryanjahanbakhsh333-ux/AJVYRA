from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class AnimeBible:
    project_id: str

    world_name: str = ""
    era: str = ""
    world_description: str = ""

    main_theme: str = ""
    emotional_tone: str = ""
    visual_identity: str = ""

    world_rules: List[str] = field(default_factory=list)
    forbidden_elements: List[str] = field(default_factory=list)

    core_conflict: str = ""
    central_question: str = ""

    cultural_notes: List[str] = field(default_factory=list)

    originality_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)

    def add_world_rule(self, rule: str):
        if rule and rule not in self.world_rules:
            self.world_rules.append(rule)

    def add_forbidden_element(self, element: str):
        if element and element not in self.forbidden_elements:
            self.forbidden_elements.append(element)

    def add_originality_note(self, note: str):
        if note and note not in self.originality_notes:
            self.originality_notes.append(note)

    def validate(self) -> List[str]:
        problems = []

        if not self.project_id:
            problems.append("Missing project ID.")

        if not self.main_theme:
            problems.append("Main theme is missing.")

        if not self.core_conflict:
            problems.append("Core conflict is missing.")

        return problems


def create_bible(
    project_id: str,
    world_name: str,
    theme: str,
    conflict: str
) -> AnimeBible:

    return AnimeBible(
        project_id=project_id,
        world_name=world_name,
        main_theme=theme,
        core_conflict=conflict
    )


if __name__ == "__main__":
    bible = create_bible(
        "AJVYRA-DEMO",
        "A Newly Created World",
        "Identity",
        "A character must choose between two conflicting paths."
    )

    print(bible.to_dict())
