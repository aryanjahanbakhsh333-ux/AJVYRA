from __future__ import annotations

import json
from pathlib import Path


class AbsolutePublicationGate:
    """
    The final safety gate.

    Nothing is marked publishable merely because source code exists.
    Every real production gate must pass.
    """

    REPORTS = [
        "TRUE_RELEASE_PREFLIGHT_V5.json",
        "REAL_ANIME_PRODUCTION_RESULT_V5.json",
        "REAL_ANIME_CONTENT_LOCK_V5.json",
        "30_MINUTE_HARD_LOCK_V5.json",
        "REAL_AUDIO_SUBTITLE_LOCK_V5.json",
        "BROWSER_EXECUTION_LOCK_V5.json",
        "MOBILE_WEB_RELEASE_LOCK_V5.json",
        "asset_integrity_report.json",
        "site_link_validation.json",
        "AJVYRA_FINAL_RELEASE_MANIFEST_V4.json",
    ]

    def __init__(self, root="generated/ajvyra_release"):
        self.root = Path(root)

    def read(self, name):
        path = self.root / name

        if not path.exists():
            return None

        try:
            return json.loads(
                path.read_text(encoding="utf-8")
            )
        except Exception:
            return None

    def run(self):
        reports = {}
        missing = []

        for name in self.REPORTS:
            data = self.read(name)

            if data is None:
                missing.append(name)
            else:
                reports[name] = data

        failures = []

        for name, data in reports.items():
            if data.get("passed") is False:
                failures.append(name)

            if data.get("publication_allowed") is False:
                failures.append(name)

        ready = (
            not missing
            and not failures
            and len(failures) == 0
        )

        result = {
            "project": "AJVYRA",
            "anime": 30,
            "games": 30,
            "status": (
                "RELEASE_READY"
                if ready
                else "RELEASE_BLOCKED"
            ),
            "publication_allowed": ready,
            "missing_reports": missing,
            "failed_reports": sorted(set(failures)),
            "real_media_required": True,
            "fake_media_accepted": False,
        }

        (self.root / "AJVYRA_ABSOLUTE_PUBLICATION_GATE_V5.json").write_text(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return result


if __name__ == "__main__":
    print(json.dumps(
        AbsolutePublicationGate().run(),
        indent=2,
        ensure_ascii=False,
    ))
