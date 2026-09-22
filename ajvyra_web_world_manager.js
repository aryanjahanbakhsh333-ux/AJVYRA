class AJVYRAWebWorldManager {
    constructor() {
        this.levels = new Map();

        this.currentLevelId = null;

        this.tilemaps = new Map();

        this.layers = new Map();

        this.objects = new Map();
    }

    registerLevel(level) {
        const value =
            level instanceof AJVYRAWebWorldLevel
                ? level
                : new AJVYRAWebWorldLevel(level);

        if (!value.id) {
            return null;
        }

        this.levels.set(
            value.id,
            value
        );

        return value;
    }

    registerTilemap(tilemap) {
        const value =
            tilemap instanceof AJVYRAWebWorldTileMap
                ? tilemap
                : new AJVYRAWebWorldTileMap(tilemap);

        if (!value.id) {
            return null;
        }

        this.tilemaps.set(
            value.id,
            value
        );

        return value;
    }

    registerLayers(levelId, layerManager) {
        this.layers.set(
            String(levelId),
            layerManager
        );

        return layerManager;
    }

    registerObjects(levelId, objectManager) {
        this.objects.set(
            String(levelId),
            objectManager
        );

        return objectManager;
    }

    getLevel(id) {
        return this.levels.get(
            String(id)
        ) || null;
    }

    getCurrentLevel() {
        if (!this.currentLevelId) {
            return null;
        }

        return this.getLevel(
            this.currentLevelId
        );
    }

    loadLevel(id) {
        const level =
            this.getLevel(id);

        if (!level) {
            return {
                success: false,
                reason: "level_not_found"
            };
        }

        if (!level.unlocked) {
            return {
                success: false,
                reason: "level_locked"
            };
        }

        this.currentLevelId =
            level.id;

        return {
            success: true,
            level
        };
    }

    unloadLevel() {
        this.currentLevelId = null;
    }

    getCurrentTilemap() {
        const level =
            this.getCurrentLevel();

        if (!level) {
            return null;
        }

        return this.tilemaps.get(
            level.metadata.tilemapId
        ) || null;
    }

    getCurrentLayers() {
        if (!this.currentLevelId) {
            return null;
        }

        return this.layers.get(
            this.currentLevelId
        ) || null;
    }

    getCurrentObjects() {
        if (!this.currentLevelId) {
            return null;
        }

        return this.objects.get(
            this.currentLevelId
        ) || null;
    }

    completeCurrentLevel(
        objectiveState = {}
    ) {
        const level =
            this.getCurrentLevel();

        if (!level) {
            return false;
        }

        return level.complete(
            objectiveState
        );
    }

    getLevelProgress() {
        const result = [];

        for (const level of this.levels.values()) {
            result.push({
                id: level.id,
                name: level.name,
                gameId: level.gameId,
                unlocked: level.unlocked,
                completed: level.completed
            });
        }

        return result;
    }

    clear() {
        this.levels.clear();
        this.tilemaps.clear();
        this.layers.clear();
        this.objects.clear();
        this.currentLevelId = null;
    }
}
