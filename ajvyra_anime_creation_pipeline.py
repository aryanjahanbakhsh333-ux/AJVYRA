from dataclasses import dataclass, asdict
from typing import Dict, List


@dataclass
class ProductionStage:
    name: str
    status: str = "pending"
    progress: float = 0.0
    notes: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class AnimeCreationPipeline:

    DEFAULT_STAGES = [
        "concept",
        "anime_bible",
        "characters",
        "character_design",
        "story",
        "scenes",
        "dialogue",
        "digital_voice",
        "visual_assets",
        "animation",
        "sound_design",
        "subtitles",
        "editing",
        "quality_control",
        "final_export"
    ]

    def __init__(self, project_id: str):
        self.project_id = project_id

        self.stages = {
            name: ProductionStage(name)
            for name in self.DEFAULT_STAGES
        }

    def update(
        self,
        stage_name: str,
        progress: float,
        status: str = "in_progress",
        notes: str = ""
    ):

        if stage_name not in self.stages:
            raise KeyError(
                f"Unknown production stage: {stage_name}"
            )

        progress = max(
            0.0,
            min(100.0, progress)
        )

        if progress >= 100:
            status = "completed"

        self.stages[stage_name] = ProductionStage(
            name=stage_name,
            status=status,
            progress=progress,
            notes=notes
        )

    def overall_progress(self) -> float:

        if not self.stages:
            return 0.0

        return sum(
            stage.progress
            for stage in self.stages.values()
        ) / len(self.stages)

    def current_stage(self) -> str:

        for name, stage in self.stages.items():
            if stage.progress < 100:
                return name

        return "completed"

    def report(self) -> Dict:

        return {
            "project_id": self.project_id,
            "overall_progress": round(
                self.overall_progress(),
                2
            ),
            "current_stage": self.current_stage(),
            "stages": {
                name: stage.to_dict()
                for name, stage in self.stages.items()
            }
        }


if __name__ == "__main__":
    pipeline = AnimeCreationPipeline(
        "PROJECT-001"
    )

    pipeline.update(
        "concept",
        100,
        notes="Original concept approved."
    )

    pipeline.update(
        "characters",
        50,
        notes="Main cast being developed."
    )

    print(pipeline.report())
