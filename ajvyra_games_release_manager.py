from pathlib import Path
import json
import shutil


class AJVYRAGamesReleaseManager:
    """
    Creates the final release structure without modifying
    the source generation files.
    """

    def __init__(
        self,
        source="generated/final_games",
        release="release/ajvyra_games",
    ):
        self.source = Path(source)
        self.release = Path(release)

    def prepare(self):
        if not self.source.exists():
            raise FileNotFoundError(
                f"Source does not exist: {self.source}"
            )

        self.release.mkdir(
            parents=True,
            exist_ok=True,
        )

        games = []

        for directory in sorted(
            self.source.glob("game_*")
        ):
            if not directory.is_dir():
                continue

            metadata = (
                directory /
                "metadata.json"
            )

            if not metadata.exists():
                continue

            data = json.loads(
                metadata.read_text(
                    encoding="utf-8"
                )
            )

            target = (
                self.release /
                directory.name
            )

            if target.exists():
                shutil.rmtree(target)

            shutil.copytree(
                directory,
                target,
            )

            games.append(data)

        manifest = {
            "name": "AJVYRA Games",
            "release": "final",
            "total_games": len(games),
            "games": games,
        }

        (self.release / "release_manifest.json").write_text(
            json.dumps(
                manifest,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return manifest


if __name__ == "__main__":
    manager = AJVYRAGamesReleaseManager()

    result = manager.prepare()

    print(
        json.dumps(
            {
                "release": "ready",
                "games": result["total_games"],
                "directory": str(manager.release),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
