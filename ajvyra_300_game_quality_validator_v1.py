from __future__ import annotations

from typing import Any, Dict, List

from ajvyra_game_discovery_loader_v1 import (
    GameDiscoveryLoader,
)
from ajvyra_game_runtime_adapter_v1 import (
    GameRuntimeAdapter,
)


class AJVYRA300GameValidator:
    TARGET = 300

    def __init__(self):
        self.loader = GameDiscoveryLoader()

    def validate(self) -> Dict[str, Any]:
        discovered = self.loader.discover()

        report: List[Dict[str, Any]] = []

        for game in discovered:
            result = self._validate_game(game)
            report.append(result)

        ids = {
            item["game_id"]
            for item in report
        }

        missing = [
            game_id
            for game_id in range(
                1,
                self.TARGET + 1,
            )
            if game_id not in ids
        ]

        passed = [
            item
            for item in report
            if item["passed"]
        ]

        return {
            "target": self.TARGET,
            "discovered": len(discovered),
            "tested": len(report),
            "passed": len(passed),
            "failed": len(report) - len(passed),
            "missing_ids": missing,
            "release_ready": (
                len(report) == self.TARGET
                and not missing
                and len(passed) == self.TARGET
            ),
            "games": report,
        }

    def _validate_game(self, game) -> Dict[str, Any]:
        checks = {
            "module_import": False,
            "runtime_creation": False,
            "state_available": False,
            "action_available": False,
        }

        errors: List[str] = []

        checks["module_import"] = (
            game.module is not None
        )

        try:
            adapter = GameRuntimeAdapter(game)
            checks["runtime_creation"] = (
                adapter.instance is not None
            )

            state = adapter.state()

            checks["state_available"] = (
                isinstance(state, dict)
            )

            actions = [
                name
                for name in dir(adapter.instance)
                if not name.startswith("_")
                and callable(
                    getattr(
                        adapter.instance,
                        name,
                        None,
                    )
                )
            ]

            checks["action_available"] = (
                len(actions) > 0
            )

        except Exception as exc:
            errors.append(str(exc))

        passed = (
            all(checks.values())
            and not errors
        )

        return {
            "game_id": game.game_id,
            "module": game.module_name,
            "title": game.title,
            "checks": checks,
            "errors": errors,
            "passed": passed,
        }


if __name__ == "__main__":
    validator = AJVYRA300GameValidator()
    result = validator.validate()

    print(
        f"AJVYRA validation: "
        f"{result['passed']}/"
        f"{result['target']}"
    )

    print(
        "Release ready:",
        result["release_ready"],
    )
