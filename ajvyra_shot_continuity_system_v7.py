58 — ajvyra_shot_continuity_system_v7.py

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATE = ROOT / "ajvyra_shots" / "continuity.json"


class ContinuitySystem:

    def __init__(self):
        self.state = self._load()

    def _load(self):

        if not STATE.exists():
            return {
                "characters": {},
                "locations": {},
                "visual_style": (
                    "cinematic original anime, "
                    "consistent character design"
                ),
                "recent_shots": [],
            }

        try:
            return json.loads(
                STATE.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return {
                "characters": {},
                "locations": {},
                "visual_style": (
                    "cinematic original anime"
                ),
                "recent_shots": [],
            }

    def save(self):

        STATE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        STATE.write_text(
            json.dumps(
                self.state,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def register_character(
        self,
        name: str,
        description: str,
    ):

        self.state["characters"][name] = {
            "description": description
        }

        self.save()

    def register_location(
        self,
        name: str,
        description: str,
    ):

        self.state["locations"][name] = {
            "description": description
        }

        self.save()

    def context(self) -> str:

        characters = []

        for name, data in self.state[
            "characters"
        ].items():

            characters.append(
                f"{name}: "
                f"{data['description']}"
            )

        locations = []

        for name, data in self.state[
            "locations"
        ].items():

            locations.append(
                f"{name}: "
                f"{data['description']}"
            )

        return f"""
VISUAL STYLE:
{self.state["visual_style"]}

CHARACTERS:
{"; ".join(characters)}

LOCATIONS:
{"; ".join(locations)}

CONTINUITY:
Maintain the exact established character
appearance, clothing, hairstyle, age,
colors, proportions and visual identity.
Do not redesign established characters.
"""
