"""
AJVYRA Anime - Episode Timeline

Creates exact 30-minute timelines.
12 scenes x 150 seconds = 1800 seconds.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


EPISODE_SECONDS = 1800
SCENE_SECONDS = 150
SCENE_COUNT = 12


@dataclass(frozen=True)
class TimelineSegment:
    anime_id: int
    scene_number: int
    start: int
    end: int
    duration: int


def build_timeline(anime_id: int) -> List[Dict]:
    timeline = []

    for scene_number in range(1, SCENE_COUNT + 1):
        start = (scene_number - 1) * SCENE_SECONDS
        end = start + SCENE_SECONDS

        timeline.append(
            asdict(
                TimelineSegment(
                    anime_id,
                    scene_number,
                    start,
                    end,
                    SCENE_SECONDS,
                )
            )
        )

    return timeline


def format_time(seconds: int) -> str:
    minutes = seconds // 60
    remaining = seconds % 60

    return "{:02d}:{:02d}".format(minutes, remaining)


def build_readable_timeline(anime_id: int) -> List[Dict]:
    result = []

    for item in build_timeline(anime_id):
        result.append(
            {
                **item,
                "start_label": format_time(item["start"]),
                "end_label": format_time(item["end"]),
            }
        )

    return result


def validate_timeline(anime_id: int) -> Dict[str, object]:
    timeline = build_timeline(anime_id)

    return {
        "anime_id": anime_id,
        "scene_count": len(timeline),
        "episode_seconds": (
            timeline[-1]["end"] if timeline else 0
        ),
        "episode_length": (
            format_time(timeline[-1]["end"])
            if timeline
            else "00:00"
        ),
        "exact_30_minutes": (
            bool(timeline)
            and timeline[-1]["end"] == EPISODE_SECONDS
        ),
    }


def all_timelines() -> Dict[int, List[Dict]]:
    return {
        anime_id: build_timeline(anime_id)
        for anime_id in range(1, 31)
    }


if __name__ == "__main__":
    for anime_id in (1, 15, 30):
        print(validate_timeline(anime_id))
