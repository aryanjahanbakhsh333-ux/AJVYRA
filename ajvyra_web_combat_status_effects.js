class AJVYRAWebCombatStatusEffect {
    constructor(data = {}) {
        this.id = String(data.id || "");
        this.type = String(data.type || "generic");

        this.duration = Math.max(
            0,
            Number(data.duration) || 0
        );

        this.remaining = this.duration;

        this.interval = Math.max(
            0,
            Number(data.interval) || 1000
        );

        this.elapsed = 0;

        this.power = Number(data.power) || 0;
        this.stacks = Math.max(
            1,
            Number(data.stacks) || 1
        );

        this.metadata = data.metadata || {};
    }

    update(delta, target) {
        this.remaining = Math.max(
            0,
            this.remaining - delta
        );

        this.elapsed += delta;

        let triggered = false;

        while (this.elapsed >= this.interval && this.interval > 0) {
            this.elapsed -= this.interval;
            triggered = true;

            this.applyTick(target);
        }

        return {
            expired: this.remaining <= 0,
            triggered
        };
    }

    applyTick(target) {
        if (!target) {
            return;
        }

        if (
            this.type === "poison" ||
            this.type === "burn"
        ) {
            if (typeof target.takeDamage === "function") {
                target.takeDamage(this.power);
            }
        }

        if (this.type === "heal") {
            if (typeof target.heal === "function") {
                target.heal(this.power);
            }
        }

        if (this.type === "stun") {
            target.combatStunned = true;
        }
    }
}


class AJVYRAWebCombatStatusManager {
    constructor() {
        this.effects = new Map();
    }

    apply(targetId, effectData) {
        const id = String(targetId);

        if (!this.effects.has(id)) {
            this.effects.set(id, []);
        }

        const effect =
            effectData instanceof AJVYRAWebCombatStatusEffect
                ? effectData
                : new AJVYRAWebCombatStatusEffect(effectData);

        this.effects.get(id).push(effect);

        return effect;
    }

    update(targetId, delta, target) {
        const id = String(targetId);
        const effects = this.effects.get(id) || [];

        const remaining = [];

        for (const effect of effects) {
            const result = effect.update(
                Math.max(0, Number(delta) || 0),
                target
            );

            if (!result.expired) {
                remaining.push(effect);
            }
        }

        this.effects.set(id, remaining);

        return remaining;
    }

    clear(targetId) {
        this.effects.delete(String(targetId));
    }

    get(targetId) {
        return [
            ...(this.effects.get(String(targetId)) || [])
        ];
    }
}
