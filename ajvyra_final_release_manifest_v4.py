from __future__ import annotations

import hashlib
import json
from pathlib import Path


class FinalReleaseManifest:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def digest(self, path: Path):
        h = hashlib.sha256()

        with path.open("rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)

        return h.hexdigest()

    def collect(self):
        files = []

        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue

            if path.name.endswith(".json"):
                continue

            files.append({
                "path": str(path.relative_to(self.root)),
                "bytes": path.stat().st_size,
                "sha256": self.digest(path),
            })

        return files

    def run(self):
        manifest = {
            "project": "AJVYRA",
            "release": "FINAL",
            "anime_count": 30,
            "game_count": 30,
            "files": self.collect(),
        }

        output = self.root / "AJVYRA_FINAL_RELEASE_MANIFEST_V4.json"

        output.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return manifest


if __name__ == "__main__":
    result = FinalReleaseManifest().run()
    print(json.dumps({
        "files": len(result["files"]),
        "anime": result["anime_count"],
        "games": result["game_count"],
    }, indent=2))
