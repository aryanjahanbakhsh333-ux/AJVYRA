from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable


@dataclass
class GameAction:
    name: str
    callable_name: str
    label: str
    category: str = "gameplay"


@dataclass
class GameFrame:
    game_id: int
    title: str
    state: dict[str, Any]
    actions: list[dict[str, Any]]
    elapsed: float
    completed: bool
    failed: bool


@dataclass
class RuntimeSession:
    game_id: int
    game: Any
    started_at: float = field(default_factory=time.time)
    actions: int = 0


class FinalBrowserGameRuntime:
    PREFIXES = ("ajvyra_game_",)

    def __init__(self):
        self.sessions: dict[str, RuntimeSession] = {}

    def discover(self) -> list[int]:
        ids = set()

        for module in pkgutil.iter_modules():
            name = module.name
            if not name.startswith(self.PREFIXES):
                continue

            parts = name.split("_")
            try:
                number = int(parts[2])
                if 1 <= number <= 300:
                    ids.add(number)
            except (ValueError, IndexError):
                continue

        return sorted(ids)

    def import_game(self, game_id: int):
        candidates = [
            f"ajvyra_game_{game_id:03d}",
        ]

        for prefix in candidates:
            modules = [
                prefix,
                f"{prefix}_v2",
                f"{prefix}_v3",
            ]

            for module_name in modules:
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    pass

        for module_name in self._possible_modules(game_id):
            try:
                return importlib.import_module(module_name)
            except ImportError:
                continue

        raise ModuleNotFoundError(f"Game {game_id} was not found")

    def _possible_modules(self, game_id: int):
        needle = f"ajvyra_game_{game_id:03d}_"
        return [
            name
            for name in (
                m.name for m in pkgutil.iter_modules()
            )
            if name.startswith(needle)
        ]

    def create(self, game_id: int) -> RuntimeSession:
        module = self.import_game(game_id)
        game = self._construct(module)

        session_id = f"{game_id}-{int(time.time() * 1000)}"
        session = RuntimeSession(game_id=game_id, game=game)
        self.sessions[session_id] = session

        return session

    def _construct(self, module):
        for function_name in (
            "create_game",
            "build_game",
            "create",
        ):
            fn = getattr(module, function_name, None)
            if callable(fn):
                return fn()

        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != module.__name__:
                continue

            try:
                return cls()
            except TypeError:
                continue

        raise RuntimeError(f"No constructable game found in {module.__name__}")

    def actions(self, game: Any) -> list[GameAction]:
        blocked = {
            "status",
            "snapshot",
            "state",
            "to_dict",
            "serialize",
            "export",
        }

        actions = []

        for name in dir(game):
            if name.startswith("_") or name in blocked:
                continue

            try:
                fn = getattr(game, name)
            except Exception:
                continue

            if not callable(fn):
                continue

            try:
                signature = inspect.signature(fn)
            except (ValueError, TypeError):
                continue

            required = [
                p for p in signature.parameters.values()
                if p.name != "self"
                and p.default is inspect.Parameter.empty
                and p.kind in (
                    inspect.Parameter.POSITIONAL_ONLY,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                )
            ]

            # Browser action buttons can safely call zero-argument methods.
            if required:
                continue

            label = name.replace("_", " ").title()
            actions.append(
                GameAction(
                    name=name,
                    callable_name=name,
                    label=label,
                )
            )

        return actions

    def state(self, game: Any) -> dict[str, Any]:
        for name in ("status", "snapshot", "state", "to_dict"):
            fn = getattr(game, name, None)
            if callable(fn):
                try:
                    value = fn()
                    return self._json_safe(value)
                except Exception:
                    pass

        result = {}
        for key, value in vars(game).items():
            if key.startswith("_"):
                continue
            result[key] = self._json_safe(value)

        return result

    def _json_safe(self, value):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, dict):
            return {
                str(k): self._json_safe(v)
                for k, v in value.items()
            }

        if isinstance(value, (list, tuple, set)):
            return [self._json_safe(v) for v in value]

        if hasattr(value, "__dataclass_fields__"):
            return self._json_safe(asdict(value))

        if hasattr(value, "__dict__"):
            return self._json_safe(vars(value))

        return str(value)

    def execute(self, session: RuntimeSession, action: str):
        fn = getattr(session.game, action, None)

        if not callable(fn):
            raise ValueError(f"Unknown action: {action}")

        result = fn()
        session.actions += 1

        return {
            "result": self._json_safe(result),
            "state": self.state(session.game),
        }

    def frame(self, session: RuntimeSession) -> GameFrame:
        state = self.state(session.game)

        return GameFrame(
            game_id=session.game_id,
            title=self._title(session.game, session.game_id),
            state=state,
            actions=[
                asdict(action)
                for action in self.actions(session.game)
            ],
            elapsed=time.time() - session.started_at,
            completed=self._is_completed(state),
            failed=self._is_failed(state),
        )

    def _title(self, game, game_id):
        for attr in ("title", "name", "game_name"):
            value = getattr(game, attr, None)
            if isinstance(value, str) and value.strip():
                return value

        return f"AJVYRA Game {game_id:03d}"

    def _is_completed(self, state):
        keys = (
            "completed",
            "finished",
            "won",
            "escaped",
            "case_solved",
            "mission_complete",
            "expedition_complete",
            "returned",
            "rescued",
        )

        return any(state.get(k) is True for k in keys)

    def _is_failed(self, state):
        keys = ("failed", "game_over", "lost", "dead")
        return any(state.get(k) is True for k in keys)


runtime = FinalBrowserGameRuntime()
