from __future__ import annotations

import json
import subprocess
from pathlib import Path


class ThirtyMinuteHardLock:
    MIN_DURATION = 1799.0
    MAX_DURATION = 1801.0

    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def duration(self, video):
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(video),
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )

        return float(result.stdout.strip())

    def run(self):
        items = []

        for i in range(1, 31):
            video = (
                self.root
                / "anime"
                / f"anime_{i:02d}"
                / "video"
                / "main.mp4"
            )

            try:
                seconds = self.duration(video)
                valid = (
                    self.MIN_DURATION
                    <= seconds
                    <= self.MAX_DURATION
                )
                error = None
            except Exception as exc:
                seconds = None
                valid = False
                error = str(exc)

            items.append({
                "id": i,
                "duration_seconds": seconds,
                "valid": valid,
                "error": error,
            })

        passed = len(items) == 30 and all(
            item["valid"] for item in items
        )

        report = {
            "stage": "30_MINUTE_HARD_LOCK",
            "passed": passed,
            "required_seconds": 1800,
            "anime": items,
        }

        (self.root / "30_MINUTE_HARD_LOCK_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        ThirtyMinuteHardLock().run(),
        indent=2,
        ensure_ascii=False,
    ))
