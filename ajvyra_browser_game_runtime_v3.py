"""
AJVYRA Browser Game Runtime v3

Creates a real HTML5 Canvas runtime for AJVYRA games.
No paid API. No external game service.

The runtime supports:
- keyboard
- touch
- virtual joystick
- action button
- restart
- pause
- game-over / victory
- deterministic game definitions
"""

from __future__ import annotations

import html
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class BrowserGame:
    number: int
    title: str
    genre: str
    description: str
    mode: str
    goal: int


GAMES: List[BrowserGame] = [
    BrowserGame(1, "Black Run", "Arcade / Platformer", "Collect energy and reach the gate.", "collect", 8),
    BrowserGame(2, "Shadow Hunt", "Horror", "Find the keys while shadows chase you.", "hunt", 3),
    BrowserGame(3, "Neon Drift", "Racing", "Drive through checkpoints before time runs out.", "race", 12),
    BrowserGame(4, "Crystal Quest", "RPG / Adventure", "Collect crystals and defeat guardians.", "collect_combat", 10),
    BrowserGame(5, "Cipher Room", "Puzzle", "Activate switches in the correct sequence.", "switch", 4),
    BrowserGame(6, "Silent Step", "Stealth", "Reach the exit without entering enemy vision.", "stealth", 5),
    BrowserGame(7, "Meteor Zero", "Survival", "Survive falling meteors.", "survival", 25),
    BrowserGame(8, "Last Tower", "Action", "Defend the tower from incoming enemies.", "defense", 30),
    BrowserGame(9, "Lost Signal", "Mystery", "Locate signal fragments around the map.", "collect", 6),
    BrowserGame(10, "Void Arena", "Combat", "Survive waves of enemies.", "combat", 35),
    BrowserGame(11, "Frost Line", "Racing", "Cross icy checkpoints quickly.", "race", 12),
    BrowserGame(12, "Night Courier", "Adventure", "Deliver the package to the target.", "collect", 5),
    BrowserGame(13, "Red Maze", "Puzzle", "Escape the changing maze.", "maze", 3),
    BrowserGame(14, "Echo Cave", "Exploration", "Collect echoes before the cave closes.", "collect", 8),
    BrowserGame(15, "Iron Squad", "Strategy", "Protect your base and gather energy.", "defense", 30),
    BrowserGame(16, "Ghost Train", "Horror", "Escape the train while avoiding ghosts.", "hunt", 4),
    BrowserGame(17, "Skyfall", "Arcade", "Move through falling obstacles.", "survival", 25),
    BrowserGame(18, "Black Harbor", "Mystery", "Find three hidden clues.", "collect", 3),
    BrowserGame(19, "Pulse", "Rhythm / Skill", "Hit moving targets at the right time.", "pulse", 12),
    BrowserGame(20, "Dragon Core", "Action / Fantasy", "Defeat the core guardian.", "boss", 45),
    BrowserGame(21, "Deep One", "Survival", "Survive underwater hazards.", "survival", 20),
    BrowserGame(22, "Zero Gravity", "Arcade", "Collect stars in a floating arena.", "collect", 12),
    BrowserGame(23, "Hunter", "Combat", "Track targets and survive ambushes.", "combat", 25),
    BrowserGame(24, "Memory Grid", "Puzzle", "Remember and repeat the pattern.", "memory", 4),
    BrowserGame(25, "Desert Run", "Racing", "Cross the desert and avoid hazards.", "race", 20),
    BrowserGame(26, "Night Watch", "Defense", "Keep enemies away from the beacon.", "defense", 30),
    BrowserGame(27, "Phantom Key", "Stealth", "Find the key and escape unseen.", "stealth", 4),
    BrowserGame(28, "Star Forge", "Strategy", "Collect energy and build the forge.", "collect", 35),
    BrowserGame(29, "Final Gate", "Boss / Action", "Break through the guardian.", "boss", 60),
    BrowserGame(30, "AJVYRA Zero", "Mixed / Challenge", "A compact final challenge using multiple mechanics.", "mixed", 50),
]


def games_json() -> str:
    return json.dumps(
        [asdict(game) for game in GAMES],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def render_runtime(game: BrowserGame) -> str:
    data = html.escape(games_json(), quote=True)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport"
      content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>AJVYRA — {html.escape(game.title)}</title>
<style>
html,body {{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
    background:#050505;
    color:white;
    font-family:system-ui,sans-serif;
    touch-action:none;
}}
#game {{
    width:100vw;
    height:100vh;
    display:block;
    background:#070707;
}}
#hud {{
    position:fixed;
    left:0;
    top:0;
    width:100%;
    padding:10px 14px;
    box-sizing:border-box;
    pointer-events:none;
    display:flex;
    justify-content:space-between;
    font-size:14px;
    z-index:5;
}}
#touch {{
    position:fixed;
    inset:auto 0 18px 0;
    display:flex;
    justify-content:space-between;
    align-items:end;
    padding:0 20px;
    pointer-events:none;
    z-index:10;
}}
#stick {{
    width:112px;
    height:112px;
    border:2px solid #555;
    border-radius:50%;
    background:#111c;
    pointer-events:auto;
}}
#knob {{
    width:46px;
    height:46px;
    margin:31px;
    border-radius:50%;
    background:#ddd;
}}
#action {{
    width:92px;
    height:92px;
    border-radius:50%;
    border:2px solid #777;
    background:#181818;
    color:white;
    font-size:16px;
    pointer-events:auto;
}}
#pause {{
    position:fixed;
    right:14px;
    top:48px;
    z-index:20;
    background:#161616;
    color:white;
    border:1px solid #444;
    border-radius:8px;
    padding:8px 12px;
}}
#result {{
    position:fixed;
    inset:0;
    display:none;
    place-items:center;
    background:#000d;
    z-index:30;
    text-align:center;
}}
.panel {{
    padding:30px;
    border:1px solid #444;
    border-radius:16px;
    background:#0d0d0d;
}}
button {{
    cursor:pointer;
}}
</style>
</head>
<body>

<canvas id="game"></canvas>

<div id="hud">
    <div id="title"></div>
    <div id="stats"></div>
</div>

<button id="pause">PAUSE</button>

<div id="touch">
    <div id="stick"><div id="knob"></div></div>
    <button id="action">ACTION</button>
</div>

<div id="result">
    <div class="panel">
        <h1 id="resultTitle"></h1>
        <p id="resultScore"></p>
        <button onclick="restart()">RESTART</button>
    </div>
</div>

<script>
const GAMES = JSON.parse("{data}");
const GAME = GAMES.find(g => g.number === {game.number});

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

let W = 1280;
let H = 720;

function resize() {{
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    canvas.style.width = W + "px";
    canvas.style.height = H + "px";
    ctx.setTransform(dpr,0,0,dpr,0,0);
}}
addEventListener("resize", resize);
resize();

const keys = {{}};

addEventListener("keydown", e => {{
    keys[e.key.toLowerCase()] = true;

    if(e.key.toLowerCase() === "r") restart();
    if(e.key.toLowerCase() === "p") togglePause();
    if(e.key === "Escape") togglePause();
    if(e.code === "Space") {{
        e.preventDefault();
        action();
    }}
}});

addEventListener("keyup", e => {{
    keys[e.key.toLowerCase()] = false;
}});

let touchX = 0;
let touchY = 0;

const stick = document.getElementById("stick");
const knob = document.getElementById("knob");

function updateStick(e) {{
    const r = stick.getBoundingClientRect();
    let x = e.clientX - (r.left + r.width/2);
    let y = e.clientY - (r.top + r.height/2);
    const len = Math.hypot(x,y);
    const max = 42;

    if(len > max) {{
        x = x / len * max;
        y = y / len * max;
    }}

    touchX = x / max;
    touchY = y / max;
    knob.style.transform =
        `translate(${{x}}px,${{y}}px)`;
}}

stick.addEventListener("pointerdown", e => {{
    stick.setPointerCapture(e.pointerId);
    updateStick(e);
}});

stick.addEventListener("pointermove", e => {{
    if(e.pressure > 0) updateStick(e);
}});

function resetStick() {{
    touchX = 0;
    touchY = 0;
    knob.style.transform = "translate(0,0)";
}}

stick.addEventListener("pointerup", resetStick);
stick.addEventListener("pointercancel", resetStick);

document.getElementById("action").addEventListener(
    "pointerdown",
    e => {{
        e.preventDefault();
        action();
    }}
);

let player;
let objects;
let enemies;
let score;
let timeLeft;
let paused;
let ended;
let pulseClock;
let pattern;
let patternInput;
let patternVisible;

function restart() {{
    player = {{
        x: W * .18,
        y: H * .55,
        r: 16,
        speed: 290
    }};

    objects = [];
    enemies = [];
    score = 0;
    timeLeft = 60;
    paused = false;
    ended = false;
    pulseClock = 0;
    patternInput = [];
    patternVisible = true;

    pattern = Array.from(
        {{length: GAME.mode === "memory" ? 4 : 0}},
        () => Math.floor(Math.random()*9)
    );

    for(let i=0;i<Math.max(5,Math.min(12,GAME.goal/3));i++) {{
        spawnObject();
    }}

    for(let i=0;i<Math.min(6,2+Math.floor(GAME.number/6));i++) {{
        spawnEnemy();
    }}

    document.getElementById("result").style.display = "none";
}}

function spawnObject() {{
    objects.push({{
        x:80 + Math.random()*(W-160),
        y:110 + Math.random()*(H-190),
        r:10 + Math.random()*8
    }});
}}

function spawnEnemy() {{
    enemies.push({{
        x:W*.55 + Math.random()*W*.35,
        y:110 + Math.random()*(H-190),
        r:15
    }});
}}

function action() {{
    if(ended) return;

    if(GAME.mode === "memory") {{
        patternInput.push(patternInput.length % 9);

        if(patternInput.length >= pattern.length) {{
            if(patternInput.every((v,i) => v === pattern[i])) {{
                win();
            }} else {{
                lose();
            }}
        }}
        return;
    }}

    const range = GAME.mode === "boss" ? 145 : 105;

    for(let i=enemies.length-1;i>=0;i--) {{
        const e = enemies[i];

        if(Math.hypot(
            player.x-e.x,
            player.y-e.y
        ) < range) {{
            enemies.splice(i,1);
            score += GAME.mode === "boss" ? 5 : 3;
            break;
        }}
    }}

    if(GAME.mode === "switch" || GAME.mode === "pulse") {{
        score++;
    }}
}}

function togglePause() {{
    if(ended) return;
    paused = !paused;
}}

document.getElementById("pause").onclick = togglePause;

function update(dt) {{
    if(paused || ended) return;

    timeLeft -= dt;

    let dx = 0;
    let dy = 0;

    if(keys["w"] || keys["arrowup"]) dy -= 1;
    if(keys["s"] || keys["arrowdown"]) dy += 1;
    if(keys["a"] || keys["arrowleft"]) dx -= 1;
    if(keys["d"] || keys["arrowright"]) dx += 1;

    dx += touchX;
    dy += touchY;

    const len = Math.hypot(dx,dy);

    if(len > 0) {{
        dx /= len;
        dy /= len;

        player.x += dx * player.speed * dt;
        player.y += dy * player.speed * dt;
    }}

    player.x = Math.max(30,Math.min(W-30,player.x));
    player.y = Math.max(90,Math.min(H-30,player.y));

    pulseClock += dt;

    if(GAME.mode === "race") {{
        if(Math.random() < dt*.8) spawnObject();
    }}

    if(
        GAME.mode === "hunt" ||
        GAME.mode === "combat" ||
        GAME.mode === "stealth" ||
        GAME.mode === "defense" ||
        GAME.mode === "boss" ||
        GAME.mode === "mixed"
    ) {{
        for(const e of enemies) {{
            const ax = player.x-e.x;
            const ay = player.y-e.y;
            const l = Math.hypot(ax,ay)||1;
            const speed =
                GAME.mode === "stealth" ? 65 : 90;

            e.x += ax/l*speed*dt;
            e.y += ay/l*speed*dt;

            if(Math.hypot(player.x-e.x,player.y-e.y)<25) {{
                score = Math.max(0,score-1);
                player.x = W*.18;
                player.y = H*.55;
            }}
        }}
    }}

    if(GAME.mode === "survival") {{
        if(Math.random() < dt*2.2) spawnEnemy();

        for(const e of enemies) {{
            e.y += 180*dt;

            if(e.y > H+40) {{
                score++;
                e.y = 80;
                e.x = Math.random()*W;
            }}

            if(Math.hypot(player.x-e.x,player.y-e.y)<25) {{
                score = Math.max(0,score-2);
                e.y = 80;
                e.x = Math.random()*W;
            }}
        }}
    }}

    for(let i=objects.length-1;i>=0;i--) {{
        const o = objects[i];

        if(Math.hypot(player.x-o.x,player.y-o.y)<player.r+o.r) {{
            objects.splice(i,1);
            score++;

            spawnObject();
        }}
    }}

    if(GAME.mode === "collect_combat") {{
        if(Math.random()<dt*.4) spawnEnemy();
    }}

    if(GAME.mode === "race" && score >= GAME.goal) {{
        win();
    }}

    if(GAME.mode === "maze" &&
       player.x > W-100 &&
       player.y > H/2-80 &&
       player.y < H/2+80) {{
        score++;
        player.x = 60;
    }}

    if(score >= GAME.goal) win();
    if(timeLeft <= 0) lose();
}}

function drawBackground() {{
    ctx.fillStyle = "#060606";
    ctx.fillRect(0,0,W,H);

    ctx.strokeStyle = "#161616";
    ctx.lineWidth = 1;

    for(let x=0;x<W;x+=50) {{
        ctx.beginPath();
        ctx.moveTo(x,70);
        ctx.lineTo(x,H);
        ctx.stroke();
    }}

    for(let y=70;y<H;y+=50) {{
        ctx.beginPath();
        ctx.moveTo(0,y);
        ctx.lineTo(W,y);
        ctx.stroke();
    }}
}}

function draw() {{
    drawBackground();

    ctx.fillStyle = "#111";
    ctx.fillRect(0,0,W,70);

    ctx.fillStyle = "#fff";
    ctx.font = "bold 20px system-ui";
    ctx.fillText(
        String(GAME.number).padStart(2,"0")+"  "+GAME.title,
        18,30
    );

    ctx.fillStyle = "#999";
    ctx.font = "13px system-ui";
    ctx.fillText(GAME.genre,18,52);

    ctx.fillStyle = "#fff";
    ctx.fillText(
        "SCORE "+score+" / "+GAME.goal,
        W-220,30
    );

    ctx.fillStyle = "#ddd";
    ctx.fillText(
        "TIME "+Math.max(0,timeLeft).toFixed(1),
        W-120,52
    );

    for(const o of objects) {{
        ctx.fillStyle = "#e5d24a";
        ctx.beginPath();
        ctx.arc(o.x,o.y,o.r,0,Math.PI*2);
        ctx.fill();
    }}

    for(const e of enemies) {{
        ctx.fillStyle =
            GAME.mode === "stealth" ? "#a855f7" : "#e34b55";

        ctx.beginPath();
        ctx.arc(e.x,e.y,e.r,0,Math.PI*2);
        ctx.fill();
    }}

    ctx.fillStyle = "#fff";
    ctx.beginPath();
    ctx.arc(player.x,player.y,player.r,0,Math.PI*2);
    ctx.fill();

    if(GAME.mode === "memory") {{
        drawMemory();
    }}

    if(GAME.mode === "maze") {{
        ctx.strokeStyle="#49d6c8";
        ctx.lineWidth=4;
        ctx.strokeRect(W-120,H/2-80,80,160);
    }}

    if(paused) {{
        ctx.fillStyle="#000b";
        ctx.fillRect(0,0,W,H);
        ctx.fillStyle="#fff";
        ctx.font="bold 42px system-ui";
        ctx.textAlign="center";
        ctx.fillText("PAUSED",W/2,H/2);
        ctx.textAlign="left";
    }}
}}

function drawMemory() {{
    const size=55;
    const gap=15;
    const sx=W/2-(size*3+gap*2)/2;
    const sy=110;

    for(let i=0;i<9;i++) {{
        const x=sx+(i%3)*(size+gap);
        const y=sy+Math.floor(i/3)*(size+gap);

        let active=false;

        if(patternVisible && pattern.includes(i)) {{
            active=true;
        }}

        if(patternInput.includes(i)) {{
            active=true;
        }}

        ctx.fillStyle=active ? "#e5d24a" : "#202020";
        ctx.fillRect(x,y,size,size);
    }}
}}

function win() {{
    if(ended) return;

    ended=true;

    document.getElementById("resultTitle").textContent =
        "MISSION COMPLETE";

    document.getElementById("resultScore").textContent =
        "Score: "+score;

    document.getElementById("result").style.display="grid";
}}

function lose() {{
    if(ended) return;

    ended=true;

    document.getElementById("resultTitle").textContent =
        "RUN FAILED";

    document.getElementById("resultScore").textContent =
        "Score: "+score;

    document.getElementById("result").style.display="grid";
}}

document.getElementById("title").textContent =
    GAME.title;

restart();

let previous=performance.now();

function loop(now) {{
    const dt=Math.min(.05,(now-previous)/1000);
    previous=now;

    update(dt);
    draw();

    requestAnimationFrame(loop);
}}

requestAnimationFrame(loop);
</script>
</body>
</html>
"""


def build_game(number: int, output_root: Path) -> Path:
    if not 1 <= number <= len(GAMES):
        raise ValueError("Invalid game number.")

    game = GAMES[number - 1]

    output = (
        output_root
        / "games"
        / f"game_{game.number:02d}"
        / "index.html"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_runtime(game), encoding="utf-8")

    return output


def build_all(output_root: Path) -> List[Path]:
    return [build_game(game.number, output_root) for game in GAMES]
