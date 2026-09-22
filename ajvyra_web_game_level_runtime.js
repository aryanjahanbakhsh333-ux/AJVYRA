class AJVYRAWebGameLevelRuntime {
    constructor() {
        this.levels = new Map();
        this.currentLevelId = null;
        this.completedLevels = new Set();
    }

    register(level) {
        if (!level || !level.id) {
            throw new Error("Level must contain an id.");
        }

        this.levels.set(level.id, {
            ...level
        });

        return this.levels.get(level.id);
    }

    registerMany(levels) {
        if (!Array.isArray(levels)) {
            throw new TypeError("Levels must be an array.");
        }

        levels.forEach(level => this.register(level));

        return this;
    }

    load(id) {
        const level = this.levels.get(id);

        if (!level) {
            throw new Error(
                `Level "${id}" does not exist.`
            );
        }

        this.currentLevelId = id;

        return level;
    }

    getCurrent() {
        if (!this.currentLevelId) {
            return null;
        }

        return (
            this.levels.get(this.currentLevelId) ||
            null
        );
    }

    completeCurrent() {
        if (!this.currentLevelId) {
            return false;
        }

        this.completedLevels.add(
            this.currentLevelId
        );

        return true;
    }

    isCompleted(id) {
        return this.completedLevels.has(id);
    }

    getNextLevel() {
        const levels = [...this.levels.values()];
        const index = levels.findIndex(
            level => level.id === this.currentLevelId
        );

        if (index === -1 || index + 1 >= levels.length) {
            return null;
        }

        return levels[index + 1];
    }

    getAll() {
        return [...this.levels.values()];
    }

    resetProgress() {
        this.currentLevelId = null;
        this.completedLevels.clear();
    }
}

if (typeof window !== "undefined") {
    window.AJVYRAWebGameLevelRuntime =
        AJVYRAWebGameLevelRuntime;
}
