from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple


@dataclass
class Vector2:
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, value: float):
        return Vector2(self.x * value, self.y * value)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        length = self.length()
        if length <= 0:
            return Vector2()
        return Vector2(self.x / length, self.y / length)

    def distance_to(self, other):
        return (self - other).length()


@dataclass
class Transform:
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: Vector2 = field(default_factory=lambda: Vector2(1, 1))


@dataclass
class GameEntity:
    entity_id: str
    transform: Transform = field(default_factory=Transform)
    active: bool = True
    tags: set = field(default_factory=set)
    data: Dict[str, Any] = field(default_factory=dict)

    def distance_to(self, other: "GameEntity") -> float:
        return self.transform.position.distance_to(other.transform.position)


@dataclass
class PlayerStats:
    health: float = 100.0
    max_health: float = 100.0
    energy: float = 100.0
    max_energy: float = 100.0
    score: int = 0
    coins: int = 0
    level: int = 1


class InputState:
    def __init__(self):
        self.keys: set[str] = set()
        self.touches: Dict[int, Vector2] = {}
        self.buttons: set[str] = set()

    def press_key(self, key: str):
        self.keys.add(key.lower())

    def release_key(self, key: str):
        self.keys.discard(key.lower())

    def press_button(self, button: str):
        self.buttons.add(button)

    def release_button(self, button: str):
        self.buttons.discard(button)

    def touch_down(self, pointer_id: int, x: float, y: float):
        self.touches[pointer_id] = Vector2(x, y)

    def touch_up(self, pointer_id: int):
        self.touches.pop(pointer_id, None)

    def axis(self, horizontal=True):
        negative = {"a", "left"} if horizontal else {"w", "up"}
        positive = {"d", "right"} if horizontal else {"s", "down"}

        value = 0.0

        if self.keys.intersection(negative):
            value -= 1.0

        if self.keys.intersection(positive):
            value += 1.0

        return max(-1.0, min(1.0, value))

    def action(self, *names):
        return any(
            name.lower() in self.keys or name in self.buttons
            for name in names
        )


class CollisionSystem:
    @staticmethod
    def circle_collision(a: GameEntity, radius_a: float,
                         b: GameEntity, radius_b: float) -> bool:
        return a.distance_to(b) <= radius_a + radius_b

    @staticmethod
    def keep_inside(entity: GameEntity, width: float, height: float,
                    radius: float = 0.0):
        entity.transform.position.x = max(
            radius,
            min(width - radius, entity.transform.position.x)
        )
        entity.transform.position.y = max(
            radius,
            min(height - radius, entity.transform.position.y)
        )


class Timer:
    def __init__(self):
        self.started = time.monotonic()

    def elapsed(self):
        return time.monotonic() - self.started


class MobileGame:
    def __init__(self, width=960, height=540):
        self.width = width
        self.height = height
        self.input = InputState()
        self.entities: Dict[str, GameEntity] = {}
        self.stats = PlayerStats()
        self.running = False
        self.paused = False
        self.elapsed_time = 0.0
        self.random = random.Random()
        self.events: List[Dict[str, Any]] = []
        self.state: Dict[str, Any] = {}

    def add_entity(self, entity: GameEntity):
        self.entities[entity.entity_id] = entity
        return entity

    def remove_entity(self, entity_id: str):
        self.entities.pop(entity_id, None)

    def get_entity(self, entity_id: str):
        return self.entities.get(entity_id)

    def emit(self, event: str, **payload):
        self.events.append({
            "event": event,
            "payload": payload,
            "time": self.elapsed_time
        })

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def update(self, dt: float):
        if not self.running or self.paused:
            return

        dt = max(0.0, min(dt, 0.1))
        self.elapsed_time += dt
        self.events.clear()
        self.update_game(dt)

    def update_game(self, dt: float):
        pass

    def snapshot(self):
        return {
            "time": self.elapsed_time,
            "score": self.stats.score,
            "coins": self.stats.coins,
            "health": self.stats.health,
            "level": self.stats.level,
            "state": self.state.copy(),
            "entities": {
                entity_id: {
                    "x": entity.transform.position.x,
                    "y": entity.transform.position.y,
                    "rotation": entity.transform.rotation,
                    "active": entity.active,
                    "tags": list(entity.tags),
                    "data": entity.data.copy()
                }
                for entity_id, entity in self.entities.items()
                if entity.active
            }
        }
