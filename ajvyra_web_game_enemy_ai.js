"use strict";

class AJVYRAWebEnemyAI {
    constructor(enemy, options = {}) {
        if (!enemy) {
            throw new TypeError(
                "Enemy is required."
            );
        }

        this.enemy = enemy;

        this.target = null;

        this.detectionRange =
            Math.max(
                1,
                Number(
                    options.detectionRange || 500
                )
            );

        this.attackRange =
            Math.max(
                1,
                Number(
                    options.attackRange || 60
                )
            );

        this.attackCooldown =
            Math.max(
                0,
                Number(
                    options.attackCooldown || 1
                )
            );

        this.attackTimer = 0;

        this.fleeHealthRatio =
            Math.max(
                0,
                Math.min(
                    1,
                    Number(
                        options.fleeHealthRatio || 0.15
                    )
                )
            );

        this.patrolDistance =
            Math.max(
                0,
                Number(
                    options.patrolDistance || 180
                )
            );

        this.spawnX =
            enemy.body?.x || 0;

        this.patrolDirection = 1;

        this.stateMachine =
            new AJVYRAWebAIStateMachine(
                this
            );

        this._buildStates();

        this.stateMachine.changeState(
            "idle"
        );
    }

    _buildStates() {
        this.stateMachine.addState(
            new AJVYRAWebAIState(
                "idle",
                {
                    update: (owner, context) => {
                        const ai = owner;

                        ai.enemy.move(
                            0
                        );

                        if (ai.canSeeTarget()) {
                            ai.stateMachine.changeState(
                                "chase"
                            );
                        }
                    }
                }
            )
        );

        this.stateMachine.addState(
            new AJVYRAWebAIState(
                "patrol",
                {
                    update: (owner, context) => {
                        const ai = owner;

                        if (
                            ai.canSeeTarget()
                        ) {
                            ai.stateMachine.changeState(
                                "chase"
                            );

                            return;
                        }

                        const body =
                            ai.enemy.body;

                        if (!body) {
                            return;
                        }

                        const distance =
                            body.x -
                            ai.spawnX;

                        if (
                            Math.abs(distance) >=
                            ai.patrolDistance
                        ) {
                            ai.patrolDirection *= -1;
                        }

                        ai.enemy.move(
                            ai.patrolDirection
                        );
                    }
                }
            )
        );

        this.stateMachine.addState(
            new AJVYRAWebAIState(
                "chase",
                {
                    update: (owner) => {
                        const ai = owner;

                        if (
                            !ai.target ||
                            !ai.target.isAlive()
                        ) {
                            ai.target = null;

                            ai.stateMachine.changeState(
                                "patrol"
                            );

                            return;
                        }

                        const distance =
                            ai.enemy.distanceTo(
                                ai.target
                            );

                        if (
                            distance >
                            ai.detectionRange * 1.35
                        ) {
                            ai.target = null;

                            ai.stateMachine.changeState(
                                "patrol"
                            );

                            return;
                        }

                        if (
                            distance <=
                            ai.attackRange
                        ) {
                            ai.stateMachine.changeState(
                                "attack"
                            );

                            return;
                        }

                        const enemyBody =
                            ai.enemy.body;

                        const targetBody =
                            ai.target.body;

                        if (
                            !enemyBody ||
                            !targetBody
                        ) {
                            return;
                        }

                        const direction =
                            targetBody.centerX >
                            enemyBody.centerX
                                ? 1
                                : -1;

                        ai.enemy.move(
                            direction
                        );
                    }
                }
            )
        );

        this.stateMachine.addState(
            new AJVYRAWebAIState(
                "attack",
                {
                    enter: (owner) => {
                        owner.enemy.state =
                            "attacking";
                    },

                    update: (owner, context) => {
                        const ai = owner;

                        if (
                            !ai.target ||
                            !ai.target.isAlive()
                        ) {
                            ai.stateMachine.changeState(
                                "patrol"
                            );

                            return;
                        }

                        const distance =
                            ai.enemy.distanceTo(
                                ai.target
                            );

                        if (
                            distance >
                            ai.attackRange * 1.25
                        ) {
                            ai.stateMachine.changeState(
                                "chase"
                            );

                            return;
                        }

                        ai.enemy.move(0);

                        ai.attackTimer -=
                            context.delta;

                        if (
                            ai.attackTimer <= 0
                        ) {
                            ai.attack();

                            ai.attackTimer =
                                ai.attackCooldown;
                        }
                    }
                }
            )
        );

        this.stateMachine.addState(
            new AJVYRAWebAIState(
                "flee",
                {
                    update: (owner) => {
                        const ai = owner;

                        if (
                            !ai.target ||
                            !ai.target.isAlive()
                        ) {
                            ai.stateMachine.changeState(
                                "patrol"
                            );

                            return;
                        }

                        const enemyBody =
                            ai.enemy.body;

                        const targetBody =
                            ai.target.body;

                        if (
                            !enemyBody ||
                            !targetBody
                        ) {
                            return;
                        }

                        const direction =
                            targetBody.centerX >
                            enemyBody.centerX
                                ? -1
                                : 1;

                        ai.enemy.move(
                            direction,
                            true
                        );
                    }
                }
            )
        );
    }

    setTarget(target) {
        this.target = target;
    }

    canSeeTarget() {
        if (
            !this.target ||
            !this.target.isAlive()
        ) {
            return false;
        }

        return (
            this.enemy.distanceTo(
                this.target
            ) <= this.detectionRange
        );
    }

    attack() {
        if (
            !this.target ||
            !this.target.isAlive()
        ) {
            return false;
        }

        const distance =
            this.enemy.distanceTo(
                this.target
            );

        if (
            distance > this.attackRange
        ) {
            return false;
        }

        const damage =
            Math.max(
                0,
                Number(
                    this.enemy.attackDamage ||
                    10
                )
            );

        this.target.takeDamage(
            damage,
            this.enemy
        );

        return true;
    }

    update(delta) {
        if (
            !this.enemy.isAlive()
        ) {
            this.enemy.state =
                "dead";

            return;
        }

        if (
            this.enemy.getHealthRatio() <=
            this.fleeHealthRatio
        ) {
            if (
                this.target &&
                this.stateMachine.getState() !==
                    "flee"
            ) {
                this.stateMachine.changeState(
                    "flee"
                );
            }
        }

        this.stateMachine.update(
            delta
        );
    }

    getState() {
        return this.stateMachine.getState();
    }
}

window.AJVYRAWebEnemyAI =
    AJVYRAWebEnemyAI;
