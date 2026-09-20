from dataclasses import dataclass, asdict, field
from typing import List, Dict


@dataclass
class CharacterAppearance:
    character_id: str

    height: str = ""
    body_type: str = ""

    skin_description: str = ""
    hair_style: str = ""
    hair_color: str = ""

    eye_shape: str = ""
    eye_color: str = ""

    face_shape: str = ""
    distinctive_features: List[str] = field(default_factory=list)

    everyday_clothing: str = ""
    formal_clothing: str = ""
    action_clothing: str = ""

    accessories: List[str] = field(default_factory=list)

    color_palette: List[str] = field(default_factory=list)

    visual_prompt: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class CharacterDesignManager:

    def __init__(self):
        self.designs: Dict[str, CharacterAppearance] = {}

    def create_design(
        self,
        character_id: str,
        **kwargs
    ) -> CharacterAppearance:

        if character_id in self.designs:
            raise ValueError(
                "A design already exists for this character."
            )

        design = CharacterAppearance(
            character_id=character_id,
            **kwargs
        )

        self.designs[character_id] = design
        return design

    def get_design(
        self,
        character_id: str
    ) -> CharacterAppearance | None:

        return self.designs.get(character_id)

    def visual_prompt(
        self,
        character_id: str
    ) -> str:

        design = self.get_design(character_id)

        if design is None:
            raise KeyError("Character design not found.")

        return design.visual_prompt

    def export_all(self) -> List[Dict]:
        return [
            design.to_dict()
            for design in self.designs.values()
        ]


if __name__ == "__main__":
    manager = CharacterDesignManager()

    design = manager.create_design(
        "CHAR-DEMO",
        height="tall",
        body_type="slim",
        hair_style="messy layered",
        hair_color="silver-black",
        eye_color="deep violet",
        face_shape="sharp",
        everyday_clothing="dark oversized jacket",
        accessories=["small metal pendant"],
        visual_prompt=(
            "Original anime character, consistent appearance, "
            "silver-black layered hair, deep violet eyes."
        )
    )

    print(design.to_dict())
