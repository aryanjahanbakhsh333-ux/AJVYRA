"""
AJVYRA Cloud Wan Video Worker V1

Consumes the AJVYRA production queue and requests REAL
text-to-video generation from a cloud inference provider.

Required:
    HF_TOKEN

Optional:
    HF_PROVIDER=fal-ai
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from huggingface_hub import InferenceClient


MODEL = "Wan-AI/Wan2.1-T2V-1.3B"


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp = path.with_suffix(".tmp")

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

    tmp.replace(path)


def generate(client, job, output):
    prompt = job["prompt"]

    negative = job.get(
        "negative_prompt",
        ""
    )

    seed = job.get("seed")

    kwargs = {
        "prompt": prompt,
        "model": MODEL,
    }

    if negative:
        kwargs["negative_prompt"] = negative

    if seed is not None:
        kwargs["seed"] = seed

    video = client.text_to_video(
        **kwargs
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(output, "wb") as f:
        f.write(video)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--queue",
        required=True
    )

    parser.add_argument(
        "--output-root",
        required=True
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None
    )

    parser.add_argument(
        "--retry",
        type=int,
        default=3
    )

    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")

    if not token:
        raise RuntimeError(
            "HF_TOKEN environment variable is required."
        )

    provider = os.environ.get(
        "HF_PROVIDER",
        "fal-ai"
    )

    client = InferenceClient(
        provider=provider,
        api_key=token
    )

    queue_path = Path(args.queue)
    root = Path(args.output_root)

    data = load(queue_path)

    jobs = data["jobs"]

    if args.limit:
        jobs = jobs[:args.limit]

    completed = 0
    failed = 0

    for number, job in enumerate(
        jobs,
        start=1
    ):

        relative = Path(
            job["output_file"]
        )

        output = root / relative

        if output.exists() and output.stat().st_size > 1024:
            print(
                f"[{number}/{len(jobs)}] SKIP "
                f"{job['job_id']}"
            )
            completed += 1
            continue

        print(
            f"[{number}/{len(jobs)}] GENERATE "
            f"{job['film_title']} / "
            f"{job['job_id']}"
        )

        success = False

        for attempt in range(
            1,
            args.retry + 1
        ):

            try:

                generate(
                    client,
                    job,
                    output
                )

                if output.exists() and output.stat().st_size > 1024:
                    success = True
                    completed += 1
                    break

            except Exception as exc:

                print(
                    f"Attempt {attempt} failed: {exc}"
                )

                time.sleep(
                    min(attempt * 5, 30)
                )

        if not success:
            failed += 1

            print(
                f"FAILED: {job['job_id']}"
            )

            # Stop rather than silently producing
            # an incomplete film.
            break

    state = {
        "completed": completed,
        "failed": failed,
        "finished": failed == 0
    }

    save(
        root / "cloud-worker-state.json",
        state
    )

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
