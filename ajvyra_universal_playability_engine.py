/* ============================================================
   AJVYRA — UNIVERSAL MOBILE GAME RUNTIME
   PACKAGE 1 / 2
   ============================================================ */

class AJVYRA_GameRuntime {

    constructor(options = {}) {

        this.canvas =
            options.canvas ||
            document.querySelector("#gameCanvas");

        if (!this.canvas) {
            throw new Error("AJVYRA: #gameCanvas was not found.");
        }

        this.ctx = this.canvas.getContext("2d", {
            alpha: false,
            desynchronized: true
        });

        this.canvas.tabIndex = 0;

        this.width = 1280;
        this.height = 720;

        this.running = false;
        this.paused = false;

        this.lastTime = 0;
        this.delta = 0;

        this.score = 0;
        this.coins = 0;
        this.level = 1;

        this.player = null;
        this.entities = [];
        this.particles = [];

        this.camera = {
            x: 0,
            y: 0,
            shake: 0
        };

        this.keys = new Set();
        this.pointer = {
            x: 0,
            y: 0,
            down: false,
            justPressed: false
        };

        this.touchButtons = new Map();

        this.audio = {
            enabled: true,
            context: null,
            master: null
        };

        this.game = null;

        this.resize();
        this.installInput();
        this.installTouchControls();
        this.installAudio();

        window.addEventListener(
            "resize",
            () => this.resize(),
            { passive: true }
        );
    }

    /* --------------------------------------------------------
       DISPLAY
       -------------------------------------------------------- */

    resize() {

        const rect = this.canvas.getBoundingClientRect();

        const dpr = Math.min(
            window.devicePixelRatio || 1,
            2
        );

        this.canvas.width =
            Math.max(1, Math.floor(rect.width * dpr));

        this.canvas.height =
            Math.max(1, Math.floor(rect.height * dpr));

        this.ctx.setTransform(
            dpr,
            0,
            0,
            dpr,
            0,
            0
        );

        this.viewportWidth = rect.width;
        this.viewportHeight = rect.height;
    }

    clear() {

        this.ctx.save();

        this.ctx.fillStyle = "#050505";
        this.ctx.fillRect(
            0,
            0,
            this.viewportWidth,
            this.viewportHeight
        );

        this.ctx.restore();
    }

    /* --------------------------------------------------------
       INPUT
       -------------------------------------------------------- */

    installInput() {

        window.addEventListener("keydown", event => {

            this.keys.add(event.code);

            if (
                event.code === "Space" ||
                event.code === "ArrowUp" ||
                event.code === "ArrowDown" ||
                event.code === "ArrowLeft" ||
                event.code === "ArrowRight"
            ) {
                event.preventDefault();
            }

            if (event.code === "Escape") {
                this.togglePause();
            }
        });

        window.addEventListener("keyup", event => {
            this.keys.delete(event.code);
        });

        this.canvas.addEventListener("pointerdown", event => {

            this.pointer.down = true;
            this.pointer.justPressed = true;

            this.updatePointer(event);
            this.canvas.focus();
        });

        this.canvas.addEventListener("pointermove", event => {
            this.updatePointer(event);
        });

        window.addEventListener("pointerup", () => {
            this.pointer.down = false;
        });
    }

    updatePointer(event) {

        const rect =
            this.canvas.getBoundingClientRect();

        this.pointer.x =
            event.clientX - rect.left;

        this.pointer.y =
            event.clientY - rect.top;
    }

    key(...codes) {

        return codes.some(code =>
            this.keys.has(code)
        );
    }

    /* --------------------------------------------------------
       TOUCH CONTROL SYSTEM
       -------------------------------------------------------- */

    installTouchControls() {

        const bindButton = (name, selector) => {

            const button =
                document.querySelector(selector);

            if (!button) return;

            const press = event => {

                event.preventDefault();

                this.touchButtons.set(name, true);
            };

            const release = event => {

                event.preventDefault();

                this.touchButtons.set(name, false);
            };

            button.addEventListener(
                "pointerdown",
                press
            );

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
        };

        bindButton("left", "[data-aj-left]");
        bindButton("right", "[data-aj-right]");
        bindButton("up", "[data-aj-up]");
        bindButton("down", "[data-aj-down]");
        bindButton("jump", "[data-aj-jump]");
        bindButton("attack", "[data-aj-attack]");
        bindButton("dash", "[data-aj-dash]");
        bindButton("action", "[data-aj-action]");
    }

    action(name, keyboardCodes = []) {

        return (
            this.touchButtons.get(name) === true ||
            this.key(...keyboardCodes)
        );
    }

    /* --------------------------------------------------------
       AUDIO
       -------------------------------------------------------- */

    installAudio() {

        try {

            const AudioContext =
                window.AudioContext ||
                window.webkitAudioContext;

            if (!AudioContext) return;

            this.audio.context =
                new AudioContext();

            this.audio.master =
                this.audio.context.createGain();

            this.audio.master.gain.value = 0.18;

            this.audio.master.connect(
                this.audio.context.destination
            );

        } catch (_) {

            this.audio.enabled = false;
        }
    }

    tone(
        frequency = 440,
        duration = 0.08,
        type = "sine",
        volume = 0.08
    ) {

        if (
            !this.audio.enabled ||
            !this.audio.context ||
            !this.audio.master
        ) {
            return;
        }

        const ctx = this.audio.context;

        if (ctx.state === "suspended") {
            ctx.resume().catch(() => {});
        }

        const oscillator =
            ctx.createOscillator();

        const gain =
            ctx.createGain();

        oscillator.type = type;
        oscillator.frequency.value = frequency;

        gain.gain.setValueAtTime(
            volume,
            ctx.currentTime
        );

        gain.gain.exponentialRampToValueAtTime(
            0.001,
            ctx.currentTime + duration
        );

        oscillator.connect(gain);
        gain.connect(this.audio.master);

        oscillator.start();

        oscillator.stop(
            ctx.currentTime + duration
        );
    }

    /* --------------------------------------------------------
       GAME OBJECTS
       -------------------------------------------------------- */

    createEntity(data = {}) {

        const entity = {

            id:
                data.id ||
                crypto.randomUUID(),

            x: Number(data.x) || 0,
            y: Number(data.y) || 0,

            width:
                Number(data.width) ||
                32,

            height:
                Number(data.height) ||
                32,

            vx: Number(data.vx) || 0,
            vy: Number(data.vy) || 0,

            gravity:
                Number.isFinite(data.gravity)
                    ? data.gravity
                    : 1000,

            speed:
                Number(data.speed) ||
                240,

            maxSpeed:
                Number(data.maxSpeed) ||
                900,

            hp:
                Number.isFinite(data.hp)
                    ? data.hp
                    : 100,

            maxHp:
                Number.isFinite(data.maxHp)
                    ? data.maxHp
                    : 100,

            damage:
                Number(data.damage) ||
                10,

            grounded: false,

            alive: true,

            type:
                data.type ||
                "entity",

            color:
                data.color ||
                "#ffffff",

            radius:
                Number(data.radius) ||
                16,

            friction:
                Number.isFinite(data.friction)
                    ? data.friction
                    : 0.82,

            custom:
                data.custom || {}
        };

        this.entities.push(entity);

        return entity;
    }

    removeDeadEntities() {

        this.entities =
            this.entities.filter(
                entity => entity.alive
            );
    }

    /* --------------------------------------------------------
       PHYSICS
       -------------------------------------------------------- */

    physics(entity, dt, options = {}) {

        const gravity =
            Number.isFinite(options.gravity)
                ? options.gravity
                : entity.gravity;

        entity.vy += gravity * dt;

        entity.vx =
            Math.max(
                -entity.maxSpeed,
                Math.min(
                    entity.maxSpeed,
                    entity.vx
                )
            );

        entity.vy =
            Math.max(
                -entity.maxSpeed,
                Math.min(
                    entity.maxSpeed,
                    entity.vy
                )
            );

        entity.x += entity.vx * dt;
        entity.y += entity.vy * dt;

        if (options.floor !== false) {

            const floor =
                Number.isFinite(options.floor)
                    ? options.floor
                    : 620;

            if (
                entity.y +
                entity.height / 2 >= floor
            ) {

                entity.y =
                    floor -
                    entity.height / 2;

                entity.vy = 0;

                entity.grounded = true;

            } else {

                entity.grounded = false;
            }
        }
    }

    /* --------------------------------------------------------
       COLLISION
       -------------------------------------------------------- */

    static rectCollision(a, b) {

        return (
            a.x - a.width / 2 <
                b.x + b.width / 2 &&

            a.x + a.width / 2 >
                b.x - b.width / 2 &&

            a.y - a.height / 2 <
                b.y + b.height / 2 &&

            a.y + a.height / 2 >
                b.y - b.height / 2
        );
    }

    damage(target, amount) {

        if (!target || !target.alive) {
            return false;
        }

        target.hp -= Math.max(
            0,
            Number(amount) || 0
        );

        this.spawnParticles(
            target.x,
            target.y,
            8
        );

        this.tone(
            120,
            0.06,
            "square",
            0.04
        );

        if (target.hp <= 0) {

            target.hp = 0;
            target.alive = false;

            this.score +=
                target.custom.reward || 100;
        }

        return true;
    }

    /* --------------------------------------------------------
       PARTICLES
       -------------------------------------------------------- */

    spawnParticles(x, y, amount = 10) {

        const count =
            Math.max(
                1,
                Math.min(
                    100,
                    Math.floor(amount)
                )
            );

        for (let i = 0; i < count; i++) {

            const angle =
                Math.random() *
                Math.PI *
                2;

            const speed =
                60 +
                Math.random() * 260;

            this.particles.push({

                x,
                y,

                vx:
                    Math.cos(angle) *
                    speed,

                vy:
                    Math.sin(angle) *
                    speed,

                life:
                    0.3 +
                    Math.random() * 0.5,

                maxLife: 0.8,

                size:
                    2 +
                    Math.random() * 5
            });
        }
    }

    updateParticles(dt) {

        for (const p of this.particles) {

            p.life -= dt;

            p.x += p.vx * dt;
            p.y += p.vy * dt;

            p.vy += 500 * dt;

            p.vx *= 0.97;
            p.vy *= 0.97;
        }

        this.particles =
            this.particles.filter(
                p => p.life > 0
            );
    }

    drawParticles() {

        const ctx = this.ctx;

        for (const p of this.particles) {

            const alpha =
                Math.max(
                    0,
                    p.life /
                    p.maxLife
                );

            ctx.save();

            ctx.globalAlpha = alpha;

            ctx.fillStyle = "#ffffff";

            ctx.beginPath();

            ctx.arc(
                p.x - this.camera.x,
                p.y - this.camera.y,
                p.size,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.restore();
        }
    }

    /* --------------------------------------------------------
       CAMERA
       -------------------------------------------------------- */

    follow(target) {

        if (!target) return;

        const desiredX =
            target.x -
            this.viewportWidth / 2;

        const desiredY =
            target.y -
            this.viewportHeight / 2;

        this.camera.x +=
            (desiredX - this.camera.x) *
            0.08;

        this.camera.y +=
            (desiredY - this.camera.y) *
            0.08;

        if (this.camera.shake > 0) {

            this.camera.x +=
                (Math.random() - 0.5) *
                this.camera.shake;

            this.camera.y +=
                (Math.random() - 0.5) *
                this.camera.shake;

            this.camera.shake *= 0.9;

            if (this.camera.shake < 0.1) {
                this.camera.shake = 0;
            }
        }
    }

    /* --------------------------------------------------------
       DRAW ENTITY
       -------------------------------------------------------- */

    drawEntity(entity) {

        const ctx = this.ctx;

        const x =
            entity.x -
            this.camera.x;

        const y =
            entity.y -
            this.camera.y;

        ctx.save();

        ctx.translate(x, y);

        if (entity.radius && entity.type === "orb") {

            ctx.beginPath();

            ctx.arc(
                0,
                0,
                entity.radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                entity.color;

            ctx.fill();

        } else {

            ctx.fillStyle =
                entity.color;

            ctx.fillRect(
                -entity.width / 2,
                -entity.height / 2,
                entity.width,
                entity.height
            );
        }

        ctx.restore();
    }

    /* --------------------------------------------------------
       HUD
       -------------------------------------------------------- */

    drawHUD() {

        const ctx = this.ctx;

        ctx.save();

        ctx.font =
            "600 18px system-ui";

        ctx.fillStyle =
            "#ffffff";

        ctx.fillText(
            `SCORE ${this.score}`,
            18,
            30
        );

        ctx.fillText(
            `LEVEL ${this.level}`,
            18,
            56
        );

        if (this.player) {

            const hp =
                Math.max(
                    0,
                    this.player.hp
                );

            const max =
                Math.max(
                    1,
                    this.player.maxHp
                );

            const ratio =
                Math.min(
                    1,
                    hp / max
                );

            ctx.fillStyle =
                "rgba(255,255,255,.15)";

            ctx.fillRect(
                18,
                72,
                180,
                12
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.fillRect(
                18,
                72,
                180 * ratio,
                12
            );
        }

        ctx.restore();
    }

    /* --------------------------------------------------------
       GAME MANAGEMENT
       -------------------------------------------------------- */

    loadGame(gameDefinition) {

        if (
            !gameDefinition ||
            typeof gameDefinition.update !== "function" ||
            typeof gameDefinition.draw !== "function"
        ) {
            throw new Error(
                "AJVYRA: Invalid game definition."
            );
        }

        this.stop();

        this.game =
            gameDefinition;

        this.score = 0;
        this.coins = 0;
        this.level = 1;

        this.entities = [];
        this.particles = [];

        this.camera.x = 0;
        this.camera.y = 0;

        if (
            typeof this.game.init ===
            "function"
        ) {
            this.game.init(this);
        }

        this.running = true;
        this.paused = false;

        this.lastTime =
            performance.now();

        requestAnimationFrame(
            time => this.loop(time)
        );
    }

    stop() {

        this.running = false;
        this.paused = false;
    }

    togglePause() {

        if (!this.running) return;

        this.paused =
            !this.paused;

        if (!this.paused) {

            this.lastTime =
                performance.now();
        }
    }

    restart() {

        if (!this.game) return;

        const current =
            this.game;

        this.loadGame(current);
    }

    /* --------------------------------------------------------
       MAIN LOOP
       -------------------------------------------------------- */

    loop(timestamp) {

        if (!this.running) {
            return;
        }

        if (this.paused) {

            this.renderPause();

            requestAnimationFrame(
                time => this.loop(time)
            );

            return;
        }

        let dt =
            (timestamp - this.lastTime) /
            1000;

        this.lastTime =
            timestamp;

        dt =
            Math.max(
                0.001,
                Math.min(
                    dt,
                    0.033
                )
            );

        this.delta = dt;

        this.clear();

        if (
            this.game &&
            typeof this.game.update ===
            "function"
        ) {
            this.game.update(
                this,
                dt
            );
        }

        this.updateParticles(dt);
        this.removeDeadEntities();

        if (
            this.game &&
            typeof this.game.draw ===
            "function"
        ) {
            this.game.draw(
                this
            );
        }

        this.drawParticles();
        this.drawHUD();

        this.pointer.justPressed =
            false;

        requestAnimationFrame(
            time => this.loop(time)
        );
    }

    renderPause() {

        this.clear();

        if (
            this.game &&
            typeof this.game.draw ===
            "function"
        ) {
            this.game.draw(this);
        }

        const ctx = this.ctx;

        ctx.save();

        ctx.fillStyle =
            "rgba(0,0,0,.72)";

        ctx.fillRect(
            0,
            0,
            this.viewportWidth,
            this.viewportHeight
        );

        ctx.textAlign = "center";

        ctx.font =
            "700 34px system-ui";

        ctx.fillStyle =
            "#ffffff";

        ctx.fillText(
            "PAUSED",
            this.viewportWidth / 2,
            this.viewportHeight / 2
        );

        ctx.font =
            "16px system-ui";

        ctx.fillText(
            "Press ESC to continue",
            this.viewportWidth / 2,
            this.viewportHeight / 2 + 34
        );

        ctx.restore();
    }
}


/* ============================================================
   AJVYRA GAME REGISTRY
   ============================================================ */

class AJVYRA_GameRegistry {

    constructor(runtime) {

        this.runtime = runtime;
        this.games = new Map();
    }

    register(id, definition) {

        if (
            typeof id !== "string" ||
            !id.trim()
        ) {
            throw new Error(
                "AJVYRA: Game ID is required."
            );
        }

        if (
            !definition ||
            typeof definition.init !==
                "function" ||
            typeof definition.update !==
                "function" ||
            typeof definition.draw !==
                "function"
        ) {
            throw new Error(
                `AJVYRA: ${id} has an invalid runtime definition.`
            );
        }

        this.games.set(
            id,
            definition
        );
    }

    play(id) {

        const game =
            this.games.get(id);

        if (!game) {

            throw new Error(
                `AJVYRA: Game "${id}" is not registered.`
            );
        }

        this.runtime.loadGame(game);
    }

    has(id) {
        return this.games.has(id);
    }

    count() {
        return this.games.size;
    }
}


/* ============================================================
   EXAMPLE REAL GAME
   ============================================================ */

const AJVYRA_ExampleGame = {

    id: "ajvyra_example",

    init(runtime) {

        runtime.player =
            runtime.createEntity({

                id: "player",

                x: 300,
                y: 300,

                width: 42,
                height: 58,

                speed: 420,

                maxSpeed: 600,

                gravity: 1400,

                hp: 100,

                maxHp: 100,

                type: "player",

                color: "#ffffff"
            });

        runtime.createEntity({

            x: 800,
            y: 500,

            width: 50,
            height: 50,

            gravity: 0,

            type: "enemy",

            hp: 40,

            maxHp: 40,

            color: "#777777",

            custom: {
                reward: 250
            }
        });
    },

    update(runtime, dt) {

        const player =
            runtime.player;

        if (!player || !player.alive) {
            return;
        }

        let direction = 0;

        if (
            runtime.action(
                "left",
                ["ArrowLeft", "KeyA"]
            )
        ) {
            direction -= 1;
        }

        if (
            runtime.action(
                "right",
                ["ArrowRight", "KeyD"]
            )
        ) {
            direction += 1;
        }

        player.vx =
            direction *
            player.speed;

        if (
            runtime.action(
                "jump",
                ["Space", "ArrowUp", "KeyW"]
            ) &&
            player.grounded
        ) {

            player.vy = -650;
            player.grounded = false;

            runtime.tone(
                420,
                0.09,
                "triangle",
                0.05
            );
        }

        runtime.physics(
            player,
            dt,
            {
                floor:
                    runtime.height ||
                    620
            }
        );

        runtime.follow(player);

        for (const entity of runtime.entities) {

            if (
                entity === player ||
                !entity.alive
            ) {
                continue;
            }

            if (
                entity.type === "enemy" &&
                AJVYRA_GameRuntime.rectCollision(
                    player,
                    entity
                )
            ) {

                runtime.damage(
                    entity,
                    10
                );

                player.vx =
                    -player.vx ||
                    200;

                runtime.camera.shake =
                    8;
            }
        }
    },

    draw(runtime) {

        const ctx =
            runtime.ctx;

        /* World floor */

        ctx.save();

        ctx.fillStyle =
            "#111111";

        ctx.fillRect(
            0,
            620 - runtime.camera.y,
            runtime.viewportWidth,
            100
        );

        ctx.restore();

        /* Entities */

        for (const entity of runtime.entities) {

            if (!entity.alive) {
                continue;
            }

            runtime.drawEntity(entity);
        }
    }
};


/* ============================================================
   BOOTSTRAP
   ============================================================ */

const AJVYRA_RUNTIME =
    new AJVYRA_GameRuntime({

        canvas:
            document.querySelector(
                "#gameCanvas"
            )
    });

const AJVYRA_GAMES =
    new AJVYRA_GameRegistry(
        AJVYRA_RUNTIME
    );

AJVYRA_GAMES.register(
    "ajvyra_example",
    AJVYRA_ExampleGame
);

/*
   Start:
   AJVYRA_GAMES.play("ajvyra_example");
*/
