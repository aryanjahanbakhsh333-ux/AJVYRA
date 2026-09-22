from dataclasses import dataclass


@dataclass
class SceneInstruction:
    scene_id: str
    character_id: str
    location_id: str
    emotion: str
    dialogue: str


class SceneCommander:

    def inspect(
        self,
        scene: dict,
    ) -> SceneInstruction:

        required = [
            "scene_id",
            "character_id",
            "location_id",
            "emotion",
            "dialogue",
        ]

        missing = [
            key for key in required
            if key not in scene
        ]

        if missing:
            raise ValueError(
                f"Scene is missing: {', '.join(missing)}"
            )

        return SceneInstruction(
            scene_id=scene["scene_id"],
            character_id=scene["character_id"],
            location_id=scene["location_id"],
            emotion=scene["emotion"],
            dialogue=scene["dialogue"],
        )

    def build_voice_jobs(
        self,
        scene: SceneInstruction,
        anime_id: int,
        languages: list[str],
    ) -> list[dict]:

        jobs = []

        for language in languages:
            jobs.append({
                "anime_id": anime_id,
                "scene_id": scene.scene_id,
                "character_id": scene.character_id,
                "language": language,
                "emotion": scene.emotion,
                "text": scene.dialogue,
            })

        return jobs
