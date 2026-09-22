"""
AJVYRA AI CONTENT DIRECTOR

Creative control layer for all 30 anime and 70 games.

The director generates deterministic, unique production specifications
from project IDs and story seeds.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


ANIME_GENRES = (
    "Fantasy",
    "Action",
    "Sad",
    "Heartbreak",
    "Romance",
    "Horror",
)

AUDIO_LANGUAGES = ("fa", "ja")
SUBTITLE_LANGUAGES = ("en", "fa", "ja")

VISUAL_STYLES = (
    "cinematic anime realism",
    "dark cinematic anime",
    "emotional anime drama",
    "fantasy cinematic anime",
    "psychological anime",
    "horror cinematic anime",
    "rainy urban anime",
    "dreamlike anime",
)

FANTASY_NAMES = [
    "Aevrith",
    "Nyrelia",
    "Vaerion",
    "Elyndra",
    "Kaevryn",
    "Liorvane",
    "Seylith",
    "Orivelle",
    "Veyrane",
    "Auralith",
    "Neyvra",
    "Caelvyn",
    "Ravelya",
    "Eryvane",
    "Solryth",
    "Vaelith",
    "Mirevyn",
    "Lunerya",
    "Zevrane",
    "Oryndel",
    "Velrya",
    "Seraviel",
    "Noxira",
    "Aevora",
]


@dataclass
class AnimeCreativeSpec:
    anime_id: int
    title: str
    genres: List[str]
    logline: str
    synopsis: str
    themes: List[str]
    characters: List[Dict[str, Any]]
    locations: List[Dict[str, Any]]
    events: List[Dict[str, Any]]
    visual_style: str
    poster_concept: Dict[str, Any]
    audio_languages: List[str] = field(
        default_factory=lambda: list(AUDIO_LANGUAGES)
    )
    subtitle_languages: List[str] = field(
        default_factory=lambda: list(SUBTITLE_LANGUAGES)
    )
    duration_seconds: int = 1800

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GameCreativeSpec:
    game_id: int
    title: str
    genres: List[str]
    premise: str
    world: Dict[str, Any]
    characters: List[Dict[str, Any]]
    mechanics: List[str]
    levels: List[Dict[str, Any]]
    visual_style: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AJVYRAContentDirector:

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()

        self.content_root = (
            self.root / "generated" / "content"
        )

        self.content_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ---------------------------------------------------------
    # DETERMINISTIC RANDOMNESS
    # ---------------------------------------------------------

    def _rng(self, namespace: str) -> random.Random:
        digest = hashlib.sha256(
            namespace.encode("utf-8")
        ).hexdigest()

        seed = int(digest[:16], 16)

        return random.Random(seed)

    def _slug(self, value: str) -> str:
        value = value.lower().strip()
        value = re.sub(r"[^a-z0-9]+", "-", value)
        return value.strip("-")

    # ---------------------------------------------------------
    # ANIME
    # ---------------------------------------------------------

    def create_anime_spec(
        self,
        anime_id: int,
        title: str,
    ) -> AnimeCreativeSpec:

        rng = self._rng(f"anime:{anime_id}:{title}")

        genre_pool = list(ANIME_GENRES)

        # Each anime receives 2-3 genres from the requested universe.
        count = 2 + (anime_id % 2)

        genres = rng.sample(
            genre_pool,
            min(count, len(genre_pool)),
        )

        protagonist = self._unique_character(
            rng,
            role="protagonist",
            index=0,
        )

        second = self._unique_character(
            rng,
            role="deuteragonist",
            index=1,
        )

        antagonist = self._unique_character(
            rng,
            role="antagonist",
            index=2,
        )

        characters = [
            protagonist,
            second,
            antagonist,
        ]

        locations = self._locations(
            rng,
            title,
            genres,
        )

        events = self._events(
            rng,
            title,
            genres,
            characters,
            locations,
        )

        themes = self._themes(rng, genres)

        logline = self._logline(
            title,
            genres,
            protagonist,
            second,
        )

        synopsis = self._synopsis(
            title,
            genres,
            protagonist,
            second,
            antagonist,
        )

        visual_style = rng.choice(
            list(VISUAL_STYLES)
        )

        poster = self._poster_concept(
            rng,
            title,
            genres,
            characters,
            locations,
        )

        spec = AnimeCreativeSpec(
            anime_id=anime_id,
            title=title,
            genres=genres,
            logline=logline,
            synopsis=synopsis,
            themes=themes,
            characters=characters,
            locations=locations,
            events=events,
            visual_style=visual_style,
            poster_concept=poster,
        )

        self._save_anime_spec(spec)

        return spec

    def _unique_character(
        self,
        rng: random.Random,
        role: str,
        index: int,
    ) -> Dict[str, Any]:

        name_a = rng.choice(FANTASY_NAMES)
        name_b = rng.choice(FANTASY_NAMES)

        while name_b == name_a:
            name_b = rng.choice(FANTASY_NAMES)

        name = f"{name_a} {name_b}"

        traits = rng.sample(
            [
                "reserved",
                "observant",
                "protective",
                "impulsive",
                "gentle",
                "haunted",
                "determined",
                "mysterious",
                "fearful",
                "loyal",
                "rebellious",
                "melancholic",
            ],
            3,
        )

        return {
            "id": f"character-{index + 1}",
            "name": name,
            "role": role,
            "age_style": rng.choice(
                ["teen", "young adult"]
            ),
            "traits": traits,
            "voice_identity": (
                f"voice_{index + 1}_{rng.randint(1000, 9999)}"
            ),
        }

    def _locations(
        self,
        rng: random.Random,
        title: str,
        genres: List[str],
    ) -> List[Dict[str, Any]]:

        candidates = [
            "rain-soaked city district",
            "abandoned railway station",
            "quiet coastal town",
            "forgotten forest",
            "old apartment complex",
            "mountain observatory",
            "night market",
            "empty school corridor",
            "underground archive",
            "fog-covered lakeside",
            "rooftop above the city",
            "ruined fantasy settlement",
        ]

        selected = rng.sample(candidates, 5)

        return [
            {
                "id": f"location-{i + 1}",
                "name": location.title(),
                "purpose": (
                    "primary"
                    if i == 0
                    else "secondary"
                ),
                "atmosphere": rng.choice(
                    [
                        "rain",
                        "fog",
                        "night",
                        "sunset",
                        "overcast",
                        "moonlight",
                    ]
                ),
            }
            for i, location in enumerate(selected)
        ]

    def _events(
        self,
        rng: random.Random,
        title: str,
        genres: List[str],
        characters: List[Dict[str, Any]],
        locations: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:

        templates = [
            "unexpected meeting",
            "hidden memory is revealed",
            "relationship changes",
            "character disappears",
            "danger arrives",
            "truth is discovered",
            "emotional confrontation",
            "false assumption collapses",
            "sacrifice becomes necessary",
            "final decision",
            "quiet aftermath",
            "new beginning",
        ]

        rng.shuffle(templates)

        events = []

        for i, event_name in enumerate(templates):
            events.append(
                {
                    "event_id": i + 1,
                    "title": event_name,
                    "timestamp_seconds": int(
                        (1800 / len(templates)) * i
                    ),
                    "characters": [
                        c["id"]
                        for c in characters[:2 + (i % 2)]
                    ],
                    "location": locations[
                        i % len(locations)
                    ]["id"],
                    "intensity": round(
                        0.35 + ((i % 6) * 0.1),
                        2,
                    ),
                }
            )

        return events

    def _themes(
        self,
        rng: random.Random,
        genres: List[str],
    ) -> List[str]:

        all_themes = [
            "identity",
            "memory",
            "loss",
            "trust",
            "love",
            "loneliness",
            "fear",
            "hope",
            "forgiveness",
            "choice",
            "belonging",
            "change",
        ]

        return rng.sample(
            all_themes,
            4,
        )

    def _logline(
        self,
        title: str,
        genres: List[str],
        protagonist: Dict[str, Any],
        second: Dict[str, Any],
    ) -> str:

        genre_text = ", ".join(genres)

        return (
            f"{protagonist['name']} is pulled into a "
            f"{genre_text.lower()} story when "
            f"{second['name']} changes the direction of "
            f"their life."
        )

    def _synopsis(
        self,
        title: str,
        genres: List[str],
        protagonist: Dict[str, Any],
        second: Dict[str, Any],
        antagonist: Dict[str, Any],
    ) -> str:

        return (
            f"{title} follows {protagonist['name']} through "
            f"a story shaped by {', '.join(g.lower() for g in genres)}. "
            f"The connection with {second['name']} begins quietly, "
            f"but hidden truths force them to confront "
            f"{antagonist['name']}. Every decision changes what "
            f"they believe about love, fear, memory and themselves."
        )

    def _poster_concept(
        self,
        rng: random.Random,
        title: str,
        genres: List[str],
        characters: List[Dict[str, Any]],
        locations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:

        composition = rng.choice(
            [
                "two-character cinematic composition",
                "single protagonist close-up",
                "silhouette against environment",
                "split emotional composition",
                "wide cinematic environment with characters",
            ]
        )

        lighting = rng.choice(
            [
                "cold moonlight",
                "rainy blue night",
                "warm sunset against darkness",
                "desaturated gray atmosphere",
                "deep cinematic shadows",
                "soft misty light",
            ]
        )

        return {
            "title": title,
            "composition": composition,
            "lighting": lighting,
            "genres": genres,
            "characters": [
                c["name"]
                for c in characters
            ],
            "location": locations[0]["name"],
            "mood": (
                "dark emotional cinematic "
                + ", ".join(genres)
            ),
            "must_be_story_specific": True,
            "avoid_generic_poster": True,
        }

    def _save_anime_spec(
        self,
        spec: AnimeCreativeSpec,
    ) -> None:

        path = (
            self.content_root
            / "anime"
            / f"anime_{spec.anime_id:02d}"
            / "creative_spec.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                spec.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # GAMES
    # ---------------------------------------------------------

    def create_game_spec(
        self,
        game_id: int,
        title: str | None = None,
    ) -> GameCreativeSpec:

        rng = self._rng(
            f"game:{game_id}:{title or ''}"
        )

        final_title = (
            title
            or f"AJVYRA Realm {game_id:02d}"
        )

        genres = rng.sample(
            [
                "RPG",
                "Action",
                "Adventure",
                "Fantasy",
                "Horror",
                "Mystery",
                "Survival",
            ],
            2,
        )

        characters = [
            self._unique_character(
                rng,
                role="player",
                index=0,
            ),
            self._unique_character(
                rng,
                role="ally",
                index=1,
            ),
            self._unique_character(
                rng,
                role="boss",
                index=2,
            ),
        ]

        mechanics = rng.sample(
            [
                "exploration",
                "combat",
                "dialogue choices",
                "inventory",
                "crafting",
                "stealth",
                "environment puzzles",
                "character progression",
                "branching quests",
                "boss encounters",
            ],
            5,
        )

        levels = [
            {
                "level": i,
                "name": f"Realm {i}",
                "objective": rng.choice(
                    [
                        "discover the hidden path",
                        "defeat the guardian",
                        "recover a lost artifact",
                        "solve the ancient puzzle",
                        "escape the corrupted zone",
                    ]
                ),
            }
            for i in range(1, 11)
        ]

        spec = GameCreativeSpec(
            game_id=game_id,
            title=final_title,
            genres=genres,
            premise=(
                f"{characters[0]['name']} enters a world "
                f"where every choice changes the path forward."
            ),
            world={
                "theme": rng.choice(
                    [
                        "dark fantasy",
                        "forgotten civilization",
                        "night city",
                        "mysterious island",
                        "dream realm",
                    ]
                ),
                "scale": "medium",
            },
            characters=characters,
            mechanics=mechanics,
            levels=levels,
            visual_style=rng.choice(
                list(VISUAL_STYLES)
            ),
        )

        path = (
            self.content_root
            / "games"
            / f"game_{game_id:02d}"
            / "creative_spec.json"
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                spec.to_dict(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return spec
