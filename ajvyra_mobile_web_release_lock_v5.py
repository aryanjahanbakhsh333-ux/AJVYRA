from __future__ import annotations

import json
from pathlib import Path


class MobileWebReleaseLock:
    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def run(self):
        site = self.root / "site" / "index.html"

        valid = False

        if site.exists():
            html = site.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            required = [
                "viewport",
                "width=device-width",
                "playsinline",
            ]

            valid = all(
                token in html
                for token in required
            )

        report = {
            "stage": "MOBILE_WEB_RELEASE_LOCK",
            "passed": valid,
            "android_browser": valid,
            "iphone_browser": valid,
            "installation_required": False,
        }

        (self.root / "MOBILE_WEB_RELEASE_LOCK_V5.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return report


if __name__ == "__main__":
    print(json.dumps(
        MobileWebReleaseLock().run(),
        indent=2,
        ensure_ascii=False,
    ))
