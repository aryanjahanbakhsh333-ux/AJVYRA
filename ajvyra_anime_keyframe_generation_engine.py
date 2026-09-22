from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


class AJVYRAKeyframeProvider:
    def generate(
        self,
        prompt: str,
        output_path: Path,
        reference_images: Optional[List[str]] = None,
    ) -> Path:
        raise NotImplementedError


class AJVYRAKeyframeGeminiProvider(AJVYRAKeyframeProvider):
    """
    Uses Gemini image generation when the SDK/API is configured.
    """

    def __init__(
        self,
        model: str = "gemini-3.1-flash-image-preview",
    ):
        self.model = model

    def generate(
        self,
        prompt: str,
        output_path: Path,
        reference_images: Optional[List[str]] = None,
    ) -> Path:

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Install google-genai to use the real image provider."
            ) from exc

        if not (
            os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
        ):
            raise RuntimeError(
                "GEMINI_API_KEY or GOOGLE_API_KEY is required."
            )

        client = genai.Client()

        response = client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_modalities": ["IMAGE"],
            },
        )

        image_bytes = None

        for part in getattr(response, "parts", []):
            if getattr(part, "inline_data", None):
                image_bytes = part.inline_data.data
                break

        if image_bytes is None:
            raise RuntimeError(
                "Image provider returned no image."
            )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_bytes(image_bytes)

        return output_path


class AJVYRAKeyframeEngine:
    def __init__(
        self,
        root: str = "generated/anime_production",
        provider: Optional[AJVYRAKeyframeProvider] = None,
    ):
        self.root = Path(root)
        self.provider = provider

    def generate_episode_keyframes(
        self,
        anime_id: str,
        episode_id: str,
        shot_plan: Dict[str, Any],
    ) -> List[Path]:

        if self.provider is None:
            raise RuntimeError(
                "No keyframe provider configured."
            )

        output_dir = (
            self.root
            / anime_id
            / "season_01"
            / episode_id
            / "keyframes"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        generated = []

        previous_frame = None

        for shot in shot_plan.get("shots", []):
            shot_id = shot["shot_id"]

            prompt = self._build_keyframe_prompt(
                shot,
                previous_frame,
            )

            output = output_dir / f"{shot_id}.png"

            self.provider.generate(
                prompt=prompt,
                output_path=output,
                reference_images=shot.get(
                    "reference_images",
                    [],
                ),
            )

            shot["first_frame"] = str(output)

            generated.append(output)

            previous_frame = output

        return generated

    @staticmethod
    def _build_keyframe_prompt(
        shot: Dict[str, Any],
        previous_frame: Optional[Path],
    ) -> str:

        previous_context = ""

        if previous_frame:
            previous_context = (
                "Preserve visual continuity with the previous shot. "
                "Keep the same characters, clothing, proportions, "
                "lighting and environment."
            )

        return (
            "Create a production-quality cinematic anime keyframe. "
            "This is an original fictional production. "
            f"Characters: {', '.join(shot.get('characters', []))}. "
            f"Location: {shot.get('location', '')}. "
            f"Emotion: {shot.get('emotion', '')}. "
            f"Camera: {shot.get('camera', '')}. "
            f"Action: {shot.get('prompt', '')}. "
            f"{previous_context}"
        )
