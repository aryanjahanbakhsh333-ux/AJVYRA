from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path("generated/ajvyra_release")


STEPS = [
    "ajvyra_true_release_preflight_v5.py",
    "ajvyra_real_anime_production_launcher_v5.py",
    "ajvyra_real_anime_content_lock_v5.py",
    "ajvyra_30_minute_duration_hard_lock_v5.py",
    "ajvyra_real_audio_subtitle_lock_v5.py",
    "ajvyra_browser_execution_lock_v5.py",
    "ajvyra_mobile_web_release_lock_v5.py",
    "ajvyra_asset_integrity_gate_v4.py",
    "ajvyra_site_link_validator_v4.py",
    "ajvyra_final_release_manifest_v4.py",
    "ajvyra_absolute_publication_gate_v5.py",
]


def run_step(script):
    print(f"\n[AJVYRA FINAL] {script}")

    result = subprocess.run(
        [sys.executable, script],
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Release step failed: {script}"
        )


def main():
    ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    for script in STEPS:
        run_step(script)

    gate_path = (
        ROOT
        / "AJVYRA_ABSOLUTE_PUBLICATION_GATE_V5.json"
    )

    if not gate_path.exists():
        raise RuntimeError(
            "Absolute publication gate did not produce a report."
        )

    gate = json.loads(
        gate_path.read_text(
            encoding="utf-8"
        )
    )

    status = {
        "project": "AJVYRA",
        "release_version": "V5",
        "anime_count": 30,
        "game_count": 30,
        "status": gate["status"],
        "publication_allowed": gate[
            "publication_allowed"
        ],
        "publication_package": (
            "generated/AJVYRA_PUBLICATION"
            if gate["publication_allowed"]
            else None
        ),
    }

    output = ROOT / "AJVYRA_REAL_FINAL_STATUS_V5.json"

    output.write_text(
        json.dumps(
            status,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\n========================================")
    print("          AJVYRA REAL FINAL RELEASE")
    print("========================================")
    print(json.dumps(
        status,
        indent=2,
        ensure_ascii=False,
    ))

    if not gate["publication_allowed"]:
        print(
            "\nRELEASE BLOCKED: "
            "real production requirements are not satisfied."
        )
        raise SystemExit(2)

    print(
        "\nRELEASE READY: "
        "the publication package passed every gate."
    )


if __name__ == "__main__":
    main()
