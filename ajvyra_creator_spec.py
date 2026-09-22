from dataclasses import dataclass, field
from typing import Any


@dataclass
class CreatorRequest:
    request_id: str
    project_type: str
    title: str
    description: str

    target_language: str = "fa"
    style: str = "anime"

    duration_minutes: int | None = None

    features: list[str] = field(default_factory=list)
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass
class CreatorResult:
    request_id: str
    project_type: str
    project_path: str
    generated_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    status: str = "created"


def validate_request(request: CreatorRequest) -> None:
    allowed_types = {
        "anime",
        "game",
    }

    if request.project_type not in allowed_types:
        raise ValueError(
            "project_type must be 'anime' or 'game'."
        )

    if not request.title.strip():
        raise ValueError(
            "Project title cannot be empty."
        )

    if not request.description.strip():
        raise ValueError(
            "Project description cannot be empty."
        )
