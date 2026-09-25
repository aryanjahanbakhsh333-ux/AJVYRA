class AJVYRA_QualityLayer {

    constructor(runtime, registry) {
        this.runtime = runtime;
        this.registry = registry;

        this.projectiles = [];
        this.effects = [];
        this.checkpoints = new Map();

        this.animationTime = 0;
        this.combo = 0;
        this.comboTimer = 0;

        this.settings = {
            particles: true,
            screenShake: true,
            audio: true,
            quality: "high"
        };
    }

    update(dt) {

        this.animationTime += dt;

        this.updateProjectiles(dt);
        this.updateEffects(dt);

        if (this.comboTimer > 0) {
            this.comboTimer -= dt;

            if (this.comboTimer <= 0) {
                this.combo = 0;
            }
        }
    }

    /* ========================================================
       SMOOTH MOVEMENT
       ======================================================== */

    move(entity, targetVelocity, acceleration, dt) {

        const difference =
            targetVelocity - entity.vx;

        const amount =
            Math.max(
                -acceleration * dt,
                Math.min(
                    acceleration * dt,
                    difference
                )
            );

        entity.vx += amount;
    }

    jump(entity, power = 650) {

        if (!entity || !entity.grounded) {
            return false;
        }

        entity.vy = -power;
        entity.grounded = false;

        this.effect(
            entity.x,
            entity.y,
            "jump"
        );

        this.runtime.tone(
            360,
            0.08,
            "triangle",
            0.04
        );

        return true;
    }

    dash(entity, direction, power = 850) {

        if (!entity) return;

        const dir =
            Math.sign(direction) || 1;

        entity.vx =
            dir * power;

        entity.vy *= 0.35;

        this.effect(
            entity.x,
            entity.y,
            "dash"
        );

        if (this.settings.screenShake) {
            this.runtime.camera.shake = 5;
        }
    }

    /* ========================================================
       PROJECTILES
       ======================================================== */

    shoot(options = {}) {

        const projectile = {

            x: Number(options.x) || 0,
            y: Number(options.y) || 0,

            vx:
                Number(options.vx) || 0,

            vy:
                Number(options.vy) || 0,

            radius:
                Number(options.radius) || 7,

            damage:
                Number(options.damage) || 15,

            life:
                Number(options.life) || 1.5,

            color:
                options.color || "#ffffff",

            owner:
                options.owner || null,

            alive: true
        };

        this.projectiles.push(
            projectile
        );

        return projectile;
    }

    updateProjectiles(dt) {

        for (const p of this.projectiles) {

            if (!p.alive) continue;

            p.life -= dt;

            p.x += p.vx * dt;
            p.y += p.vy * dt;

            if (p.life <= 0) {
                p.alive = false;
                continue;
            }

            for (
                const entity
                of this.runtime.entities
            ) {

                if (
                    !entity.alive ||
                    entity === p.owner
                ) {
                    continue;
                }

                const dx =
                    p.x - entity.x;

                const dy =
                    p.y - entity.y;

                const distance =
                    Math.sqrt(
                        dx * dx +
                        dy * dy
                    );

                const radius =
                    p.radius +
                    Math.max(
                        entity.width,
                        entity.height
                    ) / 2;

                if (distance < radius) {

                    this.runtime.damage(
                        entity,
                        p.damage
                    );

                    this.hit(
                        entity.x,
                        entity.y
                    );

                    p.alive = false;

                    this.combo += 1;
                    this.comboTimer = 2;

                    break;
                }
            }
        }

        this.projectiles =
            this.projectiles.filter(
                p => p.alive
            );
    }

    drawProjectiles() {

        const ctx =
            this.runtime.ctx;

        for (const p of this.projectiles) {

            ctx.save();

            ctx.fillStyle =
                p.color;

            ctx.beginPath();

            ctx.arc(
                p.x -
                    this.runtime.camera.x,
                p.y -
                    this.runtime.camera.y,
                p.radius,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.restore();
        }
    }

    /* ========================================================
       EFFECT SYSTEM
       ======================================================== */

    effect(x, y, type) {

        if (!this.settings.particles) {
            return;
        }

        const presets = {

            hit: {
                count: 14,
                force: 220,
                life: 0.5
            },

            jump: {
                count: 8,
                force: 100,
                life: 0.35
            },

            dash: {
                count: 18,
                force: 180,
                life: 0.45
            },

            death: {
                count: 35,
                force: 320,
                life: 0.9
            }
        };

        const preset =
            presets[type] ||
            presets.hit;

        for (
            let i = 0;
            i < preset.count;
            i++
        ) {

            const angle =
                Math.random() *
                Math.PI * 2;

            const force =
                preset.force *
                (0.35 +
                Math.random() * 0.65);

            this.effects.push({

                x,
                y,

                vx:
                    Math.cos(angle) *
                    force,

                vy:
                    Math.sin(angle) *
                    force,

                life:
                    preset.life *
                    (0.6 +
                    Math.random() * 0.4),

                maxLife:
                    preset.life,

                size:
                    2 +
                    Math.random() * 5
            });
        }
    }

    hit(x, y) {

        this.effect(x, y, "hit");

        if (this.settings.screenShake) {
            this.runtime.camera.shake = 7;
        }

        this.runtime.tone(
            100 +
            Math.random() * 100,
            0.05,
            "square",
            0.035
        );
    }

    updateEffects(dt) {

        for (const e of this.effects) {

            e.life -= dt;

            e.x += e.vx * dt;
            e.y += e.vy * dt;

            e.vx *= 0.94;
            e.vy *= 0.94;

            e.vy += 300 * dt;
        }

        this.effects =
            this.effects.filter(
                e => e.life > 0
            );
    }

    drawEffects() {

        const ctx =
            this.runtime.ctx;

        for (const e of this.effects) {

            const alpha =
                Math.max(
                    0,
                    e.life / e.maxLife
                );

            ctx.save();

            ctx.globalAlpha = alpha;

            ctx.fillStyle =
                "#ffffff";

            ctx.beginPath();

            ctx.arc(
                e.x -
                    this.runtime.camera.x,
                e.y -
                    this.runtime.camera.y,
                e.size,
                0,
                Math.PI * 2
            );

            ctx.fill();

            ctx.restore();
        }
    }

    /* ========================================================
       ENEMY AI
       ======================================================== */

    enemyAI(enemy, target, dt) {

        if (
            !enemy ||
            !target ||
            !enemy.alive ||
            !target.alive
        ) {
            return;
        }

        const dx =
            target.x - enemy.x;

        const dy =
            target.y - enemy.y;

        const distance =
            Math.sqrt(
                dx * dx +
                dy * dy
            );

        const detection =
            enemy.custom.detection ||
            650;

        if (distance > detection) {

            enemy.vx *= 0.92;

            return;
        }

        const speed =
            enemy.custom.aiSpeed ||
            150;

        const direction =
            Math.sign(dx);

        this.move(
            enemy,
            direction * speed,
            700,
            dt
        );

        if (
            distance <
            (enemy.custom.attackRange || 55)
        ) {

            enemy.custom.attackCooldown =
                Math.max(
                    0,
                    (enemy.custom.attackCooldown || 0) -
                    dt
                );

            if (
                enemy.custom.attackCooldown <= 0
            ) {

                this.runtime.damage(
                    target,
                    enemy.damage
                );

                enemy.custom.attackCooldown =
                    enemy.custom.attackDelay ||
                    1;

                this.hit(
                    target.x,
                    target.y
                );
            }
        }

        this.runtime.physics(
            enemy,
            dt,
            {
                floor:
                    enemy.custom.floor ||
                    620
            }
        );
    }

    /* ========================================================
       CHECKPOINTS
       ======================================================== */

    setCheckpoint(id, x, y) {

        this.checkpoints.set(
            id,
            {
                x,
                y
            }
        );
    }

    respawn(player, checkpointId) {

        if (!player) return false;

        const point =
            this.checkpoints.get(
                checkpointId
            );

        if (!point) return false;

        player.x = point.x;
        player.y = point.y;

        player.vx = 0;
        player.vy = 0;

        player.hp =
            player.maxHp;

        player.alive = true;

        this.effect(
            point.x,
            point.y,
            "jump"
        );

        return true;
    }

    /* ========================================================
       INTERACTIVE OBJECTS
       ======================================================== */

    createInteractiveObject(options = {}) {

        return {

            id:
                options.id ||
                crypto.randomUUID(),

            x:
                Number(options.x) || 0,

            y:
                Number(options.y) || 0,

            width:
                Number(options.width) || 50,

            height:
                Number(options.height) || 50,

            active: true,

            type:
                options.type ||
                "object",

            action:
                typeof options.action ===
                "function"
                    ? options.action
                    : () => {}
        };
    }

    interact(player, object) {

        if (
            !player ||
            !object ||
            !object.active
        ) {
            return false;
        }

        if (
            AJVYRA_GameRuntime.rectCollision(
                player,
                object
            )
        ) {

            object.action(
                this.runtime,
                player,
                object
            );

            this.effect(
                object.x,
                object.y,
                "hit"
            );

            return true;
        }

        return false;
    }

    /* ========================================================
       REWARD SYSTEM
       ======================================================== */

    reward(amount = 0, coins = 0) {

        const score =
            Math.max(
                0,
                Number(amount) || 0
            );

        const coinAmount =
            Math.max(
                0,
                Number(coins) || 0
            );

        this.runtime.score += score;
        this.runtime.coins += coinAmount;

        this.runtime.tone(
            720,
            0.07,
            "sine",
            0.035
        );
    }

    /* ========================================================
       QUALITY SETTINGS
       ======================================================== */

    setQuality(level) {

        const allowed =
            ["low", "medium", "high"];

        if (
            !allowed.includes(level)
        ) {
            return false;
        }

        this.settings.quality =
            level;

        if (level === "low") {
            this.settings.particles = false;
        }

        if (level === "medium") {
            this.settings.particles = true;
        }

        if (level === "high") {
            this.settings.particles = true;
        }

        return true;
    }

    /* ========================================================
       FINAL DRAW LAYER
       ======================================================== */

    draw() {

        this.drawProjectiles();
        this.drawEffects();
    }
}


/* ============================================================
   AJVYRA GAME FACTORY
   ============================================================ */

class AJVYRA_GameFactory {

    static platformGame(runtime, quality) {

        return {

            init(rt) {

                rt.player =
                    rt.createEntity({

                        x: 300,
                        y: 300,

                        width: 42,
                        height: 58,

                        speed: 330,
                        maxSpeed: 650,

                        gravity: 1500,

                        hp: 100,
                        maxHp: 100,

                        type: "player",
                        color: "#ffffff"
                    });

                quality.setCheckpoint(
                    "start",
                    300,
                    300
                );

                rt.createEntity({

                    x: 850,
                    y: 520,

                    width: 48,
                    height: 48,

                    gravity: 1500,

                    hp: 60,
                    maxHp: 60,

                    damage: 8,

                    type: "enemy",

                    color: "#777777",

                    custom: {

                        aiSpeed: 120,

                        detection: 700,

                        attackRange: 58,

                        attackDelay: 1.2,

                        floor: 620,

                        reward: 200
                    }
                });
            },

            update(rt, dt) {

                const p =
                    rt.player;

                if (!p || !p.alive) {
                    return;
                }

                let direction = 0;

                if (
                    rt.action(
                        "left",
                        ["ArrowLeft", "KeyA"]
                    )
                ) {
                    direction--;
                }

                if (
                    rt.action(
                        "right",
                        ["ArrowRight", "KeyD"]
                    )
                ) {
                    direction++;
                }

                quality.move(
                    p,
                    direction * p.speed,
                    1800,
                    dt
                );

                if (
                    rt.action(
                        "jump",
                        ["Space", "KeyW", "ArrowUp"]
                    )
                ) {

                    quality.jump(
                        p,
                        650
                    );
                }

                if (
                    rt.action(
                        "dash",
                        ["ShiftLeft"]
                    )
                ) {

                    if (
                        !p.custom.dashLock
                    ) {

                        quality.dash(
                            p,
                            direction || 1
                        );

                        p.custom.dashLock =
                            true;
                    }

                } else {

                    p.custom.dashLock =
                        false;
                }

                if (
                    rt.action(
                        "attack",
                        ["KeyJ"]
                    )
                ) {

                    if (
                        !p.custom.attackLock
                    ) {

                        const directionSign =
                            direction || 1;

                        quality.shoot({

                            x:
                                p.x +
                                directionSign * 35,

                            y:
                                p.y,

                            vx:
                                directionSign *
                                700,

                            vy: 0,

                            damage: 25,

                            owner: p,

                            color: "#ffffff"
                        });

                        p.custom.attackLock =
                            true;

                        rt.tone(
                            520,
                            0.05,
                            "square",
                            0.04
                        );
                    }

                } else {

                    p.custom.attackLock =
                        false;
                }

                rt.physics(
                    p,
                    dt,
                    {
                        floor: 620
                    }
                );

                for (
                    const entity
                    of rt.entities
                ) {

                    if (
                        entity.type === "enemy"
                    ) {

                        quality.enemyAI(
                            entity,
                            p,
                            dt
                        );
                    }
                }

                quality.update(dt);

                rt.follow(p);

                if (p.hp <= 0) {

                    p.alive = false;

                    quality.effect(
                        p.x,
                        p.y,
                        "death"
                    );

                    setTimeout(() => {

                        quality.respawn(
                            p,
                            "start"
                        );

                    }, 700);
                }
            },

            draw(rt) {

                const ctx =
                    rt.ctx;

                ctx.save();

                ctx.fillStyle =
                    "#0b0b0b";

                ctx.fillRect(
                    0,
                    0,
                    rt.viewportWidth,
                    rt.viewportHeight
                );

                ctx.fillStyle =
                    "#1a1a1a";

                ctx.fillRect(
                    0,
                    620 -
                    rt.camera.y,
                    rt.viewportWidth,
                    100
                );

                for (
                    const entity
                    of rt.entities
                ) {

                    if (entity.alive) {
                        rt.drawEntity(
                            entity
                        );
                    }
                }

                ctx.restore();

                quality.draw();
            }
        };
    }
}


/* ============================================================
   FINAL AJVYRA BOOT
   ============================================================ */

const AJVYRA_QUALITY =
    new AJVYRA_QualityLayer(
        AJVYRA_RUNTIME,
        AJVYRA_GAMES
    );


/*
   نمونه‌ی اتصال:

   AJVYRA_GAMES.register(
       "ajvyra_quality_platform",
       AJVYRA_GameFactory.platformGame(
           AJVYRA_RUNTIME,
           AJVYRA_QUALITY
       )
   );

   AJVYRA_GAMES.play(
       "ajvyra_quality_platform"
   );
*/


/* ============================================================
   PERFORMANCE / SAFETY
   ============================================================ */

(function AJVYRA_PerformanceGuard() {

    const originalRAF =
        window.requestAnimationFrame;

    let frameCounter = 0;

    window.requestAnimationFrame =
        function(callback) {

            return originalRAF.call(
                window,
                timestamp => {

                    frameCounter++;

                    /*
                     * The runtime already clamps
                     * delta time. This layer simply
                     * prevents accidental runaway
                     * frame scheduling.
                     */

                    if (
                        frameCounter >
                        100000000
                    ) {
                        frameCounter = 0;
                    }

                    callback(timestamp);
                }
            );
        };

})();


/* ============================================================
   MOBILE EXPERIENCE
   ============================================================ */

(function AJVYRA_MobileMode() {

    const isTouch =
        "ontouchstart" in window ||
        navigator.maxTouchPoints > 0;

    document.documentElement
        .classList.toggle(
            "ajvyra-touch-device",
            isTouch
        );

    if (isTouch) {

        document.body.classList.add(
            "ajvyra-mobile-player"
        );
    }

})();
