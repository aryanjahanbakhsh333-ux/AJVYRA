from __future__ import annotations

import os
import secrets
import tempfile
from pathlib import Path
from typing import Optional

import torch

try:
    import spaces
except ImportError:
    class _SpacesFallback:
        @staticmethod
        def GPU(*args, **kwargs):
            def decorator(function):
                return function
            return decorator

    spaces = _SpacesFallback()

from diffusers import WanPipeline
from diffusers.utils import export_to_video

from ajvyra_ai_video_prompt_engine_v1 import prepare_anime_prompt


MODEL_ID = os.getenv(
    "AJVYRA_VIDEO_MODEL",
    "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
)

OUTPUT_DIR = Path(
    os.getenv(
        "AJVYRA_AI_VIDEO_OUTPUT",
        "ajvyra_ai_generated_videos",
    )
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


_PIPELINE: Optional[WanPipeline] = None


def _load_pipeline() -> WanPipeline:
    global _PIPELINE

    if _PIPELINE is not None:
        return _PIPELINE

    dtype = torch.bfloat16

    _PIPELINE = WanPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
    )

    # Wan supports CPU offloading for lower VRAM pressure.
    _PIPELINE.enable_model_cpu_offload()

    return _PIPELINE


def _safe_video_name() -> str:
    return f"ajvyra-ai-{secrets.token_hex(8)}.mp4"


@spaces.GPU(duration=180)
def generate_anime_video(
    prompt: str,
    num_frames: int = 49,
    fps: int = 16,
    inference_steps: int = 20,
    guidance_scale: float = 5.0,
    seed: Optional[int] = None,
) -> str:

    prepared = prepare_anime_prompt(prompt)

    if seed is None:
        seed = secrets.randbelow(2_147_483_647)

    num_frames = max(17, min(int(num_frames), 81))
    fps = max(8, min(int(fps), 24))
    inference_steps = max(8, min(int(inference_steps), 40))
    guidance_scale = max(1.0, min(float(guidance_scale), 10.0))

    pipeline = _load_pipeline()

    generator = torch.Generator(device="cuda").manual_seed(seed)

    result = pipeline(
        prompt=prepared["prompt"],
        negative_prompt=prepared["negative_prompt"],
        num_frames=num_frames,
        guidance_scale=guidance_scale,
        num_inference_steps=inference_steps,
        generator=generator,
    )

    frames = result.frames[0]

    output_path = OUTPUT_DIR / _safe_video_name()

    export_to_video(
        frames,
        str(output_path),
        fps=fps,
    )

    if not output_path.exists():
        raise RuntimeError("Video generation completed without an output file.")

    if output_path.stat().st_size < 1024:
        raise RuntimeError("Generated video file is unexpectedly small.")

    return str(output_path)
