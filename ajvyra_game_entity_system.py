from dataclasses import dataclass, field
from typing import Dict, List, Optional
import math


@dataclass
class GameEntity:
    entity_id: str
    x: float
    y: float
    width: float = 24
    height: float = 24
    vx: float = 0.0
    vy: float = 0.0
    health: float = 100.0
    max_health: float = 100.0
    active: bool = True
    visible: bool = True
    tags: List[str] = field(default_factory=list)
    data: Dict[str, object] = field(default_factory=dict)

    def distance_to(self, other: "GameEntity") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2
        )

    def damage(self, amount: float):
        if not self.active:
            return

        self.health = max(
            0.0,
            self.health - amount,
        )

        if self.health <= 0:
            self.active = False

    def heal(self, amount: float):
        if not self.active:
            return

        self.health = min(
            self.max_health,
            self.health + amount,
        )

    def move(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt


@dataclass
class Projectile(GameEntity):
    damage_amount: float = 10.0
    lifetime: float = 3.0

    def update(self, dt: float):
        self.move(dt)
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.active = False


class AJVYRAEntitySystem:
    """
    Shared entity lifecycle for every game genre.
    """

    def __init__(self):
        self.entities: Dict[str, GameEntity] = {}
        self.projectiles: Dict[str, Projectile] = {}
        self._counter = 0

    def create_entity(
        self,
        x: float,
        y: float,
        **kwargs,
    ) -> GameEntity:

        self._counter += 1

        entity = GameEntity(
            entity_id=f"entity_{self._counter}",
            x=x,
            y=y,
            **kwargs,
        )

        self.entities[entity.entity_id] = entity

        return entity

    def create_projectile(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        damage: float = 10.0,
    ) -> Projectile:

        self._counter += 1

        projectile = Projectile(
            entity_id=f"projectile_{self._counter}",
            x=x,
            y=y,
            vx=vx,
            vy=vy,
            damage_amount=damage,
        )

        self.projectiles[
            projectile.entity_id
        ] = projectile

        return projectile

    def update(self, dt: float):
        for entity in self.entities.values():
            if entity.active:
                entity.move(dt)

        for projectile in self.projectiles.values():
            if projectile.active:
                projectile.update(dt)

        self.remove_inactive()

    def remove_inactive(self):
        self.entities = {
            key: value
            for key, value in self.entities.items()
            if value.active
        }

        self.projectiles = {
            key: value
            for key, value in self.projectiles.items()
            if value.active
        }

    def get_active_entities(self) -> List[GameEntity]:
        return [
            entity
            for entity in self.entities.values()
            if entity.active
        ]

    def clear(self):
        self.entities.clear()
        self.projectiles.clear()
