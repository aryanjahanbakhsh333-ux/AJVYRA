(function (global) {
    "use strict";

    class AJVYRA30GameUniqueMechanics {

        static create(runtime, profile) {
            const genres = profile.genre || [];

            const systems = [];

            if (genres.includes("racing")) {
                systems.push(
                    new AJVYRARacingSystem(runtime)
                );
            }

            if (genres.includes("fighting")) {
                systems.push(
                    new AJVYRAFightingSystem(runtime)
                );
            }

            if (genres.includes("shooter")) {
                systems.push(
                    new AJVYRAShooterSystem(runtime)
                );
            }

            if (genres.includes("survival")) {
                systems.push(
                    new AJVYRASurvivalSystem(runtime)
                );
            }

            if (genres.includes("strategy")) {
                systems.push(
                    new AJVYRAStrategySystem(runtime)
                );
            }

            if (genres.includes("puzzle")) {
                systems.push(
                    new AJVYRAPuzzleSystem(runtime)
                );
            }

            if (genres.includes("horror")) {
                systems.push(
                    new AJVYRAHorrorSystem(runtime)
                );
            }

            if (genres.includes("boss")) {
                systems.push(
                    new AJVYRABossSystem(runtime)
                );
            }

            if (genres.includes("rpg")) {
                systems.push(
                    new AJVYRARPGSystem(runtime)
                );
            }

            if (genres.includes("adventure")) {
                systems.push(
                    new AJVYRAAdventureSystem(runtime)
                );
            }

            if (genres.includes("action")) {
                systems.push(
                    new AJVYRAActionSystem(runtime)
                );
            }

            return new AJVYRAUniqueMechanicsContainer(
                runtime,
                profile,
                systems
            );
        }
    }

    class AJVYRAUniqueMechanicsContainer {
        constructor(runtime, profile, systems) {
            this.runtime = runtime;
            this.profile = profile;
            this.systems = systems;
        }

        update(dt) {
            for (const system of this.systems) {
                system.update?.(dt);
            }
        }

        render(ctx) {
            for (const system of this.systems) {
                system.render?.(ctx);
            }
        }

        action(action, payload = {}) {
            let handled = false;

            for (const system of this.systems) {
                if (
                    system.action?.(
                        action,
                        payload
                    )
                ) {
                    handled = true;
                }
            }

            return handled;
        }

        getState() {
            return this.systems.map(
                system =>
                    system.getState?.() || {}
            );
        }
    }

    class AJVYRABaseSystem {
        constructor(runtime) {
            this.runtime = runtime;
        }

        get core() {
            return this.runtime?.core || null;
        }

        get player() {
            return this.core?.player || null;
        }

        score(value) {
            if (!this.core) return;

            if (
                typeof this.core.addScore ===
                "function"
            ) {
                this.core.addScore(value);
            } else {
                this.core.score =
                    (this.core.score || 0) +
                    value;
            }
        }
    }

    class AJVYRARacingSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.speed = 0;
            this.maxSpeed = 320;

            this.boost = 100;
            this.drift = 0;

            this.checkpoint = 0;
            this.totalCheckpoints = 6;

            this.finished = false;
        }

        update(dt) {
            if (!this.player) return;

            this.speed =
                Math.max(
                    0,
                    this.speed -
                    dt * 40
                );

            this.player.x +=
                this.speed * dt;

            if (
                this.player.x >
                (this.checkpoint + 1) * 450
            ) {
                this.checkpoint++;
                this.score(100);
            }

            if (
                this.checkpoint >=
                this.totalCheckpoints
            ) {
                this.finished = true;

                if (this.core) {
                    this.core.state =
                        "won";
                }
            }
        }

        accelerate() {
            this.speed =
                Math.min(
                    this.maxSpeed,
                    this.speed + 45
                );

            return true;
        }

        brake() {
            this.speed =
                Math.max(
                    0,
                    this.speed - 75
                );

            return true;
        }

        boostSpeed() {
            if (this.boost < 25) {
                return false;
            }

            this.boost -= 25;
            this.speed =
                Math.min(
                    this.maxSpeed * 1.5,
                    this.speed + 150
                );

            return true;
        }

        driftAction() {
            this.drift =
                Math.min(
                    100,
                    this.drift + 20
                );

            this.score(25);

            return true;
        }

        action(action) {
            if (action === "accelerate") {
                return this.accelerate();
            }

            if (action === "brake") {
                return this.brake();
            }

            if (action === "boost") {
                return this.boostSpeed();
            }

            if (action === "drift") {
                return this.driftAction();
            }

            return false;
        }

        render(ctx) {
            if (!ctx) return;

            ctx.save();

            ctx.fillStyle =
                "rgba(0,0,0,.7)";

            ctx.fillRect(
                360,
                18,
                260,
                55
            );

            ctx.fillStyle =
                "#fff";

            ctx.font =
                "14px Arial";

            ctx.fillText(
                `SPEED ${Math.round(this.speed)}`,
                375,
                42
            );

            ctx.fillText(
                `CHECKPOINT ${this.checkpoint}/${this.totalCheckpoints}`,
                375,
                62
            );

            ctx.restore();
        }

        getState() {
            return {
                speed: this.speed,
                boost: this.boost,
                checkpoint: this.checkpoint,
                finished: this.finished
            };
        }
    }

    class AJVYRAFightingSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.combo = 0;
            this.round = 1;
            this.enemyHP = 100;
            this.enemyMaxHP = 100;
            this.stamina = 100;
        }

        attack() {
            const damage =
                8 +
                this.combo * 3;

            this.combo++;

            this.enemyHP =
                Math.max(
                    0,
                    this.enemyHP - damage
                );

            this.score(
                20 + this.combo * 5
            );

            if (
                this.enemyHP <= 0
            ) {
                this.round++;

                if (this.round > 3) {
                    this.core.state =
                        "won";
                } else {
                    this.enemyHP =
                        this.enemyMaxHP;
                    this.combo = 0;
                }
            }

            return true;
        }

        dodge() {
            if (this.stamina < 20) {
                return false;
            }

            this.stamina -= 20;
            return true;
        }

        update(dt) {
            this.stamina =
                Math.min(
                    100,
                    this.stamina +
                    dt * 10
                );
        }

        action(action) {
            if (
                action === "attack" ||
                action === "melee"
            ) {
                return this.attack();
            }

            if (action === "dodge") {
                return this.dodge();
            }

            return false;
        }

        getState() {
            return {
                combo: this.combo,
                round: this.round,
                enemyHP: this.enemyHP,
                stamina: this.stamina
            };
        }
    }

    class AJVYRAShooterSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.ammo = 30;
            this.reserve = 120;
            this.kills = 0;
        }

        shoot() {
            if (this.ammo <= 0) {
                return false;
            }

            this.ammo--;

            const enemies =
                this.core?.enemies || [];

            const target =
                enemies.find(
                    enemy =>
                        enemy &&
                        !enemy.dead
                );

            if (target) {
                target.hp =
                    Math.max(
                        0,
                        (target.hp || 0) -
                        25
                    );

                if (target.hp <= 0) {
                    target.dead = true;
                    this.kills++;
                    this.score(50);
                }
            }

            return true;
        }

        reload() {
            if (this.reserve <= 0) {
                return false;
            }

            const needed =
                30 - this.ammo;

            const amount =
                Math.min(
                    needed,
                    this.reserve
                );

            this.ammo += amount;
            this.reserve -= amount;

            return true;
        }

        action(action) {
            if (action === "shoot") {
                return this.shoot();
            }

            if (action === "reload") {
                return this.reload();
            }

            return false;
        }

        getState() {
            return {
                ammo: this.ammo,
                reserve: this.reserve,
                kills: this.kills
            };
        }
    }

    class AJVYRASurvivalSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.wave = 1;
            this.maxWave = 8;
            this.time = 0;
            this.food = 100;
        }

        update(dt) {
            this.time += dt;

            this.food =
                Math.max(
                    0,
                    this.food -
                    dt * 0.35
                );

            if (
                this.time > 30
            ) {
                this.time = 0;
                this.wave++;

                if (
                    this.wave >
                    this.maxWave
                ) {
                    this.core.state =
                        "won";
                }
            }

            if (this.food <= 0) {
                this.core.state =
                    "lost";
            }
        }

        scavenge() {
            this.food =
                Math.min(
                    100,
                    this.food + 25
                );

            this.score(30);

            return true;
        }

        action(action) {
            if (action === "scavenge") {
                return this.scavenge();
            }

            return false;
        }

        getState() {
            return {
                wave: this.wave,
                maxWave: this.maxWave,
                food: this.food
            };
        }
    }

    class AJVYRAStrategySystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.resources = 100;
            this.base = 50;
            this.enemyBase = 100;
            this.units = 3;
        }

        build() {
            if (this.resources < 20) {
                return false;
            }

            this.resources -= 20;
            this.base += 10;

            return true;
        }

        deploy() {
            if (this.resources < 15) {
                return false;
            }

            this.resources -= 15;
            this.units++;

            this.enemyBase =
                Math.max(
                    0,
                    this.enemyBase -
                    12
                );

            this.score(40);

            if (
                this.enemyBase <= 0
            ) {
                this.core.state =
                    "won";
            }

            return true;
        }

        update(dt) {
            this.resources =
                Math.min(
                    200,
                    this.resources +
                    dt * 2
                );
        }

        action(action) {
            if (action === "build") {
                return this.build();
            }

            if (action === "deploy") {
                return this.deploy();
            }

            return false;
        }

        getState() {
            return {
                resources: this.resources,
                base: this.base,
                enemyBase: this.enemyBase,
                units: this.units
            };
        }
    }

    class AJVYRAPuzzleSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.level = 1;
            this.sequence = [];
            this.progress = 0;

            this.generate();
        }

        generate() {
            this.sequence = [];

            for (
                let i = 0;
                i < this.level + 2;
                i++
            ) {
                this.sequence.push(
                    Math.floor(
                        Math.random() * 4
                    )
                );
            }

            this.progress = 0;
        }

        input(value) {
            if (
                this.sequence[
                    this.progress
                ] !== value
            ) {
                this.progress = 0;
                return false;
            }

            this.progress++;

            if (
                this.progress >=
                this.sequence.length
            ) {
                this.score(
                    this.level * 100
                );

                this.level++;

                if (this.level > 5) {
                    this.core.state =
                        "won";
                } else {
                    this.generate();
                }
            }

            return true;
        }

        action(action, payload = {}) {
            if (action === "puzzle") {
                return this.input(
                    Number(payload.value)
                );
            }

            return false;
        }

        getState() {
            return {
                level: this.level,
                progress: this.progress,
                length:
                    this.sequence.length
            };
        }
    }

    class AJVYRAHorrorSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.tension = 0;
            this.sanity = 100;
            this.distance = 0;
        }

        update(dt) {
            this.tension =
                Math.min(
                    100,
                    this.tension +
                    dt * 2
                );

            this.sanity =
                Math.max(
                    0,
                    this.sanity -
                    dt * 0.4
                );

            if (
                this.sanity <= 0
            ) {
                this.core.state =
                    "lost";
            }

            if (
                this.distance >= 1000
            ) {
                this.core.state =
                    "won";
            }
        }

        hide() {
            this.tension =
                Math.max(
                    0,
                    this.tension - 15
                );

            return true;
        }

        action(action) {
            if (action === "hide") {
                return this.hide();
            }

            return false;
        }

        getState() {
            return {
                tension: this.tension,
                sanity: this.sanity,
                distance: this.distance
            };
        }
    }

    class AJVYRABossSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.hp = 1000;
            this.maxHP = 1000;
            this.phase = 1;
        }

        damage(value) {
            this.hp =
                Math.max(
                    0,
                    this.hp -
                    Math.max(
                        1,
                        Number(value) || 1
                    )
                );

            const ratio =
                this.hp /
                this.maxHP;

            this.phase =
                ratio <= 0.25
                    ? 4
                    : ratio <= 0.50
                        ? 3
                        : ratio <= 0.75
                            ? 2
                            : 1;

            if (this.hp <= 0) {
                this.core.state =
                    "won";
            }

            return true;
        }

        action(action, payload = {}) {
            if (action === "bossDamage") {
                return this.damage(
                    payload.amount || 10
                );
            }

            return false;
        }

        getState() {
            return {
                hp: this.hp,
                maxHP: this.maxHP,
                phase: this.phase
            };
        }
    }

    class AJVYRARPGSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.level = 1;
            this.xp = 0;
            this.gold = 0;
            this.quest = 0;
        }

        gainXP(value) {
            this.xp += value;

            const needed =
                this.level * 100;

            if (this.xp >= needed) {
                this.xp -= needed;
                this.level++;

                this.score(100);
            }

            return true;
        }

        completeQuest() {
            this.quest++;

            this.gold +=
                25 +
                this.quest * 10;

            this.gainXP(
                75
            );

            if (this.quest >= 5) {
                this.core.state =
                    "won";
            }

            return true;
        }

        action(action) {
            if (action === "quest") {
                return this.completeQuest();
            }

            return false;
        }

        getState() {
            return {
                level: this.level,
                xp: this.xp,
                gold: this.gold,
                quest: this.quest
            };
        }
    }

    class AJVYRAAdventureSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.locations = 0;
            this.totalLocations = 5;
        }

        discover() {
            this.locations++;

            this.score(80);

            if (
                this.locations >=
                this.totalLocations
            ) {
                this.core.state =
                    "won";
            }

            return true;
        }

        action(action) {
            if (
                action === "discover" ||
                action === "interact"
            ) {
                return this.discover();
            }

            return false;
        }

        getState() {
            return {
                locations: this.locations,
                total:
                    this.totalLocations
            };
        }
    }

    class AJVYRAActionSystem
        extends AJVYRABaseSystem {

        constructor(runtime) {
            super(runtime);

            this.combo = 0;
            this.energy = 100;
            this.checkpoint = 0;
            this.total = 5;
        }

        attack() {
            this.combo++;
            this.energy =
                Math.max(
                    0,
                    this.energy - 3
                );

            this.score(
                10 +
                this.combo * 2
            );

            return true;
        }

        dash() {
            if (this.energy < 20) {
                return false;
            }

            this.energy -= 20;

            if (this.player) {
                this.player.x += 180;
            }

            return true;
        }

        ability() {
            if (this.energy < 40) {
                return false;
            }

            this.energy -= 40;

            this.score(100);

            return true;
        }

        update(dt) {
            this.energy =
                Math.min(
                    100,
                    this.energy +
                    dt * 6
                );

            if (
                this.player &&
                this.player.x >
                (this.checkpoint + 1) *
                400
            ) {
                this.checkpoint++;

                this.score(100);

                if (
                    this.checkpoint >=
                    this.total
                ) {
                    this.core.state =
                        "won";
                }
            }
        }

        action(action) {
            if (
                action === "attack" ||
                action === "melee"
            ) {
                return this.attack();
            }

            if (action === "dash") {
                return this.dash();
            }

            if (action === "ability") {
                return this.ability();
            }

            return false;
        }

        getState() {
            return {
                combo: this.combo,
                energy: this.energy,
                checkpoint: this.checkpoint,
                total: this.total
            };
        }
    }

    global.AJVYRA30GameUniqueMechanics =
        AJVYRA30GameUniqueMechanics;

})(window);
