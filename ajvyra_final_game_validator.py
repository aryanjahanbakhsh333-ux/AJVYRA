from pathlib import Path
import json


class AJVYRAFinalGameValidator:

    REQUIRED_FILES = (
        "index.html",
        "game.js",
        "game.css",
        "metadata.json",
    )

    REQUIRED_JS_MARKERS = (
        "requestAnimationFrame",
        "localStorage",
        "function update",
        "function draw",
        "function win",
        "function lose",
    )

    def validate_game(self, directory: str):
        root = Path(directory)
        errors = []

        if not root.exists():
            return {
                "valid": False,
                "errors": ["Game directory does not exist."],
            }

        for filename in self.REQUIRED_FILES:
            if not (root / filename).is_file():
                errors.append(
                    f"Missing file: {filename}"
                )

        metadata = root / "metadata.json"

        if metadata.exists():
            try:
                data = json.loads(
                    metadata.read_text(
                        encoding="utf-8"
                    )
                )

                if not data.get("playable"):
                    errors.append(
                        "metadata.playable is false."
                    )

                if not data.get("genre"):
                    errors.append(
                        "Missing genre."
                    )

                if not data.get("title"):
                    errors.append(
                        "Missing title."
                    )

            except Exception as exc:
                errors.append(
                    f"Invalid metadata: {exc}"
                )

        js = root / "game.js"

        if js.exists():
            content = js.read_text(
                encoding="utf-8"
            )

            for marker in self.REQUIRED_JS_MARKERS:
                if marker not in content:
                    errors.append(
                        f"Missing runtime marker: {marker}"
                    )

        return {
            "valid": not errors,
            "errors": errors,
            "directory": str(root),
        }

    def validate_all(
        self,
        root_directory: str,
        expected: int = 70,
    ):
        root = Path(root_directory)

        results = []

        for game_id in range(1, expected + 1):
            directory = (
                root / f"game_{game_id:02d}"
            )

            result = self.validate_game(
                str(directory)
            )

            result["game_id"] = game_id
            results.append(result)

        valid = [
            result
            for result in results
            if result["valid"]
        ]

        return {
            "expected": expected,
            "valid": len(valid),
            "invalid": expected - len(valid),
            "all_valid": len(valid) == expected,
            "results": results,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--root",
        default="generated/final_games",
    )

    args = parser.parse_args()

    validator = AJVYRAFinalGameValidator()

    result = validator.validate_all(
        args.root
    )

    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )
