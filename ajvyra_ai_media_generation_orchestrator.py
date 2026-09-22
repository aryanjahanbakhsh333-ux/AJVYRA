"""
AJVYRA AI MEDIA GENERATION ORCHESTRATOR

The AI-facing layer.

It receives a creative project and automatically coordinates:

IMAGE
VOICE
VIDEO

The orchestrator deliberately does not require the owner to manually
provide every asset.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from ajvyra_ai_image_generation_engine import (
    AJVYRAAIImageGenerationEngine,
)

from ajvyra_ai_voice_generation_engine import (
    AJVYRAAIVoiceGenerationEngine,
    VoiceRequest,
)

from ajvyra_ai_video_generation_engine import (
    AJVYRAAIVideoGenerationEngine,
    VideoRequest,
)


class AJVYRAAIMediaGenerationOrchestrator:

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self.root = Path(root).resolve()

        self.images = (
            AJVYRAAIImageGenerationEngine(
                self.root
            )
        )

        self.voices = (
            AJVYRAAIVoiceGenerationEngine(
                self.root
            )
        )

        self.videos = (
            AJVYRAAIVideoGenerationEngine(
                self.root
            )
        )

    # =========================================================
    # COMPLETE ANIME
    # =========================================================

    def generate_anime_media(
        self,
        project: Dict[str, Any],
    ) -> Dict[str, Any]:

        project_id = str(
            project["project_id"]
        )

        title = project.get(
            "title",
            project_id,
        )

        story = project.get(
            "story",
            "",
        )

        genre = project.get(
            "genre",
            "Fantasy",
        )

        characters = project.get(
            "characters",
            [],
        )

        locations = project.get(
            "locations",
            [],
        )

        scenes = project.get(
            "scenes",
            [],
        )

        dialogue = project.get(
            "dialogue",
            [],
        )

        result = {
            "project_id": project_id,
            "title": title,
            "images": [],
            "voices": [],
            "videos": [],
        }

        # -----------------------------------------------------
        # POSTER
        # -----------------------------------------------------

        poster = self.images.generate_poster(
            project_id=project_id,
            title=title,
            story=story,
            characters=[
                self._character_name(c)
                for c in characters
            ],
            genre=genre,
        )

        result["images"].append(
            poster
        )

        # -----------------------------------------------------
        # CHARACTERS
        # -----------------------------------------------------

        for character in characters:

            name = self._character_name(
                character
            )

            description = (
                character.get(
                    "description",
                    "",
                )
                if isinstance(
                    character,
                    dict,
                )
                else str(character)
            )

            result["images"].append(
                self.images.generate_character(
                    project_id=project_id,
                    character_name=name,
                    description=description,
                )
            )

        # -----------------------------------------------------
        # LOCATIONS
        # -----------------------------------------------------

        for location in locations:

            if isinstance(
                location,
                dict,
            ):

                name = location.get(
                    "name",
                    "location",
                )

                description = location.get(
                    "description",
                    "",
                )

            else:

                name = str(location)
                description = ""

            result["images"].append(
                self.images.generate_location(
                    project_id=project_id,
                    location_name=name,
                    description=description,
                )
            )

        # -----------------------------------------------------
        # SCENES
        # -----------------------------------------------------

        frames_dir = (
            self.root
            / "generated"
            / "frames"
            / project_id
        )

        frames_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for index, scene in enumerate(
            scenes
        ):

            if isinstance(
                scene,
                dict,
            ):

                scene_id = str(
                    scene.get(
                        "id",
                        index + 1,
                    )
                )

                description = scene.get(
                    "description",
                    "",
                )

                scene_characters = [
                    self._character_name(c)
                    for c in scene.get(
                        "characters",
                        [],
                    )
                ]

                location = scene.get(
                    "location",
                    "",
                )

                emotion = scene.get(
                    "emotion",
                    "",
                )

            else:

                scene_id = str(
                    index + 1
                )

                description = str(
                    scene
                )

                scene_characters = []

                location = ""
                emotion = ""

            generated = (
                self.images.generate_scene(
                    project_id=project_id,
                    scene_id=scene_id,
                    scene_description=description,
                    characters=scene_characters,
                    location=location,
                    emotion=emotion,
                )
            )

            source = Path(
                generated["path"]
            )

            frame = (
                frames_dir
                / f"frame_{index + 1:06d}.png"
            )

            if source.exists():
                frame.write_bytes(
                    source.read_bytes()
                )

            result["images"].append(
                generated
            )

        # -----------------------------------------------------
        # VOICES
        # -----------------------------------------------------

        audio_files = []

        for index, line in enumerate(
            dialogue
        ):

            if not isinstance(
                line,
                dict,
            ):
                continue

            text = str(
                line.get(
                    "text",
                    "",
                )
            )

            if not text:
                continue

            language = line.get(
                "language",
                "fa",
            )

            speaker = line.get(
                "speaker",
                "narrator",
            )

            emotion = line.get(
                "emotion",
                "neutral",
            )

            voice = (
                self.voices.generate(
                    VoiceRequest(
                        project_id=project_id,
                        speaker_id=speaker,
                        text=text,
                        language=language,
                        emotion=emotion,
                        output_name=(
                            f"dialogue_"
                            f"{index + 1:05d}.wav"
                        ),
                    )
                )
            )

            result["voices"].append(
                voice
            )

            audio_files.append(
                voice["path"]
            )

        # -----------------------------------------------------
        # VIDEO
        # -----------------------------------------------------

        if list(
            frames_dir.glob(
                "frame_*.png"
            )
        ):

            video = self.videos.render(
                VideoRequest(
                    project_id=project_id,
                    output_name="episode.mp4",
                    duration_seconds=int(
                        project.get(
                            "duration_seconds",
                            1800,
                        )
                    ),
                    frames_dir=str(
                        frames_dir
                    ),
                    audio_files=audio_files,
                )
            )

            result["videos"].append(
                video
            )

        # -----------------------------------------------------
        # MANIFEST
        # -----------------------------------------------------

        manifest_dir = (
            self.root
            / "generated"
            / "media_manifests"
        )

        manifest_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        manifest = (
            manifest_dir
            / f"{project_id}.json"
        )

        manifest.write_text(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return result

    # =========================================================
    # CHARACTER NAME
    # =========================================================

    @staticmethod
    def _character_name(
        character: Any,
    ) -> str:

        if isinstance(
            character,
            dict,
        ):
            return str(
                character.get(
                    "name",
                    "unknown",
                )
            )

        return str(
            character
        )
