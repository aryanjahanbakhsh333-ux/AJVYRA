from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from ajvyra_native_visual_engine import (
    NativeVisualEngine,
    VisualCharacter,
)


@dataclass
class SceneCharacter:
    character_id: str
    name: str
    x: float
    y: float
    scale: float = 1.0
    hair: str = "dark"
    skin: str = "light"
    outfit: str = "dark"
    expression: str = "neutral"


@dataclass
class SceneSpec:
    anime_id: int
    scene_id: str
    location: str
    atmosphere: str
    duration_seconds: float
    characters: List[SceneCharacter] = field(default_factory=list)
    seed: int = 42


class NativeSceneRenderer:
    """
    Converts an anime scene description into a deterministic
    frame sequence.
    """

    ATMOSPHERE_MAP = {
        "dark": "night",
        "sad": "rain",
        "lonely": "night",
        "romantic": "sunset",
        "mysterious": "night",
        "fantasy": "fantasy",
        "sci-fi": "space",
        "forest": "forest",
        "city": "city",
        "rain": "rain",
        "day": "default",
    }

    def __init__(
        self,
        root: str | Path = "ajvyra_projects/scenes",
        width: int = 1280,
        height: int = 720,
        fps: int = 24,
    ):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

        self.engine = NativeVisualEngine()

        self.width = width
        self.height = height
        self.fps = fps

    def _scene_type(self, atmosphere: str) -> str:
        key = atmosphere.lower().strip()

        for name, scene_type in self.ATMOSPHERE_MAP.items():
            if name in key:
                return scene_type

        return "default"

    def _camera_offset(self, frame: int, total_frames: int):
        if total_frames <= 1:
            return 0.0

        progress = frame / (total_frames - 1)

        # slow cinematic pan
        return math.sin(progress * math.pi) * 0.035

    def render_scene(
        self,
        scene: SceneSpec,
        output_dir: str | Path | None = None,
    ) -> Path:
        if output_dir is None:
            output_dir = (
                self.root
                / f"anime_{scene.anime_id:02d}"
                / scene.scene_id
            )

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        total_frames = max(
            1,
            int(scene.duration_seconds * self.fps),
        )

        scene_type = self._scene_type(scene.atmosphere)

        for frame_number in range(total_frames):
            offset = self._camera_offset(
                frame_number,
                total_frames,
            )

            visual_characters = []

            for character in scene.characters:
                visual_characters.append(
                    VisualCharacter(
                        name=character.name,
                        x=max(
                            0.05,
                            min(0.95, character.x + offset),
                        ),
                        y=character.y,
                        scale=character.scale,
                        hair=character.hair,
                        skin=character.skin,
                        outfit=character.outfit,
                        expression=character.expression,
                    )
                )

            image = self.engine.render_frame(
                scene_type=scene_type,
                characters=visual_characters,
                frame=frame_number,
            )

            frame_path = output_dir / (
                f"frame_{frame_number + 1:06d}.png"
            )

            image.save(frame_path)

        manifest = {
            "anime_id": scene.anime_id,
            "scene_id": scene.scene_id,
            "location": scene.location,
            "atmosphere": scene.atmosphere,
            "duration_seconds": scene.duration_seconds,
            "fps": self.fps,
            "frame_count": total_frames,
            "frame_pattern": "frame_%06d.png",
        }

        manifest_path = output_dir / "scene.json"

        with manifest_path.open("w", encoding="utf-8") as f:
            json.dump(
                manifest,
                f,
                ensure_ascii=False,
                indent=2,
            )

        return output_dir


if __name__ == "__main__":
    renderer = NativeSceneRenderer()

    renderer.render_scene(
        SceneSpec(
            anime_id=1,
            scene_id="scene_001",
            location="Rainy City Street",
            atmosphere="rain",
            duration_seconds=5,
            characters=[
                SceneCharacter(
                    character_id="vey_001",
                    name="Veyrion",
                    x=0.50,
                    y=0.91,
                    scale=1.35,
                    hair="black",
                    skin="pale",
                    outfit="dark",
                    expression="sad",
                )
            ],
        )
    )

    print("Scene frame sequence created.")
