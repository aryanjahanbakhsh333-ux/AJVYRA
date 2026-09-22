from __future__ import annotations

import hashlib
import json
import math
import random
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


ENGINE_NAME = "AJVYRA Anime Scene Shot Director"
ENGINE_VERSION = "1.0.0"


# ============================================================
# HELPERS
# ============================================================

def utc_timestamp() -> str:
    return time.strftime(
        "%Y-%m-%dT%H:%M:%SZ",
        time.gmtime()
    )


def stable_seed(*values: Any) -> int:
    raw = "|".join(
        str(value)
        for value in values
    )

    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).digest()

    return int.from_bytes(
        digest[:4],
        "big"
    )


def safe_slug(value: str) -> str:
    result = []

    for char in value.lower():
        if char.isalnum():
            result.append(char)
        elif char in {" ", "-", "_"}:
            result.append("_")

    return "".join(result).strip("_") or "unnamed"


def write_json(
    path: Path,
    data: Any
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    with temporary.open(
        "w",
        encoding="utf-8"
    ) as handle:

        json.dump(
            data,
            handle,
            ensure_ascii=False,
            indent=2
        )

    temporary.replace(path)


# ============================================================
# CAMERA
# ============================================================

@dataclass
class CameraPlan:

    shot_type: str
    angle: str
    movement: str
    lens_style: str
    framing: str
    focus_subject: str

    def normalized(self) -> Dict[str, Any]:

        return asdict(self)


class AJVYRACameraDirector:

    SHOT_TYPES = [
        "extreme wide",
        "wide",
        "medium wide",
        "medium",
        "medium close-up",
        "close-up",
        "extreme close-up",
    ]

    ANGLES = [
        "eye level",
        "low angle",
        "high angle",
        "over shoulder",
        "profile",
        "front",
        "rear three-quarter",
    ]

    MOVEMENTS = [
        "static",
        "slow push-in",
        "slow pull-out",
        "left tracking",
        "right tracking",
        "gentle orbit",
        "vertical tilt",
        "handheld subtle",
    ]

    def create(
        self,
        shot_number: int,
        emotional_intensity: float,
        action: str,
        subject: str,
    ) -> CameraPlan:

        intensity = max(
            0.0,
            min(
                1.0,
                emotional_intensity
            )
        )

        if intensity >= 0.85:

            shot_type = "close-up"

            movement = (
                "slow push-in"
                if shot_number % 2 == 0
                else "handheld subtle"
            )

        elif intensity >= 0.60:

            shot_type = "medium close-up"
            movement = "slow push-in"

        elif intensity >= 0.35:

            shot_type = "medium"
            movement = "gentle orbit"

        else:

            shot_type = (
                "wide"
                if shot_number % 3 == 0
                else "medium"
            )

            movement = "static"

        if "running" in action.lower():

            movement = "tracking"

        if "fight" in action.lower():

            movement = "handheld subtle"

        angle = (
            "low angle"
            if intensity >= 0.90
            else "eye level"
        )

        return CameraPlan(
            shot_type=shot_type,
            angle=angle,
            movement=movement,
            lens_style=(
                "cinematic shallow depth of field"
            ),
            framing=shot_type,
            focus_subject=subject,
        )


# ============================================================
# LIGHTING
# ============================================================

@dataclass
class LightingPlan:

    key_light: str
    fill_light: str
    atmosphere: str
    color_temperature: str
    contrast: str

    def normalized(self):
        return asdict(self)


class AJVYRALightingDirector:

    def create(
        self,
        emotion: str,
        environment: str,
        time_of_day: str,
    ) -> LightingPlan:

        emotion_lower = emotion.lower()
        environment_lower = environment.lower()

        if (
            "sad" in emotion_lower
            or "heartbreak" in emotion_lower
        ):

            key = (
                "soft cold moonlight"
            )

            fill = (
                "very low neutral fill"
            )

            atmosphere = (
                "light mist and subtle rain haze"
            )

            temperature = "cold blue-gray"

        elif "angry" in emotion_lower:

            key = (
                "hard directional side light"
            )

            fill = (
                "deep shadow fill"
            )

            atmosphere = (
                "dense dramatic atmosphere"
            )

            temperature = "cool red-blue contrast"

        elif "happy" in emotion_lower:

            key = (
                "soft warm sunlight"
            )

            fill = (
                "gentle warm ambient fill"
            )

            atmosphere = (
                "clean bright atmosphere"
            )

            temperature = "warm golden"

        else:

            key = (
                "cinematic soft key light"
            )

            fill = (
                "controlled neutral fill"
            )

            atmosphere = (
                "subtle cinematic atmosphere"
            )

            temperature = (
                "neutral cinematic"
            )

        if "rain" in environment_lower:

            atmosphere += (
                ", visible rain particles "
                "and wet reflective surfaces"
            )

        return LightingPlan(
            key_light=key,
            fill_light=fill,
            atmosphere=atmosphere,
            color_temperature=temperature,
            contrast="cinematic",
        )


# ============================================================
# SHOT MODEL
# ============================================================

@dataclass
class ShotSpec:

    anime_id: str
    episode_id: str
    scene_id: str
    shot_id: str

    shot_number: int

    duration_seconds: float

    location_id: str

    characters: List[str]

    dialogue: List[Dict[str, Any]]

    action: str
    emotion: str

    camera: CameraPlan
    lighting: LightingPlan

    visual_prompt: str
    negative_prompt: str

    previous_shot_id: Optional[str]
    next_shot_id: Optional[str]

    continuity_seed: int

    reference_images: List[str] = field(
        default_factory=list
    )

    status: str = "planned"

    generated_media: Dict[str, Any] = field(
        default_factory=dict
    )

    def normalized(self):

        data = asdict(self)

        return data


# ============================================================
# SCENE MODEL
# ============================================================

@dataclass
class SceneSpec:

    anime_id: str
    episode_id: str
    scene_id: str

    title: str
    location_id: str

    characters: List[str]

    objective: str
    conflict: str

    emotion: str

    time_of_day: str

    environment: str

    target_duration_seconds: float

    shots: List[ShotSpec] = field(
        default_factory=list
    )

    def normalized(self):

        return {
            "anime_id": self.anime_id,
            "episode_id": self.episode_id,
            "scene_id": self.scene_id,
            "title": self.title,
            "location_id": self.location_id,
            "characters": self.characters,
            "objective": self.objective,
            "conflict": self.conflict,
            "emotion": self.emotion,
            "time_of_day": self.time_of_day,
            "environment": self.environment,
            "target_duration_seconds": (
                self.target_duration_seconds
            ),
            "shots": [
                shot.normalized()
                for shot in self.shots
            ],
        }


# ============================================================
# DIALOGUE
# ============================================================

@dataclass
class DialogueLine:

    character_id: str
    text: str

    language: str = "ja"

    emotion: str = "neutral"

    estimated_duration: float = 2.5

    line_id: str = ""

    def normalized(self):

        return asdict(self)


# ============================================================
# DIALOGUE TIMING
# ============================================================

class AJVYRADialogueTiming:

    @staticmethod
    def estimate(
        text: str,
        language: str,
    ) -> float:

        length = len(
            text.strip()
        )

        if language.lower() in {
            "ja",
            "japanese",
        }:

            base = length * 0.095

        elif language.lower() in {
            "fa",
            "persian",
        }:

            base = length * 0.075

        else:

            base = length * 0.085

        return max(
            1.0,
            min(
                12.0,
                base + 0.25
            )
        )


# ============================================================
# PROMPT DIRECTOR
# ============================================================

class AJVYRAVisualPromptDirector:

    def build(
        self,
        scene: SceneSpec,
        shot_number: int,
        action: str,
        emotion: str,
        camera: CameraPlan,
        lighting: LightingPlan,
    ) -> str:

        characters = ", ".join(
            scene.characters
        )

        return (
            "cinematic original anime scene, "
            "high visual consistency, "
            "feature-film quality composition, "
            f"characters: {characters}, "
            f"location: {scene.location_id}, "
            f"environment: {scene.environment}, "
            f"action: {action}, "
            f"emotion: {emotion}, "
            f"camera framing: {camera.framing}, "
            f"camera angle: {camera.angle}, "
            f"camera movement: {camera.movement}, "
            f"lighting: {lighting.key_light}, "
            f"atmosphere: {lighting.atmosphere}, "
            f"color temperature: "
            f"{lighting.color_temperature}, "
            "consistent character identity, "
            "consistent clothing, "
            "consistent environment geometry, "
            "cinematic depth, "
            "detailed eyes, "
            "natural body proportions, "
            "coherent hands and limbs, "
            "professional animation composition"
        )

    def negative_prompt(self) -> str:

        return (
            "different character identity, "
            "different hairstyle, "
            "different eye color, "
            "different clothing, "
            "bad anatomy, "
            "extra limbs, "
            "missing limbs, "
            "extra fingers, "
            "missing fingers, "
            "duplicate character, "
            "deformed face, "
            "inconsistent background, "
            "random text, "
            "watermark, "
            "logo, "
            "blurry, "
            "low detail"
        )


# ============================================================
# SCENE DIRECTOR
# ============================================================

class AJVYRASceneDirector:

    def __init__(self):

        self.camera = (
            AJVYRACameraDirector()
        )

        self.lighting = (
            AJVYRALightingDirector()
        )

        self.prompt = (
            AJVYRAVisualPromptDirector()
        )

    def create_scene(
        self,
        anime_id: str,
        episode_id: str,
        scene_id: str,
        title: str,
        location_id: str,
        characters: Sequence[str],
        objective: str,
        conflict: str,
        emotion: str,
        time_of_day: str,
        environment: str,
        target_duration_seconds: float,
        actions: Sequence[str],
        dialogues: Sequence[
            DialogueLine
        ],
    ) -> SceneSpec:

        scene = SceneSpec(
            anime_id=anime_id,
            episode_id=episode_id,
            scene_id=scene_id,
            title=title,
            location_id=location_id,
            characters=list(characters),
            objective=objective,
            conflict=conflict,
            emotion=emotion,
            time_of_day=time_of_day,
            environment=environment,
            target_duration_seconds=max(
                1.0,
                target_duration_seconds,
            ),
        )

        self._build_shots(
            scene=scene,
            actions=list(actions),
            dialogues=list(dialogues),
        )

        return scene

    def _build_shots(
        self,
        scene: SceneSpec,
        actions: List[str],
        dialogues: List[DialogueLine],
    ) -> None:

        target = (
            scene.target_duration_seconds
        )

        action_count = max(
            1,
            len(actions)
        )

        estimated_shots = max(
            2,
            min(
                30,
                math.ceil(
                    target / 7.0
                )
            )
        )

        seed = stable_seed(
            scene.anime_id,
            scene.episode_id,
            scene.scene_id,
        )

        rng = random.Random(
            seed
        )

        for index in range(
            estimated_shots
        ):

            shot_number = index + 1

            action = (
                actions[
                    index % action_count
                ]
                if actions
                else scene.objective
            )

            emotional_intensity = (
                0.3
                + (
                    index
                    /
                    max(
                        1,
                        estimated_shots - 1
                    )
                )
                * 0.5
            )

            if scene.emotion.lower() in {
                "sad",
                "heartbreak",
                "despair",
                "grief",
            }:

                emotional_intensity += 0.15

            emotional_intensity = max(
                0.0,
                min(
                    1.0,
                    emotional_intensity
                )
            )

            subject = (
                scene.characters[
                    index
                    % len(scene.characters)
                ]
                if scene.characters
                else "scene subject"
            )

            camera = self.camera.create(
                shot_number=shot_number,
                emotional_intensity=(
                    emotional_intensity
                ),
                action=action,
                subject=subject,
            )

            lighting = self.lighting.create(
                emotion=scene.emotion,
                environment=scene.environment,
                time_of_day=scene.time_of_day,
            )

            duration = (
                5.0
                + rng.random() * 4.0
            )

            if dialogues:

                duration = max(
                    duration,
                    min(
                        12.0,
                        sum(
                            line.estimated_duration
                            for line in dialogues[
                                index
                                % len(dialogues):
                                index
                                % len(dialogues)
                                + 1
                            ]
                        )
                    )
                )

            shot_id = (
                f"{scene.scene_id}_"
                f"shot_{shot_number:03d}"
            )

            previous = (
                scene.shots[-1].shot_id
                if scene.shots
                else None
            )

            visual_prompt = (
                self.prompt.build(
                    scene=scene,
                    shot_number=shot_number,
                    action=action,
                    emotion=scene.emotion,
                    camera=camera,
                    lighting=lighting,
                )
            )

            continuity_seed = (
                stable_seed(
                    scene.anime_id,
                    scene.episode_id,
                    scene.scene_id,
                    shot_id,
                )
            )

            shot = ShotSpec(
                anime_id=scene.anime_id,
                episode_id=scene.episode_id,
                scene_id=scene.scene_id,
                shot_id=shot_id,
                shot_number=shot_number,
                duration_seconds=round(
                    duration,
                    2
                ),
                location_id=scene.location_id,
                characters=list(
                    scene.characters
                ),
                dialogue=[
                    line.normalized()
                    for line in dialogues
                ],
                action=action,
                emotion=scene.emotion,
                camera=camera,
                lighting=lighting,
                visual_prompt=visual_prompt,
                negative_prompt=(
                    self.prompt.negative_prompt()
                ),
                previous_shot_id=previous,
                next_shot_id=None,
                continuity_seed=(
                    continuity_seed
                ),
            )

            if previous:

                scene.shots[-1].next_shot_id = (
                    shot_id
                )

            scene.shots.append(
                shot
            )

        self._normalize_duration(
            scene
        )

    # --------------------------------------------------------
    # Duration correction
    # --------------------------------------------------------

    def _normalize_duration(
        self,
        scene: SceneSpec,
    ) -> None:

        if not scene.shots:
            return

        current = sum(
            shot.duration_seconds
            for shot in scene.shots
        )

        target = (
            scene.target_duration_seconds
        )

        if current <= 0:
            return

        multiplier = (
            target / current
        )

        for shot in scene.shots:

            shot.duration_seconds = round(
                max(
                    2.0,
                    min(
                        15.0,
                        shot.duration_seconds
                        * multiplier
                    )
                ),
                2
            )

    # --------------------------------------------------------
    # Character reference injection
    # --------------------------------------------------------

    def attach_character_references(
        self,
        scene: SceneSpec,
        references: Dict[str, List[str]],
    ) -> SceneSpec:

        for shot in scene.shots:

            combined = []

            for character_id in (
                shot.characters
            ):

                combined.extend(
                    references.get(
                        character_id,
                        []
                    )
                )

            shot.reference_images = list(
                dict.fromkeys(
                    combined
                )
            )

        return scene


# ============================================================
# EPISODE SHOT PLANNER
# ============================================================

class AJVYRAEpisodeShotPlanner:

    def __init__(
        self,
        output_root: str | Path = (
            "generated/anime_production"
        ),
    ):

        self.output_root = Path(
            output_root
        )

        self.scene_director = (
            AJVYRASceneDirector()
        )

    def create_episode_plan(
        self,
        anime_id: str,
        episode_id: str,
        scenes: Sequence[Dict[str, Any]],
    ) -> Dict[str, Any]:

        scene_objects = []

        for scene_data in scenes:

            dialogues = []

            for index, item in enumerate(
                scene_data.get(
                    "dialogues",
                    []
                )
            ):

                line = DialogueLine(
                    character_id=item[
                        "character_id"
                    ],
                    text=item["text"],
                    language=item.get(
                        "language",
                        "ja"
                    ),
                    emotion=item.get(
                        "emotion",
                        scene_data.get(
                            "emotion",
                            "neutral"
                        )
                    ),
                    line_id=item.get(
                        "line_id",
                        (
                            f"{scene_data['scene_id']}"
                            f"_line_{index + 1:03d}"
                        )
                    ),
                )

                line.estimated_duration = (
                    AJVYRADialogueTiming.estimate(
                        line.text,
                        line.language,
                    )
                )

                dialogues.append(
                    line
                )

            scene = (
                self.scene_director.create_scene(
                    anime_id=anime_id,
                    episode_id=episode_id,
                    scene_id=scene_data[
                        "scene_id"
                    ],
                    title=scene_data.get(
                        "title",
                        "Untitled Scene"
                    ),
                    location_id=scene_data.get(
                        "location_id",
                        "unknown_location"
                    ),
                    characters=scene_data.get(
                        "characters",
                        []
                    ),
                    objective=scene_data.get(
                        "objective",
                        ""
                    ),
                    conflict=scene_data.get(
                        "conflict",
                        ""
                    ),
                    emotion=scene_data.get(
                        "emotion",
                        "neutral"
                    ),
                    time_of_day=scene_data.get(
                        "time_of_day",
                        "day"
                    ),
                    environment=scene_data.get(
                        "environment",
                        ""
                    ),
                    target_duration_seconds=(
                        scene_data.get(
                            "target_duration_seconds",
                            60.0
                        )
                    ),
                    actions=scene_data.get(
                        "actions",
                        []
                    ),
                    dialogues=dialogues,
                )
            )

            scene_objects.append(
                scene
            )

        total_duration = sum(
            sum(
                shot.duration_seconds
                for shot in scene.shots
            )
            for scene in scene_objects
        )

        plan = {
            "engine": ENGINE_NAME,
            "version": ENGINE_VERSION,
            "created_at": utc_timestamp(),
            "anime_id": anime_id,
            "episode_id": episode_id,
            "scene_count": len(
                scene_objects
            ),
            "shot_count": sum(
                len(scene.shots)
                for scene in scene_objects
            ),
            "duration_seconds": round(
                total_duration,
                2
            ),
            "duration_minutes": round(
                total_duration / 60.0,
                2
            ),
            "scenes": [
                scene.normalized()
                for scene in scene_objects
            ],
        }

        self.save_plan(
            anime_id=anime_id,
            episode_id=episode_id,
            plan=plan,
        )

        return plan

    def save_plan(
        self,
        anime_id: str,
        episode_id: str,
        plan: Dict[str, Any],
    ) -> Path:

        directory = (
            self.output_root
            / safe_slug(anime_id)
            / "season_01"
            / safe_slug(episode_id)
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        path = (
            directory
            / "shot_plan.json"
        )

        write_json(
            path,
            plan
        )

        return path


# ============================================================
# CONTINUITY ENGINE
# ============================================================

class AJVYRAShotContinuityEngine:

    def validate(
        self,
        shots: Sequence[ShotSpec],
    ) -> Dict[str, Any]:

        errors = []
        warnings = []

        if not shots:

            errors.append(
                "No shots exist."
            )

        for index, shot in enumerate(
            shots
        ):

            expected_number = index + 1

            if shot.shot_number != (
                expected_number
            ):

                warnings.append(
                    f"{shot.shot_id}: "
                    "shot number sequence mismatch"
                )

            if index > 0:

                previous = shots[
                    index - 1
                ]

                if shot.previous_shot_id != (
                    previous.shot_id
                ):

                    errors.append(
                        f"{shot.shot_id}: "
                        "previous_shot_id mismatch"
                    )

                if previous.next_shot_id != (
                    shot.shot_id
                ):

                    errors.append(
                        f"{previous.shot_id}: "
                        "next_shot_id mismatch"
                    )

            if shot.duration_seconds < 1:

                errors.append(
                    f"{shot.shot_id}: "
                    "duration is too short"
                )

            if shot.duration_seconds > 20:

                warnings.append(
                    f"{shot.shot_id}: "
                    "duration is unusually long"
                )

            if not shot.visual_prompt:

                errors.append(
                    f"{shot.shot_id}: "
                    "missing visual prompt"
                )

        return {
            "passed": not errors,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
        }


# ============================================================
# PRODUCTION CONNECTOR
# ============================================================

class AJVYRAShotProductionConnector:
    """
    Converts ShotSpec objects into jobs understood by the
    future image/video providers.
    """

    def build_jobs(
        self,
        plan: Dict[str, Any],
    ) -> List[Dict[str, Any]]:

        jobs = []

        for scene in plan.get(
            "scenes",
            []
        ):

            for shot in scene.get(
                "shots",
                []
            ):

                jobs.append(
                    {
                        "job_type": "video_shot",
                        "anime_id": plan[
                            "anime_id"
                        ],
                        "episode_id": plan[
                            "episode_id"
                        ],
                        "scene_id": scene[
                            "scene_id"
                        ],
                        "shot_id": shot[
                            "shot_id"
                        ],
                        "duration_seconds": shot[
                            "duration_seconds"
                        ],
                        "prompt": shot[
                            "visual_prompt"
                        ],
                        "negative_prompt": shot[
                            "negative_prompt"
                        ],
                        "characters": shot[
                            "characters"
                        ],
                        "reference_images": shot[
                            "reference_images"
                        ],
                        "seed": shot[
                            "continuity_seed"
                        ],
                        "camera": shot[
                            "camera"
                        ],
                        "lighting": shot[
                            "lighting"
                        ],
                        "dialogue": shot[
                            "dialogue"
                        ],
                        "status": "queued",
                    }
                )

        return jobs


# ============================================================
# FULL DIRECTOR
# ============================================================

class AJVYRAAnimeSceneShotDirector:

    def __init__(
        self,
        output_root: str | Path = (
            "generated/anime_production"
        ),
    ):

        self.planner = (
            AJVYRAEpisodeShotPlanner(
                output_root
            )
        )

        self.continuity = (
            AJVYRAShotContinuityEngine()
        )

        self.connector = (
            AJVYRAShotProductionConnector()
        )

    def build_episode(
        self,
        anime_id: str,
        episode_id: str,
        scenes: Sequence[
            Dict[str, Any]
        ],
    ) -> Dict[str, Any]:

        plan = (
            self.planner.create_episode_plan(
                anime_id=anime_id,
                episode_id=episode_id,
                scenes=scenes,
            )
        )

        all_shots = []

        for scene in plan[
            "scenes"
        ]:

            for shot in scene[
                "shots"
            ]:

                all_shots.append(
                    ShotSpec(
                        anime_id=shot[
                            "anime_id"
                        ],
                        episode_id=shot[
                            "episode_id"
                        ],
                        scene_id=shot[
                            "scene_id"
                        ],
                        shot_id=shot[
                            "shot_id"
                        ],
                        shot_number=shot[
                            "shot_number"
                        ],
                        duration_seconds=shot[
                            "duration_seconds"
                        ],
                        location_id=shot[
                            "location_id"
                        ],
                        characters=shot[
                            "characters"
                        ],
                        dialogue=shot[
                            "dialogue"
                        ],
                        action=shot[
                            "action"
                        ],
                        emotion=shot[
                            "emotion"
                        ],
                        camera=CameraPlan(
                            **shot[
                                "camera"
                            ]
                        ),
                        lighting=LightingPlan(
                            **shot[
                                "lighting"
                            ]
                        ),
                        visual_prompt=shot[
                            "visual_prompt"
                        ],
                        negative_prompt=shot[
                            "negative_prompt"
                        ],
                        previous_shot_id=shot[
                            "previous_shot_id"
                        ],
                        next_shot_id=shot[
                            "next_shot_id"
                        ],
                        continuity_seed=shot[
                            "continuity_seed"
                        ],
                        reference_images=shot.get(
                            "reference_images",
                            []
                        ),
                        status=shot.get(
                            "status",
                            "planned"
                        ),
                        generated_media=shot.get(
                            "generated_media",
                            {}
                        ),
                    )
                )

        continuity_report = (
            self.continuity.validate(
                all_shots
            )
        )

        jobs = (
            self.connector.build_jobs(
                plan
            )
        )

        plan["continuity"] = (
            continuity_report
        )

        plan["generation_jobs"] = jobs

        plan["production_ready"] = (
            continuity_report["passed"]
            and len(jobs) > 0
        )

        self.planner.save_plan(
            anime_id=anime_id,
            episode_id=episode_id,
            plan=plan,
        )

        return plan


# ============================================================
# EXAMPLE
# ============================================================

def example_episode():

    director = (
        AJVYRAAnimeSceneShotDirector()
    )

    scenes = [

        {
            "scene_id": "scene_001",
            "title": "Rainy Encounter",

            "location_id": (
                "veylora_city_station"
            ),

            "characters": [
                "veylora_main_01",
                "character_002",
            ],

            "objective": (
                "The protagonist sees someone "
                "from his past."
            ),

            "conflict": (
                "He wants to approach but "
                "hesitates."
            ),

            "emotion": "heartbreak",

            "time_of_day": "evening",

            "environment": (
                "rainy urban train station, "
                "wet pavement, distant neon lights"
            ),

            "target_duration_seconds": 75,

            "actions": [
                "walking slowly through the station",
                "stopping after recognizing the person",
                "looking toward the platform",
                "hesitating before taking a step",
                "lowering his eyes as rain falls",
            ],

            "dialogues": [

                {
                    "character_id": (
                        "veylora_main_01"
                    ),
                    "text": (
                        "もう終わったんだ..."
                    ),
                    "language": "ja",
                    "emotion": "sad",
                },

                {
                    "character_id": (
                        "veylora_main_01"
                    ),
                    "text": (
                        "دیگه تموم شده..."
                    ),
                    "language": "fa",
                    "emotion": "heartbreak",
                },

            ],
        },

        {
            "scene_id": "scene_002",
            "title": "The Choice",

            "location_id": (
                "veylora_city_bridge"
            ),

            "characters": [
                "veylora_main_01",
            ],

            "objective": (
                "The protagonist decides "
                "whether to move forward."
            ),

            "conflict": (
                "His memories pull him backward."
            ),

            "emotion": "sad",

            "time_of_day": "night",

            "environment": (
                "large city bridge, "
                "cold wind, distant lights"
            ),

            "target_duration_seconds": 60,

            "actions": [
                "standing alone on the bridge",
                "looking at the city lights",
                "closing his eyes",
                "taking a deep breath",
                "walking forward",
            ],

            "dialogues": [],
        },

    ]

    return director.build_episode(
        anime_id="Veylora",
        episode_id="episode_01",
        scenes=scenes,
    )


if __name__ == "__main__":

    result = example_episode()

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )
