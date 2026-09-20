from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class AnimeStory:
    story_id: str
    project_id: str

    premise: str = ""
    protagonist_goal: str = ""
    antagonist_force: str = ""

    beginning: str = ""
    rising_conflict: List[str] = field(default_factory=list)
    turning_points: List[str] = field(default_factory=list)

    climax: str = ""
    ending: str = ""

    emotional_arc: List[str] = field(default_factory=list)

    themes: List[str] = field(default_factory=list)

    originality_statement: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class StoryCreator:

    def __init__(self):
        self.stories: Dict[str, AnimeStory] = {}

    def create(
        self,
        story_id: str,
        project_id: str,
        premise: str,
        protagonist_goal: str,
        ending: str
    ) -> AnimeStory:

        if story_id in self.stories:
            raise ValueError("Story ID already exists.")

        story = AnimeStory(
            story_id=story_id,
            project_id=project_id,
            premise=premise,
            protagonist_goal=protagonist_goal,
            ending=ending
        )

        self.stories[story_id] = story
        return story

    def add_conflict(
        self,
        story_id: str,
        conflict: str
    ):
        self.stories[story_id].rising_conflict.append(conflict)

    def add_turning_point(
        self,
        story_id: str,
        event: str
    ):
        self.stories[story_id].turning_points.append(event)

    def get(
        self,
        story_id: str
    ) -> AnimeStory | None:

        return self.stories.get(story_id)


if __name__ == "__main__":
    creator = StoryCreator()

    story = creator.create(
        "STORY-001",
        "PROJECT-001",
        "A mysterious signal changes a lonely student's life.",
        "Discover who is sending the signal.",
        "The truth changes the protagonist forever."
    )

    creator.add_conflict(
        "STORY-001",
        "The signal begins predicting events."
    )

    print(story.to_dict())
