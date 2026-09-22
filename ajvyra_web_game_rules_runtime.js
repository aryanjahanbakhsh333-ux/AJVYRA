class AJVYRAWebGameRulesRuntime {
    constructor(rules = {}) {
        this.rules = {
            victory: rules.victory || null,
            defeat: rules.defeat || null,
            score: rules.score || {},
            timer: rules.timer || null,
            lives: rules.lives ?? null,
            objectives: rules.objectives || []
        };

        this.score = 0;
        this.lives = this.rules.lives;
        this.timeRemaining =
            this.rules.timer?.duration ?? null;

        this.objectives = this.rules.objectives.map(
            objective => ({
                id: objective.id,
                description:
                    objective.description || "",
                target:
                    Number(objective.target) || 1,
                progress: 0,
                completed: false
            })
        );

        this.result = null;
    }

    addScore(amount) {
        const value = Number(amount) || 0;

        this.score += value;

        return this.score;
    }

    loseLife(amount = 1) {
        if (this.lives === null) {
            return null;
        }

        this.lives = Math.max(
            0,
            this.lives - Math.max(1, Number(amount) || 1)
        );

        if (this.lives === 0) {
            this.result = "defeat";
        }

        return this.lives;
    }

    completeObjective(id, amount = 1) {
        const objective =
            this.objectives.find(item => item.id === id);

        if (!objective) {
            return false;
        }

        objective.progress = Math.min(
            objective.target,
            objective.progress + Math.max(
                0,
                Number(amount) || 0
            )
        );

        objective.completed =
            objective.progress >= objective.target;

        return objective.completed;
    }

    allObjectivesComplete() {
        return (
            this.objectives.length > 0 &&
            this.objectives.every(
                objective => objective.completed
            )
        );
    }

    update(deltaTime) {
        if (this.result) {
            return this.result;
        }

        if (this.timeRemaining !== null) {
            this.timeRemaining = Math.max(
                0,
                this.timeRemaining -
                Math.max(0, Number(deltaTime) || 0)
            );

            if (this.timeRemaining === 0) {
                this.result = "timeout";
            }
        }

        if (
            this.allObjectivesComplete() &&
            this.rules.victory === "objectives"
        ) {
            this.result = "victory";
        }

        return this.result;
    }

    checkVictory(context = {}) {
        if (this.result === "defeat") {
            return false;
        }

        if (this.rules.victory === "score") {
            return (
                this.score >=
                Number(context.targetScore || 0)
            );
        }

        if (this.rules.victory === "objectives") {
            return this.allObjectivesComplete();
        }

        if (typeof this.rules.victory === "function") {
            return Boolean(
                this.rules.victory(context)
            );
        }

        return false;
    }

    checkDefeat(context = {}) {
        if (this.result === "defeat") {
            return true;
        }

        if (typeof this.rules.defeat === "function") {
            return Boolean(
                this.rules.defeat(context)
            );
        }

        return this.lives === 0;
    }

    getState() {
        return {
            score: this.score,
            lives: this.lives,
            timeRemaining: this.timeRemaining,
            objectives: this.objectives.map(
                objective => ({ ...objective })
            ),
            result: this.result
        };
    }

    reset() {
        this.score = 0;
        this.lives = this.rules.lives;
        this.timeRemaining =
            this.rules.timer?.duration ?? null;

        for (const objective of this.objectives) {
            objective.progress = 0;
            objective.completed = false;
        }

        this.result = null;
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameRulesRuntime =
        AJVYRAWebGameRulesRuntime;
}
