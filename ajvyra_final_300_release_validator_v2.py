from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import traceback
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class GameValidation:
    game_id: int
    module: str = ""
    imported: bool = False
    constructed: bool = False
    state_available: bool = False
    actions_available: bool = False
    serializable: bool = False
    errors: list[str] | None = None

    @property
    def passed(self):
        return all([
            self.imported,
            self.constructed,
            self.state_available,
            self.actions_available,
            self.serializable,
            not self.errors,
        ])


class AJVYRA300ReleaseValidator:

    def discover(self):
        found = {}

        for item in pkgutil.iter_modules():
            name = item.name

            if not name.startswith("ajvyra_game_"):
                continue

            try:
                number = int(name.split("_")[2])
            except (ValueError, IndexError):
                continue

            if 1 <= number <= 300:
                found[number] = name

        return found

    def construct(self, module):
        for name in (
            "create_game",
            "build_game",
            "create",
        ):
            fn = getattr(module, name, None)

            if callable(fn):
                return fn()

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module.__name__:
                continue

            try:
                return cls()
            except TypeError:
                continue

        raise RuntimeError("No constructable game")

    def get_state(self, game):
        for name in (
            "status",
            "snapshot",
            "state",
            "to_dict",
        ):
            fn = getattr(game, name, None)

            if callable(fn):
                return fn()

        return vars(game)

    def actions(self, game):
        result = []

        for name in dir(game):
            if name.startswith("_"):
                continue

            fn = getattr(game, name, None)

            if not callable(fn):
                continue

            try:
                sig = inspect.signature(fn)
            except Exception:
                continue

            required = [
                p for p in sig.parameters.values()
                if p.name != "self"
                and p.default is inspect.Parameter.empty
            ]

            if not required:
                result.append(name)

        return result

    def json_safe(self, value):
        json.dumps(value, default=lambda obj: vars(obj))
        return True

    def validate_one(self, game_id, module_name):
        result = GameValidation(
            game_id=game_id,
            module=module_name,
            errors=[],
        )

        try:
            module = importlib.import_module(module_name)
            result.imported = True

            game = self.construct(module)
            result.constructed = True

            state = self.get_state(game)
            result.state_available = state is not None

            actions = self.actions(game)
            result.actions_available = bool(actions)

            self.json_safe(state)
            result.serializable = True

        except Exception as exc:
            result.errors.append(
                f"{type(exc).__name__}: {exc}"
            )

        return result

    def run(self):
        discovered = self.discover()
        results = []

        for game_id in range(1, 301):
            module = discovered.get(game_id)

            if not module:
                results.append(
                    GameValidation(
                        game_id=game_id,
                        errors=["MISSING_GAME_MODULE"],
                    )
                )
                continue

            results.append(
                self.validate_one(game_id, module)
            )

        passed = [
            r.game_id for r in results
            if r.passed
        ]

        failed = [
            r.game_id for r in results
            if not r.passed
        ]

        return {
            "target": 300,
            "discovered": len(discovered),
            "tested": len(results),
            "passed": len(passed),
            "failed": len(failed),
            "missing": [
                r.game_id
                for r in results
                if r.errors == ["MISSING_GAME_MODULE"]
            ],
            "failed_ids": failed,
            "release_ready": len(passed) == 300,
            "games": [asdict(r) for r in results],
        }


if __name__ == "__main__":
    report = AJVYRA300ReleaseValidator().run()

    print(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
    )

    if not report["release_ready"]:
        raise SystemExit(1)
