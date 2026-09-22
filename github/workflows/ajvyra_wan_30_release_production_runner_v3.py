"""
AJVYRA — Real 30-Film Production Runner V3

Purpose
-------
Runs the REAL Wan video generation pipeline for AJVYRA's 30 anime films.

Flow
----
Production Manifest
        ↓
Film
        ↓
Shot
        ↓
Official Wan generate.py
        ↓
Real MP4
        ↓
Production manifest/state
        ↓
Existing Assembly + QC + Release pipeline
        ↓
Existing Site Release Catalog

Important
---------
This script does NOT generate fake videos.
It does NOT create placeholder MP4 files.
It does NOT render the website before production is complete.

It is designed to run on a machine/cloud GPU where Wan2.1 is installed.

The official Wan CLI is expected to support:
    --save_file
    --task
    --size
    --frame_num
    --ckpt_dir
    --offload_model
    --t5_cpu
    --sample_steps
    --seed

Default mode:
    t2v-1.3B
    832*480
    sequential GPU production

The script is resume-safe:
existing valid MP4 files are skipped unless --force is supplied.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ============================================================
# AJVYRA 30 FILM CATALOG
# ============================================================

FILMS = [
    "Veylora",
    "Aelvryn",
    "Nyxara",
    "Kaelith",
    "Orivane",
    "Zeravia",
    "Vaelune",
    "Ravelyth",
    "Solvarya",
    "Xaveren",
    "Elyvara",
    "Neravelle",
    "Vaerith",
    "Lunavyr",
    "Averlyn",
    "Neyvara",
    "Elvaria",
    "Virelya",
    "Caelora",
    "Seravyn",
    "Mouravia",
    "Noxelya",
    "Vaelora",
    "Eryndra",
    "Neylith",
    "Auralyne",
    "Velmora",
    "Seyravia",
    "Oryvane",
    "Luminarae",
]


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class ShotJob:
    film_id: str
    film_title: str
    shot_id: str
    prompt: str
    negative_prompt: str = ""
    frame_num: int = 81
    seed: int | None = None
    reference_image: str | None = None


@dataclass
class ShotResult:
    film_id: str
    film_title: str
    shot_id: str
    status: str
    output_file: str
    started_at: str
    finished_at: str
    command: list[str]
    error: str = ""


# ============================================================
# HELPERS
# ============================================================

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_name(value: str) -> str:
    result = "".join(
        c if c.isalnum() or c in ("-", "_")
        else "_"
        for c in value.strip()
    )

    return result.strip("_") or "untitled"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(path.suffix + ".tmp")

    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(
            data,
            handle,
            ensure_ascii=False,
            indent=2,
        )

    temporary.replace(path)


def valid_mp4(path: Path) -> bool:
    if not path.exists():
        return False

    if not path.is_file():
        return False

    try:
        size = path.stat().st_size
    except OSError:
        return False

    # Prevent accepting an accidentally created empty/tiny file.
    return size >= 1024 * 1024


def normalize_prompt(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


# ============================================================
# MANIFEST NORMALIZATION
# ============================================================

def extract_films(raw: Any) -> list[dict[str, Any]]:
    """
    Supports several manifest layouts so the runner can work
    with the existing AJVYRA production manifests.
    """

    if isinstance(raw, list):
        return [
            item for item in raw
            if isinstance(item, dict)
        ]

    if not isinstance(raw, dict):
        raise ValueError("Production manifest must be a JSON object or list.")

    for key in (
        "films",
        "anime",
        "movies",
        "productions",
        "items",
    ):
        value = raw.get(key)

        if isinstance(value, list):
            return [
                item for item in value
                if isinstance(item, dict)
            ]

    raise ValueError(
        "Could not find a film collection in the production manifest."
    )


def extract_shots(film: dict[str, Any]) -> list[dict[str, Any]]:
    for key in (
        "shots",
        "segments",
        "scenes",
        "clips",
    ):
        value = film.get(key)

        if isinstance(value, list):
            return [
                item for item in value
                if isinstance(item, dict)
            ]

    return []


def build_jobs(
    manifest_path: Path,
    default_frame_num: int,
) -> list[ShotJob]:

    raw = load_json(manifest_path)

    films = extract_films(raw)

    jobs: list[ShotJob] = []

    seen_films: set[str] = set()

    for index, film in enumerate(films, start=1):

        film_id = str(
            film.get("id")
            or film.get("film_id")
            or film.get("slug")
            or f"film_{index:02d}"
        )

        film_title = str(
            film.get("title")
            or film.get("name")
            or FILMS[index - 1]
            if index <= len(FILMS)
            else film_id
        )

        if film_title in seen_films:
            continue

        seen_films.add(film_title)

        shots = extract_shots(film)

        for shot_index, shot in enumerate(shots, start=1):

            shot_id = str(
                shot.get("id")
                or shot.get("shot_id")
                or shot.get("segment_id")
                or f"shot_{shot_index:04d}"
            )

            prompt = normalize_prompt(
                shot.get("prompt")
                or shot.get("text")
                or shot.get("description")
                or shot.get("visual_prompt")
            )

            if not prompt:
                raise ValueError(
                    f"Missing prompt for {film_title}/{shot_id}"
                )

            negative_prompt = normalize_prompt(
                shot.get("negative_prompt")
                or shot.get("negative")
            )

            frame_num = int(
                shot.get("frame_num")
                or shot.get("frames")
                or default_frame_num
            )

            seed = shot.get("seed")

            if seed is not None:
                seed = int(seed)

            reference_image = (
                shot.get("reference_image")
                or shot.get("image")
                or shot.get("image_path")
            )

            jobs.append(
                ShotJob(
                    film_id=film_id,
                    film_title=film_title,
                    shot_id=shot_id,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    frame_num=frame_num,
                    seed=seed,
                    reference_image=reference_image,
                )
            )

    if not jobs:
        raise ValueError(
            "No video shots were found in the production manifest."
        )

    return jobs


# ============================================================
# WAN COMMAND BUILDER
# ============================================================

def build_wan_command(
    wan_root: Path,
    checkpoint: Path,
    task: str,
    size: str,
    frame_num: int,
    steps: int,
    seed: int | None,
    output_file: Path,
    prompt: str,
    negative_prompt: str,
    offload_model: bool,
    t5_cpu: bool,
    reference_image: str | None,
) -> list[str]:

    generate_script = wan_root / "generate.py"

    if not generate_script.exists():
        raise FileNotFoundError(
            f"Wan generate.py not found: {generate_script}"
        )

    command = [
        sys.executable,
        str(generate_script),

        "--task",
        task,

        "--size",
        size,

        "--frame_num",
        str(frame_num),

        "--ckpt_dir",
        str(checkpoint),

        "--sample_steps",
        str(steps),

        "--save_file",
        str(output_file),

        "--prompt",
        prompt,
    ]

    if negative_prompt:
        command.extend([
            "--negative_prompt",
            negative_prompt,
        ])

    if seed is not None:
        command.extend([
            "--seed",
            str(seed),
        ])

    if offload_model:
        command.extend([
            "--offload_model",
            "True",
        ])

    if t5_cpu:
        command.extend([
            "--t5_cpu",
        ])

    # I2V reference image support.
    if reference_image:
        command.extend([
            "--image",
            str(reference_image),
        ])

    return command


# ============================================================
# PRODUCTION RUNNER
# ============================================================

class AJVYRAWanProductionRunner:

    def __init__(
        self,
        wan_root: Path,
        checkpoint: Path,
        output_root: Path,
        task: str,
        size: str,
        steps: int,
        default_frame_num: int,
        offload_model: bool,
        t5_cpu: bool,
        force: bool,
        limit: int | None,
    ):

        self.wan_root = wan_root.resolve()
        self.checkpoint = checkpoint.resolve()
        self.output_root = output_root.resolve()

        self.task = task
        self.size = size
        self.steps = steps
        self.default_frame_num = default_frame_num

        self.offload_model = offload_model
        self.t5_cpu = t5_cpu

        self.force = force
        self.limit = limit

        self.state_path = (
            self.output_root
            / "ajvyra_real_30_production_state.json"
        )

        self.results_path = (
            self.output_root
            / "ajvyra_real_30_production_results.json"
        )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    def load_state(self) -> dict[str, Any]:

        if not self.state_path.exists():
            return {
                "project": "AJVYRA",
                "films": FILMS,
                "started_at": utc_now(),
                "jobs": {},
            }

        return load_json(self.state_path)

    def save_state(self, state: dict[str, Any]) -> None:
        save_json(self.state_path, state)

    # --------------------------------------------------------
    # OUTPUT PATH
    # --------------------------------------------------------

    def shot_output_path(
        self,
        job: ShotJob,
    ) -> Path:

        film_directory = (
            self.output_root
            / safe_name(job.film_title)
        )

        film_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return (
            film_directory
            / f"{safe_name(job.shot_id)}.mp4"
        )

    # --------------------------------------------------------
    # RUN ONE SHOT
    # --------------------------------------------------------

    def run_job(
        self,
        job: ShotJob,
        state: dict[str, Any],
    ) -> ShotResult:

        output_file = self.shot_output_path(job)

        job_key = f"{job.film_title}:{job.shot_id}"

        started = utc_now()

        if valid_mp4(output_file) and not self.force:

            result = ShotResult(
                film_id=job.film_id,
                film_title=job.film_title,
                shot_id=job.shot_id,
                status="SKIPPED_EXISTING",
                output_file=str(output_file),
                started_at=started,
                finished_at=utc_now(),
                command=[],
            )

            state["jobs"][job_key] = asdict(result)

            self.save_state(state)

            return result

        # ----------------------------------------------------
        # Safety: never delete an existing asset automatically.
        # --force is intentionally required.
        # ----------------------------------------------------

        if output_file.exists() and self.force:
            output_file.unlink()

        command = build_wan_command(
            wan_root=self.wan_root,
            checkpoint=self.checkpoint,
            task=self.task,
            size=self.size,
            frame_num=job.frame_num,
            steps=self.steps,
            seed=job.seed,
            output_file=output_file,
            prompt=job.prompt,
            negative_prompt=job.negative_prompt,
            offload_model=self.offload_model,
            t5_cpu=self.t5_cpu,
            reference_image=job.reference_image,
        )

        print()
        print("=" * 72)
        print(f"AJVYRA REAL PRODUCTION")
        print(f"Film : {job.film_title}")
        print(f"Shot : {job.shot_id}")
        print(f"Task : {self.task}")
        print(f"Size : {self.size}")
        print(f"Output: {output_file}")
        print("=" * 72)

        try:

            completed = subprocess.run(
                command,
                cwd=self.wan_root,
                check=False,
            )

            if completed.returncode != 0:

                result = ShotResult(
                    film_id=job.film_id,
                    film_title=job.film_title,
                    shot_id=job.shot_id,
                    status="FAILED",
                    output_file=str(output_file),
                    started_at=started,
                    finished_at=utc_now(),
                    command=command,
                    error=(
                        f"Wan exited with code "
                        f"{completed.returncode}"
                    ),
                )

                state["jobs"][job_key] = asdict(result)
                self.save_state(state)

                return result

            if not valid_mp4(output_file):

                result = ShotResult(
                    film_id=job.film_id,
                    film_title=job.film_title,
                    shot_id=job.shot_id,
                    status="FAILED_NO_VALID_OUTPUT",
                    output_file=str(output_file),
                    started_at=started,
                    finished_at=utc_now(),
                    command=command,
                    error=(
                        "Wan finished without producing "
                        "a valid MP4 output."
                    ),
                )

                state["jobs"][job_key] = asdict(result)
                self.save_state(state)

                return result

            result = ShotResult(
                film_id=job.film_id,
                film_title=job.film_title,
                shot_id=job.shot_id,
                status="READY",
                output_file=str(output_file),
                started_at=started,
                finished_at=utc_now(),
                command=command,
            )

            state["jobs"][job_key] = asdict(result)

            self.save_state(state)

            return result

        except Exception as exc:

            result = ShotResult(
                film_id=job.film_id,
                film_title=job.film_title,
                shot_id=job.shot_id,
                status="FAILED_EXCEPTION",
                output_file=str(output_file),
                started_at=started,
                finished_at=utc_now(),
                command=command,
                error=str(exc),
            )

            state["jobs"][job_key] = asdict(result)

            self.save_state(state)

            return result

    # --------------------------------------------------------
    # FULL RUN
    # --------------------------------------------------------

    def run(
        self,
        manifest_path: Path,
    ) -> int:

        print()
        print("╔══════════════════════════════════════════════════════════╗")
        print("║        AJVYRA REAL 30-FILM PRODUCTION RUNNER           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()

        print(f"Wan root   : {self.wan_root}")
        print(f"Checkpoint : {self.checkpoint}")
        print(f"Manifest   : {manifest_path}")
        print(f"Output     : {self.output_root}")
        print(f"Task       : {self.task}")
        print(f"Resolution : {self.size}")
        print(f"Steps      : {self.steps}")
        print()

        jobs = build_jobs(
            manifest_path=manifest_path,
            default_frame_num=self.default_frame_num,
        )

        if self.limit is not None:
            jobs = jobs[:self.limit]

        state = self.load_state()

        results: list[ShotResult] = []

        for number, job in enumerate(jobs, start=1):

            print(
                f"\n[{number}/{len(jobs)}] "
                f"{job.film_title} / {job.shot_id}"
            )

            result = self.run_job(
                job=job,
                state=state,
            )

            results.append(result)

            if result.status.startswith("FAILED"):
                print(
                    f"FAILED: {result.error}"
                )

                # Stop immediately.
                # A failed shot must never silently become
                # a released film.
                print()
                print(
                    "PRODUCTION STOPPED — "
                    "failed shot detected."
                )

                self.write_results(results)

                return 1

        self.write_results(results)

        print()
        print("=" * 72)
        print("ALL REQUESTED SHOTS PRODUCED SUCCESSFULLY")
        print("=" * 72)

        return 0

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    def write_results(
        self,
        results: list[ShotResult],
    ) -> None:

        payload = {
            "project": "AJVYRA",
            "generated_at": utc_now(),
            "total_jobs": len(results),
            "ready": sum(
                r.status in {
                    "READY",
                    "SKIPPED_EXISTING",
                }
                for r in results
            ),
            "failed": sum(
                r.status.startswith("FAILED")
                for r in results
            ),
            "results": [
                asdict(result)
                for result in results
            ],
        }

        save_json(
            self.results_path,
            payload,
        )


# ============================================================
# RELEASE CONNECTION
# ============================================================

def create_release_bridge(
    output_root: Path,
) -> Path:

    bridge_path = (
        output_root
        / "ajvyra-production-to-release-bridge.json"
    )

    payload = {
        "project": "AJVYRA",
        "created_at": utc_now(),
        "production_root": str(output_root),
        "next_pipeline": [
            "ajvyra_wan_real_output_controller_v2.py",
            "ajvyra_wan_30_film_assembly_factory_v2.py",
            "ajvyra_wan_30_film_release_qc_v2.py",
            "ajvyra_wan_30_final_release_manifest_v2.py",
            "ajvyra_wan_30_release_lock_v2.py",
            "ajvyra_final_release_catalog_connector_v1.js",
            "ajvyra_final_release_gate_integration_v1.js",
            "ajvyra_final_storage_asset_connector_v1.js",
            "ajvyra_final_site_bootstrap_controller_v1.js",
        ],
        "site_must_not_render_until_release_gate": True,
    }

    save_json(
        bridge_path,
        payload,
    )

    return bridge_path


# ============================================================
# CLI
# ============================================================

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real Wan 30-film production runner"
        )
    )

    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to the AJVYRA production manifest JSON.",
    )

    parser.add_argument(
        "--wan-root",
        required=True,
        help="Root directory of the Wan2.1 repository.",
    )

    parser.add_argument(
        "--checkpoint",
        required=True,
        help="Wan checkpoint directory.",
    )

    parser.add_argument(
        "--output-root",
        default="./ajvyra_real_movie_outputs",
        help="Directory for real generated MP4 shots.",
    )

    parser.add_argument(
        "--task",
        default="t2v-1.3B",
        choices=[
            "t2v-1.3B",
            "t2v-14B",
            "i2v-14B",
            "ti2v-5B",
        ],
    )

    parser.add_argument(
        "--size",
        default="832*480",
        help="Wan output size.",
    )

    parser.add_argument(
        "--frame-num",
        type=int,
        default=81,
        help="Default frame count per shot.",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=50,
        help="Wan sampling steps.",
    )

    parser.add_argument(
        "--offload-model",
        action="store_true",
        help="Enable Wan model CPU offloading.",
    )

    parser.add_argument(
        "--t5-cpu",
        action="store_true",
        help="Keep T5 on CPU to reduce VRAM usage.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Regenerate an existing shot. "
            "Without this flag existing valid MP4s are preserved."
        ),
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Generate only the first N shots for a test run.",
    )

    parser.add_argument(
        "--bridge-only",
        action="store_true",
        help="Only create the production-to-release bridge.",
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main() -> int:

    args = parse_args()

    output_root = Path(
        args.output_root
    ).expanduser().resolve()

    if args.bridge_only:

        bridge = create_release_bridge(
            output_root
        )

        print(
            f"Release bridge created: {bridge}"
        )

        return 0

    manifest = Path(
        args.manifest
    ).expanduser().resolve()

    wan_root = Path(
        args.wan_root
    ).expanduser().resolve()

    checkpoint = Path(
        args.checkpoint
    ).expanduser().resolve()

    if not manifest.exists():
        raise FileNotFoundError(
            f"Manifest not found: {manifest}"
        )

    if not wan_root.exists():
        raise FileNotFoundError(
            f"Wan root not found: {wan_root}"
        )

    if not checkpoint.exists():
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint}"
        )

    runner = AJVYRAWanProductionRunner(
        wan_root=wan_root,
        checkpoint=checkpoint,
        output_root=output_root,
        task=args.task,
        size=args.size,
        steps=args.steps,
        default_frame_num=args.frame_num,
        offload_model=args.offload_model,
        t5_cpu=args.t5_cpu,
        force=args.force,
        limit=args.limit,
    )

    exit_code = runner.run(
        manifest_path=manifest,
    )

    if exit_code == 0:
        bridge = create_release_bridge(
            output_root
        )

        print()
        print(
            f"Production → Release bridge: {bridge}"
        )

        print()
        print(
            "IMPORTANT:"
        )
        print(
            "Generated shots are NOT automatically published."
        )
        print(
            "Run the existing assembly/QC/release pipeline next."
        )

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
