from __future__ import annotations

import json
import shutil
from pathlib import Path


class AJVYRARealGameFactory:
    """
    Creates a real playable Godot game project.

    The generated project contains:
        project.godot
        main scene
        actual GDScript gameplay
        UI
        player movement
        collectible system
        enemy system
        win/lose state
    """

    def __init__(
        self,
        root: str = "games/produced",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def safe_name(title: str) -> str:
        value = ""

        for char in title.lower():
            if char.isalnum():
                value += char
            elif char in {" ", "-", "_"}:
                value += "_"

        return value.strip("_") or "ajvyra_game"

    def create(
        self,
        title: str,
        description: str,
        game_id: str,
    ) -> Path:

        name = self.safe_name(title)
        project = self.root / name

        if project.exists():
            raise FileExistsError(
                f"Game already exists: {project}"
            )

        (project / "scripts").mkdir(
            parents=True
        )

        (project / "scenes").mkdir()

        project_config = f"""
[application]

config/name="{title}"
run/main_scene="res://scenes/main.tscn"

[display]

window/size/viewport_width=960
window/size/viewport_height=540
window/size/window_width_override=960
window/size/window_height_override=540

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"

[input]

move_left={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":65)]
}}

move_right={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":68)]
}}

jump={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":32)]
}}
"""

        (project / "project.godot").write_text(
            project_config.strip(),
            encoding="utf-8",
        )

        scene = """[gd_scene load_steps=2 format=3]

[ext_resource path="res://scripts/main.gd" type="Script" id="1"]

[node name="AJVYRA_Game" type="Node2D"]
script = ExtResource("1")
"""

        (project / "scenes/main.tscn").write_text(
            scene,
            encoding="utf-8",
        )

        script = f'''
extends Node2D

var player_position := Vector2(480, 430)
var velocity := Vector2.ZERO
var collectibles := []
var enemies := []
var score := 0
var game_over := false
var won := false

const SPEED := 260.0
const GRAVITY := 900.0
const JUMP_FORCE := -430.0

func _ready():
    get_window().title = "{title}"
    create_world()

func create_world():
    for i in range(12):
        collectibles.append(
            Vector2(
                70 + i * 70,
                180 + ((i * 47) % 180)
            )
        )

    for i in range(5):
        enemies.append(
            Vector2(
                150 + i * 150,
                420
            )
        )

    queue_redraw()

func _process(delta):
    if game_over or won:
        queue_redraw()
        return

    velocity.x = 0

    if Input.is_action_pressed("move_left"):
        velocity.x -= SPEED

    if Input.is_action_pressed("move_right"):
        velocity.x += SPEED

    velocity.y += GRAVITY * delta

    if (
        Input.is_action_just_pressed("jump")
        and player_position.y >= 430
    ):
        velocity.y = JUMP_FORCE

    player_position += velocity * delta

    player_position.x = clamp(
        player_position.x,
        30.0,
        930.0
    )

    if player_position.y >= 430:
        player_position.y = 430
        velocity.y = 0

    collect_items()
    check_enemies()

    if score >= 12:
        won = true

    queue_redraw()

func collect_items():
    for item in collectibles.duplicate():
        if player_position.distance_to(item) < 32:
            collectibles.erase(item)
            score += 1

func check_enemies():
    for enemy in enemies:
        if player_position.distance_to(enemy) < 34:
            game_over = true

func _draw():
    draw_rect(
        Rect2(0, 0, 960, 540),
        Color("#090909")
    )

    draw_rect(
        Rect2(0, 455, 960, 85),
        Color("#151515")
    )

    for item in collectibles:
        draw_circle(
            item,
            12,
            Color("#d6b56b")
        )

    for enemy in enemies:
        draw_circle(
            enemy,
            20,
            Color("#771d35")
        )

    draw_circle(
        player_position,
        22,
        Color("#f0f0f0")
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(30, 45),
        "{title}",
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        26,
        Color.WHITE
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(30, 80),
        "Score: %d / 12" % score,
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        22,
        Color("#d6b56b")
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(30, 510),
        "A / D = Move    SPACE = Jump",
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        18,
        Color("#aaaaaa")
    )

    if game_over:
        draw_string(
            ThemeDB.fallback_font,
            Vector2(370, 270),
            "GAME OVER",
            HORIZONTAL_ALIGNMENT_LEFT,
            -1,
            42,
            Color("#ff7777")
        )

    if won:
        draw_string(
            ThemeDB.fallback_font,
            Vector2(390, 270),
            "YOU WIN",
            HORIZONTAL_ALIGNMENT_LEFT,
            -1,
            42,
            Color("#d6b56b")
        )
'''

        (project / "scripts/main.gd").write_text(
            script.strip(),
            encoding="utf-8",
        )

        metadata = {
            "id": game_id,
            "title": title,
            "description": description,
            "engine": "Godot",
            "real_project": True,
            "exported": False,
            "published": False,
        }

        (project / "ajvyra-game.json").write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return project


if __name__ == "__main__":
    factory = AJVYRARealGameFactory()

    path = factory.create(
        title="Veylora: Dark Run",
        description=(
            "A playable dark arcade adventure."
        ),
        game_id="ajv-game-001",
    )

    print(f"Created real Godot game: {path}")
