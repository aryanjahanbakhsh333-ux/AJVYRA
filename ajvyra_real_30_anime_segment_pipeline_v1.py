"""
AJVYRA — REAL 30 ANIME SEGMENT PIPELINE v1

30 anime
× 12 segments
= 360 REAL video-generation jobs

این فایل هنوز قسمت‌ها را به MP4 نهایی 30 دقیقه‌ای متصل نمی‌کند؛
آن کار در بسته‌های بعدی انجام می‌شود.

اینجا فقط تولید واقعی Segmentها انجام می‌شود.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ajvyra_local_real_generation_config_v1 import (
    LocalGenerationConfig,
)
from ajvyra_comfyui_real_http_v1 import (
    RealComfyUIClient,
)
from ajvyra_wan_real_workflow_v1 import (
    WanRealWorkflow,
)
from ajvyra_real_anime_job_builder_v1 import (
    build_anime_jobs,
)
from ajvyra_real_anime_job_store_v1 import (
    AnimeJobStore,
)
from ajvyra_real_anime_segment_generator_v1 import (
    RealAnimeSegmentGenerator,
)
from ajvyra_real_ffprobe_validator_v1 import (
    RealVideoValidator,
)


def run() -> int:

    config = LocalGenerationConfig.from_environment()
    config.validate()

    client = RealComfyUIClient(
        base_url=config.comfyui_url,
        timeout=config.timeout_seconds,
        poll_seconds=config.poll_seconds,
    )

    if not client.health_check():
        raise RuntimeError(
            "ComfyUI is not running or is unreachable.\n"
            "Start your local ComfyUI server first."
        )

    workflow = WanRealWorkflow(
        config.workflow_path
    )

    store = AnimeJobStore(
        config.production_root
        / "state"
        / "anime_segment_jobs.json"
    )

    generator = RealAnimeSegmentGenerator(
        config=config,
        client=client,
        workflow=workflow,
        store=store,
    )

    validator = RealVideoValidator(
        config.ffprobe_binary
    )

    jobs = build_anime_jobs(
        config.production_root
    )

    print(
        f"AJVYRA REAL PIPELINE: "
        f"{len(jobs)} segment jobs"
    )

    completed = 0

    for index, job in enumerate(
        jobs,
        start=1,
    ):

        print(
            f"[{index}/{len(jobs)}] "
            f"Anime {job.anime_number:02d} "
            f"| Segment {job.segment_number:02d} "
            f"| {job.segment_title}"
        )

        attempts = 0

        while True:

            attempts += 1

            try:

                output = generator.generate(
                    job
                )

                probe = validator.require_valid(
                    output,
                    minimum_duration=1.0,
                )

                print(
                    f"  REAL OUTPUT OK "
                    f"{probe.duration:.2f}s "
                    f"{probe.width}x{probe.height} "
                    f"{probe.codec}"
                )

                completed += 1
                break

            except Exception as exc:

                print(
                    f"  FAILED attempt {attempts}: "
                    f"{exc}"
                )

                if attempts >= config.max_retries:
                    raise RuntimeError(
                        f"Production stopped at "
                        f"Anime {job.anime_number}, "
                        f"Segment {job.segment_number}"
                    ) from exc

    print(
        f"REAL SEGMENTS COMPLETE: "
        f"{completed}/{len(jobs)}"
    )

    return 0


def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real 30-anime segment pipeline"
        )
    )

    parser.parse_args()

    return run()


if __name__ == "__main__":
    raise SystemExit(main())
