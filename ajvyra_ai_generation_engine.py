from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path("ajvyra_projects")
GENERATION_ROOT = ROOT / "generated"
QUEUE_FILE = ROOT / "generation_queue.json"

GENERATION_ROOT.mkdir(parents=True, exist_ok=True)


@dataclass
class GenerationStep:
    step_id: str
    name: str
    description: str
    status: str = "pending"
    output: Optional[str] = None


@dataclass
class GenerationProject:
    project_id: str
    item_id: int
    item_type: str
    title: str
    genre: str
    description: str

    language_audio: List[str] = field(
        default_factory=lambda: ["fa", "ja"]
    )

    subtitle_languages: List[str] = field(
        default_factory=lambda: ["en", "fa", "ja"]
    )

    steps: List[GenerationStep] = field(
        default_factory=list
    )

    created_at: str = ""
    status: str = "created"


class AJVYRAAIGenerationEngine:
    """
    Central generation planner for AJVYRA.

    Anime:
        story
        characters
        locations
        scenes
        dialogue
        digital voices
        subtitles
        visual assets
        video assembly

    Games:
        world
        mechanics
        characters
        levels
        gameplay code
        assets
        audio
        build
    """

    def __init__(self) -> None:
        self.projects: Dict[str, GenerationProject] = {}
        self._load_queue()

    # ---------------------------------------------------------
    # Storage
    # ---------------------------------------------------------

    def _load_queue(self) -> None:
        if not QUEUE_FILE.exists():
            return

        try:
            data = json.loads(
                QUEUE_FILE.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError):
            return

        for raw in data:
            try:
                steps = [
                    GenerationStep(**step)
                    for step in raw.get("steps", [])
                ]

                raw["steps"] = steps

                project = GenerationProject(**raw)

                self.projects[project.project_id] = project

            except (TypeError, ValueError):
                continue

    def _save_queue(self) -> None:
        payload = [
            asdict(project)
            for project in self.projects.values()
        ]

        QUEUE_FILE.write_text(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # Step templates
    # ---------------------------------------------------------

    @staticmethod
    def _anime_steps() -> List[GenerationStep]:
        names = [
            (
                "story",
                "Story Generation",
                "Create the complete original anime story and events."
            ),
            (
                "characters",
                "Character Generation",
                "Create original characters, identities, personalities and relationships."
            ),
            (
                "locations",
                "Location Generation",
                "Create original locations, environments and visual settings."
            ),
            (
                "scenes",
                "Scene Generation",
                "Break the story into cinematic scenes and shots."
            ),
            (
                "dialogue",
                "Dialogue Generation",
                "Generate natural dialogue for every speaking character."
            ),
            (
                "voices",
                "Digital Voice Generation",
                "Assign separate digital voices to the anime cast."
            ),
            (
                "subtitles",
                "Subtitle Generation",
                "Create English, Persian and Japanese subtitle tracks."
            ),
            (
                "visuals",
                "Visual Generation",
                "Create characters, environments and scene visual assets."
            ),
            (
                "animation",
                "Animation Assembly",
                "Transform generated visual material into animated scenes."
            ),
            (
                "video",
                "Video Assembly",
                "Combine scenes, voices, music and subtitles into the episode."
            ),
            (
                "quality",
                "Quality Control",
                "Check timing, dialogue, audio, subtitles and missing assets."
            ),
            (
                "publish",
                "Website Publishing",
                "Prepare the finished anime for the AJVYRA website."
            ),
        ]

        return [
            GenerationStep(
                step_id=key,
                name=name,
                description=description,
            )
            for key, name, description in names
        ]

    @staticmethod
    def _game_steps() -> List[GenerationStep]:
        names = [
            (
                "concept",
                "Game Concept",
                "Define the original game concept and player experience."
            ),
            (
                "world",
                "World Generation",
                "Create the game world, rules and environment."
            ),
            (
                "characters",
                "Character Generation",
                "Create original playable and non-playable characters."
            ),
            (
                "mechanics",
                "Gameplay Mechanics",
                "Define controls, abilities, combat, exploration and interactions."
            ),
            (
                "levels",
                "Level Generation",
                "Generate levels, missions, objectives and progression."
            ),
            (
                "code",
                "Gameplay Code",
                "Generate the gameplay systems and supporting code."
            ),
            (
                "visuals",
                "Game Assets",
                "Create the required visual assets and interfaces."
            ),
            (
                "audio",
                "Game Audio",
                "Generate or connect music, effects and digital voices."
            ),
            (
                "testing",
                "Automated Testing",
                "Check game logic, missing assets and broken systems."
            ),
            (
                "build",
                "Game Build",
                "Prepare the playable game build."
            ),
            (
                "quality",
                "Quality Control",
                "Run final consistency and asset checks."
            ),
            (
                "publish",
                "Website Publishing",
                "Prepare the game for the AJVYRA website."
            ),
        ]

        return [
            GenerationStep(
                step_id=key,
                name=name,
                description=description,
            )
            for key, name, description in names
        ]

    # ---------------------------------------------------------
    # Project creation
    # ---------------------------------------------------------

    def create_project(
        self,
        item_id: int,
        item_type: str,
        title: str,
        genre: str = "",
        description: str = "",
    ) -> GenerationProject:

        item_type = item_type.lower().strip()

        if item_type not in {"anime", "game"}:
            raise ValueError(
                "item_type must be 'anime' or 'game'"
            )

        project_id = (
            f"{item_type}_{item_id:02d}_"
            f"{uuid.uuid4().hex[:8]}"
        )

        steps = (
            self._anime_steps()
            if item_type == "anime"
            else self._game_steps()
        )

        project = GenerationProject(
            project_id=project_id,
            item_id=item_id,
            item_type=item_type,
            title=title,
            genre=genre,
            description=description,
            steps=steps,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        self.projects[project_id] = project

        self._create_project_directories(project)
        self._save_queue()

        return project

    # ---------------------------------------------------------
    # Project directories
    # ---------------------------------------------------------

    @staticmethod
    def _create_project_directories(
        project: GenerationProject,
    ) -> Path:

        project_root = (
            GENERATION_ROOT /
            project.item_type /
            project.project_id
        )

        directories = [
            "story",
            "characters",
            "locations",
            "scenes",
            "dialogue",
            "voices",
            "subtitles",
            "visuals",
            "audio",
            "build",
            "exports",
            "reports",
        ]

        if project.item_type == "game":
            directories += [
                "levels",
                "mechanics",
                "code",
                "assets",
                "tests",
            ]

        for directory in directories:
            (project_root / directory).mkdir(
                parents=True,
                exist_ok=True,
            )

        return project_root

    # ---------------------------------------------------------
    # Generation instructions
    # ---------------------------------------------------------

    def build_generation_instruction(
        self,
        project: GenerationProject,
    ) -> Dict[str, Any]:

        if project.item_type == "anime":
            objective = {
                "type": "anime",
                "episode_length_minutes": 30,
                "audio_languages": ["fa", "ja"],
                "subtitle_languages": ["en", "fa", "ja"],
                "subtitle_toggle": True,
                "original_characters": True,
                "original_story": True,
                "digital_voice_cast": True,
                "cinematic_scenes": True,
            }

        else:
            objective = {
                "type": "game",
                "original_gameplay": True,
                "original_characters": True,
                "original_world": True,
                "playable": True,
                "automated_testing": True,
            }

        return {
            "project_id": project.project_id,
            "item_id": project.item_id,
            "title": project.title,
            "genre": project.genre,
            "description": project.description,
            "objective": objective,
            "pipeline": [
                {
                    "id": step.step_id,
                    "name": step.name,
                    "description": step.description,
                    "status": step.status,
                }
                for step in project.steps
            ],
        }

    # ---------------------------------------------------------
    # Step execution
    # ---------------------------------------------------------

    def start_next_step(
        self,
        project_id: str,
    ) -> GenerationStep:

        project = self.projects.get(project_id)

        if project is None:
            raise KeyError(
                f"Unknown project: {project_id}"
            )

        for step in project.steps:
            if step.status == "pending":
                step.status = "running"

                project.status = "generating"

                self._save_queue()

                return step

        project.status = "completed"
        self._save_queue()

        raise RuntimeError(
            "All generation steps are already completed."
        )

    def complete_step(
        self,
        project_id: str,
        step_id: str,
        output: Optional[str] = None,
    ) -> GenerationStep:

        project = self.projects.get(project_id)

        if project is None:
            raise KeyError(
                f"Unknown project: {project_id}"
            )

        for step in project.steps:
            if step.step_id == step_id:
                step.status = "completed"
                step.output = output

                if all(
                    item.status == "completed"
                    for item in project.steps
                ):
                    project.status = "completed"

                self._save_queue()

                return step

        raise KeyError(
            f"Unknown generation step: {step_id}"
        )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def project_status(
        self,
        project_id: str,
    ) -> Dict[str, Any]:

        project = self.projects.get(project_id)

        if project is None:
            raise KeyError(
                f"Unknown project: {project_id}"
            )

        total = len(project.steps)

        completed = sum(
            step.status == "completed"
            for step in project.steps
        )

        running = sum(
            step.status == "running"
            for step in project.steps
        )

        progress = (
            round((completed / total) * 100, 2)
            if total
            else 0
        )

        return {
            "project_id": project.project_id,
            "title": project.title,
            "type": project.item_type,
            "status": project.status,
            "progress": progress,
            "completed_steps": completed,
            "running_steps": running,
            "total_steps": total,
            "next_step": next(
                (
                    step.step_id
                    for step in project.steps
                    if step.status == "pending"
                ),
                None,
            ),
        }

    # ---------------------------------------------------------
    # AI command interface
    # ---------------------------------------------------------

    def command(
        self,
        action: str,
        **kwargs: Any,
    ) -> Any:

        action = action.strip().lower()

        if action == "create":
            return self.create_project(
                item_id=kwargs["item_id"],
                item_type=kwargs["item_type"],
                title=kwargs["title"],
                genre=kwargs.get("genre", ""),
                description=kwargs.get(
                    "description",
                    "",
                ),
            )

        if action == "instruction":
            project = self.projects[
                kwargs["project_id"]
            ]

            return self.build_generation_instruction(
                project
            )

        if action == "start":
            return self.start_next_step(
                kwargs["project_id"]
            )

        if action == "complete":
            return self.complete_step(
                project_id=kwargs["project_id"],
                step_id=kwargs["step_id"],
                output=kwargs.get("output"),
            )

        if action == "status":
            return self.project_status(
                kwargs["project_id"]
            )

        if action == "list":
            return [
                asdict(project)
                for project in self.projects.values()
            ]

        raise ValueError(
            f"Unknown AI generation command: {action}"
        )


# -------------------------------------------------------------
# Global engine
# -------------------------------------------------------------

AI_GENERATION_ENGINE = AJVYRAAIGenerationEngine()


def create_anime(
    anime_id: int,
    title: str,
    genre: str,
    description: str = "",
) -> GenerationProject:

    return AI_GENERATION_ENGINE.create_project(
        item_id=anime_id,
        item_type="anime",
        title=title,
        genre=genre,
        description=description,
    )


def create_game(
    game_id: int,
    title: str,
    genre: str,
    description: str = "",
) -> GenerationProject:

    return AI_GENERATION_ENGINE.create_project(
        item_id=game_id,
        item_type="game",
        title=title,
        genre=genre,
        description=description,
    )


if __name__ == "__main__":
    print("AJVYRA AI GENERATION ENGINE")
    print("Engine ready.")
    print(f"Queue: {QUEUE_FILE}")
    print(f"Output: {GENERATION_ROOT}")
