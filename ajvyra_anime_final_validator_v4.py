from __future__ import annotations

import json
import subprocess
from pathlib import Path


class AnimeFinalValidator:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def probe_duration(self, video: Path):
        try:
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
                timeout=30,
            )

            return float(result.stdout.strip())
        except Exception:
            return None

    def validate_one(self, number):
        folder = self.root / "anime" / f"anime_{number:02d}"
        video = folder / "video" / "main.mp4"
        poster = folder / "poster.jpg"

        duration = self.probe_duration(video) if video.exists() else None

        valid = (
            video.exists()
            and poster.exists()
            and video.stat().st_size > 100_000
            and poster.stat().st_size > 10_000
            and duration is not None
            and 1799 <= duration <= 1801
        )

        return {
            "id": number,
            "valid": valid,
            "duration": duration,
            "video": str(video),
            "poster": str(poster),
        }

    def run(self):
        anime = [self.validate_one(i) for i in range(1, 31)]

        report = {
            "count": len(anime),
            "passed": all(x["valid"] for x in anime),
            "anime": anime,
        }

        output = self.root / "anime_final_validation.json"
        output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        AnimeFinalValidator().run(),
        indent=2,
        ensure_ascii=False,
    ))
