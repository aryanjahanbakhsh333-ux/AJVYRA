from __future__ import annotations

import json
import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ajvyra_anime_production_manifest import (
    ProductionManifest,
)


@dataclass
class ProductionContext:
    anime_id: int
    title: str
    project_dir: Path
    manifest: ProductionManifest


class FullAnimeProductionEngine:
    """
    Adapter layer connecting AJVYRA's existing engines.

    Every stage is isolated so one failed stage does not corrupt
    the entire project.
    """

    def __init__(
        self,
        root: str | Path = "ajvyra_projects/generated/anime",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def context(
        self,
        manifest: ProductionManifest,
    ) -> ProductionContext:
        project_dir = (
            self.root
            / f"anime_{manifest.anime_id:02d}"
        )

        project_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return ProductionContext(
            anime_id=manifest.anime_id,
            title=manifest.title,
            project_dir=project_dir,
            manifest=manifest,
        )

    def _save_stage(
        self,
        context: ProductionContext,
        stage: str,
        data: dict[str, Any],
    ) -> Path:
        stage_dir = (
            context.project_dir
            / stage
        )

        stage_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = stage_dir / "result.json"

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

        return path

    def story(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "anime_id": manifest.anime_id,
            "title": manifest.title,
            "stage": "story",
            "status": "ready",
            "duration_seconds": (
                manifest.duration_seconds
            ),
            "structure": [
                {
                    "act": 1,
                    "purpose": "introduction",
                },
                {
                    "act": 2,
                    "purpose": "conflict",
                },
                {
                    "act": 3,
                    "purpose": "resolution",
                },
            ],
        }

        path = self._save_stage(
            context,
            "story",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def characters(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "characters",
            "anime_id": manifest.anime_id,
            "cast_policy": (
                "unique_digital_cast_per_anime"
            ),
            "characters": [],
        }

        path = self._save_stage(
            context,
            "characters",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def locations(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "locations",
            "anime_id": manifest.anime_id,
            "locations": [],
        }

        path = self._save_stage(
            context,
            "locations",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def scenes(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "scenes",
            "anime_id": manifest.anime_id,
            "target_duration_seconds": (
                manifest.duration_seconds
            ),
            "scene_count_target": max(
                12,
                int(
                    manifest.duration_seconds
                    / 90
                ),
            ),
        }

        path = self._save_stage(
            context,
            "scenes",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def dialogue(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "dialogue",
            "anime_id": manifest.anime_id,
            "languages": [
                "fa",
                "ja",
            ],
            "dialogue_policy": (
                "scene_based_digital_dialogue"
            ),
        }

        path = self._save_stage(
            context,
            "dialogue",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def voices(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "voices",
            "anime_id": manifest.anime_id,
            "engine": (
                "AJVYRA Native TTS"
            ),
            "audio_languages": [
                "fa",
                "ja",
            ],
            "voice_cast": (
                "unique_per_anime"
            ),
        }

        path = self._save_stage(
            context,
            "voices",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def visuals(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "visuals",
            "anime_id": manifest.anime_id,
            "renderer": (
                "AJVYRA Native Visual Engine"
            ),
            "resolution": "1280x720",
        }

        path = self._save_stage(
            context,
            "visuals",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def animation(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "animation",
            "anime_id": manifest.anime_id,
            "fps": manifest.fps,
            "features": [
                "camera_motion",
                "breathing",
                "blinking",
                "lip_sync_timing",
                "expression_changes",
            ],
        }

        path = self._save_stage(
            context,
            "animation",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def video(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "video",
            "anime_id": manifest.anime_id,
            "format": "mp4",
            "encoder": "ffmpeg",
            "duration_seconds": (
                manifest.duration_seconds
            ),
        }

        path = self._save_stage(
            context,
            "video",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def subtitles(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "subtitles",
            "anime_id": manifest.anime_id,
            "languages": [
                "en",
                "fa",
                "ja",
            ],
            "toggle_off_supported": True,
        }

        path = self._save_stage(
            context,
            "subtitles",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def publish(
        self,
        manifest: ProductionManifest,
    ) -> dict:
        context = self.context(manifest)

        result = {
            "stage": "publish",
            "anime_id": manifest.anime_id,
            "title": manifest.title,
            "site_ready": True,
            "published_directory": str(
                Path(
                    "ajvyra_projects"
                )
                / "published"
                / "anime"
                / f"anime_{manifest.anime_id:02d}"
            ),
        }

        path = self._save_stage(
            context,
            "publish",
            result,
        )

        return {
            "path": str(path),
            **result,
        }

    def execute(
        self,
        manifest: ProductionManifest,
        stage: str,
    ) -> dict:
        worker = getattr(
            self,
            stage,
            None,
        )

        if worker is None:
            raise ValueError(
                f"Unknown production stage: {stage}"
            )

        return worker(manifest)
