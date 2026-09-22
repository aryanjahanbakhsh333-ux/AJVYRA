from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ShotProduction:
    shot_id: str
    scene_id: str
    duration: int
    prompt: str
    negative_prompt: str
    characters: List[str]
    location: str
    emotion: str
    camera: str
    previous_shot: Optional[str] = None
    first_frame: Optional[str] = None
    last_frame: Optional[str] = None
    reference_images: List[str] = None

    def __post_init__(self):
        if self.reference_images is None:
            self.reference_images = []


class AJVYRAAnimeShotProductionEngine:
    """
    Builds cinematic shot specifications and delegates actual
    video generation to the existing real video provider engine.
    """

    def __init__(
        self,
        output_root: str = "generated/anime_production",
        video_engine=None,
    ):
        self.root = Path(output_root)
        self.video_engine = video_engine

    def build_shot_plan(
        self,
        anime_id: str,
        episode_id: str,
        story: Dict[str, Any],
        *,
        target_seconds: int = 1800,
    ) -> Dict[str, Any]:

        scenes = story.get("scenes") or []

        if not scenes:
            scenes = self._create_fallback_scenes(
                story,
                target_seconds,
            )

        shots: List[Dict[str, Any]] = []

        previous_id = None
        remaining = target_seconds
        counter = 1

        for scene_index, scene in enumerate(scenes, start=1):
            scene_id = scene.get(
                "scene_id",
                f"scene_{scene_index:03d}",
            )

            scene_duration = int(
                scene.get(
                    "duration",
                    min(60, max(20, remaining)),
                )
            )

            scene_duration = min(scene_duration, remaining)

            while scene_duration > 0:
                duration = min(8, scene_duration)

                shot_id = f"shot_{counter:04d}"

                production = ShotProduction(
                    shot_id=shot_id,
                    scene_id=scene_id,
                    duration=duration,
                    prompt=self._build_prompt(scene),
                    negative_prompt=self._negative_prompt(),
                    characters=self._characters(scene),
                    location=scene.get("location", "cinematic anime environment"),
                    emotion=scene.get("emotion", "neutral"),
                    camera=scene.get("camera", "cinematic medium shot"),
                    previous_shot=previous_id,
                )

                shots.append(asdict(production))

                previous_id = shot_id
                counter += 1
                scene_duration -= duration
                remaining -= duration

                if remaining <= 0:
                    break

            if remaining <= 0:
                break

        return {
            "anime_id": anime_id,
            "episode_id": episode_id,
            "target_duration_seconds": target_seconds,
            "shot_count": len(shots),
            "shots": shots,
        }

    def generate_shot(
        self,
        anime_id: str,
        episode_id: str,
        shot: Dict[str, Any],
    ) -> Path:

        if self.video_engine is None:
            raise RuntimeError(
                "No real video engine connected."
            )

        from ajvyra_anime_real_video_generation_engine import (
            VideoShotSpec,
        )

        spec = VideoShotSpec(
            anime_id=anime_id,
            episode_id=episode_id,
            scene_id=shot["scene_id"],
            shot_id=shot["shot_id"],
            duration=int(shot["duration"]),
            prompt=shot["prompt"],
            negative_prompt=shot["negative_prompt"],
            characters=shot.get("characters", []),
            reference_images=shot.get("reference_images", []),
            aspect_ratio="16:9",
            resolution="720p",
            language="en",
            first_frame=shot.get("first_frame"),
            last_frame=shot.get("last_frame"),
            previous_video=None,
            metadata=shot,
        )

        result = self.video_engine.generate_shot(spec)

        if not result.success:
            raise RuntimeError(
                result.error or "Video generation failed."
            )

        return Path(result.output_path)

    def _build_prompt(self, scene: Dict[str, Any]) -> str:
        characters = ", ".join(
            self._characters(scene)
        )

        return (
            "Original cinematic anime scene. "
            "Maintain strict character continuity. "
            f"Characters: {characters}. "
            f"Location: {scene.get('location', 'unknown')}. "
            f"Emotion: {scene.get('emotion', 'neutral')}. "
            f"Action: {scene.get('action', 'natural movement')}. "
            f"Camera: {scene.get('camera', 'cinematic shot')}. "
            f"Lighting: {scene.get('lighting', 'cinematic lighting')}. "
            f"Style: {scene.get('style', 'original modern anime')}. "
            "Natural motion, coherent anatomy, consistent clothing, "
            "consistent environment, cinematic composition."
        )

    @staticmethod
    def _characters(scene: Dict[str, Any]) -> List[str]:
        characters = scene.get("characters", [])

        if isinstance(characters, str):
            return [characters]

        return list(characters)

    @staticmethod
    def _negative_prompt() -> str:
        return (
            "low quality, broken anatomy, duplicate character, "
            "extra limbs, unstable face, changing clothes, "
            "random character identity, text, watermark, logo, "
            "flickering, distorted hands, malformed eyes"
        )

    @staticmethod
    def _create_fallback_scenes(
        story: Dict[str, Any],
        target_seconds: int,
    ) -> List[Dict[str, Any]]:

        title = story.get("title", "AJVYRA Original Anime")
        protagonist = story.get(
            "protagonist",
            "original protagonist",
        )

        scene_count = max(10, target_seconds // 60)

        return [
            {
                "scene_id": f"scene_{i:03d}",
                "duration": 60,
                "characters": [protagonist],
                "location": "original cinematic anime world",
                "emotion": "mysterious",
                "action": f"{protagonist} explores the world of {title}",
                "camera": "slow cinematic camera movement",
                "lighting": "dramatic atmospheric lighting",
                "style": "original anime cinematic",
            }
            for i in range(1, scene_count + 1)
        ]
