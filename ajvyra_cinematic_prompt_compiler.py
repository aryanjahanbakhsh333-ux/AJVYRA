from __future__ import annotations

from typing import Any


class AJVYRACinematicPromptCompiler:
    """
    Converts structured cinematic state into provider-neutral
    generation prompts.

    The compiler does not call an AI provider.
    """

    def compile(
        self,
        *,
        scene_description: str,
        characters: list[dict[str, Any]],
        world: dict[str, Any],
        emotion: dict[str, Any],
        camera: dict[str, Any],
        lighting: dict[str, Any],
        sound: dict[str, Any],
        continuity_token: str = "",
    ) -> str:

        sections: list[str] = []

        sections.append(
            "CINEMATIC ANIMATION DIRECTION"
        )

        sections.append(
            f"SCENE:\n{scene_description.strip()}"
        )

        character_block = self._characters(
            characters
        )

        if character_block:
            sections.append(
                "CHARACTER CONTINUITY:\n"
                + character_block
            )

        sections.append(
            "WORLD:\n"
            + self._world(world)
        )

        sections.append(
            "EMOTIONAL PERFORMANCE:\n"
            + self._emotion(emotion)
        )

        sections.append(
            "CAMERA:\n"
            + self._camera(camera)
        )

        sections.append(
            "LIGHTING:\n"
            + self._lighting(lighting)
        )

        sections.append(
            "SOUND:\n"
            + self._sound(sound)
        )

        if continuity_token:
            sections.append(
                "CONTINUITY TOKEN:\n"
                + continuity_token
            )

        sections.append(
            "QUALITY REQUIREMENTS:\n"
            "Preserve character identity, clothing continuity, "
            "environment continuity, emotional continuity, "
            "cinematic composition, natural motion, coherent "
            "physics, stable anatomy, consistent visual style, "
            "and intentional camera movement."
        )

        return "\n\n".join(sections)

    def _characters(
        self,
        characters: list[dict[str, Any]],
    ) -> str:

        blocks: list[str] = []

        for character in characters:
            name = character.get(
                "name",
                "Unknown character",
            )

            appearance = character.get(
                "appearance",
                {},
            )

            clothing = character.get(
                "clothing",
                {},
            )

            personality = character.get(
                "personality",
                {},
            )

            blocks.append(
                f"- {name}\n"
                f"  appearance: {appearance}\n"
                f"  clothing: {clothing}\n"
                f"  personality: {personality}"
            )

        return "\n".join(blocks)

    def _world(
        self,
        world: dict[str, Any],
    ) -> str:

        return (
            f"location: {world.get('name', '')}\n"
            f"time: {world.get('time_of_day', '')}\n"
            f"weather: {world.get('weather', '')}\n"
            f"lighting: {world.get('lighting', '')}\n"
            f"environment: {world.get('environment', {})}"
        )

    def _emotion(
        self,
        emotion: dict[str, Any],
    ) -> str:

        return (
            f"primary: {emotion.get('primary', '')}\n"
            f"intensity: {emotion.get('intensity', 0)}\n"
            f"secondary: {emotion.get('secondary', '')}\n"
            f"direction: {emotion.get('direction', '')}\n"
            f"performance: "
            f"{emotion.get('performance', '')}"
        )

    def _camera(
        self,
        camera: dict[str, Any],
    ) -> str:

        return (
            f"shot: {camera.get('shot', 'medium')}\n"
            f"movement: {camera.get('movement', 'static')}\n"
            f"angle: {camera.get('angle', 'eye level')}\n"
            f"lens: {camera.get('lens', 'cinematic')}\n"
            f"focus: {camera.get('focus', 'subject')}"
        )

    def _lighting(
        self,
        lighting: dict[str, Any],
    ) -> str:

        return (
            f"key light: {lighting.get('key_light', '')}\n"
            f"atmosphere: {lighting.get('atmosphere', '')}\n"
            f"contrast: {lighting.get('contrast', '')}\n"
            f"color temperature: "
            f"{lighting.get('color_temperature', '')}"
        )

    def _sound(
        self,
        sound: dict[str, Any],
    ) -> str:

        return (
            f"dialogue: {sound.get('dialogue', '')}\n"
            f"ambience: {sound.get('ambience', '')}\n"
            f"sfx: {sound.get('sfx', '')}\n"
            f"music: {sound.get('music', '')}\n"
            f"silence: {sound.get('silence', '')}"
        )
