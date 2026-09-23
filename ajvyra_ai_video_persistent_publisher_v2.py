from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from huggingface_hub import HfApi, hf_hub_url


class AJVYRAAIVideoPersistentPublisher:
    """
    Publishes generated MP4 files into a Hugging Face Dataset repository.

    Required environment variables:

        HF_TOKEN
        AJVYRA_AI_VIDEO_DATASET

    Example:

        HF_TOKEN=hf_xxxxxxxxx
        AJVYRA_AI_VIDEO_DATASET=username/ajvyra-ai-videos
    """

    def __init__(
        self,
        token: str | None = None,
        repository_id: str | None = None,
    ):
        self.token = token or os.getenv("HF_TOKEN")
        self.repository_id = (
            repository_id
            or os.getenv("AJVYRA_AI_VIDEO_DATASET")
        )

        if not self.token:
            raise RuntimeError(
                "HF_TOKEN is required for persistent video publishing."
            )

        if not self.repository_id:
            raise RuntimeError(
                "AJVYRA_AI_VIDEO_DATASET is required."
            )

        self.api = HfApi(token=self.token)

    @staticmethod
    def _safe_id(value: str) -> str:
        value = value.strip().lower()
        value = re.sub(r"[^a-z0-9_-]+", "-", value)
        value = re.sub(r"-+", "-", value)
        return value.strip("-") or "video"

    def ensure_repository(self) -> None:
        self.api.create_repo(
            repo_id=self.repository_id,
            repo_type="dataset",
            private=False,
            exist_ok=True,
        )

    def publish(
        self,
        local_video_path: str | Path,
        video_id: str,
    ) -> dict[str, Any]:

        path = Path(local_video_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Video does not exist: {path}"
            )

        if path.stat().st_size < 1024:
            raise ValueError(
                "Video file is too small to be considered valid."
            )

        safe_id = self._safe_id(video_id)

        remote_path = (
            f"videos/{safe_id}/{safe_id}.mp4"
        )

        self.ensure_repository()

        self.api.upload_file(
            path_or_fileobj=str(path),
            path_in_repo=remote_path,
            repo_id=self.repository_id,
            repo_type="dataset",
            token=self.token,
            commit_message=f"Add AJVYRA AI video {safe_id}",
        )

        public_url = hf_hub_url(
            repo_id=self.repository_id,
            filename=remote_path,
            repo_type="dataset",
        )

        return {
            "video_id": video_id,
            "repository": self.repository_id,
            "remote_path": remote_path,
            "video_url": public_url,
            "published": True,
        }
