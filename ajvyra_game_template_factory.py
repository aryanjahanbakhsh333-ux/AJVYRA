import json
from pathlib import Path
from typing import Dict


class AJVYGameTemplateFactory:
    """
    Generates playable HTML5 game templates.

    The generated game runs independently in a browser.
    """

    def build(
        self,
        output_dir: Path,
        game_id: int,
        title: str,
        genre: str,
        profile: Dict,
        objective: str,
        seed: int,
    ) -> Path:

        output_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "game_id": game_id,
            "title": title,
            "genre": genre,
            "objective": objective,
            "seed": seed,
            "mobile": True,
            "playable": True,
            "runtime": "html5_canvas",
        }

        (output_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width,initial-scale=1,
    maximum-scale=1,user-scalable=no"
>
<title>{title}</title>
<link rel="stylesheet" href="game.css">
</head>

<body>

<div id="hud">
    <span id="title">{title}</span>
    <span id="status">READY</span>
    <span id="score">Score: 0</span>
</div>

<canvas id="game"></canvas>

<div id="controls">
    <button id="left">◀</button>
    <button id="action">●</button>
    <button id="right">▶</button>
</div>

<div id="overlay">
    <h1 id="message">{title}</h1>
    <p id="objective">{objective}</p>
    <button id="start">START</button>
</div>

<script>
window.AJVYRA_GAME_CONFIG = {json.dumps({
    "game_id": game_id,
    "title": title,
    "genre": genre,
    "objective": objective,
    "player_speed": profile.get("player_speed", 3),
    "enemy_speed": profile.get("enemy_speed", 1.5),
    "spawn_rate": profile.get("spawn_rate", 2),
    "health": profile.get("health", 100),
    "score_multiplier": profile.get("score_multiplier", 1),
    "seed": seed,
}, ensure_ascii=False)};
</script>

<script src="game.js"></script>
</body>
</html>
"""

        css = """
html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #090b12;
    color: white;
    font-family: Arial, sans-serif;
    touch-action: none;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
}

canvas {
    width: 100vw;
    height: 100vh;
    display: block;
    background: #101522;
}

#hud {
    position: fixed;
    top: 10px;
    left: 12px;
    right: 12px;
    z-index: 5;
    display: flex;
    justify-content: space-between;
    gap: 10px;
    pointer-events: none;
    font-size: 14px;
}

#controls {
    position: fixed;
    bottom: 20px;
    left: 0;
    right: 0;
    z-index: 10;
    display: flex;
    justify-content: center;
    gap: 25px;
}

#controls button,
#start {
    border: 0;
    border-radius: 50%;
    min-width: 64px;
    min-height: 64px;
    background: rgba(255,255,255,.15);
    color: white;
    font-size: 24px;
}

#start {
    border-radius: 12px;
    padding: 12px 30px;
    min-width: 120px;
    min-height: auto;
}

#overlay {
    position: fixed;
    inset: 0;
    z-index: 20;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: rgba(0,0,0,.72);
}

#overlay.hidden {
    display: none;
}
"""

        js = f"""
(() => {{
    const cfg = window.AJVYRA_GAME_CONFIG;

    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    const scoreEl = document.getElementById("score");
    const statusEl = document.getElementById("status");
    const overlay = document.getElementById("overlay");
    const message = document.getElementById("message");
    const startButton = document.getElementById("start");

    let width = 0;
    let height = 0;

    let running = false;
    let lastTime = 0;
    let score = 0;
    let elapsed = 0;

    const keys = {{}};
    const enemies = [];
    const particles = [];

    const player = {{
        x: 0,
        y: 0,
        size: 24,
        speed: cfg.player_speed,
        hp: cfg.health,
        cooldown: 0
    }};

    function resize() {{
        canvas.width = window.innerWidth * devicePixelRatio;
        canvas.height = window.innerHeight * devicePixelRatio;

        width = window.innerWidth;
        height = window.innerHeight;

        ctx.setTransform(
            devicePixelRatio,
            0,
            0,
            devicePixelRatio,
            0,
            0
        );

        player.x = width / 2;
        player.y = height / 2;
    }}

    window.addEventListener("resize", resize);
    resize();

    function random(min, max) {{
        return Math.random() * (max - min) + min;
    }}

    function spawnEnemy() {{
        const side = Math.floor(Math.random() * 4);

        let x;
        let y;

        if (side === 0) {{
            x = random(0, width);
            y = -30;
        }} else if (side === 1) {{
            x = width + 30;
            y = random(0, height);
        }} else if (side === 2) {{
            x = random(0, width);
            y = height + 30;
        }} else {{
            x = -30;
            y = random(0, height);
        }}

        enemies.push({{
            x,
            y,
            size: random(15, 30),
            speed: cfg.enemy_speed * random(.75, 1.25),
            hp: 1
        }});
    }}

    function distance(a, b) {{
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        return Math.sqrt(dx * dx + dy * dy);
    }}

    function shoot() {{
        for (let i = enemies.length - 1; i >= 0; i--) {{
            if (distance(player, enemies[i]) < 100) {{
                enemies.splice(i, 1);
                score += Math.round(10 * cfg.score_multiplier);
                createParticles(player.x, player.y);
                return;
            }}
        }}
    }}

    function createParticles(x, y) {{
        for (let i = 0; i < 8; i++) {{
            particles.push({{
                x,
                y,
                vx: random(-2, 2),
                vy: random(-2, 2),
                life: 1
            }});
        }}
    }}

    function update(dt) {{
        elapsed += dt;

        let dx = 0;
        let dy = 0;

        if (keys["ArrowLeft"] || keys["a"]) dx -= 1;
        if (keys["ArrowRight"] || keys["d"]) dx += 1;
        if (keys["ArrowUp"] || keys["w"]) dy -= 1;
        if (keys["ArrowDown"] || keys["s"]) dy += 1;

        const length = Math.sqrt(dx * dx + dy * dy) || 1;

        player.x += (dx / length) * player.speed * 60 * dt;
        player.y += (dy / length) * player.speed * 60 * dt;

        player.x = Math.max(15, Math.min(width - 15, player.x));
        player.y = Math.max(15, Math.min(height - 15, player.y));

        if (
            elapsed >
            cfg.spawn_rate &&
            cfg.genre !== "puzzle"
        ) {{
            elapsed = 0;
            spawnEnemy();
        }}

        for (const enemy of enemies) {{
            const dx = player.x - enemy.x;
            const dy = player.y - enemy.y;
            const len = Math.sqrt(dx * dx + dy * dy) || 1;

            enemy.x += dx / len * enemy.speed * 60 * dt;
            enemy.y += dy / len * enemy.speed * 60 * dt;
        }}

        for (let i = enemies.length - 1; i >= 0; i--) {{
            if (distance(player, enemies[i]) < 25) {{
                enemies.splice(i, 1);
                player.hp -= 10;

                if (player.hp <= 0) {{
                    endGame(false);
                    return;
                }}
            }}
        }}

        for (let i = particles.length - 1; i >= 0; i--) {{
            const p = particles[i];

            p.x += p.vx;
            p.y += p.vy;
            p.life -= dt * 2;

            if (p.life <= 0) {{
                particles.splice(i, 1);
            }}
        }}

        if (cfg.genre === "racing") {{
            score += dt * 20;
        }} else {{
            score += dt * 2;
        }}

        scoreEl.textContent =
            "Score: " + Math.floor(score);
    }}

    function render() {{
        ctx.clearRect(0, 0, width, height);

        ctx.fillStyle = "#101522";
        ctx.fillRect(0, 0, width, height);

        drawBackground();

        for (const enemy of enemies) {{
            ctx.fillStyle = "#c94c6d";
            ctx.beginPath();
            ctx.arc(
                enemy.x,
                enemy.y,
                enemy.size,
                0,
                Math.PI * 2
            );
            ctx.fill();
        }}

        for (const p of particles) {{
            ctx.globalAlpha = p.life;
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(p.x, p.y, 4, 4);
        }}

        ctx.globalAlpha = 1;

        ctx.fillStyle = "#ffffff";
        ctx.beginPath();
        ctx.arc(
            player.x,
            player.y,
            player.size / 2,
            0,
            Math.PI * 2
        );
        ctx.fill();

        if (cfg.genre === "horror") {{
            ctx.fillStyle = "rgba(0,0,0,.72)";
            ctx.fillRect(0, 0, width, height);

            const gradient = ctx.createRadialGradient(
                player.x,
                player.y,
                30,
                player.x,
                player.y,
                240
            );

            gradient.addColorStop(0, "rgba(255,255,255,.20)");
            gradient.addColorStop(1, "rgba(0,0,0,.95)");

            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, width, height);
        }}
    }}

    function drawBackground() {{
        if (cfg.genre === "racing") {{
            ctx.strokeStyle = "rgba(255,255,255,.08)";

            for (let x = 0; x < width; x += 50) {{
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, height);
                ctx.stroke();
            }}

            return;
        }}

        if (cfg.genre === "platformer") {{
            ctx.fillStyle = "#18233a";

            for (let x = 0; x < width; x += 120) {{
                ctx.fillRect(
                    x,
                    height - 80,
                    90,
                    18
                );
            }}

            return;
        }}

        ctx.strokeStyle = "rgba(255,255,255,.035)";

        for (let x = 0; x < width; x += 60) {{
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }}

        for (let y = 0; y < height; y += 60) {{
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }}
    }}

    function loop(timestamp) {{
        if (!running) return;

        const dt = Math.min(
            (timestamp - lastTime) / 1000,
            0.05
        );

        lastTime = timestamp;

        update(dt);
        render();

        requestAnimationFrame(loop);
    }}

    function startGame() {{
        score = 0;
        elapsed = 0;

        player.hp = cfg.health;
        player.x = width / 2;
        player.y = height / 2;

        enemies.length = 0;
        particles.length = 0;

        running = true;

        overlay.classList.add("hidden");
        statusEl.textContent = "PLAYING";

        lastTime = performance.now();
        requestAnimationFrame(loop);
    }}

    function endGame(won) {{
        running = false;

        statusEl.textContent = won ? "WIN" : "GAME OVER";

        message.textContent =
            won ? "VICTORY" : "GAME OVER";

        startButton.textContent = "RESTART";

        overlay.classList.remove("hidden");
    }}

    startButton.addEventListener("click", startGame);

    document.addEventListener("keydown", event => {{
        keys[event.key] = true;

        if (event.key === " ") {{
            event.preventDefault();
            shoot();
        }}
    }});

    document.addEventListener("keyup", event => {{
        keys[event.key] = false;
    }});

    function bindButton(id, key) {{
        const button = document.getElementById(id);

        button.addEventListener("pointerdown", event => {{
            event.preventDefault();
            keys[key] = true;
        }});

        button.addEventListener("pointerup", event => {{
            event.preventDefault();
            keys[key] = false;
        }});

        button.addEventListener("pointercancel", () => {{
            keys[key] = false;
        }});
    }}

    bindButton("left", "ArrowLeft");
    bindButton("right", "ArrowRight");

    document
        .getElementById("action")
        .addEventListener("pointerdown", event => {{
            event.preventDefault();
            shoot();
        }});

    statusEl.textContent = "READY";
}})();
"""

        (output_dir / "index.html").write_text(
            html,
            encoding="utf-8",
        )

        (output_dir / "game.css").write_text(
            css,
            encoding="utf-8",
        )

        (output_dir / "game.js").write_text(
            js,
            encoding="utf-8",
        )

        return output_dir
