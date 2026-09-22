from __future__ import annotations

import gc
import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import torch
from diffusers import WanPipeline
from diffusers.schedulers.scheduling_unipc_multistep import (
    UniPCMultistepScheduler,
)
from diffusers.utils import export_to_video


@dataclass
class WanGenerationRequest:
    prompt: str
    output_path: Path

    negative_prompt: str = (
        "low quality, blurry, static image, "
        "deformed anatomy, malformed hands, extra fingers, "
        "duplicate characters, inconsistent face, "
        "inconsistent clothing, bad proportions, "
        "watermark, logo, text, subtitles"
    )

    width: int = 832
    height: int = 480
    num_frames: int = 81
    fps: int = 16

    guidance_scale: float = 5.0
    flow_shift: float = 3.0

    seed: Optional[int] = None


@dataclass
class WanGenerationResult:
    success: bool
    output_path: Optional[str]
    sha256: Optional[str]
    elapsed_seconds: float
    error: Optional[str]


class AJVYRAWanAutoEngine:
    """
    Real local Wan2.1 T2V engine.

    The engine:
        1. loads Wan2.1
        2. receives a cinematic prompt
        3. generates real frames
        4. exports a real MP4
        5. validates the resulting file
        6. writes metadata
    """

    def __init__(
        self,
        model_id: str = (
            "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"
        ),
        device: str = "auto",
        cpu_offload: bool = True,
        dtype: str = "bfloat16",
    ) -> None:

        self.model_id = model_id
        self.device = self._resolve_device(device)
        self.cpu_offload = cpu_offload
        self.dtype = self._resolve_dtype(dtype)

        self.pipeline: Optional[WanPipeline] = None

    # ---------------------------------------------------------
    # Device
    # ---------------------------------------------------------

    def _resolve_device(
        self,
        device: str,
    ) -> str:

        if device != "auto":
            return device

        if torch.cuda.is_available():
            return "cuda"

        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return "mps"

        return "cpu"

    def _resolve_dtype(
        self,
        dtype: str,
    ) -> torch.dtype:

        if dtype == "float16":
            return torch.float16

        if dtype == "float32":
            return torch.float32

        if dtype == "bfloat16":

            if self.device == "cuda":
                return torch.bfloat16

            return torch.float32

        return torch.bfloat16

    # ---------------------------------------------------------
    # Load
    # ---------------------------------------------------------

    def load(self) -> None:

        if self.pipeline is not None:
            return

        if self.device == "cpu":
            raise RuntimeError(
                "Wan2.1 local video generation requires "
                "a suitable accelerator for practical production. "
                "CPU-only generation is not enabled."
            )

        print(
            f"[WAN] Loading model: {self.model_id}"
        )

        print(
            f"[WAN] Device: {self.device}"
        )

        self.pipeline = WanPipeline.from_pretrained(
            self.model_id,
            torch_dtype=self.dtype,
        )

        self.pipeline.scheduler = (
            UniPCMultistepScheduler.from_config(
                self.pipeline.scheduler.config,
                flow_shift=3.0,
            )
        )

        if self.cpu_offload:

            self.pipeline.enable_model_cpu_offload()

        else:

            self.pipeline.to(
                self.device
            )

        print(
            "[WAN] Model loaded."
        )

    # ---------------------------------------------------------
    # Generate
    # ---------------------------------------------------------

    def generate(
        self,
        request: WanGenerationRequest,
    ) -> WanGenerationResult:

        started = time.time()

        try:

            self._validate(request)

            self.load()

            request.output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            generator = None

            if request.seed is not None:

                generator = torch.Generator(
                    device=self.device
                ).manual_seed(
                    request.seed
                )

            print(
                f"[WAN] Generating:"
                f" {request.output_path.name}"
            )

            with torch.inference_mode():

                output = self.pipeline(
                    prompt=request.prompt,
                    negative_prompt=(
                        request.negative_prompt
                    ),
                    height=request.height,
                    width=request.width,
                    num_frames=request.num_frames,
                    guidance_scale=(
                        request.guidance_scale
                    ),
                    generator=generator,
                )

            frames = output.frames[0]

            export_to_video(
                frames,
                str(request.output_path),
                fps=request.fps,
            )

            if not request.output_path.exists():

                raise RuntimeError(
                    "Wan finished without creating "
                    "the requested MP4."
                )

            if request.output_path.stat().st_size <= 1024:

                raise RuntimeError(
                    "Generated MP4 is invalid or empty."
                )

            checksum = self._sha256(
                request.output_path
            )

            elapsed = (
                time.time() - started
            )

            metadata_path = (
                request.output_path.with_suffix(
                    ".json"
                )
            )

            metadata_path.write_text(
                json.dumps(
                    {
                        "model": self.model_id,
                        "device": self.device,
                        "prompt": request.prompt,
                        "negative_prompt": (
                            request.negative_prompt
                        ),
                        "width": request.width,
                        "height": request.height,
                        "num_frames": request.num_frames,
                        "fps": request.fps,
                        "seed": request.seed,
                        "sha256": checksum,
                        "elapsed_seconds": elapsed,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            self._release_memory()

            return WanGenerationResult(
                success=True,
                output_path=str(
                    request.output_path
                ),
                sha256=checksum,
                elapsed_seconds=elapsed,
                error=None,
            )

        except Exception as exc:

            self._release_memory()

            return WanGenerationResult(
                success=False,
                output_path=None,
                sha256=None,
                elapsed_seconds=(
                    time.time() - started
                ),
                error=(
                    f"{type(exc).__name__}: {exc}"
                ),
            )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @staticmethod
    def _validate(
        request: WanGenerationRequest,
    ) -> None:

        if not request.prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        if request.width <= 0:
            raise ValueError(
                "Width must be positive."
            )

        if request.height <= 0:
            raise ValueError(
                "Height must be positive."
            )

        if request.num_frames <= 1:
            raise ValueError(
                "num_frames must be greater than 1."
            )

        if (
            request.num_frames - 1
        ) % 4 != 0:

            raise ValueError(
                "Wan requires "
                "(num_frames - 1) % 4 == 0."
            )

        if request.fps <= 0:
            raise ValueError(
                "FPS must be positive."
            )

    # ---------------------------------------------------------
    # Memory
    # ---------------------------------------------------------

    @staticmethod
    def _release_memory() -> None:

        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    # ---------------------------------------------------------
    # Hash
    # ---------------------------------------------------------

    @staticmethod
    def _sha256(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as handle:

            while True:

                chunk = handle.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                digest.update(chunk)

        return digest.hexdigest()
