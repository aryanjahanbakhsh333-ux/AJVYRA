"""
AJVYRA REAL EXECUTION ENGINE
============================

A real execution runtime for AJVYRA.

Purpose:
    - Turn an AJVYRA game specification into a playable HTML5 game.
    - Provide a reusable runtime for all 70 games.
    - Support keyboard + touch controls.
    - Player movement.
    - Enemies.
    - Collision detection.
    - Health.
    - Score.
    - Levels.
    - Objectives.
    - Win / lose states.
    - Pause / restart.
    - Local save.
    - Mobile-friendly canvas.
    - Game metadata.
    - Optional connection to the existing AJVYRA AI systems.

This engine intentionally generates self-contained browser games.

No external JavaScript framework is required.
"""

from __future__ import annotations

import json
import math
import random
import time

from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# CONFIG
# ============================================================

@dataclass
class ExecutionConfig:
    width: int = 960
    height: int = 540

    target_fps: int = 60

    default_player_hp: int = 100

    default_enemy_count: int = 8

    default_level_count: int = 5

    enable_touch: bool = True

    enable_keyboard: bool = True

    enable_save: bool = True

    enable_audio: bool = True

    enable_particles: bool = True

    auto_start: bool = True


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class GamePlayer:
    name: str = "Player"
    hp: int = 100
    max_hp: int = 100
    speed: float = 240.0
    size: float = 24.0


@dataclass
class GameEnemy:
    enemy_id: str
    name: str
    x: float
    y: float
    hp: int
    max_hp: int
    speed: float
    damage: int
    size: float


@dataclass
class GameLevel:
    number: int
    name: str
    objective: str
    enemy_count: int
    difficulty: float


@dataclass
class GameSpec:
    game_id: str
    title: str
    genre: str

    story: str = ""

    player_name: str = "Player"

    levels: List[GameLevel] = field(
        default_factory=list
    )

    enemies: List[GameEnemy] = field(
        default_factory=list
    )

    player: Optional[GamePlayer] = None

    width: int = 960
    height: int = 540


# ============================================================
# ENGINE
# ============================================================

class AJVYRARealExecutionEngine:

    VERSION = "1.0.0"

    def __init__(
        self,
        root: str | Path = ".",
        config: ExecutionConfig | None = None,
    ) -> None:

        self.root = Path(root).resolve()

        self.config = (
            config
            or ExecutionConfig()
        )

        self.generated_root = (
            self.root
            / "generated"
            / "games"
        )

        self.generated_root.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.runtime_root = (
            self.root
            / "runtime"
            / "execution_engine"
        )

        self.runtime_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ========================================================
    # PUBLIC API
    # ========================================================

    def build_game(
        self,
        spec: Dict[str, Any] | GameSpec,
    ) -> Dict[str, Any]:

        spec = self.normalize_spec(
            spec
        )

        game_dir = (
            self.generated_root
            / spec.game_id
        )

        game_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        assets_dir = (
            game_dir
            / "assets"
        )

        assets_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        files = {}

        files["index.html"] = (
            self._build_html(
                spec
            )
        )

        files["game.js"] = (
            self._build_javascript(
                spec
            )
        )

        files["game.css"] = (
            self._build_css(
                spec
            )
        )

        files["metadata.json"] = (
            json.dumps(
                self._metadata(
                    spec
                ),
                ensure_ascii=False,
                indent=2,
            )
        )

        for filename, content in files.items():

            path = (
                game_dir
                / filename
            )

            path.write_text(
                content,
                encoding="utf-8",
            )

        return {
            "status": "built",
            "game_id": spec.game_id,
            "title": spec.title,
            "genre": spec.genre,
            "directory": str(
                game_dir
            ),
            "play_file": str(
                game_dir
                / "index.html"
            ),
            "files": list(
                files.keys()
            ),
        }

    def build_game_from_ai(
        self,
        game_number: int,
    ) -> Dict[str, Any]:

        spec = (
            self._load_ai_game_spec(
                game_number
            )
        )

        return self.build_game(
            spec
        )

    def build_all_games(
        self,
        count: int = 70,
    ) -> Dict[str, Any]:

        results = []

        for number in range(
            1,
            count + 1,
        ):

            try:

                result = (
                    self.build_game_from_ai(
                        number
                    )
                )

                results.append(
                    result
                )

            except Exception as exc:

                results.append(
                    {
                        "status": "failed",
                        "game_number": number,
                        "error": str(exc),
                    }
                )

        return {
            "status": "completed",
            "target": count,
            "built": sum(
                1
                for result in results
                if result.get(
                    "status"
                )
                == "built"
            ),
            "failed": sum(
                1
                for result in results
                if result.get(
                    "status"
                )
                == "failed"
            ),
            "games": results,
        }

    # ========================================================
    # SPEC NORMALIZATION
    # ========================================================

    def normalize_spec(
        self,
        raw: Dict[str, Any] | GameSpec,
    ) -> GameSpec:

        if isinstance(
            raw,
            GameSpec,
        ):
            return raw

        game_id = str(
            raw.get(
                "game_id",
                raw.get(
                    "id",
                    "game_01",
                ),
            )
        )

        title = str(
            raw.get(
                "title",
                "AJVYRA Game",
            )
        )

        genre = str(
            raw.get(
                "genre",
                "Action",
            )
        )

        story = str(
            raw.get(
                "story",
                "",
            )
        )

        player_data = (
            raw.get(
                "player"
            )
            or {}
        )

        player = GamePlayer(
            name=str(
                player_data.get(
                    "name",
                    raw.get(
                        "player_name",
                        "Player",
                    ),
                )
            ),
            hp=int(
                player_data.get(
                    "hp",
                    self.config.default_player_hp,
                )
            ),
            max_hp=int(
                player_data.get(
                    "max_hp",
                    self.config.default_player_hp,
                )
            ),
            speed=float(
                player_data.get(
                    "speed",
                    240,
                )
            ),
            size=float(
                player_data.get(
                    "size",
                    24,
                )
            ),
        )

        levels = []

        raw_levels = raw.get(
            "levels",
            []
        )

        if not raw_levels:

            raw_levels = [
                {
                    "number": i,
                    "name": f"Level {i}",
                    "objective": (
                        "Defeat all enemies"
                    ),
                    "enemy_count": (
                        self.config.default_enemy_count
                        + i - 1
                    ),
                    "difficulty": (
                        1.0
                        + (
                            (i - 1)
                            * 0.18
                        )
                    ),
                }
                for i in range(
                    1,
                    self.config.default_level_count
                    + 1,
                )
            ]

        for index, level in enumerate(
            raw_levels,
            start=1,
        ):

            levels.append(
                GameLevel(
                    number=int(
                        level.get(
                            "number",
                            index,
                        )
                    ),
                    name=str(
                        level.get(
                            "name",
                            f"Level {index}",
                        )
                    ),
                    objective=str(
                        level.get(
                            "objective",
                            "Defeat all enemies",
                        )
                    ),
                    enemy_count=int(
                        level.get(
                            "enemy_count",
                            self.config.default_enemy_count,
                        )
                    ),
                    difficulty=float(
                        level.get(
                            "difficulty",
                            1.0,
                        )
                    ),
                )
            )

        enemies = []

        raw_enemies = raw.get(
            "enemies",
            []
        )

        if not raw_enemies:

            raw_enemies = [
                {
                    "enemy_id": (
                        f"enemy_{i:02d}"
                    ),
                    "name": "Shadow",
                    "hp": 40,
                    "speed": 70,
                    "damage": 10,
                    "size": 20,
                }
                for i in range(
                    1,
                    self.config.default_enemy_count
                    + 1,
                )
            ]

        for index, enemy in enumerate(
            raw_enemies,
            start=1,
        ):

            enemies.append(
                GameEnemy(
                    enemy_id=str(
                        enemy.get(
                            "enemy_id",
                            f"enemy_{index:02d}",
                        )
                    ),
                    name=str(
                        enemy.get(
                            "name",
                            "Enemy",
                        )
                    ),
                    x=float(
                        enemy.get(
                            "x",
                            random.randint(
                                50,
                                self.config.width
                                - 50,
                            ),
                        )
                    ),
                    y=float(
                        enemy.get(
                            "y",
                            random.randint(
                                50,
                                self.config.height
                                - 50,
                            ),
                        )
                    ),
                    hp=int(
                        enemy.get(
                            "hp",
                            40,
                        )
                    ),
                    max_hp=int(
                        enemy.get(
                            "max_hp",
                            enemy.get(
                                "hp",
                                40,
                            )
                        )
                    ),
                    speed=float(
                        enemy.get(
                            "speed",
                            70,
                        )
                    ),
                    damage=int(
                        enemy.get(
                            "damage",
                            10,
                        )
                    ),
                    size=float(
                        enemy.get(
                            "size",
                            20,
                        )
                    ),
                )
            )

        return GameSpec(
            game_id=game_id,
            title=title,
            genre=genre,
            story=story,
            player_name=player.name,
            levels=levels,
            enemies=enemies,
            player=player,
            width=int(
                raw.get(
                    "width",
                    self.config.width,
                )
            ),
            height=int(
                raw.get(
                    "height",
                    self.config.height,
                )
            ),
        )

    # ========================================================
    # AI SPEC LOADER
    # ========================================================

    def _load_ai_game_spec(
        self,
        number: int,
    ) -> Dict[str, Any]:

        game_id = (
            f"game_{number:02d}"
        )

        possible_paths = [

            self.root
            / "generated"
            / "games"
            / game_id
            / "creative_spec.json",

            self.root
            / "generated"
            / "game"
            / game_id
            / "creative_spec.json",

            self.root
            / "runtime"
            / "games"
            / game_id
            / "creative_spec.json",

        ]

        for path in possible_paths:

            if not path.exists():
                continue

            try:

                data = json.loads(
                    path.read_text(
                        encoding="utf-8"
                    )
                )

                data.setdefault(
                    "game_id",
                    game_id,
                )

                return data

            except Exception:
                pass

        # ----------------------------------------------------
        # Try existing content director
        # ----------------------------------------------------

        try:

            from ajvyra_ai_content_director import (
                AJVYRAAIContentDirector
            )

            director = (
                AJVYRAAIContentDirector(
                    self.root
                )
            )

            method = getattr(
                director,
                "create_game_spec",
                None,
            )

            if callable(method):

                return method(
                    number
                )

        except Exception:
            pass

        # ----------------------------------------------------
        # Safe fallback
        # ----------------------------------------------------

        return {
            "game_id": game_id,
            "title": (
                f"AJVYRA Game {number:02d}"
            ),
            "genre": (
                "Action"
            ),
            "story": (
                "An original AJVYRA adventure."
            ),
            "player": {
                "name": "AJVYRA",
                "hp": 100,
                "max_hp": 100,
                "speed": 240,
                "size": 24,
            },
        }

    # ========================================================
    # HTML
    # ========================================================

    def _build_html(
        self,
        spec: GameSpec,
    ) -> str:

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<title>{self._escape_html(spec.title)}</title>

<link
    rel="stylesheet"
    href="game.css"
>

</head>

<body>

<div id="game-shell">

    <header id="top-bar">

        <div id="game-title">
            {self._escape_html(spec.title)}
        </div>

        <div id="hud">

            <span>
                HP:
                <strong id="hp-value">
                    100
                </strong>
            </span>

            <span>
                SCORE:
                <strong id="score-value">
                    0
                </strong>
            </span>

            <span>
                LEVEL:
                <strong id="level-value">
                    1
                </strong>
            </span>

        </div>

    </header>

    <main id="game-container">

        <canvas
            id="game"
            width="{spec.width}"
            height="{spec.height}"
        ></canvas>

        <div
            id="message"
            class="hidden"
        ></div>

        <div
            id="mobile-controls"
        >

            <button
                data-key="ArrowUp"
                class="control up"
            >
                ▲
            </button>

            <button
                data-key="ArrowLeft"
                class="control left"
            >
                ◀
            </button>

            <button
                data-key="ArrowDown"
                class="control down"
            >
                ▼
            </button>

            <button
                data-key="ArrowRight"
                class="control right"
            >
                ▶
            </button>

            <button
                id="attack-button"
                class="attack"
            >
                ATTACK
            </button>

        </div>

    </main>

    <footer id="bottom-bar">

        <button id="pause-button">
            PAUSE
        </button>

        <button id="restart-button">
            RESTART
        </button>

        <span id="objective">
            Defeat all enemies
        </span>

    </footer>

</div>

<script src="game.js"></script>

</body>
</html>
"""

    # ========================================================
    # CSS
    # ========================================================

    def _build_css(
        self,
        spec: GameSpec,
    ) -> str:

        return """
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html,
body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050509;
    color: #ffffff;
    font-family:
        Arial,
        Helvetica,
        sans-serif;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
}

#game-shell {
    width: 100%;
    max-width: 1100px;
    height: 100%;
    max-height: 800px;
    display: flex;
    flex-direction: column;
    background: #08080e;
}

#top-bar {
    min-height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 14px;
    background: #0d0d16;
    border-bottom: 1px solid #24243a;
}

#game-title {
    font-weight: 800;
    letter-spacing: 1px;
    font-size: 15px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

#hud {
    display: flex;
    gap: 14px;
    font-size: 12px;
}

#game-container {
    position: relative;
    flex: 1;
    min-height: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background:
        radial-gradient(
            circle at center,
            #161629 0%,
            #07070c 70%
        );
}

#game {
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    touch-action: none;
    display: block;
}

#bottom-bar {
    min-height: 52px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px;
    background: #0d0d16;
    border-top: 1px solid #24243a;
}

#bottom-bar button {
    background: #171725;
    color: white;
    border: 1px solid #34344c;
    border-radius: 8px;
    padding: 9px 13px;
    cursor: pointer;
}

#objective {
    margin-left: auto;
    opacity: .8;
    font-size: 12px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

#message {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    padding: 25px 35px;
    border-radius: 14px;
    background: rgba(0, 0, 0, .88);
    border: 1px solid #555577;
    text-align: center;
    font-size: 22px;
    font-weight: 800;
    z-index: 10;
}

.hidden {
    display: none !important;
}

#mobile-controls {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 12px;
    height: 150px;
    pointer-events: none;
    display: none;
}

.control,
.attack {
    position: absolute;
    width: 58px;
    height: 58px;
    border-radius: 50%;
    border: 1px solid #777799;
    background: rgba(20, 20, 35, .82);
    color: white;
    font-size: 20px;
    pointer-events: auto;
    touch-action: none;
}

.up {
    left: 78px;
    bottom: 72px;
}

.left {
    left: 15px;
    bottom: 10px;
}

.down {
    left: 78px;
    bottom: 10px;
}

.right {
    left: 141px;
    bottom: 10px;
}

.attack {
    right: 25px;
    bottom: 38px;
    width: 86px;
    height: 86px;
    font-size: 12px;
}

@media (max-width: 700px) {

    #top-bar {
        min-height: 44px;
    }

    #hud {
        gap: 7px;
        font-size: 10px;
    }

    #mobile-controls {
        display: block;
    }

    #bottom-bar {
        min-height: 44px;
    }

    #objective {
        display: none;
    }

    #bottom-bar button {
        padding: 7px 10px;
        font-size: 11px;
    }
}

@media (pointer: coarse) {

    #mobile-controls {
        display: block;
    }
}
"""

    # ========================================================
    # JAVASCRIPT
    # ========================================================

    def _build_javascript(
        self,
        spec: GameSpec,
    ) -> str:

        config_json = json.dumps(
            {
                "gameId": spec.game_id,
                "title": spec.title,
                "genre": spec.genre,
                "width": spec.width,
                "height": spec.height,
                "player": asdict(
                    spec.player
                ),
                "levels": [
                    asdict(
                        level
                    )
                    for level in spec.levels
                ],
                "enemies": [
                    asdict(
                        enemy
                    )
                    for enemy in spec.enemies
                ],
                "enableSave": (
                    self.config.enable_save
                ),
                "enableAudio": (
                    self.config.enable_audio
                ),
            },
            ensure_ascii=False,
        )

        return f"""
"use strict";

/*
 AJVYRA REAL GAME RUNTIME

 This is the actual browser-side game loop.

 Core:
     input
     ↓
     update
     ↓
     collision
     ↓
     combat
     ↓
     level
     ↓
     render
*/

const AJVYRA_CONFIG = {config_json};

const canvas =
    document.getElementById("game");

const ctx =
    canvas.getContext("2d");

const message =
    document.getElementById("message");

const hpValue =
    document.getElementById("hp-value");

const scoreValue =
    document.getElementById("score-value");

const levelValue =
    document.getElementById("level-value");

const objective =
    document.getElementById("objective");

const pauseButton =
    document.getElementById("pause-button");

const restartButton =
    document.getElementById("restart-button");


// ============================================================
// GAME STATE
// ============================================================

const state = {{

    running: true,

    paused: false,

    finished: false,

    won: false,

    lastTime: performance.now(),

    score: 0,

    level: 1,

    enemiesDefeated: 0,

    particles: [],

    keys: {{}},

    attackPressed: false,

    player: {{

        x: AJVYRA_CONFIG.width / 2,

        y: AJVYRA_CONFIG.height / 2,

        hp: AJVYRA_CONFIG.player.max_hp,

        maxHp: AJVYRA_CONFIG.player.max_hp,

        speed: AJVYRA_CONFIG.player.speed,

        size: AJVYRA_CONFIG.player.size,

        attackCooldown: 0,

        invulnerable: 0

    }},

    enemies: []

}};


// ============================================================
// UTILITIES
// ============================================================

function clamp(
    value,
    min,
    max
) {{

    return Math.max(
        min,
        Math.min(
            max,
            value
        )
    );
}}

function distance(
    a,
    b
) {{

    const dx =
        a.x - b.x;

    const dy =
        a.y - b.y;

    return Math.sqrt(
        dx * dx +
        dy * dy
    );
}}

function randomRange(
    min,
    max
) {{

    return (
        Math.random()
        * (max - min)
        + min
    );
}}


// ============================================================
// SAVE
// ============================================================

function saveGame() {{

    if (!AJVYRA_CONFIG.enableSave) {{
        return;
    }}

    const saveData = {{

        score: state.score,

        level: state.level,

        hp: state.player.hp,

        enemiesDefeated:
            state.enemiesDefeated,

        timestamp:
            Date.now()

    }};

    localStorage.setItem(
        "AJVYRA_" +
        AJVYRA_CONFIG.gameId,
        JSON.stringify(
            saveData
        )
    );
}}

function loadGame() {{

    if (!AJVYRA_CONFIG.enableSave) {{
        return;
    }}

    try {{

        const raw =
            localStorage.getItem(
                "AJVYRA_" +
                AJVYRA_CONFIG.gameId
            );

        if (!raw) {{
            return;
        }}

        const saveData =
            JSON.parse(raw);

        state.score =
            Number(
                saveData.score || 0
            );

        state.level =
            Number(
                saveData.level || 1
            );

        state.player.hp =
            Number(
                saveData.hp ||
                state.player.maxHp
            );

        state.enemiesDefeated =
            Number(
                saveData.enemiesDefeated || 0
            );

    }} catch (_) {{}}
}}


// ============================================================
// LEVEL
// ============================================================

function getCurrentLevel() {{

    return (
        AJVYRA_CONFIG.levels[
            state.level - 1
        ]
        ||
        AJVYRA_CONFIG.levels[
            AJVYRA_CONFIG.levels.length - 1
        ]
    );
}}

function spawnLevel() {{

    state.enemies = [];

    const level =
        getCurrentLevel();

    if (!level) {{
        winGame();
        return;
    }}

    const count =
        Number(
            level.enemy_count ||
            5
        );

    for (
        let i = 0;
        i < count;
        i++
    ) {{

        const source =
            AJVYRA_CONFIG.enemies[
                i %
                AJVYRA_CONFIG.enemies.length
            ];

        const enemy = {{

            id:
                source.enemy_id +
                "_" +
                i,

            name:
                source.name,

            x:
                randomRange(
                    40,
                    AJVYRA_CONFIG.width - 40
                ),

            y:
                randomRange(
                    40,
                    AJVYRA_CONFIG.height - 40
                ),

            hp:
                source.hp *
                Number(
                    level.difficulty || 1
                ),

            maxHp:
                source.max_hp *
                Number(
                    level.difficulty || 1
                ),

            speed:
                source.speed *
                Number(
                    level.difficulty || 1
                ),

            damage:
                source.damage *
                Number(
                    level.difficulty || 1
                ),

            size:
                source.size

        }};

        state.enemies.push(
            enemy
        );
    }}

    objective.textContent =
        level.objective ||
        "Defeat all enemies";
}}

function nextLevel() {{

    state.level += 1;

    if (
        state.level >
        AJVYRA_CONFIG.levels.length
    ) {{

        winGame();

        return;
    }}

    state.player.hp =
        Math.min(
            state.player.maxHp,
            state.player.hp + 25
        );

    spawnLevel();

    saveGame();
}}


// ============================================================
// COMBAT
// ============================================================

function attack() {{

    if (
        state.finished ||
        state.paused
    ) {{
        return;
    }}

    if (
        state.player.attackCooldown > 0
    ) {{
        return;
    }}

    state.player.attackCooldown =
        0.28;

    let nearest = null;

    let nearestDistance =
        Infinity;

    for (
        const enemy of state.enemies
    ) {{

        const d =
            distance(
                state.player,
                enemy
            );

        if (
            d < nearestDistance
            &&
            d < 110
        ) {{

            nearest =
                enemy;

            nearestDistance =
                d;
        }}
    }}

    if (!nearest) {{
        return;
    }}

    nearest.hp -= 35;

    createParticles(
        nearest.x,
        nearest.y,
        10
    );

    if (
        nearest.hp <= 0
    ) {{

        const index =
            state.enemies.indexOf(
                nearest
            );

        if (index !== -1) {{

            state.enemies.splice(
                index,
                1
            );
        }}

        state.score += 100;

        state.enemiesDefeated += 1;
    }}

    if (
        state.enemies.length === 0
    ) {{

        nextLevel();
    }}

    saveGame();
}}

function damagePlayer(
    amount
) {{

    if (
        state.player.invulnerable > 0
    ) {{
        return;
    }}

    state.player.hp -=
        amount;

    state.player.invulnerable =
        0.7;

    createParticles(
        state.player.x,
        state.player.y,
        8
    );

    if (
        state.player.hp <= 0
    ) {{

        state.player.hp = 0;

        loseGame();
    }}

    saveGame();
}}


// ============================================================
// UPDATE
// ============================================================

function update(
    dt
) {{

    if (
        !state.running ||
        state.paused ||
        state.finished
    ) {{
        return;
    }}

    state.player.attackCooldown =
        Math.max(
            0,
            state.player.attackCooldown - dt
        );

    state.player.invulnerable =
        Math.max(
            0,
            state.player.invulnerable - dt
        );

    let dx = 0;

    let dy = 0;

    if (
        state.keys["ArrowLeft"] ||
        state.keys["a"] ||
        state.keys["A"]
    ) {{
        dx -= 1;
    }}

    if (
        state.keys["ArrowRight"] ||
        state.keys["d"] ||
        state.keys["D"]
    ) {{
        dx += 1;
    }}

    if (
        state.keys["ArrowUp"] ||
        state.keys["w"] ||
        state.keys["W"]
    ) {{
        dy -= 1;
    }}

    if (
        state.keys["ArrowDown"] ||
        state.keys["s"] ||
        state.keys["S"]
    ) {{
        dy += 1;
    }}

    const length =
        Math.sqrt(
            dx * dx +
            dy * dy
        );

    if (length > 0) {{

        dx /= length;

        dy /= length;

        state.player.x +=
            dx *
            state.player.speed *
            dt;

        state.player.y +=
            dy *
            state.player.speed *
            dt;
    }}

    state.player.x =
        clamp(
            state.player.x,
            state.player.size,
            AJVYRA_CONFIG.width -
                state.player.size
        );

    state.player.y =
        clamp(
            state.player.y,
            state.player.size,
            AJVYRA_CONFIG.height -
                state.player.size
        );


    // --------------------------------------------------------
    // ENEMY AI
    // --------------------------------------------------------

    for (
        const enemy of state.enemies
    ) {{

        const dx =
            state.player.x -
            enemy.x;

        const dy =
            state.player.y -
            enemy.y;

        const d =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        if (
            d > 1
        ) {{

            enemy.x +=
                (dx / d) *
                enemy.speed *
                dt;

            enemy.y +=
                (dy / d) *
                enemy.speed *
                dt;
        }}

        if (
            circleCollision(
                state.player,
                enemy
            )
        ) {{

            damagePlayer(
                enemy.damage
                * dt
            );
        }}
    }}


    // --------------------------------------------------------
    // PARTICLES
    // --------------------------------------------------------

    for (
        const particle
        of state.particles
    ) {{

        particle.x +=
            particle.vx *
            dt;

        particle.y +=
            particle.vy *
            dt;

        particle.life -=
            dt;
    }}

    state.particles =
        state.particles.filter(
            p =>
                p.life > 0
        );

    updateHUD();
}}


// ============================================================
// COLLISION
// ============================================================

function circleCollision(
    a,
    b
) {{

    return (
        distance(a, b)
        <
        (
            Number(a.size || 20)
            +
            Number(b.size || 20)
        )
    );
}}


// ============================================================
// PARTICLES
// ============================================================

function createParticles(
    x,
    y,
    count
) {{

    if (
        !AJVYRA_CONFIG.enableParticles
    ) {{
        return;
    }}

    for (
        let i = 0;
        i < count;
        i++
    ) {{

        const angle =
            Math.random()
            * Math.PI
            * 2;

        const speed =
            randomRange(
                40,
                150
            );

        state.particles.push({{

            x,

            y,

            vx:
                Math.cos(angle)
                * speed,

            vy:
                Math.sin(angle)
                * speed,

            life:
                randomRange(
                    .2,
                    .6
                )

        }});
    }}
}}


// ============================================================
// RENDER
// ============================================================

function render() {{

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    // --------------------------------------------------------
    // BACKGROUND
    // --------------------------------------------------------

    const gradient =
        ctx.createRadialGradient(
            canvas.width / 2,
            canvas.height / 2,
            20,
            canvas.width / 2,
            canvas.height / 2,
            canvas.width
        );

    gradient.addColorStop(
        0,
        "#191936"
    );

    gradient.addColorStop(
        1,
        "#050509"
    );

    ctx.fillStyle =
        gradient;

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // --------------------------------------------------------
    // GRID
    // --------------------------------------------------------

    ctx.strokeStyle =
        "rgba(120,120,180,.08)";

    ctx.lineWidth = 1;

    const grid = 48;

    for (
        let x = 0;
        x < canvas.width;
        x += grid
    ) {{

        ctx.beginPath();

        ctx.moveTo(
            x,
            0
        );

        ctx.lineTo(
            x,
            canvas.height
        );

        ctx.stroke();
    }}

    for (
        let y = 0;
        y < canvas.height;
        y += grid
    ) {{

        ctx.beginPath();

        ctx.moveTo(
            0,
            y
        );

        ctx.lineTo(
            canvas.width,
            y
        );

        ctx.stroke();
    }}


    // --------------------------------------------------------
    // ENEMIES
    // --------------------------------------------------------

    for (
        const enemy
        of state.enemies
    ) {{

        ctx.beginPath();

        ctx.arc(
            enemy.x,
            enemy.y,
            enemy.size,
            0,
            Math.PI * 2
        );

        ctx.fillStyle =
            "#8e2738";

        ctx.fill();

        ctx.strokeStyle =
            "#e06a7c";

        ctx.stroke();


        // HP BAR

        const barWidth =
            enemy.size * 2;

        const ratio =
            Math.max(
                0,
                enemy.hp /
                enemy.maxHp
            );

        ctx.fillStyle =
            "#16161f";

        ctx.fillRect(
            enemy.x -
                barWidth / 2,
            enemy.y -
                enemy.size -
                10,
            barWidth,
            5
        );

        ctx.fillStyle =
            "#c74b61";

        ctx.fillRect(
            enemy.x -
                barWidth / 2,
            enemy.y -
                enemy.size -
                10,
            barWidth *
                ratio,
            5
        );
    }}


    // --------------------------------------------------------
    // PLAYER
    // --------------------------------------------------------

    ctx.save();

    if (
        state.player.invulnerable > 0
    ) {{

        ctx.globalAlpha =
            0.45 +
            Math.sin(
                performance.now()
                / 50
            ) *
            0.3;
    }}

    ctx.beginPath();

    ctx.arc(
        state.player.x,
        state.player.y,
        state.player.size,
        0,
        Math.PI * 2
    );

    ctx.fillStyle =
        "#d8d8e6";

    ctx.fill();

    ctx.strokeStyle =
        "#ffffff";

    ctx.lineWidth = 2;

    ctx.stroke();

    ctx.restore();


    // --------------------------------------------------------
    // PARTICLES
    // --------------------------------------------------------

    for (
        const particle
        of state.particles
    ) {{

        ctx.globalAlpha =
            Math.max(
                0,
                particle.life
            );

        ctx.fillStyle =
            "#ffffff";

        ctx.fillRect(
            particle.x,
            particle.y,
            4,
            4
        );
    }}

    ctx.globalAlpha = 1;


    // --------------------------------------------------------
    // PAUSED
    // --------------------------------------------------------

    if (
        state.paused
        &&
        !state.finished
    ) {{

        ctx.fillStyle =
            "rgba(0,0,0,.55)";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );

        ctx.fillStyle =
            "#ffffff";

        ctx.textAlign =
            "center";

        ctx.font =
            "bold 32px Arial";

        ctx.fillText(
            "PAUSED",
            canvas.width / 2,
            canvas.height / 2
        );
    }}
}}


// ============================================================
// HUD
// ============================================================

function updateHUD() {{

    hpValue.textContent =
        Math.max(
            0,
            Math.round(
                state.player.hp
            )
        );

    scoreValue.textContent =
        state.score;

    levelValue.textContent =
        state.level;
}}


// ============================================================
// WIN / LOSE
// ============================================================

function showMessage(
    text
) {{

    message.textContent =
        text;

    message.classList.remove(
        "hidden"
    );
}}

function winGame() {{

    state.finished = true;

    state.won = true;

    saveGame();

    showMessage(
        "YOU WIN — " +
        AJVYRA_CONFIG.title
    );
}}

function loseGame() {{

    state.finished = true;

    state.won = false;

    saveGame();

    showMessage(
        "GAME OVER"
    );
}}


// ============================================================
// INPUT
// ============================================================

window.addEventListener(
    "keydown",
    event => {{

        state.keys[
            event.key
        ] = true;

        if (
            event.key === " "
            ||
            event.key === "Enter"
        ) {{

            attack();
        }}

        if (
            event.key === "Escape"
        ) {{

            togglePause();
        }}
    }}
);

window.addEventListener(
    "keyup",
    event => {{

        state.keys[
            event.key
        ] = false;
    }}
);


// ============================================================
// TOUCH CONTROLS
// ============================================================

document
    .querySelectorAll(
        ".control"
    )
    .forEach(
        button => {{

            const key =
                button.dataset.key;

            const press =
                event => {{

                    event.preventDefault();

                    state.keys[
                        key
                    ] = true;
                }};

            const release =
                event => {{

                    event.preventDefault();

                    state.keys[
                        key
                    ] = false;
                }};

            button.addEventListener(
                "touchstart",
                press,
                {
                    passive: false
                }
            );

            button.addEventListener(
                "touchend",
                release,
                {
                    passive: false
                }
            );

            button.addEventListener(
                "mousedown",
                press
            );

            button.addEventListener(
                "mouseup",
                release
            );

            button.addEventListener(
                "mouseleave",
                release
            );
        }
    );

document
    .getElementById(
        "attack-button"
    )
    .addEventListener(
        "touchstart",
        event => {{

            event.preventDefault();

            attack();

        }},
        {
            passive: false
        }
    );

document
    .getElementById(
        "attack-button"
    )
    .addEventListener(
        "click",
        attack
    );


// ============================================================
// PAUSE
// ============================================================

function togglePause() {{

    if (
        state.finished
    ) {{
        return;
    }}

    state.paused =
        !state.paused;

    pauseButton.textContent =
        state.paused
        ? "RESUME"
        : "PAUSE";
}}

pauseButton.addEventListener(
    "click",
    togglePause
);


// ============================================================
// RESTART
// ============================================================

restartButton.addEventListener(
    "click",
    () => {{

        location.reload();

    }}
);


// ============================================================
// GAME LOOP
// ============================================================

function gameLoop(
    now
) {{

    const delta =
        Math.min(
            0.05,
            (
                now -
                state.lastTime
            ) / 1000
        );

    state.lastTime =
        now;

    update(
        delta
    );

    render();

    requestAnimationFrame(
        gameLoop
    );
}}


// ============================================================
// START
// ============================================================

function startGame() {{

    loadGame();

    spawnLevel();

    updateHUD();

    requestAnimationFrame(
        gameLoop
    );
}}

startGame();
"""

    # ========================================================
    # METADATA
    # ========================================================

    def _metadata(
        self,
        spec: GameSpec,
    ) -> Dict[str, Any]:

        return {
            "engine": (
                "AJVYRA Real Execution Engine"
            ),
            "engine_version": self.VERSION,
            "game_id": spec.game_id,
            "title": spec.title,
            "genre": spec.genre,
            "story": spec.story,
            "platform": "HTML5",
            "playable": True,
            "mobile": True,
            "keyboard": True,
            "touch": self.config.enable_touch,
            "levels": len(
                spec.levels
            ),
            "generated_at": time.time(),
        }

    # ========================================================
    # HTML ESCAPE
    # ========================================================

    @staticmethod
    def _escape_html(
        value: str,
    ) -> str:

        return (
            value
            .replace(
                "&",
                "&amp;",
            )
            .replace(
                "<",
                "&lt;",
            )
            .replace(
                ">",
                "&gt;",
            )
            .replace(
                '"',
                "&quot;",
            )
            .replace(
                "'",
                "&#39;",
            )
        )


# ============================================================
# CLI
# ============================================================

def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "AJVYRA Real Execution Engine"
        )
    )

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--game",
        type=int,
    )

    parser.add_argument(
        "--all",
        action="store_true",
    )

    args = parser.parse_args()

    engine = (
        AJVYRARealExecutionEngine(
            args.root
        )
    )

    if args.game:

        result = (
            engine.build_game_from_ai(
                args.game
            )
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    if args.all:

        result = (
            engine.build_all_games(
                70
            )
        )

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            )
        )

        return

    print(
        "AJVYRA Real Execution Engine"
    )

    print(
        "Use:"
    )

    print(
        "python ajvyra_real_execution_engine.py --game 1"
    )

    print(
        "or:"
    )

    print(
        "python ajvyra_real_execution_engine.py --all"
    )


if __name__ == "__main__":
    main()
