"""
AJVYRA Game 106 - Fashion Designer
Genre: Creative Simulation
"""

from dataclasses import dataclass


@dataclass
class Outfit:
    top: str
    bottom: str
    shoes: str
    accessory: str


class FashionDesigner:
    title = "Fashion Designer"
    character = "Sera Vane"

    STYLE_RULES = {
        "formal": {
            "top": {"blazer", "shirt"},
            "bottom": {"trousers", "skirt"},
            "shoes": {"loafers", "heels"},
            "accessory": {"watch", "brooch"},
        },
        "street": {
            "top": {"hoodie", "jacket"},
            "bottom": {"jeans", "cargo"},
            "shoes": {"sneakers", "boots"},
            "accessory": {"cap", "chain"},
        },
        "sport": {
            "top": {"jersey", "tank"},
            "bottom": {"shorts", "trackpants"},
            "shoes": {"runners"},
            "accessory": {"wristband", "cap"},
        },
    }

    def __init__(self):
        self.score = 0
        self.collection = []

    def design(self, style, outfit):
        style = style.lower()

        if style not in self.STYLE_RULES:
            return 0

        rules = self.STYLE_RULES[style]
        score = 0

        if outfit.top in rules["top"]:
            score += 25
        if outfit.bottom in rules["bottom"]:
            score += 25
        if outfit.shoes in rules["shoes"]:
            score += 30
        if outfit.accessory in rules["accessory"]:
            score += 20

        self.score += score
        self.collection.append(
            {
                "style": style,
                "outfit": outfit,
                "score": score,
            }
        )

        return score

    def preview(self, outfit):
        return {
            "designer": self.character,
            "top": outfit.top,
            "bottom": outfit.bottom,
            "shoes": outfit.shoes,
            "accessory": outfit.accessory,
        }

    def snapshot(self):
        return {
            "designer": self.character,
            "total_score": self.score,
            "designs": len(self.collection),
        }


def create_game():
    return FashionDesigner()


if __name__ == "__main__":
    game = create_game()

    outfit = Outfit(
        top="blazer",
        bottom="trousers",
        shoes="loafers",
        accessory="watch",
    )

    print(game.design("formal", outfit))
    print(game.snapshot())
