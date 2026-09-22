(function (global) {
    "use strict";

    class AJVYRASurvivalGameplay {
        constructor(runtime) {
            this.runtime = runtime;

            this.wave = 1;
            this.maxWave = 8;

            this.waveTimer = 0;
            this.waveDuration = 32;

            this.spawnTimer = 0;
            this.spawnInterval = 2.2;

            this.enemiesSpawned = 0;
            this.enemiesDefeated = 0;

            this.resources = {
                food: 100,
                scrap: 50,
                medicine: 3
            };

            this.threat = 0;
            this.night = true;

            this.finished = false;
        }

        update(dt) {
            if (this.finished) {
                return;
            }

            dt = Math.min(Math.max(dt || 0, 0), 0.05);

            this.waveTimer += dt;
            this.spawnTimer -= dt;

            this.threat = Math.min(
                100,
                this.threat + dt * 0.8
            );

            this.resources.food = Math.max(
                0,
                this.resources.food - dt * 0.9
            );

            if (this.spawnTimer <= 0) {
                this.spawnEnemy();

                this.spawnTimer =
                    Math.max(
                        0.65,
                        this.spawnInterval -
                        this.wave * 0.12
                    );
            }

            if (
                this.waveTimer >= this.waveDuration
            ) {
                this.advanceWave();
            }

            this.checkSurvivalState();
        }

        spawnEnemy() {
            const core = this.runtime && this.runtime.core;

            if (!core || !Array.isArray(core.enemies)) {
                return;
            }

            const enemyCount =
                1 +
                Math.floor(this.wave * 0.7);

            for (let i = 0; i < enemyCount; i++) {
                const enemy = {
                    id:
                        `survival-${Date.now()}-${Math.random()}`,
                    x:
                        Math.random() *
                        Math.max(
                            100,
                            core.world
                                ? core.world.width
                                : 1200
                        ),
                    y:
                        120 +
                        Math.random() *
                        420,
                    hp:
                        35 +
                        this.wave * 10,
                    maxHp:
                        35 +
                        this.wave * 10,
                    speed:
                        45 +
                        this.wave * 5,
                    damage:
                        5 +
                        this.wave * 1.5,
                    type:
                        this.selectEnemyType(),
                    dead: false
                };

                core.enemies.push(enemy);
                this.enemiesSpawned += 1;
            }
        }

        selectEnemyType() {
            const roll = Math.random();

            if (this.wave >= 6 && roll < 0.15) {
                return "elite";
            }

            if (roll < 0.25) {
                return "fast";
            }

            if (roll < 0.45) {
                return "ranged";
            }

            return "walker";
        }

        advanceWave() {
            this.waveTimer = 0;

            if (this.wave >= this.maxWave) {
                this.finish(true);
                return;
            }

            this.wave += 1;

            this.resources.scrap +=
                10 + this.wave * 3;

            this.resources.food +=
                15;

            this.threat = Math.min(
                100,
                this.threat + 8
            );

            this.spawnInterval = Math.max(
                0.7,
                this.spawnInterval - 0.12
            );
        }

        enemyDefeated() {
            this.enemiesDefeated += 1;

            this.resources.scrap += 2;

            this.threat = Math.max(
                0,
                this.threat - 1.5
            );
        }

        scavenge() {
            this.resources.food += 15;
            this.resources.scrap += 8;

            this.threat = Math.min(
                100,
                this.threat + 3
            );

            return true;
        }

        useMedicine() {
            if (this.resources.medicine <= 0) {
                return false;
            }

            const core = this.runtime && this.runtime.core;

            if (
                !core ||
                !core.player
            ) {
                return false;
            }

            this.resources.medicine -= 1;

            core.player.hp = Math.min(
                core.player.maxHp || 100,
                (core.player.hp || 0) + 35
            );

            return true;
        }

        toggleNight() {
            this.night = !this.night;
            return this.night;
        }

        checkSurvivalState() {
            const core = this.runtime && this.runtime.core;

            if (!core || !core.player) {
                return;
            }

            if (
                core.player.hp <= 0 ||
                this.resources.food <= 0
            ) {
                this.finish(false);
            }
        }

        finish(won) {
            this.finished = true;

            const core = this.runtime && this.runtime.core;

            if (!core) {
                return;
            }

            core.state = won
                ? "won"
                : "lost";
        }

        render(ctx) {
            if (!ctx) {
                return;
            }

            const width = ctx.canvas.width;

            ctx.save();

            ctx.fillStyle =
                "rgba(0,0,0,0.65)";

            ctx.fillRect(
                18,
                70,
                300,
                118
            );

            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 17px Arial";

            ctx.fillText(
                `WAVE ${this.wave}/${this.maxWave}`,
                32,
                96
            );

            ctx.font = "13px Arial";

            ctx.fillText(
                `Threat: ${Math.round(this.threat)}%`,
                32,
                119
            );

            ctx.fillText(
                `Food: ${Math.round(this.resources.food)}`,
                32,
                141
            );

            ctx.fillText(
                `Scrap: ${this.resources.scrap}`,
                32,
                162
            );

            ctx.fillText(
                `Defeated: ${this.enemiesDefeated}`,
                32,
                183
            );

            if (this.night) {
                ctx.fillStyle =
                    "rgba(10,15,35,0.20)";

                ctx.fillRect(
                    0,
                    0,
                    width,
                    ctx.canvas.height
                );
            }

            ctx.restore();
        }

        action(action) {
            switch (action) {
                case "scavenge":
                    return this.scavenge();

                case "medicine":
                    return this.useMedicine();

                case "toggleNight":
                    this.toggleNight();
                    return true;

                default:
                    return false;
            }
        }

        getState() {
            return {
                wave: this.wave,
                maxWave: this.maxWave,
                waveTimer: this.waveTimer,
                threat: this.threat,
                food: this.resources.food,
                scrap: this.resources.scrap,
                medicine: this.resources.medicine,
                enemiesSpawned: this.enemiesSpawned,
                enemiesDefeated: this.enemiesDefeated,
                night: this.night
            };
        }
    }

    global.AJVYRASurvivalGameplay =
        AJVYRASurvivalGameplay;

})(window);
