from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class AnimePrompt:
    original: str
    final_prompt: str
    negative_prompt: str


class AJVYRAAnimePromptEngine:
    """
    Converts a user's normal prompt into a controlled anime/animation prompt.

    The engine does not generate media.
    It prepares a clean prompt for the video model.
    """

    STYLE_PREFIX = (
        "high quality cinematic anime animation, "
        "original anime film aesthetic, "
        "2D/3D hybrid anime rendering, "
        "expressive character animation, "
        "detailed environment, "
        "cinematic composition, "
        "dramatic lighting, "
        "smooth motion, "
        "professional animation"
    )

    STYLE_SUFFIX = (
        "anime only, animated characters, "
        "coherent visual style, "
        "consistent character proportions"
    )

    NEGATIVE = (
        "photorealistic, live action, real person, documentary, "
        "realistic human skin, photograph, selfie, "
        "deformed face, malformed hands, extra fingers, "
        "extra limbs, duplicate character, distorted body, "
        "flickering, severe artifacts, unreadable text, watermark, logo"
    )

    MAX_PROMPT_LENGTH = 1200

    def normalize(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise ValueError("Prompt must be text.")

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Please enter a video description.")

        prompt = re.sub(r"\s+", " ", prompt)

        if len(prompt) > self.MAX_PROMPT_LENGTH:
            prompt = prompt[: self.MAX_PROMPT_LENGTH].rstrip()

        return prompt

    def build(self, prompt: str) -> AnimePrompt:
        clean = self.normalize(prompt)

        final_prompt = (
            f"{self.STYLE_PREFIX}. "
            f"Scene description: {clean}. "
            f"{self.STYLE_SUFFIX}."
        )

        return AnimePrompt(
            original=clean,
            final_prompt=final_prompt,
            negative_prompt=self.NEGATIVE,
        )


_ENGINE = AJVYRAAnimePromptEngine()


def prepare_anime_prompt(prompt: str) -> dict:
    result = _ENGINE.build(prompt)

    return {
        "original": result.original,
        "prompt": result.final_prompt,
        "negative_prompt": result.negative_prompt,
        "style": "anime-animation",
    }
