from __future__ import annotations

import json
import traceback
from pathlib import Path
from typing import Any, Dict


class AJVYRAAnimeRealProductionMaster:

    def __init__(
        self,
        root: str = "generated/anime_production",
        shot_engine=None,
        keyframe_engine=None,
        audio_engine=None,
        render_engine=None,
    ):
        self.root = Path(root)

        from ajvyra_anime_media_orchestrator import (
            AJVYRAMediaOrchestrator,
        )

        self.orchestrator = AJVYRAMediaOrchestrator(
            root=root,
            shot_engine=shot_engine,
            keyframe_engine=keyframe_engine,
            audio_engine=audio_engine,
            render_engine=render_engine,
        )

    def produce(
        self,
        anime: Dict[str, Any],
        story: Dict[str, Any],
    ) -> Dict[str, Any]:

        anime_id = anime["anime_id"]
        episode_id = "episode_01"

        report_dir = (
            self.root
            / anime_id
            / "season_01"
            / episode_id
        )

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:

            from ajvyra_anime_shot_production_engine import (
                AJVYRAAnimeShotProductionEngine,
            )

            shot_builder = (
                AJVYRAAnimeShotProductionEngine(
                    output_root=str(self.root),
                )
            )

            shot_plan = shot_builder.build_shot_plan(
                anime_id=anime_id,
                episode_id=episode_id,
                story=story,
                target_seconds=1800,
            )

            result = self.orchestrator.run(
                anime_id=anime_id,
                episode_id=episode_id,
                genre=anime["genre"],
                shot_plan=shot_plan,
                generate_video=True,
                generate_audio=True,
                render=True,
            )

            result["success"] = (
                result.get("failed_shots", 0) == 0
                and bool(result.get("output_video"))
            )

            self._save_report(
                report_dir,
                result,
            )

            return result

        except Exception as exc:

            result = {
                "success": False,
                "anime_id": anime_id,
                "episode_id": episode_id,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }

            self._save_report(
                report_dir,
                result,
            )

            return result

    @staticmethod
    def _save_report(
        directory: Path,
        report: Dict[str, Any],
    ):

        path = directory / "production_report.json"

        path.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
