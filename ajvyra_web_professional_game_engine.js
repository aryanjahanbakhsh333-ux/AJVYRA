class AJVYRAWebProfessionalGameEngine
    extends AJVYRAWebPlayableGameEngine {

    constructor(options = {}) {
        super(options);

        this.professional = {
            combo: 0,
            comboTimer: 0,

            wave: 1,
            maxWaves: 3,

            checkpoints: 0,
            checkpointsTotal: 5,

            coins: 0,
            collected: 0,

            boss: null,

            puzzleState: {
                sequence: [],
                solved: 0
            },

            strategy: {
                base: 100,
                enemyBases: []
            }
        };

        this.modeController = null;
    }

    load(definition) {
        super.load(definition);

        this.professional = {
            combo: 0,
            comboTimer: 0,

            wave: 1,
            maxWaves: definition.waves || 3,

            checkpoints: 0,
            checkpointsTotal:
                definition.checkpoints || 5,

            coins: 0,
            collected: 0,

            boss: null,

            puzzleState: {
                sequence:
                    definition.sequence || [],
                solved: 0
            },

            strategy: {
                base: 100,
                enemyBases: []
            }
        };

        this.setupProfessionalMode();

        return this;
    }

    setupProfessionalMode() {
        const d = this.definition;
        const p = this.professional;

        if (d.mode === "boss") {
            const boss = this.state.enemies[0];

            if (boss) {
                boss.hp = d.bossHp || 500;
                boss.maxHp = boss.hp;
                boss.w = 0.12;
                boss.h = 0.16;

                p.boss = boss;
            }
        }

        if (d.mode === "racing") {
            p.checkpoints =
                0;

            p.checkpointsTotal =
                d.checkpoints || 5;
        }

        if (d.mode === "strategy") {
            p.strategy.enemyBases =
                Array.from(
                    { length: d.enemyBases || 3 },
                    (_, index) => ({
                        id: index + 1,
                        hp: 100,
                        x:
                            0.65 +
                            index * 0.08,
                        y:
                            0.20 +
                            (index % 2) * 0.45
                    })
                );
        }
    }

    update(dt) {
        super.update(dt);

        if (
            !this.state ||
            this.state.status !== "playing"
        ) {
            return;
        }

        this.updateProfessionalCombat(dt);
        this.updateCombo(dt);
        this.updateSpecialMode(dt);
    }

    updateProfessionalCombat(dt) {
        const input = this.input;

        if (
            input?.wasPressed?.("attack")
        ) {
            this.professional.combo++;

            this.professional.comboTimer =
                2.0;

            this.state.score +=
                this.professional.combo * 5;
        }

        if (
            input?.wasPressed?.("special")
        ) {
            this.professional.combo += 2;
        }
    }

    updateCombo(dt) {
        const p = this.professional;

        if (p.comboTimer > 0) {
            p.comboTimer -= dt;
        } else {
            p.combo = 0;
        }
    }

    updateSpecialMode(dt) {
        const d = this.definition;
        const s = this.state;
        const p = this.professional;

        if (d.mode === "racing") {
            this.updateRacing(dt);
        }

        if (d.mode === "strategy") {
            this.updateStrategy(dt);
        }

        if (d.mode === "puzzle") {
            this.updatePuzzle();
        }

        if (d.mode === "boss") {
            this.updateBoss(dt);
        }

        if (d.mode === "survival") {
            this.updateWaves(dt);
        }

        if (
            s.objective >=
            s.objectiveTotal
        ) {
            s.won = true;
        }
    }

    updateRacing(dt) {
        const p = this.state.player;
        const checkpoints =
            this.professional;

        const next =
            Math.floor(
                this.state.time / 3
            );

        if (
            next > checkpoints.checkpoints
        ) {
            checkpoints.checkpoints =
                Math.min(
                    checkpoints.checkpointsTotal,
                    next
                );

            this.state.objective =
                checkpoints.checkpoints;

            this.state.score += 150;
        }

        if (
            checkpoints.checkpoints >=
            checkpoints.checkpointsTotal
        ) {
            this.state.won = true;
        }

        p.boost =
            Math.max(
                0,
                p.boost
            );
    }

    updateStrategy(dt) {
        const enemies =
            this.professional
                .strategy
                .enemyBases;

        if (!enemies.length) {
            this.state.won = true;
            return;
        }

        const destroyed =
            enemies.filter(
                base => base.hp <= 0
            ).length;

        this.state.objective =
            destroyed;

        if (
            destroyed >= enemies.length
        ) {
            this.state.won = true;
        }
    }

    updatePuzzle() {
        const d = this.definition;
        const input = this.input;

        if (
            !input?.wasPressed?.("interact")
        ) {
            return;
        }

        const puzzle =
            this.professional
                .puzzleState;

        puzzle.solved++;

        this.state.objective =
            puzzle.solved;

        this.state.score += 100;

        if (
            puzzle.solved >=
            (d.puzzleLength || 5)
        ) {
            this.state.won = true;
        }
    }

    updateBoss(dt) {
        const boss =
            this.professional.boss;

        if (!boss || !boss.alive) {
            this.state.won = true;
            return;
        }

        const pulse =
            Math.sin(
                this.state.time * 3
            );

        boss.x +=
            pulse *
            0.0008;

        boss.y +=
            Math.cos(
                this.state.time * 2
            ) *
            0.0005;

        if (
            boss.hp <=
            boss.maxHp * 0.5
        ) {
            boss.speed =
                Math.min(
                    0.16,
                    (boss.speed || 0.07) *
                    1.0005
                );
        }
    }

    updateWaves(dt) {
        const living =
            this.state.enemies
                .filter(
                    enemy => enemy.alive
                ).length;

        if (living === 0) {
            this.professional.wave++;

            if (
                this.professional.wave <=
                this.professional.maxWaves
            ) {
                this.spawnWave();
            } else {
                this.state.won = true;
            }
        }
    }

    spawnWave() {
        const amount =
            3 +
            this.professional.wave;

        for (
            let i = 0;
            i < amount;
            i++
        ) {
            this.state.enemies.push({
                x:
                    0.55 +
                    Math.random() * 0.35,

                y:
                    0.10 +
                    Math.random() * 0.75,

                w: 0.045,
                h: 0.07,

                hp:
                    25 +
                    this.professional.wave * 10,

                maxHp:
                    25 +
                    this.professional.wave * 10,

                speed:
                    0.05 +
                    this.professional.wave *
                    0.008,

                phase:
                    Math.random() * 6,

                alive: true
            });
        }
    }
}

window.AJVYRAWebProfessionalGameEngine =
    AJVYRAWebProfessionalGameEngine;
