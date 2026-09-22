(function (global) {
    "use strict";

    class AJVYRAFightingGameplay {
        constructor(runtime) {
            this.runtime = runtime;

            this.player = {
                stamina: 100,
                combo: 0,
                comboTimer: 0,
                blocking: false,
                dodging: false,
                attackCooldown: 0,
                parryWindow: 0
            };

            this.opponent = {
                hp: 100,
                maxHp: 100,
                stamina: 100,
                state: "idle",
                attackCooldown: 0,
                decisionTimer: 0,
                attackTimer: 0
            };

            this.round = 1;
            this.maxRounds = 3;
            this.playerRounds = 0;
            this.enemyRounds = 0;

            this.lastHitTime = 0;
            this.hitFlash = 0;
        }

        update(dt) {
            dt = Math.min(Math.max(dt || 0, 0), 0.05);

            this.player.attackCooldown = Math.max(
                0,
                this.player.attackCooldown - dt
            );

            this.player.comboTimer = Math.max(
                0,
                this.player.comboTimer - dt
            );

            this.player.parryWindow = Math.max(
                0,
                this.player.parryWindow - dt
            );

            this.opponent.attackCooldown = Math.max(
                0,
                this.opponent.attackCooldown - dt
            );

            this.opponent.decisionTimer -= dt;

            if (this.player.comboTimer <= 0) {
                this.player.combo = 0;
            }

            this.updateOpponentAI(dt);
            this.updateVisualFeedback(dt);
        }

        updateOpponentAI(dt) {
            if (this.opponent.decisionTimer > 0) {
                return;
            }

            this.opponent.decisionTimer =
                0.35 + Math.random() * 0.8;

            const roll = Math.random();

            if (roll < 0.32) {
                this.opponent.state = "aggressive";
            } else if (roll < 0.55) {
                this.opponent.state = "defensive";
            } else if (roll < 0.78) {
                this.opponent.state = "counter";
            } else {
                this.opponent.state = "idle";
            }

            if (
                this.opponent.state === "aggressive" &&
                this.opponent.attackCooldown <= 0
            ) {
                this.opponentAttack();
            }

            if (
                this.opponent.state === "counter" &&
                this.opponent.attackCooldown <= 0
            ) {
                this.opponentAttack();
            }

            if (
                this.opponent.state === "defensive" &&
                Math.random() < 0.35
            ) {
                this.player.blocking = false;
            }
        }

        opponentAttack() {
            this.opponent.attackCooldown = 1.0;
            this.opponent.attackTimer = 0.25;

            if (this.player.dodging) {
                return;
            }

            if (this.player.parryWindow > 0) {
                this.parryOpponent();
                return;
            }

            if (this.player.blocking) {
                this.player.stamina = Math.max(
                    0,
                    this.player.stamina - 18
                );

                if (this.player.stamina <= 0) {
                    this.player.blocking = false;
                }

                return;
            }

            this.damagePlayer(12 + Math.floor(Math.random() * 8));
        }

        damagePlayer(amount) {
            const core = this.runtime && this.runtime.core;

            if (!core || !core.player) {
                return;
            }

            if (typeof core.damagePlayer === "function") {
                core.damagePlayer(amount);
                return;
            }

            if (typeof core.player.hp === "number") {
                core.player.hp = Math.max(
                    0,
                    core.player.hp - amount
                );
            }
        }

        playerAttack(power = 1) {
            if (this.player.attackCooldown > 0) {
                return false;
            }

            this.player.attackCooldown =
                Math.max(0.18, 0.42 - this.player.combo * 0.025);

            if (this.player.comboTimer > 0) {
                this.player.combo += 1;
            } else {
                this.player.combo = 1;
            }

            this.player.combo = Math.min(
                this.player.combo,
                10
            );

            this.player.comboTimer = 1.2;

            const baseDamage = 10 * power;
            const comboBonus =
                1 + Math.min(this.player.combo * 0.08, 0.8);

            let damage =
                Math.round(baseDamage * comboBonus);

            if (
                this.opponent.state === "defensive"
            ) {
                damage = Math.round(damage * 0.45);
            }

            this.damageOpponent(damage);

            this.lastHitTime = 0;
            this.hitFlash = 0.12;

            return true;
        }

        damageOpponent(amount) {
            this.opponent.hp = Math.max(
                0,
                this.opponent.hp - amount
            );

            if (this.opponent.hp <= 0) {
                this.finishRound(true);
            }
        }

        block() {
            if (this.player.stamina <= 0) {
                return false;
            }

            this.player.blocking = true;
            this.player.parryWindow = 0.16;

            return true;
        }

        releaseBlock() {
            this.player.blocking = false;
        }

        dodge() {
            if (this.player.stamina < 20) {
                return false;
            }

            this.player.stamina -= 20;
            this.player.dodging = true;

            setTimeout(() => {
                this.player.dodging = false;
            }, 260);

            return true;
        }

        parryOpponent() {
            this.opponent.attackCooldown = 1.4;
            this.opponent.state = "stunned";

            this.player.combo += 1;
            this.player.comboTimer = 1.5;

            this.damageOpponent(24);
        }

        finishRound(playerWon) {
            if (playerWon) {
                this.playerRounds += 1;
            } else {
                this.enemyRounds += 1;
            }

            if (
                this.playerRounds >= 2 ||
                this.enemyRounds >= 2
            ) {
                this.finishMatch(
                    this.playerRounds > this.enemyRounds
                );
                return;
            }

            this.round += 1;

            this.opponent.hp = this.opponent.maxHp;
            this.player.stamina = 100;
            this.player.combo = 0;

            this.opponent.state = "idle";
            this.opponent.attackCooldown = 1.0;
        }

        finishMatch(playerWon) {
            const core = this.runtime && this.runtime.core;

            if (!core) {
                return;
            }

            if (playerWon) {
                core.state = "won";
            } else {
                core.state = "lost";
            }
        }

        updateVisualFeedback(dt) {
            this.hitFlash = Math.max(
                0,
                this.hitFlash - dt
            );

            this.lastHitTime += dt;
        }

        render(ctx) {
            if (!ctx) {
                return;
            }

            const width = ctx.canvas.width;
            const height = ctx.canvas.height;

            const barWidth = Math.min(
                320,
                width * 0.32
            );

            const y = 32;

            this.drawBar(
                ctx,
                width * 0.08,
                y,
                barWidth,
                16,
                this.runtime && this.runtime.core &&
                this.runtime.core.player
                    ? this.runtime.core.player.hp || 0
                    : 0,
                100,
                "PLAYER"
            );

            this.drawBar(
                ctx,
                width * 0.60,
                y,
                barWidth,
                16,
                this.opponent.hp,
                this.opponent.maxHp,
                "OPPONENT"
            );

            ctx.save();

            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 18px Arial";
            ctx.textAlign = "center";

            ctx.fillText(
                `ROUND ${this.round}`,
                width / 2,
                46
            );

            if (this.player.combo > 1) {
                ctx.font = "bold 28px Arial";

                ctx.fillText(
                    `${this.player.combo} HIT`,
                    width / 2,
                    height - 70
                );
            }

            ctx.restore();
        }

        drawBar(
            ctx,
            x,
            y,
            width,
            height,
            value,
            max,
            label
        ) {
            const ratio = Math.max(
                0,
                Math.min(1, value / Math.max(max, 1))
            );

            ctx.save();

            ctx.fillStyle = "rgba(0,0,0,0.65)";
            ctx.fillRect(
                x,
                y,
                width,
                height
            );

            ctx.fillStyle =
                ratio > 0.45
                    ? "#ffffff"
                    : "#777777";

            ctx.fillRect(
                x,
                y,
                width * ratio,
                height
            );

            ctx.strokeStyle = "#ffffff";
            ctx.strokeRect(
                x,
                y,
                width,
                height
            );

            ctx.fillStyle = "#ffffff";
            ctx.font = "11px Arial";
            ctx.textAlign = "left";

            ctx.fillText(
                label,
                x,
                y - 7
            );

            ctx.restore();
        }

        action(action, payload = {}) {
            switch (action) {
                case "attack":
                    return this.playerAttack(
                        payload.power || 1
                    );

                case "heavyAttack":
                    return this.playerAttack(1.7);

                case "block":
                    return this.block();

                case "releaseBlock":
                    this.releaseBlock();
                    return true;

                case "parry":
                    this.player.parryWindow = 0.22;
                    return true;

                case "dodge":
                    return this.dodge();

                default:
                    return false;
            }
        }

        getState() {
            return {
                round: this.round,
                playerRounds: this.playerRounds,
                enemyRounds: this.enemyRounds,
                playerCombo: this.player.combo,
                playerStamina: this.player.stamina,
                opponentHP: this.opponent.hp,
                opponentState: this.opponent.state
            };
        }
    }

    global.AJVYRAFightingGameplay =
        AJVYRAFightingGameplay;

})(window);
