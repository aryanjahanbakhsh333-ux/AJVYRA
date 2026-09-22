from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import hashlib
import json
import time

from ajvyra_local_video_model_config import (
    AJVYRALocalVideoModelConfig,
)
from ajvyra_local_video_model_loader import (
    AJVYRALocalVideoModelLoader,
)


@dataclass
class AJVYRALocalVideoGenerationRequest:
    prompt: str

    negative_prompt: str = (
        "low quality, blurry, distorted face, "
        "deformed body, extra fingers, extra limbs, "
        "duplicate person, bad anatomy, subtitles, "
        "watermark, text, logo, static image"
    )

    output_name: str = "ajvyra_video.mp4"

    width: Optional[int] = None
    height: Optional[int] = None
    num_frames: Optional[int] = None

    guidance_scale: Optional[float] = None
    seed: Optional[int] = None

    reference_image: Optional[str] = None

    def validate(self) -> None:
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")

        if self.width is not None and self.width <= 0:
            raise ValueError("width must be positive")

        if self.height is not None and self.height <= 0:
            raise ValueError("height must be positive")

        if self.num_frames is not None and self.num_frames < 5:
            raise ValueError("num_frames is too small")


@dataclass
class AJVYRALocalVideoGenerationResult:
    success: bool
    output_path: Optional[str]
    duration_seconds: float
    seed: int
    model_id: str
    task: str
    sha256: Optional[str]
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class AJVYRALocalVideoGenerationEngine:
    """
    Real local video generation engine.

    The engine delegates the actual generation to Wan2.1.
    """

    def __init__(
        self,
        config: AJVYRALocalVideoModelConfig | None = None,
        loader: AJVYRALocalVideoModelLoader | None = None,
    ):
        self.config = config or AJVYRALocalVideoModelConfig.from_environment()

        self.loader = loader or AJVYRALocalVideoModelLoader(
            self.config
        )

    def _resolve_seed(
        self,
        request: AJVYRALocalVideoGenerationRequest,
    ) -> int:
        if request.seed is not None:
            return request.seed

        return self.config.seed

    def _generator(
        self,
        seed: int,
    ):
        import torch

        device = self.config.resolved_device()

        if device == "cuda":
            return torch.Generator(device="cuda").manual_seed(seed)

        return torch.Generator().manual_seed(seed)

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            while True:
                chunk = handle.read(1024 * 1024)

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()

    def _output_path(
        self,
        request: AJVYRALocalVideoGenerationRequest,
    ) -> Path:
        filename = Path(request.output_name).name

        if not filename.lower().endswith(".mp4"):
            filename += ".mp4"

        output = Path(self.config.output_dir) / filename
        output.parent.mkdir(parents=True, exist_ok=True)

        return output

    def generate(
        self,
        request: AJVYRALocalVideoGenerationRequest,
    ) -> AJVYRALocalVideoGenerationResult:

        started = time.time()

        try:
            request.validate()

            self.config.ensure_directories()

            pipeline = self.loader.pipeline

            seed = self._resolve_seed(request)
            generator = self._generator(seed)

            width = request.width or self.config.width
            height = request.height or self.config.height
            num_frames = (
                request.num_frames
                or self.config.num_frames
            )

            guidance_scale = (
                request.guidance_scale
                or self.config.guidance_scale
            )

            if request.reference_image:
                result = self._generate_i2v(
                    pipeline=pipeline,
                    request=request,
                    generator=generator,
                    width=width,
                    height=height,
                    num_frames=num_frames,
                    guidance_scale=guidance_scale,
                )
            else:
                result = pipeline(
                    prompt=request.prompt,
                    negative_prompt=request.negative_prompt,
                    height=height,
                    width=width,
                    num_frames=num_frames,
                    guidance_scale=guidance_scale,
                    generator=generator,
                )

            frames = result.frames[0]

            output_path = self._output_path(request)

            from diffusers.utils import export_to_video

            export_to_video(
                frames,
                str(output_path),
                fps=self.config.fps,
            )

            if not output_path.exists():
                raise RuntimeError(
                    "Wan generation completed but no MP4 was created."
                )

            if output_path.stat().st_size <= 1024:
                raise RuntimeError(
                    "Generated MP4 is unexpectedly small."
                )

            elapsed = time.time() - started

            metadata_path = output_path.with_suffix(
                ".json"
            )

            metadata_path.write_text(
                json.dumps(
                    {
                        "success": True,
                        "output_path": str(output_path),
                        "model_id": self.config.model_id,
                        "task": self.config.task,
                        "seed": seed,
                        "fps": self.config.fps,
                        "frames": num_frames,
                        "width": width,
                        "height": height,
                        "generation_seconds": elapsed,
                        "sha256": self._sha256(output_path),
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            return AJVYRALocalVideoGenerationResult(
                success=True,
                output_path=str(output_path),
                duration_seconds=elapsed,
                seed=seed,
                model_id=self.config.model_id,
                task=self.config.task,
                sha256=self._sha256(output_path),
            )

        except Exception as exc:
            return AJVYRALocalVideoGenerationResult(
                success=False,
                output_path=None,
                duration_seconds=time.time() - started,
                seed=self._resolve_seed(request),
                model_id=self.config.model_id,
                task=self.config.task,
                sha256=None,
                error=f"{type(exc).__name__}: {exc}",
            )

    def _generate_i2v(
        self,
        pipeline,
        request: AJVYRALocalVideoGenerationRequest,
        generator,
        width: int,
        height: int,
        num_frames: int,
        guidance_scale: float,
    ):
        from diffusers.utils import load_image

        image_path = Path(request.reference_image)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Reference image not found: {image_path}"
            )

        image = load_image(str(image_path))

        return pipeline(
            image=image,
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            height=height,
            width=width,
            num_frames=num_frames,
            guidance_scale=guidance_scale,
            generator=generator,
        )
