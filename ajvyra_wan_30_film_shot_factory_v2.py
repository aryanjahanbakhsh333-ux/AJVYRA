from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ajvyra_wan_real_factory_bridge_v2 import (
    AJVYRAWanRealFactoryBridgeV2,
    WanGenerationJob,
)


@dataclass
class FilmShot:
    film_id: str
    film_title: str
    shot_id: str
    prompt: str
    seed: int


class AJVYRA30FilmShotFactoryV2:

    def __init__(
        self,
        bridge: AJVYRAWanRealFactoryBridgeV2,
        output_root: str = "ajvyra_production",
    ):
        self.bridge = bridge
        self.output_root = Path(output_root)

    def normalize_prompt(self, prompt: str) -> str:
        prompt = " ".join(str(prompt).split())

        if not prompt:
            raise ValueError("Empty Wan prompt.")

        return prompt

    def make_shot(
        self,
        film_id: str,
        film_title: str,
        shot_id: str,
        prompt: str,
        seed: int,
    ) -> FilmShot:

        return FilmShot(
            film_id=film_id,
            film_title=film_title,
            shot_id=shot_id,
            prompt=self.normalize_prompt(prompt),
            seed=int(seed),
        )

    def output_path(self, shot: FilmShot) -> Path:
        return (
            self.output_root
            / shot.film_id
            / "shots"
            / f"{shot.shot_id}.mp4"
        )

    def generate_shot(self, shot: FilmShot) -> Path:

        output = self.output_path(shot)

        job = WanGenerationJob(
            film_id=shot.film_id,
            film_title=shot.film_title,
            shot_id=shot.shot_id,
            prompt=shot.prompt,
            output_path=str(output),
            ckpt_dir=str(self.bridge.checkpoint_dir),
            seed=shot.seed,
        )

        self.bridge.save_job_manifest(job)

        return self.bridge.run(job)

    def generate_film(
        self,
        film_id: str,
        film_title: str,
        shots: list[dict[str, Any]],
    ) -> list[Path]:

        generated: list[Path] = []

        for index, shot in enumerate(shots, start=1):

            shot_id = str(
                shot.get("shot_id")
                or f"shot_{index:04d}"
            )

            prompt = shot.get("prompt")

            if not prompt:
                raise ValueError(
                    f"Missing prompt for {film_id}/{shot_id}"
                )

            seed = int(
                shot.get("seed", index)
            )

            normalized = self.make_shot(
                film_id=film_id,
                film_title=film_title,
                shot_id=shot_id,
                prompt=prompt,
                seed=seed,
            )

            generated.append(
                self.generate_shot(normalized)
            )

        return generated
