class AJVYRAWebWorldLevel {
    constructor(options = {}) {
        this.id = String(
            options.id || ""
        );

        this.name = String(
            options.name || this.id
        );

        this.gameId = String(
            options.gameId || ""
        );

        this.width = Math.max(
            1,
            Number(options.width) || 1280
        );

        this.height = Math.max(
            1,
            Number(options.height) || 720
        );

        this.spawnPoints = new Map();

        this.exitPoints = [];

        this.requiredObjectives =
            Array.isArray(options.requiredObjectives)
                ? [...options.requiredObjectives]
                : [];

        this.metadata =
            options.metadata || {};

        this.completed = false;

        this.unlocked =
            options.unlocked !== false;
    }

    addSpawn(id, data = {}) {
        this.spawnPoints.set(
            String(id),
            {
                id: String(id),
                x: Number(data.x) || 0,
                y: Number(data.y) || 0,
                type: String(
                    data.type || "player"
                ),
                metadata:
                    data.metadata || {}
            }
        );

        return this.spawnPoints.get(
            String(id)
        );
    }

    getSpawn(id) {
        return this.spawnPoints.get(
            String(id)
        ) || null;
    }

    addExit(data = {}) {
        this.exitPoints.push({
            id: String(
                data.id ||
                `exit_${this.exitPoints.length}`
            ),
            x: Number(data.x) || 0,
            y: Number(data.y) || 0,
            width: Math.max(
                1,
                Number(data.width) || 32
            ),
            height: Math.max(
                1,
                Number(data.height) || 32
            ),
            targetLevel:
                data.targetLevel || null
        });
    }

    isObjectiveComplete(objectiveState = {}) {
        return this.requiredObjectives.every(
            objectiveId =>
                Boolean(
                    objectiveState[objectiveId]
                )
        );
    }

    complete(objectiveState = {}) {
        if (
            !this.isObjectiveComplete(
                objectiveState
            )
        ) {
            return false;
        }

        this.completed = true;
        return true;
    }

    toJSON() {
        return {
            id: this.id,
            name: this.name,
            gameId: this.gameId,
            width: this.width,
            height: this.height,
            spawnPoints:
                Array.from(
                    this.spawnPoints.values()
                ),
            exitPoints:
                [...this.exitPoints],
            requiredObjectives:
                [...this.requiredObjectives],
            metadata: this.metadata,
            completed: this.completed,
            unlocked: this.unlocked
        };
    }
}
