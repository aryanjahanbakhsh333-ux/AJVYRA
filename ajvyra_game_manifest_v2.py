from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CharacterDefinition:
    character_id: str
    name: str
    role: str
    description: str
    abilities: List[str] = field(default_factory=list)


@dataclass
class GameDefinition:
    game_id: str
    title: str
    genre: str
    description: str
    story: str
    objective: str
    controls: Dict[str, str]
    characters: List[CharacterDefinition]
    mechanics: List[str]
    chapters: List[str]
    mobile: bool = True
    desktop: bool = True


GAME_DEFINITIONS: Dict[str, GameDefinition] = {}


def register_game(game: GameDefinition):
    if game.game_id in GAME_DEFINITIONS:
        raise ValueError(f"Duplicate game id: {game.game_id}")

    GAME_DEFINITIONS[game.game_id] = game
    return game


def get_game(game_id: str) -> Optional[GameDefinition]:
    return GAME_DEFINITIONS.get(game_id)


def all_games():
    return list(GAME_DEFINITIONS.values())


def game_count():
    return len(GAME_DEFINITIONS)
