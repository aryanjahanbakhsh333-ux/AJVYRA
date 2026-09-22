from dataclasses import dataclass


@dataclass
class CreationTask:
    task_id: str
    name: str
    category: str
    dependencies: list[str]
    status: str = "pending"


class CreatorPlanner:

    ANIME_TASKS = [
        ("story", "story"),
        ("world", "world"),
        ("characters", "characters"),
        ("locations", "locations"),
        ("scenes", "scenes"),
        ("dialogue", "dialogue"),
        ("voices", "audio"),
        ("subtitles", "language"),
        ("timeline", "media"),
        ("render", "media"),
        ("quality", "quality"),
    ]

    GAME_TASKS = [
        ("world", "world"),
        ("characters", "characters"),
        ("locations", "world"),
        ("gameplay", "gameplay"),
        ("quests", "gameplay"),
        ("dialogue", "dialogue"),
        ("audio", "audio"),
        ("ui", "interface"),
        ("save_system", "gameplay"),
        ("build", "build"),
        ("quality", "quality"),
    ]

    def plan(self, project_type: str) -> list[CreationTask]:

        source = (
            self.ANIME_TASKS
            if project_type == "anime"
            else self.GAME_TASKS
        )

        tasks = []

        previous = None

        for index, (name, category) in enumerate(
            source,
            start=1,
        ):

            task_id = f"task_{index:03d}"

            dependencies = []

            if previous:
                dependencies.append(previous)

            tasks.append(
                CreationTask(
                    task_id=task_id,
                    name=name,
                    category=category,
                    dependencies=dependencies,
                )
            )

            previous = task_id

        return tasks

    def next_ready_task(
        self,
        tasks: list[CreationTask],
    ):

        completed = {
            task.task_id
            for task in tasks
            if task.status == "completed"
        }

        for task in tasks:

            if task.status != "pending":
                continue

            if all(
                dependency in completed
                for dependency in task.dependencies
            ):
                return task

        return None
