class AJVYRAWebPlayableGameEngine {
    constructor(options = {}) {
        this.canvas = options.canvas || null;
        this.ctx = this.canvas
            ? this.canvas.getContext("2d")
            : null;

        this.input = options.input || null;
        this.hud = options.hud || null;
        this.screen = options.screen || null;

        this.definition = null;
        this.state = null;

        this.running = false;
        this.paused = false;
        this.raf = 0;
        this.lastTime = 0;

        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => {
            this.listeners.get(event)?.delete(callback);
        };
    }

    emit(event, data) {
        for (const callback of this.listeners.get(event) || []) {
            callback(data);
        }
    }

    load(definition) {
        if (!definition?.id) {
            throw new Error("Invalid AJVYRA game definition.");
        }

        this.definition = definition;
        this.reset();

        return this;
    }

    reset() {
        const d = this.definition;

        this.state = {
            status: "ready",
            time: 0,
            score: 0,
            level: 1,
            lives: d.lives ?? 3,
            objective: 0,
            objectiveTotal: d.objectiveTotal ?? 10,

            player: {
                x: 0.20,
                y: 0.50,
                w: 0.045,
                h: 0.075,

                vx: 0,
                vy: 0,

                hp: d.playerHp ?? 100,
                maxHp: d.playerHp ?? 100,

                stamina: 100,
                maxStamina: 100,

                mana: 100,
                maxMana: 100,

                cooldown: 0,
                invuln: 0,
                boost: 0,
                combo: 0
            },

            enemies: [],
            projectiles: [],
            pickups: [],
            obstacles: [],
            targets: [],

            won: false,
            lost: false
        };

        this.spawnInitial();
        this.syncHUD();
    }

    spawnInitial() {
        const d = this.definition;
        const s = this.state;

        for (let i = 0; i < (d.enemies ?? 4); i++) {
            s.enemies.push({
                x: 0.55 + (i % 4) * 0.09,
                y: 0.25 + Math.floor(i / 4) * 0.16,
                w: 0.045,
                h: 0.07,
                hp: d.enemyHp ?? 30,
                maxHp: d.enemyHp ?? 30,
                speed: d.enemySpeed ?? 0.07,
                phase: i * 0.7,
                alive: true
            });
        }

        for (let i = 0; i < (d.pickups ?? 3); i++) {
            s.pickups.push({
                x: 0.20 + ((i * 37) % 60) / 100,
                y: 0.20 + ((i * 23) % 55) / 100,
                w: 0.035,
                h: 0.035,
                active: true
            });
        }

        for (let i = 0; i < (d.targets ?? 0); i++) {
            s.targets.push({
                x: 0.15 + ((i * 29) % 70) / 100,
                y: 0.15 + ((i * 47) % 65) / 100,
                w: 0.04,
                h: 0.04,
                active: true
            });
        }

        for (let i = 0; i < (d.obstacles ?? 0); i++) {
            s.obstacles.push({
                x: 0.20 + ((i * 31) % 65) / 100,
                y: 0.18 + ((i * 19) % 62) / 100,
                w: 0.06,
                h: 0.08
            });
        }
    }

    start() {
        if (this.running) return;

        this.running = true;
        this.paused = false;
        this.state.status = "playing";

        this.input?.enable?.();
        this.screen?.hide?.();

        this.lastTime = performance.now();
        this.raf = requestAnimationFrame(
            timestamp => this.frame(timestamp)
        );
    }

    frame(timestamp) {
        if (!this.running) return;

        const delta = Math.min(
            0.05,
            Math.max(0, (timestamp - this.lastTime) / 1000)
        );

        this.lastTime = timestamp;

        if (!this.paused) {
            this.input?.update?.();
            this.update(delta);
            this.render();
        }

        this.raf = requestAnimationFrame(
            next => this.frame(next)
        );
    }

    update(dt) {
        const s = this.state;
        const d = this.definition;
        const input = this.input;

        if (!s || s.status !== "playing") {
            return;
        }

        s.time += dt;

        const movement =
            input?.getMovement?.() || { x: 0, y: 0 };

        const player = s.player;

        const speed =
            (d.playerSpeed ?? 0.45) *
            (player.boost > 0 ? 1.7 : 1);

        player.vx = movement.x * speed;
        player.vy = movement.y * speed;

        player.x = Math.max(
            0.03,
            Math.min(
                0.97 - player.w,
                player.x + player.vx * dt
            )
        );

        player.y = Math.max(
            0.03,
            Math.min(
                0.94 - player.h,
                player.y + player.vy * dt
            )
        );

        player.cooldown =
            Math.max(0, player.cooldown - dt);

        player.invuln =
            Math.max(0, player.invuln - dt);

        player.boost =
            Math.max(0, player.boost - dt);

        player.stamina =
            Math.min(
                player.maxStamina,
                player.stamina + dt * 12
            );

        if (input?.wasPressed?.("pause")) {
            this.pause();
            return;
        }

        if (
            input?.wasPressed?.("attack") &&
            player.cooldown <= 0
        ) {
            this.fire();
        }

        if (
            input?.wasPressed?.("jump") &&
            typeof d.jump === "number"
        ) {
            player.vy = -d.jump;
        }

        if (
            input?.wasPressed?.("special") &&
            player.mana >= (d.specialCost ?? 20)
        ) {
            player.mana -= d.specialCost ?? 20;
            this.special();
        }

        this.updateProjectiles(dt);
        this.updateEnemies(dt);
        this.collect();
        this.updateMode(dt);
        this.checkEnd();
        this.syncHUD();
    }

    fire() {
        const s = this.state;
        const d = this.definition;
        const p = s.player;

        p.cooldown = d.attackCooldown ?? 0.35;

        s.projectiles.push({
            x: p.x + p.w / 2,
            y: p.y + p.h / 2,
            vx: d.projectileSpeed ?? 0.85,
            vy: 0,
            w: 0.025,
            h: 0.012,
            damage: d.damage ?? 20,
            life: 1.4
        });
    }

    special() {
        const s = this.state;
        const d = this.definition;

        for (const enemy of s.enemies) {
            if (
                enemy.alive &&
                Math.hypot(
                    enemy.x - s.player.x,
                    enemy.y - s.player.y
                ) < (d.specialRange ?? 0.28)
            ) {
                enemy.hp -=
                    d.specialDamage ?? 50;

                if (enemy.hp <= 0) {
                    enemy.alive = false;
                    s.score += d.killScore ?? 100;
                    s.objective++;
                }
            }
        }

        s.player.boost =
            d.specialBoost ?? 1;
    }

    updateProjectiles(dt) {
        const s = this.state;

        for (const projectile of s.projectiles) {
            projectile.x += projectile.vx * dt;
            projectile.y += projectile.vy * dt;
            projectile.life -= dt;

            for (const enemy of s.enemies) {
                if (
                    enemy.alive &&
                    this.hit(projectile, enemy)
                ) {
                    enemy.hp -= projectile.damage;
                    projectile.life = 0;

                    if (enemy.hp <= 0) {
                        enemy.alive = false;
                        s.score +=
                            this.definition.killScore ?? 100;
                        s.objective++;
                        s.player.combo++;
                    }
                }
            }
        }

        s.projectiles =
            s.projectiles.filter(
                p =>
                    p.life > 0 &&
                    p.x > -0.1 &&
                    p.x < 1.1 &&
                    p.y > -0.1 &&
                    p.y < 1.1
            );
    }

    updateEnemies(dt) {
        const s = this.state;
        const d = this.definition;
        const p = s.player;

        for (const enemy of s.enemies) {
            if (!enemy.alive) continue;

            const dx = p.x - enemy.x;
            const dy = p.y - enemy.y;
            const distance =
                Math.hypot(dx, dy) || 1;

            if (
                d.mode === "shooter" ||
                d.mode === "boss"
            ) {
                if (distance > 0.18) {
                    enemy.x +=
                        dx / distance *
                        enemy.speed *
                        dt;

                    enemy.y +=
                        dy / distance *
                        enemy.speed *
                        dt;
                }
            } else if (
                d.mode !== "racing" &&
                d.mode !== "puzzle"
            ) {
                enemy.x +=
                    Math.sin(s.time + enemy.phase) *
                    enemy.speed *
                    0.3 *
                    dt;

                enemy.y +=
                    Math.cos(s.time * 0.8 + enemy.phase) *
                    enemy.speed *
                    0.2 *
                    dt;
            }

            if (
                this.hit(p, enemy) &&
                p.invuln <= 0
            ) {
                p.hp -=
                    d.contactDamage ?? 8;

                p.invuln = 0.6;
                p.combo = 0;
            }
        }
    }

    collect() {
        const s = this.state;
        const p = s.player;

        for (const pickup of s.pickups) {
            if (
                pickup.active &&
                this.hit(p, pickup)
            ) {
                pickup.active = false;
                s.score +=
                    this.definition.pickupScore ?? 50;
                s.objective++;

                p.hp = Math.min(
                    p.maxHp,
                    p.hp +
                        (this.definition.pickupHeal ?? 5)
                );
            }
        }

        for (const target of s.targets) {
            if (
                target.active &&
                this.hit(p, target) &&
                this.input?.wasPressed?.("interact")
            ) {
                target.active = false;
                s.objective++;
                s.score +=
                    this.definition.targetScore ?? 100;
            }
        }
    }

    updateMode() {
        const s = this.state;
        const d = this.definition;

        if (
            d.mode === "survival" &&
            s.time >= (d.timeLimit ?? 60)
        ) {
            s.won = true;
        }

        if (d.mode === "racing") {
            s.objective = Math.min(
                s.objectiveTotal,
                Math.floor(
                    s.time /
                    (d.lapTime ?? 8)
                )
            );

            if (
                s.objective >=
                s.objectiveTotal
            ) {
                s.won = true;
            }
        }

        if (
            d.mode === "puzzle" &&
            s.objective >=
            s.objectiveTotal
        ) {
            s.won = true;
        }

        if (
            d.mode !== "survival" &&
            d.mode !== "racing" &&
            s.objective >=
            s.objectiveTotal
        ) {
            s.won = true;
        }
    }

    checkEnd() {
        const s = this.state;

        if (s.player.hp <= 0) {
            s.lives--;

            if (s.lives > 0) {
                s.player.hp =
                    s.player.maxHp;

                s.player.x = 0.2;
                s.player.y = 0.5;
                s.player.invuln = 1;
            } else {
                this.finish("defeat");
            }
        }

        if (s.won) {
            this.finish("victory");
        }
    }

    finish(type) {
        if (
            this.state.status === "victory" ||
            this.state.status === "defeat"
        ) {
            return;
        }

        this.state.status =
            type === "victory"
                ? "victory"
                : "defeat";

        this.input?.disable?.();
        this.screen?.show?.(type);

        this.emit(type, this.state);
    }

    pause() {
        if (
            !this.running ||
            this.state.status !== "playing"
        ) {
            return;
        }

        this.paused = true;
        this.state.status = "paused";

        this.input?.disable?.();
        this.screen?.show?.("pause");
    }

    resume() {
        if (
            !this.running ||
            this.state.status !== "paused"
        ) {
            return;
        }

        this.paused = false;
        this.state.status = "playing";

        this.input?.enable?.();
        this.screen?.hide?.();

        this.lastTime = performance.now();
    }

    restart() {
        this.reset();
        this.start();
    }

    stop() {
        this.running = false;

        if (this.raf) {
            cancelAnimationFrame(this.raf);
        }

        this.raf = 0;
        this.input?.disable?.();
    }

    hit(a, b) {
        return (
            a.x < b.x + b.w &&
            a.x + a.w > b.x &&
            a.y < b.y + b.h &&
            a.y + a.h > b.y
        );
    }

    syncHUD() {
        const p = this.state.player;

        this.hud?.update?.({
            health: p.hp,
            maxHealth: p.maxHp,
            mana: p.mana,
            maxMana: p.maxMana,
            stamina: p.stamina,
            maxStamina: p.maxStamina,
            score: this.state.score,
            level: this.state.level,
            lives: this.state.lives
        });
    }

    render() {
        if (!this.ctx || !this.canvas) {
            return;
        }

        const c = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;
        const s = this.state;
        const d = this.definition;

        c.clearRect(0, 0, w, h);

        c.fillStyle =
            d.background || "#080808";

        c.fillRect(0, 0, w, h);

        for (const obstacle of s.obstacles) {
            this.drawRect(
                obstacle,
                "#252525"
            );
        }

        for (const pickup of s.pickups) {
            if (pickup.active) {
                this.drawRect(
                    pickup,
                    "#c9a94e"
                );
            }
        }

        for (const target of s.targets) {
            if (target.active) {
                this.drawRect(
                    target,
                    "#777777"
                );
            }
        }

        for (const enemy of s.enemies) {
            if (enemy.alive) {
                this.drawRect(
                    enemy,
                    "#7d293b"
                );
            }
        }

        for (const projectile of s.projectiles) {
            this.drawRect(
                projectile,
                "#eeeeee"
            );
        }

        this.drawRect(
            s.player,
            s.player.invuln > 0
                ? "#ffffff"
                : "#aaaaaa"
        );

        c.fillStyle = "#ffffff";
        c.font = "16px sans-serif";

        c.fillText(
            d.title,
            16,
            24
        );

        c.fillText(
            `${s.objective}/${s.objectiveTotal}`,
            16,
            46
        );
    }

    drawRect(object, color) {
        this.ctx.fillStyle = color;

        this.ctx.fillRect(
            object.x * this.canvas.width,
            object.y * this.canvas.height,
            object.w * this.canvas.width,
            object.h * this.canvas.height
        );
    }
}

window.AJVYRAWebPlayableGameEngine =
    AJVYRAWebPlayableGameEngine;
