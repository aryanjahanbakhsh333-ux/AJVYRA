"""
AJVYRA Anime - Relationship System
Defines how characters relate to each other and how relationships evolve.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class Relationship:
    anime_id: int
    source: str
    target: str
    relationship_type: str
    beginning: str
    development: str
    turning_point: str
    ending: str


RELATIONSHIPS: List[Relationship] = []


def add(anime_id, source, target, kind, beginning, development, turning, ending):
    RELATIONSHIPS.append(
        Relationship(
            anime_id,
            source,
            target,
            kind,
            beginning,
            development,
            turning,
            ending,
        )
    )


RELATIONSHIP_NAMES = {
    1: ("Veyrissa", "Caelith", "investigation partners"),
    2: ("Elyndra", "Vaerion", "adventure companions"),
    3: ("Nythera", "Caevrin", "present self / future self"),
    4: ("Kaelvyn", "Zeyrith", "trusted allies"),
    5: ("Orivena", "Neyveth", "investigation partners"),
    6: ("Zerelith", "Kavren", "technical partners"),
    7: ("Vaelith", "Luneyra", "dream-bound connection"),
    8: ("Raveth", "Nythara", "crime-investigation partners"),
    9: ("Solvethra", "Arayelle", "traveler / guide"),
    10: ("Xavren", "Vorrik", "former friends turned enemies"),
    11: ("Elyvra", "Varelyn", "anonymous correspondents"),
    12: ("Neravya", "Kaelren", "future-investigation partners"),
    13: ("Vaerun", "Eliryn", "romantic connection"),
    14: ("Lunaira", "Veyron", "mysterious connection"),
    15: ("Averin", "Selyra", "close friendship"),
    16: ("Neyrissa", "Valeryn", "manipulated connection"),
    17: ("Elvaris", "Miraelyn", "romantic connection"),
    18: ("Virell", "Ayaelis", "repeating train connection"),
    19: ("Caelven", "Ravielle", "separated travelers"),
    20: ("Serenith", "Vaylena", "quiet friendship"),
    21: ("Mouren", "Elvyra", "living person / memory"),
    22: ("Noxel", "Yverra", "self / inner-memory"),
    23: ("Vaelor", "Lerienne", "time-limited romance"),
    24: ("Eryndel", "Davren", "living person / memory"),
    25: ("Neylorn", "Variel", "investigator / recorded voice"),
    26: ("Auralis", "Lynareth", "living person / echo"),
    27: ("Velorin", "Moraelyn", "subject / memory architect"),
    28: ("Seyrane", "Avielon", "messenger / sender"),
    29: ("Oryven", "Veyalia", "slowly rebuilt trust"),
    30: ("Lumiren", "Aeralyn", "traveler / guide"),
}


for anime_id, values in RELATIONSHIP_NAMES.items():
    source, target, kind = values

    add(
        anime_id,
        source,
        target,
        kind,
        "They begin with limited trust and incomplete understanding.",
        "Shared experiences make the relationship emotionally important.",
        "A major revelation forces both characters to reconsider the bond.",
        "The relationship reaches a new form based on the anime's final choice.",
    )


def get_relationships(anime_id: int) -> List[Dict]:
    return [
        asdict(item)
        for item in RELATIONSHIPS
        if item.anime_id == anime_id
    ]


def all_relationships() -> List[Dict]:
    return [asdict(item) for item in RELATIONSHIPS]


def relationship_graph(anime_id: int) -> Dict[str, List[str]]:
    graph = {}

    for item in RELATIONSHIPS:
        if item.anime_id != anime_id:
            continue

        graph.setdefault(item.source, []).append(item.target)
        graph.setdefault(item.target, []).append(item.source)

    return graph


if __name__ == "__main__":
    print("Relationships:", len(RELATIONSHIPS))
