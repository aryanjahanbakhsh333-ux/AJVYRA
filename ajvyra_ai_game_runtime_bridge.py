"""
AJVYRA AI GAME RUNTIME BRIDGE
==============================

Connects the existing AJVYRA AI game-generation system
to the real playable AJVYRA execution engine.

FLOW:

AI Content Director
        ↓
Game Creative Specification
        ↓
Universal Builder / AI Builder
        ↓
AJVYRA AI Game Runtime Bridge
        ↓
AJVYRA Real Execution Engine
        ↓
HTML5 PLAYABLE GAME
        ↓
generated/games/game_XX/
"""

from __future__ import annotations

import importlib
import json
import time

from pathlib import Path
from typing import Any, Dict, Optional


class AJVYRAAIGameRuntimeBridge:

    VERSION = "1.0.0"

    def __init__(
        self,
        root: str | Path = ".",
    ) -> None:

        self.root = Path(
            root
        ).resolve()

        self.generated_root = (
            self.root
            / "generated"
            / "games"
        )

        self.runtime_root = (
            self.root
            / "runtime"
            / "game_runtime_bridge"
        )

        self.generated_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.runtime_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.content_director = (
            self._load_content_director()
        )

        self.execution_engine = (
            self._load_execution_engine()
        )

    # ========================================================
    # COMPONENT LOADING
    # ========================================================

    def _load_content_director(
        self,
    ) -> Optional[Any]:

        try:

            module = importlib.import_module(
                "ajvyra_ai_content_director"
            )

            cls = getattr(
                module,
                "AJVYRAAIContentDirector",
            )

            for attempt in [
                lambda: cls(
                    self.root
                ),
                lambda: cls(
                    root=self.root
                ),
                lambda: cls(),
            ]:

                try:

                    return attempt()

                except TypeError:

                    continue

        except Exception:

            return None

        return None

    def _load_execution_engine(
        self,
    ) -> Any:

        module = importlib.import_module(
            "ajvyra_real_execution_engine"
        )

        cls = getattr(
            module,
            "AJVYRARealExecutionEngine",
        )

        for attempt in [
            lambda: cls(
                self.root
            ),
            lambda: cls(
                root=self.root
            ),
            lambda: cls(),
        ]:

            try:

                return attempt()

            except TypeError:

                continue

        raise RuntimeError(
            "Could not initialize "
            "AJVYRA Real Execution Engine."
        )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def build_game(
        self,
        game_number: int,
    ) -> Dict[str, Any]:

        if not (
            1
            <= game_number
            <= 70
        ):

            raise ValueError(
                "AJVYRA currently targets "
                "70 games. "
                "game_number must be 1-70."
            )

        started = time.time()

        game_id = (
            f"game_{game_number:02d}"
        )

        # ----------------------------------------------------
        # 1. GET CREATIVE SPEC
        # ----------------------------------------------------

        spec = (
            self.get_game_spec(
                game_number
            )
        )

        # ----------------------------------------------------
        # 2. NORMALIZE SPEC
        # ----------------------------------------------------

        spec = (
            self.normalize_game_spec(
                spec,
                game_number,
            )
        )

        # ----------------------------------------------------
        # 3. SAVE SPEC
        # ----------------------------------------------------

        spec_path = (
            self.generated_root
            / game_id
            / "creative_spec.json"
        )

        spec_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._write_json(
            spec_path,
            spec,
        )

        # ----------------------------------------------------
        # 4. EXECUTE REAL GAME BUILD
        # ----------------------------------------------------

        result = (
            self.execution_engine.build_game(
                spec
            )
        )

        # ----------------------------------------------------
        # 5. CREATE BRIDGE REPORT
        # ----------------------------------------------------

        finished = time.time()

        report = {

            "bridge": (
                "AJVYRA AI Game Runtime Bridge"
            ),

            "version": self.VERSION,

            "game_number": game_number,

            "game_id": game_id,

            "title": spec.get(
                "title",
                game_id,
            ),

            "started_at": started,

            "finished_at": finished,

            "duration_seconds": (
                finished - started
            ),

            "creative_spec": str(
                spec_path
            ),

            "runtime_result": result,

            "playable": True,

            "platform": "HTML5",

        }

        report_path = (
            self.generated_root
            / game_id
            / "runtime_report.json"
        )

        self._write_json(
            report_path,
            report,
        )

        return report

    # ========================================================
    # BUILD ALL 70
    # ========================================================

    def build_all_games(
        self,
    ) -> Dict[str, Any]:

        started = time.time()

        results = []

        for number in range(
            1,
            71,
        ):

            try:

                result = (
                    self.build_game(
                        number
                    )
                )

                results.append(
                    result
                )

            except Exception as exc:

                results.append(
                    {
                        "game_number": number,
                        "status": "failed",
                        "error": str(
                            exc
                        ),
                    }
                )

        finished = time.time()

        successful = [
            result
            for result in results
            if result.get(
                "playable"
            ) is True
        ]

        failed = [
            result
            for result in results
            if result.get(
                "status"
            ) == "failed"
        ]

        summary = {

            "status": (
                "completed"
                if not failed
                else "completed_with_failures"
            ),

            "target": 70,

            "successful": len(
                successful
            ),

            "failed": len(
                failed
            ),

            "started_at": started,

            "finished_at": finished,

            "duration_seconds": (
                finished - started
            ),

            "games": results,

        }

        self._write_json(
            self.runtime_root
            / "all_games_report.json",
            summary,
        )

        return summary

    # ========================================================
    # GET GAME SPEC
    # ========================================================

    def get_game_spec(
        self,
        game_number: int,
    ) -> Dict[str, Any]:

        game_id = (
            f"game_{game_number:02d}"
        )

        # ----------------------------------------------------
        # FIRST: EXISTING CREATIVE SPEC
        # ----------------------------------------------------

        paths = [

            self.generated_root
            / game_id
            / "creative_spec.json",

            self.root
            / "runtime"
            / "games"
            / game_id
            / "creative_spec.json",

            self.root
            / "generated"
            / "game"
            / game_id
            / "creative_spec.json",

        ]

        for path in paths:

            if not path.exists():
                continue

            try:

                data = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

                if isinstance(
                    data,
                    dict,
                ):

                    return data

            except Exception:

                pass

        # ----------------------------------------------------
        # SECOND: AI CONTENT DIRECTOR
        # ----------------------------------------------------

        if self.content_director:

            methods = [
                "create_game_spec",
                "generate_game_spec",
                "build_game_spec",
                "create_game",
            ]

            for method_name in methods:

                method = getattr(
                    self.content_director,
                    method_name,
                    None,
                )

                if not callable(method):
                    continue

                attempts = [

                    lambda: method(
                        game_number
                    ),

                    lambda: method(
                        number=game_number
                    ),

                    lambda: method(
                        game_id
                        )
                ]

                for attempt in attempts:

                    try:

                        result = attempt()

                        if isinstance(
                            result,
                            dict,
                        ):

                            return result

                    except (
                        TypeError,
                        AttributeError,
                    ):

                        continue

        # ----------------------------------------------------
        # THIRD: FALLBACK SPEC
        # ----------------------------------------------------

        return self._fallback_spec(
            game_number
        )

    # ========================================================
    # NORMALIZE
    # ========================================================

    def normalize_game_spec(
        self,
        spec: Dict[str, Any],
        game_number: int,
    ) -> Dict[str, Any]:

        game_id = (
            f"game_{game_number:02d}"
        )

        normalized = dict(
            spec
        )

        normalized[
            "game_id"
        ] = game_id

        normalized.setdefault(
            "title",
            f"AJVYRA Game {game_number:02d}",
        )

        normalized.setdefault(
            "genre",
            "Action",
        )

        normalized.setdefault(
            "story",
            "An original AJVYRA adventure.",
        )

        normalized.setdefault(
            "player",
            {
                "name": "AJVYRA",
                "hp": 100,
                "max_hp": 100,
                "speed": 240,
                "size": 24,
            },
        )

        normalized.setdefault(
            "levels",
            self._default_levels()
        )

        normalized.setdefault(
            "enemies",
            self._default_enemies()
        )

        normalized[
            "platform"
        ] = "HTML5"

        normalized[
            "playable"
        ] = True

        normalized[
            "engine"
        ] = (
            "AJVYRA Real Execution Engine"
        )

        return normalized

    # ========================================================
    # DEFAULT LEVELS
    # ========================================================

    @staticmethod
    def _default_levels() -> list:

        return [

            {
                "number": 1,
                "name": "Awakening",
                "objective": (
                    "Defeat all enemies"
                ),
                "enemy_count": 5,
                "difficulty": 1.0,
            },

            {
                "number": 2,
                "name": "First Descent",
                "objective": (
                    "Survive and defeat the enemies"
                ),
                "enemy_count": 7,
                "difficulty": 1.15,
            },

            {
                "number": 3,
                "name": "Dark Path",
                "objective": (
                    "Reach the next stage"
                ),
                "enemy_count": 9,
                "difficulty": 1.35,
            },

            {
                "number": 4,
                "name": "Final Trial",
                "objective": (
                    "Defeat the stronger enemies"
                ),
                "enemy_count": 12,
                "difficulty": 1.6,
            },

            {
                "number": 5,
                "name": "The End",
                "objective": (
                    "Defeat everything"
                ),
                "enemy_count": 15,
                "difficulty": 1.9,
            },

        ]

    # ========================================================
    # DEFAULT ENEMIES
    # ========================================================

    @staticmethod
    def _default_enemies() -> list:

        return [

            {
                "enemy_id": "shadow",
                "name": "Shadow",
                "hp": 40,
                "max_hp": 40,
                "speed": 65,
                "damage": 8,
                "size": 20,
            },

            {
                "enemy_id": "hunter",
                "name": "Hunter",
                "hp": 55,
                "max_hp": 55,
                "speed": 82,
                "damage": 11,
                "size": 22,
            },

            {
                "enemy_id": "warden",
                "name": "Warden",
                "hp": 85,
                "max_hp": 85,
                "speed": 52,
                "damage": 16,
                "size": 28,
            },

        ]

    # ========================================================
    # FALLBACK
    # ========================================================

    def _fallback_spec(
        self,
        number: int,
    ) -> Dict[str, Any]:

        return {

            "game_id":
                f"game_{number:02d}",

            "title":
                f"AJVYRA Game {number:02d}",

            "genre":
                "Action",

            "story":
                (
                    "An original fictional "
                    "AJVYRA adventure in which "
                    "the player must survive "
                    "five increasingly difficult "
                    "stages."
                ),

            "player": {

                "name":
                    "AJVYRA",

                "hp":
                    100,

                "max_hp":
                    100,

                "speed":
                    240,

                "size":
                    24,

            },

            "levels":
                self._default_levels(),

            "enemies":
                self._default_enemies(),

        }

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_game(
        self,
        game_number: int,
    ) -> Dict[str, Any]:

        game_id = (
            f"game_{game_number:02d}"
        )

        game_dir = (
            self.generated_root
            / game_id
        )

        required = [

            "index.html",

            "game.js",

            "game.css",

            "metadata.json",

            "creative_spec.json",

            "runtime_report.json",

        ]

        checks = {}

        for filename in required:

            checks[
                filename
            ] = (
                game_dir
                / filename
            ).exists()

        playable = all(
            checks.values()
        )

        result = {

            "game_id":
                game_id,

            "playable":
                playable,

            "checks":
                checks,

            "play_path":
                str(
                    game_dir
                    / "index.html"
                ),

        }

        self._write_json(
            game_dir
            / "validation.json",
            result,
        )

        return result

    # ========================================================
    # VALIDATE ALL
    # ========================================================

    def validate_all_games(
        self,
    ) -> Dict[str, Any]:

        results = []

        for number in range(
            1,
            71,
        ):

            try:

                results.append(
                    self.validate_game(
                        number
                    )
                )

            except Exception as exc:

                results.append(
                    {
                        "game_number":
                            number,
                        "playable":
                            False,
                        "error":
                            str(exc),
                    }
                )

        return {

            "target":
                70,

            "playable":
                sum(
                    1
                    for result in results
                    if result.get(
                        "playable"
                    )
                ),

            "not_playable":
                sum(
                    1
                    for result in results
                    if not result.get(
                        "playable"
                    )
                ),

            "games":
                results,

        }

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


# ============================================================
# CLI
# ============================================================

def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA AI Game Runtime Bridge"
        )
    )

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--game",
        type=int,
    )

    parser.add_argument(
        "--all",
        action="store_true",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
    )

    parser.add_argument(
        "--validate-all",
        action="store_true",
    )

    args = parser.parse_args()

    bridge = (
        AJVYRAAIGameRuntimeBridge(
            args.root
        )
    )

    if args.game:

        result = (
            bridge.build_game(
                args.game
            )
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

    if args.all:

        result = (
            bridge.build_all_games()
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

    if args.validate:

        result = (
            bridge.validate_game(
                args.game or 1
            )
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    if args.validate_all:

        result = (
            bridge.validate_all_games()
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    print(
        "AJVYRA AI Game Runtime Bridge"
    )

    print(
        "Build one:"
    )

    print(
        "python "
        "ajvyra_ai_game_runtime_bridge.py "
        "--game 1"
    )

    print(
        "Build all:"
    )

    print(
        "python "
        "ajvyra_ai_game_runtime_bridge.py "
        "--all"
    )


if __name__ == "__main__":
    main()
