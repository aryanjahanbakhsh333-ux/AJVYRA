(function (global) {
    "use strict";

    class AJVYRAProfessionalGameRuntime
        extends global.AJVYRAWebProfessionalGameEngine {

        constructor(options = {}) {
            super(options);

            this.mechanics =
                new global.AJVYRAProfessionalGameMechanics(
                    this,
                    options.scenario || {}
                );

            this.professionalRenderer =
                options.canvas
                    ? new global.AJVYRAProfessionalGameRenderer(
                        options.canvas,
                        this,
                        this.mechanics,
                        options.scenario || {}
                    )
                    : null;

            this.lastRuntimeTime = 0;
            this.runtimeRunning = false;
            this.runtimeFrame = null;
        }

        checkEnd() {
            if (!this.state) {
                return;
            }

            if (
                this.state.hp !== undefined &&
                this.state.hp <= 0
            ) {
                this.state.lost = true;
            }

            if (
                this.state.lost &&
                this.state.status === "playing"
            ) {
                this.finish("defeat");
            }
        }

        update(dt) {
            if (
                !this.state ||
                this.state.status !== "playing"
            ) {
                return;
            }

            const safeDt =
                Math.min(
                    Math.max(
                        Number(dt) || 0,
                        0
                    ),
                    0.05
                );

            /*
             * The parent engine handles:
             * movement
             * combat
             * enemies
             * generic gameplay
             *
             * checkEnd() is overridden above so
             * victory cannot terminate the frame
             * before specialized mechanics execute.
             */
            super.update(safeDt);

            if (
                this.state.status !== "playing"
            ) {
                return;
            }

            this.mechanics.update(
                safeDt
            );

            if (
                this.mechanics.isComplete()
            ) {
                this.state.won = true;
            }

            if (
                this.state.lost
            ) {
                this.finish("defeat");
                return;
            }

            if (
                this.state.won
            ) {
                this.finish("victory");
            }
        }

        render(dt) {
            if (
                this.professionalRenderer
            ) {
                this.professionalRenderer.render(
                    dt
                );
            }

            if (
                typeof super.render === "function"
            ) {
                super.render(dt);
            }
        }

        startProfessionalLoop() {
            if (this.runtimeRunning) {
                return;
            }

            this.runtimeRunning = true;

            this.lastRuntimeTime =
                performance.now();

            const frame = (timestamp) => {
                if (!this.runtimeRunning) {
                    return;
                }

                const dt =
                    Math.min(
                        0.05,
                        Math.max(
                            0,
                            (timestamp -
                                this.lastRuntimeTime) /
                                1000
                        )
                    );

                this.lastRuntimeTime =
                    timestamp;

                this.update(dt);
                this.render(dt);

                if (
                    this.state.status === "playing"
                ) {
                    this.runtimeFrame =
                        requestAnimationFrame(
                            frame
                        );
                } else {
                    this.runtimeRunning = false;
                }
            };

            this.runtimeFrame =
                requestAnimationFrame(frame);
        }

        stopProfessionalLoop() {
            this.runtimeRunning = false;

            if (
                this.runtimeFrame !== null
            ) {
                cancelAnimationFrame(
                    this.runtimeFrame
                );

                this.runtimeFrame = null;
            }
        }

        submitPuzzle(value) {
            this.mechanics.submitPuzzleInput(
                value
            );
        }

        damageBoss(amount) {
            this.mechanics.damageBoss(
                amount
            );
        }

        attackEnemyBase(amount) {
            return this.mechanics.attackEnemyBase(
                amount
            );
        }

        collectItem() {
            this.mechanics.collectItem();
        }

        grantXP(amount) {
            this.mechanics.grantXP(
                amount
            );
        }

        advanceQuest() {
            this.mechanics.advanceQuest();
        }

        enemyDefeated() {
            this.mechanics.enemyDefeated();
        }

        getProfessionalState() {
            return this.mechanics.serialize();
        }

        restoreProfessionalState(data) {
            return this.mechanics.restore(
                data
            );
        }

        destroy() {
            this.stopProfessionalLoop();

            this.professionalRenderer = null;
            this.mechanics = null;

            if (
                typeof super.destroy === "function"
            ) {
                super.destroy();
            }
        }
    }

    global.AJVYRAProfessionalGameRuntime =
        AJVYRAProfessionalGameRuntime;

})(window);
