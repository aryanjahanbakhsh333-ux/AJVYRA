from __future__ import annotations

from pathlib import Path
from typing import Any

from ajvyra_local_video_model_config import (
    AJVYRALocalVideoModelConfig,
)


class AJVYRALocalVideoModelLoader:
    """
    Lazy loader for Wan2.1 Diffusers pipelines.

    No model is loaded during module import.
    """

    def __init__(
        self,
        config: AJVYRALocalVideoModelConfig | None = None,
    ):
        self.config = config or AJVYRALocalVideoModelConfig.from_environment()
        self.config.validate()
        self.config.ensure_directories()

        self._pipeline: Any | None = None
        self._loaded_task: str | None = None

    @property
    def pipeline(self):
        if self._pipeline is None:
            self.load()

        return self._pipeline

    def _require_dependencies(self):
        try:
            import torch
            import diffusers
        except ImportError as exc:
            raise RuntimeError(
                "AJVYRA local video model requires "
                "torch and diffusers. "
                "Install them before loading Wan2.1."
            ) from exc

        return torch, diffusers

    def _select_device(self) -> str:
        device = self.config.resolved_device()

        if device == "cuda":
            import torch

            if not torch.cuda.is_available():
                raise RuntimeError(
                    "CUDA was requested but no CUDA GPU is available."
                )

        return device

    def _load_text_to_video(self):
        torch, diffusers = self._require_dependencies()

        from diffusers import WanPipeline
        from diffusers.schedulers.scheduling_unipc_multistep import (
            UniPCMultistepScheduler,
        )

        model_id = self.config.model_id

        pipeline = WanPipeline.from_pretrained(
            model_id,
            torch_dtype=self.config.torch_dtype(),
            cache_dir=self.config.cache_dir,
        )

        pipeline.scheduler = (
            UniPCMultistepScheduler.from_config(
                pipeline.scheduler.config,
                flow_shift=self.config.flow_shift,
            )
        )

        device = self._select_device()

        if (
            self.config.enable_cpu_offload
            and device == "cuda"
        ):
            pipeline.enable_model_cpu_offload()
        else:
            pipeline.to(device)

        if self.config.enable_vae_tiling:
            if hasattr(pipeline.vae, "enable_tiling"):
                pipeline.vae.enable_tiling()

        return pipeline

    def _load_image_to_video(self):
        torch, diffusers = self._require_dependencies()

        from diffusers import (
            AutoencoderKLWan,
            WanImageToVideoPipeline,
        )
        from transformers import CLIPVisionModel

        model_id = self.config.model_id

        image_encoder = CLIPVisionModel.from_pretrained(
            model_id,
            subfolder="image_encoder",
            torch_dtype=torch.float32,
            cache_dir=self.config.cache_dir,
        )

        vae = AutoencoderKLWan.from_pretrained(
            model_id,
            subfolder="vae",
            torch_dtype=torch.float32,
            cache_dir=self.config.cache_dir,
        )

        pipeline = WanImageToVideoPipeline.from_pretrained(
            model_id,
            image_encoder=image_encoder,
            vae=vae,
            torch_dtype=self.config.torch_dtype(),
            cache_dir=self.config.cache_dir,
        )

        device = self._select_device()

        if (
            self.config.enable_cpu_offload
            and device == "cuda"
        ):
            pipeline.enable_model_cpu_offload()
        else:
            pipeline.to(device)

        return pipeline

    def load(self):
        if self._pipeline is not None:
            return self._pipeline

        task = self.config.task

        if task == "text_to_video":
            self._pipeline = self._load_text_to_video()

        elif task == "image_to_video":
            self._pipeline = self._load_image_to_video()

        else:
            raise ValueError(
                f"Unsupported video task: {task}"
            )

        self._loaded_task = task

        return self._pipeline

    def unload(self) -> None:
        self._pipeline = None
        self._loaded_task = None

        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except Exception:
            pass

    def model_info(self) -> dict:
        return {
            "model_id": self.config.model_id,
            "task": self.config.task,
            "device": self.config.resolved_device(),
            "dtype": self.config.dtype,
            "loaded": self._pipeline is not None,
            "cache_dir": str(
                Path(self.config.cache_dir).resolve()
            ),
        }
