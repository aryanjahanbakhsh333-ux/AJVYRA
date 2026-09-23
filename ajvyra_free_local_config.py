from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    root: Path
    output: Path
    comfy_url: str
    workflow_file: Path

    width: int
    height: int
    fps: int
    clip_seconds: int

    minimum_video_size: int
    max_retries: int

    @classmethod
    def load(cls) -> "Config":
        root = Path(
            os.getenv("AJVYRA_ROOT", ".")
        ).resolve()

        output = root / "ajvyra_free_output"

        workflow_file = root / os.getenv(
            "AJVYRA_WAN_WORKFLOW",
            "wan_workflow.json"
        )

        return cls(
            root=root,
            output=output,
            comfy_url=os.getenv(
                "AJVYRA_COMFY_URL",
                "http://127.0.0.1:8188"
            ).rstrip("/"),

            workflow_file=workflow_file,

            width=int(
                os.getenv("AJVYRA_WIDTH", "832")
            ),

            height=int(
                os.getenv("AJVYRA_HEIGHT", "480")
            ),

            fps=int(
                os.getenv("AJVYRA_FPS", "16")
            ),

            clip_seconds=int(
                os.getenv("AJVYRA_CLIP_SECONDS", "5")
            ),

            minimum_video_size=int(
                os.getenv(
                    "AJVYRA_MIN_VIDEO_SIZE",
                    "50000"
                )
            ),

            max_retries=int(
                os.getenv(
                    "AJVYRA_MAX_RETRIES",
                    "3"
                )
            ),
        )

    def prepare(self):
        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

        (
            self.output / "anime"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        (
            self.output / "games"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

        (
            self.output / "manifests"
        ).mkdir(
            parents=True,
            exist_ok=True
        )

    def validate(self):
        if not self.workflow_file.exists():
            raise FileNotFoundError(
                "Wan ComfyUI workflow was not found: "
                f"{self.workflow_file}"
            )

        if self.clip_seconds <= 0:
            raise ValueError(
                "clip_seconds must be greater than zero"
            )

        if self.fps <= 0:
            raise ValueError(
                "fps must be greater than zero"
            )
