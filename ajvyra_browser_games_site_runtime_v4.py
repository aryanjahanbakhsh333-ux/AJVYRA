"""
AJVYRA — BROWSER GAMES SITE RUNTIME V4
=======================================

30 playable browser games for AJVYRA.

Architecture:
    Python builder
        ↓
    HTML5 + Canvas + JavaScript
        ↓
    Browser
        ↓
    User plays directly inside AJVYRA

No Pygame.
No Python required on the user's device.
No installation.
Works with keyboard + mouse on desktop
and touch controls on phones/tablets.

The generated games are standalone HTML files and can be
served directly by any normal web server.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import html
import hashlib
import shutil


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_ROOT = Path("generated/ajvyra_release/games")

GAME_COUNT = 30


# ============================================================
# GAME DEFINITIONS
# ============================================================

@dataclass(frozen=True)
class BrowserGame:
    number: int
    title: str
    genre: str
    description: str
    mechanic: str
    objective: str


GAMES = [
    BrowserGame(1, "Black Run", "Action / Platformer",
                "Run through the darkness and reach the gate.",
                "runner", "Reach the portal"),

    BrowserGame(2, "Shadow Hunt", "Horror",
                "Collect the hidden fragments while shadows chase you.",
                "horror", "Collect 8 fragments"),

    BrowserGame(3, "Neon Drift", "Racing",
                "Race through a neon city and pass every checkpoint.",
                "racing", "Reach the finish"),

    BrowserGame(4, "Crystal Quest", "RPG / Adventure",
                "Collect crystals and defeat the guardian.",
                "rpg", "Collect crystals and defeat the guardian"),

    BrowserGame(5, "Cipher Room", "Puzzle",
                "Discover the correct sequence and escape.",
                "sequence", "Solve the sequence"),

    BrowserGame(6, "Silent Step", "Stealth",
                "Cross the room without entering enemy vision.",
                "stealth", "Reach the exit"),

    BrowserGame(7, "Meteor Zero", "Survival",
                "Survive as long as possible under a meteor storm.",
                "survival", "Survive 45 seconds"),

    BrowserGame(8, "Last Tower", "Defense",
                "Protect the tower from incoming enemies.",
                "defense", "Survive the assault"),

    BrowserGame(9, "Lost Signal", "Mystery",
                "Find the scattered signal fragments.",
                "collect", "Find 10 signals"),

    BrowserGame(10, "Void Arena", "Combat",
                "Fight through enemy waves in the void.",
                "combat", "Defeat 20 enemies"),

    BrowserGame(11, "Frost Line", "Racing",
                "Cross the frozen track before time runs out.",
                "racing", "Reach the finish"),

    BrowserGame(12, "Night Courier", "Adventure",
                "Deliver the mysterious package.",
                "delivery", "Reach the destination"),

    BrowserGame(13, "Red Maze", "Puzzle",
                "Escape a maze that changes while you move.",
                "maze", "Find the exit"),

    BrowserGame(14, "Echo Cave", "Exploration",
                "Explore the cave and collect its echoes.",
                "collect", "Collect 12 echoes"),

    BrowserGame(15, "Iron Squad", "Strategy",
                "Defend your base and survive enemy attacks.",
                "strategy", "Protect the base"),

    BrowserGame(16, "Ghost Train", "Horror",
                "Escape the abandoned train.",
                "horror", "Find the exit"),

    BrowserGame(17, "Skyfall", "Arcade",
                "Avoid falling obstacles and stay alive.",
                "survival", "Survive 45 seconds"),

    BrowserGame(18, "Black Harbor", "Mystery",
                "Search the harbor for hidden clues.",
                "collect", "Find 7 clues"),

    BrowserGame(19, "Pulse", "Rhythm / Skill",
                "Hit moving targets at the correct moment.",
                "timing", "Hit 15 targets"),

    BrowserGame(20, "Dragon Core", "Fantasy / Action",
                "Defeat the guardian of the Dragon Core.",
                "boss", "Defeat the guardian"),

    BrowserGame(21, "Deep One", "Survival",
                "Survive the underwater ruins.",
                "survival", "Survive 50 seconds"),

    BrowserGame(22, "Zero Gravity", "Arcade",
                "Collect stars in a gravity-free arena.",
                "collect", "Collect 15 stars"),

    BrowserGame(23, "Hunter", "Combat",
                "Track targets while surviving ambushes.",
                "combat", "Defeat 18 enemies"),

    BrowserGame(24, "Memory Grid", "Puzzle",
                "Remember the pattern and reproduce it.",
                "memory", "Complete 4 patterns"),

    BrowserGame(25, "Desert Run", "Racing",
                "Cross the desert while avoiding hazards.",
                "racing", "Reach the finish"),

    BrowserGame(26, "Night Watch", "Defense",
                "Protect the beacon from approaching enemies.",
                "defense", "Protect the beacon"),

    BrowserGame(27, "Phantom Key", "Stealth",
                "Find the key and escape without being detected.",
                "stealth", "Find the key and escape"),

    BrowserGame(28, "Star Forge", "Strategy",
                "Collect energy and activate the forge.",
                "collect", "Collect 20 energy"),

    BrowserGame(29, "Final Gate", "Boss / Action",
                "Break through the guardian of the final gate.",
                "boss", "Defeat the boss"),

    BrowserGame(30, "AJVYRA Zero", "Final Challenge",
                "A final challenge combining several mechanics.",
                "final", "Reach 100 points"),
]


# ============================================================
# HTML TEMPLATE
# ============================================================

HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width,
               initial-scale=1,
               maximum-scale=1,
               user-scalable=no,
               viewport-fit=cover">

<title>AJVYRA — {{TITLE}}</title>

<style>

* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html,
body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #050505;
    color: white;
    font-family: Arial, Helvetica, sans-serif;
}

body {
    display: flex;
    align-items: center;
    justify-content: center;
}

#gameShell {
    position: relative;
    width: 100vw;
    height: 100vh;
    background:
        radial-gradient(circle at center,
                        #171717 0%,
                        #080808 55%,
                        #000000 100%);
    overflow: hidden;
}

canvas {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: block;
    touch-action: none;
}

#topBar {
    position: absolute;
    top: 12px;
    left: 12px;
    right: 12px;
    height: 52px;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 16px;

    background: rgba(10,10,10,.78);
    border: 1px solid rgba(255,255,255,.12);
    border-radius: 14px;

    backdrop-filter: blur(12px);

    z-index: 10;
}

#logo {
    font-weight: 900;
    letter-spacing: 4px;
}

#stats {
    display: flex;
    gap: 18px;
    font-size: 14px;
}

#message {
    position: absolute;
    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    text-align: center;

    min-width: 280px;
    max-width: 90vw;

    padding: 28px;

    background: rgba(5,5,5,.92);
    border: 1px solid rgba(255,255,255,.16);
    border-radius: 20px;

    z-index: 20;

    display: none;
}

#message h1 {
    margin: 0 0 10px;
    font-size: 32px;
}

#message p {
    color: #aaa;
    line-height: 1.6;
}

button {
    border: 1px solid rgba(255,255,255,.2);
    background: #151515;
    color: white;

    padding: 12px 18px;

    border-radius: 12px;

    font-weight: 800;

    cursor: pointer;
}

button:active {
    transform: scale(.95);
}

#mobileControls {
    position: absolute;
    inset: auto 0 0 0;
    height: 190px;

    pointer-events: none;

    z-index: 15;
}

#joystick {
    position: absolute;
    left: 25px;
    bottom: 25px;

    width: 115px;
    height: 115px;

    border-radius: 50%;

    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.15);

    pointer-events: auto;
}

#stick {
    position: absolute;

    width: 50px;
    height: 50px;

    left: 32px;
    top: 32px;

    border-radius: 50%;

    background: rgba(255,255,255,.25);
    border: 1px solid rgba(255,255,255,.25);
}

#action {
    position: absolute;

    right: 28px;
    bottom: 42px;

    width: 82px;
    height: 82px;

    border-radius: 50%;

    background: rgba(255,255,255,.12);

    pointer-events: auto;
}

#pause {
    position: absolute;

    right: 28px;
    bottom: 135px;

    width: 52px;
    height: 42px;

    padding: 0;

    pointer-events: auto;
}

@media (min-width: 900px) {
    #mobileControls {
        display: none;
    }
}

@media (orientation: portrait) and (max-width: 899px) {

    #rotateNotice {
        display: flex;
    }

}

#rotateNotice {
    display: none;

    position: absolute;
    inset: 0;

    align-items: center;
    justify-content: center;

    text-align: center;

    background: #000;

    z-index: 100;

    padding: 30px;

    font-size: 20px;
    font-weight: 800;
}

</style>
</head>

<body>

<div id="gameShell">

    <canvas id="game"></canvas>

    <div id="topBar">
        <div id="logo">AJVYRA</div>

        <div id="stats">
            <span id="gameName">{{TITLE}}</span>
            <span id="score">SCORE 0</span>
            <span id="timer">TIME 60</span>
        </div>
    </div>

    <div id="message">

        <h1 id="messageTitle"></h1>

        <p id="messageText"></p>

        <button id="restart">
            PLAY AGAIN
        </button>

    </div>

    <div id="mobileControls">

        <div id="joystick">
            <div id="stick"></div>
        </div>

        <button id="action">
            ACTION
        </button>

        <button id="pause">
            II
        </button>

    </div>

    <div id="rotateNotice">
        📱<br><br>
        Rotate your phone to landscape mode
        to play AJVYRA.
    </div>

</div>


<script>

const GAME = {
    number: {{NUMBER}},
    title: "{{TITLE_JS}}",
    genre: "{{GENRE_JS}}",
    mechanic: "{{MECHANIC}}",
    objective: "{{OBJECTIVE_JS}}"
};


const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0;
let H = 0;

function resize() {

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    W = window.innerWidth;
    H = window.innerHeight;

    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);

    canvas.style.width = W + "px";
    canvas.style.height = H + "px";

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

window.addEventListener("resize", resize);
resize();


const keys = {};

window.addEventListener("keydown", e => {

    keys[e.key.toLowerCase()] = true;

    if (
        e.key === " " ||
        e.key === "ArrowUp" ||
        e.key === "ArrowDown" ||
        e.key === "ArrowLeft" ||
        e.key === "ArrowRight"
    ) {
        e.preventDefault();
    }

    if (e.key.toLowerCase() === "p") {
        togglePause();
    }

    if (e.key.toLowerCase() === "r") {
        resetGame();
    }

});

window.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()] = false;
});


const input = {
    x: 0,
    y: 0,
    action: false
};


const joystick = document.getElementById("joystick");
const stick = document.getElementById("stick");

let joystickActive = false;


function joystickMove(clientX, clientY) {

    const rect = joystick.getBoundingClientRect();

    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;

    let dx = clientX - cx;
    let dy = clientY - cy;

    const max = 42;

    const length = Math.hypot(dx, dy);

    if (length > max) {

        dx = dx / length * max;
        dy = dy / length * max;

    }

    input.x = dx / max;
    input.y = dy / max;

    stick.style.transform =
        `translate(${dx}px, ${dy}px)`;
}


joystick.addEventListener("pointerdown", e => {

    joystickActive = true;

    joystick.setPointerCapture(e.pointerId);

    joystickMove(e.clientX, e.clientY);

});


joystick.addEventListener("pointermove", e => {

    if (!joystickActive) return;

    joystickMove(e.clientX, e.clientY);

});


joystick.addEventListener("pointerup", () => {

    joystickActive = false;

    input.x = 0;
    input.y = 0;

    stick.style.transform = "translate(0,0)";

});


document.getElementById("action")
.addEventListener("pointerdown", () => {

    input.action = true;

});


document.getElementById("pause")
.addEventListener("pointerdown", togglePause);


function getX() {

    return (
        input.x ||
        ((keys["d"] || keys["arrowright"]) ? 1 : 0) -
        ((keys["a"] || keys["arrowleft"]) ? 1 : 0)
    );

}


function getY() {

    return (
        input.y ||
        ((keys["s"] || keys["arrowdown"]) ? 1 : 0) -
        ((keys["w"] || keys["arrowup"]) ? 1 : 0)
    );

}


function consumeAction() {

    const value =
        input.action ||
        keys[" "] ||
        keys["enter"];

    input.action = false;

    return value;
}


let player;
let objects;
let enemies;

let score;
let timeLeft;

let running;
let paused;
let won;

let lastTime = 0;

let spawnClock = 0;

let particles = [];


function random(min, max) {

    return Math.random() * (max - min) + min;

}


function createPlayer() {

    return {

        x: W * .2,
        y: H * .55,

        r: 18,

        speed: 260,

        hp: 100,

        dash: 0

    };

}


function createObject() {

    return {

        x: random(100, W - 100),
        y: random(100, H - 100),

        r: 13,

        collected: false,

        pulse: random(0, Math.PI * 2)

    };

}


function createEnemy() {

    const side = Math.floor(random(0, 4));

    let x;
    let y;

    if (side === 0) {

        x = random(0, W);
        y = -30;

    } else if (side === 1) {

        x = W + 30;
        y = random(70, H);

    } else if (side === 2) {

        x = random(0, W);
        y = H + 30;

    } else {

        x = -30;
        y = random(70, H);

    }

    return {

        x,
        y,

        r: 16,

        speed: random(65, 120),

        hp: 1

    };

}


function resetGame() {

    player = createPlayer();

    objects = [];
    enemies = [];

    particles = [];

    score = 0;

    timeLeft = 60;

    running = true;
    paused = false;
    won = false;

    spawnClock = 0;

    setupGame();

    hideMessage();

}


function setupGame() {

    const m = GAME.mechanic;

    let count = 10;

    if (m === "collect") count = 14;
    if (m === "racing") count = 7;
    if (m === "sequence") count = 4;
    if (m === "memory") count = 4;
    if (m === "boss") count = 3;

    for (let i = 0; i < count; i++) {
        objects.push(createObject());
    }

    for (let i = 0; i < 3; i++) {
        enemies.push(createEnemy());
    }

}


function distance(a, b) {

    return Math.hypot(
        a.x - b.x,
        a.y - b.y
    );

}


function addParticle(x, y) {

    particles.push({

        x,
        y,

        vx: random(-120, 120),
        vy: random(-120, 120),

        life: .5

    });

}


function updateParticles(dt) {

    for (const p of particles) {

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        p.life -= dt;

    }

    particles =
        particles.filter(p => p.life > 0);

}


function updatePlayer(dt) {

    let dx = getX();
    let dy = getY();

    if (dx || dy) {

        const length = Math.hypot(dx, dy);

        if (length > 1) {
            dx /= length;
            dy /= length;
        }

        player.x += dx * player.speed * dt;
        player.y += dy * player.speed * dt;

    }

    player.x =
        Math.max(25, Math.min(W - 25, player.x));

    player.y =
        Math.max(80, Math.min(H - 25, player.y));

}


function updateEnemies(dt) {

    for (const enemy of enemies) {

        const dx = player.x - enemy.x;
        const dy = player.y - enemy.y;

        const length = Math.hypot(dx, dy) || 1;

        enemy.x +=
            dx / length *
            enemy.speed *
            dt;

        enemy.y +=
            dy / length *
            enemy.speed *
            dt;

        if (distance(player, enemy)
            < player.r + enemy.r) {

            player.hp -= 28 * dt;

        }

    }

}


function collectObjects() {

    for (const object of objects) {

        if (object.collected) continue;

        if (
            distance(player, object)
            < player.r + object.r + 5
        ) {

            object.collected = true;

            score += 10;

            addParticle(object.x, object.y);

        }

    }

}


function spawnEnemies(dt) {

    spawnClock += dt;

    if (spawnClock > 3) {

        spawnClock = 0;

        if (enemies.length < 10) {
            enemies.push(createEnemy());
        }

    }

}


function objectiveComplete() {

    const collected =
        objects.filter(x => x.collected).length;

    if (GAME.mechanic === "collect") {
        return collected >= Math.min(10, objects.length);
    }

    if (GAME.mechanic === "survival") {
        return timeLeft <= 0;
    }

    if (GAME.mechanic === "racing") {

        return (
            player.x > W - 100
            && player.y > H * .35
            && player.y < H * .65
        );

    }

    if (GAME.mechanic === "boss") {

        return score >= 100;

    }

    if (GAME.mechanic === "final") {

        return score >= 100;

    }

    return score >= 100 ||
           collected >= 8;

}


function update(dt) {

    if (!running || paused) return;

    timeLeft -= dt;

    updatePlayer(dt);

    updateEnemies(dt);

    collectObjects();

    spawnEnemies(dt);

    updateParticles(dt);

    if (GAME.mechanic === "survival") {

        if (timeLeft <= 0) {

            winGame();

            return;

        }

    }

    if (objectiveComplete()) {

        winGame();

        return;

    }

    if (player.hp <= 0) {

        loseGame();

    }

}


function drawBackground() {

    ctx.fillStyle = "#050505";

    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle =
        "rgba(255,255,255,.035)";

    const grid = 50;

    for (let x = 0; x < W; x += grid) {

        ctx.beginPath();

        ctx.moveTo(x, 60);
        ctx.lineTo(x, H);

        ctx.stroke();

    }

    for (let y = 80; y < H; y += grid) {

        ctx.beginPath();

        ctx.moveTo(0, y);
        ctx.lineTo(W, y);

        ctx.stroke();

    }

}


function drawPlayer() {

    ctx.beginPath();

    ctx.arc(
        player.x,
        player.y,
        player.r,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";

    ctx.fill();

}


function drawObjects() {

    for (const object of objects) {

        if (object.collected) continue;

        object.pulse += .04;

        const radius =
            object.r +
            Math.sin(object.pulse) * 3;

        ctx.beginPath();

        ctx.arc(
            object.x,
            object.y,
            radius,
            0,
            Math.PI * 2
        );

        ctx.strokeStyle =
            "rgba(255,255,255,.8)";

        ctx.lineWidth = 2;

        ctx.stroke();

    }

}


function drawEnemies() {

    for (const enemy of enemies) {

        ctx.beginPath();

        ctx.arc(
            enemy.x,
            enemy.y,
            enemy.r,
            0,
            Math.PI * 2
        );

        ctx.fillStyle = "#8b1e2d";

        ctx.fill();

    }

}


function drawFinish() {

    if (GAME.mechanic !== "racing") return;

    ctx.fillStyle = "#ffffff";

    ctx.fillRect(
        W - 100,
        H * .35,
        20,
        H * .30
    );

}


function drawParticles() {

    for (const p of particles) {

        ctx.globalAlpha =
            Math.max(0, p.life * 2);

        ctx.fillStyle = "#ffffff";

        ctx.fillRect(
            p.x,
            p.y,
            4,
            4
        );

    }

    ctx.globalAlpha = 1;

}


function draw() {

    drawBackground();

    drawFinish();

    drawObjects();

    drawEnemies();

    drawPlayer();

    drawParticles();

    document.getElementById("score")
        .textContent =
        "SCORE " + Math.floor(score);

    document.getElementById("timer")
        .textContent =
        "TIME " +
        Math.max(0, Math.ceil(timeLeft));

}


function gameLoop(timestamp) {

    const dt =
        Math.min(
            .033,
            (timestamp - lastTime) / 1000 || 0
        );

    lastTime = timestamp;

    update(dt);

    draw();

    requestAnimationFrame(gameLoop);

}


function winGame() {

    if (!running) return;

    running = false;
    won = true;

    showMessage(
        "VICTORY",
        "You completed " + GAME.title + "."
    );

}


function loseGame() {

    if (!running) return;

    running = false;
    won = false;

    showMessage(
        "GAME OVER",
        "The darkness got you."
    );

}


function showMessage(title, text) {

    document.getElementById("messageTitle")
        .textContent = title;

    document.getElementById("messageText")
        .textContent = text;

    document.getElementById("message")
        .style.display = "block";

}


function hideMessage() {

    document.getElementById("message")
        .style.display = "none";

}


function togglePause() {

    if (!running) return;

    paused = !paused;

    if (paused) {

        showMessage(
            "PAUSED",
            "Press P or the pause button to continue."
        );

    } else {

        hideMessage();

    }

}


document.getElementById("restart")
    .addEventListener(
        "click",
        resetGame
    );


resetGame();

requestAnimationFrame(gameLoop);

</script>

</body>
</html>
'''


# ============================================================
# SAFE JS STRING
# ============================================================

def js_string(value: str) -> str:
    return (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
    )


# ============================================================
# BUILD ONE GAME
# ============================================================

def build_game(game: BrowserGame) -> Path:

    game_dir = (
        OUTPUT_ROOT /
        f"game_{game.number:02d}"
    )

    game_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = game_dir / "index.html"

    content = HTML_TEMPLATE

    content = content.replace(
        "{{NUMBER}}",
        str(game.number)
    )

    content = content.replace(
        "{{TITLE}}",
        html.escape(game.title)
    )

    content = content.replace(
        "{{TITLE_JS}}",
        js_string(game.title)
    )

    content = content.replace(
        "{{GENRE_JS}}",
        js_string(game.genre)
    )

    content = content.replace(
        "{{MECHANIC}}",
        js_string(game.mechanic)
    )

    content = content.replace(
        "{{OBJECTIVE_JS}}",
        js_string(game.objective)
    )

    filename.write_text(
        content,
        encoding="utf-8"
    )

    return filename


# ============================================================
# VALIDATION
# ============================================================

def validate_game(path: Path) -> list[str]:

    errors = []

    if not path.exists():
        errors.append("missing_file")
        return errors

    text = path.read_text(
        encoding="utf-8"
    )

    required = [
        "<canvas",
        "requestAnimationFrame",
        "keydown",
        "pointerdown",
        "touch-action",
        "resetGame",
        "winGame",
        "loseGame",
        "GAME =",
    ]

    for token in required:

        if token not in text:
            errors.append(
                f"missing:{token}"
            )

    if len(text) < 10000:
        errors.append("game_html_too_small")

    return errors


# ============================================================
# MANIFEST
# ============================================================

def sha256(path: Path) -> str:

    digest = hashlib.sha256()

    with path.open("rb") as f:

        for chunk in iter(
            lambda: f.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def build_manifest(
    built_games: list[tuple[BrowserGame, Path]]
) -> Path:

    entries = []

    for game, path in built_games:

        errors = validate_game(path)

        entries.append({

            "number": game.number,

            "title": game.title,

            "genre": game.genre,

            "description": game.description,

            "mechanic": game.mechanic,

            "objective": game.objective,

            "browser_playable": len(errors) == 0,

            "path":
                str(
                    path.relative_to(
                        OUTPUT_ROOT.parent.parent
                    )
                ).replace("\\", "/"),

            "sha256":
                sha256(path)
                if not errors
                else None,

            "validation_errors":
                errors,

        })

    manifest = {

        "project": "AJVYRA",

        "type": "browser_games",

        "version": "v4",

        "total_games": len(entries),

        "play_inside_site": True,

        "requires_installation": False,

        "requires_pygame": False,

        "desktop_controls": [
            "WASD",
            "Arrow Keys",
            "P",
            "R",
        ],

        "mobile_controls": [
            "Touch Joystick",
            "Action Button",
            "Pause Button",
        ],

        "games": entries,

    }

    output = (
        OUTPUT_ROOT.parent /
        "ajvyra_browser_games_manifest_v4.json"
    )

    output.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    return output


# ============================================================
# SITE GAME HUB
# ============================================================

def build_hub(
    games: list[BrowserGame]
) -> Path:

    cards = []

    for game in games:

        cards.append(f"""
<a class="game-card"
   href="./game_{game.number:02d}/index.html">

    <div class="number">
        #{game.number:02d}
    </div>

    <h2>
        {html.escape(game.title)}
    </h2>

    <div class="genre">
        {html.escape(game.genre)}
    </div>

    <p>
        {html.escape(game.description)}
    </p>

    <span class="play">
        PLAY
    </span>

</a>
""")

    page = f"""<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1">

<title>AJVYRA — Games</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    min-height: 100vh;

    background: #000;
    color: #fff;

    font-family:
        Arial,
        Helvetica,
        sans-serif;
}}

header {{
    padding: 45px 7vw 25px;
}}

.logo {{
    font-weight: 900;
    letter-spacing: 7px;
    font-size: 30px;
}}

h1 {{
    font-size: clamp(42px, 8vw, 90px);
    margin: 35px 0 10px;
}}

.subtitle {{
    color: #888;
    max-width: 650px;
    line-height: 1.7;
}}

.games {{
    padding: 35px 7vw 80px;

    display: grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(250px, 1fr)
        );

    gap: 18px;
}}

.game-card {{
    position: relative;

    display: block;

    min-height: 260px;

    padding: 24px;

    color: white;

    text-decoration: none;

    background:
        linear-gradient(
            145deg,
            #171717,
            #070707
        );

    border:
        1px solid #242424;

    border-radius: 20px;

    transition:
        transform .2s,
        border-color .2s;
}}

.game-card:hover {{
    transform: translateY(-5px);
    border-color: #666;
}}

.number {{
    color: #666;
    font-size: 13px;
    letter-spacing: 2px;
}}

.game-card h2 {{
    margin-top: 25px;
    margin-bottom: 10px;
}}

.genre {{
    color: #aaa;
    font-size: 13px;
}}

.game-card p {{
    color: #888;
    line-height: 1.6;
}}

.play {{
    position: absolute;

    bottom: 22px;
    right: 22px;

    font-weight: 900;
    letter-spacing: 2px;
}}

</style>

</head>

<body>

<header>

<div class="logo">
AJVYRA
</div>

<h1>
GAMES
</h1>

<div class="subtitle">
30 browser-playable AJVYRA games.
Choose a game and play directly inside the website.
No installation required.
</div>

</header>

<main class="games">

{''.join(cards)}

</main>

</body>

</html>
"""

    output = (
        OUTPUT_ROOT.parent /
        "index.html"
    )

    output.write_text(
        page,
        encoding="utf-8"
    )

    return output


# ============================================================
# FINAL CHECK
# ============================================================

def final_check(
    built_games: list[tuple[BrowserGame, Path]]
) -> dict:

    valid = 0
    invalid = []

    for game, path in built_games:

        errors = validate_game(path)

        if errors:
            invalid.append({
                "game": game.number,
                "title": game.title,
                "errors": errors,
            })
        else:
            valid += 1

    return {

        "project": "AJVYRA",

        "browser_games_required": GAME_COUNT,

        "browser_games_built":
            len(built_games),

        "browser_games_valid":
            valid,

        "browser_games_invalid":
            len(invalid),

        "release_ready":
            len(built_games) == GAME_COUNT
            and valid == GAME_COUNT,

        "invalid_games":
            invalid,

    }


# ============================================================
# MAIN
# ============================================================

def main() -> int:

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    built = []

    for game in GAMES:

        path = build_game(game)

        built.append(
            (game, path)
        )

    manifest = build_manifest(built)

    hub = build_hub(GAMES)

    status = final_check(built)

    status_path = (
        OUTPUT_ROOT.parent /
        "AJVYRA_BROWSER_GAMES_STATUS_V4.json"
    )

    status_path.write_text(
        json.dumps(
            status,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

    print("=" * 60)

    print("AJVYRA BROWSER GAME BUILD")

    print("=" * 60)

    print(
        f"Games built: "
        f"{status['browser_games_built']}/30"
    )

    print(
        f"Games valid: "
        f"{status['browser_games_valid']}/30"
    )

    print(
        f"Games invalid: "
        f"{status['browser_games_invalid']}"
    )

    print(
        f"Release ready: "
        f"{status['release_ready']}"
    )

    print(
        f"Hub: {hub}"
    )

    print(
        f"Manifest: {manifest}"
    )

    print(
        f"Status: {status_path}"
    )

    print("=" * 60)

    return 0 if status["release_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
