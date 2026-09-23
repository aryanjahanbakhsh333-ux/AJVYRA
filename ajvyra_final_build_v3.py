"""
AJVYRA FINAL BUILD — LAST FILE

Build order:

1. Build 30 browser games
2. Validate their runtime
3. Probe playability
4. Build game manifest
5. Build game hub
6. Validate 30 real anime outputs
7. Build final release manifest
8. Open publication gate

The final result is either:

    RELEASE_READY

or:

    RELEASE_BLOCKED

There is no fake success state.
"""

from __future__ import annotations

import json
from pathlib import Path

from ajvyra_browser_game_builder_v3 import main as build_games
from ajvyra_browser_game_runtime_v3 import GAMES
from ajvyra_game_hub_v3 import build_hub
from ajvyra_game_library_manifest_v3 import write_manifest
from ajvyra_game_playability_probe_v3 import run_probe
from ajvyra_game_runtime_validator_v3 import write_report
from ajvyra_final_publication_gate_v3 import publish_gate


ROOT = Path("generated/ajvyra_release")


def final_build() -> dict:
    ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # STEP 1 — browser games
    # ---------------------------------------------------------

    build_games()

    if len(GAMES) != 30:
        raise RuntimeError(
            "AJVYRA game catalog must contain exactly 30 games."
        )

    # ---------------------------------------------------------
    # STEP 2 — static runtime validation
    # ---------------------------------------------------------

    write_report(ROOT)

    # ---------------------------------------------------------
    # STEP 3 — gameplay probe
    # ---------------------------------------------------------

    run_probe(ROOT)

    # ---------------------------------------------------------
    # STEP 4 — game library
    # ---------------------------------------------------------

    write_manifest(ROOT)

    # ---------------------------------------------------------
    # STEP 5 — browser game hub
    # ---------------------------------------------------------

    build_hub(ROOT)

    # ---------------------------------------------------------
    # STEP 6 — final anime + game publication gate
    # ---------------------------------------------------------

    result = publish_gate(ROOT)

    status_path = ROOT / "FINAL_STATUS.json"

    status_path.write_text(
        json.dumps(
            {
                "project": "AJVYRA",
                "final": True,
                "anime": 30,
                "games": 30,
                "browser_games": 30,
                "release": result,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return result


if __name__ == "__main__":
    result = final_build()

    print()
    print("=" * 60)
    print("AJVYRA FINAL RELEASE")
    print("=" * 60)
    print(json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    ))
    print("=" * 60)
