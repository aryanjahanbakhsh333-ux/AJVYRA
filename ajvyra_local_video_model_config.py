from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import os


@dataclass
class AJVYRALocalVideoModelConfig:
    """
    Configuration for AJVYRA's local video generation model.

    Default model:
        Wan2.1 T2V 1.3B

    The 1.3B model is intentionally the starting point.
    Larger Wan models can be selected later without changing
    the rest of the AJVYRA generation architecture.
    """

    model_id: str = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

    task: str = "text_to_video"

    device: str = "auto"
    dtype: str = "bfloat16"

    width: int = 832
    height: int = 480

    fps: int = 16
    num_frames: int = 81

    guidance_scale: float = 5.0
    flow_shift: float = 3.0

    enable_cpu_offload: bool = True
    enable_vae_tiling: bool = False

    cache_dir: str = "./models/wan"

    output_dir: str = "./generated_video"

    seed: int = 42

    def resolved_device(self) -> str:
        if self.device != "auto":
            return self.device

        try:
            import torch

            if torch.cuda.is_available():
                return "cuda"

            if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                return "mps"

        except Exception:
            pass

        return "cpu"

    def torch_dtype(self):
        import torch

        normalized = self.dtype.lower()

        if normalized == "float16":
            return torch.float16

        if normalized == "float32":
            return torch.float32

        if normalized == "bfloat16":
            if hasattr(torch, "bfloat16"):
                return torch.bfloat16

        return torch.float32

    def ensure_directories(self) -> None:
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        if self.task not in {
            "text_to_video",
            "image_to_video",
        }:
            raise ValueError(
                "task must be 'text_to_video' or 'image_to_video'"
            )

        if self.width <= 0 or self.height <= 0:
            raise ValueError("width and height must be positive")

        if self.fps <= 0:
            raise ValueError("fps must be positive")

        if self.num_frames < 5:
            raise ValueError("num_frames is too small")

        if self.guidance_scale <= 0:
            raise ValueError("guidance_scale must be positive")

        if self.flow_shift <= 0:
            raise ValueError("flow_shift must be positive")

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> Path:
        self.validate()

        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(
            json.dumps(self.to_dict(), indent=2),
            encoding="utf-8",
        )

        return target

    @classmethod
    def load(cls, path: str | Path) -> "AJVYRALocalVideoModelConfig":
        source = Path(path)

        data = json.loads(
            source.read_text(encoding="utf-8")
        )

        config = cls(**data)
        config.validate()

        return config

    @classmethod
    def from_environment(cls) -> "AJVYRALocalVideoModelConfig":
        config = cls(
            model_id=os.getenv(
                "AJVYRA_VIDEO_MODEL_ID",
                cls.model_id,
            ),
            task=os.getenv(
                "AJVYRA_VIDEO_TASK",
                cls.task,
            ),
            device=os.getenv(
                "AJVYRA_VIDEO_DEVICE",
                cls.device,
            ),
            dtype=os.getenv(
                "AJVYRA_VIDEO_DTYPE",
                cls.dtype,
            ),
            width=int(
                os.getenv(
                    "AJVYRA_VIDEO_WIDTH",
                    str(cls.width),
                )
            ),
            height=int(
                os.getenv(
                    "AJVYRA_VIDEO_HEIGHT",
                    str(cls.height),
                )
            ),
            fps=int(
                os.getenv(
                    "AJVYRA_VIDEO_FPS",
                    str(cls.fps),
                )
            ),
            num_frames=int(
                os.getenv(
                    "AJVYRA_VIDEO_FRAMES",
                    str(cls.num_frames),
                )
            ),
            guidance_scale=float(
                os.getenv(
                    "AJVYRA_VIDEO_GUIDANCE",
                    str(cls.guidance_scale),
                )
            ),
            flow_shift=float(
                os.getenv(
                    "AJVYRA_VIDEO_FLOW_SHIFT",
                    str(cls.flow_shift),
                )
            ),
            cache_dir=os.getenv(
                "AJVYRA_VIDEO_CACHE",
                cls.cache_dir,
            ),
            output_dir=os.getenv(
                "AJVYRA_VIDEO_OUTPUT",
                cls.output_dir,
            ),
        )

        config.validate()
        return config
