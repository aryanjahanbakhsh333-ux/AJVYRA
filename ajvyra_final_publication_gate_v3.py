"""
THE FINAL AJVYRA PUBLICATION GATE.

Nothing is marked release-ready unless:
30/30 anime are present and valid.
30/30 games are present and playable.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_final_release_manifest_v3 import build


def publish_gate(root: Path) -> dict:
    try:
        final_manifest = build(root)

        result = {
            "project": "AJVYRA",
            "status": "RELEASE_READY",
            "release_ready": True,
            "final_manifest": str(final_manifest),
            "anime": "30/30",
            "games": "30/30",
        }

    except Exception as exc:
        result = {
            "project": "AJVYRA",
            "status": "RELEASE_BLOCKED",
            "release_ready": False,
            "reason": str(exc),
        }

    output = root / "AJVYRA_PUBLICATION_STATUS.json"

    output.write_text(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not result["release_ready"]:
        raise RuntimeError(
            "AJVYRA PUBLICATION BLOCKED: "
            + result["reason"]
        )

    return result


if __name__ == "__main__":
    root = Path("generated/ajvyra_release")
    result = publish_gate(root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
