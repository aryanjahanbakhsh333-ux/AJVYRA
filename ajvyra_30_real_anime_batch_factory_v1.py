from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

import torch
from diffusers import AutoencoderKLWan, WanPipeline
from diffusers.utils import export_to_video


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


class AJVYRA30RealAnimeFactory:
    MODEL_ID = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

    NEGATIVE_PROMPT = (
        "low quality, blurry, distorted face, deformed hands, "
        "extra fingers, extra limbs, duplicated characters, "
        "bad anatomy, flickering, static image, subtitles, text, "
        "watermark, logo, broken motion, corrupted frames"
    )

    def __init__(
        self,
        root: str = "assets/anime-production-v1",
        final_root: str = "assets/anime-final",
        shots_per_movie: int = 6,
        frames: int = 81,
        width: int = 832,
        height: int = 480,
        steps: int = 30,
        fps: int = 16,
    ):
        self.root = Path(root)
        self.final_root = Path(final_root)

        self.shots_per_movie = max(1, shots_per_movie)
        self.frames = frames
        self.width = width
        self.height = height
        self.steps = steps
        self.fps = fps

        self.root.mkdir(parents=True, exist_ok=True)
        self.final_root.mkdir(parents=True, exist_ok=True)

        self.pipe = None

    @staticmethod
    def slug(value: str) -> str:
        return "".join(
            c.lower() if c.isalnum() else "_"
            for c in value
        ).strip("_")

    def load_model(self):
        if self.pipe is not None:
            return

        dtype = (
            torch.bfloat16
            if torch.cuda.is_available()
            else torch.float32
        )

        vae = AutoencoderKLWan.from_pretrained(
            self.MODEL_ID,
            subfolder="vae",
            torch_dtype=torch.float32,
        )

        self.pipe = WanPipeline.from_pretrained(
            self.MODEL_ID,
            vae=vae,
            torch_dtype=dtype,
        )

        if torch.cuda.is_available():
            self.pipe.enable_model_cpu_offload()
        else:
            self.pipe.to("cpu")

    def prompt_for(
        self,
        title: str,
        shot_number: int,
    ) -> str:

        shots = [
            (
                "wide cinematic establishing shot of a mysterious "
                "anime city at night, rain, neon reflections"
            ),
            (
                "close cinematic shot of the main anime protagonist "
                "walking alone through rain, emotional expression"
            ),
            (
                "dynamic anime action sequence, protagonist running "
                "through a dark ruined street, dramatic camera movement"
            ),
            (
                "quiet emotional anime scene, protagonist standing "
                "under a lonely street light, wind moving clothing"
            ),
            (
                "dramatic confrontation between anime characters, "
                "cinematic lighting, controlled camera movement"
            ),
            (
                "final emotional anime scene at dawn, protagonist "
                "looking toward the distant horizon"
            ),
        ]

        scene = shots[
            min(shot_number, len(shots) - 1)
        ]

        return (
            f"{title}, original anime cinematic film, "
            f"{scene}, detailed character design, "
            f"consistent character appearance, "
            f"cinematic composition, smooth motion, "
            f"professional animated-film look"
        )

    def generate_shot(
        self,
        title: str,
        movie_dir: Path,
        shot_number: int,
    ) -> Path:

        self.load_model()

        output = movie_dir / (
            f"shot_{shot_number + 1:02d}.mp4"
        )

        if output.exists() and output.stat().st_size > 10_000:
            return output

        prompt = self.prompt_for(
            title,
            shot_number,
        )

        seed = 1000 + (
            FILMS.index(title) * 100
        ) + shot_number

        generator = torch.Generator(
            device="cpu"
        ).manual_seed(seed)

        result = self.pipe(
            prompt=prompt,
            negative_prompt=self.NEGATIVE_PROMPT,
            height=self.height,
            width=self.width,
            num_frames=self.frames,
            guidance_scale=5.0,
            generator=generator,
        )

        frames = result.frames[0]

        export_to_video(
            frames,
            str(output),
            fps=self.fps,
        )

        if not output.exists():
            raise RuntimeError(
                f"Wan failed to create {output}"
            )

        if output.stat().st_size <= 10_000:
            raise RuntimeError(
                f"Generated video is invalid: {output}"
            )

        return output

    def assemble(
        self,
        title: str,
        shots: list[Path],
    ) -> Path:

        slug = self.slug(title)

        final_movie = (
            self.final_root /
            f"{slug}.mp4"
        )

        concat_file = (
            self.root /
            f"{slug}_concat.txt"
        )

        with concat_file.open(
            "w",
            encoding="utf-8",
        ) as handle:

            for shot in shots:
                absolute = shot.resolve()
                handle.write(
                    f"file '{absolute.as_posix()}'\n"
                )

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(final_movie),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                result.stderr
            )

        if not final_movie.exists():
            raise RuntimeError(
                f"Final movie was not created: {final_movie}"
            )

        return final_movie

    def write_release(
        self,
        title: str,
        shots: list[Path],
        final_movie: Path,
    ) -> Path:

        slug = self.slug(title)

        record = {
            "type": "anime",
            "id": f"anime-{slug}",
            "title": title,
            "model": self.MODEL_ID,
            "real_generated": True,
            "shots": [
                {
                    "path": str(path),
                    "bytes": path.stat().st_size,
                }
                for path in shots
            ],
            "final_video": str(final_movie),
            "ready": True,
            "published": True,
        }

        output = (
            self.final_root /
            f"{slug}.release.json"
        )

        output.write_text(
            json.dumps(
                record,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return output

    def produce_movie(
        self,
        title: str,
    ) -> dict[str, Any]:

        slug = self.slug(title)

        movie_dir = (
            self.root /
            slug
        )

        movie_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        shots = []

        for shot_number in range(
            self.shots_per_movie
        ):
            print(
                f"[ANIME] {title} "
                f"{shot_number + 1}/"
                f"{self.shots_per_movie}"
            )

            shots.append(
                self.generate_shot(
                    title,
                    movie_dir,
                    shot_number,
                )
            )

        final_movie = self.assemble(
            title,
            shots,
        )

        release = self.write_release(
            title,
            shots,
            final_movie,
        )

        return {
            "title": title,
            "video": str(final_movie),
            "release": str(release),
            "ready": True,
        }

    def produce_all(self) -> list[dict[str, Any]]:

        results = []

        for title in FILMS:
            results.append(
                self.produce_movie(title)
            )

        if len(results) != 30:
            raise RuntimeError(
                "30-anime production failed."
            )

        return results


if __name__ == "__main__":
    factory = AJVYRA30RealAnimeFactory()

    results = factory.produce_all()

    print(
        f"AJVYRA REAL ANIME: "
        f"{len(results)}/30"
    )
