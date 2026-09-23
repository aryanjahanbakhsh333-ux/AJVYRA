from __future__ import annotations

import json
from pathlib import Path


GAMES = [
    ("Veylora Run", "runner"),
    ("Aelvryn Escape", "escape"),
    ("Nyxara Hunt", "hunt"),
    ("Kaelith Arena", "arena"),
    ("Orivane Dash", "dash"),
    ("Zeravia Quest", "quest"),
    ("Vaelune Survivor", "survivor"),
    ("Ravelyth Chase", "chase"),
    ("Solvarya Rush", "rush"),
    ("Xaveren Trials", "trials"),
    ("Elyvara Maze", "maze"),
    ("Neravelle Hunter", "hunter"),
    ("Vaerith Battle", "battle"),
    ("Lunavyr Runner", "runner"),
    ("Averlyn Escape", "escape"),
    ("Neyvara Hunt", "hunt"),
    ("Elvaria Arena", "arena"),
    ("Virelya Dash", "dash"),
    ("Caelora Quest", "quest"),
    ("Seravyn Survivor", "survivor"),
    ("Mouravia Chase", "chase"),
    ("Noxelya Rush", "rush"),
    ("Vaelora Trials", "trials"),
    ("Eryndra Maze", "maze"),
    ("Neylith Hunter", "hunter"),
    ("Auralyne Battle", "battle"),
    ("Velmora Runner", "runner"),
    ("Seyravia Escape", "escape"),
    ("Oryvane Hunt", "hunt"),
    ("Luminarae Arena", "arena"),
]


class AJVYRA30RealGameFactory:

    def __init__(
        self,
        root: str = "games/real-projects",
    ):
        self.root = Path(root)
        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def slug(value: str) -> str:
        return "".join(
            c.lower() if c.isalnum() else "_"
            for c in value
        ).strip("_")

    def project_config(
        self,
        title: str,
    ) -> str:

        return f'''
[application]

config/name="{title}"
run/main_scene="res://main.tscn"

[display]

window/size/viewport_width=960
window/size/viewport_height=540
window/size/window_width_override=960
window/size/window_height_override=540

[rendering]

renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"

[input]

left={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":65)]
}}

right={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":68)]
}}

jump={{
"deadzone": 0.5,
"events": [Object(InputEventKey,"physical_keycode":32)]
}}
'''

    def scene(self) -> str:
        return '''
[gd_scene load_steps=2 format=3]

[ext_resource path="res://main.gd" type="Script" id="1"]

[node name="AJVYRA_Game" type="Node2D"]
script = ExtResource("1")
'''

    def script(
        self,
        title: str,
        mode: str,
        index: int,
    ) -> str:

        target = 8 + (
            index % 7
        )

        speed = 210 + (
            index * 9
        )

        enemy_count = 3 + (
            index % 6
        )

        return f'''
extends Node2D

const SPEED := {speed}.0
const GRAVITY := 1000.0
const JUMP_FORCE := -450.0
const TARGET_SCORE := {target}

var player := Vector2(480, 430)
var velocity := Vector2.ZERO
var score := 0
var ended := false
var won := false

var collectibles: Array[Vector2] = []
var enemies: Array[Vector2] = []

func _ready():
    get_window().title = "{title}"
    build_level()

func build_level():
    for i in range(TARGET_SCORE):
        collectibles.append(
            Vector2(
                70 + ((i * 113 + {index} * 17) % 820),
                150 + ((i * 71 + {index} * 23) % 260)
            )
        )

    for i in range({enemy_count}):
        enemies.append(
            Vector2(
                100 + i * 150,
                430
            )
        )

    queue_redraw()

func _process(delta):
    if ended:
        queue_redraw()
        return

    velocity.x = 0

    if Input.is_action_pressed("left"):
        velocity.x -= SPEED

    if Input.is_action_pressed("right"):
        velocity.x += SPEED

    velocity.y += GRAVITY * delta

    if (
        Input.is_action_just_pressed("jump")
        and player.y >= 430
    ):
        velocity.y = JUMP_FORCE

    player += velocity * delta

    player.x = clamp(
        player.x,
        25.0,
        935.0
    )

    if player.y >= 430:
        player.y = 430
        velocity.y = 0

    collect()
    collide()

    if score >= TARGET_SCORE:
        won = true
        ended = true

    queue_redraw()

func collect():
    for item in collectibles.duplicate():
        if player.distance_to(item) < 30:
            collectibles.erase(item)
            score += 1

func collide():
    for enemy in enemies:
        if player.distance_to(enemy) < 35:
            ended = true
            won = false

func _draw():

    draw_rect(
        Rect2(0, 0, 960, 540),
        Color("#070707")
    )

    draw_rect(
        Rect2(0, 460, 960, 80),
        Color("#141414")
    )

    for item in collectibles:
        draw_circle(
            item,
            11,
            Color("#d8b56a")
        )

    for enemy in enemies:
        draw_circle(
            enemy,
            19,
            Color("#8b2440")
        )

    draw_circle(
        player,
        22,
        Color("#eeeeee")
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(28, 38),
        "{title}",
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        25,
        Color.WHITE
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(28, 72),
        "Score: %d / %d" %
        [score, TARGET_SCORE],
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        20,
        Color("#d8b56a")
    )

    draw_string(
        ThemeDB.fallback_font,
        Vector2(28, 515),
        "A / D: Move    SPACE: Jump",
        HORIZONTAL_ALIGNMENT_LEFT,
        -1,
        18,
        Color("#999999")
    )

    if won:
        draw_string(
            ThemeDB.fallback_font,
            Vector2(370, 270),
            "VICTORY",
            HORIZONTAL_ALIGNMENT_LEFT,
            -1,
            46,
            Color("#d8b56a")
        )

    elif ended:
        draw_string(
            ThemeDB.fallback_font,
            Vector2(370, 270),
            "GAME OVER",
            HORIZONTAL_ALIGNMENT_LEFT,
            -1,
            42,
            Color("#ff7777")
        )
'''

    def create_game(
        self,
        index: int,
        title: str,
        mode: str,
    ) -> Path:

        slug = self.slug(title)
        project = self.root / slug

        if project.exists():
            raise FileExistsError(
                f"Refusing to overwrite existing game: "
                f"{project}"
            )

        project.mkdir(
            parents=True
        )

        (project / "project.godot").write_text(
            self.project_config(title),
            encoding="utf-8",
        )

        (project / "main.tscn").write_text(
            self.scene(),
            encoding="utf-8",
        )

        (project / "main.gd").write_text(
            self.script(
                title,
                mode,
                index,
            ),
            encoding="utf-8",
        )

        metadata = {
            "id": f"ajvyra-game-{index + 1:02d}",
            "title": title,
            "genre": mode,
            "engine": "Godot",
            "real_project": True,
            "ready_for_export": True,
            "published": False,
        }

        (project / "game.json").write_text(
            json.dumps(
                metadata,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return project

    def create_all(self) -> list[Path]:

        projects = []

        for index, (
            title,
            mode,
        ) in enumerate(GAMES):

            print(
                f"[GAME] Creating "
                f"{index + 1}/30: {title}"
            )

            projects.append(
                self.create_game(
                    index,
                    title,
                    mode,
                )
            )

        if len(projects) != 30:
            raise RuntimeError(
                "30 game projects were not created."
            )

        return projects


if __name__ == "__main__":
    factory = AJVYRA30RealGameFactory()
    projects = factory.create_all()

    print(
        f"REAL GAME PROJECTS: "
        f"{len(projects)}/30"
    )
