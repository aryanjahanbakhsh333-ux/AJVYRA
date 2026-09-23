from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import torch

from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.schedulers.scheduling_unipc_multistep import (
    UniPCMultistepScheduler,
)
from diffusers.utils import export_to_video

from ajvyra_anime_real_production_engine import (
    AJVYRAAnimeRealProductionEngine,
    MediaAsset,
    ProductionConfig,
    ProviderError,
    stable_id,
)


class AJVYRAWanRealVideoProvider:
    """
    Real Wan2.1 T2V provider.

    This class implements the VideoProvider contract expected by
    AJVYRAAnimeRealProductionEngine.

    It does NOT create placeholder videos.
    If CUDA/Wan is unavailable, it fails instead of pretending
    that a real video was generated.
    """

    name = "wan2.1-t2v-1.3b-real"

    MODEL_ID = os.getenv(
        "AJVYRA_WAN_MODEL",
        "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
    )

    def __init__(
        self,
        flow_shift: float = 5.0,
        guidance_scale: float = 5.0,
    ):
        if not torch.cuda.is_available():
            raise ProviderError(
                "Wan real generation requires a CUDA GPU. "
                "No CUDA device is available."
            )

        self.flow_shift = float(
            os.getenv(
                "AJVYRA_WAN_FLOW_SHIFT",
                str(flow_shift),
            )
        )

        self.guidance_scale = float(
            os.getenv(
                "AJVYRA_WAN_GUIDANCE_SCALE",
                str(guidance_scale),
            )
        )

        self.pipe = self._load_pipeline()

    def _load_pipeline(self) -> WanPipeline:
        """
        Load the official Wan2.1 T2V 1.3B Diffusers pipeline.
        """

        dtype = (
            torch.bfloat16
            if torch.cuda.is_bf16_supported()
            else torch.float16
        )

        vae = AutoencoderKLWan.from_pretrained(
            self.MODEL_ID,
            subfolder="vae",
            torch_dtype=torch.float32,
        )

        pipe = WanPipeline.from_pretrained(
            self.MODEL_ID,
            vae=vae,
            torch_dtype=dtype,
        )

        pipe.scheduler = (
            UniPCMultistepScheduler.from_config(
                pipe.scheduler.config,
                flow_shift=self.flow_shift,
            )
        )

        pipe.enable_model_cpu_offload()

        return pipe

    @staticmethod
    def _frame_count(
        duration: float,
        fps: int,
    ) -> int:
        """
        Wan recommends frame counts of 4*k + 1.
        """

        duration = max(
            1.0,
            float(duration),
        )

        fps = max(
            8,
            min(24, int(fps)),
        )

        requested = max(
            81,
            round(duration * fps),
        )

        k = max(
            20,
            round((requested - 1) / 4),
        )

        return 4 * k + 1

    @staticmethod
    def _resolution(
        metadata: Dict[str, Any],
    ):
        raw = str(
            metadata.get(
                "resolution",
                os.getenv(
                    "AJVYRA_WAN_RESOLUTION",
                    "832x480",
                ),
            )
        )

        try:
            width, height = raw.lower().split(
                "x",
                1,
            )

            width = int(width)
            height = int(height)

        except Exception as exc:
            raise ProviderError(
                f"Invalid Wan resolution: {raw}"
            ) from exc

        if width < 256 or height < 256:
            raise ProviderError(
                f"Wan resolution too small: {raw}"
            )

        return width, height

    @staticmethod
    def _negative_prompt() -> str:
        return (
            "bright tones, overexposed, static, "
            "blurred details, subtitles, text, logos, "
            "low quality, worst quality, JPEG artifacts, "
            "ugly, incomplete, deformed face, "
            "poorly drawn face, extra fingers, "
            "fused fingers, malformed hands, "
            "misshapen limbs, duplicate people, "
            "three legs, distorted body, "
            "still picture, messy background"
        )

    def generate(
        self,
        prompt: str,
        first_frame: Optional[Path],
        references: Sequence[Path],
        duration: float,
        output: Path,
        metadata: Dict[str, Any],
    ) -> MediaAsset:

        if not prompt.strip():
            raise ProviderError(
                "Wan received an empty prompt."
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fps = int(
            metadata.get(
                "fps",
                16,
            )
        )

        width, height = self._resolution(
            metadata
        )

        num_frames = self._frame_count(
            duration,
            fps,
        )

        seed = int(
            metadata.get(
                "seed",
                0,
            )
        )

        if seed <= 0:
            seed = (
                int(
                    stable_id(
                        metadata.get(
                            "anime_id",
                            "anime",
                        ),
                        metadata.get(
                            "shot_id",
                            "shot",
                        ),
                    ),
                    16,
                )
                % (2**31 - 1)
            )

        generator = torch.Generator(
            device="cuda"
        ).manual_seed(seed)

        try:

            result = self.pipe(
                prompt=prompt,
                negative_prompt=(
                    self._negative_prompt()
                ),
                height=height,
                width=width,
                num_frames=num_frames,
                guidance_scale=(
                    self.guidance_scale
                ),
                generator=generator,
            )

            frames = result.frames[0]

            export_to_video(
                frames,
                str(output),
                fps=fps,
            )

        except Exception as exc:

            raise ProviderError(
                "Wan generation failed: "
                f"{exc}"
            ) from exc

        if not output.exists():
            raise ProviderError(
                "Wan completed without creating "
                f"the expected MP4: {output}"
            )

        if output.stat().st_size < 10_000:
            raise ProviderError(
                "Wan created an invalid or empty MP4: "
                f"{output}"
            )

        actual_duration = (
            len(frames) / fps
        )

        metadata_out = {
            **metadata,
            "model": self.MODEL_ID,
            "provider": self.name,
            "width": width,
            "height": height,
            "fps": fps,
            "frames": num_frames,
            "actual_duration": actual_duration,
            "seed": seed,
            "real_generation": True,
        }

        return MediaAsset(
            asset_id=stable_id(
                self.name,
                output,
            ),
            asset_type="video",
            path=str(output),
            duration=actual_duration,
            mime_type="video/mp4",
            provider=self.name,
            status="created",
            metadata=metadata_out,
        )


class AJVYRAWanAnimeProductionEngine(
    AJVYRAAnimeRealProductionEngine
):
    """
    AJVYRA's real anime engine with Wan2.1
    replacing the placeholder video provider.
    """

    def _providers(self):

        image, _, voice, music = (
            super()._providers()
        )

        wan_video = (
            AJVYRAWanRealVideoProvider()
        )

        return (
            image,
            wan_video,
            voice,
            music,
        )


def load_catalog(
    path: str,
):
    catalog_path = Path(path)

    if not catalog_path.exists():
        raise FileNotFoundError(
            f"Anime catalog not found: "
            f"{catalog_path}"
        )

    data = json.loads(
        catalog_path.read_text(
            encoding="utf-8"
        )
    )

    if isinstance(data, dict):
        data = data.get(
            "anime",
            data.get(
                "items",
                [],
            ),
        )

    if not isinstance(data, list):
        raise ValueError(
            "Anime catalog must contain a list."
        )

    if len(data) != 30:
        raise ValueError(
            f"Expected exactly 30 anime. "
            f"Found {len(data)}."
        )

    return data


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real 30-anime Wan2.1 "
            "production bridge"
        )
    )

    parser.add_argument(
        "--catalog",
        required=True,
        help="Path to the 30-anime catalog JSON.",
    )

    parser.add_argument(
        "--mode",
        default="auto",
        choices=["auto", "http", "local"],
        help=(
            "Kept for compatibility with the "
            "existing production engine."
        ),
    )

    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Disable final FFmpeg assembly.",
    )

    parser.add_argument(
        "--log-level",
        default="INFO",
    )

    args = parser.parse_args()

    import logging

    logging.basicConfig(
        level=getattr(
            logging,
            args.log_level.upper(),
            logging.INFO,
        ),
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
    )

    catalog = load_catalog(
        args.catalog
    )

    config = ProductionConfig.from_env(
        provider_mode="local",
        render_enabled=not args.no_render,
        resolution=os.getenv(
            "AJVYRA_WAN_RESOLUTION",
            "832x480",
        ),
        target_fps=int(
            os.getenv(
                "AJVYRA_WAN_FPS",
                "16",
            )
        ),
    )

    engine = (
        AJVYRAWanAnimeProductionEngine(
            config
        )
    )

    reports = (
        engine.produce_30_anime_first_episodes(
            catalog,
            dry_run=False,
        )
    )

    failed = [
        report
        for report in reports
        if report.status != "complete"
    ]

    print(
        json.dumps(
            [
                {
                    "anime_id": report.anime_id,
                    "episode_id": report.episode_id,
                    "status": report.status,
                    "shots_total": report.shots_total,
                    "shots_ready": report.shots_ready,
                    "shots_failed": report.shots_failed,
                    "output_video": report.output_video,
                }
                for report in reports
            ],
            ensure_ascii=False,
            indent=2,
        )
    )

    if failed:
        print(
            "\nAJVYRA WAN RELEASE BLOCKED"
        )
        print(
            f"Failed anime: "
            f"{len(failed)}/30"
        )
        return 2

    print(
        "\nAJVYRA WAN ANIME PRODUCTION: 30/30"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
