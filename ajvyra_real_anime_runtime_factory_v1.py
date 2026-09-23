from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class RealAnimeRuntimeFactory:
    """
    AJVYRA real anime production runtime.

    Pipeline:
        manifest
        -> Wan generation
        -> real MP4 shots
        -> validation
        -> final MP4
        -> release manifest

    This class does not create fake URLs or placeholder videos.
    """

    MODEL = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

    def __init__(
        self,
        output_root: str = "assets/anime-production",
        fps: int = 16,
    ):
        self.output_root = Path(output_root)
        self.fps = fps
        self.output_root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_name(value: str) -> str:
        chars = []
        for char in value.lower():
            if char.isalnum():
                chars.append(char)
            elif char in {" ", "-", "_"}:
                chars.append("_")
        return "".join(chars).strip("_") or "untitled"

    def build_wan_command(
        self,
        prompt: str,
        output_file: Path,
        width: int = 832,
        height: int = 480,
        frames: int = 81,
        steps: int = 30,
        seed: int = 42,
        wan_generate_py: str = "generate.py",
        model_type: str = "t2v-1.3B",
        offload_model: bool = True,
        t5_cpu: bool = False,
    ) -> list[str]:

        command = [
            sys.executable,
            wan_generate_py,
            "--task",
            model_type,
            "--size",
            f"{width}*{height}",
            "--frame_num",
            str(frames),
            "--ckpt_dir",
            self.MODEL,
            "--prompt",
            prompt,
            "--base_seed",
            str(seed),
            "--sample_steps",
            str(steps),
            "--save_file",
            str(output_file),
        ]

        if offload_model:
            command.append("--offload_model")

        if t5_cpu:
            command.append("--t5_cpu")

        return command

    def generate_shot(
        self,
        prompt: str,
        output_file: str,
        **kwargs: Any,
    ) -> Path:

        target = Path(output_file)
        target.parent.mkdir(parents=True, exist_ok=True)

        command = self.build_wan_command(
            prompt=prompt,
            output_file=target,
            **kwargs,
        )

        print("\n[AJVYRA] REAL ANIME SHOT")
        print(" ".join(command))

        result = subprocess.run(
            command,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Wan generation failed with exit code "
                f"{result.returncode}"
            )

        if not target.exists():
            raise RuntimeError(
                f"Wan reported success but MP4 was not created: {target}"
            )

        if target.stat().st_size < 1024:
            raise RuntimeError(
                f"Generated MP4 is suspiciously small: {target}"
            )

        return target

    def validate_mp4(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {
                "ready": False,
                "reason": "missing",
                "path": str(path),
            }

        if path.suffix.lower() != ".mp4":
            return {
                "ready": False,
                "reason": "not_mp4",
                "path": str(path),
            }

        size = path.stat().st_size

        if size < 1024:
            return {
                "ready": False,
                "reason": "file_too_small",
                "path": str(path),
            }

        return {
            "ready": True,
            "path": str(path),
            "bytes": size,
        }

    def write_movie_manifest(
        self,
        title: str,
        shots: list[Path],
        final_movie: Path,
    ) -> Path:

        validations = [
            self.validate_mp4(path)
            for path in shots
        ]

        if not all(item["ready"] for item in validations):
            raise RuntimeError(
                f"Cannot release {title}: one or more shots failed validation."
            )

        if not final_movie.exists():
            raise RuntimeError(
                f"Final movie does not exist: {final_movie}"
            )

        manifest = {
            "title": title,
            "model": self.MODEL,
            "fps": self.fps,
            "shots": [
                {
                    "path": str(path),
                    "bytes": path.stat().st_size,
                }
                for path in shots
            ],
            "final_movie": {
                "path": str(final_movie),
                "bytes": final_movie.stat().st_size,
            },
            "ready": True,
            "published": False,
        }

        name = self._safe_name(title)

        manifest_path = (
            self.output_root /
            f"{name}.release.json"
        )

        manifest_path.write_text(
            json.dumps(
                manifest,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return manifest_path


if __name__ == "__main__":
    print(
        "AJVYRA Real Anime Runtime Factory loaded."
    )
