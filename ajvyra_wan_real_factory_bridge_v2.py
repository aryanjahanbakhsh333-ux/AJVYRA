from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class WanGenerationJob:
    film_id: str
    film_title: str
    shot_id: str
    prompt: str
    output_path: str
    ckpt_dir: str
    task: str = "t2v-1.3B"
    size: str = "832*480"
    frame_num: Optional[int] = None
    seed: int = 0
    offload_model: bool = True
    t5_cpu: bool = True
    sample_shift: int = 8
    sample_guide_scale: float = 6.0


class AJVYRAWanRealFactoryBridgeV2:
    """
    Real execution bridge between AJVYRA's production factory
    and the official Wan2.1 generate.py entrypoint.

    This class does not fake generated media.
    A successful job requires an actual output video file.
    """

    def __init__(
        self,
        wan_root: str,
        checkpoint_dir: str,
        output_root: str = "ajvyra_production",
        python_executable: str = "python",
    ):
        self.wan_root = Path(wan_root).resolve()
        self.checkpoint_dir = Path(checkpoint_dir).resolve()
        self.output_root = Path(output_root).resolve()
        self.python_executable = python_executable

        self.generate_script = self.wan_root / "generate.py"

        self.output_root.mkdir(parents=True, exist_ok=True)

    def validate_installation(self) -> None:
        if not self.wan_root.exists():
            raise FileNotFoundError(
                f"Wan root does not exist: {self.wan_root}"
            )

        if not self.generate_script.exists():
            raise FileNotFoundError(
                f"Wan generate.py was not found: {self.generate_script}"
            )

        if not self.checkpoint_dir.exists():
            raise FileNotFoundError(
                f"Wan checkpoint directory does not exist: "
                f"{self.checkpoint_dir}"
            )

    def build_command(self, job: WanGenerationJob) -> list[str]:
        command = [
            self.python_executable,
            str(self.generate_script),
            "--task",
            job.task,
            "--size",
            job.size,
            "--ckpt_dir",
            str(job.ckpt_dir),
            "--prompt",
            job.prompt,
            "--offload_model",
            str(job.offload_model),
            "--t5_cpu",
            str(job.t5_cpu),
            "--sample_shift",
            str(job.sample_shift),
            "--sample_guide_scale",
            str(job.sample_guide_scale),
            "--base_seed",
            str(job.seed),
        ]

        if job.frame_num is not None:
            command.extend(
                [
                    "--frame_num",
                    str(job.frame_num),
                ]
            )

        return command

    def run(self, job: WanGenerationJob) -> Path:
        self.validate_installation()

        output_path = Path(job.output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        command = self.build_command(job)

        result = subprocess.run(
            command,
            cwd=str(self.wan_root),
            capture_output=True,
            text=True,
        )

        log_path = output_path.with_suffix(".wan.log")
        log_path.write_text(
            result.stdout + "\n" + result.stderr,
            encoding="utf-8",
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Wan generation failed for "
                f"{job.film_id}/{job.shot_id}. "
                f"See {log_path}"
            )

        if not output_path.exists():
            raise RuntimeError(
                f"Wan process completed but expected output was not found: "
                f"{output_path}"
            )

        if output_path.stat().st_size <= 0:
            raise RuntimeError(
                f"Wan produced an empty output file: {output_path}"
            )

        return output_path

    def save_job_manifest(self, job: WanGenerationJob) -> Path:
        path = Path(job.output_path).with_suffix(".job.json")
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(
                asdict(job),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return path
