"""
AJVYRA Anime - Location Catalog
Real-world inspired and fictional locations used by the stories.
"""

from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass(frozen=True)
class Location:
    anime_id: int
    location_id: str
    name: str
    location_type: str
    description: str
    visual_style: str
    story_function: str


LOCATIONS: List[Location] = []


def add(anime_id, number, name, kind, description, visual, function):
    LOCATIONS.append(
        Location(
            anime_id,
            "A{:02d}-L{:02d}".format(anime_id, number),
            name,
            kind,
            description,
            visual,
            function,
        )
    )


LOCATION_DATA = {
    1: [
        ("Veylora Harbor", "real-inspired city", "A quiet coastal district with old buildings.", "misty blue streets", "home"),
        ("Old Observatory", "fictional landmark", "An abandoned observatory above the city.", "dark stone and broken glass", "mystery"),
        ("Signal Chamber", "fictional facility", "A buried room containing the transmitter.", "metal corridors and red lights", "climax"),
    ],
    2: [
        ("Aelvryn", "fictional mountain city", "A city surrounded by snowy peaks.", "blue night sky", "home"),
        ("Northern Observatory", "observatory", "A tower overlooking the mountains.", "silver architecture", "investigation"),
        ("Star Vault", "fantasy facility", "A chamber storing impossible lights.", "floating stars", "climax"),
    ],
    3: [
        ("Nyxara Central", "futuristic city", "A dense city of elevated trains.", "neon rain", "home"),
        ("Terminal Nine", "subway station", "An abandoned station connected to the timeline event.", "empty platforms", "mystery"),
        ("Temporal Lab", "science facility", "A hidden laboratory studying timelines.", "white glass and blue light", "climax"),
    ],
}


for anime_id in range(1, 31):
    if anime_id in LOCATION_DATA:
        for number, item in enumerate(LOCATION_DATA[anime_id], 1):
            add(anime_id, number, *item)
        continue

    base_names = {
        4: ["Kaelith Capital", "Forbidden Temple", "Royal District"],
        5: ["Orivane City", "Memory District", "Archive Hall"],
        6: ["Zeravia Colony", "Control Facility", "Orbital Command"],
        7: ["Vaelune Town", "Dream Garden", "Moonlit Station"],
        8: ["Ravelyth City", "Prediction Bureau", "Hidden Archive"],
        9: ["Solvarya Railway", "Century City", "Central Platform"],
        10: ["Xaveren Airbase", "Border City", "War Control Room"],
        11: ["Elyvara Library", "Old Letter Box", "Riverside Street"],
        12: ["Neravelle", "Photograph Studio", "Future Alley"],
        13: ["Vaerith District", "Rainy Station", "Apartment Rooftop"],
        14: ["Lunavyr Street", "Moon Garden", "Old Bridge"],
        15: ["Averlyn School", "Riverside Park", "Train Station"],
        16: ["Neyvara City", "Message Center", "Archive Room"],
        17: ["Elvaria Town", "Glass Workshop", "Memory Garden"],
        18: ["Virelya Station", "Winter Train", "Empty Platform"],
        19: ["Caelora Road", "Mountain Village", "Crossroads"],
        20: ["Seravyn School", "Quiet Café", "School Rooftop"],
        21: ["Mouravia District", "Old Waiting Place", "Memorial Street"],
        22: ["Noxelya Apartment", "Memory Corridor", "Notebook Room"],
        23: ["Vaelora City", "Departure Station", "Rainy Square"],
        24: ["Eryndra Town", "Old Music Room", "Memory Hill"],
        25: ["Neylith City", "Recording Studio", "Abandoned House"],
        26: ["Auralyne City", "Old Speaker Tower", "Underground Echo Chamber"],
        27: ["Velmora City", "Memory Clinic", "Artificial Memory Room"],
        28: ["Seyravia Station", "Mountain Road", "Final Destination"],
        29: ["Oryvane District", "Quiet Café", "Riverside Path"],
        30: ["Luminarae", "Memory Forest", "Glass Memory Palace"],
    }

    names = base_names[anime_id]

    for number, name in enumerate(names, 1):
        add(
            anime_id,
            number,
            name,
            "story location",
            "A distinct location created for anime {}.".format(anime_id),
            "cinematic anime environment",
            "supports the narrative progression",
        )


def get_locations(anime_id: int) -> List[Dict]:
    return [
        asdict(item)
        for item in LOCATIONS
        if item.anime_id == anime_id
    ]


def all_locations() -> List[Dict]:
    return [asdict(item) for item in LOCATIONS]


if __name__ == "__main__":
    print("Locations:", len(LOCATIONS))
