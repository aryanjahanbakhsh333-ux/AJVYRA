from __future__ import annotations

import json
from pathlib import Path


class RealAnimeContentLock:
    """
    Hard lock:
    every anime must contain a real non-empty MP4.
    Placeholder files are rejected.
    """

    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def validate_video(self, path: Path):
        if not path.exists():
            return False, "missing"

        if path.stat().st_size < 100_000:
            return False, "too_small"

        with path.open("rb") as f:
            header = f.read(32)

        if b"ftyp" not in header:
            return False, "not_mp4"

        return True, "valid"

    def run(self):
        results = []

        for i in range(1, 31):
            video = (
                self.root
                / "anime"
                / f"anime_{i:02d}"
                / "video"
                / "main.mp4"
            )

            valid, reason = self.validate_video(video)

            results.append({
                "id": i,
                "valid": valid,
                "reason": reason,
                "path": str(video),
            })

        passed = (
            len(results) == 30
            and all(item["valid"] for item in results)
        )

        report = {
            "stage": "REAL_ANIME_CONTENT_LOCK",
            "passed": passed,
            "anime_count": 30,
            "items": results,
        }

        self.root.mkdir(parents=True, exist_ok=True)

        (self.root / "REAL_ANIME_CONTENT_LOCK_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        RealAnimeContentLock().run(),
        indent=2,
        ensure_ascii=False,
    ))
