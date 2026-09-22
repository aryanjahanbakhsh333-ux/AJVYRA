"""
AJVYRA Anime - Quality Guard

Structural integrity checks.
This module does NOT rank anime or assign artistic quality scores.
It only detects missing, duplicated or inconsistent production data.
"""

from typing import Dict, List, Set

from ajvyra_anime_full_story_catalog import STORIES
from ajvyra_anime_character_catalog import CHARACTERS
from ajvyra_anime_event_catalog import get_events
from ajvyra_anime_scene_catalog import get_scenes
from ajvyra_anime_timeline import (
    build_timeline,
    EPISODE_SECONDS,
)


REQUIRED_STORY_FIELDS = (
    "opening",
    "inciting_incident",
    "rising_action",
    "midpoint",
    "major_reversal",
    "crisis",
    "climax",
    "ending",
)


def check_story_catalog() -> List[str]:
    errors = []

    if len(STORIES) != 30:
        errors.append("Story catalog does not contain exactly 30 anime.")

    ids = [item.anime_id for item in STORIES]

    if sorted(ids) != list(range(1, 31)):
        errors.append("Anime IDs must be exactly 1..30.")

    titles = [item.title for item in STORIES]

    if len(titles) != len(set(titles)):
        errors.append("Duplicate anime title detected.")

    for story in STORIES:
        for field in REQUIRED_STORY_FIELDS:
            value = getattr(story, field, "")

            if not isinstance(value, str) or not value.strip():
                errors.append(
                    "Anime {} has empty story field '{}'.".format(
                        story.anime_id,
                        field,
                    )
                )

    return errors


def check_character_catalog() -> List[str]:
    errors = []

    names = [character.name for character in CHARACTERS]
    ids = [character.character_id for character in CHARACTERS]

    if len(names) != len(set(names)):
        errors.append("Duplicate fictional character name detected.")

    if len(ids) != len(set(ids)):
        errors.append("Duplicate character ID detected.")

    anime_ids = {character.anime_id for character in CHARACTERS}

    if anime_ids != set(range(1, 31)):
        errors.append("At least one anime has no registered characters.")

    return errors


def check_events() -> List[str]:
    errors = []

    for anime_id in range(1, 31):
        events = get_events(anime_id)

        if len(events) < 8:
            errors.append(
                "Anime {} has fewer than 8 story events.".format(anime_id)
            )

    return errors


def check_scenes() -> List[str]:
    errors = []

    for anime_id in range(1, 31):
        scenes = get_scenes(anime_id)

        if len(scenes) != 12:
            errors.append(
                "Anime {} must have exactly 12 scenes.".format(anime_id)
            )

    return errors


def check_timelines() -> List[str]:
    errors = []

    for anime_id in range(1, 31):
        timeline = build_timeline(anime_id)

        if not timeline:
            errors.append(
                "Anime {} has no timeline.".format(anime_id)
            )
            continue

        if timeline[-1]["end"] != EPISODE_SECONDS:
            errors.append(
                "Anime {} does not end at 1800 seconds.".format(anime_id)
            )

        previous_end = 0

        for segment in timeline:
            if segment["start"] != previous_end:
                errors.append(
                    "Timeline gap/overlap in anime {} scene {}.".format(
                        anime_id,
                        segment["scene_number"],
                    )
                )

            previous_end = segment["end"]

    return errors


def run_quality_guard() -> Dict[str, object]:
    errors = []

    errors.extend(check_story_catalog())
    errors.extend(check_character_catalog())
    errors.extend(check_events())
    errors.extend(check_scenes())
    errors.extend(check_timelines())

    return {
        "anime_count": 30,
        "errors": errors,
        "error_count": len(errors),
        "passed": len(errors) == 0,
    }


def print_quality_report() -> None:
    report = run_quality_guard()

    print("=" * 60)
    print("AJVYRA ANIME QUALITY GUARD")
    print("=" * 60)

    print("Anime:", report["anime_count"])
    print("Errors:", report["error_count"])
    print("PASSED:", report["passed"])

    if report["errors"]:
        print("\nProblems:")

        for error in report["errors"]:
            print("-", error)
    else:
        print("\nAll structural checks passed.")


if __name__ == "__main__":
    print_quality_report()
