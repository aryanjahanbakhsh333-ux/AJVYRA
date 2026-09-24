from enum import Enum
from typing import Optional

from ajvyra_mobile_engine_v2 import Vector2


class AIState(Enum):
    IDLE = "idle"
    PATROL = "patrol"
    CHASE = "chase"
    ATTACK = "attack"
    FLEE = "flee"


class SimpleCombatAI:
    def __init__(
        self,
        game,
        entity,
        target,
        speed=90.0,
        detection_range=220.0,
        attack_range=45.0
    ):
        self.game = game
        self.entity = entity
        self.target = target
        self.speed = speed
        self.detection_range = detection_range
        self.attack_range = attack_range
        self.state = AIState.IDLE
        self.attack_cooldown = 0.0

    def update(self, dt):
        if not self.entity.active or not self.target.active:
            return

        distance = self.entity.distance_to(self.target)

        if distance <= self.attack_range:
            self.state = AIState.ATTACK

        elif distance <= self.detection_range:
            self.state = AIState.CHASE

        else:
            self.state = AIState.PATROL

        if self.state == AIState.CHASE:
            direction = (
                self.target.transform.position -
                self.entity.transform.position
            ).normalized()

            self.entity.transform.position.x += (
                direction.x * self.speed * dt
            )

            self.entity.transform.position.y += (
                direction.y * self.speed * dt
            )

        elif self.state == AIState.ATTACK:
            self.attack_cooldown -= dt

            if self.attack_cooldown <= 0:
                self.attack_cooldown = 1.0
                self.game.emit(
                    "ai_attack",
                    attacker=self.entity.entity_id,
                    target=self.target.entity_id
                )
