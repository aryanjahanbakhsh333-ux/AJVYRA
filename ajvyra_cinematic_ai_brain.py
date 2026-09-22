"""
AJVYRA CINEMATIC AI BRAIN
--------------------------
Independent intelligence layer for AJVYRA cinematic anime.

Responsibilities:
- Film-level state
- Long-term cinematic memory
- Story/character/world continuity
- Emotional state tracking
- Director decisions
- Production state
- Deterministic project snapshots

This module does NOT generate fake media.
It creates the intelligence/state required by real media engines.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


def stable_id(*parts: Any) -> str:
    raw = "::".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


@dataclass
class EmotionalState:
    primary: str = "neutral"
    secondary: str = "calm"

    intensity: float = 0.0
    tension: float = 0.0
    sadness: float = 0.0
    joy: float = 0.0
    fear: float = 0.0
    anger: float = 0.0
    love: float = 0.0
    hope: float = 0.0

    def normalize(self) -> None:
        self.intensity = clamp(self.intensity)
        self.tension = clamp(self.tension)
        self.sadness = clamp(self.sadness)
        self.joy = clamp(self.joy)
        self.fear = clamp(self.fear)
        self.anger = clamp(self.anger)
        self.love = clamp(self.love)
        self.hope = clamp(self.hope)


@dataclass
class CharacterMemory:
    character_id: str
    name: str

    emotional_state: EmotionalState = field(
        default_factory=EmotionalState
    )

    current_location: str = ""
    current_goal: str = ""
    current_conflict: str = ""

    known_characters: List[str] = field(default_factory=list)
    memories: List[str] = field(default_factory=list)
    injuries: List[str] = field(default_factory=list)
    clothing_state: str = ""

    relationship_states: Dict[str, str] = field(default_factory=dict)

    def remember(self, event: str, max_items: int = 100) -> None:
        if event and event not in self.memories:
            self.memories.append(event)

        if len(self.memories) > max_items:
            self.memories = self.memories[-max_items:]


@dataclass
class WorldMemory:
    locations: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    objects: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    rules: List[str] = field(default_factory=list)
    weather: str = "clear"
    time_of_day: str = "day"
    world_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FilmMemory:
    film_id: str
    title: str
    genre: str

    duration_seconds: int = 1800

    current_time: float = 0.0
    current_act: int = 1

    characters: Dict[str, CharacterMemory] = field(
        default_factory=dict
    )
    world: WorldMemory = field(
        default_factory=WorldMemory
    )

    emotional_history: List[Dict[str, Any]] = field(
        default_factory=list
    )

    continuity_events: List[Dict[str, Any]] = field(
        default_factory=list
    )

    director_decisions: List[Dict[str, Any]] = field(
        default_factory=list
    )

    production_flags: Dict[str, bool] = field(
        default_factory=dict
    )


class AJVYRACinematicAIBrain:
    """
    Central stateful intelligence for one cinematic film.

    The brain does not pretend to be a generative model by itself.
    It provides structured reasoning/state interfaces that actual
    AI providers can consume later.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        film_id: str,
        title: str,
        genre: str,
        duration_seconds: int = 1800,
        memory_path: Optional[str | Path] = None,
    ) -> None:
        self.memory_path = Path(memory_path) if memory_path else None

        self.memory = FilmMemory(
            film_id=film_id,
            title=title,
            genre=genre,
            duration_seconds=max(60, int(duration_seconds)),
        )

        self.memory.production_flags.update(
            {
                "story_locked": False,
                "characters_locked": False,
                "world_locked": False,
                "director_locked": False,
                "visual_ready": False,
                "audio_ready": False,
                "render_ready": False,
                "final_qc_passed": False,
            }
        )

        if self.memory_path and self.memory_path.exists():
            self.load()

    # ---------------------------------------------------------
    # Character memory
    # ---------------------------------------------------------

    def register_character(
        self,
        character_id: str,
        name: str,
        location: str = "",
        goal: str = "",
    ) -> CharacterMemory:
        if character_id in self.memory.characters:
            return self.memory.characters[character_id]

        character = CharacterMemory(
            character_id=character_id,
            name=name,
            current_location=location,
            current_goal=goal,
        )

        self.memory.characters[character_id] = character
        return character

    def get_character(
        self,
        character_id: str,
    ) -> Optional[CharacterMemory]:
        return self.memory.characters.get(character_id)

    def update_character(
        self,
        character_id: str,
        **changes: Any,
    ) -> CharacterMemory:
        character = self.memory.characters.get(character_id)

        if character is None:
            raise KeyError(
                f"Unknown cinematic character: {character_id}"
            )

        for key, value in changes.items():
            if hasattr(character, key):
                setattr(character, key, value)

        return character

    # ---------------------------------------------------------
    # World memory
    # ---------------------------------------------------------

    def register_location(
        self,
        location_id: str,
        name: str,
        description: str,
        visual_identity: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.memory.world.locations[location_id] = {
            "name": name,
            "description": description,
            "visual_identity": visual_identity or {},
        }

    def register_object(
        self,
        object_id: str,
        name: str,
        description: str,
    ) -> None:
        self.memory.world.objects[object_id] = {
            "name": name,
            "description": description,
        }

    # ---------------------------------------------------------
    # Emotional intelligence
    # ---------------------------------------------------------

    def set_character_emotion(
        self,
        character_id: str,
        emotion: EmotionalState,
    ) -> None:
        character = self.get_character(character_id)

        if character is None:
            raise KeyError(character_id)

        emotion.normalize()
        character.emotional_state = emotion

        self.memory.emotional_history.append(
            {
                "timestamp": self.memory.current_time,
                "character_id": character_id,
                "emotion": asdict(emotion),
            }
        )

    def get_dominant_emotion(
        self,
        character_id: str,
    ) -> str:
        character = self.get_character(character_id)

        if character is None:
            return "neutral"

        emotion = character.emotional_state

        values = {
            "sadness": emotion.sadness,
            "joy": emotion.joy,
            "fear": emotion.fear,
            "anger": emotion.anger,
            "love": emotion.love,
            "hope": emotion.hope,
        }

        return max(values, key=values.get)

    # ---------------------------------------------------------
    # Film timeline
    # ---------------------------------------------------------

    def advance_time(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("Film time cannot move backwards.")

        self.memory.current_time = min(
            self.memory.duration_seconds,
            self.memory.current_time + seconds,
        )

        self._update_act()

    def seek(self, seconds: float) -> None:
        self.memory.current_time = max(
            0.0,
            min(
                self.memory.duration_seconds,
                float(seconds),
            ),
        )
        self._update_act()

    def _update_act(self) -> None:
        progress = (
            self.memory.current_time
            / self.memory.duration_seconds
        )

        if progress < 0.25:
            self.memory.current_act = 1
        elif progress < 0.70:
            self.memory.current_act = 2
        else:
            self.memory.current_act = 3

    # ---------------------------------------------------------
    # Continuity
    # ---------------------------------------------------------

    def record_event(
        self,
        event_type: str,
        description: str,
        importance: float = 0.5,
        **metadata: Any,
    ) -> str:
        event_id = stable_id(
            self.memory.film_id,
            self.memory.current_time,
            event_type,
            description,
        )

        event = {
            "id": event_id,
            "time": self.memory.current_time,
            "type": event_type,
            "description": description,
            "importance": clamp(importance),
            "metadata": metadata,
        }

        self.memory.continuity_events.append(event)
        return event_id

    def continuity_snapshot(self) -> Dict[str, Any]:
        return {
            "film_id": self.memory.film_id,
            "time": self.memory.current_time,
            "act": self.memory.current_act,
            "characters": {
                cid: {
                    "location": char.current_location,
                    "goal": char.current_goal,
                    "conflict": char.current_conflict,
                    "emotion": asdict(
                        char.emotional_state
                    ),
                    "injuries": list(char.injuries),
                    "clothing": char.clothing_state,
                }
                for cid, char in self.memory.characters.items()
            },
            "world": asdict(self.memory.world),
        }

    # ---------------------------------------------------------
    # Director memory
    # ---------------------------------------------------------

    def record_director_decision(
        self,
        decision_type: str,
        decision: str,
        reason: str = "",
        confidence: float = 0.8,
    ) -> None:
        self.memory.director_decisions.append(
            {
                "time": self.memory.current_time,
                "type": decision_type,
                "decision": decision,
                "reason": reason,
                "confidence": clamp(confidence),
            }
        )

    # ---------------------------------------------------------
    # Production state
    # ---------------------------------------------------------

    def set_flag(self, flag: str, value: bool) -> None:
        self.memory.production_flags[flag] = bool(value)

    def ready_for(self, stage: str) -> bool:
        requirements = {
            "visual": ["story_locked", "characters_locked"],
            "audio": ["story_locked", "characters_locked"],
            "render": [
                "visual_ready",
                "audio_ready",
            ],
            "publish": [
                "render_ready",
                "final_qc_passed",
            ],
        }

        required = requirements.get(stage, [])

        return all(
            self.memory.production_flags.get(
                item,
                False,
            )
            for item in required
        )

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    def snapshot(self) -> Dict[str, Any]:
        return {
            "brain_version": self.VERSION,
            "saved_at": time.time(),
            "memory": asdict(self.memory),
        }

    def save(
        self,
        path: Optional[str | Path] = None,
    ) -> Path:
        target = Path(path) if path else self.memory_path

        if target is None:
            raise ValueError(
                "No memory path supplied."
            )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                self.snapshot(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target

    def load(
        self,
        path: Optional[str | Path] = None,
    ) -> None:
        target = Path(path) if path else self.memory_path

        if target is None or not target.exists():
            return

        data = json.loads(
            target.read_text(
                encoding="utf-8"
            )
        )

        raw = data["memory"]

        self.memory = FilmMemory(
            film_id=raw["film_id"],
            title=raw["title"],
            genre=raw["genre"],
            duration_seconds=raw["duration_seconds"],
            current_time=raw["current_time"],
            current_act=raw["current_act"],
            world=WorldMemory(**raw["world"]),
            production_flags=raw.get(
                "production_flags",
                {},
            ),
        )

        for cid, raw_char in raw.get(
            "characters",
            {},
        ).items():
            emotion = EmotionalState(
                **raw_char.pop(
                    "emotional_state",
                    {},
                )
            )

            self.memory.characters[cid] = (
                CharacterMemory(
                    emotional_state=emotion,
                    **raw_char,
                )
            )

        self.memory.emotional_history = raw.get(
            "emotional_history",
            [],
        )

        self.memory.continuity_events = raw.get(
            "continuity_events",
            [],
        )

        self.memory.director_decisions = raw.get(
            "director_decisions",
            [],
        )


if __name__ == "__main__":
    brain = AJVYRACinematicAIBrain(
        film_id="veyllora-film-01",
        title="Veylora",
        genre="dark_fantasy",
        memory_path=(
            "generated/cinematic/veyllora/"
            "cinematic_memory.json"
        ),
    )

    brain.register_character(
        "char_01",
        "Veylora",
        location="Moonlit Harbor",
        goal="Find the missing letter",
    )

    brain.set_character_emotion(
        "char_01",
        EmotionalState(
            primary="loneliness",
            secondary="hope",
            intensity=0.72,
            sadness=0.76,
            hope=0.31,
        ),
    )

    brain.register_location(
        "loc_01",
        "Moonlit Harbor",
        "A silent coastal city beneath cold rain.",
        {
            "palette": "blue_gray",
            "weather": "rain",
        },
    )

    brain.record_event(
        "character_realization",
        "Veylora realizes the letter was never sent.",
        importance=0.91,
    )

    brain.record_director_decision(
        "camera",
        "Slow push-in",
        "The realization should feel intimate.",
    )

    brain.save()

    print(
        json.dumps(
            brain.continuity_snapshot(),
            ensure_ascii=False,
            indent=2,
        )
    )
