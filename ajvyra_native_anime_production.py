from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ajvyra_native_animation_engine import (
    AnimationKeyframe,
    NativeAnimationEngine,
)
from ajvyra_native_scene_renderer import (
    NativeSceneRenderer,
    SceneCharacter,
    SceneSpec,
)
from ajvyra_native_visual_engine import (
    NativeVisualEngine,
)


@dataclass
class AnimeProductionRequest:
    anime_id: int
    title: str
    scene_type: str = "night"
    duration_seconds: float = 30.0
    fps: int = 24


class NativeAnimeProduction:
    """
    Final native production controller.

    Pipeline:

    AI/content data
        ↓
    Scene
        ↓
    Visual frames
        ↓
    Animation timing
        ↓
    FFmpeg
        ↓
    MP4
        ↓
    Published anime folder
        ↓
    Website manifest
    """

    def __init__(
        self,
        root: str | Path = "ajvyra_projects",
    ):
        self.root = Path(root)

        self.generated = (
            self.root / "generated" / "anime"
        )

        self.published = (
            self.root / "published" / "anime"
        )

        self.generated.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.published.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.scene_renderer = NativeSceneRenderer()
        self.animation_engine = NativeAnimationEngine()

    def _ffmpeg_path(self) -> Optional[str]:
        return shutil.which("ffmpeg")

    def _create_scene(
        self,
        request: AnimeProductionRequest,
    ) -> Path:
        project_dir = (
            self.generated
            / f"anime_{request.anime_id:02d}"
        )

        scene_dir = project_dir / "scene_001"

        scene_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        scene = SceneSpec(
            anime_id=request.anime_id,
            scene_id="scene_001",
            location="Original Location",
            atmosphere=request.scene_type,
            duration_seconds=request.duration_seconds,
            characters=[
                SceneCharacter(
                    character_id=f"anime_{request.anime_id:02d}_character_001",
                    name=f"Original Character {request.anime_id:02d}",
                    x=0.50,
                    y=0.91,
                    scale=1.30,
                    hair="black",
                    skin="pale",
                    outfit="dark",
                    expression="neutral",
                )
            ],
        )

        return self.scene_renderer.render_scene(
            scene,
            scene_dir,
        )

    def _create_animation_manifest(
        self,
        request: AnimeProductionRequest,
        scene_dir: Path,
    ) -> Path:
        animation_dir = (
            self.generated
            / f"anime_{request.anime_id:02d}"
            / "animation"
        )

        animation_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        total_frames = int(
            request.duration_seconds * request.fps
        )

        animation = self.animation_engine.build_animation(
            animation_id=(
                f"anime_{request.anime_id:02d}_scene_001"
            ),
            duration_seconds=request.duration_seconds,
            keyframes=[
                AnimationKeyframe(
                    frame=0,
                    x=0.50,
                    y=0.91,
                    scale=1.30,
                    expression="neutral",
                ),
                AnimationKeyframe(
                    frame=max(1, total_frames - 1),
                    x=0.53,
                    y=0.91,
                    scale=1.34,
                    expression="sad",
                ),
            ],
            speech_duration=request.duration_seconds,
        )

        return animation

    def _compose_video(
        self,
        request: AnimeProductionRequest,
        scene_dir: Path,
        audio: str | Path | None = None,
    ) -> Path:
        ffmpeg = self._ffmpeg_path()

        if not ffmpeg:
            raise RuntimeError(
                "FFmpeg was not found. Install FFmpeg and make sure "
                "the ffmpeg command is available in PATH."
            )

        output_dir = (
            self.generated
            / f"anime_{request.anime_id:02d}"
            / "video"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output = output_dir / "main.mp4"

        pattern = str(
            scene_dir / "frame_%06d.png"
        )

        command = [
            ffmpeg,
            "-y",
            "-framerate",
            str(request.fps),
            "-i",
            pattern,
        ]

        if audio:
            command.extend(
                [
                    "-i",
                    str(audio),
                    "-map",
                    "0:v:0",
                    "-map",
                    "1:a:0",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "aac",
                    "-shortest",
                    str(output),
                ]
            )
        else:
            command.extend(
                [
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-an",
                    str(output),
                ]
            )

        subprocess.run(
            command,
            check=True,
        )

        return output

    def _publish(
        self,
        request: AnimeProductionRequest,
        video_path: Path,
        scene_dir: Path,
    ) -> Path:
        publish_dir = (
            self.published
            / f"anime_{request.anime_id:02d}"
        )

        publish_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        video_dir = publish_dir / "video"
        video_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        final_video = video_dir / "main.mp4"

        shutil.copy2(
            video_path,
            final_video,
        )

        poster = (
            scene_dir
            / "frame_000001.png"
        )

        if poster.exists():
            shutil.copy2(
                poster,
                publish_dir / "poster.png",
            )

        manifest = {
            "anime_id": request.anime_id,
            "title": request.title,
            "duration_seconds": request.duration_seconds,
            "fps": request.fps,
            "video": "video/main.mp4",
            "poster": "poster.png",
            "status": "published",
            "generated_by": "AJVYRA Native Anime Production",
        }

        manifest_path = (
            publish_dir / "anime.json"
        )

        with manifest_path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                manifest,
                f,
                ensure_ascii=False,
                indent=2,
            )

        self._update_site_manifest(
            manifest
        )

        return publish_dir

    def _update_site_manifest(
        self,
        anime_manifest: dict,
    ):
        site_dir = self.root / "site"
        site_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest_path = (
            site_dir / "anime_manifest.json"
        )

        if manifest_path.exists():
            try:
                with manifest_path.open(
                    "r",
                    encoding="utf-8",
                ) as f:
                    catalog = json.load(f)
            except Exception:
                catalog = []
        else:
            catalog = []

        catalog = [
            item
            for item in catalog
            if item.get("anime_id")
            != anime_manifest["anime_id"]
        ]

        catalog.append(anime_manifest)

        catalog.sort(
            key=lambda item: item["anime_id"]
        )

        with manifest_path.open(
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                catalog,
                f,
                ensure_ascii=False,
                indent=2,
            )

    def create(
        self,
        request: AnimeProductionRequest,
        audio: str | Path | None = None,
    ) -> dict:
        """
        Creates a complete small production test.

        For a full 30-minute anime, pass duration_seconds=1800.
        """

        scene_dir = self._create_scene(request)

        animation = self._create_animation_manifest(
            request,
            scene_dir,
        )

        video = self._compose_video(
            request,
            scene_dir,
            audio=audio,
        )

        published = self._publish(
            request,
            video,
            scene_dir,
        )

        return {
            "anime_id": request.anime_id,
            "title": request.title,
            "scene": str(scene_dir),
            "animation": str(animation),
            "video": str(video),
            "published": str(published),
            "site_manifest": str(
                self.root
                / "site"
                / "anime_manifest.json"
            ),
            "status": "published",
        }


if __name__ == "__main__":
    production = NativeAnimeProduction()

    result = production.create(
        AnimeProductionRequest(
            anime_id=1,
            title="Veylora",
            scene_type="rain",
            duration_seconds=10,
            fps=24,
        )
    )

    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    ))
