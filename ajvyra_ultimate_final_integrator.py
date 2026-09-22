from __future__ import annotations

import json
import math
import shutil
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent

FINAL_GAMES = ROOT / "generated" / "final_games"
SOURCE_ASSETS = ROOT / "generated" / "ajvyra_assets"
ULTIMATE_OUTPUT = ROOT / "generated" / "ultimate_final_games"
REPORT_DIR = ROOT / "generated" / "ultimate_final_report"

GAME_COUNT = 70


# ============================================================
# CONFIG
# ============================================================

@dataclass
class GameProfile:
    game_id: int
    genre: str
    difficulty: str
    world_width: int
    world_height: int
    enemy_count: int
    particle_count: int
    mobile: bool = True
    gamepad: bool = True
    audio: bool = True
    webgl: bool = True
    save_system: bool = True


GENRES = [
    "rpg",
    "platformer",
    "horror",
    "racing",
    "puzzle",
    "survival",
    "adventure",
    "shooter",
    "stealth",
    "runner",
]


# ============================================================
# HELPERS
# ============================================================

def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


# ============================================================
# PROFILE GENERATION
# ============================================================

class ProfileFactory:

    def create(self, game_id: int) -> GameProfile:
        genre = GENRES[(game_id - 1) % len(GENRES)]

        difficulty_index = ((game_id - 1) // len(GENRES)) % 4
        difficulties = ["easy", "normal", "hard", "nightmare"]

        difficulty = difficulties[difficulty_index]

        enemy_count = {
            "rpg": 8,
            "platformer": 6,
            "horror": 4,
            "racing": 10,
            "puzzle": 0,
            "survival": 14,
            "adventure": 7,
            "shooter": 18,
            "stealth": 8,
            "runner": 12,
        }[genre]

        particles = {
            "rpg": 120,
            "platformer": 80,
            "horror": 160,
            "racing": 180,
            "puzzle": 40,
            "survival": 220,
            "adventure": 120,
            "shooter": 260,
            "stealth": 100,
            "runner": 180,
        }[genre]

        return GameProfile(
            game_id=game_id,
            genre=genre,
            difficulty=difficulty,
            world_width=3200 + game_id * 17,
            world_height=1800 + game_id * 11,
            enemy_count=enemy_count,
            particle_count=particles,
        )


# ============================================================
# WEBGL RENDERER
# ============================================================

WEBGL_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAWebGLRenderer {

    constructor(canvas) {
        this.canvas = canvas;
        this.gl = null;
        this.ctx2d = null;
        this.mode = "canvas";
        this.program = null;
        this.positionBuffer = null;
        this.colorBuffer = null;

        this.vertexSource = `
            attribute vec2 a_position;
            attribute vec4 a_color;

            uniform vec2 u_resolution;
            uniform vec2 u_camera;

            varying vec4 v_color;

            void main() {
                vec2 position = a_position - u_camera;

                vec2 zeroToOne = position / u_resolution;
                vec2 zeroToTwo = zeroToOne * 2.0;
                vec2 clip = zeroToTwo - 1.0;

                gl_Position = vec4(clip * vec2(1.0, -1.0), 0.0, 1.0);
                v_color = a_color;
            }
        `;

        this.fragmentSource = `
            precision mediump float;

            varying vec4 v_color;

            void main() {
                gl_FragColor = v_color;
            }
        `;

        this.init();
    }

    init() {
        try {
            this.gl =
                this.canvas.getContext("webgl2", {
                    antialias: true,
                    alpha: false,
                    powerPreference: "high-performance"
                }) ||
                this.canvas.getContext("webgl", {
                    antialias: true,
                    alpha: false,
                    powerPreference: "high-performance"
                });
        } catch (_) {
            this.gl = null;
        }

        if (this.gl) {
            this.mode = "webgl";
            this.setupWebGL();
            return;
        }

        this.ctx2d = this.canvas.getContext("2d");
        this.mode = "canvas";
    }

    compileShader(type, source) {
        const shader = this.gl.createShader(type);

        this.gl.shaderSource(shader, source);
        this.gl.compileShader(shader);

        if (!this.gl.getShaderParameter(shader, this.gl.COMPILE_STATUS)) {
            const message = this.gl.getShaderInfoLog(shader);
            this.gl.deleteShader(shader);
            throw new Error(message || "Shader compilation failed");
        }

        return shader;
    }

    setupWebGL() {
        const gl = this.gl;

        const vertex = this.compileShader(
            gl.VERTEX_SHADER,
            this.vertexSource
        );

        const fragment = this.compileShader(
            gl.FRAGMENT_SHADER,
            this.fragmentSource
        );

        this.program = gl.createProgram();

        gl.attachShader(this.program, vertex);
        gl.attachShader(this.program, fragment);
        gl.linkProgram(this.program);

        if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) {
            throw new Error(gl.getProgramInfoLog(this.program));
        }

        this.positionBuffer = gl.createBuffer();
        this.colorBuffer = gl.createBuffer();

        this.positionLocation =
            gl.getAttribLocation(this.program, "a_position");

        this.colorLocation =
            gl.getAttribLocation(this.program, "a_color");

        this.resolutionLocation =
            gl.getUniformLocation(this.program, "u_resolution");

        this.cameraLocation =
            gl.getUniformLocation(this.program, "u_camera");
    }

    resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);

        const width = Math.max(1, Math.floor(
            this.canvas.clientWidth * dpr
        ));

        const height = Math.max(1, Math.floor(
            this.canvas.clientHeight * dpr
        ));

        if (
            this.canvas.width !== width ||
            this.canvas.height !== height
        ) {
            this.canvas.width = width;
            this.canvas.height = height;
        }

        if (this.gl) {
            this.gl.viewport(
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );
        }
    }

    begin(cameraX, cameraY) {
        this.resize();

        if (this.mode === "webgl") {
            const gl = this.gl;

            gl.clearColor(0.025, 0.03, 0.045, 1);
            gl.clear(gl.COLOR_BUFFER_BIT);

            gl.useProgram(this.program);

            gl.uniform2f(
                this.resolutionLocation,
                this.canvas.width,
                this.canvas.height
            );

            gl.uniform2f(
                this.cameraLocation,
                cameraX,
                cameraY
            );
        } else {
            this.ctx2d.setTransform(1, 0, 0, 1, 0, 0);

            this.ctx2d.fillStyle = "#080b12";
            this.ctx2d.fillRect(
                0,
                0,
                this.canvas.width,
                this.canvas.height
            );
        }
    }

    drawRect(x, y, width, height, color, cameraX, cameraY) {
        if (this.mode === "canvas") {
            const ctx = this.ctx2d;

            ctx.fillStyle = color;

            ctx.fillRect(
                x - cameraX,
                y - cameraY,
                width,
                height
            );

            return;
        }

        const gl = this.gl;

        const vertices = new Float32Array([
            x, y,
            x + width, y,
            x, y + height,
            x + width, y + height
        ]);

        const parsed = this.parseColor(color);

        const colors = new Float32Array([
            ...parsed, ...parsed,
            ...parsed, ...parsed
        ]);

        gl.bindBuffer(gl.ARRAY_BUFFER, this.positionBuffer);

        gl.bufferData(
            gl.ARRAY_BUFFER,
            vertices,
            gl.DYNAMIC_DRAW
        );

        gl.enableVertexAttribArray(this.positionLocation);

        gl.vertexAttribPointer(
            this.positionLocation,
            2,
            gl.FLOAT,
            false,
            0,
            0
        );

        gl.bindBuffer(gl.ARRAY_BUFFER, this.colorBuffer);

        gl.bufferData(
            gl.ARRAY_BUFFER,
            colors,
            gl.DYNAMIC_DRAW
        );

        gl.enableVertexAttribArray(this.colorLocation);

        gl.vertexAttribPointer(
            this.colorLocation,
            4,
            gl.FLOAT,
            false,
            0,
            0
        );

        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    parseColor(value) {
        if (typeof value !== "string") {
            return [1, 1, 1, 1];
        }

        if (value.startsWith("#")) {
            let hex = value.slice(1);

            if (hex.length === 3) {
                hex = hex
                    .split("")
                    .map(x => x + x)
                    .join("");
            }

            const number = parseInt(hex, 16);

            return [
                ((number >> 16) & 255) / 255,
                ((number >> 8) & 255) / 255,
                (number & 255) / 255,
                1
            ];
        }

        return [1, 1, 1, 1];
    }

    drawCircle(x, y, radius, color, cameraX, cameraY) {
        if (this.mode === "canvas") {
            const ctx = this.ctx2d;

            ctx.beginPath();

            ctx.arc(
                x - cameraX,
                y - cameraY,
                radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle = color;
            ctx.fill();

            return;
        }

        // Circle approximation on WebGL.
        const steps = 24;

        for (let i = 0; i < steps; i++) {
            const a1 = (i / steps) * Math.PI * 2;
            const a2 = ((i + 1) / steps) * Math.PI * 2;

            const x1 = x + Math.cos(a1) * radius;
            const y1 = y + Math.sin(a1) * radius;

            const x2 = x + Math.cos(a2) * radius;
            const y2 = y + Math.sin(a2) * radius;

            this.drawRect(
                Math.min(x1, x2),
                Math.min(y1, y2),
                Math.abs(x2 - x1) + 2,
                Math.abs(y2 - y1) + 2,
                color,
                cameraX,
                cameraY
            );
        }
    }
}

window.AJVYRAWebGLRenderer = AJVYRAWebGLRenderer;

})();
"""


# ============================================================
# PHYSICS
# ============================================================

PHYSICS_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAAdvancedPhysics {

    constructor() {
        this.gravity = 1500;
        this.friction = 0.82;
        this.entities = new Map();
    }

    add(entity) {
        if (!entity || !entity.id) {
            return;
        }

        this.entities.set(entity.id, entity);
    }

    remove(id) {
        this.entities.delete(id);
    }

    integrate(entity, dt) {
        if (!entity) return;

        entity.vx = Number(entity.vx || 0);
        entity.vy = Number(entity.vy || 0);

        entity.x += entity.vx * dt;
        entity.y += entity.vy * dt;

        if (entity.gravity !== false) {
            entity.vy += this.gravity * dt;
        }

        entity.vx *= Math.pow(this.friction, dt * 60);
    }

    overlap(a, b) {
        if (!a || !b) return false;

        return (
            a.x < b.x + b.w &&
            a.x + a.w > b.x &&
            a.y < b.y + b.h &&
            a.y + a.h > b.y
        );
    }

    resolveBounds(entity, worldWidth, worldHeight) {
        if (!entity) return;

        if (entity.x < 0) {
            entity.x = 0;
            entity.vx = Math.abs(entity.vx) * 0.25;
        }

        if (entity.y < 0) {
            entity.y = 0;
            entity.vy = Math.abs(entity.vy) * 0.25;
        }

        if (entity.x + entity.w > worldWidth) {
            entity.x = worldWidth - entity.w;
            entity.vx = -Math.abs(entity.vx) * 0.25;
        }

        if (entity.y + entity.h > worldHeight) {
            entity.y = worldHeight - entity.h;
            entity.vy = -Math.abs(entity.vy) * 0.25;
            entity.grounded = true;
        }
    }

    update(dt, worldWidth, worldHeight) {
        for (const entity of this.entities.values()) {
            this.integrate(entity, dt);
            this.resolveBounds(
                entity,
                worldWidth,
                worldHeight
            );
        }
    }
}

window.AJVYRAAdvancedPhysics = AJVYRAAdvancedPhysics;

})();
"""


# ============================================================
# AI
# ============================================================

AI_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAEnemyAI {

    constructor() {
        this.agents = new Map();
    }

    add(agent) {
        if (!agent || !agent.id) return;

        this.agents.set(agent.id, {
            ...agent,
            state: agent.state || "idle",
            targetId: agent.targetId || "player"
        });
    }

    remove(id) {
        this.agents.delete(id);
    }

    distance(a, b) {
        const dx = (a.x || 0) - (b.x || 0);
        const dy = (a.y || 0) - (b.y || 0);

        return Math.sqrt(dx * dx + dy * dy);
    }

    update(dt, world) {
        const player = world.player;

        if (!player) return;

        for (const agent of this.agents.values()) {
            const d = this.distance(agent, player);

            const detection =
                Number(agent.detectionRadius || 500);

            if (d < detection) {
                agent.state = "chase";
            } else {
                agent.state = "patrol";
            }

            if (agent.state === "chase") {
                const dx = player.x - agent.x;
                const dy = player.y - agent.y;

                const length =
                    Math.sqrt(dx * dx + dy * dy) || 1;

                const speed =
                    Number(agent.speed || 100);

                agent.vx = (dx / length) * speed;
                agent.vy = (dy / length) * speed;
            } else {
                agent.vx *= 0.96;
                agent.vy *= 0.96;
            }
        }
    }
}

window.AJVYRAEnemyAI = AJVYRAEnemyAI;

})();
"""


# ============================================================
# INPUT
# ============================================================

INPUT_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAUniversalInput {

    constructor(root) {
        this.root = root;
        this.keys = new Set();

        this.axisX = 0;
        this.axisY = 0;

        this.actions = {
            attack: false,
            jump: false,
            dash: false,
            pause: false,
            interact: false
        };

        this.setupKeyboard();
        this.setupGamepad();
        this.setupTouch();
    }

    setupKeyboard() {
        window.addEventListener("keydown", e => {
            this.keys.add(e.code);

            if (e.code === "Space") {
                this.actions.jump = true;
            }

            if (
                e.code === "KeyJ" ||
                e.code === "KeyX"
            ) {
                this.actions.attack = true;
            }

            if (
                e.code === "ShiftLeft" ||
                e.code === "ShiftRight"
            ) {
                this.actions.dash = true;
            }

            if (e.code === "Escape") {
                this.actions.pause = true;
            }

            if (e.code === "KeyE") {
                this.actions.interact = true;
            }
        });

        window.addEventListener("keyup", e => {
            this.keys.delete(e.code);
        });
    }

    setupGamepad() {
        window.addEventListener(
            "gamepadconnected",
            () => {}
        );
    }

    readGamepad() {
        if (!navigator.getGamepads) {
            return;
        }

        const pads = navigator.getGamepads();

        const pad = pads && pads[0];

        if (!pad) return;

        const deadzone = 0.16;

        const x = Number(pad.axes[0] || 0);
        const y = Number(pad.axes[1] || 0);

        this.axisX =
            Math.abs(x) > deadzone ? x : 0;

        this.axisY =
            Math.abs(y) > deadzone ? y : 0;

        if (pad.buttons[0] && pad.buttons[0].pressed) {
            this.actions.jump = true;
        }

        if (pad.buttons[2] && pad.buttons[2].pressed) {
            this.actions.attack = true;
        }
    }

    setupTouch() {
        if (!("ontouchstart" in window)) {
            return;
        }

        const layer = document.createElement("div");

        layer.id = "ajvyra-touch-layer";

        layer.style.cssText = `
            position:fixed;
            inset:auto 0 0 0;
            height:190px;
            pointer-events:none;
            z-index:9999;
        `;

        const left = document.createElement("div");

        left.style.cssText = `
            position:absolute;
            left:22px;
            bottom:22px;
            width:120px;
            height:120px;
            border:2px solid rgba(255,255,255,.25);
            border-radius:50%;
            pointer-events:auto;
            touch-action:none;
        `;

        const right = document.createElement("button");

        right.type = "button";

        right.textContent = "ATTACK";

        right.style.cssText = `
            position:absolute;
            right:24px;
            bottom:46px;
            width:90px;
            height:90px;
            border-radius:50%;
            border:1px solid rgba(255,255,255,.3);
            background:rgba(20,20,30,.7);
            color:white;
            font-weight:bold;
            pointer-events:auto;
        `;

        left.addEventListener("pointerdown", e => {
            left.setPointerCapture(e.pointerId);
            left.dataset.active = "1";
        });

        left.addEventListener("pointermove", e => {
            if (left.dataset.active !== "1") return;

            const r = left.getBoundingClientRect();

            const cx = r.left + r.width / 2;
            const cy = r.top + r.height / 2;

            let x = (e.clientX - cx) / (r.width / 2);
            let y = (e.clientY - cy) / (r.height / 2);

            x = Math.max(-1, Math.min(1, x));
            y = Math.max(-1, Math.min(1, y));

            this.axisX = x;
            this.axisY = y;
        });

        const reset = () => {
            left.dataset.active = "0";
            this.axisX = 0;
            this.axisY = 0;
        };

        left.addEventListener("pointerup", reset);
        left.addEventListener("pointercancel", reset);

        right.addEventListener("pointerdown", () => {
            this.actions.attack = true;
        });

        layer.appendChild(left);
        layer.appendChild(right);

        document.body.appendChild(layer);
    }

    update() {
        let x = this.axisX;
        let y = this.axisY;

        if (this.keys.has("ArrowLeft") || this.keys.has("KeyA")) {
            x -= 1;
        }

        if (this.keys.has("ArrowRight") || this.keys.has("KeyD")) {
            x += 1;
        }

        if (this.keys.has("ArrowUp") || this.keys.has("KeyW")) {
            y -= 1;
        }

        if (this.keys.has("ArrowDown") || this.keys.has("KeyS")) {
            y += 1;
        }

        return {
            x: Math.max(-1, Math.min(1, x)),
            y: Math.max(-1, Math.min(1, y)),
            actions: {...this.actions}
        };
    }

    clearActions() {
        for (const key of Object.keys(this.actions)) {
            this.actions[key] = false;
        }
    }
}

window.AJVYRAUniversalInput = AJVYRAUniversalInput;

})();
"""


# ============================================================
# AUDIO
# ============================================================

AUDIO_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAAudioSystem {

    constructor() {
        this.context = null;
        this.master = null;
        this.started = false;
    }

    ensure() {
        if (this.context) return;

        const AudioContext =
            window.AudioContext ||
            window.webkitAudioContext;

        if (!AudioContext) {
            return;
        }

        this.context = new AudioContext();

        this.master =
            this.context.createGain();

        this.master.gain.value = 0.35;

        this.master.connect(
            this.context.destination
        );
    }

    resume() {
        this.ensure();

        if (
            this.context &&
            this.context.state === "suspended"
        ) {
            this.context.resume();
        }

        this.started = true;
    }

    tone(
        frequency = 440,
        duration = 0.08,
        type = "sine",
        volume = 0.08
    ) {
        this.ensure();

        if (!this.context || !this.master) {
            return;
        }

        const osc =
            this.context.createOscillator();

        const gain =
            this.context.createGain();

        osc.type = type;
        osc.frequency.value = frequency;

        gain.gain.setValueAtTime(
            0,
            this.context.currentTime
        );

        gain.gain.linearRampToValueAtTime(
            volume,
            this.context.currentTime + 0.005
        );

        gain.gain.exponentialRampToValueAtTime(
            0.0001,
            this.context.currentTime + duration
        );

        osc.connect(gain);
        gain.connect(this.master);

        osc.start();

        osc.stop(
            this.context.currentTime + duration + 0.02
        );
    }

    attack() {
        this.tone(180, 0.06, "square", 0.06);
        this.tone(90, 0.12, "sawtooth", 0.04);
    }

    jump() {
        this.tone(520, 0.1, "triangle", 0.04);
    }

    damage() {
        this.tone(80, 0.18, "sawtooth", 0.08);
    }

    win() {
        this.tone(523, 0.12, "triangle", 0.05);

        setTimeout(() => {
            this.tone(659, 0.12, "triangle", 0.05);
        }, 100);

        setTimeout(() => {
            this.tone(784, 0.2, "triangle", 0.05);
        }, 200);
    }
}

window.AJVYRAAudioSystem = AJVYRAAudioSystem;

})();
"""


# ============================================================
# PARTICLES
# ============================================================

PARTICLE_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAParticleSystem {

    constructor(limit = 300) {
        this.limit = Math.max(20, limit);
        this.particles = [];
    }

    burst(
        x,
        y,
        count = 12,
        color = "#ffffff"
    ) {
        const amount = Math.min(
            count,
            this.limit - this.particles.length
        );

        for (let i = 0; i < amount; i++) {
            const angle =
                Math.random() * Math.PI * 2;

            const speed =
                40 + Math.random() * 260;

            this.particles.push({
                x,
                y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed,
                life: 0.35 + Math.random() * 0.7,
                maxLife: 1,
                size: 2 + Math.random() * 5,
                color
            });
        }
    }

    update(dt) {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            const p = this.particles[i];

            p.life -= dt;

            p.x += p.vx * dt;
            p.y += p.vy * dt;

            p.vx *= Math.pow(0.05, dt);
            p.vy += 600 * dt;

            if (p.life <= 0) {
                this.particles.splice(i, 1);
            }
        }
    }

    render(renderer, cameraX, cameraY) {
        for (const p of this.particles) {
            renderer.drawRect(
                p.x,
                p.y,
                p.size,
                p.size,
                p.color,
                cameraX,
                cameraY
            );
        }
    }
}

window.AJVYRAParticleSystem = AJVYRAParticleSystem;

})();
"""


# ============================================================
# CAMERA
# ============================================================

CAMERA_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAAdvancedCamera {

    constructor() {
        this.x = 0;
        this.y = 0;
        this.targetX = 0;
        this.targetY = 0;

        this.shake = 0;
        this.zoom = 1;
    }

    follow(target, dt, width, height) {
        if (!target) return;

        this.targetX =
            target.x + target.w / 2 - width / 2;

        this.targetY =
            target.y + target.h / 2 - height / 2;

        const smoothing =
            1 - Math.pow(0.0001, dt);

        this.x +=
            (this.targetX - this.x) * smoothing;

        this.y +=
            (this.targetY - this.y) * smoothing;

        if (this.shake > 0) {
            this.x +=
                (Math.random() - 0.5) * this.shake;

            this.y +=
                (Math.random() - 0.5) * this.shake;

            this.shake *= Math.pow(0.02, dt);

            if (this.shake < 0.1) {
                this.shake = 0;
            }
        }
    }

    impact(amount = 10) {
        this.shake =
            Math.max(this.shake, amount);
    }
}

window.AJVYRAAdvancedCamera = AJVYRAAdvancedCamera;

})();
"""


# ============================================================
# UI
# ============================================================

UI_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAHUD {

    constructor() {
        this.root = document.createElement("div");

        this.root.style.cssText = `
            position:fixed;
            top:14px;
            left:14px;
            z-index:9998;
            color:white;
            font-family:system-ui,sans-serif;
            user-select:none;
            pointer-events:none;
            text-shadow:0 2px 8px rgba(0,0,0,.7);
        `;

        this.root.innerHTML = `
            <div id="ajv-health"></div>
            <div id="ajv-score"></div>
            <div id="ajv-level"></div>
            <div id="ajv-fps"></div>
        `;

        document.body.appendChild(this.root);

        this.health =
            this.root.querySelector("#ajv-health");

        this.score =
            this.root.querySelector("#ajv-score");

        this.level =
            this.root.querySelector("#ajv-level");

        this.fps =
            this.root.querySelector("#ajv-fps");
    }

    update(state) {
        if (!state) return;

        this.health.textContent =
            "HP: " +
            Math.max(
                0,
                Math.round(state.hp ?? 100)
            );

        this.score.textContent =
            "SCORE: " +
            Math.round(state.score ?? 0);

        this.level.textContent =
            "LEVEL: " +
            Math.round(state.level ?? 1);

        this.fps.textContent =
            "FPS: " +
            Math.round(state.fps ?? 0);
    }
}

window.AJVYRAHUD = AJVYRAHUD;

})();
"""


# ============================================================
# QUALITY / SAVE
# ============================================================

QUALITY_RUNTIME = r"""
(function () {
"use strict";

class AJVYRAQualityManager {

    constructor() {
        this.quality = "high";
        this.samples = [];
        this.lastChange = performance.now();
    }

    update(fps) {
        if (!Number.isFinite(fps)) return;

        this.samples.push(fps);

        if (this.samples.length > 60) {
            this.samples.shift();
        }

        if (performance.now() - this.lastChange < 3000) {
            return;
        }

        const average =
            this.samples.reduce(
                (a, b) => a + b,
                0
            ) / Math.max(1, this.samples.length);

        if (average < 28) {
            this.quality = "low";
        } else if (average < 45) {
            this.quality = "medium";
        } else {
            this.quality = "high";
        }

        this.lastChange = performance.now();
    }
}


class AJVYRASaveSystem {

    constructor(key) {
        this.key = key;
    }

    save(data) {
        try {
            localStorage.setItem(
                this.key,
                JSON.stringify(data)
            );

            return true;
        } catch (_) {
            return false;
        }
    }

    load() {
        try {
            const raw =
                localStorage.getItem(this.key);

            return raw ? JSON.parse(raw) : null;
        } catch (_) {
            return null;
        }
    }

    clear() {
        try {
            localStorage.removeItem(this.key);
        } catch (_) {}
    }
}

window.AJVYRAQualityManager = AJVYRAQualityManager;
window.AJVYRASaveSystem = AJVYRASaveSystem;

})();
"""


# ============================================================
# MAIN BRIDGE
# ============================================================

BRIDGE_RUNTIME_TEMPLATE = r"""
(function () {
"use strict";

const PROFILE = __PROFILE__;

class AJVYRAUltimateBridge {

    constructor(canvas) {
        this.canvas = canvas;

        this.renderer =
            new window.AJVYRAWebGLRenderer(canvas);

        this.physics =
            new window.AJVYRAAdvancedPhysics();

        this.ai =
            new window.AJVYRAEnemyAI();

        this.input =
            new window.AJVYRAUniversalInput(document);

        this.audio =
            new window.AJVYRAAudioSystem();

        this.particles =
            new window.AJVYRAParticleSystem(
                PROFILE.particle_count
            );

        this.camera =
            new window.AJVYRAAdvancedCamera();

        this.hud =
            new window.AJVYRAHUD();

        this.quality =
            new window.AJVYRAQualityManager();

        this.save =
            new window.AJVYRASaveSystem(
                "ajvyra-ultimate-game-" +
                PROFILE.game_id
            );

        this.lastTime = performance.now();
        this.fps = 60;

        this.player = {
            id: "player",
            x: PROFILE.world_width / 2,
            y: PROFILE.world_height / 2,
            w: 42,
            h: 64,
            vx: 0,
            vy: 0,
            hp: 100,
            maxHp: 100,
            grounded: false,
            gravity: true
        };

        this.enemies = [];

        this.score = 0;
        this.level = 1;
        this.running = true;
        this.started = false;

        this.createEnemies();

        this.bindUserActivation();
    }

    bindUserActivation() {
        const activate = () => {
            this.audio.resume();

            if (!this.started) {
                this.started = true;
                this.audio.tone(
                    260,
                    0.08,
                    "triangle",
                    0.025
                );
            }
        };

        window.addEventListener(
            "pointerdown",
            activate,
            {once: false}
        );

        window.addEventListener(
            "keydown",
            activate,
            {once: false}
        );
    }

    createEnemies() {
        for (
            let i = 0;
            i < PROFILE.enemy_count;
            i++
        ) {
            const enemy = {
                id: "enemy-" + i,
                x: 180 + (
                    i * 271
                ) % Math.max(
                    500,
                    PROFILE.world_width - 250
                ),
                y: 100 + (
                    i * 157
                ) % Math.max(
                    400,
                    PROFILE.world_height - 300
                ),
                w: 40,
                h: 50,
                vx: 0,
                vy: 0,
                speed:
                    65 +
                    (i % 5) * 20,
                detectionRadius:
                    PROFILE.genre === "horror"
                        ? 700
                        : 500,
                hp:
                    20 +
                    PROFILE.game_id % 20,
                gravity: true
            };

            this.enemies.push(enemy);

            this.physics.add(enemy);

            this.ai.add(enemy);
        }

        this.physics.add(this.player);
    }

    update(dt) {
        if (!this.running) {
            return;
        }

        this.input.readGamepad();

        const input =
            this.input.update();

        const moveSpeed =
            PROFILE.genre === "racing"
                ? 700
                : PROFILE.genre === "runner"
                    ? 560
                    : 330;

        this.player.vx =
            input.x * moveSpeed;

        if (
            input.actions.jump &&
            this.player.grounded
        ) {
            this.player.vy = -700;
            this.player.grounded = false;
            this.audio.jump();

            this.particles.burst(
                this.player.x,
                this.player.y + this.player.h,
                8,
                "#8bd5ff"
            );
        }

        if (input.actions.attack) {
            this.attack();
        }

        if (input.actions.dash) {
            this.player.vx +=
                input.x * 500;

            this.camera.impact(5);
        }

        this.physics.update(
            dt,
            PROFILE.world_width,
            PROFILE.world_height
        );

        this.ai.update(dt, {
            player: this.player
        });

        for (const enemy of this.enemies) {
            this.physics.integrate(
                enemy,
                dt
            );

            this.physics.resolveBounds(
                enemy,
                PROFILE.world_width,
                PROFILE.world_height
            );

            if (
                this.physics.overlap(
                    this.player,
                    enemy
                )
            ) {
                this.player.hp -=
                    10 * dt;

                this.camera.impact(4);
            }
        }

        this.particles.update(dt);

        const width =
            this.canvas.clientWidth || 800;

        const height =
            this.canvas.clientHeight || 600;

        this.camera.follow(
            this.player,
            dt,
            width,
            height
        );

        if (this.player.hp <= 0) {
            this.player.hp = 0;
            this.running = false;
        }

        this.score += dt * 10;

        if (
            this.score > 1000 &&
            this.level === 1
        ) {
            this.level = 2;
            this.audio.win();
        }

        this.hud.update({
            hp: this.player.hp,
            score: this.score,
            level: this.level,
            fps: this.fps
        });

        this.quality.update(this.fps);

        this.input.clearActions();
    }

    attack() {
        this.audio.attack();

        this.camera.impact(8);

        this.particles.burst(
            this.player.x + this.player.w / 2,
            this.player.y + this.player.h / 2,
            16,
            "#ffffff"
        );

        const radius = 100;

        for (const enemy of this.enemies) {
            const dx =
                enemy.x - this.player.x;

            const dy =
                enemy.y - this.player.y;

            const distance =
                Math.sqrt(
                    dx * dx +
                    dy * dy
                );

            if (distance < radius) {
                enemy.hp -= 25;

                enemy.vx +=
                    Math.sign(dx || 1) * 300;

                enemy.vy -= 200;

                this.score += 50;
            }
        }

        this.enemies =
            this.enemies.filter(
                enemy => enemy.hp > 0
            );
    }

    render() {
        const cameraX =
            this.camera.x;

        const cameraY =
            this.camera.y;

        this.renderer.begin(
            cameraX,
            cameraY
        );

        const bg = {
            r: 0.03,
            g: 0.04,
            b: 0.06
        };

        // World grid.
        const grid = 160;

        for (
            let x = 0;
            x < PROFILE.world_width;
            x += grid
        ) {
            this.renderer.drawRect(
                x,
                0,
                2,
                PROFILE.world_height,
                "#151c28",
                cameraX,
                cameraY
            );
        }

        for (
            let y = 0;
            y < PROFILE.world_height;
            y += grid
        ) {
            this.renderer.drawRect(
                0,
                y,
                PROFILE.world_width,
                2,
                "#151c28",
                cameraX,
                cameraY
            );
        }

        // Player.
        this.renderer.drawRect(
            this.player.x,
            this.player.y,
            this.player.w,
            this.player.h,
            PROFILE.genre === "horror"
                ? "#d6d6d6"
                : "#7bdcff",
            cameraX,
            cameraY
        );

        // Player core.
        this.renderer.drawCircle(
            this.player.x + this.player.w / 2,
            this.player.y + 18,
            8,
            "#ffffff",
            cameraX,
            cameraY
        );

        // Enemies.
        for (const enemy of this.enemies) {
            const color =
                PROFILE.genre === "horror"
                    ? "#7b1834"
                    : PROFILE.genre === "stealth"
                        ? "#503c8f"
                        : "#ff4d6d";

            this.renderer.drawRect(
                enemy.x,
                enemy.y,
                enemy.w,
                enemy.h,
                color,
                cameraX,
                cameraY
            );

            this.renderer.drawCircle(
                enemy.x + enemy.w / 2,
                enemy.y + 15,
                5,
                "#ffffff",
                cameraX,
                cameraY
            );
        }

        this.particles.render(
            this.renderer,
            cameraX,
            cameraY
        );
    }

    saveGame() {
        this.save.save({
            game_id: PROFILE.game_id,
            score: this.score,
            level: this.level,
            hp: this.player.hp,
            player: {
                x: this.player.x,
                y: this.player.y
            }
        });
    }

    loadGame() {
        const data = this.save.load();

        if (!data) return;

        this.score =
            Number(data.score || 0);

        this.level =
            Number(data.level || 1);

        this.player.hp =
            Number(data.hp || 100);

        if (data.player) {
            this.player.x =
                Number(data.player.x || this.player.x);

            this.player.y =
                Number(data.player.y || this.player.y);
        }
    }

    loop(now) {
        const dt =
            Math.min(
                0.05,
                Math.max(
                    0.001,
                    (now - this.lastTime) / 1000
                )
            );

        this.lastTime = now;

        this.fps =
            1 / dt;

        this.update(dt);
        this.render();

        requestAnimationFrame(
            this.loop.bind(this)
        );
    }

    start() {
        this.loadGame();

        requestAnimationFrame(
            this.loop.bind(this)
        );

        setInterval(
            () => this.saveGame(),
            5000
        );
    }
}

window.AJVYRAUltimateBridge =
    AJVYRAUltimateBridge;

})();
"""


# ============================================================
# BOOTSTRAP
# ============================================================

BOOTSTRAP_RUNTIME = r"""
(function () {
"use strict";

function waitForCanvas() {
    const canvas =
        document.querySelector("canvas");

    if (!canvas) {
        requestAnimationFrame(waitForCanvas);
        return;
    }

    if (
        !window.AJVYRAUltimateBridge ||
        !window.AJVYRAWebGLRenderer ||
        !window.AJVYRAAdvancedPhysics ||
        !window.AJVYRAEnemyAI ||
        !window.AJVYRAUniversalInput ||
        !window.AJVYRAAudioSystem ||
        !window.AJVYRAParticleSystem ||
        !window.AJVYRAAdvancedCamera ||
        !window.AJVYRAHUD ||
        !window.AJVYRAQualityManager ||
        !window.AJVYRASaveSystem
    ) {
        setTimeout(waitForCanvas, 20);
        return;
    }

    if (window.__AJVYRA_ULTIMATE_STARTED__) {
        return;
    }

    window.__AJVYRA_ULTIMATE_STARTED__ = true;

    const game =
        new window.AJVYRAUltimateBridge(canvas);

    window.AJVYRAUltimateGame = game;

    game.start();
}

waitForCanvas();

})();
"""


# ============================================================
# PYTHON INTEGRATOR
# ============================================================

class AJVYRAUltimateFinalIntegrator:

    def __init__(self):
        self.profile_factory = ProfileFactory()

        self.files = {
            "webgl": "ultimate_webgl.js",
            "physics": "ultimate_physics.js",
            "ai": "ultimate_ai.js",
            "input": "ultimate_input.js",
            "audio": "ultimate_audio.js",
            "particles": "ultimate_particles.js",
            "camera": "ultimate_camera.js",
            "ui": "ultimate_ui.js",
            "quality": "ultimate_quality.js",
            "bridge": "ultimate_bridge.js",
            "boot": "ultimate_boot.js",
        }

    # --------------------------------------------------------
    # Existing systems
    # --------------------------------------------------------

    def discover_previous_systems(self) -> Dict[str, bool]:

        names = [
            "ajvyra_real_execution_engine.py",
            "ajvyra_ai_game_runtime_bridge.py",
            "ajvyra_game_genre_registry.py",
            "ajvyra_game_mechanics_engine.py",
            "ajvyra_game_template_factory.py",
            "ajvyra_ai_game_variation_engine.py",
            "ajvyra_70_game_production_controller.py",
            "ajvyra_game_input_system.py",
            "ajvyra_game_collision_system.py",
            "ajvyra_game_entity_system.py",
            "ajvyra_game_genre_runtime.py",
            "ajvyra_final_game_runtime.py",
            "ajvyra_final_game_compiler.py",
            "ajvyra_final_game_validator.py",
            "ajvyra_final_70_game_builder.py",
            "ajvyra_games_release_manager.py",
            "ajvyra_games_final_command.py",
            "ajvyra_asset_model_registry.py",
            "ajvyra_procedural_asset_factory.py",
            "ajvyra_browser_asset_model_loader.py",
            "ajvyra_game_asset_runtime_connector.py",
            "ajvyra_asset_model_final_build.py",
        ]

        return {
            name: (ROOT / name).exists()
            for name in names
        }

    # --------------------------------------------------------
    # Assets
    # --------------------------------------------------------

    def integrate_assets(
        self,
        game_id: int,
        target: Path
    ) -> Dict[str, Any]:

        source =
            SOURCE_ASSETS /
            f"game_{game_id:02d}" /
            "assets"

        destination =
            target / "assets"

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        copied = []
        missing = []

        if not source.exists():
            return {
                "source_exists": False,
                "copied": [],
                "missing": []
            }

        for asset in source.rglob("*"):
            if not asset.is_file():
                continue

            relative =
                asset.relative_to(source)

            out =
                destination / relative

            out.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                asset,
                out
            )

            copied.append(
                str(relative)
            )

        return {
            "source_exists": True,
            "copied": copied,
            "missing": missing
        }

    # --------------------------------------------------------
    # Runtime files
    # --------------------------------------------------------

    def write_runtime(
        self,
        target: Path,
        profile: GameProfile
    ) -> List[str]:

        runtime_dir =
            target / "ultimate_runtime"

        runtime_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        generated = []

        mapping = {
            self.files["webgl"]:
                WEBGL_RUNTIME,

            self.files["physics"]:
                PHYSICS_RUNTIME,

            self.files["ai"]:
                AI_RUNTIME,

            self.files["input"]:
                INPUT_RUNTIME,

            self.files["audio"]:
                AUDIO_RUNTIME,

            self.files["particles"]:
                PARTICLE_RUNTIME,

            self.files["camera"]:
                CAMERA_RUNTIME,

            self.files["ui"]:
                UI_RUNTIME,

            self.files["quality"]:
                QUALITY_RUNTIME,
        }

        for filename, content in mapping.items():

            path =
                runtime_dir / filename

            write_text(
                path,
                content
            )

            generated.append(
                str(path.relative_to(target))
            )

        bridge =
            BRIDGE_RUNTIME_TEMPLATE.replace(
                "__PROFILE__",
                json.dumps(
                    asdict(profile),
                    ensure_ascii=False
                )
            )

        bridge_path =
            runtime_dir / self.files["bridge"]

        write_text(
            bridge_path,
            bridge
        )

        generated.append(
            str(
                bridge_path.relative_to(target)
            )
        )

        boot_path =
            runtime_dir / self.files["boot"]

        write_text(
            boot_path,
            BOOTSTRAP_RUNTIME
        )

        generated.append(
            str(
                boot_path.relative_to(target)
            )
        )

        return generated

    # --------------------------------------------------------
    # HTML integration
    # --------------------------------------------------------

    def patch_html(
        self,
        target: Path
    ) -> Dict[str, Any]:

        html =
            target / "index.html"

        if not html.exists():
            return {
                "ok": False,
                "reason": "index.html missing"
            }

        content =
            html.read_text(
                encoding="utf-8"
            )

        marker =
            "AJVYRA_ULTIMATE_FINAL_INTEGRATOR"

        if marker in content:
            return {
                "ok": True,
                "already_integrated": True
            }

        scripts = [
            self.files["webgl"],
            self.files["physics"],
            self.files["ai"],
            self.files["input"],
            self.files["audio"],
            self.files["particles"],
            self.files["camera"],
            self.files["ui"],
            self.files["quality"],
            self.files["bridge"],
            self.files["boot"],
        ]

        tag_block = (
            "\n<!-- " +
            marker +
            " -->\n"
        )

        for script in scripts:
            tag_block += (
                '<script src="ultimate_runtime/'
                + script
                + '"></script>\n'
            )

        tag_block += (
            "<!-- END_AJVYRA_ULTIMATE_FINAL_INTEGRATOR -->\n"
        )

        lower =
            content.lower()

        position =
            lower.rfind("</body>")

        if position >= 0:
            content = (
                content[:position]
                + tag_block
                + content[position:]
            )
        else:
            content += tag_block

        html.write_text(
            content,
            encoding="utf-8"
        )

        return {
            "ok": True,
            "already_integrated": False,
            "scripts": scripts
        }

    # --------------------------------------------------------
    # PWA / offline
    # --------------------------------------------------------

    def create_manifest(
        self,
        target: Path,
        profile: GameProfile
    ) -> None:

        manifest = {
            "name":
                f"AJVYRA Game {profile.game_id}",
            "short_name":
                f"AJVYRA {profile.game_id}",
            "start_url":
                "./index.html",
            "display":
                "fullscreen",
            "orientation":
                "landscape",
            "background_color":
                "#080b12",
            "theme_color":
                "#080b12",
            "description":
                f"AJVYRA {profile.genre} game",
            "icons": []
        }

        write_json(
            target / "manifest.json",
            manifest
        )

    def create_service_worker(
        self,
        target: Path
    ) -> None:

        js = r"""
const CACHE = "ajvyra-ultimate-v1";

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE).then(cache => {
            return cache.addAll([
                "./",
                "./index.html",
                "./manifest.json"
            ]);
        })
    );

    self.skipWaiting();
});

self.addEventListener("activate", event => {
    event.waitUntil(
        self.clients.claim()
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(cached => {
                return cached || fetch(event.request)
                    .then(response => {

                        if (
                            response &&
                            response.ok
                        ) {
                            const copy =
                                response.clone();

                            caches.open(CACHE)
                                .then(cache => {
                                    cache.put(
                                        event.request,
                                        copy
                                    );
                                });
                        }

                        return response;
                    })
                    .catch(() => cached);
            })
    );
});
"""

        write_text(
            target / "sw.js",
            js
        )

    # --------------------------------------------------------
    # Runtime metadata
    # --------------------------------------------------------

    def write_profile(
        self,
        target: Path,
        profile: GameProfile
    ) -> None:

        write_json(
            target / "ultimate_profile.json",
            asdict(profile)
        )

    def write_connection_report(
        self,
        target: Path,
        game_id: int,
        profile: GameProfile,
        assets: Dict[str, Any],
        html: Dict[str, Any]
    ) -> None:

        report = {
            "game_id": game_id,
            "profile": asdict(profile),
            "previous_systems": self.discover_previous_systems(),
            "asset_integration": assets,
            "html_integration": html,
            "runtime": {
                "webgl2": True,
                "webgl_fallback": True,
                "canvas_fallback": True,
                "physics": True,
                "enemy_ai": True,
                "gamepad": True,
                "touch": True,
                "audio": True,
                "particles": True,
                "camera": True,
                "hud": True,
                "dynamic_quality": True,
                "save_system": True,
                "pwa": True
            }
        }

        write_json(
            target / "ultimate_connection.json",
            report
        )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_game(
        self,
        game_id: int
    ) -> Dict[str, Any]:

        target =
            FINAL_GAMES /
            f"game_{game_id:02d}"

        checks = {}

        checks["game_directory"] =
            target.exists()

        checks["index"] =
            (target / "index.html").exists()

        checks["game_js"] =
            (target / "game.js").exists()

        checks["game_css"] =
            (target / "game.css").exists()

        checks["metadata"] =
            (target / "metadata.json").exists()

        checks["ultimate_runtime"] =
            (target / "ultimate_runtime").exists()

        required_runtime = [
            self.files["webgl"],
            self.files["physics"],
            self.files["ai"],
            self.files["input"],
            self.files["audio"],
            self.files["particles"],
            self.files["camera"],
            self.files["ui"],
            self.files["quality"],
            self.files["bridge"],
            self.files["boot"],
        ]

        checks["runtime_files"] = all(
            (
                target /
                "ultimate_runtime" /
                filename
            ).exists()
            for filename in required_runtime
        )

        html =
            target / "index.html"

        if html.exists():
            text =
                html.read_text(
                    encoding="utf-8"
                )

            checks["runtime_marker"] =
                "AJVYRA_ULTIMATE_FINAL_INTEGRATOR" in text

            checks["webgl_reference"] =
                "ultimate_webgl.js" in text

            checks["boot_reference"] =
                "ultimate_boot.js" in text

        else:
            checks["runtime_marker"] = False
            checks["webgl_reference"] = False
            checks["boot_reference"] = False

        checks["manifest"] =
            (target / "manifest.json").exists()

        checks["service_worker"] =
            (target / "sw.js").exists()

        asset_dir =
            target / "assets"

        checks["assets_directory"] =
            asset_dir.exists()

        asset_count = 0

        if asset_dir.exists():
            asset_count =
                sum(
                    1
                    for x in asset_dir.rglob("*")
                    if x.is_file()
                )

        checks["asset_count"] =
            asset_count

        checks["ok"] =
            all(checks.values())

        return {
            "game_id": game_id,
            "checks": checks,
            "ok": checks["ok"]
        }

    # --------------------------------------------------------
    # Build
    # --------------------------------------------------------

    def build_game(
        self,
        game_id: int
    ) -> Dict[str, Any]:

        source =
            FINAL_GAMES /
            f"game_{game_id:02d}"

        if not source.exists():
            return {
                "game_id": game_id,
                "ok": False,
                "reason": "final game directory missing"
            }

        # We do not overwrite the original final game.
        target =
            ULTIMATE_OUTPUT /
            f"game_{game_id:02d}"

        if target.exists():
            shutil.rmtree(target)

        shutil.copytree(
            source,
            target
        )

        profile =
            self.profile_factory.create(
                game_id
            )

        assets =
            self.integrate_assets(
                game_id,
                target
            )

        runtime =
            self.write_runtime(
                target,
                profile
            )

        html =
            self.patch_html(
                target
            )

        self.create_manifest(
            target,
            profile
        )

        self.create_service_worker(
            target
        )

        self.write_profile(
            target,
            profile
        )

        self.write_connection_report(
            target,
            game_id,
            profile,
            assets,
            html
        )

        return {
            "game_id": game_id,
            "genre": profile.genre,
            "runtime_files": runtime,
            "asset_files":
                len(assets.get("copied", [])),
            "html": html,
            "ok": True
        }

    def build_all(self) -> Dict[str, Any]:

        ULTIMATE_OUTPUT.mkdir(
            parents=True,
            exist_ok=True
        )

        REPORT_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        results = []

        for game_id in range(
            1,
            GAME_COUNT + 1
        ):
            try:
                results.append(
                    self.build_game(game_id)
                )
            except Exception as exc:
                results.append({
                    "game_id": game_id,
                    "ok": False,
                    "error": repr(exc)
                })

        report = {
            "engine":
                "AJVYRA Ultimate Final Integrator",
            "game_count":
                GAME_COUNT,
            "results":
                results,
            "previous_systems":
                self.discover_previous_systems()
        }

        write_json(
            REPORT_DIR /
            "build_report.json",
            report
        )

        return report

    # --------------------------------------------------------
    # Validate ultimate output
    # --------------------------------------------------------

    def validate_all(self) -> Dict[str, Any]:

        results = []

        for game_id in range(
            1,
            GAME_COUNT + 1
        ):

            target =
                ULTIMATE_OUTPUT /
                f"game_{game_id:02d}"

            checks = {
                "directory":
                    target.exists(),
                "index":
                    (target / "index.html").exists(),
                "manifest":
                    (target / "manifest.json").exists(),
                "service_worker":
                    (target / "sw.js").exists(),
                "runtime":
                    (
                        target /
                        "ultimate_runtime"
                    ).exists(),
                "connection":
                    (
                        target /
                        "ultimate_connection.json"
                    ).exists(),
            }

            runtime =
                target / "ultimate_runtime"

            required = [
                self.files["webgl"],
                self.files["physics"],
                self.files["ai"],
                self.files["input"],
                self.files["audio"],
                self.files["particles"],
                self.files["camera"],
                self.files["ui"],
                self.files["quality"],
                self.files["bridge"],
                self.files["boot"],
            ]

            checks["all_runtime_files"] = all(
                (
                    runtime / name
                ).exists()
                for name in required
            )

            if (
                target /
                "index.html"
            ).exists():

                html =
                    (
                        target /
                        "index.html"
                    ).read_text(
                        encoding="utf-8"
                    )

                checks["boot_link"] =
                    "ultimate_boot.js" in html

                checks["bridge_link"] =
                    "ultimate_bridge.js" in html

            else:
                checks["boot_link"] = False
                checks["bridge_link"] = False

            checks["ok"] =
                all(checks.values())

            results.append({
                "game_id": game_id,
                "checks": checks,
                "ok": checks["ok"]
            })

        passed =
            sum(
                1
                for item in results
                if item["ok"]
            )

        report = {
            "game_count": GAME_COUNT,
            "passed": passed,
            "failed": GAME_COUNT - passed,
            "release_ready": passed == GAME_COUNT,
            "results": results
        }

        write_json(
            REPORT_DIR /
            "ultimate_validation.json",
            report
        )

        return report

    # --------------------------------------------------------
    # Release copy
    # --------------------------------------------------------

    def create_release(self) -> Dict[str, Any]:

        validation =
            self.validate_all()

        if not validation["release_ready"]:
            return {
                "ok": False,
                "reason":
                    "Ultimate validation failed",
                "validation":
                    validation
            }

        release =
            ROOT /
            "release" /
            "ajvyra_ultimate_games"

        if release.exists():
            shutil.rmtree(release)

        release.mkdir(
            parents=True,
            exist_ok=True
        )

        for game_id in range(
            1,
            GAME_COUNT + 1
        ):

            source =
                ULTIMATE_OUTPUT /
                f"game_{game_id:02d}"

            destination =
                release /
                f"game_{game_id:02d}"

            shutil.copytree(
                source,
                destination
            )

        checksums = {}

        for path in release.rglob("*"):
            if path.is_file():
                relative =
                    str(
                        path.relative_to(release)
                    )

                checksums[relative] =
                    sha256_file(path)

        write_json(
            release /
            "release_checksums.json",
            checksums
        )

        manifest = {
            "name":
                "AJVYRA Ultimate Games",
            "games":
                GAME_COUNT,
            "runtime":
                "AJVYRA Ultimate Final Runtime",
            "release_ready":
                True,
            "checksums":
                "release_checksums.json"
        }

        write_json(
            release /
            "release_manifest.json",
            manifest
        )

        write_text(
            release /
            "GAMES_FINAL_RELEASE_READY.txt",
            (
                "AJVYRA 70-game ultimate runtime "
                "integration completed.\n"
                "Static integration validation passed "
                "for all 70 generated game packages.\n"
                "Browser gameplay still requires real "
                "browser execution testing."
            )
        )

        return {
            "ok": True,
            "release":
                str(release),
            "games":
                GAME_COUNT
        }


# ============================================================
# CLI
# ============================================================

def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description=
        "AJVYRA Ultimate Final Games Integrator"
    )

    parser.add_argument(
        "command",
        choices=[
            "build",
            "validate",
            "release",
            "all"
        ]
    )

    parser.add_argument(
        "--game",
        type=int,
        default=0
    )

    args = parser.parse_args()

    engine =
        AJVYRAUltimateFinalIntegrator()

    if args.command == "build":

        if args.game:
            result =
                engine.build_game(
                    args.game
                )

            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2
                )
            )
        else:
            result =
                engine.build_all()

            print(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    indent=2
                )
            )

    elif args.command == "validate":

        result =
            engine.validate_all()

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )

    elif args.command == "release":

        result =
            engine.create_release()

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )

    elif args.command == "all":

        build =
            engine.build_all()

        validation =
            engine.validate_all()

        release = None

        if validation["release_ready"]:
            release =
                engine.create_release()

        result = {
            "build": build,
            "validation": validation,
            "release": release
        }

        print(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2
            )
        )


if __name__ == "__main__":
    main()
