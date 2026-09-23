from __future__ import annotations

import json
from pathlib import Path


class Queue:

    def __init__(
        self,
        file: Path
    ):
        self.file = file
        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not file.exists():
            self.save([])

    def load(self):
        return json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

    def save(self, jobs):
        temp = self.file.with_suffix(
            ".tmp"
        )

        temp.write_text(
            json.dumps(
                jobs,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        temp.replace(
            self.file
        )

    def create(self, jobs):

        current = self.load()

        known = {
            job["job_id"]
            for job in current
        }

        for job in jobs:

            data = {
                "job_id": job.job_id,
                "anime_number":
                    job.anime_number,
                "anime_id":
                    job.anime_id,
                "segment_number":
                    job.segment_number,
                "segment_title":
                    job.segment_title,
                "prompt":
                    job.prompt,
                "negative_prompt":
                    job.negative_prompt,
                "output_file":
                    job.output_file,
                "status":
                    job.status,
                "retries":
                    job.retries,
                "error":
                    job.error,
            }

            if data["job_id"] not in known:
                current.append(data)

        self.save(current)

    def update(
        self,
        job_id,
        **changes
    ):

        jobs = self.load()

        for job in jobs:

            if job["job_id"] == job_id:
                job.update(
                    changes
                )
                self.save(jobs)
                return

        raise KeyError(
            f"Unknown job: {job_id}"
        )

    def pending(self):

        return [
            job
            for job in self.load()
            if job["status"]
            in {
                "pending",
                "retry"
            }
        ]
