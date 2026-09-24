"""
AJVYRA — Pre-Release Production Queue + Hourly Shot Engine v12

Goals:
1. Maintain exactly 30 required game slots for pre-release.
2. Maintain exactly 30 required real anime-shot slots for pre-release.
3. Never mark an asset complete unless a real file exists and is non-empty.
4. Run the real shot-production backend once every hour.
5. Keep production state durable in JSON so the process can restart safely.

This scheduler does NOT fake video generation. It invokes a real backend
command supplied by AJVYRA_REAL_SHOT_COMMAND.

Example:
  AJVYRA_REAL_SHOT_COMMAND="python real_shot_worker.py" python this_file.py

The worker must create the real media file at the path supplied in:
  AJVYRA_SHOT_OUTPUT

For games, the queue expects real playable build files/directories registered
by the game's build pipeline.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any


ROOT = Path(os.getenv("AJVYRA_ROOT", Path(__file__).resolve().parent))

RELEASE_ROOT = ROOT / "production" / "release"
GAME_ROOT = RELEASE_ROOT / "games"
SHOT_ROOT = RELEASE_ROOT / "anime_shots"
STATE_ROOT = RELEASE_ROOT / "state"

STATE_FILE = STATE_ROOT / "pre_release_state.json"

REQUIRED_GAMES = 30
REQUIRED_SHOTS = 30

HOURLY_SECONDS = 60 * 60

REAL_SHOT_COMMAND = os.getenv(
    "AJVYRA_REAL_SHOT_COMMAND",
    ""
).strip()


@dataclass
class Asset:
    asset_id: str
    kind: str
    status: str = "pending"
    path: str = ""
    created_at: float = 0.0
    completed_at: float = 0.0
    error: str = ""


def ensure_dirs() -> None:
    GAME_ROOT.mkdir(parents=True, exist_ok=True)
    SHOT_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_ROOT.mkdir(parents=True, exist_ok=True)


def atomic_json_write(path: Path, data: Dict[str, Any]) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    tmp.replace(path)


def load_state() -> Dict[str, Any]:
    ensure_dirs()

    if STATE_FILE.exists():
        return json.loads(
            STATE_FILE.read_text(encoding="utf-8")
        )

    state = {
        "schema": "ajvyra.pre_release.v12",
        "required_games": REQUIRED_GAMES,
        "required_shots": REQUIRED_SHOTS,
        "games": [],
        "anime_shots": [],
        "last_hourly_generation": 0.0,
        "generation_lock": False,
    }

    atomic_json_write(STATE_FILE, state)
    return state


def save_state(state: Dict[str, Any]) -> None:
    atomic_json_write(STATE_FILE, state)


def initialize_slots(state: Dict[str, Any]) -> None:
    existing_games = {
        x["asset_id"] for x in state["games"]
    }

    for index in range(1, REQUIRED_GAMES + 1):
        asset_id = f"game_{index:02d}"

        if asset_id not in existing_games:
            state["games"].append(
                asdict(
                    Asset(
                        asset_id=asset_id,
                        kind="game",
                    )
                )
            )

    existing_shots = {
        x["asset_id"] for x in state["anime_shots"]
    }

    for index in range(1, REQUIRED_SHOTS + 1):
        asset_id = f"anime_shot_{index:02d}"

        if asset_id not in existing_shots:
            state["anime_shots"].append(
                asdict(
                    Asset(
                        asset_id=asset_id,
                        kind="anime_shot",
                    )
                )
            )

    state["games"] = sorted(
        state["games"],
        key=lambda x: x["asset_id"],
    )

    state["anime_shots"] = sorted(
        state["anime_shots"],
        key=lambda x: x["asset_id"],
    )

    save_state(state)


def real_file(path: Path) -> bool:
    return (
        path.exists()
        and path.is_file()
        and path.stat().st_size > 0
    )


def refresh_game_status(state: Dict[str, Any]) -> None:
    """
    A game is complete only if its registered build path is real.
    The actual game build pipeline is responsible for registering paths.
    """
    for game in state["games"]:
        if not game.get("path"):
            continue

        path = ROOT / game["path"]

        if real_file(path):
            game["status"] = "ready"
            game["completed_at"] = (
                game["completed_at"] or time.time()
            )
        else:
            game["status"] = "pending"


def refresh_shot_status(state: Dict[str, Any]) -> None:
    for shot in state["anime_shots"]:
        if not shot.get("path"):
            continue

        path = ROOT / shot["path"]

        if real_file(path):
            shot["status"] = "ready"
            shot["completed_at"] = (
                shot["completed_at"] or time.time()
            )
        else:
            shot["status"] = "pending"


def next_pending_shot(state: Dict[str, Any]):
    for shot in state["anime_shots"]:
        if shot["status"] != "ready":
            return shot

    return None


def run_real_shot_generation(
    state: Dict[str, Any],
    shot: Dict[str, Any],
) -> bool:
    """
    Executes the configured real generation worker.

    The worker receives:
      AJVYRA_SHOT_ID
      AJVYRA_SHOT_OUTPUT

    It MUST write a real media file to AJVYRA_SHOT_OUTPUT.
    """
    if not REAL_SHOT_COMMAND:
        raise RuntimeError(
            "AJVYRA_REAL_SHOT_COMMAND is not configured. "
            "No fake generation will be performed."
        )

    if state.get("generation_lock"):
        return False

    state["generation_lock"] = True
    save_state(state)

    output = (
        SHOT_ROOT /
        f"{shot['asset_id']}.mp4"
    )

    environment = os.environ.copy()
    environment["AJVYRA_SHOT_ID"] = shot["asset_id"]
    environment["AJVYRA_SHOT_OUTPUT"] = str(output)
    environment["AJVYRA_ROOT"] = str(ROOT)

    shot["status"] = "generating"
    shot["created_at"] = time.time()
    shot["error"] = ""
    save_state(state)

    try:
        result = subprocess.run(
            REAL_SHOT_COMMAND,
            shell=True,
            env=environment,
            cwd=ROOT,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Real shot worker exited with code "
                f"{result.returncode}"
            )

        if not real_file(output):
            raise RuntimeError(
                "Worker finished but did not create a "
                "real non-empty media file."
            )

        shot["status"] = "ready"
        shot["path"] = str(
            output.relative_to(ROOT)
        )
        shot["completed_at"] = time.time()

        state["last_hourly_generation"] = time.time()
        save_state(state)

        return True

    except Exception as exc:
        shot["status"] = "failed"
        shot["error"] = str(exc)
        save_state(state)
        return False

    finally:
        state["generation_lock"] = False
        save_state(state)


def production_counts(
    state: Dict[str, Any]
) -> Dict[str, int]:
    games_ready = sum(
        x["status"] == "ready"
        for x in state["games"]
    )

    shots_ready = sum(
        x["status"] == "ready"
        for x in state["anime_shots"]
    )

    return {
        "games_ready": games_ready,
        "games_required": REQUIRED_GAMES,
        "anime_shots_ready": shots_ready,
        "anime_shots_required": REQUIRED_SHOTS,
    }


def pre_release_ready(
    state: Dict[str, Any]
) -> bool:
    counts = production_counts(state)

    return (
        counts["games_ready"] >= REQUIRED_GAMES
        and counts["anime_shots_ready"] >= REQUIRED_SHOTS
    )


def run_hourly_cycle(state: Dict[str, Any]) -> None:
    refresh_game_status(state)
    refresh_shot_status(state)

    if pre_release_ready(state):
        save_state(state)
        return

    now = time.time()
    last = float(
        state.get("last_hourly_generation", 0)
    )

    if now - last < HOURLY_SECONDS:
        save_state(state)
        return

    shot = next_pending_shot(state)

    if shot is None:
        save_state(state)
        return

    run_real_shot_generation(
        state,
        shot,
    )


def print_status(state: Dict[str, Any]) -> None:
    counts = production_counts(state)

    print(
        json.dumps(
            {
                "project": "AJVYRA",
                "pre_release_ready":
                    pre_release_ready(state),
                **counts,
                "last_hourly_generation":
                    state.get(
                        "last_hourly_generation",
                        0,
                    ),
                "next_rule":
                    "one real shot every hour",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> None:
    ensure_dirs()

    state = load_state()
    initialize_slots(state)

    if "--status" in sys.argv:
        refresh_game_status(state)
        refresh_shot_status(state)
        save_state(state)
        print_status(state)
        return

    print(
        "AJVYRA v12 production engine started."
    )
    print(
        "Real generation only; no placeholder media."
    )

    while True:
        state = load_state()

        try:
            run_hourly_cycle(state)
            print_status(state)
        except Exception as exc:
            print(
                f"[AJVYRA] production cycle error: {exc}",
                file=sys.stderr,
            )

        time.sleep(60)


if __name__ == "__main__":
    main()
