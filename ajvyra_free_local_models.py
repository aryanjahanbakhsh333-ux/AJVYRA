from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class AnimeJob:
    job_id: str
    anime_number: int
    anime_id: str
    segment_number: int
    segment_title: str
    prompt: str
    negative_prompt: str
    output_file: str
    status: str = "pending"
    retries: int = 0
    error: str = ""


@dataclass
class QCResult:
    valid: bool
    path: str
    errors: List[str]
    warnings: List[str]


@dataclass
class ReleaseResult:
    ready: bool
    anime_ready: int
    anime_total: int
    games_ready: int
    games_total: int
    errors: List[str]
