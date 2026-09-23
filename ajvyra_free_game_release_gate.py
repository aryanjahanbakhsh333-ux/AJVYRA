from __future__ import annotations

import ast
from pathlib import Path


class GameReleaseGate:

    def __init__(
        self,
        root: Path
    ):
        self.root = root

    def check(self):

        file = (
            self.root
            / "ajvyra_30_games.py"
        )

        if not file.exists():
            return {
                "ready": False,
                "total": 0,
                "errors": [
                    "ajvyra_30_games.py is missing"
                ]
            }

        try:

            source = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(
                source
            )

        except Exception as exc:

            return {
                "ready": False,
                "total": 0,
                "errors": [
                    str(exc)
                ]
            }

        numbers = set()

        for node in ast.walk(tree):

            if not isinstance(
                node,
                ast.Call
            ):
                continue

            if not isinstance(
                node.func,
                ast.Name
            ):
                continue

            if node.func.id != "GameInfo":
                continue

            if not node.args:
                continue

            value = node.args[0]

            if (
                isinstance(
                    value,
                    ast.Constant
                )
                and isinstance(
                    value.value,
                    int
                )
            ):
                numbers.add(
                    value.value
                )

        expected = set(
            range(1, 31)
        )

        errors = []

        if numbers != expected:
            errors.append(
                "The game catalog does not contain "
                "exactly games 1..30."
            )

        return {
            "ready": not errors,
            "total": len(numbers),
            "errors": errors
        }
