from __future__ import annotations

import json
import os
import random
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# ============================================================
# AJVYRA — REAL WAN / COMFYUI LOCAL VIDEO ENGINE v9
# ============================================================
#
# Pipeline:
#
# AJVYRA shot
#      ↓
# World / Character prompt
#      ↓
# Real Wan 2.1 T2V
#      ↓
# ComfyUI /prompt
#      ↓
# GPU inference
#      ↓
# WebM output
#      ↓
# FFmpeg
#      ↓
# MP4
#      ↓
# AJVYRA public media
#
# IMPORTANT:
# This file does NOT use Comfy Cloud/API credits.
# It connects to a LOCAL ComfyUI server.
#
# Required:
#   - ComfyUI
#   - Wan 2.1 T2V 1.3B
#   - UMT5 text encoder
#   - Wan VAE
#   - FFmpeg
#
# Default ComfyUI:
#   http://127.0.0.1:8188
#
# ============================================================


class AJVYRAWanConfig:
    COMFY_URL = os.getenv(
        "AJVYRA_COMFY_URL",
        "http://127.0.0.1:8188"
    ).rstrip("/")

    OUTPUT_ROOT = Path(
        os.getenv(
            "AJVYRA_WAN_OUTPUT",
            "ajvyra_public_media/anime"
        )
    )

    MODEL = os.getenv(
        "AJVYRA_WAN_MODEL",
        "wan2.1_t2v_1.3B_fp16.safetensors"
    )

    TEXT_ENCODER = os.getenv(
        "AJVYRA_WAN_TEXT_ENCODER",
        "umt5_xxl_fp8_e4m3fn_scaled.safetensors"
    )

    VAE = os.getenv(
        "AJVYRA_WAN_VAE",
        "wan_2.1_vae.safetensors"
    )

    WIDTH = int(os.getenv("AJVYRA_WAN_WIDTH", "832"))
    HEIGHT = int(os.getenv("AJVYRA_WAN_HEIGHT", "480"))

    # 161 = approximately 10 seconds at 16fps.
    # Use 81 for a lighter first test.
    FRAMES = int(os.getenv("AJVYRA_WAN_FRAMES", "161"))

    FPS = int(os.getenv("AJVYRA_WAN_FPS", "16"))

    STEPS = int(os.getenv("AJVYRA_WAN_STEPS", "30"))
    CFG = float(os.getenv("AJVYRA_WAN_CFG", "6"))

    SHIFT = float(os.getenv("AJVYRA_WAN_SHIFT", "8"))

    SAMPLER = os.getenv(
        "AJVYRA_WAN_SAMPLER",
        "uni_pc"
    )

    SCHEDULER = os.getenv(
        "AJVYRA_WAN_SCHEDULER",
        "simple"
    )

    TIMEOUT = int(
        os.getenv(
            "AJVYRA_WAN_TIMEOUT",
            "7200"
        )
    )

    POLL_SECONDS = float(
        os.getenv(
            "AJVYRA_WAN_POLL",
            "3"
        )
    )


# ============================================================
# HTTP
# ============================================================

class ComfyHTTP:

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Any:

        url = self.base_url + path

        body = None

        headers = {
            "Accept": "application/json",
        }

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        request = Request(
            url,
            data=body,
            headers=headers,
            method=method,
        )

        with urlopen(request, timeout=60) as response:
            raw = response.read()

        if not raw:
            return {}

        try:
            return json.loads(
                raw.decode("utf-8")
            )
        except Exception:
            return raw

    def get(self, path: str):
        return self.request("GET", path)

    def post(self, path: str, payload):
        return self.request(
            "POST",
            path,
            payload,
        )


# ============================================================
# WAN API GRAPH
# ============================================================

class Wan21Graph:

    @staticmethod
    def create(
        prompt: str,
        negative_prompt: str,
        seed: int,
        width: int,
        height: int,
        frames: int,
        steps: int,
        cfg: float,
        shift: float,
        fps: int,
        filename_prefix: str,
    ) -> Dict[str, Any]:

        if frames < 5:
            raise ValueError(
                "Wan video must contain multiple frames."
            )

        # Wan frame count follows 4n+1.
        if (frames - 1) % 4 != 0:
            frames = ((frames - 1) // 4) * 4 + 1

        return {

            # ------------------------------------------------
            # KSampler
            # ------------------------------------------------

            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": "uni_pc",
                    "scheduler": "simple",
                    "denoise": 1.0,

                    "model": [
                        "48",
                        0
                    ],

                    "positive": [
                        "6",
                        0
                    ],

                    "negative": [
                        "7",
                        0
                    ],

                    "latent_image": [
                        "40",
                        0
                    ],
                },

                "class_type": "KSampler",

                "_meta": {
                    "title": "AJVYRA Wan KSampler"
                },
            },

            # ------------------------------------------------
            # Positive prompt
            # ------------------------------------------------

            "6": {
                "inputs": {

                    "text": prompt,

                    "clip": [
                        "38",
                        0
                    ],
                },

                "class_type": "CLIPTextEncode",

                "_meta": {
                    "title": "AJVYRA Positive Prompt"
                },
            },

            # ------------------------------------------------
            # Negative prompt
            # ------------------------------------------------

            "7": {
                "inputs": {

                    "text": negative_prompt,

                    "clip": [
                        "38",
                        0
                    ],
                },

                "class_type": "CLIPTextEncode",

                "_meta": {
                    "title": "AJVYRA Negative Prompt"
                },
            },

            # ------------------------------------------------
            # VAE decode
            # ------------------------------------------------

            "8": {
                "inputs": {

                    "samples": [
                        "3",
                        0
                    ],

                    "vae": [
                        "39",
                        0
                    ],
                },

                "class_type": "VAEDecode",

                "_meta": {
                    "title": "AJVYRA VAE Decode"
                },
            },

            # ------------------------------------------------
            # Wan diffusion model
            # ------------------------------------------------

            "37": {
                "inputs": {

                    "unet_name":
                        AJVYRAWanConfig.MODEL,

                    "weight_dtype":
                        "default",
                },

                "class_type":
                    "UNETLoader",

                "_meta": {
                    "title":
                        "AJVYRA Wan 2.1 Diffusion Model"
                },
            },

            # ------------------------------------------------
            # Wan text encoder
            # ------------------------------------------------

            "38": {
                "inputs": {

                    "clip_name":
                        AJVYRAWanConfig.TEXT_ENCODER,

                    "type":
                        "wan",

                    "device":
                        "default",
                },

                "class_type":
                    "CLIPLoader",

                "_meta": {
                    "title":
                        "AJVYRA Wan Text Encoder"
                },
            },

            # ------------------------------------------------
            # Wan VAE
            # ------------------------------------------------

            "39": {
                "inputs": {

                    "vae_name":
                        AJVYRAWanConfig.VAE,
                },

                "class_type":
                    "VAELoader",

                "_meta": {
                    "title":
                        "AJVYRA Wan VAE"
                },
            },

            # ------------------------------------------------
            # Video latent
            # ------------------------------------------------

            "40": {
                "inputs": {

                    "width":
                        width,

                    "height":
                        height,

                    "length":
                        frames,

                    "batch_size":
                        1,
                },

                "class_type":
                    "EmptyHunyuanLatentVideo",

                "_meta": {
                    "title":
                        "AJVYRA 10 Second Shot Latent"
                },
            },

            # ------------------------------------------------
            # Wan sampling
            # ------------------------------------------------

            "48": {
                "inputs": {

                    "shift":
                        shift,

                    "model": [
                        "37",
                        0
                    ],
                },

                "class_type":
                    "ModelSamplingSD3",

                "_meta": {
                    "title":
                        "AJVYRA Wan Sampling"
                },
            },

            # ------------------------------------------------
            # Video output
            #
            # ComfyUI creates WebM.
            # AJVYRA converts it to MP4 after completion.
            # ------------------------------------------------

            "47": {
                "inputs": {

                    "images": [
                        "8",
                        0
                    ],

                    "filename_prefix":
                        filename_prefix,

                    "codec":
                        "vp9",

                    "fps":
                        fps,

                    "crf":
                        24,
                },

                "class_type":
                    "SaveWEBM",

                "_meta": {
                    "title":
                        "AJVYRA Wan Video Output"
                },
            },
        }


# ============================================================
# AJVYRA WAN ENGINE
# ============================================================

class AJVYRAWanEngine:

    def __init__(
        self,
        config=AJVYRAWanConfig,
    ):
        self.config = config

        self.http = ComfyHTTP(
            config.COMFY_URL
        )

        self.config.OUTPUT_ROOT.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    def health(self) -> Dict[str, Any]:

        try:

            system = self.http.get(
                "/system_stats"
            )

            return {
                "online": True,
                "comfyui": self.config.COMFY_URL,
                "system": system,
            }

        except Exception as exc:

            return {
                "online": False,
                "error": str(exc),
                "comfyui": self.config.COMFY_URL,
            }

    # --------------------------------------------------------
    # Queue
    # --------------------------------------------------------

    def queue(
        self,
        prompt: str,
        negative_prompt: str = "",
        seed: Optional[int] = None,
        shot_id: str = "shot_001",
    ) -> str:

        if seed is None:
            seed = random.randint(
                1,
                999999999999999
            )

        if not negative_prompt:
            negative_prompt = (
                "low quality, blurry, distorted face, "
                "bad anatomy, extra fingers, extra limbs, "
                "deformed body, duplicate character, "
                "flickering, static frame, text, watermark, "
                "logo, subtitles, oversaturated, "
                "jpeg artifacts"
            )

        prefix = (
            "AJVYRA/"
            + self._safe_name(shot_id)
        )

        graph = Wan21Graph.create(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            width=self.config.WIDTH,
            height=self.config.HEIGHT,
            frames=self.config.FRAMES,
            steps=self.config.STEPS,
            cfg=self.config.CFG,
            shift=self.config.SHIFT,
            fps=self.config.FPS,
            filename_prefix=prefix,
        )

        client_id = str(
            uuid.uuid4()
        )

        payload = {
            "prompt": graph,
            "client_id": client_id,
        }

        result = self.http.post(
            "/prompt",
            payload
        )

        if not isinstance(result, dict):
            raise RuntimeError(
                "ComfyUI returned an invalid response."
            )

        if result.get("error"):
            raise RuntimeError(
                "ComfyUI rejected workflow: "
                + json.dumps(
                    result,
                    ensure_ascii=False
                )
            )

        prompt_id = result.get(
            "prompt_id"
        )

        if not prompt_id:
            raise RuntimeError(
                "ComfyUI did not return prompt_id."
            )

        return prompt_id

    # --------------------------------------------------------
    # Wait
    # --------------------------------------------------------

    def wait(
        self,
        prompt_id: str,
    ) -> Dict[str, Any]:

        started = time.time()

        while True:

            if (
                time.time() - started
                > self.config.TIMEOUT
            ):
                raise TimeoutError(
                    "Wan generation timed out."
                )

            history = self.http.get(
                "/history/"
                + prompt_id
            )

            if (
                isinstance(history, dict)
                and prompt_id in history
            ):

                item = history[
                    prompt_id
                ]

                status = item.get(
                    "status",
                    {}
                )

                if status.get(
                    "status_str"
                ) == "error":

                    raise RuntimeError(
                        "ComfyUI/Wan generation failed:\n"
                        + json.dumps(
                            item,
                            ensure_ascii=False,
                            indent=2
                        )
                    )

                if item.get(
                    "outputs"
                ):

                    return item

            time.sleep(
                self.config.POLL_SECONDS
            )

    # --------------------------------------------------------
    # Find output
    # --------------------------------------------------------

    def find_video(
        self,
        history: Dict[str, Any]
    ) -> Dict[str, Any]:

        outputs = history.get(
            "outputs",
            {}
        )

        candidates = []

        for node_id, node_output in (
            outputs.items()
        ):

            for key in (
                "videos",
                "gifs",
                "images",
            ):

                values = node_output.get(
                    key,
                    []
                )

                if not isinstance(
                    values,
                    list
                ):
                    continue

                for item in values:

                    if not isinstance(
                        item,
                        dict
                    ):
                        continue

                    filename = item.get(
                        "filename"
                    )

                    if not filename:
                        continue

                    candidates.append({
                        "node_id": node_id,
                        "filename": filename,
                        "subfolder":
                            item.get(
                                "subfolder",
                                ""
                            ),
                        "type":
                            item.get(
                                "type",
                                "output"
                            ),
                    })

        if not candidates:
            raise RuntimeError(
                "ComfyUI finished, but no video output was found."
            )

        # Prefer actual video extensions.
        video_candidates = [
            x for x in candidates
            if Path(
                x["filename"]
            ).suffix.lower()
            in {
                ".webm",
                ".mp4",
                ".mov",
                ".mkv",
                ".avi",
            }
        ]

        if video_candidates:
            return video_candidates[0]

        raise RuntimeError(
            "Wan completed but did not return "
            "a video file."
        )

    # --------------------------------------------------------
    # Download
    # --------------------------------------------------------

    def download(
        self,
        output_info: Dict[str, Any],
        destination: Path,
    ) -> Path:

        filename = output_info[
            "filename"
        ]

        subfolder = output_info.get(
            "subfolder",
            ""
        )

        file_type = output_info.get(
            "type",
            "output"
        )

        path = (
            "/view?"
            "filename="
            + self._url_quote(filename)
            + "&subfolder="
            + self._url_quote(subfolder)
            + "&type="
            + self._url_quote(file_type)
        )

        url = (
            self.config.COMFY_URL
            + path
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        request = Request(
            url,
            headers={
                "Accept":
                    "video/*,application/octet-stream"
            }
        )

        with urlopen(
            request,
            timeout=300
        ) as response:

            data = response.read()

        if len(data) < 1024:
            raise RuntimeError(
                "Downloaded Wan output is too small."
            )

        destination.write_bytes(
            data
        )

        return destination

    # --------------------------------------------------------
    # Convert to MP4
    # --------------------------------------------------------

    def convert_to_mp4(
        self,
        source: Path,
        destination: Path,
    ) -> Path:

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(source),

            "-c:v",
            "libx264",

            "-preset",
            "medium",

            "-crf",
            "18",

            "-pix_fmt",
            "yuv420p",

            "-movflags",
            "+faststart",

            str(destination),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                "FFmpeg MP4 conversion failed:\n"
                + result.stderr[-5000:]
            )

        if (
            not destination.exists()
            or destination.stat().st_size
            < 100_000
        ):

            raise RuntimeError(
                "Generated MP4 is invalid or too small."
            )

        return destination

    # --------------------------------------------------------
    # Complete shot
    # --------------------------------------------------------

    def generate_shot(
        self,
        shot_id: str,
        prompt: str,
        negative_prompt: str = "",
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:

        shot_dir = (
            self.config.OUTPUT_ROOT
            / self._safe_name(
                shot_id
            )
        )

        shot_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        webm = (
            shot_dir
            / "wan_output.webm"
        )

        mp4 = (
            shot_dir
            / "main.mp4"
        )

        metadata = (
            shot_dir
            / "production.json"
        )

        prompt_id = self.queue(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            shot_id=shot_id,
        )

        history = self.wait(
            prompt_id
        )

        output_info = self.find_video(
            history
        )

        self.download(
            output_info,
            webm
        )

        self.convert_to_mp4(
            webm,
            mp4
        )

        record = {
            "project": "AJVYRA",
            "engine": "Wan 2.1",
            "provider": "ComfyUI Local",
            "shot_id": shot_id,
            "prompt_id": prompt_id,
            "prompt": prompt,
            "negative_prompt":
                negative_prompt,
            "seed": seed,
            "width":
                self.config.WIDTH,
            "height":
                self.config.HEIGHT,
            "frames":
                self.config.FRAMES,
            "fps":
                self.config.FPS,
            "expected_seconds":
                round(
                    self.config.FRAMES
                    / self.config.FPS,
                    3
                ),
            "webm":
                str(webm),
            "mp4":
                str(mp4),
            "status":
                "READY",
            "created_at":
                time.time(),
        }

        metadata.write_text(
            json.dumps(
                record,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return record

    # --------------------------------------------------------
    # Utility
    # --------------------------------------------------------

    @staticmethod
    def _safe_name(
        value: str
    ) -> str:

        allowed = (
            "abcdefghijklmnopqrstuvwxyz"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "0123456789"
            "_-"
        )

        cleaned = "".join(
            c if c in allowed else "_"
            for c in value
        )

        return cleaned.strip(
            "_"
        ) or "shot"

    @staticmethod
    def _url_quote(
        value: str
    ) -> str:

        from urllib.parse import quote

        return quote(
            value,
            safe=""
        )


# ============================================================
# AJVYRA SHOT FACTORY
# ============================================================

class AJVYRAShotFactory:

    def __init__(
        self,
        engine: Optional[
            AJVYRAWanEngine
        ] = None,
    ):

        self.engine = (
            engine
            or AJVYRAWanEngine()
        )

    def create_shot(
        self,
        shot_number: int,
        character: str,
        location: str,
        action: str,
        emotion: str,
        camera: str,
        lighting: str,
    ) -> Dict[str, Any]:

        shot_id = (
            f"shot_{shot_number:04d}"
        )

        prompt = (
            "cinematic original anime film, "
            "high quality anime animation, "
            "consistent character design, "
            f"character: {character}, "
            f"location: {location}, "
            f"action: {action}, "
            f"emotion: {emotion}, "
            f"camera movement: {camera}, "
            f"lighting: {lighting}, "
            "detailed environment, "
            "natural movement, "
            "coherent anatomy, "
            "consistent face, "
            "consistent clothing, "
            "cinematic composition, "
            "smooth temporal motion, "
            "dramatic storytelling"
        )

        negative = (
            "low quality, blurry, "
            "bad anatomy, deformed face, "
            "extra fingers, extra arms, "
            "extra legs, duplicate person, "
            "flicker, frame interpolation artifacts, "
            "static image, frozen movement, "
            "camera jitter, watermark, logo, "
            "text, subtitles, distorted eyes"
        )

        return self.engine.generate_shot(
            shot_id=shot_id,
            prompt=prompt,
            negative_prompt=negative,
        )


# ============================================================
# TEST
# ============================================================

def test_connection():

    engine = AJVYRAWanEngine()

    result = engine.health()

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
            default=str
        )
    )


def generate_one_test_shot():

    factory = AJVYRAShotFactory()

    result = factory.create_shot(
        shot_number=1,

        character=(
            "Kael Veyron, a fictional young "
            "anime swordsman with black hair, "
            "dark coat and silver eyes"
        ),

        location=(
            "the abandoned upper district "
            "of the Broken City at night"
        ),

        action=(
            "Kael slowly walks through the rain "
            "while holding an old glowing memory crystal"
        ),

        emotion=(
            "quiet sadness mixed with determination"
        ),

        camera=(
            "slow cinematic tracking shot "
            "from behind, then subtle side profile"
        ),

        lighting=(
            "cold moonlight, soft blue reflections "
            "on wet streets, distant warm windows"
        ),
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2
        )
    )


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA real Wan 2.1 "
            "ComfyUI local production engine"
        )
    )

    parser.add_argument(
        "command",
        choices=[
            "test",
            "shot",
        ],
        help=(
            "test = check ComfyUI, "
            "shot = generate a real test shot"
        )
    )

    args = parser.parse_args()

    if args.command == "test":
        test_connection()

    elif args.command == "shot":
        generate_one_test_shot()
