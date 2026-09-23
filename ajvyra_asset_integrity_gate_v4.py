from __future__ import annotations

import hashlib
import json
from pathlib import Path


class AssetIntegrityGate:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def sha256(self, path: Path) -> str:
        h = hashlib.sha256()

        with path.open("rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)

        return h.hexdigest()

    def validate_anime(self):
        result = []

        for i in range(1, 31):
            folder = self.root / "anime" / f"anime_{i:02d}"
            video = folder / "video" / "main.mp4"
            poster = folder / "poster.jpg"

            valid = (
                folder.exists()
                and video.exists()
                and poster.exists()
                and video.stat().st_size > 100_000
                and poster.stat().st_size > 10_000
            )

            result.append({
                "id": i,
                "valid": valid,
                "video": str(video),
                "poster": str(poster),
            })

        return result

    def validate_games(self):
        result = []

        for i in range(1, 31):
            path = (
                self.root
                / "games"
                / f"game_{i:02d}"
                / "index.html"
            )

            valid = path.exists() and path.stat().st_size > 1_000

            result.append({
                "id": i,
                "valid": valid,
                "path": str(path),
            })

        return result

    def run(self):
        anime = self.validate_anime()
        games = self.validate_games()

        passed = (
            len(anime) == 30
            and len(games) == 30
            and all(x["valid"] for x in anime)
            and all(x["valid"] for x in games)
        )

        report = {
            "gate": "ASSET_INTEGRITY",
            "passed": passed,
            "anime": anime,
            "games": games,
        }

        output = self.root / "asset_integrity_report.json"
        output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        AssetIntegrityGate().run(),
        indent=2,
        ensure_ascii=False,
    ))
