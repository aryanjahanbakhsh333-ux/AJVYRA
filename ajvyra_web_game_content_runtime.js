class AJVYRAWebGameContentRuntime {
    constructor(options = {}) {
        this.registry = options.registry || null;
        this.activeGame = null;
        this.activeLevel = null;
        this.state = "idle";
        this.elapsedTime = 0;
    }

    loadGame(gameDefinition) {
        if (!gameDefinition || !gameDefinition.id) {
            throw new Error("Invalid game definition.");
        }

        this.activeGame = {
            ...gameDefinition,
            settings: {
                ...(gameDefinition.settings || {})
            }
        };

        this.activeLevel = null;
        this.elapsedTime = 0;
        this.state = "loaded";

        return this.activeGame;
    }

    start() {
        if (!this.activeGame) {
            throw new Error("No game has been loaded.");
        }

        this.state = "playing";
        this.elapsedTime = 0;
    }

    pause() {
        if (this.state === "playing") {
            this.state = "paused";
        }
    }

    resume() {
        if (this.state === "paused") {
            this.state = "playing";
        }
    }

    stop() {
        this.state = "stopped";
    }

    update(deltaTime) {
        if (this.state !== "playing") {
            return;
        }

        const dt = Math.max(
            0,
            Math.min(Number(deltaTime) || 0, 0.1)
        );

        this.elapsedTime += dt;
    }

    loadLevel(level) {
        if (!level || !level.id) {
            throw new Error("Invalid level definition.");
        }

        this.activeLevel = {
            ...level
        };

        return this.activeLevel;
    }

    getGame() {
        return this.activeGame;
    }

    getLevel() {
        return this.activeLevel;
    }

    getState() {
        return this.state;
    }

    getElapsedTime() {
        return this.elapsedTime;
    }

    reset() {
        this.activeLevel = null;
        this.elapsedTime = 0;
        this.state = this.activeGame
            ? "loaded"
            : "idle";
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameContentRuntime =
        AJVYRAWebGameContentRuntime;
}
