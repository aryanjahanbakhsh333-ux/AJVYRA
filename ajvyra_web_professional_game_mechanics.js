(function (global) {
    "use strict";

    class AJVYRAProfessionalGameMechanics {
        constructor(engine, scenario) {
            this.engine = engine;
            this.scenario = scenario || {};

            this.state = {
                race: {
                    checkpoints: [],
                    currentCheckpoint: 0,
                    laps: 0,
                    totalLaps: 3,
                    completed: false
                },

                strategy: {
                    bases: [],
                    selectedBase: 0,
                    playerBaseHealth: 100,
                    enemyBaseHealth: 100,
                    resources: 0
                },

                puzzle: {
                    sequence: [],
                    playerSequence: [],
                    solved: false,
                    mistakes: 0,
                    progress: 0
                },

                rpg: {
                    xp: 0,
                    level: 1,
                    gold: 0,
                    questStep: 0
                },

                boss: {
                    phase: 1,
                    health: 100,
                    maxHealth: 100,
                    enraged: false
                },

                survival: {
                    wave: 1,
                    enemiesRemaining: 0,
                    timer: 0
                },

                collection: {
                    collected: 0,
                    required: 0
                }
            };

            this.initialize();
        }

        initialize() {
            const mode = this.scenario.mode || "";

            if (mode === "racing") {
                this.initializeRace();
            }

            if (mode === "strategy") {
                this.initializeStrategy();
            }

            if (mode === "puzzle") {
                this.initializePuzzle();
            }

            if (mode === "rpg") {
                this.initializeRPG();
            }

            if (mode === "boss") {
                this.initializeBoss();
            }

            if (mode === "survival") {
                this.initializeSurvival();
            }

            if (mode === "adventure") {
                this.initializeCollection();
            }
        }

        initializeRace() {
            const count = 6;

            this.state.race.checkpoints = [];

            for (let i = 0; i < count; i++) {
                this.state.race.checkpoints.push({
                    id: i,
                    x: 140 + i * 180,
                    y: 220 + Math.sin(i * 1.4) * 80,
                    passed: false
                });
            }

            this.state.race.totalLaps = 3;
        }

        initializeStrategy() {
            this.state.strategy.bases = [
                {
                    id: "player",
                    x: 140,
                    y: 360,
                    health: 100,
                    owner: "player"
                },
                {
                    id: "enemy",
                    x: 820,
                    y: 180,
                    health: 100,
                    owner: "enemy"
                }
            ];

            this.state.strategy.resources = 25;
        }

        initializePuzzle() {
            const length = 5;

            this.state.puzzle.sequence = [];

            for (let i = 0; i < length; i++) {
                this.state.puzzle.sequence.push(
                    Math.floor(Math.random() * 4)
                );
            }
        }

        initializeRPG() {
            this.state.rpg = {
                xp: 0,
                level: 1,
                gold: 25,
                questStep: 0,
                questTotal: 5
            };
        }

        initializeBoss() {
            this.state.boss.maxHealth = 100;
            this.state.boss.health = 100;
            this.state.boss.phase = 1;
            this.state.boss.enraged = false;
        }

        initializeSurvival() {
            this.state.survival.wave = 1;
            this.state.survival.timer = 0;
            this.state.survival.enemiesRemaining = 5;
        }

        initializeCollection() {
            this.state.collection.required =
                Number(this.scenario.requiredCollectibles || 5);

            this.state.collection.collected = 0;
        }

        update(dt) {
            if (!this.engine || this.engine.state?.status !== "playing") {
                return;
            }

            const mode = this.scenario.mode || "";

            if (mode === "racing") {
                this.updateRace(dt);
            }

            if (mode === "strategy") {
                this.updateStrategy(dt);
            }

            if (mode === "puzzle") {
                this.updatePuzzle(dt);
            }

            if (mode === "rpg") {
                this.updateRPG(dt);
            }

            if (mode === "boss") {
                this.updateBoss(dt);
            }

            if (mode === "survival") {
                this.updateSurvival(dt);
            }

            if (mode === "adventure") {
                this.updateCollection(dt);
            }
        }

        updateRace(dt) {
            const player = this.engine.player;

            if (!player) {
                return;
            }

            const checkpoint =
                this.state.race.checkpoints[
                    this.state.race.currentCheckpoint
                ];

            if (!checkpoint) {
                return;
            }

            const dx = player.x - checkpoint.x;
            const dy = player.y - checkpoint.y;

            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 65) {
                checkpoint.passed = true;

                this.state.race.currentCheckpoint += 1;

                if (
                    this.state.race.currentCheckpoint >=
                    this.state.race.checkpoints.length
                ) {
                    this.state.race.currentCheckpoint = 0;
                    this.state.race.laps += 1;

                    for (const item of this.state.race.checkpoints) {
                        item.passed = false;
                    }
                }

                if (this.state.race.laps >= this.state.race.totalLaps) {
                    this.state.race.completed = true;
                }
            }
        }

        updateStrategy(dt) {
            const strategy = this.state.strategy;

            strategy.resources += dt * 2;

            const enemyBase = strategy.bases.find(
                (base) => base.owner === "enemy"
            );

            if (enemyBase && enemyBase.health <= 0) {
                enemyBase.health = 0;
                this.engine.state.won = true;
            }

            if (strategy.playerBaseHealth <= 0) {
                this.engine.state.lost = true;
            }
        }

        attackEnemyBase(amount) {
            const enemyBase = this.state.strategy.bases.find(
                (base) => base.owner === "enemy"
            );

            if (!enemyBase) {
                return false;
            }

            const damage = Math.max(
                1,
                Number(amount) || 1
            );

            enemyBase.health = Math.max(
                0,
                enemyBase.health - damage
            );

            return true;
        }

        updatePuzzle() {
            const puzzle = this.state.puzzle;

            if (
                puzzle.playerSequence.length ===
                puzzle.sequence.length
            ) {
                const correct =
                    puzzle.playerSequence.every(
                        (value, index) =>
                            value === puzzle.sequence[index]
                    );

                if (correct) {
                    puzzle.solved = true;
                    puzzle.progress = 100;
                    this.engine.state.won = true;
                } else {
                    puzzle.mistakes += 1;
                    puzzle.playerSequence = [];
                    puzzle.progress = 0;
                }
            } else {
                puzzle.progress =
                    (puzzle.playerSequence.length /
                        puzzle.sequence.length) *
                    100;
            }
        }

        submitPuzzleInput(value) {
            const puzzle = this.state.puzzle;

            if (puzzle.solved) {
                return;
            }

            const numeric = Number(value);

            if (!Number.isInteger(numeric) || numeric < 0 || numeric > 3) {
                return;
            }

            puzzle.playerSequence.push(numeric);

            this.updatePuzzle();
        }

        updateRPG() {
            const rpg = this.state.rpg;

            const required =
                rpg.level * 100;

            if (rpg.xp >= required) {
                rpg.xp -= required;
                rpg.level += 1;

                if (this.engine.player?.stats) {
                    this.engine.player.stats.level = rpg.level;
                }
            }

            if (
                rpg.questStep >= rpg.questTotal
            ) {
                this.engine.state.won = true;
            }
        }

        grantXP(amount) {
            this.state.rpg.xp += Math.max(
                0,
                Number(amount) || 0
            );
        }

        advanceQuest() {
            this.state.rpg.questStep = Math.min(
                this.state.rpg.questTotal,
                this.state.rpg.questStep + 1
            );
        }

        updateBoss() {
            const boss = this.state.boss;

            if (boss.health <= boss.maxHealth * 0.5) {
                boss.phase = 2;
                boss.enraged = true;
            }

            if (boss.health <= boss.maxHealth * 0.2) {
                boss.phase = 3;
            }

            if (boss.health <= 0) {
                boss.health = 0;
                this.engine.state.won = true;
            }
        }

        damageBoss(amount) {
            const boss = this.state.boss;

            if (boss.health <= 0) {
                return;
            }

            let damage = Math.max(
                1,
                Number(amount) || 1
            );

            if (boss.phase === 3) {
                damage *= 0.75;
            }

            boss.health = Math.max(
                0,
                boss.health - damage
            );
        }

        updateSurvival(dt) {
            const survival = this.state.survival;

            survival.timer += dt;

            if (survival.enemiesRemaining <= 0) {
                survival.wave += 1;
                survival.enemiesRemaining =
                    4 + survival.wave * 2;
                survival.timer = 0;
            }

            if (survival.wave >= 10) {
                this.engine.state.won = true;
            }
        }

        enemyDefeated() {
            if (
                this.scenario.mode !== "survival"
            ) {
                return;
            }

            this.state.survival.enemiesRemaining =
                Math.max(
                    0,
                    this.state.survival.enemiesRemaining - 1
                );
        }

        updateCollection() {
            const collection = this.state.collection;

            if (
                collection.collected >=
                collection.required
            ) {
                this.engine.state.won = true;
            }
        }

        collectItem() {
            const collection = this.state.collection;

            collection.collected = Math.min(
                collection.required,
                collection.collected + 1
            );
        }

        isComplete() {
            const mode = this.scenario.mode || "";

            if (mode === "racing") {
                return this.state.race.completed;
            }

            if (mode === "strategy") {
                return this.state.strategy.bases.some(
                    (base) =>
                        base.owner === "enemy" &&
                        base.health <= 0
                );
            }

            if (mode === "puzzle") {
                return this.state.puzzle.solved;
            }

            if (mode === "boss") {
                return this.state.boss.health <= 0;
            }

            if (mode === "survival") {
                return this.state.survival.wave >= 10;
            }

            if (mode === "adventure") {
                return (
                    this.state.collection.collected >=
                    this.state.collection.required
                );
            }

            if (mode === "rpg") {
                return (
                    this.state.rpg.questStep >=
                    this.state.rpg.questTotal
                );
            }

            return false;
        }

        serialize() {
            return JSON.parse(
                JSON.stringify(this.state)
            );
        }

        restore(data) {
            if (!data || typeof data !== "object") {
                return false;
            }

            this.state = {
                ...this.state,
                ...data
            };

            return true;
        }
    }

    global.AJVYRAProfessionalGameMechanics =
        AJVYRAProfessionalGameMechanics;

})(window);
