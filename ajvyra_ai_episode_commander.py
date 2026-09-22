from dataclasses import dataclass


@dataclass
class EpisodePlan:
    anime_id: int
    episode_number: int
    scenes: list[dict]


class EpisodeCommander:

    def create_plan(
        self,
        anime_id: int,
        episode_number: int,
        scenes: list[dict],
    ) -> EpisodePlan:

        if anime_id < 1 or anime_id > 30:
            raise ValueError(
                "AJVYRA currently supports anime 1-30."
            )

        if episode_number < 1:
            raise ValueError(
                "Episode number must be positive."
            )

        return EpisodePlan(
            anime_id=anime_id,
            episode_number=episode_number,
            scenes=scenes,
        )

    def estimate_jobs(
        self,
        plan: EpisodePlan,
        audio_languages: list[str],
    ) -> int:

        return len(plan.scenes) * len(audio_languages)

    def build_execution_order(
        self,
        plan: EpisodePlan,
    ) -> list[dict]:

        result = []

        for index, scene in enumerate(plan.scenes, start=1):
            result.append({
                "order": index,
                "scene": scene,
            })

        return result
