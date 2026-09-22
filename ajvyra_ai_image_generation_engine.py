"""
AJVYRA AI IMAGE GENERATION ENGINE
=================================

Story-aware image generation layer.

Responsibilities:
- character images
- locations
- scene frames
- anime posters
- backgrounds
- visual continuity
- deterministic seeds
- optional external/local image-model adapters

The engine does not pretend that a procedural image is a neural
generation. Adapters can later connect a real image model without
changing the rest of AJVYRA.
"""

from __future__ import annotations

import hashlib
import json
import random
import subprocess
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class ImageRequest:
    project_id: str
    prompt: str
    negative_prompt: str = ""
    width: int = 1280
    height: int = 720
    seed: Optional[int] = None
    style: str = "anime cinematic"
    output_name: str = "image.png"


class AJVYRAAIImageGenerationEngine:

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self.root = Path(root).resolve()

        self.output_root = (
            self.root
            / "generated"
            / "images"
        )

        self.output_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def generate(
        self,
        request: ImageRequest,
    ) -> Dict[str, Any]:

        seed = (
            request.seed
            if request.seed is not None
            else self._seed_from_request(request)
        )

        output_dir = (
            self.output_root
            / request.project_id
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            output_dir
            / request.output_name
        )

        metadata = {
            "request": asdict(request),
            "seed": seed,
            "output": str(output_path),
            "generator": "AJVYRA-AI-IMAGE-ENGINE",
        }

        # -----------------------------------------------------
        # 1. REAL IMAGE MODEL ADAPTER
        # -----------------------------------------------------

        generated = self._try_external_model(
            request,
            output_path,
        )

        if generated:
            metadata["backend"] = "external-model"

        else:

            # -------------------------------------------------
            # 2. EXISTING AJVYRA VISUAL ENGINE
            # -------------------------------------------------

            generated = self._try_native_visual_engine(
                request,
                output_path,
                seed,
            )

            if generated:
                metadata["backend"] = "ajvyra-native-visual"

            else:

                # -------------------------------------------------
                # 3. SAFE FALLBACK
                # -------------------------------------------------

                self._create_placeholder(
                    output_path,
                    request,
                    seed,
                )

                metadata["backend"] = (
                    "fallback-placeholder"
                )

        metadata_path = (
            output_path.with_suffix(
                ".json"
            )
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return {
            "status": "generated",
            "path": str(output_path),
            "metadata": str(metadata_path),
            "backend": metadata["backend"],
            "seed": seed,
        }

    # =========================================================
    # CHARACTER
    # =========================================================

    def generate_character(
        self,
        project_id: str,
        character_name: str,
        description: str,
        style: str = "cinematic anime",
    ) -> Dict[str, Any]:

        prompt = (
            f"Original anime character named {character_name}. "
            f"{description}. "
            f"Style: {style}. "
            "Consistent facial identity, consistent hairstyle, "
            "consistent clothing, cinematic lighting."
        )

        request = ImageRequest(
            project_id=project_id,
            prompt=prompt,
            style=style,
            output_name=(
                f"{self._safe_name(character_name)}.png"
            ),
        )

        return self.generate(request)

    # =========================================================
    # LOCATION
    # =========================================================

    def generate_location(
        self,
        project_id: str,
        location_name: str,
        description: str,
    ) -> Dict[str, Any]:

        request = ImageRequest(
            project_id=project_id,
            prompt=(
                f"Original fictional anime location "
                f"named {location_name}. "
                f"{description}. "
                "Cinematic environment concept art."
            ),
            output_name=(
                f"location_{self._safe_name(location_name)}.png"
            ),
        )

        return self.generate(request)

    # =========================================================
    # SCENE
    # =========================================================

    def generate_scene(
        self,
        project_id: str,
        scene_id: str,
        scene_description: str,
        characters: list[str] | None = None,
        location: str = "",
        emotion: str = "",
    ) -> Dict[str, Any]:

        character_text = ", ".join(
            characters or []
        )

        prompt = (
            "Original cinematic anime scene. "
            f"Scene: {scene_description}. "
            f"Characters: {character_text}. "
            f"Location: {location}. "
            f"Emotion: {emotion}. "
            "Maintain character identity and visual continuity."
        )

        request = ImageRequest(
            project_id=project_id,
            prompt=prompt,
            output_name=(
                f"scene_{self._safe_name(scene_id)}.png"
            ),
        )

        return self.generate(request)

    # =========================================================
    # POSTER
    # =========================================================

    def generate_poster(
        self,
        project_id: str,
        title: str,
        story: str,
        characters: list[str],
        genre: str,
    ) -> Dict[str, Any]:

        prompt = (
            "Create an original cinematic anime poster. "
            f"Title: {title}. "
            f"Genre: {genre}. "
            f"Story: {story}. "
            f"Main characters: {', '.join(characters)}. "
            "The poster must visually represent the actual story, "
            "not a generic anime poster. "
            "Strong composition, cinematic lighting, "
            "professional anime key visual."
        )

        request = ImageRequest(
            project_id=project_id,
            prompt=prompt,
            width=1280,
            height=720,
            style="anime cinematic key visual",
            output_name="poster.png",
        )

        return self.generate(request)

    # =========================================================
    # EXTERNAL MODEL
    # =========================================================

    def _try_external_model(
        self,
        request: ImageRequest,
        output_path: Path,
    ) -> bool:

        endpoint = (
            __import__("os").environ.get(
                "AJVYRA_IMAGE_MODEL_URL",
                "",
            )
        )

        if not endpoint:
            return False

        payload = json.dumps(
            asdict(request)
        ).encode("utf-8")

        try:

            req = urllib.request.Request(
                endpoint,
                data=payload,
                headers={
                    "Content-Type":
                        "application/json"
                },
                method="POST",
            )

            with urllib.request.urlopen(
                req,
                timeout=300,
            ) as response:

                data = response.read()

            output_path.write_bytes(
                data
            )

            return output_path.exists()

        except Exception:
            return False

    # =========================================================
    # NATIVE ENGINE
    # =========================================================

    def _try_native_visual_engine(
        self,
        request: ImageRequest,
        output_path: Path,
        seed: int,
    ) -> bool:

        try:

            from ajvyra_native_visual_engine import (
                NativeVisualEngine,
            )

            engine = NativeVisualEngine(
                root=self.root
            )

            method = getattr(
                engine,
                "generate_image",
                None,
            )

            if callable(method):

                result = method(
                    prompt=request.prompt,
                    output_path=output_path,
                    width=request.width,
                    height=request.height,
                    seed=seed,
                )

                return bool(
                    result
                    and output_path.exists()
                )

        except Exception:
            pass

        return False

    # =========================================================
    # FALLBACK
    # =========================================================

    def _create_placeholder(
        self,
        output_path: Path,
        request: ImageRequest,
        seed: int,
    ) -> None:

        try:

            from PIL import Image, ImageDraw

            random.seed(seed)

            image = Image.new(
                "RGB",
                (
                    request.width,
                    request.height,
                ),
                (
                    20,
                    22,
                    30,
                ),
            )

            draw = ImageDraw.Draw(
                image
            )

            draw.rectangle(
                (
                    20,
                    20,
                    request.width - 20,
                    request.height - 20,
                ),
                outline=(100, 100, 120),
                width=4,
            )

            draw.text(
                (
                    50,
                    50,
                ),
                "AJVYRA AI",
            )

            draw.text(
                (
                    50,
                    90,
                ),
                request.prompt[:180],
            )

            image.save(
                output_path
            )

        except Exception:

            output_path.write_bytes(
                b"AJVYRA_IMAGE_PLACEHOLDER"
            )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _seed_from_request(
        request: ImageRequest,
    ) -> int:

        value = (
            request.project_id
            + request.prompt
            + request.style
        )

        digest = hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

        return int(
            digest[:12],
            16,
        )

    @staticmethod
    def _safe_name(
        value: str,
    ) -> str:

        chars = []

        for char in value.lower():

            if char.isalnum():
                chars.append(char)
            elif char in {" ", "-", "_"}:
                chars.append("_")

        return "".join(chars).strip("_")
