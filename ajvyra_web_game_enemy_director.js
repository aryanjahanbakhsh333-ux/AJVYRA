class AJVYRAWebGameEnemyDirector {
    constructor(engine) {
        this.engine = engine;
    }

    update(dt) {
        const engine = this.engine;

        if (
            !engine?.state ||
            engine.state.status !== "playing"
        ) {
            return;
        }

        const enemies =
            engine.state.enemies;

        const player =
            engine.state.player;

        const mode =
            engine.definition.mode;

        for (
            const [index, enemy]
            of enemies.entries()
        ) {
            if (!enemy.alive) {
                continue;
            }

            const behavior =
                this.getBehavior(
                    mode,
                    index
                );

            this.applyBehavior(
                behavior,
                enemy,
                player,
                dt
            );
        }
    }

    getBehavior(mode, index) {
        if (mode === "horror") {
            return index % 2 === 0
                ? "stalker"
                : "ambusher";
        }

        if (mode === "shooter") {
            return "ranged";
        }

        if (mode === "fighting") {
            return index % 2 === 0
                ? "aggressive"
                : "defensive";
        }

        if (mode === "boss") {
            return "boss";
        }

        if (mode === "survival") {
            return "hunter";
        }

        if (mode === "strategy") {
            return "guard";
        }

        return "wander";
    }

    applyBehavior(
        behavior,
        enemy,
        player,
        dt
    ) {
        const dx =
            player.x - enemy.x;

        const dy =
            player.y - enemy.y;

        const distance =
            Math.hypot(dx, dy) || 1;

        const speed =
            enemy.speed || 0.06;

        if (behavior === "stalker") {
            enemy.x +=
                (dx / distance) *
                speed *
                dt *
                0.9;

            enemy.y +=
                (dy / distance) *
                speed *
                dt *
                0.9;

            return;
        }

        if (behavior === "ambusher") {
            enemy.x +=
                Math.sign(dx) *
                speed *
                dt *
                0.35;

            enemy.y +=
                Math.sign(dy) *
                speed *
                dt *
                0.35;

            if (distance < 0.25) {
                enemy.x +=
                    (dx / distance) *
                    speed *
                    dt;

                enemy.y +=
                    (dy / distance) *
                    speed *
                    dt;
            }

            return;
        }

        if (behavior === "ranged") {
            if (distance < 0.22) {
                enemy.x -=
                    (dx / distance) *
                    speed *
                    dt;

                enemy.y -=
                    (dy / distance) *
                    speed *
                    dt;
            }

            return;
        }

        if (behavior === "aggressive") {
            enemy.x +=
                (dx / distance) *
                speed *
                dt *
                1.25;

            enemy.y +=
                (dy / distance) *
                speed *
                dt *
                1.25;

            return;
        }

        if (behavior === "defensive") {
            if (distance < 0.3) {
                enemy.x -=
                    (dx / distance) *
                    speed *
                    dt;

                enemy.y -=
                    (dy / distance) *
                    speed *
                    dt;
            }

            return;
        }

        if (behavior === "boss") {
            enemy.x +=
                Math.sin(
                    this.engine.state.time
                ) *
                speed *
                dt;

            enemy.y +=
                Math.cos(
                    this.engine.state.time *
                    0.7
                ) *
                speed *
                dt;

            return;
        }

        if (behavior === "guard") {
            enemy.x +=
                Math.sin(
                    this.engine.state.time
                ) *
                speed *
                0.15 *
                dt;

            return;
        }

        enemy.x +=
            Math.sin(
                this.engine.state.time +
                enemy.phase
            ) *
            speed *
            dt *
            0.4;

        enemy.y +=
            Math.cos(
                this.engine.state.time +
                enemy.phase
            ) *
            speed *
            dt *
            0.4;
    }
}

window.AJVYRAWebGameEnemyDirector =
    AJVYRAWebGameEnemyDirector;
