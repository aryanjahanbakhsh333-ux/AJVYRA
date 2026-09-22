class AJVYRAWebGameLevelDirector {
    constructor(engine) {
        this.engine = engine;

        this.level = 1;
        this.maxLevel = 3;

        this.levelStarted = false;
    }

    load() {
        this.level = 1;
        this.levelStarted = false;
    }

    update() {
        const engine = this.engine;

        if (!engine?.state) {
            return;
        }

        if (
            engine.state.status !== "playing"
        ) {
            return;
        }

        if (!this.levelStarted) {
            this.startLevel();
        }

        if (
            engine.state.won &&
            this.level < this.maxLevel
        ) {
            this.nextLevel();
        }
    }

    startLevel() {
        this.levelStarted = true;

        this.engine.state.level =
            this.level;

        this.engine.state.score +=
            this.level * 50;
    }

    nextLevel() {
        this.level++;

        this.levelStarted = false;

        this.engine.state.won = false;

        this.engine.state.objective = 0;

        this.engine.state.objectiveTotal =
            Math.max(
                5,
                this.engine.definition
                    .objectiveTotal +
                this.level * 2
            );

        this.engine.state.enemies =
            [];

        this.engine.state.pickups =
            [];

        this.engine.spawnInitial();

        this.startLevel();
    }

    isComplete() {
        return (
            this.level >=
            this.maxLevel &&
            this.engine.state.won
        );
    }
}

window.AJVYRAWebGameLevelDirector =
    AJVYRAWebGameLevelDirector;
