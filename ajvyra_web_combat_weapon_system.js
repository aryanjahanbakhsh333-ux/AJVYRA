class AJVYRAWebCombatWeapon {
    constructor(data = {}) {
        this.id = String(data.id || "");
        this.name = String(data.name || "Weapon");

        this.type = String(
            data.type || "melee"
        );

        this.power = Math.max(
            0,
            Number(data.power) || 10
        );

        this.range = Math.max(
            0,
            Number(data.range) || 1
        );

        this.cooldown = Math.max(
            0,
            Number(data.cooldown) || 500
        );

        this.multiplier = Math.max(
            0,
            Number(data.multiplier) || 1
        );

        this.criticalChance = Math.max(
            0,
            Math.min(1, Number(data.criticalChance) || 0)
        );

        this.criticalMultiplier = Math.max(
            1,
            Number(data.criticalMultiplier) || 1.5
        );

        this.penetration = Math.max(
            0,
            Math.min(1, Number(data.penetration) || 0)
        );

        this.ammoType = data.ammoType || null;
        this.ammoCost = Math.max(
            0,
            Number(data.ammoCost) || 0
        );

        this.metadata = data.metadata || {};
    }
}


class AJVYRAWebCombatWeaponSystem {
    constructor() {
        this.weapons = new Map();
        this.cooldowns = new Map();
    }

    registerWeapon(data) {
        const weapon =
            data instanceof AJVYRAWebCombatWeapon
                ? data
                : new AJVYRAWebCombatWeapon(data);

        if (!weapon.id) {
            return null;
        }

        this.weapons.set(weapon.id, weapon);

        return weapon;
    }

    getWeapon(id) {
        return this.weapons.get(String(id)) || null;
    }

    canUse(entityId, weaponId, now = Date.now()) {
        const key =
            `${String(entityId)}:${String(weaponId)}`;

        const readyAt =
            Number(this.cooldowns.get(key)) || 0;

        return now >= readyAt;
    }

    use(entityId, weaponId, now = Date.now()) {
        const weapon = this.getWeapon(weaponId);

        if (!weapon) {
            return {
                success: false,
                reason: "weapon_not_found"
            };
        }

        if (!this.canUse(entityId, weaponId, now)) {
            return {
                success: false,
                reason: "cooldown"
            };
        }

        const key =
            `${String(entityId)}:${String(weaponId)}`;

        this.cooldowns.set(
            key,
            now + weapon.cooldown
        );

        return {
            success: true,
            weapon
        };
    }

    clearEntity(entityId) {
        const prefix = `${String(entityId)}:`;

        for (const key of this.cooldowns.keys()) {
            if (key.startsWith(prefix)) {
                this.cooldowns.delete(key);
            }
        }
    }
}
