"use strict";

class AJVYRAWebGameEntityManager {
    constructor() {
        this.entities = new Map();

        this.aiControllers = new Map();

        this.spawnedEntities = 0;
    }

    add(entity) {
        if (!entity?.id) {
            throw new TypeError(
                "Entity must have an id."
            );
        }

        if (
            this.entities.has(entity.id)
        ) {
            throw new Error(
                `Entity already exists: ${entity.id}`
            );
        }

        this.entities.set(
            entity.id,
            entity
        );

        this.spawnedEntities += 1;

        return entity;
    }

    remove(entityId) {
        this.aiControllers.delete(
            entityId
        );

        return this.entities.delete(
            entityId
        );
    }

    get(entityId) {
        return this.entities.get(
            entityId
        ) || null;
    }

    addAI(entityId, ai) {
        if (!this.entities.has(entityId)) {
            throw new Error(
                `Cannot attach AI. Entity not found: ${entityId}`
            );
        }

        if (
            !ai ||
            typeof ai.update !== "function"
        ) {
            throw new TypeError(
                "AI controller must expose update()."
            );
        }

        this.aiControllers.set(
            entityId,
            ai
        );

        return ai;
    }

    update(delta) {
        for (
            const entity
            of this.entities.values()
        ) {
            if (
                typeof entity.update ===
                "function"
            ) {
                entity.update(delta);
            }
        }

        for (
            const [
                entityId,
                ai
            ]
            of this.aiControllers.entries()
        ) {
            const entity =
                this.entities.get(
                    entityId
                );

            if (!entity) {
                this.aiControllers.delete(
                    entityId
                );

                continue;
            }

            ai.update(delta);
        }
    }

    findByTeam(team) {
        const result = [];

        for (
            const entity
            of this.entities.values()
        ) {
            if (entity.team === team) {
                result.push(entity);
            }
        }

        return result;
    }

    findNearest(
        source,
        filter = () => true
    ) {
        let nearest = null;
        let nearestDistance = Infinity;

        for (
            const entity
            of this.entities.values()
        ) {
            if (
                entity === source ||
                !filter(entity)
            ) {
                continue;
            }

            if (
                typeof source.distanceTo !==
                "function"
            ) {
                continue;
            }

            const distance =
                source.distanceTo(entity);

            if (
                distance < nearestDistance
            ) {
                nearestDistance = distance;
                nearest = entity;
            }
        }

        return nearest;
    }

    getAliveEntities() {
        const result = [];

        for (
            const entity
            of this.entities.values()
        ) {
            if (
                typeof entity.isAlive ===
                    "function" &&
                entity.isAlive()
            ) {
                result.push(entity);
            }
        }

        return result;
    }

    getSnapshot() {
        return {
            entityCount:
                this.entities.size,

            aiCount:
                this.aiControllers.size,

            spawnedEntities:
                this.spawnedEntities,

            aliveEntities:
                this.getAliveEntities().length
        };
    }

    clear() {
        this.entities.clear();
        this.aiControllers.clear();
    }
}

window.AJVYRAWebGameEntityManager =
    AJVYRAWebGameEntityManager;
