from __future__ import annotations

import json
import re
from pathlib import Path


class SiteLinkValidator:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def validate(self):
        index = self.root / "site" / "index.html"

        if not index.exists():
            return {
                "passed": False,
                "reason": "site index missing",
            }

        text = index.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        missing = []

        for i in range(1, 31):
            anime_path = f"anime/anime_{i:02d}/index.html"
            game_path = f"games/game_{i:02d}/index.html"

            if anime_path not in text:
                missing.append(anime_path)

            if game_path not in text:
                missing.append(game_path)

        broken_files = []

        for href in re.findall(r'href=["\']([^"\']+)["\']', text):
            if href.startswith(("http://", "https://", "#")):
                continue

            target = self.root / "site" / href

            if not target.exists():
                target = self.root / href

            if not target.exists():
                broken_files.append(href)

        passed = not missing and not broken_files

        report = {
            "passed": passed,
            "missing_expected_links": missing,
            "broken_links": broken_files,
        }

        output = self.root / "site_link_validation.json"
        output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        SiteLinkValidator().validate(),
        indent=2,
        ensure_ascii=False,
    ))
