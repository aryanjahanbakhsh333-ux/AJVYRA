"""
AJVYRA AI FULL SYSTEM BRIDGE
=============================

FINAL INTEGRATION LAYER FOR AJVYRA

This file does NOT replace the existing engines.

It connects the engines that already exist:

AI Commander
    ↓
Training Directive
    ↓
Content Director
    ↓
Story / Character / Location / Scene systems
    ↓
Image / Visual Engine
    ↓
Voice / TTS Engine
    ↓
Animation Engine
    ↓
Video / FFmpeg Engine
    ↓
Subtitle Engine
    ↓
Poster Engine
    ↓
Site Catalog
    ↓
Completion Gate
    ↓
Autonomous Publisher

The bridge is deliberately defensive:
- missing optional modules do not immediately destroy the whole pipeline
- every stage is recorded
- failures are retried
- already-completed stages are skipped
- state is persistent
- the system can resume after interruption
"""

from __future__ import annotations

import hashlib
import importlib
import inspect
import json
import os
import shutil
import subprocess
import time
import traceback

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional


# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class BridgeConfig:

    anime_target: int = 30
    game_target: int = 70

    anime_duration_seconds: int = 1800

    max_retries: int = 3

    retry_delay_seconds: float = 2.0

    skip_completed: bool = True

    auto_publish: bool = True

    generate_posters: bool = True

    generate_subtitles: bool = True

    generate_audio: bool = True

    generate_video: bool = True

    generate_visuals: bool = True

    strict_completion: bool = True

    save_logs: bool = True


@dataclass
class StageResult:

    stage: str

    status: str

    started_at: float

    finished_at: float

    attempts: int = 1

    output: Dict[str, Any] = field(
        default_factory=dict
    )

    error: Optional[str] = None

    traceback_text: Optional[str] = None


@dataclass
class ProjectState:

    project_id: str

    project_type: str

    number: int

    title: str = ""

    status: str = "created"

    current_stage: str = ""

    completed_stages: List[str] = field(
        default_factory=list
    )

    failed_stages: List[str] = field(
        default_factory=list
    )

    stage_results: Dict[str, Any] = field(
        default_factory=dict
    )

    attempts: Dict[str, int] = field(
        default_factory=dict
    )

    updated_at: float = field(
        default_factory=time.time
    )


# ============================================================
# MAIN BRIDGE
# ============================================================

class AJVYRAAIFullSystemBridge:

    VERSION = "1.0.0"

    def __init__(
        self,
        root: Path | str,
        config: BridgeConfig | None = None,
    ) -> None:

        self.root = Path(
            root
        ).resolve()

        self.config = (
            config
            or BridgeConfig()
        )

        self.generated = (
            self.root
            / "generated"
        )

        self.runtime = (
            self.root
            / "runtime"
            / "full_system_bridge"
        )

        self.generated.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.runtime.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.state_dir = (
            self.runtime
            / "states"
        )

        self.logs_dir = (
            self.runtime
            / "logs"
        )

        self.state_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.logs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.components: Dict[
            str,
            Any
        ] = {}

        self.component_errors: Dict[
            str,
            str
        ] = {}

        self._load_existing_components()

    # ========================================================
    # COMPONENT LOADING
    # ========================================================

    def _load_existing_components(
        self,
    ) -> None:

        components = {

            "training_directive": (
                "ajvyra_ai_training_directive",
                "AJVYRAAITrainingDirective",
            ),

            "content_director": (
                "ajvyra_ai_content_director",
                "AJVYRAAIContentDirector",
            ),

            "media_engine": (
                "ajvyra_ai_media_engine",
                "AJVYRAAIMediaEngine",
            ),

            "poster_creator": (
                "ajvyra_ai_poster_creator",
                "AJVYRAPosterCreator",
            ),

            "universal_builder": (
                "ajvyra_ai_universal_builder",
                "AJVYRAUniversalBuilder",
            ),

            "completion_gate": (
                "ajvyra_ai_completion_gate",
                "AJVYRACompletionGate",
            ),

            "publisher": (
                "ajvyra_ai_autonomous_publisher",
                "AJVYRAAutonomousPublisher",
            ),

            "site_catalog": (
                "ajvyra_ai_site_catalog_runtime",
                "AJVYRAAISiteCatalogRuntime",
            ),

            "generation_engine": (
                "ajvyra_ai_generation_engine",
                "AJVYRAAIGenerationEngine",
            ),

            "native_visual": (
                "ajvyra_native_visual_engine",
                "NativeVisualEngine",
            ),

            "native_animation": (
                "ajvyra_native_animation_engine",
                "NativeAnimationEngine",
            ),

            "native_production": (
                "ajvyra_native_anime_production",
                "NativeAnimeProduction",
            ),

            "subtitle_engine": (
                "ajvyra_anime_subtitle_engine",
                None,
            ),

            "tts_engine": (
                "ajvyra_anime_tts_engine",
                None,
            ),
        }

        for key, definition in components.items():

            module_name, class_name = definition

            try:

                module = importlib.import_module(
                    module_name
                )

                if class_name is None:

                    self.components[key] = module

                    continue

                component_class = getattr(
                    module,
                    class_name,
                )

                instance = (
                    self._instantiate(
                        component_class
                    )
                )

                self.components[key] = instance

            except Exception as exc:

                self.component_errors[key] = (
                    f"{type(exc).__name__}: {exc}"
                )

    # ========================================================
    # SAFE INSTANTIATION
    # ========================================================

    def _instantiate(
        self,
        component_class: Any,
    ) -> Any:

        attempts = [

            lambda: component_class(
                root=self.root
            ),

            lambda: component_class(
                self.root
            ),

            lambda: component_class(),

        ]

        last_error = None

        for attempt in attempts:

            try:

                return attempt()

            except Exception as exc:

                last_error = exc

        if last_error:

            raise last_error

        raise RuntimeError(
            "Could not instantiate component."
        )

    # ========================================================
    # STATUS
    # ========================================================

    def status(
        self,
    ) -> Dict[str, Any]:

        anime_states = list(
            self.state_dir.glob(
                "anime_*.json"
            )
        )

        game_states = list(
            self.state_dir.glob(
                "game_*.json"
            )
        )

        completed_anime = 0
        completed_games = 0

        for path in anime_states:

            state = self._load_state_file(
                path
            )

            if (
                state
                and state.get("status")
                == "completed"
            ):
                completed_anime += 1

        for path in game_states:

            state = self._load_state_file(
                path
            )

            if (
                state
                and state.get("status")
                == "completed"
            ):
                completed_games += 1

        return {

            "bridge": (
                "AJVYRA-AI-FULL-SYSTEM-BRIDGE"
            ),

            "version": self.VERSION,

            "targets": {
                "anime": self.config.anime_target,
                "games": self.config.game_target,
            },

            "completed": {
                "anime": completed_anime,
                "games": completed_games,
            },

            "components": {
                key: {
                    "loaded": (
                        key in self.components
                    ),
                    "error": self.component_errors.get(
                        key
                    ),
                }
                for key in set(
                    list(self.components)
                    + list(self.component_errors)
                )
            },

            "ffmpeg": shutil.which(
                "ffmpeg"
            ) is not None,

            "ffprobe": shutil.which(
                "ffprobe"
            ) is not None,
        }

    # ========================================================
    # PREPARE
    # ========================================================

    def prepare(
        self,
    ) -> Dict[str, Any]:

        directive = self.components.get(
            "training_directive"
        )

        directive_result = None

        if directive:

            directive_result = (
                self._call_first(
                    directive,
                    [
                        "save",
                        "initialize",
                        "prepare",
                    ],
                )
            )

        status = self.status()

        result = {
            "status": "prepared",
            "directive": directive_result,
            "system": status,
        }

        self._write_json(
            self.runtime
            / "prepare_report.json",
            result,
        )

        return result

    # ========================================================
    # BUILD ALL ANIME
    # ========================================================

    def build_all_anime(
        self,
    ) -> Dict[str, Any]:

        results = []

        for number in range(
            1,
            self.config.anime_target + 1,
        ):

            result = (
                self.build_anime(
                    number
                )
            )

            results.append(
                result
            )

        summary = {
            "target": self.config.anime_target,
            "processed": len(results),
            "completed": sum(
                1
                for result in results
                if result.get(
                    "status"
                )
                == "completed"
            ),
            "failed": sum(
                1
                for result in results
                if result.get(
                    "status"
                )
                == "failed"
            ),
            "projects": results,
        }

        self._write_json(
            self.runtime
            / "anime_master_report.json",
            summary,
        )

        return summary

    # ========================================================
    # BUILD ONE ANIME
    # ========================================================

    def build_anime(
        self,
        number: int,
    ) -> Dict[str, Any]:

        if not (
            1
            <= number
            <= self.config.anime_target
        ):
            raise ValueError(
                f"Anime number must be 1-{self.config.anime_target}."
            )

        project_id = (
            f"anime_{number:02d}"
        )

        state = (
            self._load_project_state(
                project_id,
                "anime",
                number,
            )
        )

        if (
            self.config.skip_completed
            and state.status == "completed"
        ):

            return {
                "project_id": project_id,
                "status": "completed",
                "resumed": False,
                "skipped": True,
            }

        try:

            # ------------------------------------------------
            # 1. CREATIVE DIRECTOR
            # ------------------------------------------------

            spec = (
                self._run_stage(
                    state,
                    "creative_spec",
                    lambda: self._create_anime_spec(
                        number
                    ),
                )
            )

            # ------------------------------------------------
            # 2. STORY / CHARACTER / LOCATION / SCENE
            # ------------------------------------------------

            self._run_stage(
                state,
                "story_structure",
                lambda: self._ensure_story_structure(
                    spec
                ),
            )

            # ------------------------------------------------
            # 3. POSTER
            # ------------------------------------------------

            if self.config.generate_posters:

                self._run_stage(
                    state,
                    "poster",
                    lambda: self._generate_poster(
                        spec
                    ),
                )

            # ------------------------------------------------
            # 4. VISUALS
            # ------------------------------------------------

            if self.config.generate_visuals:

                self._run_stage(
                    state,
                    "visuals",
                    lambda: self._generate_visuals(
                        spec
                    ),
                )

            # ------------------------------------------------
            # 5. VOICE
            # ------------------------------------------------

            if self.config.generate_audio:

                self._run_stage(
                    state,
                    "voices",
                    lambda: self._generate_voices(
                        spec
                    ),
                )

            # ------------------------------------------------
            # 6. ANIMATION
            # ------------------------------------------------

            self._run_stage(
                state,
                "animation",
                lambda: self._generate_animation(
                    spec
                ),
            )

            # ------------------------------------------------
            # 7. SUBTITLES
            # ------------------------------------------------

            if self.config.generate_subtitles:

                self._run_stage(
                    state,
                    "subtitles",
                    lambda: self._generate_subtitles(
                        spec
                    ),
                )

            # ------------------------------------------------
            # 8. FINAL VIDEO
            # ------------------------------------------------

            if self.config.generate_video:

                self._run_stage(
                    state,
                    "video",
                    lambda: self._generate_video(
                        spec
                    ),
                )

            # ------------------------------------------------
            # 9. SITE
            # ------------------------------------------------

            self._run_stage(
                state,
                "site",
                lambda: self._sync_site(
                    spec
                ),
            )

            # ------------------------------------------------
            # 10. COMPLETION
            # ------------------------------------------------

            completion = (
                self._run_stage(
                    state,
                    "completion",
                    lambda: self._validate_project(
                        number
                    ),
                )
            )

            if (
                self.config.strict_completion
                and not self._completion_is_valid(
                    completion
                )
            ):

                state.status = "incomplete"

                self._save_state(
                    state
                )

                return {
                    "project_id": project_id,
                    "status": "incomplete",
                    "completion": completion,
                }

            state.status = "completed"
            state.current_stage = ""
            state.updated_at = time.time()

            self._save_state(
                state
            )

            return {
                "project_id": project_id,
                "status": "completed",
                "title": state.title,
                "stages": state.completed_stages,
            }

        except Exception as exc:

            state.status = "failed"
            state.updated_at = time.time()

            self._save_state(
                state
            )

            return {
                "project_id": project_id,
                "status": "failed",
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "completed_stages": (
                    state.completed_stages
                ),
            }

    # ========================================================
    # CREATIVE SPEC
    # ========================================================

    def _create_anime_spec(
        self,
        number: int,
    ) -> Dict[str, Any]:

        director = self.components.get(
            "content_director"
        )

        if director:

            method = getattr(
                director,
                "create_anime_spec",
                None,
            )

            if callable(method):

                spec = method(
                    number
                )

                return spec

        # Fallback to universal builder
        builder = self.components.get(
            "universal_builder"
        )

        if builder:

            director = getattr(
                builder,
                "director",
                None
            )

            if director:

                method = getattr(
                    director,
                    "create_anime_spec",
                    None,
                )

                if callable(method):

                    return method(
                        number
                    )

        raise RuntimeError(
            "No anime content director is available."
        )

    # ========================================================
    # STORY STRUCTURE
    # ========================================================

    def _ensure_story_structure(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        required = [
            "story",
            "characters",
            "locations",
            "scenes",
            "dialogue",
            "events",
        ]

        missing = [
            key
            for key in required
            if not spec.get(key)
        ]

        if missing:

            raise RuntimeError(
                "Creative specification is missing: "
                + ", ".join(missing)
            )

        return {
            "status": "valid",
            "required_fields": required,
        }

    # ========================================================
    # POSTER
    # ========================================================

    def _generate_poster(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        poster_creator = self.components.get(
            "poster_creator"
        )

        if poster_creator:

            method = getattr(
                poster_creator,
                "create",
                None,
            )

            if callable(method):

                return method(
                    spec
                )

        media = self.components.get(
            "media_engine"
        )

        if media:

            method = getattr(
                media,
                "generate_image",
                None,
            )

            if callable(method):

                result = method(
                    project_id=spec[
                        "project_id"
                    ],
                    prompt=self._poster_prompt(
                        spec
                    ),
                    output_name="poster.png",
                    width=1280,
                    height=720,
                )

                return result

        raise RuntimeError(
            "No poster/image generation component is available."
        )

    # ========================================================
    # VISUALS
    # ========================================================

    def _generate_visuals(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        media = self.components.get(
            "media_engine"
        )

        if media:

            method = getattr(
                media,
                "generate_anime",
                None,
            )

            if callable(method):

                result = method(
                    spec
                )

                return {
                    "status": "generated",
                    "result": result,
                }

        native_visual = self.components.get(
            "native_visual"
        )

        if native_visual:

            return self._generic_component_call(
                native_visual,
                [
                    "generate",
                    "generate_scene",
                    "render",
                ],
                spec,
            )

        return {
            "status": "skipped",
            "reason": "visual component unavailable",
        }

    # ========================================================
    # VOICES
    # ========================================================

    def _generate_voices(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        media = self.components.get(
            "media_engine"
        )

        if media:

            # generate_anime may already create voices.
            method = getattr(
                media,
                "generate_anime",
                None,
            )

            if callable(method):

                result = method(
                    spec
                )

                return {
                    "status": "generated",
                    "result": result,
                }

        tts = self.components.get(
            "tts_engine"
        )

        if tts:

            return self._generic_component_call(
                tts,
                [
                    "synthesize",
                    "generate",
                    "create_voice",
                ],
                spec,
            )

        return {
            "status": "skipped",
            "reason": "voice component unavailable",
        }

    # ========================================================
    # ANIMATION
    # ========================================================

    def _generate_animation(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        animation = self.components.get(
            "native_animation"
        )

        if animation:

            result = self._generic_component_call(
                animation,
                [
                    "animate",
                    "generate",
                    "render",
                    "create_animation",
                ],
                spec,
            )

            if result:

                return result

        production = self.components.get(
            "native_production"
        )

        if production:

            return self._generic_component_call(
                production,
                [
                    "produce",
                    "generate",
                    "render",
                    "create_episode",
                ],
                spec,
            )

        return {
            "status": "prepared",
            "reason": (
                "animation component has no compatible "
                "public method"
            ),
        }

    # ========================================================
    # SUBTITLES
    # ========================================================

    def _generate_subtitles(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        subtitle_engine = self.components.get(
            "subtitle_engine"
        )

        if not subtitle_engine:

            return {
                "status": "skipped",
                "reason": "subtitle engine unavailable",
            }

        # Try common public APIs without assuming
        # one exact implementation.

        for method_name in [
            "generate",
            "create_tracks",
            "build_tracks",
            "create_subtitles",
            "generate_subtitles",
        ]:

            method = getattr(
                subtitle_engine,
                method_name,
                None,
            )

            if not callable(method):
                continue

            attempts = [
                lambda: method(
                    spec
                ),
                lambda: method(
                    project_id=spec[
                        "project_id"
                    ],
                    dialogue=spec.get(
                        "dialogue",
                        [],
                    ),
                    languages=[
                        "en",
                        "fa",
                        "ja",
                    ],
                ),
            ]

            for attempt in attempts:

                try:

                    return {
                        "status": "generated",
                        "result": attempt(),
                    }

                except TypeError:
                    continue

        return {
            "status": "prepared",
            "reason": (
                "subtitle module loaded but "
                "no compatible method was found"
            ),
        }

    # ========================================================
    # VIDEO
    # ========================================================

    def _generate_video(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        media = self.components.get(
            "media_engine"
        )

        if media:

            method = getattr(
                media,
                "generate_anime",
                None,
            )

            if callable(method):

                result = method(
                    spec
                )

                return {
                    "status": "generated",
                    "result": result,
                }

        # ----------------------------------------------------
        # Existing native production
        # ----------------------------------------------------

        production = self.components.get(
            "native_production"
        )

        if production:

            result = self._generic_component_call(
                production,
                [
                    "produce",
                    "render",
                    "generate",
                    "create_episode",
                ],
                spec,
            )

            if result:

                return result

        # ----------------------------------------------------
        # Existing generation engine
        # ----------------------------------------------------

        generation = self.components.get(
            "generation_engine"
        )

        if generation:

            result = self._generic_component_call(
                generation,
                [
                    "generate_anime",
                    "generate",
                    "run",
                ],
                spec,
            )

            if result:

                return result

        raise RuntimeError(
            "No compatible video production component exists."
        )

    # ========================================================
    # SITE
    # ========================================================

    def _sync_site(
        self,
        spec: Dict[str, Any],
    ) -> Dict[str, Any]:

        catalog = self.components.get(
            "site_catalog"
        )

        if catalog:

            result = self._generic_component_call(
                catalog,
                [
                    "sync",
                    "build",
                    "generate",
                    "refresh",
                    "write",
                ],
                spec,
            )

            if result:

                return result

        # ----------------------------------------------------
        # Minimal local site metadata
        # ----------------------------------------------------

        site_dir = (
            self.generated
            / "site"
            / "anime"
            / spec[
                "project_id"
            ]
        )

        site_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        metadata = {
            "title": spec[
                "title"
            ],
            "project_id": spec[
                "project_id"
            ],
            "genre": spec[
                "genre"
            ],
            "duration_seconds": 1800,
            "audio": [
                "fa",
                "ja",
            ],
            "subtitles": [
                "en",
                "fa",
                "ja",
            ],
        }

        self._write_json(
            site_dir
            / "metadata.json",
            metadata,
        )

        return {
            "status": "site_metadata_created",
            "path": str(
                site_dir
            ),
        }

    # ========================================================
    # COMPLETION
    # ========================================================

    def _validate_project(
        self,
        number: int,
    ) -> Dict[str, Any]:

        gate = self.components.get(
            "completion_gate"
        )

        if not gate:

            return self._local_completion_check(
                number
            )

        # Try the existing gate without assuming
        # its exact public API.

        for method_name in [
            "validate_anime",
            "validate_project",
            "validate",
            "check_anime",
        ]:

            method = getattr(
                gate,
                method_name,
                None,
            )

            if not callable(method):
                continue

            for args, kwargs in [

                (
                    (number,),
                    {},
                ),

                (
                    (),
                    {
                        "anime_number": number
                    },
                ),

                (
                    (),
                    {
                        "project_id":
                            f"anime_{number:02d}"
                    },
                ),

            ]:

                try:

                    return {
                        "status": "checked",
                        "result": method(
                            *args,
                            **kwargs,
                        ),
                    }

                except TypeError:
                    continue

        return self._local_completion_check(
            number
        )

    # ========================================================
    # LOCAL COMPLETION CHECK
    # ========================================================

    def _local_completion_check(
        self,
        number: int,
    ) -> Dict[str, Any]:

        project_id = (
            f"anime_{number:02d}"
        )

        project_dir = (
            self.generated
            / "anime"
            / project_id
        )

        creative_spec = (
            project_dir
            / "creative_spec.json"
        )

        metadata = (
            project_dir
            / "metadata.json"
        )

        poster = (
            self.generated
            / "posters"
            / project_id
            / "poster.png"
        )

        videos = []

        if project_dir.exists():

            videos = [
                p
                for p in project_dir.rglob("*")
                if p.is_file()
                and p.suffix.lower()
                in {
                    ".mp4",
                    ".webm",
                    ".mov",
                }
            ]

        checks = {
            "creative_spec": (
                creative_spec.exists()
            ),
            "metadata": (
                metadata.exists()
            ),
            "poster": (
                poster.exists()
            ),
            "video": (
                len(videos) > 0
            ),
        }

        return {
            "status": (
                "complete"
                if all(checks.values())
                else "incomplete"
            ),
            "checks": checks,
            "videos": [
                str(path)
                for path in videos
            ],
        }

    # ========================================================
    # COMPLETION INTERPRETATION
    # ========================================================

    @staticmethod
    def _completion_is_valid(
        result: Dict[str, Any],
    ) -> bool:

        if not result:
            return False

        if result.get(
            "status"
        ) == "complete":
            return True

        nested = result.get(
            "result"
        )

        if isinstance(
            nested,
            dict,
        ):

            if nested.get(
                "status"
            ) == "complete":
                return True

            if nested.get(
                "valid"
            ) is True:
                return True

        checks = result.get(
            "checks"
        )

        if isinstance(
            checks,
            dict,
        ):

            return all(
                bool(value)
                for value in checks.values()
            )

        return False

    # ========================================================
    # PUBLISH
    # ========================================================

    def publish(
        self,
    ) -> Dict[str, Any]:

        publisher = self.components.get(
            "publisher"
        )

        if not publisher:

            return {
                "status": "publisher_unavailable",
                "error": self.component_errors.get(
                    "publisher"
                ),
            }

        for method_name in [
            "publish",
            "publish_everything",
            "run",
        ]:

            method = getattr(
                publisher,
                method_name,
                None,
            )

            if not callable(method):
                continue

            try:

                result = method()

                return {
                    "status": "published",
                    "result": result,
                }

            except TypeError:

                try:

                    result = method(
                        root=self.root
                    )

                    return {
                        "status": "published",
                        "result": result,
                    }

                except Exception:
                    pass

        return {
            "status": "publisher_method_not_found",
        }

    # ========================================================
    # COMPLETE AUTONOMOUS MISSION
    # ========================================================

    def run_full_mission(
        self,
    ) -> Dict[str, Any]:

        started = time.time()

        preparation = self.prepare()

        anime = self.build_all_anime()

        publishing = None

        if self.config.auto_publish:

            publishing = self.publish()

        finished = time.time()

        result = {

            "status": (
                "completed"
                if anime.get(
                    "failed",
                    0,
                ) == 0
                else "completed_with_failures"
            ),

            "started_at": started,

            "finished_at": finished,

            "duration_seconds": (
                finished - started
            ),

            "preparation": preparation,

            "anime": anime,

            "publishing": publishing,

            "final_status": self.status(),
        }

        self._write_json(
            self.runtime
            / "full_mission_report.json",
            result,
        )

        return result

    # ========================================================
    # RESUME FAILED / INCOMPLETE
    # ========================================================

    def resume_incomplete_anime(
        self,
    ) -> Dict[str, Any]:

        results = []

        for number in range(
            1,
            self.config.anime_target + 1,
        ):

            project_id = (
                f"anime_{number:02d}"
            )

            state = (
                self._load_project_state(
                    project_id,
                    "anime",
                    number,
                )
            )

            if state.status == "completed":
                continue

            results.append(
                self.build_anime(
                    number
                )
            )

        return {
            "status": "resume_finished",
            "processed": len(results),
            "results": results,
        }

    # ========================================================
    # RETRY STAGE
    # ========================================================

    def _run_stage(
        self,
        state: ProjectState,
        stage: str,
        function: Callable[[], Any],
    ) -> Any:

        if (
            self.config.skip_completed
            and stage in state.completed_stages
        ):

            return (
                state.stage_results.get(
                    stage,
                    {
                        "status": "already_completed"
                    },
                )
            )

        state.current_stage = stage
        state.updated_at = time.time()

        self._save_state(
            state
        )

        started = time.time()

        last_error = None
        last_traceback = None

        max_attempts = (
            self.config.max_retries
            + 1
        )

        for attempt in range(
            1,
            max_attempts + 1,
        ):

            state.attempts[
                stage
            ] = attempt

            try:

                output = function()

                finished = time.time()

                stage_result = StageResult(
                    stage=stage,
                    status="completed",
                    started_at=started,
                    finished_at=finished,
                    attempts=attempt,
                    output=self._safe_json(
                        output
                    ),
                )

                state.stage_results[
                    stage
                ] = asdict(
                    stage_result
                )

                if (
                    stage
                    not in state.completed_stages
                ):

                    state.completed_stages.append(
                        stage
                    )

                if (
                    stage
                    in state.failed_stages
                ):

                    state.failed_stages.remove(
                        stage
                    )

                state.updated_at = time.time()

                self._save_state(
                    state
                )

                return output

            except Exception as exc:

                last_error = str(
                    exc
                )

                last_traceback = (
                    traceback.format_exc()
                )

                if (
                    attempt
                    < max_attempts
                ):

                    time.sleep(
                        self.config.retry_delay_seconds
                    )

        finished = time.time()

        stage_result = StageResult(
            stage=stage,
            status="failed",
            started_at=started,
            finished_at=finished,
            attempts=max_attempts,
            output={},
            error=last_error,
            traceback_text=last_traceback,
        )

        state.stage_results[
            stage
        ] = asdict(
            stage_result
        )

        if (
            stage
            not in state.failed_stages
        ):

            state.failed_stages.append(
                stage
            )

        self._save_state(
            state
        )

        raise RuntimeError(
            f"Stage '{stage}' failed after "
            f"{max_attempts} attempts: "
            f"{last_error}"
        )

    # ========================================================
    # GENERIC COMPONENT CALL
    # ========================================================

    def _generic_component_call(
        self,
        component: Any,
        method_names: Iterable[str],
        spec: Dict[str, Any],
    ) -> Any:

        for method_name in method_names:

            method = getattr(
                component,
                method_name,
                None,
            )

            if not callable(method):
                continue

            attempts = [

                lambda: method(
                    spec
                ),

                lambda: method(
                    project=spec
                ),

                lambda: method(
                    project_spec=spec
                ),

                lambda: method(
                    data=spec
                ),

                lambda: method(
                    project_id=spec[
                        "project_id"
                    ],
                    spec=spec,
                ),

            ]

            for attempt in attempts:

                try:

                    return attempt()

                except TypeError:
                    continue

        return None

    # ========================================================
    # SAFE CALL
    # ========================================================

    @staticmethod
    def _call_first(
        component: Any,
        methods: List[str],
    ) -> Any:

        for method_name in methods:

            method = getattr(
                component,
                method_name,
                None,
            )

            if not callable(method):
                continue

            for args, kwargs in [
                ((), {}),
            ]:

                try:

                    return method(
                        *args,
                        **kwargs,
                    )

                except TypeError:
                    continue

        return None

    # ========================================================
    # POSTER PROMPT
    # ========================================================

    @staticmethod
    def _poster_prompt(
        spec: Dict[str, Any],
    ) -> str:

        characters = ", ".join(
            str(
                character.get(
                    "name",
                    "",
                )
            )
            for character in spec.get(
                "characters",
                [],
            )
            if isinstance(
                character,
                dict,
            )
        )

        return (
            "Original cinematic anime poster. "
            f"Title: {spec.get('title', '')}. "
            f"Genre: {spec.get('genre', '')}. "
            f"Story: {spec.get('story', '')}. "
            f"Characters: {characters}. "
            "The visual must represent the actual story "
            "and emotional climax. "
            "Original fictional characters."
        )

    # ========================================================
    # STATE
    # ========================================================

    def _load_project_state(
        self,
        project_id: str,
        project_type: str,
        number: int,
    ) -> ProjectState:

        path = (
            self.state_dir
            / f"{project_id}.json"
        )

        if not path.exists():

            return ProjectState(
                project_id=project_id,
                project_type=project_type,
                number=number,
            )

        try:

            data = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

            return ProjectState(
                **data
            )

        except Exception:

            return ProjectState(
                project_id=project_id,
                project_type=project_type,
                number=number,
            )

    def _save_state(
        self,
        state: ProjectState,
    ) -> None:

        path = (
            self.state_dir
            / f"{state.project_id}.json"
        )

        self._write_json(
            path,
            asdict(state),
        )

    def _load_state_file(
        self,
        path: Path,
    ) -> Optional[Dict[str, Any]]:

        try:

            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            return None

    # ========================================================
    # LOGGING
    # ========================================================

    def _write_log(
        self,
        project_id: str,
        stage: str,
        message: str,
    ) -> None:

        if not self.config.save_logs:
            return

        path = (
            self.logs_dir
            / f"{project_id}.log"
        )

        timestamp = time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with path.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                f"[{timestamp}] "
                f"[{stage}] "
                f"{message}\n"
            )

    # ========================================================
    # JSON
    # ========================================================

    @staticmethod
    def _write_json(
        path: Path,
        data: Any,
    ) -> None:

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

    @staticmethod
    def _safe_json(
        value: Any,
    ) -> Any:

        try:

            json.dumps(
                value
            )

            return value

        except Exception:

            return str(
                value
            )


# ============================================================
# CLI
# ============================================================

def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA AI Full System Bridge"
        )
    )

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--prepare",
        action="store_true",
    )

    parser.add_argument(
        "--anime",
        type=int,
    )

    parser.add_argument(
        "--all-anime",
        action="store_true",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
    )

    parser.add_argument(
        "--mission",
        action="store_true",
    )

    parser.add_argument(
        "--publish",
        action="store_true",
    )

    parser.add_argument(
        "--status",
        action="store_true",
    )

    args = parser.parse_args()

    bridge = (
        AJVYRAAIFullSystemBridge(
            args.root
        )
    )

    if args.prepare:

        print(
            json.dumps(
                bridge.prepare(),
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.status:

        print(
            json.dumps(
                bridge.status(),
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.anime:

        result = bridge.build_anime(
            args.anime
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.all_anime:

        result = (
            bridge.build_all_anime()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.resume:

        result = (
            bridge.resume_incomplete_anime()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.publish:

        result = bridge.publish()

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    if args.mission:

        result = (
            bridge.run_full_mission()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
                default=str,
            )
        )

        return

    print(
        json.dumps(
            bridge.status(),
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
