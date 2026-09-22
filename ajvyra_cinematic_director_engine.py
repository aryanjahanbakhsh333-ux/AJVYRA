"""
AJVYRA CINEMATIC DIRECTOR ENGINE
--------------------------------
Digital director layer for AJVYRA cinematic anime.

Transforms story/emotional/character state into cinematic
direction decisions:
- camera language
- framing
- movement
- lighting
- pacing
- acting direction
- silence
- sound emphasis

This is a decision engine, not a fake video generator.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class CameraPlan:
    shot_scale: str
    angle: str
    movement: str
    lens_feel: str
    focus_target: str
    depth_of_field: str


@dataclass
class ActingPlan:
    body_language: str
    facial_expression: str
    eye_direction: str
    movement_energy: float
    speech_energy: float
    pause_before_dialogue: float


@dataclass
class LightingPlan:
    key_light: str
    fill_light: str
    contrast: float
    color_temperature: str
    atmosphere: str


@dataclass
class SoundPlan:
    ambience: str
    music_energy: float
    music_character: str
    sfx_priority: str
    silence_duration: float


@dataclass
class CinematicDirection:
    moment_id: str
    emotion: str
    intensity: float

    camera: CameraPlan
    acting: ActingPlan
    lighting: LightingPlan
    sound: SoundPlan

    pacing: str
    visual_priority: str

    director_notes: List[str] = field(
        default_factory=list
    )


class AJVYRACinematicDirectorEngine:
    VERSION = "1.0.0"

    EMOTION_PRESETS = {
        "love": {
            "scale": "medium_close",
            "movement": "slow_push_in",
            "lighting": "soft_backlight",
            "temperature": "warm",
            "body": "subtle_forward_lean",
            "face": "soft_unguarded_expression",
            "eyes": "hold_eye_contact",
            "music": "intimate_strings",
        },
        "sadness": {
            "scale": "close_up",
            "movement": "very_slow_push_in",
            "lighting": "soft_side_light",
            "temperature": "cold",
            "body": "minimal_movement",
            "face": "restrained_sadness",
            "eyes": "downward_or_away",
            "music": "sparse_piano",
        },
        "fear": {
            "scale": "close_up",
            "movement": "slow_drift",
            "lighting": "low_key",
            "temperature": "cold",
            "body": "defensive_tension",
            "face": "controlled_fear",
            "eyes": "searching",
            "music": "low_drone",
        },
        "anger": {
            "scale": "medium_close",
            "movement": "controlled_forward_motion",
            "lighting": "hard_side_light",
            "temperature": "neutral_cold",
            "body": "rigid_shoulders",
            "face": "restrained_anger",
            "eyes": "direct_stare",
            "music": "low_percussion",
        },
        "hope": {
            "scale": "medium",
            "movement": "gentle_rise",
            "lighting": "soft_open_light",
            "temperature": "neutral_warm",
            "body": "relaxed_open_posture",
            "face": "quiet_hope",
            "eyes": "look_toward_light",
            "music": "rising_strings",
        },
        "neutral": {
            "scale": "medium",
            "movement": "static_or_subtle_drift",
            "lighting": "balanced_soft_light",
            "temperature": "neutral",
            "body": "natural_posture",
            "face": "natural_expression",
            "eyes": "contextual",
            "music": "ambient",
        },
    }

    GENRE_PRESETS = {
        "dark_fantasy": {
            "contrast": 0.82,
            "atmosphere": "mist_and_soft_particles",
            "visual_priority": (
                "character_emotion_and_environment"
            ),
        },
        "romance": {
            "contrast": 0.52,
            "atmosphere": "soft_depth_and_bokeh",
            "visual_priority": (
                "facial_expression_and_relationship"
            ),
        },
        "heartbreak": {
            "contrast": 0.72,
            "atmosphere": "rain_or_empty_space",
            "visual_priority": (
                "silence_and_micro_expression"
            ),
        },
        "horror": {
            "contrast": 0.95,
            "atmosphere": "darkness_and_unstable_space",
            "visual_priority": (
                "uncertainty_and_reaction"
            ),
        },
        "action": {
            "contrast": 0.88,
            "atmosphere": "dynamic_environment",
            "visual_priority": (
                "movement_and_spatial_clarity"
            ),
        },
        "fantasy": {
            "contrast": 0.68,
            "atmosphere": "magical_environment",
            "visual_priority": (
                "world_scale_and_character"
            ),
        },
        "sad": {
            "contrast": 0.64,
            "atmosphere": "quiet_empty_space",
            "visual_priority": (
                "emotion_and_memory"
            ),
        },
    }

    def __init__(
        self,
        genre: str,
    ) -> None:
        self.genre = genre.lower()

    # ---------------------------------------------------------
    # Main direction
    # ---------------------------------------------------------

    def direct(
        self,
        moment_id: str,
        emotion: str,
        intensity: float,
        character_name: str = "",
        dialogue_present: bool = False,
        location: str = "",
    ) -> CinematicDirection:

        emotion = emotion.lower().strip()

        preset = self.EMOTION_PRESETS.get(
            emotion,
            self.EMOTION_PRESETS["neutral"],
        )

        genre = self.GENRE_PRESETS.get(
            self.genre,
            self.GENRE_PRESETS["fantasy"],
        )

        intensity = max(
            0.0,
            min(1.0, float(intensity)),
        )

        camera = CameraPlan(
            shot_scale=self._scale_for_intensity(
                preset["scale"],
                intensity,
            ),
            angle=self._angle_for_emotion(
                emotion
            ),
            movement=preset["movement"],
            lens_feel=self._lens_for_emotion(
                emotion
            ),
            focus_target=(
                character_name
                if character_name
                else "primary_subject"
            ),
            depth_of_field=(
                "shallow"
                if intensity >= 0.65
                else "moderate"
            ),
        )

        acting = ActingPlan(
            body_language=preset["body"],
            facial_expression=preset["face"],
            eye_direction=preset["eyes"],
            movement_energy=round(
                self._movement_energy(
                    emotion,
                    intensity,
                ),
                3,
            ),
            speech_energy=round(
                self._speech_energy(
                    emotion,
                    intensity,
                    dialogue_present,
                ),
                3,
            ),
            pause_before_dialogue=round(
                self._dialogue_pause(
                    emotion,
                    intensity,
                ),
                2,
            ),
        )

        lighting = LightingPlan(
            key_light=preset["lighting"],
            fill_light=(
                "minimal"
                if intensity >= 0.7
                else "soft"
            ),
            contrast=genre["contrast"],
            color_temperature=preset[
                "temperature"
            ],
            atmosphere=genre["atmosphere"],
        )

        sound = SoundPlan(
            ambience=self._ambience(
                emotion,
                location,
            ),
            music_energy=round(
                self._music_energy(
                    emotion,
                    intensity,
                ),
                3,
            ),
            music_character=preset["music"],
            sfx_priority=(
                "high"
                if emotion in {
                    "fear",
                    "anger",
                }
                else "medium"
            ),
            silence_duration=round(
                self._silence_duration(
                    emotion,
                    intensity,
                    dialogue_present,
                ),
                2,
            ),
        )

        notes = self._director_notes(
            emotion,
            intensity,
            dialogue_present,
        )

        return CinematicDirection(
            moment_id=moment_id,
            emotion=emotion,
            intensity=intensity,
            camera=camera,
            acting=acting,
            lighting=lighting,
            sound=sound,
            pacing=self._pacing(
                emotion,
                intensity,
            ),
            visual_priority=genre[
                "visual_priority"
            ],
            director_notes=notes,
        )

    # ---------------------------------------------------------
    # Decision logic
    # ---------------------------------------------------------

    @staticmethod
    def _scale_for_intensity(
        base: str,
        intensity: float,
    ) -> str:
        if intensity >= 0.88:
            return "extreme_close_or_dynamic_medium"

        if intensity >= 0.70:
            return "close_or_medium_close"

        return base

    @staticmethod
    def _angle_for_emotion(
        emotion: str,
    ) -> str:
        return {
            "fear": "slightly_off_axis",
            "anger": "subtle_low_angle",
            "sadness": "eye_level_or_slight_high_angle",
            "love": "eye_level",
            "hope": "slight_open_upward_angle",
        }.get(
            emotion,
            "eye_level",
        )

    @staticmethod
    def _lens_for_emotion(
        emotion: str,
    ) -> str:
        return {
            "love": "portrait_cinematic",
            "sadness": "compressed_intimate",
            "fear": "slightly_wide_uncomfortable",
            "anger": "compressed_powerful",
            "hope": "open_cinematic",
        }.get(
            emotion,
            "natural_cinematic",
        )

    @staticmethod
    def _movement_energy(
        emotion: str,
        intensity: float,
    ) -> float:
        base = {
            "love": 0.25,
            "sadness": 0.12,
            "fear": 0.48,
            "anger": 0.72,
            "hope": 0.35,
            "neutral": 0.20,
        }.get(emotion, 0.20)

        return min(
            1.0,
            base + intensity * 0.25,
        )

    @staticmethod
    def _speech_energy(
        emotion: str,
        intensity: float,
        dialogue_present: bool,
    ) -> float:
        if not dialogue_present:
            return 0.0

        base = {
            "love": 0.30,
            "sadness": 0.22,
            "fear": 0.52,
            "anger": 0.78,
            "hope": 0.42,
            "neutral": 0.35,
        }.get(emotion, 0.35)

        return min(
            1.0,
            base + intensity * 0.20,
        )

    @staticmethod
    def _dialogue_pause(
        emotion: str,
        intensity: float,
    ) -> float:
        if emotion == "sadness":
            return 0.8 + intensity * 1.3

        if emotion == "fear":
            return 0.5 + intensity * 0.8

        if emotion == "love":
            return 0.25 + intensity * 0.5

        return 0.15 + intensity * 0.35

    @staticmethod
    def _music_energy(
        emotion: str,
        intensity: float,
    ) -> float:
        if emotion == "sadness":
            return 0.20 + intensity * 0.20

        if emotion == "love":
            return 0.25 + intensity * 0.30

        if emotion == "anger":
            return 0.45 + intensity * 0.45

        if emotion == "fear":
            return 0.30 + intensity * 0.40

        return 0.20 + intensity * 0.25

    @staticmethod
    def _silence_duration(
        emotion: str,
        intensity: float,
        dialogue_present: bool,
    ) -> float:
        if not dialogue_present:
            return 0.0

        if emotion == "sadness":
            return 0.8 + intensity * 1.2

        if emotion == "fear":
            return 0.4 + intensity * 0.8

        return 0.2 + intensity * 0.4

    @staticmethod
    def _ambience(
        emotion: str,
        location: str,
    ) -> str:
        location = location or "environment"

        presets = {
            "sadness": (
                f"quiet {location}, distant ambience, "
                "subtle rain or wind"
            ),
            "fear": (
                f"low-detail {location} ambience, "
                "distant environmental movement"
            ),
            "love": (
                f"soft {location} ambience, "
                "gentle environmental detail"
            ),
            "anger": (
                f"tense {location} ambience, "
                "strong environmental presence"
            ),
        }

        return presets.get(
            emotion,
            f"natural ambience of {location}",
        )

    @staticmethod
    def _pacing(
        emotion: str,
        intensity: float,
    ) -> str:
        if emotion == "anger" and intensity > 0.7:
            return "fast"

        if emotion == "fear":
            return "uneven"

        if emotion == "sadness":
            return "slow"

        if emotion == "love":
            return "slow_intimate"

        return "measured"

    @staticmethod
    def _director_notes(
        emotion: str,
        intensity: float,
        dialogue_present: bool,
    ) -> List[str]:
        notes = []

        if emotion == "sadness":
            notes.append(
                "Do not overplay the emotion."
            )
            notes.append(
                "Allow silence and micro-expression to carry meaning."
            )

        if emotion == "love":
            notes.append(
                "Prioritize eye contact and small gestures."
            )

        if emotion == "fear":
            notes.append(
                "Reveal information gradually."
            )

        if emotion == "anger":
            notes.append(
                "Keep physical acting readable rather than chaotic."
            )

        if intensity > 0.85:
            notes.append(
                "This is a major emotional peak."
            )

        if dialogue_present:
            notes.append(
                "Synchronize acting with vocal pauses."
            )

        return notes

    # ---------------------------------------------------------
    # Export
    # ---------------------------------------------------------

    def save_direction(
        self,
        direction: CinematicDirection,
        path: str | Path,
    ) -> Path:
        target = Path(path)
        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            json.dumps(
                asdict(direction),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return target


if __name__ == "__main__":
    director = (
        AJVYRACinematicDirectorEngine(
            genre="dark_fantasy"
        )
    )

    direction = director.direct(
        moment_id="veyllora_01_moment_001",
        emotion="sadness",
        intensity=0.87,
        character_name="Veylora",
        dialogue_present=True,
        location="Moonlit Harbor",
    )

    print(
        json.dumps(
            asdict(direction),
            ensure_ascii=False,
            indent=2,
        )
    )
