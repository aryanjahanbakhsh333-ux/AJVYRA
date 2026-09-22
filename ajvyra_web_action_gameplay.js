(function (global) {
    "use strict";

    class AJVYRAActionGameplay {
        constructor(runtime) {
            this.runtime = runtime;

            this.combo = 0;
            this.comboTimer = 0;

            this.dashCooldown = 0;
            this.abilityCooldown = 0;

            this.checkpoints = [
                {
                    x: 420,
                    reached: false
                },
                {
                    x: 920,
                    reached: false
                },
                {
                    x: 1480,
                    reached: false
                },
                {
                    x: 2100,
                    reached: false
                }
            ];

            this.currentCheckpoint = 0;

            this.abilityEnergy = 100;

            this.missionState =
                "in_progress";
        }

        update(dt) {
            dt = Math.min(Math.max(dt || 0, 0), 0.05);

            this.comboTimer =
                Math.max(
                    0,
                    this.comboTimer - dt
                );

            this.dashCooldown =
                Math.max(
                    0,
                    this.dashCooldown - dt
                );

            this.abilityCooldown =
                Math.max(
                    0,
                    this.abilityCooldown - dt
                );

            this.abilityEnergy =
                Math.min(
                    100,
                    this.abilityEnergy +
                    dt * 4
                );

            if (this.comboTimer <= 0) {
                this.combo = 0;
            }

            this.checkCheckpoint();

            if (
                this.currentCheckpoint >=
                this.checkpoints.length
            ) {
                this.missionState =
                    "complete";

                const core =
                    this.runtime &&
                    this.runtime.core;

                if (core) {
                    core.state = "won";
                }
            }
        }

        checkCheckpoint() {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core || !core.player) {
                return;
            }

            const playerX =
                core.player.x || 0;

            const checkpoint =
                this.checkpoints[
                    this.currentCheckpoint
                ];

            if (
                checkpoint &&
                playerX >= checkpoint.x
            ) {
                checkpoint.reached = true;
                this.currentCheckpoint += 1;

                this.onCheckpointReached();
            }
        }

        onCheckpointReached() {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return;
            }

            if (
                typeof core.addScore ===
                "function"
            ) {
                core.addScore(100);
            } else {
                core.score =
                    (core.score || 0) + 100;
            }

            this.abilityEnergy =
                Math.min(
                    100,
                    this.abilityEnergy + 20
                );
        }

        meleeAttack() {
            this.combo =
                this.comboTimer > 0
                    ? this.combo + 1
                    : 1;

            this.combo =
                Math.min(
                    this.combo,
                    8
                );

            this.comboTimer = 1.0;

            const damage =
                8 +
                this.combo * 3;

            const core =
                this.runtime &&
                this.runtime.core;

            if (
                core &&
                Array.isArray(core.enemies)
            ) {
                const player =
                    core.player;

                for (const enemy of core.enemies) {
                    if (!enemy || enemy.dead) {
                        continue;
                    }

                    const dx =
                        (enemy.x || 0) -
                        (player.x || 0);

                    const dy =
                        (enemy.y || 0) -
                        (player.y || 0);

                    const distance =
                        Math.sqrt(
                            dx * dx +
                            dy * dy
                        );

                    if (distance < 115) {
                        enemy.hp =
                            Math.max(
                                0,
                                (enemy.hp || 0) -
                                damage
                            );

                        if (enemy.hp <= 0) {
                            enemy.dead = true;
                        }

                        break;
                    }
                }
            }

            return damage;
        }

        dash(direction = 1) {
            if (
                this.dashCooldown > 0
            ) {
                return false;
            }

            const core =
                this.runtime &&
                this.runtime.core;

            if (!core || !core.player) {
                return false;
            }

            this.dashCooldown = 1.1;

            core.player.x +=
                190 *
                (direction >= 0 ? 1 : -1);

            if (
                core.world &&
                core.world.width
            ) {
                core.player.x =
                    Math.max(
                        0,
                        Math.min(
                            core.world.width,
                            core.player.x
                        )
                    );
            }

            return true;
        }

        useAbility() {
            if (
                this.abilityCooldown > 0 ||
                this.abilityEnergy < 30
            ) {
                return false;
            }

            this.abilityCooldown = 2.5;
            this.abilityEnergy -= 30;

            const core =
                this.runtime &&
                this.runtime.core;

            if (
                core &&
                Array.isArray(core.enemies)
            ) {
                for (const enemy of core.enemies) {
                    if (!enemy || enemy.dead) {
                        continue;
                    }

                    enemy.hp =
                        Math.max(
                            0,
                            (enemy.hp || 0) -
                            45
                        );

                    if (enemy.hp <= 0) {
                        enemy.dead = true;
                    }
                }
            }

            return true;
        }

        interact() {
            const core =
                this.runtime &&
                this.runtime.core;

            if (!core) {
                return false;
            }

            if (
                typeof core.addScore ===
                "function"
            ) {
                core.addScore(50);
            } else {
                core.score =
                    (core.score || 0) + 50;
            }

            return true;
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

            ctx.fillStyle =
                "rgba(0,0,0,0.65)";

            ctx.fillRect(
                width - 285,
                72,
                255,
                110
            );

            ctx.fillStyle =
                "#ffffff";

            ctx.font =
                "bold 15px Arial";

            ctx.textAlign =
                "left";

            ctx.fillText(
                `MISSION ${this.currentCheckpoint}/${this.checkpoints.length}`,
                width - 268,
                96
            );

            ctx.font =
                "13px Arial";

            ctx.fillText(
                `Combo: ${this.combo}`,
                width - 268,
                121
            );

            ctx.fillText(
                `Ability: ${Math.round(this.abilityEnergy)}%`,
                width - 268,
                145
            );

            ctx.fillText(
                this.missionState ===
                "complete"
                    ? "MISSION COMPLETE"
                    : "Reach the next checkpoint",
                width - 268,
                169
            );

            ctx.restore();

            for (
                let i = 0;
                i < this.checkpoints.length;
                i++
            ) {
                const checkpoint =
                    this.checkpoints[i];

                ctx.save();

                ctx.strokeStyle =
                    checkpoint.reached
                        ? "#ffffff"
                        : "#777777";

                ctx.lineWidth = 3;

                ctx.beginPath();

                ctx.moveTo(
                    checkpoint.x,
                    100
                );

                ctx.lineTo(
                    checkpoint.x,
                    height - 70
                );

                ctx.stroke();

                ctx.restore();
            }
        }

        action(action, payload = {}) {
            switch (action) {
                case "attack":
                case "melee":
                    return this.meleeAttack();

                case "dash":
                    return this.dash(
                        payload.direction || 1
                    );

                case "ability":
                    return this.useAbility();

                case "interact":
                    return this.interact();

                default:
                    return false;
            }
        }

        getState() {
            return {
                combo: this.combo,
                dashCooldown: this.dashCooldown,
                abilityCooldown:
                    this.abilityCooldown,
                abilityEnergy:
                    this.abilityEnergy,
                currentCheckpoint:
                    this.currentCheckpoint,
                totalCheckpoints:
                    this.checkpoints.length,
                missionState:
                    this.missionState
            };
        }
    }

    global.AJVYRAActionGameplay =
        AJVYRAActionGameplay;

})(window);
