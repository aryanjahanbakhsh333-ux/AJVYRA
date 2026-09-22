"""
AJVYRA CINEMATIC MASTER CONTROLLER
-----------------------------------
Top-level controller for cinematic anime production.

Pipeline:

Idea
 -> Story
 -> Characters
 -> World
 -> Emotion
 -> Direction
 -> Visual Specification
 -> Audio Timeline
 -> Media Generation
 -> Render
 -> QC
 -> Publish

The controller owns the project state.
Providers/backends remain replaceable.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from ajvyra_cinematic_ai_brain import (
    AJVYRACinematicAIBrain,
)

from ajvyra_cinematic_emotion_engine import (
    AJVYRAEmotionEngine,
)

from ajvyra_cinematic_film_engine import (
    AJVYRACinematicFilmEngine,
    CinematicFilm,
)

from ajvyra_cinematic_story_intelligence import (
    AJVYRACinematicStoryIntelligence,
    StoryRequest,
)

from ajvyra_cinematic_character_intelligence import (
    AJVYRACinematicCharacterIntelligence,
    AppearanceProfile,
    PersonalityProfile,
    CharacterArc,
)

from ajvyra_cinematic_director_engine import (
    AJVYRACinematicDirectorEngine,
)

from ajvyra_cinematic_visual_director import (
    AJVYRACinematicVisualDirector,
    VisualCharacterState,
    VisualEnvironment,
)

from ajvyra_cinematic_audio_timeline import (
    AJVYRACinematicAudioTimeline,
)

from ajvyra_cinematic_render_engine import (
    AJVYRACinematicRenderEngine,
)


@dataclass
class CinematicProjectStatus:
    film_id: str
    title: str
    status: str

    story_ready: bool = False
    characters_ready: bool = False
    world_ready: bool = False
    direction_ready: bool = False

    visual_ready: bool = False
    audio_ready: bool = False
    render_ready: bool = False

    published: bool = False

    created_at: float = field(
        default_factory=time.time
    )


class AJVYRACinematicMasterController:
    VERSION = "1.0.0"

    def __init__(
        self,
        film_id: str,
        title: str,
        genre: str,
        duration_seconds: int = 1800,
        root: str | Path = (
            "generated/cinematic"
        ),
    ) -> None:
        self.film_id = film_id
        self.title = title
        self.genre = genre
        self.duration_seconds = (
            max(60, int(duration_seconds))
        )

        self.root = Path(root)

        self.project_dir = (
            self.root / film_id
        )

        self.project_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.film = CinematicFilm(
            film_id=film_id,
            title=title,
            genre=genre,
            duration_seconds=(
                self.duration_seconds
            ),
        )

        self.film_engine = (
            AJVYRACinematicFilmEngine(
                self.film,
                project_root=self.root,
            )
        )

        self.brain = (
            self.film_engine.brain
        )

        self.story_engine = (
            AJVYRACinematicStoryIntelligence()
        )

        self.character_engine = (
            AJVYRACinematicCharacterIntelligence()
        )

        self.emotion_engine = (
            AJVYRAEmotionEngine()
        )

        self.director_engine = (
            AJVYRACinematicDirectorEngine(
                genre=genre
            )
        )

        self.visual_director = (
            AJVYRACinematicVisualDirector(
                film_id=film_id,
                genre=genre,
            )
        )

        self.audio_timeline = (
            AJVYRACinematicAudioTimeline(
                duration=(
                    self.duration_seconds
                )
            )
        )

        self.render_engine = (
            AJVYRACinematicRenderEngine(
                film_id=film_id,
                workspace=(
                    self.project_dir
                    / "render"
                ),
            )
        )

        self.status = (
            CinematicProjectStatus(
                film_id=film_id,
                title=title,
                status="created",
            )
        )

        self._save_status()

    # ---------------------------------------------------------
    # Project preparation
    # ---------------------------------------------------------

    def prepare_project(
        self,
        themes: Optional[
            List[str]
        ] = None,
        protagonist: str = "",
        antagonist: str = "",
        ending_type: str = "bittersweet",
    ) -> Dict:

        request = StoryRequest(
            title=self.title,
            genre=self.genre,
            duration_seconds=(
                self.duration_seconds
            ),
            themes=themes or [],
            protagonist=protagonist,
            antagonist=antagonist,
            ending_type=ending_type,
        )

        story = (
            self.story_engine.create_story(
                request
            )
        )

        errors = (
            self.story_engine.validate(
                story
            )
        )

        if errors:
            raise RuntimeError(
                "\n".join(errors)
            )

        self.story_engine.save(
            story,
            self.project_dir
            / "story_arc.json",
        )

        self.status.story_ready = True

        self.brain.set_flag(
            "story_locked",
            True,
        )

        self.status.status = (
            "story_prepared"
        )

        self._save_status()

        return asdict(story)

    # ---------------------------------------------------------
    # Character system
    # ---------------------------------------------------------

    def create_character(
        self,
        character_id: str,
        name: str,
        role: str,
        face: str,
        hair: str,
        eyes: str,
        clothing: str,
        personality: List[str],
        desires: List[str],
        fears: List[str],
    ) -> Dict:

        character = (
            self.character_engine.create(
                character_id=character_id,
                name=name,
                role=role,
                appearance=(
                    AppearanceProfile(
                        face=face,
                        hair=hair,
                        eyes=eyes,
                        default_clothing=clothing,
                        visual_style=(
                            "cinematic original anime"
                        ),
                    )
                ),
                personality=(
                    PersonalityProfile(
                        traits=personality,
                        desires=desires,
                        fears=fears,
                    )
                ),
                arc=CharacterArc(),
            )
        )

        self.brain.register_character(
            character_id=character_id,
            name=name,
            goal=(
                desires[0]
                if desires
                else ""
            ),
        )

        self.status.characters_ready = True

        self.brain.set_flag(
            "characters_locked",
            True,
        )

        self._save_status()

        return asdict(character)

    # ---------------------------------------------------------
    # World
    # ---------------------------------------------------------

    def create_location(
        self,
        location_id: str,
        name: str,
        description: str,
        visual_identity: Optional[
            Dict
        ] = None,
    ) -> None:

        self.brain.register_location(
            location_id,
            name,
            description,
            visual_identity,
        )

        self.status.world_ready = True

        self.brain.set_flag(
            "world_locked",
            True,
        )

        self._save_status()

    # ---------------------------------------------------------
    # Direction
    # ---------------------------------------------------------

    def direct_moment(
        self,
        moment_id: str,
        character_id: str,
        emotion: str,
        intensity: float,
        location: str,
        dialogue_present: bool = True,
    ) -> Dict:

        character = (
            self.character_engine.get(
                character_id
            )
        )

        if character is None:
            raise KeyError(
                character_id
            )

        vector = (
            self.emotion_engine.profile(
                emotion,
                intensity,
            )
        )

        direction = (
            self.emotion_engine.record(
                timestamp=(
                    self.brain.memory.current_time
                ),
                character_id=character_id,
                vector=vector,
            )
        )

        cinematic_direction = (
            self.director_engine.direct(
                moment_id=moment_id,
                emotion=emotion,
                intensity=intensity,
                character_name=(
                    character.name
                ),
                dialogue_present=(
                    dialogue_present
                ),
                location=location,
            )
        )

        visual_char = (
            VisualCharacterState(
                character_id=(
                    character.character_id
                ),
                identity_lock=(
                    character.continuity_hash
                ),
                name=character.name,
                appearance=(
                    f"{character.appearance.face}; "
                    f"{character.appearance.hair}; "
                    f"{character.appearance.eyes}"
                ),
                clothing=(
                    character.clothing_state
                ),
                emotion=(
                    direction.primary
                ),
                body_language=(
                    direction.body_language
                ),
                eye_direction=(
                    direction.eye_behavior
                ),
            )
        )

        environment = (
            self.brain.memory.world.locations
            .get(
                location,
                {},
            )
        )

        visual_environment = (
            VisualEnvironment(
                location=location,
                time_of_day=(
                    self.brain.memory.world.time_of_day
                ),
                weather=(
                    self.brain.memory.world.weather
                ),
                lighting=(
                    cinematic_direction
                    .lighting
                    .key_light
                ),
                atmosphere=(
                    cinematic_direction
                    .lighting
                    .atmosphere
                ),
                architecture=(
                    environment
                    .get(
                        "description",
                        "",
                    )
                ),
            )
        )

        visual = (
            self.visual_director.build(
                moment_id=moment_id,
                characters=[
                    visual_char
                ],
                environment=(
                    visual_environment
                ),
                camera=(
                    asdict(
                        cinematic_direction
                        .camera
                    )
                ),
                emotion=(
                    direction.primary
                ),
            )
        )

        self.brain.record_director_decision(
            "cinematic_moment",
            (
                f"{moment_id}: "
                f"{direction.primary}"
            ),
            reason=(
                "Generated from unified "
                "emotion and character state."
            ),
        )

        self.status.direction_ready = True

        self._save_status()

        return {
            "emotion": asdict(
                direction
            ),
            "direction": asdict(
                cinematic_direction
            ),
            "visual": asdict(
                visual
            ),
        }

    # ---------------------------------------------------------
    # Audio
    # ---------------------------------------------------------

    def add_dialogue(
        self,
        start: float,
        duration: float,
        path: str,
        language: str,
        character_id: str,
        emotion: str,
    ) -> None:

        self.audio_timeline.add_dialogue(
            start=start,
            duration=duration,
            audio_path=path,
            language=language,
            character_id=character_id,
            emotion=emotion,
        )

        self.status.audio_ready = True

        self.brain.set_flag(
            "audio_ready",
            True,
        )

        self._save_status()

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------

    def render(
        self,
        video_segments,
        audio_files,
        output: str | Path,
    ) -> Dict:

        report = self.render_engine.render(
            video_segments=video_segments,
            audio_files=audio_files,
            output=output,
        )

        if report.status == "completed":
            self.status.render_ready = True
            self.brain.set_flag(
                "render_ready",
                True,
            )

        self.status.status = (
            report.status
        )

        self._save_status()

        return asdict(report)

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def status_report(self) -> Dict:
        return {
            "version": self.VERSION,
            "status": asdict(
                self.status
            ),
            "film": self.film_engine.manifest(),
            "characters": {
                cid: asdict(character)
                for cid, character
                in self.character_engine.characters.items()
            },
            "audio": asdict(
                self.audio_timeline.timeline
            ),
        }

    def _save_status(self) -> None:
        path = (
            self.project_dir
            / "cinematic_project_status.json"
        )

        path.write_text(
            json.dumps(
                self.status_report(),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )


if __name__ == "__main__":
    controller = (
        AJVYRACinematicMasterController(
            film_id="veyllora_cinematic_01",
            title="Veylora",
            genre="dark_fantasy",
            duration_seconds=1800,
        )
    )

    controller.prepare_project(
        themes=[
            "memory",
            "loneliness",
            "love",
            "truth",
        ],
        protagonist="Veylora",
        antagonist="The Keeper of Forgotten Names",
        ending_type="bittersweet",
    )

    controller.create_character(
        character_id="vey_01",
        name="Veylora",
        role="protagonist",
        face=(
            "adult anime woman with a narrow "
            "expressive face"
        ),
        hair=(
            "long silver-black hair"
        ),
        eyes=(
            "violet reflective eyes"
        ),
        clothing=(
            "long black cinematic coat"
        ),
        personality=[
            "quiet",
            "observant",
            "kind",
        ],
        desires=[
            "discover the truth",
            "recover a lost memory",
        ],
        fears=[
            "losing someone again",
        ],
    )

    controller.create_location(
        location_id="harbor_01",
        name="Moonlit Harbor",
        description=(
            "An old coastal city with wet stone "
            "streets, dark ocean water and distant "
            "warm lights."
        ),
        visual_identity={
            "palette": [
                "blue_gray",
                "silver",
                "warm_amber",
            ],
            "weather": "light_rain",
        },
    )

    moment = controller.direct_moment(
        moment_id="veyllora_0001",
        character_id="vey_01",
        emotion="sadness",
        intensity=0.88,
        location="harbor_01",
        dialogue_present=True,
    )

    print(
        json.dumps(
            moment,
            ensure_ascii=False,
            indent=2,
        )
    )
