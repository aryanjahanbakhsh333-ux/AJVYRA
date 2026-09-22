(function (global) {
    "use strict";

    class AJVYRAProfessionalGameRenderer {
        constructor(canvas, engine, mechanics, scenario) {
            this.canvas = canvas;
            this.ctx = canvas.getContext("2d");
            this.engine = engine;
            this.mechanics = mechanics;
            this.scenario = scenario || {};

            this.particles = [];
            this.time = 0;

            this.resize();

            window.addEventListener(
                "resize",
                () => this.resize()
            );
        }

        resize() {
            const rect =
                this.canvas.getBoundingClientRect();

            const width =
                Math.max(320, rect.width || 960);

            const height =
                Math.max(240, rect.height || 540);

            const dpr =
                Math.min(
                    window.devicePixelRatio || 1,
                    2
                );

            this.canvas.width =
                Math.floor(width * dpr);

            this.canvas.height =
                Math.floor(height * dpr);

            this.canvas.style.width =
                `${width}px`;

            this.canvas.style.height =
                `${height}px`;

            this.ctx.setTransform(
                dpr,
                0,
                0,
                dpr,
                0,
                0
            );

            this.width = width;
            this.height = height;
        }

        render(dt) {
            if (!this.ctx) {
                return;
            }

            this.time += dt;

            this.clear();

            this.drawBackground();
            this.drawScenario();
            this.drawEntities();
            this.drawSpecialMechanics();
            this.drawParticles();
            this.drawCrosshair();
        }

        clear() {
            this.ctx.clearRect(
                0,
                0,
                this.width,
                this.height
            );
        }

        drawBackground() {
            const ctx = this.ctx;

            const gradient =
                ctx.createLinearGradient(
                    0,
                    0,
                    0,
                    this.height
                );

            gradient.addColorStop(
                0,
                "#07070a"
            );

            gradient.addColorStop(
                1,
                "#15151b"
            );

            ctx.fillStyle = gradient;

            ctx.fillRect(
                0,
                0,
                this.width,
                this.height
            );

            ctx.strokeStyle =
                "rgba(255,255,255,0.035)";

            ctx.lineWidth = 1;

            const grid = 48;

            for (
                let x = 0;
                x < this.width;
                x += grid
            ) {
                ctx.beginPath();
                ctx.moveTo(x, 0);
                ctx.lineTo(x, this.height);
                ctx.stroke();
            }

            for (
                let y = 0;
                y < this.height;
                y += grid
            ) {
                ctx.beginPath();
                ctx.moveTo(0, y);
                ctx.lineTo(this.width, y);
                ctx.stroke();
            }
        }

        drawScenario() {
            const mode =
                this.scenario.mode || "";

            if (mode === "racing") {
                this.drawRace();
            }

            if (mode === "strategy") {
                this.drawStrategy();
            }

            if (mode === "puzzle") {
                this.drawPuzzle();
            }

            if (mode === "boss") {
                this.drawBoss();
            }

            if (mode === "survival") {
                this.drawSurvival();
            }

            if (mode === "adventure") {
                this.drawAdventure();
            }
        }

        drawRace() {
            const race =
                this.mechanics.state.race;

            const ctx = this.ctx;

            ctx.strokeStyle =
                "rgba(255,255,255,0.16)";

            ctx.lineWidth = 80;

            ctx.beginPath();

            ctx.moveTo(80, 260);

            ctx.bezierCurveTo(
                280,
                100,
                620,
                420,
                920,
                240
            );

            ctx.stroke();

            ctx.strokeStyle =
                "rgba(255,255,255,0.05)";

            ctx.lineWidth = 2;

            for (
                const checkpoint
                of race.checkpoints
            ) {
                ctx.beginPath();

                ctx.arc(
                    checkpoint.x,
                    checkpoint.y,
                    28,
                    0,
                    Math.PI * 2
                );

                ctx.stroke();

                if (
                    checkpoint.passed
                ) {
                    ctx.fillStyle =
                        "rgba(255,255,255,0.18)";

                    ctx.fill();
                }
            }
        }

        drawStrategy() {
            const ctx = this.ctx;

            const bases =
                this.mechanics.state.strategy.bases;

            for (const base of bases) {
                ctx.fillStyle =
                    base.owner === "player"
                        ? "#d9d9df"
                        : "#5b5b65";

                ctx.fillRect(
                    base.x - 35,
                    base.y - 35,
                    70,
                    70
                );

                const health =
                    Math.max(
                        0,
                        base.health
                    );

                ctx.fillStyle =
                    "rgba(255,255,255,0.12)";

                ctx.fillRect(
                    base.x - 45,
                    base.y - 55,
                    90,
                    7
                );

                ctx.fillStyle =
                    "#eeeeee";

                ctx.fillRect(
                    base.x - 45,
                    base.y - 55,
                    90 * (health / 100),
                    7
                );
            }
        }

        drawPuzzle() {
            const ctx = this.ctx;

            const puzzle =
                this.mechanics.state.puzzle;

            const size = 64;
            const gap = 14;

            const startX =
                this.width / 2 -
                ((size * 4 + gap * 3) / 2);

            const y =
                this.height / 2 -
                size / 2;

            for (let i = 0; i < 4; i++) {
                const x =
                    startX +
                    i * (size + gap);

                ctx.fillStyle =
                    puzzle.playerSequence.length > i
                        ? "#dcdce2"
                        : "#1d1d24";

                ctx.fillRect(
                    x,
                    y,
                    size,
                    size
                );

                ctx.strokeStyle =
                    "rgba(255,255,255,0.18)";

                ctx.strokeRect(
                    x,
                    y,
                    size,
                    size
                );

                ctx.fillStyle =
                    "rgba(255,255,255,0.5)";

                ctx.font =
                    "18px system-ui";

                ctx.textAlign = "center";

                ctx.fillText(
                    String(i + 1),
                    x + size / 2,
                    y + size / 2 + 6
                );
            }
        }

        drawBoss() {
            const boss =
                this.mechanics.state.boss;

            const ctx = this.ctx;

            const radius =
                90 +
                Math.sin(this.time * 3) * 5;

            ctx.beginPath();

            ctx.arc(
                this.width / 2,
                this.height / 2,
                radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                boss.enraged
                    ? "#22222a"
                    : "#15151c";

            ctx.fill();

            ctx.strokeStyle =
                "#eeeeee";

            ctx.lineWidth = 3;

            ctx.stroke();

            const barWidth = 360;
            const barX =
                this.width / 2 -
                barWidth / 2;

            const barY = 80;

            ctx.fillStyle =
                "rgba(255,255,255,0.12)";

            ctx.fillRect(
                barX,
                barY,
                barWidth,
                14
            );

            ctx.fillStyle =
                "#ededed";

            ctx.fillRect(
                barX,
                barY,
                barWidth *
                    Math.max(
                        0,
                        boss.health /
                        boss.maxHealth
                    ),
                14
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "600 16px system-ui";

            ctx.textAlign =
                "center";

            ctx.fillText(
                `BOSS — PHASE ${boss.phase}`,
                this.width / 2,
                barY - 12
            );
        }

        drawSurvival() {
            const survival =
                this.mechanics.state.survival;

            const ctx = this.ctx;

            ctx.fillStyle =
                "rgba(255,255,255,0.04)";

            ctx.fillRect(
                20,
                20,
                180,
                56
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "600 16px system-ui";

            ctx.textAlign =
                "left";

            ctx.fillText(
                `WAVE ${survival.wave}`,
                36,
                45
            );

            ctx.font =
                "13px system-ui";

            ctx.fillText(
                `${survival.enemiesRemaining} enemies remaining`,
                36,
                64
            );
        }

        drawAdventure() {
            const collection =
                this.mechanics.state.collection;

            const ctx = this.ctx;

            ctx.fillStyle =
                "rgba(255,255,255,0.05)";

            ctx.fillRect(
                20,
                this.height - 70,
                240,
                42
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "600 15px system-ui";

            ctx.fillText(
                `COLLECT ${collection.collected}/${collection.required}`,
                36,
                this.height - 43
            );
        }

        drawEntities() {
            const player =
                this.engine.player;

            if (player) {
                this.drawEntity(
                    player,
                    true
                );
            }

            const enemies =
                this.engine.enemies || [];

            for (
                const enemy of enemies
            ) {
                if (
                    enemy &&
                    !enemy.dead
                ) {
                    this.drawEntity(
                        enemy,
                        false
                    );
                }
            }
        }

        drawEntity(entity, player) {
            const ctx = this.ctx;

            const x =
                Number(entity.x) || 0;

            const y =
                Number(entity.y) || 0;

            const radius =
                player ? 15 : 12;

            ctx.beginPath();

            ctx.arc(
                x,
                y,
                radius,
                0,
                Math.PI * 2
            );

            ctx.fillStyle =
                player
                    ? "#ffffff"
                    : "#777780";

            ctx.fill();

            ctx.strokeStyle =
                "rgba(255,255,255,0.35)";

            ctx.stroke();
        }

        drawSpecialMechanics() {
            const mode =
                this.scenario.mode || "";

            if (mode === "racing") {
                const race =
                    this.mechanics.state.race;

                this.drawText(
                    `LAP ${Math.min(
                        race.laps + 1,
                        race.totalLaps
                    )}/${race.totalLaps}`,
                    24,
                    this.height - 24
                );
            }

            if (mode === "strategy") {
                const strategy =
                    this.mechanics.state.strategy;

                this.drawText(
                    `RESOURCES ${Math.floor(
                        strategy.resources
                    )}`,
                    24,
                    30
                );
            }

            if (mode === "rpg") {
                const rpg =
                    this.mechanics.state.rpg;

                this.drawText(
                    `LV ${rpg.level}  XP ${Math.floor(
                        rpg.xp
                    )}`,
                    24,
                    30
                );
            }
        }

        drawParticles() {
            const ctx = this.ctx;

            for (
                const particle
                of this.particles
            ) {
                particle.x +=
                    particle.vx;

                particle.y +=
                    particle.vy;

                particle.life -= 1;

                ctx.globalAlpha =
                    Math.max(
                        0,
                        particle.life /
                        particle.maxLife
                    );

                ctx.fillStyle =
                    "#ffffff";

                ctx.fillRect(
                    particle.x,
                    particle.y,
                    2,
                    2
                );
            }

            ctx.globalAlpha = 1;

            this.particles =
                this.particles.filter(
                    (p) => p.life > 0
                );
        }

        burst(x, y, amount = 12) {
            for (
                let i = 0;
                i < amount;
                i++
            ) {
                const angle =
                    Math.random() *
                    Math.PI * 2;

                const speed =
                    0.5 +
                    Math.random() * 2;

                this.particles.push({
                    x,
                    y,
                    vx:
                        Math.cos(angle) *
                        speed,
                    vy:
                        Math.sin(angle) *
                        speed,
                    life: 30 +
                        Math.random() * 30,
                    maxLife: 60
                });
            }
        }

        drawCrosshair() {
            if (
                this.scenario.mode !== "shooter"
            ) {
                return;
            }

            const ctx = this.ctx;

            const x =
                this.width / 2;

            const y =
                this.height / 2;

            ctx.strokeStyle =
                "rgba(255,255,255,0.55)";

            ctx.lineWidth = 1;

            ctx.beginPath();

            ctx.moveTo(x - 10, y);
            ctx.lineTo(x + 10, y);

            ctx.moveTo(x, y - 10);
            ctx.lineTo(x, y + 10);

            ctx.stroke();
        }

        drawText(text, x, y) {
            const ctx = this.ctx;

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "600 14px system-ui";

            ctx.textAlign =
                "left";

            ctx.fillText(
                String(text),
                x,
                y
            );
        }
    }

    global.AJVYRAProfessionalGameRenderer =
        AJVYRAProfessionalGameRenderer;

})(window);
