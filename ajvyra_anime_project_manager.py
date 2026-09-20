from dataclasses import dataclass, field, asdict
from pathlib import Path
import json
from typing import List, Dict, Optional


DATA_DIR = Path("ajvyra_data")
PROJECTS_FILE = DATA_DIR / "anime_projects.json"


@dataclass
class AnimeProject:
    project_id: str
    title: str
    original_title: str = ""
    genres: List[str] = field(default_factory=list)
    language_tracks: List[str] = field(
        default_factory=lambda: ["fa", "ja"]
    )
    subtitle_languages: List[str] = field(
        default_factory=lambda: ["en", "fa", "ja"]
    )
    duration_minutes: int = 30
    status: str = "planned"
    description: str = ""
    universe: str = ""
    created_by: str = "AJVYRA"

    def to_dict(self) -> Dict:
        return asdict(self)


class AnimeProjectManager:

    VALID_STATUSES = {
        "planned",
        "development",
        "writing",
        "voice",
        "animation",
        "editing",
        "completed",
        "published"
    }

    def __init__(self, file_path: Path = PROJECTS_FILE):
        self.file_path = file_path
        self.projects: Dict[str, AnimeProject] = {}
        self.load()

    def load(self):
        if not self.file_path.exists():
            return

        data = json.loads(self.file_path.read_text(encoding="utf-8"))

        for item in data:
            project = AnimeProject(**item)
            self.projects[project.project_id] = project

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        data = [
            project.to_dict()
            for project in self.projects.values()
        ]

        self.file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def create(
        self,
        project_id: str,
        title: str,
        genres: Optional[List[str]] = None,
        description: str = ""
    ) -> AnimeProject:

        if project_id in self.projects:
            raise ValueError("Project ID already exists.")

        project = AnimeProject(
            project_id=project_id,
            title=title,
            genres=genres or [],
            description=description
        )

        self.projects[project_id] = project
        self.save()

        return project

    def get(self, project_id: str) -> Optional[AnimeProject]:
        return self.projects.get(project_id)

    def update_status(self, project_id: str, status: str):
        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid production status.")

        project = self.get(project_id)

        if project is None:
            raise KeyError("Project not found.")

        project.status = status
        self.save()

    def search_title(self, query: str) -> List[AnimeProject]:
        query = query.lower().strip()

        return [
            project
            for project in self.projects.values()
            if query in project.title.lower()
            or query in project.original_title.lower()
        ]

    def all_projects(self) -> List[AnimeProject]:
        return list(self.projects.values())


if __name__ == "__main__":
    manager = AnimeProjectManager()

    print("AJVYRA Anime Project Manager")
    print(f"Projects: {len(manager.all_projects())}")
