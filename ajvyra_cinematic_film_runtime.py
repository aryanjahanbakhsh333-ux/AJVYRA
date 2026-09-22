from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Any


@dataclass
class CinematicSceneRequest:
    scene_id: str
    order: int
    prompt: str
    duration_target: float
    character_ids: list[str]
    first_frame: Optional[Any] = None
    last_frame: Optional[Any] = None


@dataclass
class CinematicSceneResult:
    scene_id: str
    status: str
    output_path: Optional[str]
    error: Optional[str] = None


class AJVYRACinematicFilmRuntime:

    def __init__(
        self,
        film_id: str,
        workspace: str | Path,
        veo_runner: Any,
        reference_continuity: Any,
    ) -> None:

        self.film_id = film_id
        self.workspace = Path(workspace)
        self.workspace.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.veo = veo_runner
        self.references = reference_continuity

        self.results: list[
            CinematicSceneResult
        ] = []

    def generate_scene(
        self,
        scene: CinematicSceneRequest,
    ) -> CinematicSceneResult:

        scene_dir = (
            self.workspace
            / "films"
            / self.film_id
            / "scenes"
        )

        scene_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            scene_dir
            / f"{scene.order:05d}_{scene.scene_id}.mp4"
        )

        prompt_parts = []

        for character_id in scene.character_ids:
            reference = self.references.get(
                character_id
            )

            if reference:
                prompt_parts.append(
                    self.references.build_prompt(
                        character_id,
                        scene.prompt,
                    )
                )

        if not prompt_parts:
            prompt_parts.append(scene.prompt)

        final_prompt = "\n".join(prompt_parts)

        from ajvyra_cinematic_veo_real_runner import (
            VeoGenerationRequest,
        )

        request = VeoGenerationRequest(
            prompt=final_prompt,
            output_path=str(output_path),
            first_frame=scene.first_frame,
            last_frame=scene.last_frame,
        )

        result = self.veo.generate(request)

        scene_result = CinematicSceneResult(
            scene_id=scene.scene_id,
            status=result.status,
            output_path=result.output_path,
            error=result.error,
        )

        self.results.append(scene_result)
        self._save_scene_result(scene_result)

        return scene_result

    def generate_film(
        self,
        scenes: list[CinematicSceneRequest],
    ) -> list[CinematicSceneResult]:

        ordered = sorted(
            scenes,
            key=lambda item: item.order,
        )

        results = []

        for scene in ordered:
            result = self.generate_scene(scene)
            results.append(result)

            if result.status != "COMPLETED":
                break

        return results

    def successful_outputs(self) -> list[str]:
        return [
            result.output_path
            for result in self.results
            if result.status == "COMPLETED"
            and result.output_path
        ]

    def _save_scene_result(
        self,
        result: CinematicSceneResult,
    ) -> None:

        report_dir = (
            self.workspace
            / "films"
            / self.film_id
            / "scene_reports"
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            report_dir
            / f"{result.scene_id}.json"
        )

        path.write_text(
            json.dumps(
                asdict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
