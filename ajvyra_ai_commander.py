from dataclasses import dataclass, field
from typing import Any


@dataclass
class AICommand:
    action: str
    payload: dict[str, Any] = field(default_factory=dict)
    priority: int = 100


class AJVYRAAICommander:
    """
    فرمانده مرکزی AJVYRA.
    تمام بخش‌های موتور از این لایه فرمان می‌گیرند.
    """

    def __init__(self):
        self.modules: dict[str, Any] = {}
        self.history: list[AICommand] = []

    def register(self, name: str, module: Any) -> None:
        self.modules[name] = module

    def command(
        self,
        action: str,
        payload: dict[str, Any] | None = None,
        priority: int = 100,
    ) -> Any:

        command = AICommand(
            action=action,
            payload=payload or {},
            priority=priority,
        )

        self.history.append(command)

        if action not in self.modules:
            raise KeyError(
                f"AJVYRA module is not registered: {action}"
            )

        module = self.modules[action]

        if callable(module):
            return module(**command.payload)

        if hasattr(module, "execute"):
            return module.execute(**command.payload)

        raise TypeError(
            f"Module '{action}' cannot execute commands."
        )

    def status(self) -> dict[str, Any]:
        return {
            "commander": "online",
            "modules": sorted(self.modules.keys()),
            "commands_executed": len(self.history),
        }
