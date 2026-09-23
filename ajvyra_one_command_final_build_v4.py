from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path("generated/ajvyra_release")


def run_module(module: str):
    print(f"\n[AJVYRA] RUNNING {module}")

    result = subprocess.run(
        [sys.executable, module],
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{module} failed with code "
            f"{result.returncode}"
        )


def main():
    ROOT.mkdir(parents=True, exist_ok=True)

    # Existing game build.
    run_module("ajvyra_browser_game_builder_v3.py")

    # Existing game validation.
    run_module("ajvyra_game_runtime_validator_v3.py")
    run_module("ajvyra_game_playability_probe_v3.py")
    run_module("ajvyra_game_library_manifest_v3.py")

    # Existing anime publication bundle.
    run_module("ajvyra_real_anime_publish_bundle_v2.py")

    # Final integration.
    run_module("ajvyra_final_site_integration_v4.py")
    run_module("ajvyra_unified_anime_game_router_v4.py")

    # Final integrity.
    run_module("ajvyra_asset_integrity_gate_v4.py")
    run_module("ajvyra_browser_game_final_validator_v4.py")
    run_module("ajvyra_anime_final_validator_v4.py")
    run_module("ajvyra_site_link_validator_v4.py")

    # Production state.
    run_module("ajvyra_production_completion_manager_v4.py")

    # Final manifest.
    run_module("ajvyra_final_release_manifest_v4.py")

    # Absolute final gate.
    run_module("ajvyra_final_release_gate_v4.py")

    gate_path = ROOT / "AJVYRA_FINAL_RELEASE_GATE_V4.json"

    if not gate_path.exists():
        raise RuntimeError("Final gate report was not created.")

    gate = json.loads(
        gate_path.read_text(encoding="utf-8")
    )

    final_status = {
        "project": "AJVYRA",
        "anime_target": 30,
        "game_target": 30,
        "status": gate.get(
            "status",
            "RELEASE_BLOCKED",
        ),
        "publication_allowed": gate.get(
            "publication_allowed",
            False,
        ),
    }

    output = ROOT / "AJVYRA_FINAL_STATUS_V4.json"

    output.write_text(
        json.dumps(
            final_status,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\n==============================")
    print("        AJVYRA FINAL BUILD")
    print("==============================")
    print(json.dumps(
        final_status,
        indent=2,
        ensure_ascii=False,
    ))

    if not final_status["publication_allowed"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
