from __future__ import annotations

import inspect


ALIASES = {
    "primary": (
        "attack", "strike", "shoot", "serve", "cast",
        "explore", "drive", "sprint", "move",
    ),
    "secondary": (
        "defend", "guard", "repair", "rest", "recover",
        "scan", "study", "train",
    ),
    "utility": (
        "upgrade", "build", "collect", "search",
        "refuel", "recharge", "sell", "buy",
    ),
    "finish": (
        "finish", "complete", "escape", "win",
        "return", "land", "open_final_gate",
    ),
}


class GameplayAdapter:
    def __init__(self, game):
        self.game = game

    def available_actions(self):
        actions = []

        for name in dir(self.game):
            if name.startswith("_"):
                continue

            fn = getattr(self.game, name, None)

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
                actions.append(name)

        return actions

    def controls(self):
        available = set(self.available_actions())
        result = {}

        for category, names in ALIASES.items():
            for name in names:
                if name in available:
                    result[category] = name
                    break

        return result

    def invoke(self, action):
        fn = getattr(self.game, action, None)

        if not callable(fn):
            raise ValueError(f"Action unavailable: {action}")

        return fn()
