"""
Builds all 30 browser games.
"""

from pathlib import Path

from ajvyra_browser_game_runtime_v3 import build_all, GAMES


def main() -> int:
    root = Path("generated/ajvyra_release")
    files = build_all(root)

    if len(files) != 30:
        raise RuntimeError("AJVYRA must contain exactly 30 browser games.")

    missing = [str(p) for p in files if not p.exists() or p.stat().st_size < 5000]

    if missing:
        raise RuntimeError(
            "Browser game build incomplete:\n" +
            "\n".join(missing)
        )

    print(f"AJVYRA browser games built: {len(files)}/30")

    for game, path in zip(GAMES, files):
        print(
            f"{game.number:02d} | "
            f"{game.title} | "
            f"{path}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
