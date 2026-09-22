class AJVYRAWebGameLauncherRuntime {
    constructor(options = {}) {
        this.registry = options.registry || null;
        this.contentRuntime =
            options.contentRuntime || null;

        this.rulesRuntime = null;
        this.levelRuntime = null;

        this.currentGame = null;
        this.running = false;

        this.listeners = new Map();
    }

    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }

        this.listeners.get(event).add(callback);

        return () => {
            this.listeners.get(event)?.delete(callback);
        };
    }

    emit(event, data) {
        const listeners = this.listeners.get(event);

        if (!listeners) {
            return;
        }

        for (const callback of [...listeners]) {
            callback(data);
        }
    }

    load(gameId) {
        if (!this.registry) {
            throw new Error("Game registry is required.");
        }

        const game = this.registry.get(gameId);

        if (!game) {
            throw new Error(
                `Game "${gameId}" was not found.`
            );
        }

        this.currentGame = game;

        if (this.contentRuntime) {
            this.contentRuntime.loadGame(game);
        }

        this.rulesRuntime =
            new AJVYRAWebGameRulesRuntime(
                game.rules || {}
            );

        this.levelRuntime =
            new AJVYRAWebGameLevelRuntime();

        if (Array.isArray(game.levels)) {
            this.levelRuntime.registerMany(
                game.levels
            );
        }

        this.emit("loaded", game);

        return game;
    }

    start() {
        if (!this.currentGame) {
            throw new Error("No game loaded.");
        }

        if (this.contentRuntime) {
            this.contentRuntime.start();
        }

        this.running = true;

        this.emit("started", this.currentGame);
    }

    pause() {
        if (this.contentRuntime) {
            this.contentRuntime.pause();
        }

        this.running = false;

        this.emit("paused");
    }

    resume() {
        if (!this.currentGame) {
            return;
        }

        if (this.contentRuntime) {
            this.contentRuntime.resume();
        }

        this.running = true;

        this.emit("resumed");
    }

    update(deltaTime, context = {}) {
        if (!this.running) {
            return null;
        }

        if (this.contentRuntime) {
            this.contentRuntime.update(deltaTime);
        }

        if (this.rulesRuntime) {
            const result =
                this.rulesRuntime.update(deltaTime);

            if (result) {
                this.running = false;
                this.emit("finished", {
                    result,
                    state:
                        this.rulesRuntime.getState()
                });

                return result;
            }

            if (
                this.rulesRuntime.checkVictory(context)
            ) {
                this.running = false;
                this.rulesRuntime.result = "victory";

                this.emit("finished", {
                    result: "victory",
                    state:
                        this.rulesRuntime.getState()
                });

                return "victory";
            }

            if (
                this.rulesRuntime.checkDefeat(context)
            ) {
                this.running = false;
                this.rulesRuntime.result = "defeat";

                this.emit("finished", {
                    result: "defeat",
                    state:
                        this.rulesRuntime.getState()
                });

                return "defeat";
            }
        }

        return null;
    }

    stop() {
        this.running = false;

        if (this.contentRuntime) {
            this.contentRuntime.stop();
        }

        this.emit("stopped");
    }

    reset() {
        this.running = false;

        if (this.contentRuntime) {
            this.contentRuntime.reset();
        }

        if (this.rulesRuntime) {
            this.rulesRuntime.reset();
        }

        if (this.levelRuntime) {
            this.levelRuntime.resetProgress();
        }

        this.emit("reset");
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameLauncherRuntime =
        AJVYRAWebGameLauncherRuntime;
}
