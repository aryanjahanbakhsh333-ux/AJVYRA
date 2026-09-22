from pathlib import Path
import json
import html


class AJVYRAFinalGameCompiler:
    """
    Final compiler for AJVYRA browser games.

    Produces a self-contained playable HTML5 game:
        index.html
        game.js
        game.css
        metadata.json
    """

    GENRE_RULES = {
        "rpg": {
            "objective": "Defeat enemies and reach the boss.",
            "color": "#6d5dfc",
            "mechanic": "combat",
        },
        "platformer": {
            "objective": "Jump across platforms and reach the exit.",
            "color": "#3f8cff",
            "mechanic": "platformer",
        },
        "horror": {
            "objective": "Find the key and escape before the darkness catches you.",
            "color": "#541f63",
            "mechanic": "horror",
        },
        "racing": {
            "objective": "Pass checkpoints and finish the race.",
            "color": "#e05b35",
            "mechanic": "racing",
        },
        "puzzle": {
            "objective": "Solve the board before the move limit ends.",
            "color": "#36a269",
            "mechanic": "puzzle",
        },
        "survival": {
            "objective": "Survive increasingly difficult enemy waves.",
            "color": "#c38b31",
            "mechanic": "survival",
        },
        "adventure": {
            "objective": "Explore the world and discover hidden locations.",
            "color": "#3b9b91",
            "mechanic": "adventure",
        },
        "shooter": {
            "objective": "Destroy enemy waves.",
            "color": "#b83b4b",
            "mechanic": "shooter",
        },
        "stealth": {
            "objective": "Reach the objective without being detected.",
            "color": "#354052",
            "mechanic": "stealth",
        },
        "runner": {
            "objective": "Run as far as possible without hitting obstacles.",
            "color": "#d39a36",
            "mechanic": "runner",
        },
    }

    def compile(
        self,
        output_dir: str,
        game_id: int,
        title: str,
        genre: str,
        seed: int,
        difficulty: float = 1.0,
    ):
        genre = genre.lower().strip()

        if genre not in self.GENRE_RULES:
            raise ValueError(f"Unsupported genre: {genre}")

        root = Path(output_dir)
        root.mkdir(parents=True, exist_ok=True)

        rule = self.GENRE_RULES[genre]

        metadata = {
            "id": game_id,
            "title": title,
            "genre": genre,
            "seed": seed,
            "difficulty": difficulty,
            "engine": "AJVYRA_FINAL_HTML5",
            "playable": True,
            "mobile": True,
            "desktop": True,
            "gamepad": True,
            "save_system": "localStorage",
            "objective": rule["objective"],
        }

        (root / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        css = self._css(rule["color"])
        js = self._javascript(
            game_id,
            title,
            genre,
            seed,
            difficulty,
        )

        page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
      content="width=device-width,
               initial-scale=1,
               maximum-scale=1,
               user-scalable=no">

<title>{html.escape(title)}</title>

<link rel="stylesheet" href="game.css">
</head>

<body>

<div id="hud">
    <strong>{html.escape(title)}</strong>
    <span id="genre">{genre.upper()}</span>
    <span id="score">0</span>
    <span id="status">READY</span>
</div>

<canvas id="game"></canvas>

<div id="touch">
    <button data-key="ArrowLeft">◀</button>
    <button data-key="ArrowUp">▲</button>
    <button data-key="ArrowDown">▼</button>
    <button data-key="ArrowRight">▶</button>
    <button id="action">ACTION</button>
</div>

<div id="menu">
    <h1>{html.escape(title)}</h1>
    <p id="objective">{html.escape(rule["objective"])}</p>
    <button id="start">START</button>
    <button id="continue">CONTINUE</button>
</div>

<script>
window.AJVYRA_CONFIG = {json.dumps(metadata, ensure_ascii=False)};
</script>

<script src="game.js"></script>

</body>
</html>
"""

        (root / "index.html").write_text(
            page,
            encoding="utf-8",
        )

        (root / "game.css").write_text(
            css,
            encoding="utf-8",
        )

        (root / "game.js").write_text(
            js,
            encoding="utf-8",
        )

        return root

    def _css(self, accent: str):
        return f"""
:root {{
    --accent: {accent};
}}

* {{
    box-sizing: border-box;
}}

html,
body {{
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #080a10;
    color: white;
    font-family: Arial, sans-serif;
    touch-action: none;
}}

body {{
    position: relative;
}}

canvas {{
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    display: block;
}}

#hud {{
    position: fixed;
    top: 12px;
    left: 12px;
    right: 12px;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    font-size: 13px;
    pointer-events: none;
}}

#hud strong {{
    color: var(--accent);
}}

#touch {{
    position: fixed;
    left: 0;
    right: 0;
    bottom: 18px;
    z-index: 20;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
}}

#touch button,
#menu button {{
    border: 1px solid rgba(255,255,255,.18);
    background: rgba(20,24,35,.82);
    color: white;
    border-radius: 14px;
    min-width: 58px;
    min-height: 52px;
    font-weight: bold;
}}

#touch button:active,
#menu button:active {{
    transform: scale(.96);
}}

#action {{
    min-width: 90px !important;
}}

#menu {{
    position: fixed;
    inset: 0;
    z-index: 30;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 25px;
    background: rgba(3,5,10,.90);
}}

#menu.hidden {{
    display: none;
}}

#menu h1 {{
    margin-bottom: 8px;
}}

#objective {{
    max-width: 480px;
    opacity: .8;
    line-height: 1.5;
}}

#menu button {{
    margin-top: 10px;
    padding: 10px 24px;
}}
"""

    def _javascript(
        self,
        game_id: int,
        title: str,
        genre: str,
        seed: int,
        difficulty: float,
    ):
        return f"""
(() => {{
"use strict";

const CFG = window.AJVYRA_CONFIG;
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 0;
let H = 0;
let running = false;
let paused = false;
let lastTime = 0;

const input = new Set();

const game = {{
    score: 0,
    level: 1,
    hp: 100,
    lives: 3,
    progress: 0,
    elapsed: 0,
    battery: 100,
    moves: 40,
    distance: 0,
    checkpoints: 0,
    detected: 0,
    wave: 1,
    won: false,
    lost: false,
}};

const player = {{
    x: 0,
    y: 0,
    w: 28,
    h: 28,
    vx: 0,
    vy: 0,
    speed: 260,
    jump: -560,
    grounded: false,
}};

let enemies = [];
let objects = [];
let particles = [];
let platforms = [];

function resize() {{
    W = window.innerWidth;
    H = window.innerHeight;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);

    canvas.width = Math.floor(W * dpr);
    canvas.height = Math.floor(H * dpr);

    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    if (!running) resetWorld();
}}

window.addEventListener("resize", resize);

function resetWorld() {{
    player.x = W / 2;
    player.y = H / 2;
    player.vx = 0;
    player.vy = 0;

    enemies = [];
    objects = [];
    particles = [];
    platforms = [];

    game.score = 0;
    game.level = 1;
    game.hp = 100;
    game.lives = 3;
    game.progress = 0;
    game.elapsed = 0;
    game.battery = 100;
    game.moves = 40;
    game.distance = 0;
    game.checkpoints = 0;
    game.detected = 0;
    game.wave = 1;
    game.won = false;
    game.lost = false;

    if (CFG.genre === "platformer") {{
        createPlatforms();
    }}

    if (CFG.genre === "puzzle") {{
        createPuzzle();
    }}

    if (CFG.genre === "racing") {{
        createRace();
    }}

    if (CFG.genre === "horror") {{
        createKey();
    }}
}}

function rand(min, max) {{
    return Math.random() * (max - min) + min;
}}

function clamp(value, min, max) {{
    return Math.max(min, Math.min(max, value));
}}

function rectHit(a, b) {{
    return (
        a.x < b.x + b.w &&
        a.x + a.w > b.x &&
        a.y < b.y + b.h &&
        a.y + a.h > b.y
    );
}}

function spawnEnemy() {{
    enemies.push({{
        x: rand(20, W - 40),
        y: -40,
        w: 24,
        h: 24,
        speed: rand(55, 100) * CFG.difficulty,
        hp: 1
    }});
}}

function createPlatforms() {{
    for (let i = 0; i < 12; i++) {{
        platforms.push({{
            x: i * (W / 10),
            y: H - 100 - ((i * 47) % 180),
            w: 110,
            h: 18
        }});
    }}
}}

function createKey() {{
    objects.push({{
        type: "key",
        x: rand(50, W - 80),
        y: rand(80, H - 160),
        w: 22,
        h: 22
    }});
}}

function createRace() {{
    for (let i = 0; i < 8; i++) {{
        objects.push({{
            type: "checkpoint",
            x: rand(80, W - 100),
            y: rand(80, H - 140),
            w: 35,
            h: 35
        }});
    }}
}}

function createPuzzle() {{
    objects = [];

    const size = 5;
    const gap = 8;
    const cell = Math.min(62, W / 7);

    const startX = (W - size * cell) / 2;
    const startY = (H - size * cell) / 2;

    for (let y = 0; y < size; y++) {{
        for (let x = 0; x < size; x++) {{
            objects.push({{
                type: "tile",
                x: startX + x * cell + gap,
                y: startY + y * cell + gap,
                w: cell - gap * 2,
                h: cell - gap * 2,
                active: Math.random() > .45
            }});
        }}
    }}
}}

function action() {{
    if (!running) return;

    if (CFG.genre === "rpg" ||
        CFG.genre === "shooter") {{
        for (let i = enemies.length - 1; i >= 0; i--) {{
            const e = enemies[i];

            const dx = e.x - player.x;
            const dy = e.y - player.y;
            const d = Math.hypot(dx, dy);

            if (d < 130) {{
                enemies.splice(i, 1);
                game.score += 50;
                burst(e.x, e.y);
                break;
            }}
        }}
    }}

    if (CFG.genre === "puzzle") {{
        const tile = objects.find(o =>
            o.type === "tile" &&
            Math.hypot(
                o.x + o.w / 2 - player.x,
                o.y + o.h / 2 - player.y
            ) < 100
        );

        if (tile) {{
            tile.active = !tile.active;
            game.moves--;

            const active = objects.filter(
                o => o.type === "tile" && o.active
            ).length;

            game.progress =
                ((25 - active) / 25) * 100;

            if (active === 0) {{
                win();
            }}
        }}
    }}
}}

function update(dt) {{
    game.elapsed += dt;

    if (CFG.genre === "platformer") {{
        updatePlatformer(dt);
    }} else if (CFG.genre === "racing") {{
        updateRacing(dt);
    }} else if (CFG.genre === "puzzle") {{
        updatePuzzle(dt);
    }} else if (CFG.genre === "horror") {{
        updateHorror(dt);
    }} else if (CFG.genre === "stealth") {{
        updateStealth(dt);
    }} else if (CFG.genre === "runner") {{
        updateRunner(dt);
    }} else if (CFG.genre === "survival") {{
        updateSurvival(dt);
    }} else {{
        updateCombat(dt);
    }}

    updateParticles(dt);

    if (game.hp <= 0 || game.lives <= 0) {{
        lose();
    }}

    saveGame();
}}

function movePlayer(dt) {{
    let x = 0;
    let y = 0;

    if (input.has("ArrowLeft") || input.has("a")) x--;
    if (input.has("ArrowRight") || input.has("d")) x++;
    if (input.has("ArrowUp") || input.has("w")) y--;
    if (input.has("ArrowDown") || input.has("s")) y++;

    const length = Math.hypot(x, y) || 1;

    player.x += x / length * player.speed * dt;
    player.y += y / length * player.speed * dt;

    player.x = clamp(player.x, 0, W - player.w);
    player.y = clamp(player.y, 0, H - player.h);
}}

function updateCombat(dt) {{
    movePlayer(dt);

    if (Math.random() < dt * CFG.difficulty) {{
        spawnEnemy();
    }}

    for (const e of enemies) {{
        const dx = player.x - e.x;
        const dy = player.y - e.y;
        const d = Math.hypot(dx, dy) || 1;

        e.x += dx / d * e.speed * dt;
        e.y += dy / d * e.speed * dt;

        if (rectHit(player, e)) {{
            e.hp = 0;
            game.hp -= 10 * dt;
        }}
    }}

    enemies = enemies.filter(e => e.hp > 0);

    game.progress = Math.min(
        100,
        game.score / 1000 * 100
    );

    if (game.progress >= 100) win();
}}

function updatePlatformer(dt) {{
    let horizontal = 0;

    if (input.has("ArrowLeft") || input.has("a"))
        horizontal--;

    if (input.has("ArrowRight") || input.has("d"))
        horizontal++;

    player.vx = horizontal * player.speed;

    if (
        (input.has("ArrowUp") ||
         input.has("w")) &&
        player.grounded
    ) {{
        player.vy = player.jump;
        player.grounded = false;
    }}

    player.vy += 1500 * dt;

    player.x += player.vx * dt;
    player.y += player.vy * dt;

    player.grounded = false;

    for (const p of platforms) {{
        if (
            player.x < p.x + p.w &&
            player.x + player.w > p.x &&
            player.y + player.h >= p.y &&
            player.y + player.h <= p.y + 30 &&
            player.vy >= 0
        ) {{
            player.y = p.y - player.h;
            player.vy = 0;
            player.grounded = true;
        }}
    }}

    if (player.y > H + 100) {{
        game.lives--;
        player.x = 40;
        player.y = H / 2;
        player.vy = 0;
    }}

    game.progress =
        clamp(player.x / Math.max(W * 3, 1) * 100, 0, 100);

    if (game.progress >= 100) win();
}}

function updateRacing(dt) {{
    movePlayer(dt);

    if (input.has("ArrowUp") || input.has("w")) {{
        game.distance += 350 * dt;
        game.score += 20 * dt;
    }} else {{
        game.distance += 80 * dt;
    }}

    for (const c of objects) {{
        if (c.type !== "checkpoint") continue;

        if (!c.hit && rectHit(player, c)) {{
            c.hit = true;
            game.checkpoints++;
            game.score += 150;
        }}
    }}

    game.progress =
        Math.min(
            100,
            game.checkpoints /
            Math.max(objects.length, 1) *
            100
        );

    if (game.checkpoints >= objects.length) win();
}}

function updatePuzzle(dt) {{
    movePlayer(dt);

    if (game.moves <= 0) lose();
}}

function updateHorror(dt) {{
    movePlayer(dt);

    game.battery =
        Math.max(0, game.battery - dt * 2);

    const key = objects.find(o => o.type === "key");

    if (key && rectHit(player, key)) {{
        key.collected = true;
        game.progress = 100;
        win();
    }}

    if (game.battery <= 0) {{
        game.hp -= 12 * dt;
    }}
}}

function updateStealth(dt) {{
    movePlayer(dt);

    if (Math.random() < dt * .25) {{
        game.detected += 4;
    }} else {{
        game.detected =
            Math.max(0, game.detected - dt * 6);
    }}

    if (game.detected >= 100) {{
        game.lives--;
        game.detected = 0;
    }}

    game.progress =
        Math.min(100, player.x / W * 100);

    if (game.progress >= 100) win();
}}

function updateRunner(dt) {{
    player.y = H - 140;

    game.distance +=
        (260 + game.elapsed * 8) * dt;

    game.score =
        Math.floor(game.distance / 5);

    if (Math.random() < dt * .8) {{
        objects.push({{
            type: "obstacle",
            x: W + 30,
            y: H - 150,
            w: 35,
            h: 35
        }});
    }}

    for (const o of objects) {{
        if (o.type === "obstacle") {{
            o.x -= (330 + game.elapsed * 8) * dt;

            if (rectHit(player, o)) {{
                o.hit = true;
                game.lives--;
            }}
        }}
    }}

    objects = objects.filter(
        o => o.x > -100 && !o.hit
    );

    if (game.distance >= 5000) win();
}}

function updateSurvival(dt) {{
    movePlayer(dt);

    if (Math.random() <
        dt * (0.7 + game.wave * .1)) {{
        spawnEnemy();
    }}

    game.progress =
        Math.min(100, game.elapsed / 90 * 100);

    if (game.elapsed >= 90) win();

    for (const e of enemies) {{
        const dx = player.x - e.x;
        const dy = player.y - e.y;
        const d = Math.hypot(dx, dy) || 1;

        e.x += dx / d * e.speed * dt;
        e.y += dy / d * e.speed * dt;

        if (rectHit(player, e)) {{
            game.hp -= 15 * dt;
        }}
    }}
}}

function burst(x, y) {{
    for (let i = 0; i < 10; i++) {{
        particles.push({{
            x,
            y,
            vx: rand(-120, 120),
            vy: rand(-120, 120),
            life: 1
        }});
    }}
}}

function updateParticles(dt) {{
    for (const p of particles) {{
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.life -= dt * 2;
    }}

    particles =
        particles.filter(p => p.life > 0);
}}

function draw() {{
    ctx.clearRect(0, 0, W, H);

    drawBackground();

    if (CFG.genre === "platformer") {{
        drawPlatforms();
    }}

    if (CFG.genre === "puzzle") {{
        drawPuzzle();
    }}

    if (CFG.genre === "racing") {{
        drawRace();
    }}

    if (CFG.genre === "horror") {{
        drawHorrorObjects();
    }}

    if (CFG.genre === "runner") {{
        drawRunnerObjects();
    }}

    drawEnemies();
    drawPlayer();
    drawParticles();

    if (CFG.genre === "horror") {{
        drawDarkness();
    }}
}}

function drawBackground() {{
    ctx.fillStyle = "#0b1020";
    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle = "rgba(255,255,255,.035)";

    for (let x = 0; x < W; x += 60) {{
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, H);
        ctx.stroke();
    }}

    for (let y = 0; y < H; y += 60) {{
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();
    }}
}}

function drawPlayer() {{
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(
        player.x,
        player.y,
        player.w,
        player.h
    );
}}

function drawEnemies() {{
    ctx.fillStyle = "#d94d65";

    for (const e of enemies) {{
        ctx.fillRect(
            e.x,
            e.y,
            e.w,
            e.h
        );
    }}
}}

function drawPlatforms() {{
    ctx.fillStyle = "#3d6fbd";

    for (const p of platforms) {{
        ctx.fillRect(
            p.x,
            p.y,
            p.w,
            p.h
        );
    }}
}}

function drawPuzzle() {{
    for (const o of objects) {{
        if (o.type !== "tile") continue;

        ctx.fillStyle =
            o.active ? "#4da879" : "#202838";

        ctx.fillRect(
            o.x,
            o.y,
            o.w,
            o.h
        );
    }}
}}

function drawRace() {{
    ctx.strokeStyle = "#6d7380";
    ctx.lineWidth = 5;

    for (const o of objects) {{
        if (o.type !== "checkpoint") continue;

        ctx.strokeRect(
            o.x,
            o.y,
            o.w,
            o.h
        );
    }}

    ctx.lineWidth = 1;
}}

function drawHorrorObjects() {{
    for (const o of objects) {{
        if (o.type !== "key" || o.collected) continue;

        ctx.fillStyle = "#e8d35b";
        ctx.fillRect(
            o.x,
            o.y,
            o.w,
            o.h
        );
    }}
}}

function drawRunnerObjects() {{
    ctx.fillStyle = "#d96f45";

    for (const o of objects) {{
        if (o.type === "obstacle") {{
            ctx.fillRect(
                o.x,
                o.y,
                o.w,
                o.h
            );
        }}
    }}
}}

function drawParticles() {{
    for (const p of particles) {{
        ctx.globalAlpha = p.life;
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(p.x, p.y, 4, 4);
    }}

    ctx.globalAlpha = 1;
}}

function drawDarkness() {{
    const gradient =
        ctx.createRadialGradient(
            player.x + player.w / 2,
            player.y + player.h / 2,
            25,
            player.x + player.w / 2,
            player.y + player.h / 2,
            260
        );

    gradient.addColorStop(
        0,
        "rgba(255,255,255,.16)"
    );

    gradient.addColorStop(
        1,
        "rgba(0,0,0,.96)"
    );

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, W, H);
}}

function win() {{
    if (game.won || game.lost) return;

    game.won = true;
    running = false;

    document.getElementById("status").textContent =
        "VICTORY";

    showMenu("VICTORY", "PLAY AGAIN");
    saveGame();
}}

function lose() {{
    if (game.won || game.lost) return;

    game.lost = true;
    running = false;

    document.getElementById("status").textContent =
        "GAME OVER";

    showMenu("GAME OVER", "RESTART");
    saveGame();
}}

function showMenu(title, button) {{
    const menu = document.getElementById("menu");

    menu.classList.remove("hidden");

    menu.querySelector("h1").textContent = title;
    document.getElementById("start").textContent = button;
}}

function startGame(load = false) {{
    if (!load) resetWorld();

    document.getElementById("menu")
        .classList.add("hidden");

    running = true;
    game.won = false;
    game.lost = false;

    document.getElementById("status")
        .textContent = "PLAYING";

    lastTime = performance.now();

    requestAnimationFrame(loop);
}}

function loop(timestamp) {{
    if (!running) {{
        draw();
        return;
    }}

    const dt =
        Math.min(
            (timestamp - lastTime) / 1000,
            .05
        );

    lastTime = timestamp;

    update(dt);
    draw();

    document.getElementById("score")
        .textContent =
        Math.floor(game.score);

    requestAnimationFrame(loop);
}}

function saveGame() {{
    try {{
        localStorage.setItem(
            "ajvyra_game_{game_id}",
            JSON.stringify(game)
        );
    }} catch (_) {{}}
}}

function loadGame() {{
    try {{
        const raw =
            localStorage.getItem(
                "ajvyra_game_{game_id}"
            );

        if (!raw) return false;

        Object.assign(game, JSON.parse(raw));
        return true;
    }} catch (_) {{
        return false;
    }}
}}

document.addEventListener(
    "keydown",
    event => {{
        input.add(event.key);

        if (event.key === " ") {{
            event.preventDefault();
            action();
        }}

        if (event.key === "Escape") {{
            paused = !paused;
        }}
    }}
);

document.addEventListener(
    "keyup",
    event => {{
        input.delete(event.key);
    }}
);

document.querySelectorAll(
    "#touch button[data-key]"
).forEach(button => {{
    const key = button.dataset.key;

    button.addEventListener(
        "pointerdown",
        e => {{
            e.preventDefault();
            input.add(key);
        }}
    );

    const release = e => {{
        e.preventDefault();
        input.delete(key);
    }};

    button.addEventListener(
        "pointerup",
        release
    );

    button.addEventListener(
        "pointercancel",
        release
    );

    button.addEventListener(
        "pointerleave",
        release
    );
}});

document.getElementById("action")
    .addEventListener(
        "pointerdown",
        e => {{
            e.preventDefault();
            action();
        }}
    );

document.getElementById("start")
    .addEventListener(
        "click",
        () => startGame(false)
    );

document.getElementById("continue")
    .addEventListener(
        "click",
        () => {{
            if (loadGame()) {{
                startGame(true);
            }} else {{
                startGame(false);
            }}
        }}
    );

resize();
draw();

}})();
"""
