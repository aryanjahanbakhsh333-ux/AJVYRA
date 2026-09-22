from __future__ import annotations

import argparse
from pathlib import Path

from ajvyra_local_video_model_config import (
    AJVYRALocalVideoModelConfig,
)
from ajvyra_local_video_model_loader import (
    AJVYRALocalVideoModelLoader,
)
from ajvyra_local_video_generation_engine import (
    AJVYRALocalVideoGenerationEngine,
    AJVYRALocalVideoGenerationRequest,
)


DEFAULT_PROMPT = """
cinematic dark anime film scene,
a young anime protagonist standing alone on a rainy
empty street at night,
black coat moving gently in the wind,
wet pavement reflecting distant city lights,
subtle emotional expression,
slow cinematic camera movement,
dramatic depth of field,
moody blue-gray atmosphere,
detailed anime film aesthetic,
natural body movement,
volumetric rain,
beautiful cinematic lighting,
high visual consistency,
16:9 composition
""".strip()


def build_parser():
    parser = argparse.ArgumentParser(
        description="AJVYRA Local Video Model"
    )

    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
    )

    parser.add_argument(
        "--output",
        default="ajvyra_test_video.mp4",
    )

    parser.add_argument(
        "--model",
        default=None,
    )

    parser.add_argument(
        "--device",
        default=None,
        choices=[
            "auto",
            "cuda",
            "mps",
            "cpu",
        ],
    )

    parser.add_argument(
        "--width",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--height",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--info",
        action="store_true",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    config = AJVYRALocalVideoModelConfig.from_environment()

    if args.model:
        config.model_id = args.model

    if args.device:
        config.device = args.device

    if args.width:
        config.width = args.width

    if args.height:
        config.height = args.height

    if args.frames:
        config.num_frames = args.frames

    config.validate()
    config.ensure_directories()

    loader = AJVYRALocalVideoModelLoader(
        config
    )

    if args.info:
        print(
            "AJVYRA LOCAL VIDEO MODEL"
        )

        for key, value in loader.model_info().items():
            print(
                f"{key}: {value}"
            )

        return 0

    engine = AJVYRALocalVideoGenerationEngine(
        config=config,
        loader=loader,
    )

    request = AJVYRALocalVideoGenerationRequest(
        prompt=args.prompt,
        output_name=Path(
            args.output
        ).name,
        width=args.width,
        height=args.height,
        num_frames=args.frames,
        seed=args.seed,
    )

    print(
        "Loading AJVYRA local video model..."
    )

    result = engine.generate(
        request
    )

    if not result.success:
        print(
            "VIDEO GENERATION FAILED"
        )
        print(
            result.error
        )
        return 1

    print(
        "VIDEO GENERATION SUCCESS"
    )
    print(
        f"Output: {result.output_path}"
    )
    print(
        f"Seed: {result.seed}"
    )
    print(
        f"Model: {result.model_id}"
    )
    print(
        f"SHA256: {result.sha256}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
