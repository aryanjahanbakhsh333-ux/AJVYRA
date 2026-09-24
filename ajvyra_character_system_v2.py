from dataclasses import dataclass, field
from typing import Dict, List

from ajvyra_mobile_engine_v2 import GameEntity, Vector2


@dataclass
class Character:
    character_id: str
    name: str
    role: str
    entity: GameEntity
    health: float = 100.0
    max_health: float = 100.0
    speed: float = 180.0
    abilities: List[str] = field(default_factory=list)
    inventory: List[str] = field(default_factory=list)
    relationships: Dict[str, int] = field(default_factory=dict)

    def damage(self, amount: float):
        self.health = max(0.0, self.health - amount)

    def heal(self, amount: float):
        self.health = min(self.max_health, self.health + amount)

    @property
    def alive(self):
        return self.health > 0


class CharacterSystem:
    def __init__(self, game):
        self.game = game
        self.characters: Dict[str, Character] = {}

    def create(
        self,
        character_id,
        name,
        role,
        x,
        y,
        speed=180,
        abilities=None
    ):
        entity = GameEntity(
            entity_id=f"character:{character_id}",
            transform=__import__(
                "ajvyra_mobile_engine_v2",
                fromlist=["Transform"]
            ).Transform(Vector2(x, y)),
            tags={"character"}
        )

        character = Character(
            character_id=character_id,
            name=name,
            role=role,
            entity=entity,
            speed=speed,
            abilities=abilities or []
        )

        self.characters[character_id] = character
        self.game.add_entity(entity)
        return character

    def get(self, character_id):
        return self.characters.get(character_id)

    def move_character(self, character_id, dx, dy, dt):
        character = self.get(character_id)

        if not character or not character.alive:
            return

        direction = Vector2(dx, dy).normalized()

        character.entity.transform.position.x += (
            direction.x * character.speed * dt
        )

        character.entity.transform.position.y += (
            direction.y * character.speed * dt
        )

        from ajvyra_mobile_engine_v2 import CollisionSystem

        CollisionSystem.keep_inside(
            character.entity,
            self.game.width,
            self.game.height,
            20
        )

    def damage(self, character_id, amount):
        character = self.get(character_id)

        if character:
            character.damage(amount)

            if not character.alive:
                self.game.emit(
                    "character_defeated",
                    character_id=character_id
                )
