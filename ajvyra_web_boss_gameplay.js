(function (global) {
    "use strict";

    class AJVYRABossGameplay {
        constructor(runtime) {
            this.runtime = runtime;

            this.boss = {
                hp: 1000,
                maxHp: 1000,
                phase: 1,
                enrage: false,
                attackTimer: 2,
                attackCooldown: 2
            };

            this.hazards = [];

            this.phaseThresholds = [
                0.75,
                0.50,
                0.25
            ];

            this.telegraph = null;
            this.finished = false;

            this.elapsed = 0;
        }

        update(dt) {
            if (this.finished) {
                return;
            }

            dt = Math.min(Math.max(dt || 0, 0), 0.05);

            this.elapsed += dt;

            this.updatePhase();

            this.boss.attackTimer -= dt;

            if (this.boss.attackTimer <= 0) {
                this.chooseAttack();
            }

            this.updateHazards(dt);
            this.updateEnrage();
        }

        updatePhase() {
            const ratio =
                this.boss.hp /
                this.boss.maxHp;

            let phase = 1;

            if (ratio <= 0.25) {
                phase = 4;
            } else if (ratio <= 0.50) {
                phase = 3;
            } else if (ratio <= 0.75) {
                phase = 2;
            }

            if (phase !== this.boss.phase) {
                this.boss.phase = phase;
                this.onPhaseChange(phase);
            }

            if (this.boss.hp <= 0) {
                this.finish(true);
            }
        }

        onPhaseChange(phase) {
            this.boss.attackCooldown =
                Math.max(
                    0.7,
                    2.2 - phase * 0.3
                );

            this.spawnPhaseHazard(phase);
        }

        updateEnrage() {
            const ratio =
                this.boss.hp /
                this.boss.maxHp;

            if (
                ratio <= 0.20 &&
                !this.boss.enrage
            ) {
                this.boss.enrage = true;
                this.boss.attackCooldown = 0.55;
            }
        }

        chooseAttack() {
            const attacks = [
                "slam",
                "projectile",
                "shockwave",
                "arenaHazard"
            ];

            const attack =
                attacks[
                    Math.floor(
                        Math.random() *
                        attacks.length
                    )
                ];

            this.telegraph = {
                type: attack,
                timer: this.boss.enrage
                    ? 0.35
                    : 0.65
            };

            this.boss.attackTimer =
                this.telegraph.timer;

            setTimeout(() => {
                if (
                    this.finished ||
                    !this.telegraph
                ) {
                    return;
                }

                this.executeAttack(
                    this.telegraph.type
                );

                this.telegraph = null;
            }, this.telegraph.timer * 1000);
        }

        executeAttack(type) {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return;
            }

            switch (type) {
                case "slam":
                    this.playerDamage(18);
                    break;

                case "projectile":
                    this.playerDamage(14);
                    break;

                case "shockwave":
                    this.playerDamage(24);
                    break;

                case "arenaHazard":
                    this.spawnArenaHazard();
                    break;
            }
        }

        playerDamage(amount) {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core || !core.player) {
                return;
            }

            if (
                typeof core.damagePlayer ===
                "function"
            ) {
                core.damagePlayer(amount);
                return;
            }

            core.player.hp = Math.max(
                0,
                (core.player.hp || 0) - amount
            );

            if (core.player.hp <= 0) {
                this.finish(false);
            }
        }

        spawnPhaseHazard(phase) {
            for (let i = 0; i < phase; i++) {
                this.spawnArenaHazard();
            }
        }

        spawnArenaHazard() {
            this.hazards.push({
                x:
                    120 +
                    Math.random() * 1040,
                y:
                    140 +
                    Math.random() * 420,
                radius:
                    35 +
                    Math.random() * 30,
                life: 4.5,
                warning: 1.25
            });
        }

        updateHazards(dt) {
            const core =
                this.runtime &&
                this.runtime.core;

            for (const hazard of this.hazards) {
                hazard.life -= dt;
                hazard.warning -= dt;

                if (
                    hazard.warning <= 0 &&
                    core &&
                    core.player
                ) {
                    const px =
                        core.player.x || 0;

                    const py =
                        core.player.y || 0;

                    const dx =
                        px - hazard.x;

                    const dy =
                        py - hazard.y;

                    const distance =
                        Math.sqrt(
                            dx * dx +
                            dy * dy
                        );

                    if (
                        distance <
                        hazard.radius
                    ) {
                        this.playerDamage(
                            12 * dt
                        );
                    }
                }
            }

            this.hazards =
                this.hazards.filter(
                    hazard =>
                        hazard.life > 0
                );
        }

        damage(amount) {
            if (this.finished) {
                return false;
            }

            const finalDamage =
                Math.max(
                    1,
                    Number(amount) || 0
                );

            this.boss.hp =
                Math.max(
                    0,
                    this.boss.hp -
                    finalDamage
                );

            this.updatePhase();

            return true;
        }

        finish(won) {
            if (this.finished) {
                return;
            }

            this.finished = true;

            const core =
                this.runtime &&
                this.runtime.core;

            if (core) {
                core.state =
                    won
                        ? "won"
                        : "lost";
            }
        }

        render(ctx) {
            if (!ctx) {
                return;
            }

            const width =
                ctx.canvas.width;

            const height =
                ctx.canvas.height;

            ctx.save();

            const barWidth =
                Math.min(
                    620,
                    width * 0.55
                );

            const x =
                (width - barWidth) / 2;

            const y = 76;

            ctx.fillStyle =
                "rgba(0,0,0,0.75)";

            ctx.fillRect(
                x,
                y,
                barWidth,
                20
            );

            ctx.fillStyle =
                this.boss.phase >= 3
                    ? "#ffffff"
                    : "#bbbbbb";

            ctx.fillRect(
                x,
                y,
                barWidth *
                Math.max(
                    0,
                    this.boss.hp /
                    this.boss.maxHp
                ),
                20
            );

            ctx.strokeStyle =
                "#ffffff";

            ctx.strokeRect(
                x,
                y,
                barWidth,
                20
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "bold 15px Arial";

            ctx.textAlign =
                "center";

            ctx.fillText(
                `BOSS • PHASE ${this.boss.phase}`,
                width / 2,
                y - 10
            );

            if (this.boss.enrage) {
                ctx.font =
                    "bold 22px Arial";

                ctx.fillText(
                    "ENRAGED",
                    width / 2,
                    height - 35
                );
            }

            for (const hazard of this.hazards) {
                ctx.beginPath();

                ctx.arc(
                    hazard.x,
                    hazard.y,
                    hazard.radius,
                    0,
                    Math.PI * 2
                );

                ctx.strokeStyle =
                    hazard.warning > 0
                        ? "#ffffff"
                        : "#888888";

                ctx.lineWidth = 3;

                ctx.stroke();

                if (
                    hazard.warning <= 0
                ) {
                    ctx.fillStyle =
                        "rgba(255,255,255,0.10)";

                    ctx.fill();
                }
            }

            ctx.restore();
        }

        action(action, payload = {}) {
            if (action === "bossDamage") {
                return this.damage(
                    payload.amount || 10
                );
            }

            if (action === "dodge") {
                this.runtime.dispatchGameAction?.(
                    "dodge",
                    payload
                );

                return true;
            }

            return false;
        }

        getState() {
            return {
                hp: this.boss.hp,
                maxHp: this.boss.maxHp,
                phase: this.boss.phase,
                enrage: this.boss.enrage,
                hazards: this.hazards.length,
                finished: this.finished
            };
        }
    }

    global.AJVYRABossGameplay =
        AJVYRABossGameplay;

})(window);
