"use strict";

class AJVYRAHitbox {
    constructor(options = {}) {
        this.id =
            String(options.id || "hitbox");

        this.ownerId =
            String(options.ownerId || "");

        this.x =
            Number(options.x || 0);

        this.y =
            Number(options.y || 0);

        this.width =
            Math.max(
                1,
                Number(options.width || 20)
            );

        this.height =
            Math.max(
                1,
                Number(options.height || 20)
            );

        this.damage =
            Math.max(
                0,
                Number(options.damage || 0)
            );

        this.active =
            options.active !== false;

        this.team =
            String(options.team || "neutral");

        this.oncePerTarget =
            options.oncePerTarget === true;

        this.hitTargets = new Set();
    }

    setPosition(x, y) {
        this.x = Number(x) || 0;
        this.y = Number(y) || 0;
    }

    reset() {
        this.hitTargets.clear();
    }

    canHit(targetId) {
        if (!this.oncePerTarget) {
            return true;
        }

        return !this.hitTargets.has(targetId);
    }

    registerHit(targetId) {
        if (this.oncePerTarget) {
            this.hitTargets.add(targetId);
        }
    }
}


class AJVYRAHurtbox {
    constructor(options = {}) {
        this.id =
            String(options.id || "hurtbox");

        this.ownerId =
            String(options.ownerId || "");

        this.x =
            Number(options.x || 0);

        this.y =
            Number(options.y || 0);

        this.width =
            Math.max(
                1,
                Number(options.width || 20)
            );

        this.height =
            Math.max(
                1,
                Number(options.height || 20)
            );

        this.active =
            options.active !== false;

        this.team =
            String(options.team || "neutral");

        this.invulnerable =
            options.invulnerable === true;
    }

    setPosition(x, y) {
        this.x = Number(x) || 0;
        this.y = Number(y) || 0;
    }
}


class AJVYRAHitboxSystem {
    constructor() {
        this.hitboxes = new Map();
        this.hurtboxes = new Map();

        this.listeners = new Set();
    }

    addHitbox(hitbox) {
        if (
            !(hitbox instanceof AJVYRAHitbox)
        ) {
            throw new TypeError(
                "Invalid hitbox."
            );
        }

        this.hitboxes.set(
            hitbox.id,
            hitbox
        );

        return hitbox;
    }

    addHurtbox(hurtbox) {
        if (
            !(hurtbox instanceof AJVYRAHurtbox)
        ) {
            throw new TypeError(
                "Invalid hurtbox."
            );
        }

        this.hurtboxes.set(
            hurtbox.id,
            hurtbox
        );

        return hurtbox;
    }

    removeHitbox(id) {
        this.hitboxes.delete(id);
    }

    removeHurtbox(id) {
        this.hurtboxes.delete(id);
    }

    onHit(callback) {
        if (typeof callback !== "function") {
            throw new TypeError(
                "Hit listener must be a function."
            );
        }

        this.listeners.add(callback);

        return () => {
            this.listeners.delete(callback);
        };
    }

    update() {
        for (const hitbox of this.hitboxes.values()) {
            if (!hitbox.active) {
                continue;
            }

            for (const hurtbox of this.hurtboxes.values()) {
                if (!hurtbox.active) {
                    continue;
                }

                if (
                    hurtbox.invulnerable ||
                    hitbox.ownerId === hurtbox.ownerId
                ) {
                    continue;
                }

                if (
                    hitbox.team !== "neutral" &&
                    hurtbox.team !== "neutral" &&
                    hitbox.team === hurtbox.team
                ) {
                    continue;
                }

                if (!AJVYRAWebCollisionSystem.rectRect(
                    hitbox,
                    hurtbox
                )) {
                    continue;
                }

                if (
                    !hitbox.canHit(
                        hurtbox.ownerId
                    )
                ) {
                    continue;
                }

                hitbox.registerHit(
                    hurtbox.ownerId
                );

                const event = {
                    hitbox,
                    hurtbox,
                    damage: hitbox.damage,
                    sourceId: hitbox.ownerId,
                    targetId: hurtbox.ownerId,
                };

                for (const listener of this.listeners) {
                    listener(event);
                }
            }
        }
    }

    clear() {
        this.hitboxes.clear();
        this.hurtboxes.clear();
        this.listeners.clear();
    }
}


window.AJVYRAHitbox =
    AJVYRAHitbox;

window.AJVYRAHurtbox =
    AJVYRAHurtbox;

window.AJVYRAHitboxSystem =
    AJVYRAHitboxSystem;
