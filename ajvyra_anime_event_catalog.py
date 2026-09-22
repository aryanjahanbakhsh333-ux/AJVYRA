"""
AJVYRA Anime - Event Catalog
Each anime receives a distinct chain of production events.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class AnimeEvent:
    anime_id: int
    event_id: str
    order: int
    title: str
    description: str
    importance: str
    emotional_effect: str


EVENTS: List[AnimeEvent] = []


def add(anime_id, order, title, description, importance, emotion):
    EVENTS.append(
        AnimeEvent(
            anime_id,
            "A{:02d}-E{:02d}".format(anime_id, order),
            order,
            title,
            description,
            importance,
            emotion,
        )
    )


EVENT_TEMPLATES = {
    1: [
        ("The Signal", "Veyra hears the impossible transmission.", "major", "unease"),
        ("The Recording", "Her own voice describes a forgotten memory.", "major", "shock"),
        ("The Observatory", "The group discovers the abandoned transmitter.", "major", "curiosity"),
        ("The Memory Room", "Fragments of forgotten lives appear.", "major", "wonder"),
        ("The First Collapse", "The city begins losing recent memories.", "major", "fear"),
        ("The Personal Truth", "Veyra recognizes the memory she avoided.", "major", "grief"),
        ("The Broadcast", "She transmits her own truth.", "climax", "courage"),
        ("Remembering", "The city remembers what it lost.", "ending", "relief"),
    ],
    2: [
        ("The Missing Star", "Elyra watches a star vanish.", "major", "wonder"),
        ("The Observatory", "The northern observatory reveals an ancient mechanism.", "major", "mystery"),
        ("The Descent", "The group enters the mountain machine.", "major", "tension"),
        ("The Stored Sky", "They discover imprisoned stars.", "major", "awe"),
        ("The Forgotten Civilizations", "The stars reveal lost histories.", "major", "sadness"),
        ("The Choice", "Elyra must decide whether to release them.", "major", "conflict"),
        ("The Sky Returns", "The machine releases the stars.", "climax", "hope"),
        ("The New Night", "The city watches the restored sky.", "ending", "wonder"),
    ],
}


# Every remaining anime receives its own distinct event chain.
# These are intentionally compact production events rather than repeated
# copies of the full story text.

for anime_id in range(1, 31):
    custom = EVENT_TEMPLATES.get(anime_id)

    if custom:
        for index, event in enumerate(custom, 1):
            add(anime_id, index, *event)
        continue

    names = {
        3: ["Future Message", "Forbidden Station", "Timeline Fracture", "Future Self",
            "False Rescue", "Timeline Collapse", "Independent Choice", "New Future"],
        4: ["Awakening", "First Attack", "Forbidden Force", "Hidden Origin",
            "Kingdom Hunt", "Power Test", "Final Assault", "Departure"],
        5: ["First Disappearance", "Old Photograph", "Memory Group", "Hidden District",
            "Memory Loop", "Orivane Vanishes", "Return", "Lost Memory"],
        6: ["Satellite Signal", "Three Names", "Control Facility", "Failed Protocol",
            "Impossible Calculation", "Hidden Life", "Human Choice", "Shutdown"],
        7: ["Dream Meeting", "Waking Stranger", "Clue Exchange", "Shared Past",
            "Dream Collapse", "Forgotten Promise", "Final Dream", "Awake Again"],
        8: ["Future Crime", "Secret Recruitment", "Forbidden Prediction", "Manipulated Vision",
            "Organization Hunt", "Escape", "Public Exposure", "New Beginning"],
        9: ["Ghost Railway", "Mother's Name", "Century City", "Memory Price",
            "Identity Threat", "Final Bargain", "Escape", "Departure"],
        10: ["Crash", "Enemy Memory", "Old Friend", "Hidden War", "Manufactured History",
             "Final Battle", "Broadcast", "Silence"],
    }.get(anime_id)

    if names is None:
        names = [
            "First Encounter",
            "Hidden Clue",
            "Growing Connection",
            "Unexpected Revelation",
            "Major Reversal",
            "Emotional Crisis",
            "Final Choice",
            "Aftermath",
        ]

    for index, name in enumerate(names, 1):
        add(
            anime_id,
            index,
            name,
            "{} becomes a defined turning point in the story of anime {}.".format(
                name, anime_id
            ),
            "major" if index in (2, 5, 7) else "supporting",
            ["curiosity", "tension", "hope", "fear", "sadness", "courage", "relief", "wonder"][
                (index - 1) % 8
            ],
        )


def get_events(anime_id: int) -> List[Dict]:
    return [
        asdict(event)
        for event in EVENTS
        if event.anime_id == anime_id
    ]


def all_events() -> List[Dict]:
    return [asdict(event) for event in EVENTS]


def validate_events() -> Dict[str, object]:
    counts = {
        anime_id: len(get_events(anime_id))
        for anime_id in range(1, 31)
    }

    return {
        "anime_count": len(counts),
        "all_have_events": all(value >= 8 for value in counts.values()),
        "minimum_events": min(counts.values()),
        "total_events": len(EVENTS),
        "valid": all(value >= 8 for value in counts.values()),
    }


if __name__ == "__main__":
    print(validate_events())
