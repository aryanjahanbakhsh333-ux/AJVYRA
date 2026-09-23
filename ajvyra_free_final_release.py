from __future__ import annotations

import json
import sys
from pathlib import Path

from ajvyra_free_local_config import Config
from ajvyra_free_anime_jobs import (
    make_jobs,
    seed_for,
)
from ajvyra_free_production_queue import (
    Queue,
)
from ajvyra_free_wan_workflow import (
    WanWorkflow,
)
from ajvyra_free_comfyui_client import (
    ComfyUIClient,
)
from ajvyra_free_quality_gate import (
    QualityGate,
)
from ajvyra_free_game_release_gate import (
    GameReleaseGate,
)


def save_json(
    path: Path,
    data
):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def main():

    config = Config.load()

    config.prepare()

    print(
        "AJVYRA FREE LOCAL PRODUCTION"
    )

    print(
        "Paid API: NONE"
    )

    print(
        "Provider: Local ComfyUI + Wan"
    )

    config.validate()

    jobs = make_jobs(
        config.root,
        config.output
    )

    queue = Queue(
        config.output
        / "manifests"
        / "production_queue.json"
    )

    queue.create(
        jobs
    )

    workflow_builder = WanWorkflow(
        config.workflow_file
    )

    client = ComfyUIClient(
        config.comfy_url
    )

    quality = QualityGate(
        config.minimum_video_size
    )

    pending = queue.pending()

    print(
        f"Jobs waiting: {len(pending)}"
    )

    for job in pending:

        job_id = job["job_id"]

        output = Path(
            job["output_file"]
        )

        if output.exists():

            errors = quality.check_video(
                output
            )

            if not errors:

                queue.update(
                    job_id,
                    status="complete",
                    error=""
                )

                continue

        retries = int(
            job.get("retries", 0)
        )

        if retries >= config.max_retries:

            queue.update(
                job_id,
                status="failed",
                error="maximum retries exceeded"
            )

            continue

        queue.update(
            job_id,
            status="running",
            retries=retries + 1
        )

        try:

            workflow = workflow_builder.build(
                prompt=job["prompt"],
                negative_prompt=job[
                    "negative_prompt"
                ],
                seed=seed_for(
                    job["anime_number"],
                    job["segment_number"]
                ),
                width=config.width,
                height=config.height,
            )

            prompt_id = client.queue_prompt(
                workflow
            )

            print(
                f"[GENERATING] {job_id}"
            )

            history = client.wait(
                prompt_id
            )

            files = client.find_outputs(
                history
            )

            if not files:
                raise RuntimeError(
                    "ComfyUI finished but returned "
                    "no video output."
                )

            print(
                f"[DONE] {job_id}"
            )

            queue.update(
                job_id,
                status="complete",
                error=""
            )

        except Exception as exc:

            queue.update(
                job_id,
                status="retry",
                error=str(exc)
            )

            print(
                f"[RETRY] {job_id}: {exc}"
            )

    anime_errors = {}

    for number in range(1, 31):

        folder = (
            config.output
            / "anime"
            / f"anime_{number:02d}"
        )

        errors = quality.check_anime(
            folder
        )

        if errors:
            anime_errors[
                f"anime_{number:02d}"
            ] = errors

    games = GameReleaseGate(
        config.root
    ).check()

    ready_anime = (
        30 - len(anime_errors)
    )

    release_ready = (
        ready_anime == 30
        and games["ready"]
    )

    report = {
        "project": "AJVYRA",

        "production": {
            "paid_api": False,
            "local_comfyui": True,
            "wan_generation": True,
        },

        "anime": {
            "required": 30,
            "ready": ready_anime,
            "failed": len(
                anime_errors
            ),
            "errors": anime_errors,
        },

        "games": games,

        "release_ready":
            release_ready,
    }

    report_file = (
        config.output
        / "manifests"
        / "FINAL_RELEASE.json"
    )

    save_json(
        report_file,
        report
    )

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2
        )
    )

    if not release_ready:

        print(
            "\nRELEASE BLOCKED"
        )

        sys.exit(2)

    print(
        "\nAJVYRA FINAL RELEASE READY"
    )


if __name__ == "__main__":
    main()
