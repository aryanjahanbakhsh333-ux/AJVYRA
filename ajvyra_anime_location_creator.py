from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class AnimeLocation:
    location_id: str
    name: str

    location_type: str = "unknown"

    country: str = ""
    city: str = ""
    real_world: bool = False

    description: str = ""
    atmosphere: str = ""

    time_variants: List[str] = field(default_factory=list)
    visual_details: List[str] = field(default_factory=list)

    recurring: bool = False

    def to_dict(self) -> Dict:
        return asdict(self)


class LocationCreator:

    def __init__(self):
        self.locations: Dict[str, AnimeLocation] = {}

    def create(
        self,
        location_id: str,
        name: str,
        location_type: str,
        description: str = "",
        real_world: bool = False,
        city: str = "",
        country: str = ""
    ) -> AnimeLocation:

        if location_id in self.locations:
            raise ValueError("Location already exists.")

        location = AnimeLocation(
            location_id=location_id,
            name=name,
            location_type=location_type,
            description=description,
            real_world=real_world,
            city=city,
            country=country
        )

        self.locations[location_id] = location
        return location

    def get(
        self,
        location_id: str
    ) -> AnimeLocation | None:

        return self.locations.get(location_id)

    def all(self) -> List[AnimeLocation]:
        return list(self.locations.values())


if __name__ == "__main__":
    creator = LocationCreator()

    location = creator.create(
        "LOC-001",
        "Rain District",
        "city_street",
        "A quiet urban street after midnight.",
        real_world=False
    )

    print(location.to_dict())
